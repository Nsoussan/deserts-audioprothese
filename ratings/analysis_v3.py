"""Compléments demandés par le rapporteur (ronde 2) : tests de dispersion groupés par commune, fenêtre fixe d'avis, sans opticiens,
identifiants Places distincts, interactions propriétaire, régression empilée centres/coiffeurs, gradient sur les 879 communes."""
import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf, json, warnings
from scipy import stats
warnings.filterwarnings("ignore")
OUT = open("outputs/v2/results_v3.txt","w")
def W(x=""): OUT.write(str(x)+"\n")
ok = pd.read_csv("outputs/v2/sample_analysis_v2.csv", dtype={"code_insee":str,"site_id":str})
ok["bande10"] = pd.Categorical(ok["bande10"].astype(str), ["0","1-2","3-9","10+"], ordered=True)
ok["type5"] = pd.Categorical(ok["type5"], ["integrated chain","brand network","optician-hosted","mutualist network","unbranded independent"])
ok["captive"] = ok["bande10"].isin(["0","1-2"]).astype(float)
def wmean(x,w):
    x=np.asarray(x,float); w=np.asarray(w,float); k=~np.isnan(x); return (x[k]*w[k]).sum()/w[k].sum()
def wsd(x,w):
    x=np.asarray(x,float); w=np.asarray(w,float); k=~np.isnan(x); x,w=x[k],w[k]; return np.sqrt(wmean((x-wmean(x,w))**2,w))
def wls(y, X, w, groups):
    X = sm.add_constant(X.astype(float)); k = y.notna() & X.notna().all(axis=1)
    return sm.WLS(y[k].astype(float), X[k], weights=w[k]).fit(cov_type="cluster", cov_kwds={"groups": groups[k]})
def tab(r, keep=None):
    t = pd.DataFrame({"coef": r.params, "se": r.bse, "p": r.pvalues}); return (t.loc[[k for k in keep if k in t.index]] if keep else t).round(3)
rng = np.random.default_rng(21)
def cboot_diff(df, col, fn, B=500):
    codes=df["code_insee"].values; x=df[col].values.astype(float); w=df["poids"].values.astype(float); cap=df["captive"].values
    uniq, inv = np.unique(codes, return_inverse=True); idx=[np.where(inv==i)[0] for i in range(len(uniq))]; out=[]
    for _ in range(B):
        ii=np.concatenate([idx[p] for p in rng.integers(0,len(uniq),len(uniq))]); out.append(fn(x[ii][cap[ii]==0],w[ii][cap[ii]==0]) - fn(x[ii][cap[ii]==1],w[ii][cap[ii]==1]))
    return np.percentile(out,2.5), np.percentile(out,97.5)
