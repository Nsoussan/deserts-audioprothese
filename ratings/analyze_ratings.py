"""Analyse descriptive : notes Google des centres d'audioprothèse selon la concurrence locale.
Entrées : sample_3000.csv (échantillon stratifié, poids), places_raw.jsonl (collecte Places).
Sorties : outputs/ratings_*.csv (tables), outputs/fig_*.png (figures), outputs/summary.txt.
"""
import json, os, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
os.makedirs("outputs", exist_ok=True)

s = pd.read_csv("sample_3000.csv", dtype={"code_insee":str,"code_postal":str,"siret":str})
rows=[]
for line in open("places_raw.jsonl", encoding="utf-8"):
    rec=json.loads(line); b=rec.get("best") or {}
    rows.append({"site_id":rec["site_id"], "collected": True, "api_error": "error" in rec["raw"], **b})
m = pd.DataFrame(rows).drop_duplicates("site_id", keep="last")
d = s.merge(m, on="site_id", how="left")
d = d[d["collected"]==True].copy()
# Validation de l'appariement
NONSTORE = {"local_government_office","hospital","dental_clinic","dentist","general_hospital","association_or_organization","corporate_office","medical_clinic","health"}
d["match_ok"] = d["place_id"].notna() & (d["dist_centroide_km"].fillna(99) <= 10) & ~d["primary_type"].isin(NONSTORE) & (d["name_match"].fillna(False) | d["primary_type"].isin({"store","electronics_store","doctor","medical_supply_store"}))
d["found"] = d["place_id"].notna()
d["has_rating"] = d["match_ok"] & d["user_rating_count"].fillna(0).gt(0)
d["n_reviews"] = np.where(d["match_ok"], d["user_rating_count"].fillna(0), np.nan)
d["rating_v"] = np.where(d["has_rating"], d["rating"], np.nan)
d["has_website"] = np.where(d["match_ok"], d["website"].notna(), np.nan)
d["bande10"] = pd.Categorical(d["bande10"].astype(str), ["0","1-2","3-9","10+"], ordered=True)
d["type"] = pd.Categorical(d["type"], ["enseigne nationale","mutualiste","indépendant"])
d["log_pop"] = np.log(d["population_2023"].clip(lower=1))
d["optique"] = d["groupe"].isin(["Optical Center","Krys Audition","Alain Afflelou Acousticien","Atol","Optic 2000","Lissac","Generale d'Optique","Acuitis"])

def wmean(x, w):
    x = np.asarray(x, float); w = np.asarray(w, float); k = ~np.isnan(x)
    return (x[k]*w[k]).sum()/w[k].sum() if w[k].sum()>0 else np.nan
def wq(x, w, q=0.5):
    x = np.asarray(x, float); w = np.asarray(w, float); k = ~np.isnan(x); x, w = x[k], w[k]
    if len(x)==0: return np.nan
    o = np.argsort(x); x, w = x[o], w[o]; c = np.cumsum(w)/w.sum()
    return x[np.searchsorted(c, q)]

def table(g):
    n = len(g); ok = g["match_ok"].sum()
    return pd.Series({"n": n, "n_apparies": ok, "part_trouves_google": wmean(g["found"], g["poids"]),
        "part_appariement_valide": wmean(g["match_ok"], g["poids"]),
        "part_avec_avis": wmean(g.loc[g["match_ok"],"has_rating"], g.loc[g["match_ok"],"poids"]),
        "avis_median": wq(g["n_reviews"], g["poids"]), "avis_moyen": wmean(g["n_reviews"], g["poids"]),
        "note_moyenne": wmean(g["rating_v"], g["poids"]), "note_ecart_type": np.sqrt(wmean((g["rating_v"]-wmean(g["rating_v"],g["poids"]))**2, g["poids"])),
        "part_note_5": wmean(np.where(g["has_rating"], (g["rating_v"]>=4.95).astype(float), np.nan), g["poids"]),
        "part_site_web": wmean(g["has_website"], g["poids"])})

t_band = d.groupby("bande10", observed=True).apply(table)
t_type = d.groupby("type", observed=True).apply(table)
t_cross = d.groupby(["bande10","type"], observed=True).apply(table)
t_band.to_csv("outputs/ratings_par_bande.csv"); t_type.to_csv("outputs/ratings_par_type.csv"); t_cross.to_csv("outputs/ratings_bande_x_type.csv")

# Tests : notes et volume d'avis selon la bande (Kruskal-Wallis, non pondéré) ; corrélations de rang avec l'APL
ok = d[d["match_ok"]].copy()
kw_rating = stats.kruskal(*[g["rating_v"].dropna() for _,g in ok.groupby("bande10", observed=True)])
kw_reviews = stats.kruskal(*[g["n_reviews"].dropna() for _,g in ok.groupby("bande10", observed=True)])
rho_apl_reviews = stats.spearmanr(ok["apl"], ok["n_reviews"], nan_policy="omit")
rho_apl_rating = stats.spearmanr(ok.loc[ok["has_rating"],"apl"], ok.loc[ok["has_rating"],"rating_v"], nan_policy="omit")
rho_c10_reviews = stats.spearmanr(ok["concurrents_10km"], ok["n_reviews"], nan_policy="omit")

