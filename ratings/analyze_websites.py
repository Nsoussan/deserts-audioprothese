"""Contenu des sites web × concurrence × type × notes."""
import numpy as np, pandas as pd, statsmodels.api as sm
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
d = pd.read_csv("outputs/sites_ratings_sample_ext.csv", dtype={"code_insee":str,"site_id":str})
w = pd.read_csv("outputs/websites_coded.csv", dtype={"site_id":str})
d = d.merge(w, on="site_id", how="left")
d["bande10"] = pd.Categorical(d["bande10"].astype(str), ["0","1-2","3-9","10+"], ordered=True)
d["type"] = pd.Categorical(d["type"], ["enseigne nationale","mutualiste","indépendant"])
d["site_listed"] = d["has_website"].astype(float)              # site web référencé sur la fiche Google
d["site_lu"] = np.where(d["site_listed"]==1, d["web_ok"].fillna(0), 0.0)
VARS = ["prix_affiche","grille_tarifs","sante100","classe2","essai_gratuit","bilan_gratuit","rdv_en_ligne","devis","garantie_suivi"]
for v in VARS: d[v] = np.where(d["site_lu"]==1, d[v], np.nan)   # codé seulement si site lu
def wmean(x, wt):
    x=np.asarray(x,float); wt=np.asarray(wt,float); k=~np.isnan(x); return (x[k]*wt[k]).sum()/wt[k].sum() if wt[k].sum()>0 else np.nan
out = open("outputs/summary_websites.txt","w")
def W(s=""): out.write(str(s)+"\n")
W(f"sites appariés : {len(d)} · site web référencé : {int(d['site_listed'].sum())} · site lu et codé : {int(d['site_lu'].sum())}")
t = d.groupby("type", observed=True).apply(lambda g: pd.Series({"n":len(g),"site_referencé":wmean(g["site_listed"],g["poids"]),"site_lu":wmean(g["site_lu"],g["poids"]), **{v: wmean(g[v],g["poids"]) for v in VARS}}))
W("\nPar type (pondéré ; variables de contenu conditionnelles à un site lu) :"); W(t.round(3).to_string()); t.to_csv("outputs/web_par_type.csv")
t = d.groupby("bande10", observed=True).apply(lambda g: pd.Series({"n":len(g),"site_referencé":wmean(g["site_listed"],g["poids"]),"site_lu":wmean(g["site_lu"],g["poids"]), **{v: wmean(g[v],g["poids"]) for v in VARS}}))
W("\nPar bande (pondéré) :"); W(t.round(3).to_string()); t.to_csv("outputs/web_par_bande.csv")
ind = d[d["type"]=="indépendant"]
t = ind.groupby("bande10", observed=True).apply(lambda g: pd.Series({"n":len(g),"site_referencé":wmean(g["site_listed"],g["poids"]),"site_lu":wmean(g["site_lu"],g["poids"]), **{v: wmean(g[v],g["poids"]) for v in VARS}}))
W("\nIndépendants seuls, par bande (leurs sites sont les leurs) :"); W(t.round(3).to_string()); t.to_csv("outputs/web_indep_par_bande.csv")
# Régressions (indépendants, site lu) : contenu ~ bandes + contrôles
ii = ind[ind["site_lu"]==1].copy(); ii["log_pop"]=ii["log_pop"].fillna(np.log(ii["population_2023"].clip(lower=1))); ii["revenu_k"]=ii["revenu_median_uc"].fillna(25000)/1000
X = pd.get_dummies(ii[["bande10"]], drop_first=True).astype(float); X["log_pop"]=ii["log_pop"]; X["revenu_k"]=ii["revenu_k"]; X["n_praticiens"]=ii["n_praticiens"].astype(float)
W("\nWLS (indépendants, site lu) : contenu ~ bandes + log pop + revenu + praticiens")
for v in ["prix_affiche","grille_tarifs","sante100","essai_gratuit","bilan_gratuit","rdv_en_ligne"]:
    y = ii[v].astype(float); k = y.notna()
    r = sm.WLS(y[k], sm.add_constant(X[k]), weights=ii["poids"][k]).fit(cov_type="HC1")
    W(f"  {v:15s} n={int(r.nobs)}  1-2: {r.params['bande10_1-2']:+.3f} (p={r.pvalues['bande10_1-2']:.2f})  3-9: {r.params['bande10_3-9']:+.3f} (p={r.pvalues['bande10_3-9']:.2f})  10+: {r.params['bande10_10+']:+.3f} (p={r.pvalues['bande10_10+']:.2f})  logpop: {r.params['log_pop']:+.3f} (p={r.pvalues['log_pop']:.2f})")
