"""Variables v2 : type organisationnel en 5 classes (fondé sur la part de sites avec praticien titulaire), propriétaire sur site,
demande à 10 km (population 65+ des communes à moins de 10 km) et demande par site, population à 10 km."""
import pandas as pd, numpy as np, os
from scipy.spatial import cKDTree
R=6371.0
def xyz(lat, lon):
    la, lo = np.radians(lat), np.radians(lon); return np.c_[R*np.cos(la)*np.cos(lo), R*np.cos(la)*np.sin(lo), R*np.sin(la)]
s = pd.read_csv("sites_audio_2026.csv", dtype={"code_insee":str,"code_postal":str,"siret":str})
alt = pd.read_csv("sites_retail_alternatives.csv", dtype={"code_insee":str})[["site_id","alternatives_10km","alternatives_20km","memes_enseigne_10km","nb_audio_2022_commune","entrant_commune"]]
s = s.merge(alt, on="site_id", how="left")
s["owner_on_site"] = (s["n_titulaires"]>0).astype(int)
OPT = {"Optical Center","Krys Audition","Alain Afflelou Acousticien","Atol","Optic 2000","Lissac","Generale d'Optique","Acuitis"}
share = s[s["retail"]].groupby("groupe")["owner_on_site"].mean()
def type5(g):
    if g=="Indépendant / autre": return "unbranded independent"
    if "mutualiste" in g: return "mutualist network"
    if g in OPT: return "optician-hosted"
    return "brand network" if share.get(g,0) >= 0.45 else "integrated chain"
s["type5"] = s["groupe"].map(type5)
s["brand"] = np.where(s["groupe"]=="Indépendant / autre", "", s["groupe"])
# Demande à 10 km
c = pd.read_csv(os.path.expanduser("~/mnt/deserts-audioprothese/data/processed/communes_scoring_2026_v21.csv"), dtype={"code_insee":str})
cc = c.dropna(subset=["lat","lon"]).copy()
cc["p65"] = cc["population_2023"]*cc["part_65_plus_pct"].fillna(cc["part_65_plus_pct"].median())/100
tree = cKDTree(xyz(cc["lat"].values, cc["lon"].values))
pts = xyz(s["lat"].values, s["lon"].values)
neigh = tree.query_ball_point(pts, 2*R*np.sin(10/(2*R)))
s["pop_10km"] = [cc["population_2023"].values[n].sum() for n in neigh]
s["pop65_10km"] = [cc["p65"].values[n].sum() for n in neigh]
s["demand65_per_site"] = s["pop65_10km"]/(s["concurrents_10km"].fillna(0)+1)
s["apl_v21"] = s["code_insee"].map(c.set_index("code_insee")["apl_v21"])
s.to_csv("sites_v2.csv", index=False)
r = s[s["retail"]]
print(r["type5"].value_counts()); print(); print(r.groupby("type5")["owner_on_site"].mean().round(2))
print("\nclassement des marques :"); print(pd.DataFrame({"share_owner": share.round(2), "type5": pd.Series({g: type5(g) for g in share.index})}).sort_values("type5").to_string())
print("\ndemande 65+ par site : ", r["demand65_per_site"].describe().round(0).to_string())