# Régressions descriptives (WLS avec poids de sondage, erreurs robustes)
def wls(y, X, w):
    X = sm.add_constant(X.astype(float)); k = y.notna() & X.notna().all(axis=1)
    return sm.WLS(y[k].astype(float), X[k], weights=w[k]).fit(cov_type="HC1")
dd = ok.copy()
Xb = pd.get_dummies(dd[["bande10","type"]], drop_first=True).astype(float)
Xb["log_pop"] = dd["log_pop"]; Xb["revenu_k"] = dd["revenu_median_uc"]/1000; Xb["optique"] = dd["optique"].astype(float)
r_reviews = wls(np.log1p(dd["n_reviews"]), Xb, dd["poids"])
r_rating = wls(dd["rating_v"], Xb, dd["poids"])
r_site = wls(dd["has_website"].astype(float), Xb, dd["poids"])
r_hasr = wls(dd["has_rating"].astype(float), Xb, dd["poids"])

with open("outputs/summary.txt","w") as f:
    f.write(f"Sites collectés : {len(d)} · trouvés sur Google : {int(d['found'].sum())} · appariements valides : {int(d['match_ok'].sum())}\n")
    f.write(f"Parmi les appariés : avec au moins un avis : {int(d['has_rating'].sum())} ({d['has_rating'].sum()/d['match_ok'].sum():.1%})\n\n")
    f.write("Par bande de concurrence (10 km), pondéré :\n" + t_band.round(3).to_string() + "\n\n")
    f.write("Par type, pondéré :\n" + t_type.round(3).to_string() + "\n\n")
    f.write("Bande x type, pondéré :\n" + t_cross.round(3).to_string() + "\n\n")
    f.write(f"Kruskal-Wallis note ~ bande : H={kw_rating.statistic:.2f}, p={kw_rating.pvalue:.3g}\n")
    f.write(f"Kruskal-Wallis nb avis ~ bande : H={kw_reviews.statistic:.2f}, p={kw_reviews.pvalue:.3g}\n")
    f.write(f"Spearman APL ~ nb avis : rho={rho_apl_reviews.statistic:.3f}, p={rho_apl_reviews.pvalue:.3g}\n")
    f.write(f"Spearman APL ~ note : rho={rho_apl_rating.statistic:.3f}, p={rho_apl_rating.pvalue:.3g}\n")
    f.write(f"Spearman concurrents 10 km ~ nb avis : rho={rho_c10_reviews.statistic:.3f}, p={rho_c10_reviews.pvalue:.3g}\n\n")
    for name, r in [("log(1+nb avis)", r_reviews), ("note (si >=1 avis)", r_rating), ("a un site web", r_site), ("a au moins un avis", r_hasr)]:
        f.write(f"=== WLS {name} (poids de sondage, HC1) · n={int(r.nobs)} · R2={r.rsquared:.3f}\n")
        f.write(pd.DataFrame({"coef": r.params, "se": r.bse, "p": r.pvalues}).round(3).to_string() + "\n\n")
print(open("outputs/summary.txt").read())

# Figures : deux panneaux chacune, chaînes vs indépendants (+ ensemble), IC bootstrap à 95 % (pondéré)
COL = {"enseigne nationale":"#2a78d6", "indépendant":"#1baf7a", "tous":"#6b6b6b"}
MK = {"enseigne nationale":"o", "indépendant":"^", "tous":"s"}
LAB = {"enseigne nationale":"National chains", "indépendant":"Independents", "tous":"All sites"}
bands = ["0","1-2","3-9","10+"]; xl = ["0", "1–2", "3–9", "10+"]
rng = np.random.default_rng(1)
def boot(x, w, fn, B=500):
    x = np.asarray(x, float); w = np.asarray(w, float); k = ~np.isnan(x); x, w = x[k], w[k]
    if len(x) < 5: return (np.nan, np.nan, np.nan)
    p = w / w.sum(); est = fn(x, w)
    bs = [fn(x[i], w[i]) for i in (rng.choice(len(x), len(x), p=p) for _ in range(B))]
    return est, np.nanpercentile(bs, 2.5), np.nanpercentile(bs, 97.5)
def series(metric_col, fn, sub):
    out = []
    for b in bands:
        g = sub[sub["bande10"]==b]
        out.append(boot(g[metric_col], g["poids"], fn))
    return np.array(out)
