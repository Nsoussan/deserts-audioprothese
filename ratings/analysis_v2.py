"""Analyse v2 du document de travail : typologie en 5 classes, propriétaire sur site, contrôles de demande, erreurs groupées par commune,
dispersion résiduelle, robustesses. Sorties : outputs/v2/*.csv, outputs/v2/results.txt, figures."""
import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf, os, json, warnings
from scipy import stats
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
os.makedirs("outputs/v2", exist_ok=True)
OUT = open("outputs/v2/results.txt","w")
def W(x=""): OUT.write(str(x)+"\n")

# ---------- données ----------
d = pd.read_csv("outputs/sites_ratings_sample_web.csv", dtype={"code_insee":str,"site_id":str})
smp_all = pd.read_csv("sample_3000.csv", dtype={"code_insee":str,"site_id":str})
missing = smp_all[~smp_all["site_id"].isin(d["site_id"])].copy()
for c in d.columns:
    if c not in missing.columns: missing[c] = np.nan
missing["match_ok"] = False; missing["has_rating"] = 0.0; missing["has_website"] = 0.0; missing["user_rating_count"] = 0.0; missing["site_lu"] = 0.0
d = pd.concat([d, missing[d.columns]], ignore_index=True)
v2 = pd.read_csv("sites_v2.csv", dtype={"code_insee":str,"site_id":str})[["site_id","type5","brand","owner_on_site","pop_10km","pop65_10km","demand65_per_site","apl_v21","dist_concurrent_km","n_titulaires","n_salaries"]]
d = d.drop(columns=[c for c in ["dist_concurrent_km","n_titulaires","n_salaries"] if c in d.columns]).merge(v2, on="site_id", how="left")
d["matched"] = d["match_ok"].fillna(False).astype(bool)
d["log_pop"] = np.nan
d["bande10"] = pd.Categorical(d["bande10"].astype(str), ["0","1-2","3-9","10+"], ordered=True)
d["type5"] = pd.Categorical(d["type5"], ["integrated chain","brand network","optician-hosted","mutualist network","unbranded independent"])
d["rev_missing"] = d["revenu_median_uc"].isna().astype(float)
d["revenu_k"] = d["revenu_median_uc"].fillna(25000)/1000
d["log_pop"] = np.log(d["population_2023"].clip(lower=1)); d["log_pop10"] = np.log(d["pop_10km"].clip(lower=1))
d["log_dem65"] = np.log(d["demand65_per_site"].clip(lower=1)); d["share65"] = d["part_65_plus_pct"].fillna(d["part_65_plus_pct"].median())
d["log_comp"] = np.log1p(d["concurrents_10km"]); d["log_dist"] = np.log1p(d["dist_concurrent_km"].fillna(50))
d["npr"] = d["n_praticiens"].astype(float); d["owner"] = d["owner_on_site"].astype(float)
d["n_reviews0"] = np.where(d["matched"], d["user_rating_count"].fillna(0), 0.0)   # non appariés = 0 avis (borne basse)
d["log_reviews1"] = np.log1p(d["n_reviews"]); d["rated"] = d["has_rating"].astype(float)
d["closed"] = d["business_status"].fillna("").str.contains("CLOSED").astype(float)
ok = d[d["matched"]].copy()
W(f"Échantillon : {len(d)} sites · appariés {len(ok)} · notés {int(ok['rated'].sum())} · communes {ok['code_insee'].nunique()}")
W(f"Revenu manquant (imputé 25 000 €) : {int(ok['rev_missing'].sum())} sites, par bande : {ok.groupby('bande10', observed=True)['rev_missing'].sum().astype(int).to_dict()}")
W(f"Statut Google fermé (CLOSED_*) : {int(ok['closed'].sum())} sites ({ok['closed'].mean():.1%}) ; par bande : {ok.groupby('bande10', observed=True)['closed'].mean().round(3).to_dict()}")

def wmean(x, w):
    x=np.asarray(x,float); w=np.asarray(w,float); k=~np.isnan(x); return (x[k]*w[k]).sum()/w[k].sum() if w[k].sum()>0 else np.nan
