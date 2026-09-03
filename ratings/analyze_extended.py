"""Analyses complémentaires : alternatives réelles, gradient de revenu, entrants, effets fixes commune."""
import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import stats
d = pd.read_csv("outputs/sites_ratings_sample.csv", dtype={"code_insee":str})
smp = pd.read_csv("sample_3000.csv", dtype={"code_insee":str})
d = d.merge(smp[["site_id","alternatives_10km","alternatives_20km","memes_enseigne_10km","bande_alt10","nb_audio_2022_commune","entrant_commune"]], on="site_id", how="left")
ok = d[d["match_ok"]].copy()
ok["bande10"] = pd.Categorical(ok["bande10"].astype(str), ["0","1-2","3-9","10+"], ordered=True)
ok["bande_alt10"] = pd.Categorical(ok["bande_alt10"].astype(str), ["0","1-2","3-9","10+"], ordered=True)
ok["type"] = pd.Categorical(ok["type"], ["enseigne nationale","mutualiste","indépendant"])
ok["log_reviews1"] = np.log1p(ok["n_reviews"]); ok["indep"] = (ok["type"]=="indépendant").astype(float)
ok["revenu_impute"] = ok["revenu_median_uc"].isna().astype(float)
ok["revenu_median_uc"] = ok["revenu_median_uc"].fillna(25000)  # convention du rapport (secret statistique)
ok["revenu_k"] = ok["revenu_median_uc"]/1000
ok["log_pop"] = ok["log_pop"].fillna(np.log(ok["population_2023"].clip(lower=1)))
ok["has_website"] = ok["has_website"].astype(float)
def wmean(x, w):
    x=np.asarray(x,float); w=np.asarray(w,float); k=~np.isnan(x); return (x[k]*w[k]).sum()/w[k].sum() if w[k].sum()>0 else np.nan
def wq(x, w, q=.5):
    x=np.asarray(x,float); w=np.asarray(w,float); k=~np.isnan(x); x,w=x[k],w[k]
    if len(x)==0: return np.nan
    o=np.argsort(x); x,w=x[o],w[o]; c=np.cumsum(w)/w.sum(); return x[np.searchsorted(c,q)]
out = open("outputs/summary_extended.txt","w")
def W(s=""): out.write(str(s)+"\n")

# 1. Alternatives réelles (enseignes distinctes) : robustesse
W("=== 1. Alternatives réelles à 10 km (enseignes distinctes ; chaque indépendant compte pour une) ===")
t = ok.groupby("bande_alt10", observed=True).apply(lambda g: pd.Series({"n":len(g),"part_avec_avis":wmean(g["has_rating"],g["poids"]),"avis_median":wq(g["n_reviews"],g["poids"]),"note_moyenne":wmean(g["rating_v"],g["poids"])}))
W(t.round(3).to_string()); t.to_csv("outputs/ext_alternatives_par_bande.csv")
W(f"Sites déplacés de bande par rapport au comptage brut : {(ok['bande_alt10'].astype(str)!=ok['bande10'].astype(str)).sum()} sur {len(ok)}")
X = pd.get_dummies(ok[["bande_alt10","type"]], drop_first=True).astype(float); X["log_pop"]=ok["log_pop"]; X["revenu_k"]=ok["revenu_k"]; X["optique"]=ok["optique"].astype(float)
r = sm.WLS(ok["log_reviews1"], sm.add_constant(X), weights=ok["poids"]).fit(cov_type="HC1")
W("WLS log(1+avis) ~ bandes d'alternatives + contrôles"); W(pd.DataFrame({"coef":r.params,"se":r.bse,"p":r.pvalues}).round(3).to_string()); W()