def panel(ax, metric_col, fn, ylabel, title, pct=False, groups=("enseigne nationale","indépendant","tous")):
    for j, t in enumerate(groups):
        sub = ok if t=="tous" else ok[ok["type"]==t]
        v = series(metric_col, fn, sub); y, lo, hi = v[:,0], v[:,1], v[:,2]
        if pct: y, lo, hi = y*100, lo*100, hi*100
        xs = np.arange(4) + (j-1)*0.06
        ax.errorbar(xs, y, yerr=[y-lo, hi-y], fmt=MK[t]+"-", color=COL[t], lw=1.8, ms=6, capsize=2.5, label=LAB[t])
    ax.set_xticks(range(4)); ax.set_xticklabels(xl); ax.set_ylabel(ylabel); ax.set_title(title, fontsize=10.5, loc="left")
    ax.grid(axis="y", color="#e5e5e5", lw=0.8); ax.spines[["top","right"]].set_visible(False)
wmed = lambda x, w: wq(x, w, 0.5)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
panel(axes[0], "n_reviews", wmed, "Median number of Google reviews", "A. Review volume rises with local competition")
panel(axes[1], "has_rating", wmean, "Sites with at least one review (%)", "B. Share of sites with at least one review", pct=True)
axes[0].legend(frameon=False, fontsize=9)
for ax in axes: ax.set_xlabel("Competing hearing-aid sites within 10 km (straight line)")
plt.tight_layout(); plt.savefig("outputs/fig1_review_activity.png", dpi=220); plt.close()
ok["perfect5"] = np.where(ok["has_rating"], (ok["rating_v"]>=4.95).astype(float), np.nan)
wsd = lambda x, w: np.sqrt(wmean((x - wmean(x, w))**2, w))
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
panel(axes[0], "rating_v", wmean, "Mean Google rating (sites with ≥1 review)", "A. Rating level is close to the ceiling everywhere")
axes[0].set_ylim(4.4, 5.0)
ok_all = ok; ok = ok_all[ok_all["n_reviews"]>=30].copy()
panel(axes[1], "rating_v", wsd, "Std. dev. of ratings across sites (≥30 reviews)", "B. Ratings are more compressed where there is no alternative")
ok = ok_all
axes[0].legend(frameon=False, fontsize=9)
for ax in axes: ax.set_xlabel("Competing hearing-aid sites within 10 km (straight line)")
plt.tight_layout(); plt.savefig("outputs/fig2_rating_content.png", dpi=220); plt.close()
# Tables complémentaires : part de 5,0 et dispersion selon le seuil d'avis
rows=[]
for thr in (1,10,30):
    sub = ok[ok["n_reviews"]>=thr]
    for b,g in sub.groupby("bande10", observed=True):
        rows.append({"seuil_avis":thr,"bande10":b,"n":len(g),"part_5.0":wmean(g["perfect5"],g["poids"]),"note_moyenne":wmean(g["rating_v"],g["poids"]),"sd_notes":wsd(g["rating_v"],g["poids"]),"part_inf_4.5":wmean((g["rating_v"]<4.5).astype(float),g["poids"])})
pd.DataFrame(rows).round(3).to_csv("outputs/ratings_distribution_par_seuil.csv", index=False)
Xp = pd.get_dummies(ok[["bande10","type"]], drop_first=True).astype(float); Xp["log_reviews"]=np.log(ok["n_reviews"].clip(lower=1)); Xp["log_pop"]=ok["log_pop"]; Xp["optique"]=ok["optique"].astype(float)
r_p5 = wls(ok["perfect5"], Xp, ok["poids"])
with open("outputs/summary.txt","a") as f:
    f.write(f"=== WLS note = 5,0 (si >=1 avis) ~ bande + type + log(avis) + log(pop) + optique · n={int(r_p5.nobs)} · R2={r_p5.rsquared:.3f}\n")
    f.write(pd.DataFrame({"coef": r_p5.params, "se": r_p5.bse, "p": r_p5.pvalues}).round(3).to_string() + "\n\n")
    f.write("Distribution des notes selon le seuil d'avis :\n" + pd.DataFrame(rows).round(3).to_string() + "\n")
# Nb d'avis médian conditionnel à la présence d'avis, par bande (pour la note)
t_rated = ok[ok["has_rating"]].groupby("bande10", observed=True).apply(lambda g: pd.Series({"avis_median_si_note": wq(g["n_reviews"], g["poids"]), "avis_q25": wq(g["n_reviews"], g["poids"], .25), "avis_q75": wq(g["n_reviews"], g["poids"], .75)}))
t_rated.to_csv("outputs/ratings_avis_conditionnels.csv"); print(t_rated.round(1))
for f in ["fig1_reviews_by_competition.png","fig2_rating_by_competition.png","fig3_share_rated_by_competition.png","fig4_website_by_competition.png"]:
    p = "outputs/"+f
    if os.path.exists(p): os.remove(p)
d.to_csv("outputs/sites_ratings_sample.csv", index=False)
print("figures écrites dans outputs/")