# --- Identifiants Places distincts
W("=== Identifiants Places ===")
W(f"appariements : {len(ok)} ; place_id distincts : {ok['place_id'].nunique()} ; sites partageant un place_id : {int(ok.duplicated('place_id', keep=False).sum())}")
dup = ok[ok.duplicated("place_id", keep=False)]; W("formes des doublons : " + dup["type5"].value_counts().to_dict().__str__())
W(f"listings fermés (CLOSED_*) conservés dans l'analyse : {int(ok['business_status'].fillna('').str.contains('CLOSED').sum())}")
# --- Non-appariement par bande
smp = pd.read_csv("sample_3000.csv", dtype={"site_id":str}); smp["bande10"]=smp["bande10"].astype(str)
nm = smp[~smp["site_id"].isin(ok["site_id"])]; W("non appariés par bande : " + nm["bande10"].value_counts().to_dict().__str__() + " sur " + smp["bande10"].value_counts().to_dict().__str__())
# --- B1 : dispersion, tests groupés par commune
W("\n=== B1. Dispersion : quart supérieur par bande, tests groupés ===")
rated = ok[ok["rated"]==1].copy(); q = rated.groupby("bande10", observed=True)["n_reviews"].transform(lambda x: x.quantile(.75)); top = rated[rated["n_reviews"]>=q].copy()
top["low45"]=(top["rating_v"]<4.5).astype(float); top["low46"]=(top["rating_v"]<4.6).astype(float); top["low47"]=(top["rating_v"]<4.7).astype(float)
for lab, df in [("tous", top), ("sans opticiens", top[top["type5"]!="optician-hosted"])]:
    sd = df.groupby("bande10", observed=True).apply(lambda g: wsd(g["rating_v"], g["poids"])); n = df.groupby("bande10", observed=True).size()
    low = df.groupby("bande10", observed=True).apply(lambda g: pd.Series({"n_low45": int((g["rating_v"]<4.5).sum()), "n": len(g), "p45": wmean(g["low45"], g["poids"]), "p46": wmean(g["low46"], g["poids"]), "p47": wmean(g["low47"], g["poids"]), "d10": g["rating_v"].quantile(.10)}))
    dsd = wsd(df.loc[df["captive"]==0,"rating_v"], df.loc[df["captive"]==0,"poids"]) - wsd(df.loc[df["captive"]==1,"rating_v"], df.loc[df["captive"]==1,"poids"])
    ci = cboot_diff(df, "rating_v", wsd)
    W(f"[{lab}] n par bande {n.to_dict()} ; SD {sd.round(3).to_dict()} ; diff SD (≥3 − ≤2) = {dsd:.3f}, IC95 bootstrap communes [{ci[0]:.3f}; {ci[1]:.3f}]")
    W(low.round(3).to_string())
    X = pd.get_dummies(df[["bande10","type5"]], drop_first=True).astype(float); X["owner"]=df["owner"]; X["log_reviews"]=np.log(df["n_reviews"])
    r = wls(df["low45"], X, df["poids"], df["code_insee"]); W("LPM < 4,5 ~ bandes + forme + propriétaire + log avis (grappes communes) :"); W(tab(r, ["bande10_1-2","bande10_3-9","bande10_10+","type5_optician-hosted","type5_unbranded independent","owner","log_reviews"]).to_string())
    Xc = pd.get_dummies(df[["type5"]], drop_first=True).astype(float); Xc["competitive"]=1-df["captive"]; Xc["owner"]=df["owner"]; Xc["log_reviews"]=np.log(df["n_reviews"])
    r = wls(df["low45"], Xc, df["poids"], df["code_insee"]); W(f"LPM < 4,5 : ≥3 vs ≤2 = {r.params['competitive']:+.3f} (se {r.bse['competitive']:.3f}, p={r.pvalues['competitive']:.3g})")
    # test de tendance : |écart à la moyenne de bande| ~ bande (Levene-type, groupé)
    df2 = df.copy(); df2["absdev"] = (df2["rating_v"] - df2.groupby("bande10", observed=True)["rating_v"].transform("median")).abs()
    r = wls(df2["absdev"], pd.get_dummies(df2[["bande10","type5"]], drop_first=True).astype(float), df2["poids"], df2["code_insee"]); W("Levene groupé (|écart à la médiane de bande| ~ bandes + forme) :"); W(tab(r, ["bande10_1-2","bande10_3-9","bande10_10+"]).to_string())
    wt = r.wald_test(["bande10_1-2","bande10_3-9","bande10_10+"], scalar=True); W(f"  test 4 bandes (Wald groupé) p = {float(wt.pvalue):.3g}")
    df2["band_num"] = df2["bande10"].cat.codes.astype(float); Xt = pd.get_dummies(df2[["type5"]], drop_first=True).astype(float); Xt["band_num"]=df2["band_num"]
    r = wls(df2["absdev"], Xt, df2["poids"], df2["code_insee"]); W(f"  tendance linéaire : {r.params['band_num']:+.4f} (p={r.pvalues['band_num']:.3g})")