def wq(x, w, q=.5):
    x=np.asarray(x,float); w=np.asarray(w,float); k=~np.isnan(x); x,w=x[k],w[k]
    if len(x)==0: return np.nan
    o=np.argsort(x); x,w=x[o],w[o]; c=np.cumsum(w)/w.sum(); return x[np.searchsorted(c,q)]
def wsd(x, w):
    x=np.asarray(x,float); w=np.asarray(w,float); k=~np.isnan(x); x,w=x[k],w[k]
    return np.sqrt(wmean((x-wmean(x,w))**2, w)) if len(x)>1 else np.nan
def wls(y, X, w, groups):
    X = sm.add_constant(X.astype(float)); k = y.notna() & X.notna().all(axis=1)
    return sm.WLS(y[k].astype(float), X[k], weights=w[k]).fit(cov_type="cluster", cov_kwds={"groups": groups[k]})
def tab(r, keep=None):
    t = pd.DataFrame({"coef": r.params, "se": r.bse, "p": r.pvalues})
    return (t.loc[[k for k in keep if k in t.index]] if keep else t).round(3)

# ---------- 1. Statistiques descriptives ----------
W("\n=== 1. Descriptives par type (pondéré) ===")
def desc(g):
    return pd.Series({"n": len(g), "owner_share": wmean(g["owner"], g["poids"]), "practitioners": wmean(g["npr"], g["poids"]),
        "competitors_10km": wmean(g["concurrents_10km"], g["poids"]), "dist_nearest_km": wmean(g["dist_concurrent_km"], g["poids"]),
        "rated": wmean(g["rated"], g["poids"]), "reviews_median": wq(g["n_reviews"], g["poids"]), "reviews_q75": wq(g["n_reviews"], g["poids"], .75),
        "rating_mean": wmean(g["rating_v"], g["poids"]), "website": wmean(g["has_website"], g["poids"]),
        "pop_commune": wmean(g["population_2023"], g["poids"]), "income_k": wmean(g["revenu_k"], g["poids"]), "apl": wmean(g["apl_v21"], g["poids"])})
t = ok.groupby("type5", observed=True).apply(desc); t.loc["all"] = desc(ok); W(t.round(2).to_string()); t.to_csv("outputs/v2/desc_by_type.csv")
t = ok.groupby("bande10", observed=True).apply(desc); W(t.round(2).to_string()); t.to_csv("outputs/v2/desc_by_band.csv")
W("\nBande x type5 (n, part notée, avis médian, note) :")
t = ok.groupby(["bande10","type5"], observed=True).apply(lambda g: pd.Series({"n":len(g),"rated":wmean(g["rated"],g["poids"]),"reviews_median":wq(g["n_reviews"],g["poids"]),"rating":wmean(g["rating_v"],g["poids"])}))
W(t.round(3).to_string()); t.to_csv("outputs/v2/band_x_type5.csv")
W("\nPart de propriétaires sur site par bande : " + ok.groupby("bande10", observed=True).apply(lambda g: round(wmean(g["owner"],g["poids"]),3)).to_dict().__str__())

# ---------- 2. Activité ----------
W("\n=== 2. Activité de notation (erreurs groupées par commune) ===")
def X_base(df, extra=()):
    X = pd.get_dummies(df[["bande10","type5"]], drop_first=True).astype(float)
    X["owner"] = df["owner"]; X["npr"] = df["npr"]; X["log_pop"] = df["log_pop"]; X["revenu_k"] = df["revenu_k"]; X["rev_missing"] = df["rev_missing"]
    for e in extra: X[e] = df[e]
    return X
KEEP = ["bande10_1-2","bande10_3-9","bande10_10+","type5_brand network","type5_optician-hosted","type5_mutualist network","type5_unbranded independent","owner","npr","log_pop","log_dem65","share65","revenu_k","log_comp","log_dist"]
specs = {"A. base": (), "B. + demande 65+ par site, part 65+": ("log_dem65","share65")}
res_act = {}
for name, extra in specs.items():
    X = X_base(ok, extra)
    for y, lab in [("log_reviews1","log(1+avis)"),("rated","noté (LPM)"),("rating_v","note (notés)")]:
        r = wls(ok[y], X, ok["poids"], ok["code_insee"]); res_act[(name,lab)] = r
        W(f"\n[{name}] {lab} · n={int(r.nobs)} · R2={r.rsquared:.3f}"); W(tab(r, KEEP).to_string())
