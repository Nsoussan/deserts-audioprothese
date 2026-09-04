import numpy as np, pandas as pd, json, os
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, matplotlib.ticker as mt
plt.rcParams.update({"font.size":8.5,"axes.titlesize":9.5,"axes.labelsize":8.5,"xtick.labelsize":8,"ytick.labelsize":8,"legend.fontsize":7.5,"font.family":"serif"})
ok = pd.read_csv("outputs/v2/sample_analysis_v2.csv", dtype={"code_insee":str})
ok["bande10"] = pd.Categorical(ok["bande10"].astype(str), ["0","1-2","3-9","10+"], ordered=True)
bench = pd.read_csv("outputs/v2/benchmark_coiffeurs.csv", dtype={"code_insee":str}); bench["bande10"] = pd.Categorical(bench["bande10"].astype(str), ["0","1-2","3-9","10+"], ordered=True)
def wmean(x,w):
    x=np.asarray(x,float); w=np.asarray(w,float); k=~np.isnan(x); return (x[k]*w[k]).sum()/w[k].sum()
def wq(x,w,q=.5):
    x=np.asarray(x,float); w=np.asarray(w,float); k=~np.isnan(x); x,w=x[k],w[k]; o=np.argsort(x); x,w=x[o],w[o]; c=np.cumsum(w)/w.sum(); return x[np.searchsorted(c,q)]
def wsd(x,w):
    x=np.asarray(x,float); w=np.asarray(w,float); k=~np.isnan(x); x,w=x[k],w[k]; return np.sqrt(wmean((x-wmean(x,w))**2,w))
rng = np.random.default_rng(11); bands=["0","1-2","3-9","10+"]; xl=["0","1–2","3–9","10+"]
def cboot(df, col, fn, B=200):
    """bootstrap par communes (rapide)"""
    codes = df["code_insee"].values; x = df[col].values.astype(float); w = df["poids"].values.astype(float)
    uniq, inv = np.unique(codes, return_inverse=True); idx_by = [np.where(inv==i)[0] for i in range(len(uniq))]
    out=[]
    for _ in range(B):
        pick = rng.integers(0, len(uniq), len(uniq)); ii = np.concatenate([idx_by[p] for p in pick]); out.append(fn(x[ii], w[ii]))
    return np.nanpercentile(out,2.5), np.nanpercentile(out,97.5)
def series(df, col, fn):
    return np.array([[fn(df[df["bande10"]==b][col], df[df["bande10"]==b]["poids"]), *cboot(df[df["bande10"]==b], col, fn)] for b in bands])
COL={"integrated chain":"#2a78d6","unbranded independent":"#1baf7a","all":"#000000","bench":"#eb6834"}
LS={"integrated chain":"-","unbranded independent":":","all":"-","bench":"--"}
MK={"integrated chain":"o","unbranded independent":"^","all":"s","bench":"D"}
LAB={"integrated chain":"Integrated chains","unbranded independent":"Unbranded independents","all":"All hearing-aid centres","bench":"Hairdressers, same communes"}
def panel(ax, col, fn, ylabel, title, pct=False, bench_col=None):
    for j,t in enumerate(["integrated chain","unbranded independent","all"]):
        sub = ok if t=="all" else ok[ok["type5"]==t]; v=series(sub,col,fn); y,lo,hi=v[:,0],v[:,1],v[:,2]
        if pct: y,lo,hi=y*100,lo*100,hi*100
        ax.errorbar(np.arange(4)+(j-1)*0.06, y, yerr=[y-lo,hi-y], fmt=MK[t]+LS[t], color=COL[t], lw=1.4, ms=4, capsize=2, label=LAB[t])
    if bench_col:
        bb=bench.copy(); bb["poids"]=1.0; v=series(bb,bench_col,fn); y,lo,hi=v[:,0],v[:,1],v[:,2]
        if pct: y,lo,hi=y*100,lo*100,hi*100
        ax.errorbar(np.arange(4)+0.12, y, yerr=[y-lo,hi-y], fmt=MK["bench"]+"--", color=COL["bench"], lw=1.2, ms=4, capsize=2, label=LAB["bench"])
    ax.set_xticks(range(4)); ax.set_xticklabels(xl); ax.set_ylabel(ylabel); ax.set_title(title, loc="left"); ax.grid(axis="y", color="#e5e5e5", lw=.8); ax.spines[["top","right"]].set_visible(False)
    ax.set_xlabel("Competing hearing-aid centres within 10 km")