# fenêtre fixe 30-90 avis
W("\nFenêtre fixe 30–90 avis (toutes formes / sans opticiens) :")
for lab, df in [("tous", rated[(rated["n_reviews"]>=30)&(rated["n_reviews"]<=90)]), ("sans opticiens", rated[(rated["n_reviews"]>=30)&(rated["n_reviews"]<=90)&(rated["type5"]!="optician-hosted")])]:
    df = df.copy(); df["low45"]=(df["rating_v"]<4.5).astype(float)
    t = df.groupby("bande10", observed=True).apply(lambda g: pd.Series({"n":len(g),"sd":wsd(g["rating_v"],g["poids"]),"mean":wmean(g["rating_v"],g["poids"]),"p45":wmean(g["low45"],g["poids"]),"n_low45":int((g["rating_v"]<4.5).sum())}))
    ci = cboot_diff(df, "rating_v", wsd); W(f"[{lab}] IC95 diff SD (≥3 − ≤2) [{ci[0]:.3f}; {ci[1]:.3f}]"); W(t.round(3).to_string())
# note pondérée par avis sans opticiens
W("\nNote pondérée par le nombre d'avis, sans opticiens : " + rated[rated["type5"]!="optician-hosted"].groupby("bande10", observed=True).apply(lambda g: round(np.average(g["rating_v"], weights=g["poids"]*g["n_reviews"]),3)).to_dict().__str__())
# --- B3 : interactions propriétaire
W("\n=== B3. Propriétaire × bande, propriétaire × forme (log(1+avis)) ===")
X = pd.get_dummies(ok[["bande10","type5"]], drop_first=True).astype(float); X["owner"]=ok["owner"]; X["npr"]=ok["n_praticiens"].astype(float); X["log_pop"]=np.log(ok["population_2023"].clip(lower=1)); X["revenu_k"]=ok["revenu_median_uc"].fillna(25000)/1000
for b in ["bande10_1-2","bande10_3-9","bande10_10+"]: X[b+"_x_owner"]=X[b]*X["owner"]
r = wls(ok["log_reviews1"], X, ok["poids"], ok["code_insee"]); W(tab(r, ["owner","bande10_1-2_x_owner","bande10_3-9_x_owner","bande10_10+_x_owner"]).to_string()); W(f"  Wald interactions = 0 : p = {float(r.wald_test([c for c in X.columns if c.endswith('_x_owner')], scalar=True).pvalue):.3f}")
X = pd.get_dummies(ok[["bande10","type5"]], drop_first=True).astype(float); X["owner"]=ok["owner"]; X["npr"]=ok["n_praticiens"].astype(float); X["log_pop"]=np.log(ok["population_2023"].clip(lower=1)); X["revenu_k"]=ok["revenu_median_uc"].fillna(25000)/1000
for t5 in ["type5_brand network","type5_optician-hosted","type5_unbranded independent"]: X[t5+"_x_owner"]=X[t5]*X["owner"]
r = wls(ok["log_reviews1"], X, ok["poids"], ok["code_insee"]); W(tab(r, ["owner"]+[c for c in X.columns if c.endswith("_x_owner")]).to_string()); W(f"  Wald interactions = 0 : p = {float(r.wald_test([c for c in X.columns if c.endswith('_x_owner')], scalar=True).pvalue):.3f}")
W("effet propriétaire par forme (owner + interaction) : " + ", ".join(f"{t5.replace('type5_','')}: {r.params['owner']+r.params[t5+'_x_owner']:+.2f}" for t5 in ["type5_brand network","type5_optician-hosted","type5_unbranded independent"]) + f", integrated chain: {r.params['owner']:+.2f}")
# interaction bande x indépendant (coefficients)
X = pd.get_dummies(ok[["bande10","type5"]], drop_first=True).astype(float); X["owner"]=ok["owner"]; X["npr"]=ok["n_praticiens"].astype(float); X["log_pop"]=np.log(ok["population_2023"].clip(lower=1)); X["revenu_k"]=ok["revenu_median_uc"].fillna(25000)/1000
for b in ["bande10_1-2","bande10_3-9","bande10_10+"]: X[b+"_x_ind"]=X[b]*X["type5_unbranded independent"]
r = wls(ok["log_reviews1"], X, ok["poids"], ok["code_insee"]); W("interactions bande × indépendant : " + tab(r, [c for c in X.columns if c.endswith("_x_ind")]).to_string())
# --- I3 : régression empilée centres / coiffeurs, effets fixes commune
W("\n=== I3. Empilement centres + coiffeurs (879 communes), effets fixes commune ===")
b = pd.read_csv("outputs/v2/benchmark_coiffeurs.csv", dtype={"code_insee":str}); b["bande10"]=b["bande10"].astype(str); b = b[b["n_reviews"]>0].copy()
bc = set(b["code_insee"]); cen = rated[rated["code_insee"].isin(bc)].copy()
st = pd.concat([pd.DataFrame({"code_insee":cen["code_insee"], "bande10":cen["bande10"].astype(str), "rating":cen["rating_v"], "n_reviews":cen["n_reviews"], "credence":1.0, "poids":cen["poids"]}),
                pd.DataFrame({"code_insee":b["code_insee"], "bande10":b["bande10"], "rating":b["rating"], "n_reviews":b["n_reviews"], "credence":0.0, "poids":1.0})], ignore_index=True)