# Poisson (PPML) sur le nombre d'avis
X = sm.add_constant(X_base(ok, ("log_dem65","share65")).astype(float).drop(columns=["rev_missing"]))
try:
    pp = sm.GLM(ok["n_reviews"].astype(float), X, family=sm.families.Poisson(), var_weights=ok["poids"]).fit(cov_type="cluster", cov_kwds={"groups": ok["code_insee"]})
    W("\n[PPML] nombre d'avis ~ spec B"); W(tab(pp, KEEP).to_string())
except Exception as e: W(f"PPML échec : {e}")
# Logit sur noté
try:
    lg = sm.GLM(ok["rated"], X, family=sm.families.Binomial(), var_weights=ok["poids"]).fit(cov_type="cluster", cov_kwds={"groups": ok["code_insee"]})
    W("\n[Logit] noté ~ spec B (coefficients log-odds)"); W(tab(lg, KEEP).to_string())
except Exception as e: W(f"Logit échec : {e}")
# Concurrence continue
X = X_base(ok, ("log_dem65","share65")); X = X.drop(columns=[c for c in X.columns if c.startswith("bande10_")]); X["log_comp"] = ok["log_comp"]; X["log_dist"] = ok["log_dist"]
r = wls(ok["log_reviews1"], X, ok["poids"], ok["code_insee"]); W("\n[continu] log(1+avis) ~ log(1+concurrents 10 km) + log(1+distance au plus proche) + contrôles B"); W(tab(r, KEEP).to_string())
# Alternatives distinctes (spec B)
Xa = X_base(ok, ("log_dem65","share65")).drop(columns=["bande10_1-2","bande10_3-9","bande10_10+"])
Xa = pd.concat([Xa, pd.get_dummies(pd.Categorical(ok["bande_alt10"].astype(str), ["0","1-2","3-9","10+"]), prefix="alt", drop_first=True).astype(float)], axis=1)
r = wls(ok["log_reviews1"], Xa, ok["poids"], ok["code_insee"]); W("\n[alternatives distinctes, spec B] log(1+avis)"); W(tab(r, ["alt_1-2","alt_3-9","alt_10+"]).to_string())
W(f"sites déplacés de bande (alternatives vs sites) : {int((ok['bande_alt10'].astype(str)!=ok['bande10'].astype(str)).sum())}")
# Non appariés = 0 avis
dd = d.copy(); dd["rated0"] = (dd["n_reviews0"]>0).astype(float); X = X_base(dd, ("log_dem65","share65"))
r = wls(dd["rated0"], X, dd["poids"], dd["code_insee"]); W(f"\n[robustesse] noté, non appariés recodés à 0 avis · n={int(r.nobs)}"); W(tab(r, ["bande10_1-2","bande10_3-9","bande10_10+"]).to_string())
W("part notée par bande, non appariés à 0 : " + dd.groupby("bande10", observed=True).apply(lambda g: round(wmean(g["rated0"], g["poids"]),3)).to_dict().__str__())
# Interaction bande x type (Wald)
X = X_base(ok, ("log_dem65","share65")); Xi = X.copy()
for b in ["bande10_1-2","bande10_3-9","bande10_10+"]:
    Xi[b+"_x_indep"] = X[b]*X["type5_unbranded independent"]