bench["rated"]=(bench["n_reviews"]>0).astype(float)
fig,axes=plt.subplots(1,2,figsize=(6.5,3.1))
panel(axes[0],"n_reviews",lambda x,w: wq(x,w,.5),"Median number of Google reviews (log scale)","A. Review volume", bench_col="n_reviews")
axes[0].set_yscale("log"); axes[0].set_yticks([5,10,20,50,100]); axes[0].yaxis.set_major_formatter(mt.ScalarFormatter()); axes[0].yaxis.set_minor_formatter(mt.NullFormatter())
panel(axes[1],"rated",wmean,"Sites with at least one review (%)","B. Share with at least one review", pct=True, bench_col="rated")
axes[0].legend(frameon=False); plt.tight_layout(); plt.savefig("outputs/v2/fig1_activity.png", dpi=300); plt.close()
# Figure 2 : niveau (tous notés ; ≥10 avis) et dispersion (quart supérieur par bande), avec benchmark
rated=ok[ok["rated"]==1].copy(); q=rated.groupby("bande10", observed=True)["n_reviews"].transform(lambda x: x.quantile(.75)); top=rated[rated["n_reviews"]>=q]
br=bench[bench["rated"]==1].copy(); bq=br.groupby("bande10", observed=True)["n_reviews"].transform(lambda x: x.quantile(.75)); btop=br[br["n_reviews"]>=bq]; btop["poids"]=1.0; br["poids"]=1.0
fig,axes=plt.subplots(2,2,figsize=(6.6,5.6)); axes=axes.ravel(); axes[3].axis("off")
ax=axes[0]
for j,(df,lab,c,m,ls) in enumerate([(rated,"All rated centres","#000000","s","-"),(rated[rated["n_reviews"]>=10],"Centres with ≥10 reviews","#2a78d6","o",":"),(br,"Hairdressers, same communes","#eb6834","D","--")]):
    v=series(df,"rating_v" if "rating_v" in df else "rating",wmean); ax.errorbar(np.arange(4)+(j-1)*0.06, v[:,0], yerr=[v[:,0]-v[:,1],v[:,2]-v[:,0]], fmt=m+ls, color=c, lw=1.4, ms=4, capsize=2, label=lab)
ax.set_ylim(4.5,5.0); ax.set_xticks(range(4)); ax.set_xticklabels(xl); ax.set_ylabel("Mean Google rating"); ax.set_title("A. Rating level", loc="left"); ax.grid(axis="y", color="#e5e5e5", lw=.8); ax.spines[["top","right"]].set_visible(False); ax.legend(frameon=False); ax.set_xlabel("Competing hearing-aid centres within 10 km")
ax=axes[1]
for j,(df,lab,c,m,col) in enumerate([(top,"Hearing-aid centres","#2a78d6","o","rating_v"),(btop,"Hairdressers, same communes","#eb6834","D","rating")]):
    v=series(df,col,wsd); ax.errorbar(np.arange(4)+(j-0.5)*0.06, v[:,0], yerr=[v[:,0]-v[:,1],v[:,2]-v[:,0]], fmt=m+("--" if "Hairdressers" in lab else "-"), color=c, lw=1.4, ms=4, capsize=2, label=lab)
ax.set_xticks(range(4)); ax.set_xticklabels(xl); ax.set_ylabel("S.D. of ratings across sites"); ax.set_title("B. Dispersion, most-reviewed quarter", loc="left"); ax.grid(axis="y", color="#e5e5e5", lw=.8); ax.spines[["top","right"]].set_visible(False); ax.legend(frameon=False); ax.set_xlabel("Competing hearing-aid centres within 10 km")
ax=axes[2]
for j,(df,lab,c,m,col) in enumerate([(top,"Hearing-aid centres","#2a78d6","o","rating_v"),(btop,"Hairdressers, same communes","#eb6834","D","rating")]):
    df=df.copy(); df["b45"]=(df[col]<4.5).astype(float); v=series(df,"b45",wmean)*100; ax.errorbar(np.arange(4)+(j-0.5)*0.06, v[:,0], yerr=[v[:,0]-v[:,1],v[:,2]-v[:,0]], fmt=m+("--" if "Hairdressers" in lab else "-"), color=c, lw=1.4, ms=4, capsize=2, label=lab)
ax.set_xticks(range(4)); ax.set_xticklabels(xl); ax.set_ylabel("Sites rated below 4.5 (%)"); ax.set_title("C. Share below 4.5, most-reviewed quarter", loc="left"); ax.grid(axis="y", color="#e5e5e5", lw=.8); ax.spines[["top","right"]].set_visible(False); ax.set_xlabel("Competing hearing-aid centres within 10 km")
plt.tight_layout(); plt.savefig("outputs/v2/fig2_content.png", dpi=300); plt.close()
# Figure 0 : carte des 8 421 sites par bande (métropole)
s = pd.read_csv("sites_v2.csv", dtype={"code_insee":str}); s=s[s["retail"]]
c = pd.read_csv(os.path.expanduser("~/mnt/deserts-audioprothese/data/processed/communes_scoring_2026_v21.csv"), dtype={"code_insee":str}).dropna(subset=["lat","lon"])
met = lambda df: df[(df["lat"]>41)&(df["lat"]<51.5)&(df["lon"]>-5.5)&(df["lon"]<10)]
s["band"]=pd.cut(s["concurrents_10km"],[-1,0,2,9,1e9],labels=["0","1-2","3-9","10+"])
fig,ax=plt.subplots(figsize=(6.4,6.4)); cm=met(c); ax.scatter(cm["lon"],cm["lat"],s=0.15,color="#ececec",rasterized=True)
cols={"10+":"#a9bcd8","3-9":"#3f78c3","1-2":"#eb6834","0":"#b30000"}; sizes={"10+":3,"3-9":5,"1-2":11,"0":16}
for b in ["10+","3-9","1-2","0"]:
    g=met(s[s["band"]==b]); ax.scatter(g["lon"],g["lat"],s=sizes[b],color=cols[b],label=f"{b} competitors within 10 km (n = {int((s['band']==b).sum()):,})",linewidths=0,rasterized=True)
ax.set_aspect(1/np.cos(np.radians(46.5))); ax.plot([3.0,4.2],[41.6,41.6],color="k",lw=1.5); ax.text(3.6,41.72,"100 km",ha="center",fontsize=8); ax.axis("off"); ax.legend(frameon=False, loc="lower left", markerscale=2)
plt.tight_layout(); plt.savefig("outputs/v2/fig0_map.png", dpi=300); plt.close()
print("figures v2 écrites")
