"""v2.1 : intègre les 45 arrondissements municipaux (Paris, Lyon, Marseille) au calcul des distances et de l'APL.
Dans la v2.0, ces 45 lignes (3,5 M d'habitants, ~800 activités) n'avaient pas de centroïde et étaient absentes du 2SFCA,
comme offre et comme demande. Ce script recalcule et compare."""
import sys, numpy as np, pandas as pd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from analyses_2026 import distances, apl_2sfca, xyz, R_TERRE
ROOT = Path(__file__).resolve().parents[1]
c = pd.read_csv(ROOT/"data/processed/communes_scoring_2026.csv", dtype={"code_insee":str})
arr = pd.read_csv(ROOT/"data/geo/arrondissements_centroides.csv", dtype={"code_insee":str,"code_ville":str})
v = c.copy()
m = v["code_insee"].isin(arr["code_insee"])
v.loc[m, "lat"] = v.loc[m, "code_insee"].map(arr.set_index("code_insee")["lat"])
v.loc[m, "lon"] = v.loc[m, "code_insee"].map(arr.set_index("code_insee")["lon"])
v.loc[m, "commune"] = v.loc[m, "code_insee"].map(arr.set_index("code_insee")["nom"])
print("arrondissements géocodés :", int(m.sum()), "| communes sans centroïde restantes :", int(v["lat"].isna().sum()))
v["dist_audio_km_v21"] = distances(v, "nb_audioprothesistes_2026")
v["apl_v21"] = apl_2sfca(v, "nb_audioprothesistes_2026")
p65 = v["population_2023"] * v["part_65_plus_pct"].fillna(v["part_65_plus_pct"].median())/100
def wavg(col, mask=None):
    d = v if mask is None else v[mask]; w = p65[d.index]; k = d[col].notna()
    return (d.loc[k, col]*w[k]).sum()/w[k].sum()
rows = []
for lab, mask in [("France", None), ("Île-de-France", v["region"].str.startswith("11")), ("Paris (arrondissements)", v["code_insee"].str.match(r"751\d\d")),
                  ("Lyon (arr.)", v["code_insee"].str.match(r"6938\d")), ("Marseille (arr.)", v["code_insee"].str.match(r"132\d\d")),
                  ("Hauts-de-Seine", v["code_insee"].str.startswith("92")), ("Seine-Saint-Denis", v["code_insee"].str.startswith("93")), ("Val-de-Marne", v["code_insee"].str.startswith("94")),
                  ("Rhône", v["code_insee"].str.startswith("69")), ("Bouches-du-Rhône", v["code_insee"].str.startswith("13"))]:
    rows.append({"zone": lab, "APL_v2.0": round(wavg("apl", mask),1), "APL_v2.1": round(wavg("apl_v21", mask),1)})
cmp = pd.DataFrame(rows); print(cmp.to_string(index=False))
print("\nmédiane communale APL : v2.0 =", round(v["apl"].median(),1), "| v2.1 =", round(v["apl_v21"].median(),1))
print("communes APL nulle : v2.0 =", int((v["apl"]==0).sum()), "| v2.1 =", int((v["apl_v21"]==0).sum()))
print("65+ sous APL 30 (millions) : v2.0 =", round(p65[v["apl"]<30].sum()/1e6,2), "| v2.1 =", round(p65[v["apl_v21"]<30].sum()/1e6,2))
lo = v["apl"].notna() & v["apl_v21"].notna()
print("corrélation de rang v2.0/v2.1 (communes déjà couvertes) :", round(v.loc[lo,["apl","apl_v21"]].corr("spearman").iloc[0,1],4))
d = (v["apl_v21"]-v["apl"]); print("écart absolu médian :", round(d.abs().median(),2), "| communes avec |écart|>5 :", int((d.abs()>5).sum()), "| >10 :", int((d.abs()>10).sum()))
print("\ncommunes les plus affectées :"); print(v.loc[d.abs().sort_values(ascending=False).index[:10], ["code_insee","commune","apl","apl_v21"]].round(1).to_string(index=False))
# cumul accès faible / âgé / modeste (tertiles) avant/après
def cumul(col):
    q = v[col].quantile(1/3); a = v["part_65_plus_pct"].quantile(2/3); r = v["revenu_median_uc"].fillna(25000).quantile(1/3)
    return int(((v[col]<=q)&(v["part_65_plus_pct"]>=a)&(v["revenu_median_uc"].fillna(25000)<=r)).sum())
print("\ncumul (tertiles) : v2.0 =", cumul("apl"), "| v2.1 =", cumul("apl_v21"))
print("sans_audio_5k inchangé :", int(v["sans_audio_5k"].sum()), "| dist v2.1 max écart :", round((v["dist_audio_km_v21"]-v["dist_audio_km"]).abs().max(),2))
v.to_csv(ROOT/"data/processed/communes_scoring_2026_v21.csv", index=False)
cmp.to_csv(ROOT/"outputs/tables/apl_v20_v21_comparaison.csv", index=False)
print("\nécrit : data/processed/communes_scoring_2026_v21.csv")
