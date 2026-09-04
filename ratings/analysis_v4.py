"""Compléments de la version 2.3 : effet plafond (part de 5,0 et Levene avec log avis), une structure par fiche Google, effectif de la
régression sur les communes du benchmark, robustesse Audilab (chaîne intégrée) et alternatives Demant, scission des corners opticiens,
terciles d'APL dans chaque bande, bandes à 20 km, coiffeurs dans la fenêtre 30-90 avis, liste des communes du benchmark, mesures de
concurrence aux centroïdes d'arrondissement. Sorties : outputs/v2/results_v4.txt et CSV associés."""
import os, json, numpy as np, pandas as pd, statsmodels.api as sm, warnings
from scipy import stats
from scipy.spatial import cKDTree
warnings.filterwarnings("ignore")
REPO = os.path.expanduser("~/mnt/deserts-audioprothese")
OUT = open("outputs/v2/results_v4.txt", "w")
def W(x=""): OUT.write(str(x)+"\n")
ok = pd.read_csv("outputs/v2/sample_analysis_v2.csv", dtype={"code_insee":str,"site_id":str,"place_id":str})
ok["bande10"] = pd.Categorical(ok["bande10"].astype(str), ["0","1-2","3-9","10+"], ordered=True)
ok["type5"] = pd.Categorical(ok["type5"], ["integrated chain","brand network","optician-hosted","mutualist network","unbranded independent"])
def wmean(x,w):
    x=np.asarray(x,float); w=np.asarray(w,float); k=~np.isnan(x); return (x[k]*w[k]).sum()/w[k].sum() if w[k].sum()>0 else np.nan
def wq(x,w,q=.5):
    x=np.asarray(x,float); w=np.asarray(w,float); k=~np.isnan(x); x,w=x[k],w[k]
    if len(x)==0: return np.nan
    o=np.argsort(x); x,w=x[o],w[o]; c=np.cumsum(w)/w.sum(); return x[np.searchsorted(c,q)]
def wsd(x,w):
    x=np.asarray(x,float); w=np.asarray(w,float); k=~np.isnan(x); x,w=x[k],w[k]; return np.sqrt(wmean((x-wmean(x,w))**2,w)) if len(x)>1 else np.nan
def wls(y, X, w, groups):
    X = sm.add_constant(X.astype(float)); k = y.notna() & X.notna().all(axis=1)
    return sm.WLS(y[k].astype(float), X[k], weights=w[k]).fit(cov_type="cluster", cov_kwds={"groups": groups[k]})
def tab(r, keep=None):
    t = pd.DataFrame({"coef": r.params, "se": r.bse, "p": r.pvalues}); return (t.loc[[k for k in keep if k in t.index]] if keep else t).round(3)
def X_base(df, bands="bande10", typ="type5"):
    X = pd.get_dummies(df[[bands, typ]], drop_first=True).astype(float)
    for c in ["owner","npr","log_pop","revenu_k","rev_missing","log_dem65","share65"]: X[c] = df[c]
    return X
BANDS = ["bande10_1-2","bande10_3-9","bande10_10+"]
FORMS = ["type5_brand network","type5_optician-hosted","type5_mutualist network","type5_unbranded independent","owner"]
OUTC = [("log_reviews1","log(1+avis)"),("rated","noté"),("rating_v","note")]
rated = ok[ok["rated"]==1].copy(); q = rated.groupby("bande10", observed=True)["n_reviews"].transform(lambda x: x.quantile(.75)); top = rated[rated["n_reviews"]>=q].copy()

# ---------- A. Effet plafond ----------
W("=== A. Effet plafond : quart supérieur d'avis par bande ===")
t = top.groupby("bande10", observed=True).apply(lambda g: pd.Series({"n":len(g),"mean":wmean(g["rating_v"],g["poids"]),"sd":wsd(g["rating_v"],g["poids"]),"share_5.0":wmean((g["rating_v"]>=4.95).astype(float),g["poids"]),"share_4.9plus":wmean((g["rating_v"]>=4.85).astype(float),g["poids"])}))
W(t.round(3).to_string()); t.to_csv("outputs/v2/top_quartile_ceiling.csv")
top["absdev"] = (top["rating_v"] - top.groupby("bande10", observed=True)["rating_v"].transform("median")).abs(); top["log_reviews"] = np.log(top["n_reviews"])
X = pd.get_dummies(top[["bande10","type5"]], drop_first=True).astype(float); X["owner"]=top["owner"]; X["log_reviews"]=top["log_reviews"]
r = wls(top["absdev"], X, top["poids"], top["code_insee"]); W("Levene groupé avec log(avis) : |écart à la médiane de bande| ~ bandes + forme + propriétaire + log avis"); W(tab(r, BANDS+["log_reviews"]).to_string())
wt = r.wald_test(BANDS, scalar=True); W(f"  test 4 bandes p = {float(wt.pvalue):.3g}")
# ---------- B. Une structure par fiche Google ; effectif benchmark ----------
W("\n=== B. Une structure par fiche Google (spec B) ===")
dedup = ok.sort_values("site_id").drop_duplicates("place_id", keep="first")
for y, lab in OUTC:
    r = wls(dedup[y], X_base(dedup), dedup["poids"], dedup["code_insee"]); W(f"[dédoublonné] {lab} · n={int(r.nobs)}"); W(tab(r, BANDS+["owner"]).to_string())