# Transparence des prix et activité de notation (tous types, site lu), à concurrence et type contrôlés
dd = d[d["site_lu"]==1].copy(); dd["log_pop"]=dd["log_pop"].fillna(np.log(dd["population_2023"].clip(lower=1))); dd["revenu_k"]=dd["revenu_median_uc"].fillna(25000)/1000
X = pd.get_dummies(dd[["bande10","type"]], drop_first=True).astype(float); X["log_pop"]=dd["log_pop"]; X["revenu_k"]=dd["revenu_k"]; X["optique"]=dd["optique"].astype(float)
W("\nWLS : notes ~ transparence des prix + bandes + type + contrôles (sites lus)")
for v in ["prix_affiche","grille_tarifs","sante100","essai_gratuit"]:
    Xv = X.copy(); Xv[v] = dd[v].astype(float)
    for y, lab in [("log_reviews1","log(1+avis)"),("rating_v","note")]:
        yy = dd[y].astype(float); k = yy.notna() & Xv[v].notna()
        r = sm.WLS(yy[k], sm.add_constant(Xv[k]), weights=dd["poids"][k]).fit(cov_type="HC1")
        W(f"  {lab:12s} ~ {v:14s} : {r.params[v]:+.3f} (se {r.bse[v]:.3f}, p={r.pvalues[v]:.3f}) n={int(r.nobs)}")
out.close(); print(open("outputs/summary_websites.txt").read())
# Figure 4 : contenu des sites des indépendants par bande
COL={"prix_affiche":"#2a78d6","sante100":"#eb6834","essai_gratuit":"#1baf7a","rdv_en_ligne":"#6b6b6b"}
LAB={"prix_affiche":"Own prices displayed","sante100":"Mentions fully reimbursed class I","essai_gratuit":"Free trial offered","rdv_en_ligne":"Online booking"}
MK={"prix_affiche":"o","sante100":"s","essai_gratuit":"^","rdv_en_ligne":"v"}
bands=["0","1-2","3-9","10+"]; xl=["0","1–2","3–9","10+"]; rng=np.random.default_rng(2)
def boot(x,wt,B=400):
    x=np.asarray(x,float); wt=np.asarray(wt,float); k=~np.isnan(x); x,wt=x[k],wt[k]
    if len(x)<5: return (np.nan,np.nan,np.nan)
    p=wt/wt.sum(); est=wmean(x,wt); bs=[wmean(x[i],wt[i]) for i in (rng.choice(len(x),len(x),p=p) for _ in range(B))]
    return est,np.nanpercentile(bs,2.5),np.nanpercentile(bs,97.5)
plt.figure(figsize=(6.6,4.4))
for j,v in enumerate(["prix_affiche","sante100","essai_gratuit","rdv_en_ligne"]):
    vals=np.array([boot(ii[ii["bande10"]==b][v], ii[ii["bande10"]==b]["poids"]) for b in bands])*100
    plt.errorbar(np.arange(4)+(j-1.5)*0.05, vals[:,0], yerr=[vals[:,0]-vals[:,1], vals[:,2]-vals[:,0]], fmt=MK[v]+"-", color=COL[v], lw=1.8, ms=6, capsize=2.5, label=LAB[v])
plt.xticks(range(4), xl); plt.ylabel("Share of independents' websites (%)"); plt.xlabel("Competing hearing-aid sites within 10 km (straight line)")
plt.title("Website content of independent centres by local competition", fontsize=10.5, loc="left"); plt.grid(axis="y", color="#e5e5e5", lw=.8)
plt.gca().spines[["top","right"]].set_visible(False); plt.legend(frameon=False, fontsize=8.5); plt.tight_layout(); plt.savefig("outputs/fig4_websites_independents.png", dpi=220); plt.close()
d.to_csv("outputs/sites_ratings_sample_web.csv", index=False); print("fig4 écrite")