r = wls(ok["log_reviews1"], Xi, ok["poids"], ok["code_insee"]); wt = r.wald_test([c for c in Xi.columns if c.endswith("_x_indep")], scalar=True)
W(f"\n[interaction bande x indépendant] log(1+avis) : Wald p = {float(wt.pvalue):.3f} ; coefs " + tab(r, [c for c in Xi.columns if c.endswith('_x_indep')]).to_string())
# Sans opticiens
o2 = ok[ok["type5"]!="optician-hosted"]; X = X_base(o2, ("log_dem65","share65")).drop(columns=["type5_optician-hosted"])
r = wls(o2["log_reviews1"], X, o2["poids"], o2["code_insee"]); W(f"\n[sans opticiens] log(1+avis) · n={int(r.nobs)}"); W(tab(r, ["bande10_1-2","bande10_3-9","bande10_10+","owner","type5_unbranded independent"]).to_string())
W("\nKruskal-Wallis (non pondéré) avis ~ bande : H=%.1f p=%.2g ; note ~ bande : H=%.1f p=%.2g" % (*stats.kruskal(*[g["n_reviews"].dropna() for _,g in ok.groupby("bande10", observed=True)]), *stats.kruskal(*[g["rating_v"].dropna() for _,g in ok.groupby("bande10", observed=True)])))

# ---------- 3. Contenu : niveau conditionnel ----------
W("\n=== 3. Niveau des notes selon le seuil d'avis, avec et sans contrôle de log(avis) ===")
rows=[]
for thr in (1,10,30):
    sub = ok[ok["n_reviews"]>=thr]
    for ctrl in (False, True):
        X = X_base(sub, ("log_dem65","share65"))
        if ctrl: X["log_reviews"] = np.log(sub["n_reviews"])
        r = wls(sub["rating_v"], X, sub["poids"], sub["code_insee"])
        rows.append({"seuil": thr, "ctrl_log_avis": ctrl, "n": int(r.nobs), **{b: f"{r.params[b]:+.3f} ({r.pvalues[b]:.2f})" for b in ["bande10_1-2","bande10_3-9","bande10_10+"]}, "owner": f"{r.params['owner']:+.3f} ({r.pvalues['owner']:.2f})", "indep": f"{r.params['type5_unbranded independent']:+.3f} ({r.pvalues['type5_unbranded independent']:.2f})", "log_avis": (f"{r.params['log_reviews']:+.3f} ({r.pvalues['log_reviews']:.2f})" if ctrl else "")})
t = pd.DataFrame(rows); W(t.to_string(index=False)); t.to_csv("outputs/v2/rating_level_by_threshold.csv", index=False)
W("\nMoyenne des notes pondérée par le nombre d'avis, par bande : " + ok[ok["rated"]==1].groupby("bande10", observed=True).apply(lambda g: round(np.average(g["rating_v"], weights=g["poids"]*g["n_reviews"]),3)).to_dict().__str__())

# ---------- 4. Dispersion ----------
W("\n=== 4. Dispersion des notes entre sites ===")
rated = ok[ok["rated"]==1].copy()
rated["bin"] = pd.cut(rated["n_reviews"], [0,4,9,19,49,1e9], labels=["1-4","5-9","10-19","20-49","50+"])
t = rated.groupby(["bin","bande10"], observed=True).apply(lambda g: pd.Series({"n":len(g),"sd":wsd(g["rating_v"],g["poids"]),"mean":wmean(g["rating_v"],g["poids"]),"below45":wmean((g["rating_v"]<4.5).astype(float),g["poids"])})).unstack("bande10")
W("SD (et n) par tranche d'avis x bande :"); W(t.round(3).to_string()); t.to_csv("outputs/v2/sd_by_bin_band.csv")
# Dispersion résiduelle : note ~ log(avis) x bande + type5 + owner + opticien
rated["lr"] = np.log(rated["n_reviews"])
m = smf.wls("rating_v ~ lr*C(bande10) + C(type5) + owner + npr", data=rated, weights=rated["poids"]).fit()
rated["resid"] = m.resid
t = rated.groupby("bande10", observed=True).apply(lambda g: pd.Series({"n":len(g),"resid_sd":wsd(g["resid"],g["poids"]),"resid_iqr": wq(g["resid"],g["poids"],.75)-wq(g["resid"],g["poids"],.25)}))
W("\nDispersion résiduelle (note ~ log avis x bande + type + propriétaire + praticiens) :"); W(t.round(3).to_string()); t.to_csv("outputs/v2/resid_dispersion.csv")
bf = stats.levene(*[g["resid"].values for _,g in rated.groupby("bande10", observed=True)], center="median"); W(f"Brown-Forsythe sur résidus (4 bandes) : W={bf.statistic:.2f}, p={bf.pvalue:.3g}")
bf2 = stats.levene(rated.loc[rated["bande10"].isin(["0","1-2"]),"resid"], rated.loc[rated["bande10"].isin(["3-9","10+"]),"resid"], center="median"); W(f"Brown-Forsythe ≤2 vs ≥3 concurrents : W={bf2.statistic:.2f}, p={bf2.pvalue:.3g}")
# bootstrap par grappes (communes) de l'écart-type résiduel par bande
rng = np.random.default_rng(7); communes = rated["code_insee"].unique(); B=300; boots={b:[] for b in ["0","1-2","3-9","10+"]}
grp = {c: g for c, g in rated.groupby("code_insee")}
for _ in range(B):
    samp = pd.concat([grp[c] for c in rng.choice(communes, len(communes))])
    for b in boots: g = samp[samp["bande10"]==b]; boots[b].append(wsd(g["resid"], g["poids"]))