b = pd.read_csv("outputs/v2/benchmark_coiffeurs.csv", dtype={"code_insee":str})
bc = ok[ok["code_insee"].isin(set(b["code_insee"]))]
Xb = pd.get_dummies(bc[["bande10"]], drop_first=True).astype(float); Xb["log_pop"]=bc["log_pop"]; Xb["revenu_k"]=bc["revenu_k"]
r = wls(bc["log_reviews1"], Xb, bc["poids"], bc["code_insee"]); W(f"\ncentres dans les {b['code_insee'].nunique()} communes du benchmark : log(1+avis) ~ bandes + log pop + revenu · n = {int(r.nobs)}"); W(tab(r, BANDS).to_string())
b[["code_insee","bande10"]].drop_duplicates().assign(n_salons=lambda d: d["code_insee"].map(b.groupby("code_insee").size())).sort_values("code_insee").to_csv("outputs/v2/benchmark_communes.csv", index=False)
W("liste des communes du benchmark écrite : outputs/v2/benchmark_communes.csv")

# ---------- C. Audilab et alternatives Demant ----------
W("\n=== C. Audilab reclassée en chaîne intégrée ; alternatives avec Audika et Audilab fusionnées ===")
okc = ok.copy(); okc["type5"] = pd.Categorical(np.where(okc["brand"]=="Audilab", "integrated chain", okc["type5"].astype(str)), ["integrated chain","brand network","optician-hosted","mutualist network","unbranded independent"])
W(f"sites Audilab dans l'échantillon apparié : {int((ok['brand']=='Audilab').sum())}")
for y, lab in OUTC:
    r = wls(okc[y], X_base(okc), okc["poids"], okc["code_insee"]); W(f"[Audilab = chaîne intégrée] {lab} · n={int(r.nobs)}"); W(tab(r, BANDS+FORMS).to_string())
alt = pd.read_csv("sites_retail_alternatives.csv", dtype={"site_id":str})
if "bande_alt10_demant" in alt.columns:
    oka = ok.merge(alt[["site_id","bande_alt10_demant","alternatives_10km_demant"]], on="site_id", how="left")
    W(f"sites de l'échantillon changeant de bande d'alternatives avec la fusion Demant : {int((oka['bande_alt10'].astype(str)!=oka['bande_alt10_demant'].astype(str)).sum())}")
    Xa = X_base(oka).drop(columns=BANDS); Xa = pd.concat([Xa, pd.get_dummies(pd.Series(pd.Categorical(oka["bande_alt10_demant"].astype(str), ["0","1-2","3-9","10+"]), index=oka.index), prefix="altd", drop_first=True).astype(float)], axis=1)
    r = wls(oka["log_reviews1"], Xa, oka["poids"], oka["code_insee"]); W("[alternatives distinctes, Demant fusionné] log(1+avis)"); W(tab(r, ["altd_1-2","altd_3-9","altd_10+"]).to_string())
else:
    W("sites_retail_alternatives.csv sans colonnes Demant : relancer build_alternatives.py")

