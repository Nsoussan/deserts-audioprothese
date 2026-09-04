import pandas as pd, numpy as np, re, os
from scipy.spatial import cKDTree
REPO = os.path.expanduser("~/mnt/deserts-audioprothese")
d = pd.read_csv("rpps_audio_lignes.csv", dtype=str).fillna("")
d = d[d["Code commune (coord. structure)"]!=""].copy()
c = pd.read_csv(f"{REPO}/data/processed/communes_scoring_2026.csv", dtype={"code_insee":str})
d = d[d["Code commune (coord. structure)"].isin(set(c["code_insee"]))]

up = lambda s: s.str.upper().str.strip()
d["ens"] = up(d["Enseigne commerciale site"]); d["rs"] = up(d["Raison sociale site"])

# Classification par mots-clés sur enseigne et raison sociale (heuristique). v2.3 : Krys avant Entendre ; « Entendre » exclut Mieux/Bien/S'/D'Entendre et Entendre et Comprendre ; Harmonie restreint à Harmonie Mutuelle.
RULES = [
 ("Audika", r"AUDIKA|SOGECA"), ("Amplifon", r"AMPLIFON"), ("Audition Santé (Sonova)", r"SONOVA|AUDITION ?SANTE"),
 ("Optical Center", r"OPTICAL CENTER"), ("Audilab", r"AUDILAB"), ("Audition Conseil", r"AUDITION CONSEIL"),
 ("Alain Afflelou Acousticien", r"AFFLELOU"), ("Krys Audition", r"\bKRYS\b"),
 ("Entendre", r"(?<!MIEUX )(?<!BIEN )(?<!S')(?<!D')\bENTENDRE\b(?! ET COMPRENDRE)"),
 ("Sonance Audition", r"SONANCE"), ("Audio 2000", r"AUDIO ?2000"), ("Écouter Voir / mutualiste", r"ECOUTER VOIR|MUTUALIST|MUTUALITE|VYV ?3|\bOXANCE\b|UNION DE GESTION|\bSSAM\b|HARMONIE MUTUELLE"),
 ("Acuitis", r"ACUITIS"), ("GrandAudition", r"GRAND ?AUDITION"), ("VivaSon", r"VIVASON"), ("Idéal Audition", r"IDEAL AUDITION"),
 ("Atol", r"\bATOL\b"), ("Optic 2000", r"OPTIC ?2000"), ("Solusons", r"SOLUSONS"), ("Audio pour tous", r"AUDIO POUR TOUS"),
 ("Manéo Audition", r"MANEO"), ("Benoit Audition", r"BENOIT AUDITION|AUDITION BENOIT|LABORATOIRE D'AUDITION BENOIT"),
 ("Audition Marc Boulet", r"MARC BOULET"), ("Generale d'Optique", r"GENERALE D'OPTIQUE"), ("Lissac", r"LISSAC"),
]
def classify(row):
    for name, pat in RULES:
        if re.search(pat, row["ens"]) or re.search(pat, row["rs"]):
            return name
    return "Indépendant / autre"
d["groupe"] = d.apply(classify, axis=1)

sid = "Identifiant technique de la structure"
def first_nonempty(s):
    s = s[s!=""]; return s.iloc[0] if len(s) else ""
def adresse(g):
    r = g.iloc[0]
    parts = [r["Numéro Voie (coord. structure)"], r["Indice répétition voie (coord. structure)"],
             r["Libellé type de voie (coord. structure)"], r["Libellé Voie (coord. structure)"]]
    return " ".join(p for p in parts if p).strip()
rows=[]
for s, g in d.groupby(sid):
    rows.append({
        "site_id": s, "siret": first_nonempty(g["Numéro SIRET site"]),
        "enseigne": first_nonempty(g["Enseigne commerciale site"]), "raison_sociale": first_nonempty(g["Raison sociale site"]),
        "groupe": g["groupe"].mode().iloc[0],
        "adresse": adresse(g), "code_postal": first_nonempty(g["Code postal (coord. structure)"]),
        "code_insee": g["Code commune (coord. structure)"].iloc[0], "commune_rpps": first_nonempty(g["Libellé commune (coord. structure)"]),
        "telephone": first_nonempty(g["Téléphone (coord. structure)"]),
        "secteur": g["Libellé secteur d'activité"].mode().iloc[0],
        "n_praticiens": g["Identifiant PP"].nunique(),
        "n_salaries": g.loc[g["Libellé mode exercice"]=="Salarié","Identifiant PP"].nunique(),
        "n_titulaires": g.loc[g["Libellé rôle"]=="Titulaire de cabinet","Identifiant PP"].nunique(),
    })