ci = {b: (round(np.percentile(v,2.5),3), round(np.percentile(v,97.5),3)) for b,v in boots.items()}; W(f"IC 95 % bootstrap par communes de l'écart-type résiduel : {ci}")
# quartile supérieur d'avis au sein de chaque bande
q = rated.groupby("bande10", observed=True)["n_reviews"].transform(lambda x: x.quantile(.75)); top = rated[rated["n_reviews"]>=q]
t = top.groupby("bande10", observed=True).apply(lambda g: pd.Series({"n":len(g),"min_reviews":g["n_reviews"].min(),"sd":wsd(g["rating_v"],g["poids"]),"mean":wmean(g["rating_v"],g["poids"]),"below45":wmean((g["rating_v"]<4.5).astype(float),g["poids"])}))
W("\nQuart supérieur d'avis au sein de chaque bande :"); W(t.round(3).to_string()); t.to_csv("outputs/v2/top_quartile_dispersion.csv")
lv = stats.levene(top.loc[top["bande10"].isin(["0","1-2"]),"rating_v"], top.loc[top["bande10"].isin(["3-9","10+"]),"rating_v"], center="median"); W(f"Brown-Forsythe quart supérieur, ≤2 vs ≥3 concurrents : W={lv.statistic:.2f}, p={lv.pvalue:.3g}")
lv4 = stats.levene(*[g["rating_v"].values for _,g in top.groupby("bande10", observed=True)], center="median"); W(f"Brown-Forsythe quart supérieur, 4 bandes : W={lv4.statistic:.2f}, p={lv4.pvalue:.3g}")
ft = stats.fisher_exact([[int((top.loc[top["bande10"].isin(["0","1-2"]),"rating_v"]<4.5).sum()), int((top.loc[top["bande10"].isin(["0","1-2"]),"rating_v"]>=4.5).sum())],[int((top.loc[top["bande10"].isin(["3-9","10+"]),"rating_v"]<4.5).sum()), int((top.loc[top["bande10"].isin(["3-9","10+"]),"rating_v"]>=4.5).sum())]]); W(f"Fisher part < 4,5 quart supérieur ≤2 vs ≥3 : p={ft[1]:.3g}")
t50 = rated[rated["n_reviews"]>=50]; lv50 = stats.levene(t50.loc[t50["bande10"].isin(["0","1-2"]),"rating_v"], t50.loc[t50["bande10"].isin(["3-9","10+"]),"rating_v"], center="median"); W(f"Brown-Forsythe ≥50 avis, ≤2 vs ≥3 : W={lv50.statistic:.2f}, p={lv50.pvalue:.3g} (n={int((t50['bande10'].isin(['0','1-2'])).sum())} vs {int((t50['bande10'].isin(['3-9','10+'])).sum())})")
# quart supérieur par type (chaînes intégrées / indépendants)
for tp in ["integrated chain","unbranded independent"]:
    tt = top[top["type5"]==tp].groupby("bande10", observed=True).apply(lambda g: pd.Series({"n":len(g),"sd":wsd(g["rating_v"],g["poids"]),"below45":wmean((g["rating_v"]<4.5).astype(float),g["poids"])}))
    W(f"quart supérieur, {tp} :"); W(tt.round(3).to_string())