# ---------- D. Scission des corners opticiens ----------
W("\n=== D. Corners opticiens : fiche du magasin ou fiche propre ===")
# La fiche Google des corners est celle du magasin d'optique chez Optical Center, Acuitis, Générale d'Optique, Lissac, Atol et Optic 2000
# (médianes d'avis de 59 à 417, types Google du magasin) ; Alain Afflelou Acousticien et Krys Audition ont le plus souvent une fiche propre (médianes 17 et 12).
SHOP = {"Optical Center","Acuitis","Generale d'Optique","Lissac","Atol","Optic 2000"}
W("types Google des corners (premiers) : " + ok.loc[ok["type5"]=="optician-hosted","primary_type"].fillna("").value_counts().head(6).to_dict().__str__())
ok["corner_shop"] = ((ok["type5"]=="optician-hosted") & ok["brand"].isin(SHOP)).astype(int)
ok["type6"] = np.where(ok["type5"]=="optician-hosted", np.where(ok["corner_shop"]==1, "corner, shop listing", "corner, own listing"), ok["type5"].astype(str))
t = ok[ok["type5"]=="optician-hosted"].groupby("brand").agg(n=("site_id","size"), shop_listing=("corner_shop","mean"), owner=("owner","mean"), median_reviews=("n_reviews","median"), rating=("rating_v","mean")).round(2); W(t.to_string()); t.to_csv("outputs/v2/corner_split.csv")
ok["type6"] = pd.Categorical(ok["type6"], ["integrated chain","brand network","corner, shop listing","corner, own listing","mutualist network","unbranded independent"])
for y, lab in OUTC:
    r = wls(ok[y], X_base(ok, typ="type6"), ok["poids"], ok["code_insee"]); W(f"[type6] {lab} · n={int(r.nobs)}"); W(tab(r, BANDS+["type6_brand network","type6_corner, shop listing","type6_corner, own listing","type6_mutualist network","type6_unbranded independent","owner"]).to_string())
X = X_base(ok, typ="type6")
for f in ["type6_corner, shop listing","type6_corner, own listing","type6_brand network","type6_unbranded independent"]: X["owner_x_"+f] = X[f]*ok["owner"]
r = wls(ok["log_reviews1"], X, ok["poids"], ok["code_insee"]); W("propriétaire × forme (type6), log(1+avis) :"); W(tab(r, ["owner"]+[c for c in X.columns if c.startswith("owner_x_")]).to_string())

# ---------- E. Terciles d'APL dans chaque bande ----------
W("\n=== E. Accessibilité (APL v2.1) : terciles pondérés dans l'échantillon apparié ===")
cuts = [wq(ok["apl_v21"], ok["poids"], q) for q in (1/3, 2/3)]; ok["apl_terc"] = pd.cut(ok["apl_v21"], [-np.inf]+cuts+[np.inf], labels=["A1","A2","A3"])
W(f"bornes des terciles d'APL : {[round(c,1) for c in cuts]}")
t = ok.groupby(["bande10","apl_terc"], observed=True).apply(lambda g: pd.Series({"n":len(g),"rated":wmean(g["rated"],g["poids"]),"reviews_median":wq(g["n_reviews"],g["poids"]),"rating":wmean(g["rating_v"],g["poids"])})); W(t.round(3).to_string()); t.to_csv("outputs/v2/apl_x_band.csv")
X = X_base(ok); X = pd.concat([X, pd.get_dummies(ok["apl_terc"], prefix="apl", drop_first=True).astype(float)], axis=1)
for y, lab in OUTC:
    r = wls(ok[y], X, ok["poids"], ok["code_insee"]); W(f"{lab} : A2 {r.params['apl_A2']:+.3f} (p={r.pvalues['apl_A2']:.2f}) · A3 {r.params['apl_A3']:+.3f} (p={r.pvalues['apl_A3']:.2f}) ; bandes {[round(r.params[b],3) for b in BANDS]}")
X = X_base(ok); X["log_apl"] = np.log1p(ok["apl_v21"])
for y, lab in OUTC:
    r = wls(ok[y], X, ok["poids"], ok["code_insee"]); W(f"{lab} : log(1+APL) {r.params['log_apl']:+.3f} (se {r.bse['log_apl']:.3f}, p={r.pvalues['log_apl']:.2f}) ; bandes {[round(r.params[b],3) for b in BANDS]}")
W("corrélation de Spearman APL / avis : %.3f ; APL / note : %.3f" % (stats.spearmanr(ok["apl_v21"], ok["n_reviews"], nan_policy="omit")[0], stats.spearmanr(ok.loc[ok['rated']==1,"apl_v21"], ok.loc[ok['rated']==1,"rating_v"], nan_policy="omit")[0]))

# ---------- F. Bandes à 20 km ----------
W("\n=== F. Concurrence à 20 km ===")
ok["bande20"] = pd.Categorical(pd.cut(ok["concurrents_20km"], [-1,0,2,9,1e9], labels=["0","1-2","3-9","10+"]).astype(str), ["0","1-2","3-9","10+"], ordered=True)
W("effectifs (échantillon apparié) par bande à 20 km : " + ok["bande20"].value_counts().sort_index().to_dict().__str__() + " ; pondérés : " + ok.groupby("bande20", observed=True)["poids"].sum().round(0).to_dict().__str__())
t = ok.groupby("bande20", observed=True).apply(lambda g: pd.Series({"n":len(g),"rated":wmean(g["rated"],g["poids"]),"reviews_median":wq(g["n_reviews"],g["poids"]),"rating":wmean(g["rating_v"],g["poids"])})); W(t.round(3).to_string()); t.to_csv("outputs/v2/bands20_desc.csv")
for y, lab in OUTC:
    r = wls(ok[y], X_base(ok, bands="bande20"), ok["poids"], ok["code_insee"]); W(f"[bandes 20 km] {lab}"); W(tab(r, ["bande20_1-2","bande20_3-9","bande20_10+"]).to_string())