# 2. Gradient de revenu
W("=== 2. Revenu médian communal (terciles pondérés sur l'échantillon) ===")
cuts = [wq(ok["revenu_median_uc"], ok["poids"], q) for q in (1/3, 2/3)]
ok["tercile_revenu"] = pd.cut(ok["revenu_median_uc"], [-np.inf]+cuts+[np.inf], labels=["T1 (bas)","T2","T3 (haut)"])
W(f"bornes des terciles : {cuts[0]:.0f} € et {cuts[1]:.0f} €")
t = ok.groupby("tercile_revenu", observed=True).apply(lambda g: pd.Series({"n":len(g),"part_avec_avis":wmean(g["has_rating"],g["poids"]),"avis_median":wq(g["n_reviews"],g["poids"]),"note_moyenne":wmean(g["rating_v"],g["poids"]),"part_indep":wmean(g["indep"],g["poids"]),"part_site_web":wmean(g["has_website"],g["poids"])}))
W(t.round(3).to_string()); t.to_csv("outputs/ext_revenu_terciles.csv")
t2 = ok.groupby(["bande10","tercile_revenu"], observed=True).apply(lambda g: pd.Series({"n":len(g),"part_avec_avis":wmean(g["has_rating"],g["poids"]),"avis_median":wq(g["n_reviews"],g["poids"]),"note_moyenne":wmean(g["rating_v"],g["poids"])}))
W(t2.round(3).to_string()); t2.to_csv("outputs/ext_revenu_x_bande.csv")
X = pd.get_dummies(ok[["bande10","type","tercile_revenu"]], drop_first=True).astype(float); X["log_pop"]=ok["log_pop"]; X["optique"]=ok["optique"].astype(float)
for y, lab in [("log_reviews1","log(1+avis)"),("has_rating","a au moins un avis"),("rating_v","note (si >=1 avis)")]:
    yy = ok[y].astype(float); k = yy.notna()
    r = sm.WLS(yy[k], sm.add_constant(X[k]), weights=ok["poids"][k]).fit(cov_type="HC1")
    W(f"WLS {lab} ~ bandes + type + terciles de revenu + log pop + optique · n={int(r.nobs)}"); W(pd.DataFrame({"coef":r.params,"se":r.bse,"p":r.pvalues}).round(3).to_string()); W()

# 3. Entrants (commune sans audioprothésiste en 2022)
W("=== 3. Entrants : sites situés dans une commune sans audioprothésiste en 2022 ===")
e = ok[ok["nb_audio_2022_commune"].notna()].copy(); e["entrant"] = e["entrant_commune"].astype(float)
t = e.groupby(["entrant_commune","type"], observed=True).apply(lambda g: pd.Series({"n":len(g),"part_avec_avis":wmean(g["has_rating"],g["poids"]),"avis_median":wq(g["n_reviews"],g["poids"]),"avis_q75":wq(g["n_reviews"],g["poids"],.75),"note_moyenne":wmean(g["rating_v"],g["poids"]),"part_site_web":wmean(g["has_website"],g["poids"])}))
W(t.round(3).to_string()); t.to_csv("outputs/ext_entrants.csv")
X = pd.get_dummies(e[["bande10","type"]], drop_first=True).astype(float); X["entrant"]=e["entrant"]; X["log_pop"]=e["log_pop"]; X["revenu_k"]=e["revenu_k"]; X["optique"]=e["optique"].astype(float)
for y, lab in [("log_reviews1","log(1+avis)"),("has_rating","a au moins un avis"),("rating_v","note (si >=1 avis)")]:
    yy = e[y].astype(float); k = yy.notna()
    r = sm.WLS(yy[k], sm.add_constant(X[k]), weights=e["poids"][k]).fit(cov_type="HC1")
    W(f"WLS {lab} ~ entrant + bandes + type + contrôles · n={int(r.nobs)}"); W(pd.DataFrame({"coef":r.params,"se":r.bse,"p":r.pvalues}).loc[["entrant","type_indépendant","log_pop"]].round(3).to_string()); W()