# même chose sans opticiens
t = rated[rated["type5"]!="optician-hosted"].groupby("bande10", observed=True).apply(lambda g: pd.Series({"n":len(g),"resid_sd":wsd(g["resid"],g["poids"])}))
W("Dispersion résiduelle sans opticiens :"); W(t.round(3).to_string())
# Part de 5,0 avec tranches d'avis
X = pd.get_dummies(rated[["bande10","type5","bin"]], drop_first=True).astype(float); X["owner"]=rated["owner"]; X["log_pop"]=rated["log_pop"]
r = wls((rated["rating_v"]>=4.95).astype(float), X, rated["poids"], rated["code_insee"]); W("\nPart de 5,0 ~ bandes + tranches d'avis + type + propriétaire :"); W(tab(r, ["bande10_1-2","bande10_3-9","bande10_10+","type5_unbranded independent","owner"]).to_string())

# ---------- 5. Effets fixes commune ----------
W("\n=== 5. Effets fixes commune ===")
multi = ok[ok.groupby("code_insee")["site_id"].transform("count")>=2].copy()
W(f"communes à ≥2 sites appariés : {multi['code_insee'].nunique()} · sites : {len(multi)} · composition par bande : {multi['bande10'].value_counts().to_dict()}")
for y, lab in [("log_reviews1","log(1+avis)"),("rated","noté"),("rating_v","note"),("has_website","site web")]:
    m2 = multi[multi[y].notna()].copy(); m2["y"]=m2[y].astype(float)
    r = smf.wls("y ~ owner + C(type5) + npr + C(code_insee)", data=m2, weights=m2["poids"]).fit(cov_type="cluster", cov_kwds={"groups": m2["code_insee"]})
    keys = [k for k in r.params.index if not k.startswith("C(code_insee)")]
    W(f"\nFE commune · {lab} · n={int(r.nobs)}"); W(pd.DataFrame({"coef":r.params[keys],"se":r.bse[keys],"p":r.pvalues[keys]}).round(3).to_string())

# ---------- 6. Revenu, entrants ----------
W("\n=== 6. Revenu (terciles) et entrants ===")
cuts = [wq(ok["revenu_k"], ok["poids"], q) for q in (1/3, 2/3)]; ok["terc"] = pd.cut(ok["revenu_k"], [-np.inf]+cuts+[np.inf], labels=["T1","T2","T3"])
X = X_base(ok, ("log_dem65","share65")).drop(columns=["revenu_k"]); X = pd.concat([X, pd.get_dummies(ok["terc"], prefix="terc", drop_first=True).astype(float)], axis=1)
for y, lab in [("log_reviews1","log(1+avis)"),("rated","noté"),("rating_v","note")]:
    r = wls(ok[y], X, ok["poids"], ok["code_insee"]); W(f"{lab} : T2 {r.params['terc_T2']:+.3f} (p={r.pvalues['terc_T2']:.2f}) · T3 {r.params['terc_T3']:+.3f} (p={r.pvalues['terc_T3']:.2f})")
e = ok[ok["nb_audio_2022_commune"].notna()].copy(); e["entrant"]=e["entrant_commune"].astype(float); X = X_base(e, ("log_dem65","share65")); X["entrant"]=e["entrant"]
for y, lab in [("log_reviews1","log(1+avis)"),("rated","noté"),("rating_v","note")]:
    r = wls(e[y], X, e["poids"], e["code_insee"]); W(f"entrant · {lab} : {r.params['entrant']:+.3f} (se {r.bse['entrant']:.3f}, p={r.pvalues['entrant']:.2f}, IC95 [{r.params['entrant']-1.96*r.bse['entrant']:+.2f};{r.params['entrant']+1.96*r.bse['entrant']:+.2f}]) n={int(r.nobs)}")
W(f"entrants dans l'échantillon apparié : {int(e['entrant'].sum())} ; 2022 inconnu : {int(ok['nb_audio_2022_commune'].isna().sum())}")