st["captive"]=st["bande10"].isin(["0","1-2"]).astype(float); st["competitive"]=1-st["captive"]
# quart supérieur au sein de chaque (bien, bande)
st["q75"]=st.groupby(["credence","bande10"])["n_reviews"].transform(lambda x: x.quantile(.75)); tp = st[st["n_reviews"]>=st["q75"]].copy(); tp["low45"]=(tp["rating"]<4.5).astype(float)
W(f"communes : {tp['code_insee'].nunique()} ; centres {int((tp['credence']==1).sum())} ; salons {int((tp['credence']==0).sum())}")
m = smf.wls("low45 ~ credence*competitive + C(code_insee)", data=tp, weights=tp["poids"]).fit(cov_type="cluster", cov_kwds={"groups": tp["code_insee"]})
W("LPM < 4,5 ~ credence × competitive + FE commune (quart supérieur par bien × bande) :"); W(pd.DataFrame({"coef":m.params,"se":m.bse,"p":m.pvalues}).loc[["credence","credence:competitive"]].round(3).to_string())
m2 = smf.wls("low45 ~ credence*C(bande10) + C(code_insee)", data=tp, weights=tp["poids"]).fit(cov_type="cluster", cov_kwds={"groups": tp["code_insee"]})
W("par bande :"); W(pd.DataFrame({"coef":m2.params,"se":m2.bse,"p":m2.pvalues}).loc[[k for k in m2.params.index if k.startswith("credence")]].round(3).to_string())
tp["absdev"] = (tp["rating"] - tp.groupby(["credence","bande10"])["rating"].transform("median")).abs()
m3 = smf.wls("absdev ~ credence*competitive + C(code_insee)", data=tp, weights=tp["poids"]).fit(cov_type="cluster", cov_kwds={"groups": tp["code_insee"]})
W("Levene empilé (|écart| ~ credence × competitive + FE commune) :"); W(pd.DataFrame({"coef":m3.params,"se":m3.bse,"p":m3.pvalues}).loc[["credence","competitive","credence:competitive"]].round(3).to_string())
# gradient d'activité des centres sur les 879 communes du benchmark
c879 = ok[ok["code_insee"].isin(bc)].copy(); X = pd.get_dummies(c879[["bande10"]], drop_first=True).astype(float); X["log_pop"]=np.log(c879["population_2023"].clip(lower=1)); X["revenu_k"]=c879["revenu_median_uc"].fillna(25000)/1000
r = wls(c879["log_reviews1"], X, c879["poids"], c879["code_insee"]); W(f"\ngradient centres sur les {c879['code_insee'].nunique()} communes du benchmark (mêmes contrôles que coiffeurs) :"); W(tab(r).to_string())
# salons par bande (quart supérieur) pour A2
W("salons notés par bande : " + b.groupby("bande10").size().to_dict().__str__())
OUT.close(); print(open("outputs/v2/results_v3.txt").read())