# 4. Effets fixes commune : enseignes vs indépendants à marché constant
W("=== 4. Effets fixes commune (communes de l'échantillon avec au moins 2 sites appariés de types différents) ===")
g = ok.groupby("code_insee")
multi = ok[g["site_id"].transform("count")>=2]
multi = multi[multi.groupby("code_insee")["indep"].transform("nunique")==2]
W(f"communes : {multi['code_insee'].nunique()} · sites : {len(multi)}")
for y, lab in [("log_reviews1","log(1+avis)"),("has_rating","a au moins un avis"),("rating_v","note (si >=1 avis)"),("has_website","a un site web")]:
    m = multi[multi[y].notna()].copy(); m["y"]=m[y].astype(float); m["opt"]=m["optique"].astype(float); m["npr"]=m["n_praticiens"].astype(float)
    r = smf.wls("y ~ indep + opt + npr + C(code_insee)", data=m, weights=m["poids"]).fit(cov_type="cluster", cov_kwds={"groups": m["code_insee"]})
    W(f"FE commune · {lab} · n={int(r.nobs)} : indépendant = {r.params['indep']:.3f} (se {r.bse['indep']:.3f}, p={r.pvalues['indep']:.3f}) ; optique = {r.params['opt']:.3f} (p={r.pvalues['opt']:.3f}) ; praticiens = {r.params['npr']:.3f} (p={r.pvalues['npr']:.3f})")
W()
out.close(); print(open("outputs/summary_extended.txt").read())

# Figure 3 : revenu x concurrence (activité), deux panneaux
COLS = {"T1 (bas)":"#eb6834","T2":"#6b6b6b","T3 (haut)":"#2a78d6"}; MK={"T1 (bas)":"v","T2":"s","T3 (haut)":"^"}
bands=["0","1-2","3-9","10+"]; xl=["0","1–2","3–9","10+"]
rng=np.random.default_rng(3)
def boot(x,w,fn,B=400):
    x=np.asarray(x,float); w=np.asarray(w,float); k=~np.isnan(x); x,w=x[k],w[k]
    if len(x)<5: return (np.nan,np.nan,np.nan)
    p=w/w.sum(); est=fn(x,w); bs=[fn(x[i],w[i]) for i in (rng.choice(len(x),len(x),p=p) for _ in range(B))]
    return est,np.nanpercentile(bs,2.5),np.nanpercentile(bs,97.5)
fig, axes = plt.subplots(1,2,figsize=(11,4.2))
for ax,(col,fn,yl,title,pct) in zip(axes,[("n_reviews",lambda x,w: wq(x,w,.5),"Median number of Google reviews","A. Review volume by competition and commune income",False),("has_rating",wmean,"Sites with at least one review (%)","B. Share rated, by competition and commune income",True)]):
    for j,tc in enumerate(["T1 (bas)","T2","T3 (haut)"]):
        sub=ok[ok["tercile_revenu"]==tc]; v=np.array([boot(sub[sub["bande10"]==b][col], sub[sub["bande10"]==b]["poids"], fn) for b in bands])
        y,lo,hi=v[:,0],v[:,1],v[:,2]
        if pct: y,lo,hi=y*100,lo*100,hi*100
        ax.errorbar(np.arange(4)+(j-1)*0.06,y,yerr=[y-lo,hi-y],fmt=MK[tc]+"-",color=COLS[tc],lw=1.8,ms=6,capsize=2.5,label={"T1 (bas)":"Bottom income tercile","T2":"Middle tercile","T3 (haut)":"Top income tercile"}[tc])
    ax.set_xticks(range(4)); ax.set_xticklabels(xl); ax.set_ylabel(yl); ax.set_title(title,fontsize=10.5,loc="left"); ax.grid(axis="y",color="#e5e5e5",lw=.8); ax.spines[["top","right"]].set_visible(False)
    ax.set_xlabel("Competing hearing-aid sites within 10 km (straight line)")
axes[0].legend(frameon=False,fontsize=9); plt.tight_layout(); plt.savefig("outputs/fig3_income_gradient.png",dpi=220); plt.close()
ok.to_csv("outputs/sites_ratings_sample_ext.csv", index=False)
print("fig3 écrite")