# ---------- 7. Sites web ----------
W("\n=== 7. Sites web (erreurs groupées par domaine) ===")
wb = ok[ok["site_lu"]==1].copy(); wb["domain"] = wb["domain"].fillna("none")
VARS = ["prix_affiche","grille_tarifs","sante100","classe2","essai_gratuit","bilan_gratuit","rdv_en_ligne","devis","garantie_suivi"]
t = wb.groupby("type5", observed=True).apply(lambda g: pd.Series({"n":len(g), **{v: wmean(g[v], g["poids"]) for v in VARS}})); W(t.round(3).to_string()); t.to_csv("outputs/v2/web_by_type5.csv")
W("\nPar marque (sites lus, part) :"); tb = wb[wb["brand"]!=""].groupby("brand").apply(lambda g: pd.Series({"n":len(g), "prix":g["prix_affiche"].mean(), "page_tarifs":g["grille_tarifs"].mean(), "sante100":g["sante100"].mean()})); W(tb.round(2).sort_values("n", ascending=False).to_string()); tb.to_csv("outputs/v2/web_by_brand.csv")
ind = wb[wb["type5"]=="unbranded independent"].copy()
W("\nIndépendants non enseignés : contenu ~ bandes + contrôles (grappes communes)")
X = X_base(ind, ("log_dem65","share65")).drop(columns=[c for c in X_base(ind).columns if c.startswith("type5_")])
rows=[]
for v in VARS:
    r = wls(ind[v], X, ind["poids"], ind["code_insee"]); rows.append({"var":v, "n":int(r.nobs), **{b: f"{r.params[b]:+.3f} ({r.pvalues[b]:.2f})" for b in ["bande10_1-2","bande10_3-9","bande10_10+"]}, "owner": f"{r.params['owner']:+.3f} ({r.pvalues['owner']:.2f})"})
t = pd.DataFrame(rows); W(t.to_string(index=False)); t.to_csv("outputs/v2/web_indep_bands.csv", index=False)
W("\nNotes ~ chaque variable de contenu + bandes + type5 + contrôles (grappes domaine) :")
rows=[]
for v in VARS:
    X = X_base(wb, ("log_dem65","share65")); X[v] = wb[v].astype(float)
    for y, lab in [("log_reviews1","log(1+avis)"),("rating_v","note")]:
        r = wls(wb[y], X, wb["poids"], wb["domain"]); rows.append({"var":v, "y":lab, "coef":round(r.params[v],3), "se":round(r.bse[v],3), "p":round(r.pvalues[v],3), "n":int(r.nobs)})
