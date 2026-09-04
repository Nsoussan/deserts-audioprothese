"""Étape 5 bis : couche établissement publique minimisée, sites_public_v2.csv, à partir de sites_v2.csv (build_v2_vars.py),
sample_3000.csv (strate et poids du plan de sondage) et outputs/websites_coded.csv (variables de sites web codées).
Aucun nom, adresse, numéro de téléphone, identifiant de praticien ni champ Google. Voir DATA-PROTECTION.md.
Usage : python3 make_public_layer.py [--check]   (--check compare à la couche publiée sans l'écraser)."""
import sys, numpy as np, pandas as pd
s = pd.read_csv("sites_v2.csv", dtype={"code_insee":str,"code_insee_geo":str,"site_id":str})
smp = pd.read_csv("sample_3000.csv", dtype={"site_id":str})[["site_id","strate","poids"]]
w = pd.read_csv("outputs/websites_coded.csv", dtype={"site_id":str})
VARS = ["prix_affiche","grille_tarifs","sante100","classe2","essai_gratuit","bilan_gratuit","rdv_en_ligne","devis","garantie_suivi"]
w = w[["site_id","web_ok"]+VARS].copy()
for v in VARS: w[v] = np.where(w["web_ok"]==1, w[v], np.nan)
p = s.merge(smp, on="site_id", how="left").merge(w, on="site_id", how="left")
p["practitioners_topcoded_4"] = p["n_praticiens"].clip(upper=4)
out = p[["site_id","code_insee","code_insee_geo","commune","region","retail","type5","brand","owner_on_site","practitioners_topcoded_4",
         "concurrents_10km","concurrents_20km","concurrents_30km","alternatives_10km","dist_concurrent_km","n_sites_commune",
         "pop_10km","pop65_10km","demand65_per_site","apl_v21","entrant_commune","strate","poids","web_ok"]+VARS].rename(columns={"site_id":"rpps_structure_id"})
out["brand"] = out["brand"].fillna("")
if "--check" in sys.argv:
    old = pd.read_csv("sites_public_v2.csv", dtype=str)
    new = out.copy(); new.index = new["rpps_structure_id"]; old.index = old["rpps_structure_id"]
    common = [c for c in old.columns if c in new.columns]; diffs = {}
    for c in common:
        a = old[c].fillna("").astype(str).str.strip(); b = new.loc[old.index, c].fillna("").astype(str).str.strip()
        try:
            fa = pd.to_numeric(a.replace("", np.nan)); fb = pd.to_numeric(b.replace("", np.nan)); d = ~(np.isclose(fa, fb, equal_nan=True, atol=1e-6))
        except Exception:
            d = a != b
        diffs[c] = int(d.sum())
    print("lignes", len(old), len(new), "; colonnes absentes de la nouvelle :", [c for c in old.columns if c not in new.columns], "; différences par colonne :", {k: v for k, v in diffs.items() if v})
else:
    out.to_csv("sites_public_v2.csv", index=False); print(len(out), "structures écrites dans sites_public_v2.csv")