X = X_base(ok); X["log_comp20"] = np.log1p(ok["concurrents_20km"])
r = wls(ok["log_reviews1"], X, ok["poids"], ok["code_insee"]); W(f"log(1+avis) : log(1+concurrents 20 km) en plus des bandes 10 km : {r.params['log_comp20']:+.3f} (se {r.bse['log_comp20']:.3f}) ; bandes 10 km {[round(r.params[b],3) for b in BANDS]}")
r20 = rated.copy(); r20["bande20"] = ok.loc[r20.index, "bande20"]; q20 = r20.groupby("bande20", observed=True)["n_reviews"].transform(lambda x: x.quantile(.75)); t20 = r20[r20["n_reviews"]>=q20]
W("quart supérieur par bande à 20 km : " + t20.groupby("bande20", observed=True).apply(lambda g: pd.Series({"n":len(g),"sd":round(wsd(g["rating_v"],g["poids"]),3)})).to_dict("index").__str__())

# ---------- G. Coiffeurs, fenêtre 30-90 avis ----------
W("\n=== G. Coiffeurs dans la fenêtre 30-90 avis ===")
b["bande10"] = pd.Categorical(b["bande10"].astype(str), ["0","1-2","3-9","10+"], ordered=True); bw = b[(b["n_reviews"]>=30)&(b["n_reviews"]<=90)]
t = bw.groupby("bande10", observed=True).apply(lambda g: pd.Series({"n":len(g),"sd":g["rating"].std(ddof=0),"mean":g["rating"].mean(),"below45":(g["rating"]<4.5).mean()})); W(t.round(3).to_string()); t.to_csv("outputs/v2/benchmark_window_30_90.csv")
lv = stats.levene(bw.loc[bw["bande10"].isin(["0","1-2"]),"rating"], bw.loc[bw["bande10"].isin(["3-9","10+"]),"rating"], center="median"); W(f"Brown-Forsythe coiffeurs 30-90, ≤2 vs ≥3 : W={lv.statistic:.2f}, p={lv.pvalue:.3g}")

# ---------- H. Centroïdes d'arrondissement ----------
W("\n=== H. Mesures de concurrence aux centroïdes d'arrondissement (Paris, Lyon, Marseille) ===")
s = pd.read_csv("sites_v2.csv", dtype={"code_insee":str,"code_insee_geo":str,"site_id":str}); rs = s[s["retail"]].copy()
c21 = pd.read_csv(f"{REPO}/data/processed/communes_scoring_2026_v21.csv", dtype={"code_insee":str}).set_index("code_insee")
arr = rs["code_insee"].str.match(r"751\d\d|6938\d|132\d\d")
rs["lat2"] = np.where(arr, rs["code_insee"].map(c21["lat"]), rs["lat"]); rs["lon2"] = np.where(arr, rs["code_insee"].map(c21["lon"]), rs["lon"])
g = rs.dropna(subset=["lat2","lon2"]).copy(); R=6371.0
def xyz(lat, lon):
    la, lo = np.radians(lat), np.radians(lon); return np.c_[R*np.cos(la)*np.cos(lo), R*np.cos(la)*np.sin(lo), R*np.sin(la)]
pts = xyz(g["lat2"].values, g["lon2"].values); tree = cKDTree(pts)
g["c10_arr"] = tree.query_ball_point(pts, 2*R*np.sin(10/(2*R)), return_length=True) - 1
g["b_old"] = pd.cut(g["concurrents_10km"], [-1,0,2,9,1e9], labels=["0","1-2","3-9","10+"]).astype(str); g["b_new"] = pd.cut(g["c10_arr"], [-1,0,2,9,1e9], labels=["0","1-2","3-9","10+"]).astype(str)
ch = g[g["b_old"]!=g["b_new"]]
W(f"sites d'arrondissement : {int(arr.sum())} ; sites retail dont le compte à 10 km change : {int((g['c10_arr']!=g['concurrents_10km']).sum())} ; dont la bande change : {len(ch)} " + (ch.groupby(["b_old","b_new"]).size().to_dict().__str__() if len(ch) else ""))
W(f"sites de l'échantillon dont la bande change : {int(ok['site_id'].isin(set(ch['site_id'])).sum())}")
OUT.close(); print(open("outputs/v2/results_v4.txt").read())