t = pd.DataFrame(rows); W(t.to_string(index=False)); t.to_csv("outputs/v2/web_vs_ratings.csv", index=False)
# ---------- 8. Traçabilité : parts de 5,0, A4, comptages ----------
W("\n=== 8. Traçabilité ===")
W("Part de notes = 5,0 par bande (notés, pondéré) : " + rated.groupby("bande10", observed=True).apply(lambda g: round(wmean((g["rating_v"]>=4.95).astype(float), g["poids"]),3)).to_dict().__str__())
W("Moyenne des notes ≥10 avis par bande : " + rated[rated["n_reviews"]>=10].groupby("bande10", observed=True).apply(lambda g: round(wmean(g["rating_v"], g["poids"]),3)).to_dict().__str__())
W(f"Terciles de revenu (bornes k€) : {[round(c,2) for c in cuts]}")
t = ok.groupby(["bande10","terc"], observed=True).apply(lambda g: pd.Series({"n":len(g),"rated":wmean(g["rated"],g["poids"]),"reviews_median":wq(g["n_reviews"],g["poids"]),"rating":wmean(g["rating_v"],g["poids"])})); W(t.round(3).to_string()); t.to_csv("outputs/v2/A4_income_x_band.csv")
W(f"sites avec site web référencé : {int(ok['has_website'].sum())} ; domaines distincts : {ok['domain'].dropna().nunique()} ; sites lus : {int(ok['site_lu'].sum())}")
allsites = pd.read_csv("sites_v2.csv", dtype={"code_insee":str}); rs = allsites[allsites["retail"]]
W(f"couche sites : {len(allsites)} structures, {len(rs)} retail ; bandes 10 km : {rs['concurrents_10km'].pipe(lambda x: pd.cut(x,[-1,0,2,9,1e9],labels=['0','1-2','3-9','10+'])).value_counts().sort_index().to_dict()} ; part ≥10 concurrents à 30 km : {(rs['concurrents_30km']>=10).mean():.3f}")
W(f"Google : listings trouvés {int((d['place_id'].notna()).sum())} / {len(d)} ; appariés {len(ok)} ; non appariés {len(d)-len(ok)}")
raw_n = sum(1 for _ in open("places_raw.jsonl", encoding="utf-8")); W(f"lignes de collecte Google (dont re-requêtes) : {raw_n}")
ind_w = wb[wb["type5"]=="unbranded independent"]; W("Indépendants, parts brutes par bande (site lu) :"); W(ind_w.groupby("bande10", observed=True).apply(lambda g: pd.Series({"n":len(g),"prix":wmean(g["prix_affiche"],g["poids"]),"page_tarifs":wmean(g["grille_tarifs"],g["poids"]),"sante100":wmean(g["sante100"],g["poids"])})).round(3).to_string())
# ---------- 9. Benchmark coiffeurs ----------
W("\n=== 9. Benchmark coiffeurs (mêmes communes) ===")
b = pd.read_csv("outputs/v2/benchmark_coiffeurs.csv", dtype={"code_insee":str}); b["bande10"] = pd.Categorical(b["bande10"].astype(str), ["0","1-2","3-9","10+"], ordered=True); b["poids"]=1.0; b["rated"]=(b["n_reviews"]>0).astype(float)
W(f"salons : {len(b)} ; communes : {b['code_insee'].nunique()} ; moyenne globale des notes : {b.loc[b['rated']==1,'rating'].mean():.3f}")
t = b.groupby("bande10", observed=True).apply(lambda g: pd.Series({"n":len(g),"rated":g["rated"].mean(),"reviews_median":g["n_reviews"].median(),"rating_mean":g.loc[g["rated"]==1,"rating"].mean(),"share_5":(g.loc[g["rated"]==1,"rating"]>=4.95).mean()})); W(t.round(3).to_string())
Xb = pd.get_dummies(b[["bande10"]], drop_first=True).astype(float); Xb["log_pop"]=b["log_pop"]; Xb["rev"]=b["rev"]
rb = sm.WLS(np.log1p(b["n_reviews"]), sm.add_constant(Xb)).fit(cov_type="cluster", cov_kwds={"groups": b["code_insee"]}); W("log(1+avis) coiffeurs ~ bandes + log pop + revenu (grappes communes) :"); W(tab(rb).to_string())
rr = b[b["rated"]==1]; rb2 = sm.WLS(rr["rating"], sm.add_constant(Xb.loc[rr.index])).fit(cov_type="cluster", cov_kwds={"groups": rr["code_insee"]}); W("note coiffeurs ~ bandes + contrôles :"); W(tab(rb2).to_string())
qb = rr.groupby("bande10", observed=True)["n_reviews"].transform(lambda x: x.quantile(.75)); btop = rr[rr["n_reviews"]>=qb]
t = btop.groupby("bande10", observed=True).apply(lambda g: pd.Series({"n":len(g),"min_reviews":g["n_reviews"].min(),"sd":g["rating"].std(ddof=0),"mean":g["rating"].mean(),"below45":(g["rating"]<4.5).mean()})); W("quart supérieur coiffeurs :"); W(t.round(3).to_string()); t.to_csv("outputs/v2/benchmark_top_quartile.csv")
lvb = stats.levene(btop.loc[btop["bande10"].isin(["0","1-2"]),"rating"], btop.loc[btop["bande10"].isin(["3-9","10+"]),"rating"], center="median"); W(f"Brown-Forsythe coiffeurs quart sup ≤2 vs ≥3 : W={lvb.statistic:.2f}, p={lvb.pvalue:.3g}")
OUT.close(); print(open("outputs/v2/results.txt").read())
ok.to_csv("outputs/v2/sample_analysis_v2.csv", index=False)
