"""Étape 1 bis : alternatives distinctes à 10 et 20 km (une enseigne comptée une fois), sites de même enseigne, effectif 2022 de la
commune et indicateur d'entrant. Lit sites_audio_2026.csv (sortie de build_sites.py) et le jeu communal ; écrit
sites_retail_alternatives.csv (non redistribué : noms et adresses). Reproduit la construction faite le 3 septembre 2026, avec en plus
la variante où Audika et Audilab, deux enseignes du groupe Demant, comptent pour une seule alternative (colonnes *_demant)."""
import os, numpy as np, pandas as pd
from scipy.spatial import cKDTree
REPO = os.path.expanduser("~/mnt/deserts-audioprothese")
R = 6371.0
def xyz(lat, lon):
    la, lo = np.radians(lat), np.radians(lon); return np.c_[R*np.cos(la)*np.cos(lo), R*np.cos(la)*np.sin(lo), R*np.sin(la)]
s = pd.read_csv("sites_audio_2026.csv", dtype={"code_insee":str,"code_postal":str,"siret":str,"code_insee_geo":str})
c = pd.read_csv(f"{REPO}/data/processed/communes_scoring_2026.csv", dtype={"code_insee":str})
r = s[s["retail"] & s["lat"].notna()].copy().reset_index(drop=True)
pts = xyz(r["lat"].values, r["lon"].values); tree = cKDTree(pts)
grp = r["groupe"].values
grp_demant = np.where(np.isin(grp, ["Audika", "Audilab"]), "Demant (Audika, Audilab)", grp)
indep = (grp == "Indépendant / autre")
for km in (10, 20):
    neigh = tree.query_ball_point(pts, 2*R*np.sin(km/(2*R)))
    alt, same, altd = [], [], []
    for i, nb in enumerate(neigh):
        nb = [j for j in nb if j != i]
        # une enseigne compte une fois ; chaque indépendant compte pour lui-même
        keys = {("indep", j) if indep[j] else ("brand", grp[j]) for j in nb}
        keysd = {("indep", j) if indep[j] else ("brand", grp_demant[j]) for j in nb}
        alt.append(len(keys)); altd.append(len(keysd)); same.append(sum(1 for j in nb if (not indep[i]) and grp[j] == grp[i]))
    r[f"alternatives_{km}km"] = alt; r[f"memes_enseigne_{km}km"] = same; r[f"alternatives_{km}km_demant"] = altd
r["bande_alt10"] = pd.cut(r["alternatives_10km"], [-1, 0, 2, 9, 1e9], labels=["0","1-2","3-9","10+"])
r["bande_alt10_demant"] = pd.cut(r["alternatives_10km_demant"], [-1, 0, 2, 9, 1e9], labels=["0","1-2","3-9","10+"])
n22 = c.set_index("code_insee")["nb_audioprothesistes_2022"]
r["nb_audio_2022_commune"] = r["code_insee"].map(n22)
r["entrant_commune"] = r["nb_audio_2022_commune"].eq(0)
r.to_csv("sites_retail_alternatives.csv", index=False)
print(len(r), "sites retail ;", r["bande_alt10"].value_counts().sort_index().to_dict(), "; entrants :", int(r["entrant_commune"].sum()),
      "; 2022 inconnu :", int(r["nb_audio_2022_commune"].isna().sum()),
      "; sites changeant de bande avec Audika+Audilab fusionnés :", int((r["bande_alt10"].astype(str) != r["bande_alt10_demant"].astype(str)).sum()))