s = pd.DataFrame(rows)
s["nom_site"] = np.where(s["enseigne"]!="", s["enseigne"], s["raison_sociale"])
s["retail"] = s["secteur"].eq("Appareillage médical")
s["type"] = np.where(s["groupe"]=="Indépendant / autre", "indépendant", np.where(s["groupe"].str.contains("mutualiste"), "mutualiste", "enseigne nationale"))

# Jointure communale
def ville(code):
    if code.startswith("751") and len(code)==5: return "75056"
    if code.startswith("6938"): return "69123"
    if code.startswith("132") and len(code)==5: return "13055"
    return code
s["code_insee_geo"] = s["code_insee"].map(ville)
cc = c[["code_insee","commune","region","population_2023","part_65_plus_pct","revenu_median_uc","nb_audioprothesistes_2026","lat","lon","dist_audio_km","apl"]].rename(columns={"code_insee":"code_insee_geo"})
s = s.merge(cc, on="code_insee_geo", how="left")
# Arrondissements de Paris / Lyon / Marseille : pas de centroïde dans le jeu publié -> centroïde de la ville (approximation, à remplacer par les centroïdes d'arrondissement en v2.1)
import json
V = json.load(open("villes_centroides.json"))
for k,(la,lo,nom) in V.items():
    m = s["code_insee_geo"]==k
    s.loc[m,"lat"]=la; s.loc[m,"lon"]=lo; s.loc[m,"commune"]=nom
    s.loc[m,"dist_audio_km"]=0.0
# population / 65+ / revenu de l'arrondissement lui-même (présents dans le jeu publié sous le code arrondissement)
arr = c[c["code_insee"].str.match(r"751\d\d|6938\d|132\d\d")].set_index("code_insee")
for col in ["population_2023","part_65_plus_pct","revenu_median_uc","nb_audioprothesistes_2026"]:
    m = s["code_insee"].isin(arr.index)
    s.loc[m,col] = s.loc[m,"code_insee"].map(arr[col])
s["n_sites_commune"] = s.groupby("code_insee")["site_id"].transform("count")

# Concurrence : sites concurrents à 10 / 20 / 30 km (orthodromie, centroïdes communaux)
R=6371.0
def xyz(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.c_[R*np.cos(la)*np.cos(lo), R*np.cos(la)*np.sin(lo), R*np.sin(la)]
g = s.dropna(subset=["lat","lon"])
pts = xyz(g["lat"].values, g["lon"].values); tree = cKDTree(pts)
for km in (10,20,30):
    cnt = tree.query_ball_point(pts, 2*R*np.sin(km/(2*R)), return_length=True) - 1  # moins soi-même
    s.loc[g.index, f"concurrents_{km}km"] = cnt
# distance au site concurrent le plus proche (hors même site ; même commune = 0)
dd, ii = tree.query(pts, k=2)
s.loc[g.index, "dist_concurrent_km"] = np.round(2*R*np.arcsin(np.clip(dd[:,1]/(2*R),0,1)),1)
s["bande_concurrence"] = pd.cut(s["concurrents_30km"].fillna(-1), [-2,-0.5,0.5,2.5,9.5,1e9], labels=["n.d.","0 à 30 km","1-2","3-9","10+"])
s.to_csv("sites_audio_2026.csv", index=False)
print(len(s), "sites")
print(s["type"].value_counts()); print(); print(s["groupe"].value_counts().head(30))
print(); print(s["bande_concurrence"].value_counts())
print(); print(s[["n_praticiens","n_sites_commune","concurrents_30km","dist_concurrent_km","apl"]].describe().round(1))
print("sans coordonnées :", s["lat"].isna().sum())
