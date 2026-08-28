"""
Jointure des codes INSEE sur le jeu de données communal.

Le jeu source identifie les communes par (nom, région). Ce script les apparie
au Code officiel géographique via le référentiel france-geojson (dérivé
d'OpenStreetMap / Etalab) et produit data/processed/communes_scoring_geo.csv
avec une colonne code_insee.

Règles d'appariement :
  1. clé = (code région, nom normalisé) — accents, articles, "Saint/St" unifiés ;
  2. les homonymes intra-région du référentiel sont exclus de l'appariement
     automatique (aucune devinette) ;
  3. une table de corrections manuelles traite les communes nouvelles issues
     de fusions récentes, absentes du référentiel sous leur nom actuel, et
     l'homonymie Bompas (Pyrénées-Orientales vs Ariège) tranchée par la
     population.

Taux d'appariement obtenu : ~95 % des 34 965 communes, 100 % des 331
communes prioritaires.
"""

import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
GEO = ROOT / "data" / "geo"
SRC = ROOT / "data" / "processed" / "communes_scoring.csv"
DST = ROOT / "data" / "processed" / "communes_scoring_geo.csv"

REGION_SLUGS = {
    "11": "ile-de-france", "24": "centre-val-de-loire", "27": "bourgogne-franche-comte",
    "28": "normandie", "32": "hauts-de-france", "44": "grand-est",
    "52": "pays-de-la-loire", "53": "bretagne", "75": "nouvelle-aquitaine",
    "76": "occitanie", "84": "auvergne-rhone-alpes", "93": "provence-alpes-cote-d-azur",
    "94": "corse", "01": "guadeloupe", "02": "martinique", "03": "guyane",
    "04": "la-reunion", "06": "mayotte",
}

# Communes nouvelles (fusions) et homonymies tranchées à la main.
# Le code INSEE d'une commune nouvelle est celui de la commune chef-lieu.
MANUAL_CODES = {
    ("76", "bompas"): "66021",                       # P.-O. (l'homonyme ariégeois fait ~200 hab)
    ("11", "herblay-sur-seine"): "95306",            # ex-Herblay
    ("52", "chateau-gontier-sur-mayenne"): "53062",  # ex-Château-Gontier
    ("75", "marennes-hiers-brouage"): "17219",       # ex-Marennes
    ("75", "morcenx-la-nouvelle"): "40197",          # ex-Morcenx
    ("53", "lamballe-armor"): "22093",               # ex-Lamballe
    ("76", "st-christol-lez-ales"): "30243",         # variante lès/lez
    ("24", "controis-en-sologne"): "41059",          # ex-Contres
    ("52", "montaigu-vendee"): "85146",              # ex-Montaigu
    ("84", "valserhone"): "01033",                   # ex-Bellegarde-sur-Valserine
    ("75", "moncoutant-sur-sevre"): "79179",         # ex-Moncoutant
    ("84", "belleville-en-beaujolais"): "69019",     # ex-Belleville
}


def normalize(name: str) -> str:
    if not isinstance(name, str):
        return ""
    s = unicodedata.normalize("NFD", name.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"^(le |la |les |l')", "", s.strip())
    s = s.replace("saint-", "st-").replace("sainte-", "ste-")
    s = s.replace("saint ", "st-").replace("sainte ", "ste-")
    s = re.sub(r"[\s'’\-]+", "-", s).strip("-")
    return s


def main() -> None:
    df = pd.read_csv(SRC)
    df["region_code"] = df["region"].str.split(" - ").str[0].str.strip()
    df["_key"] = df["commune"].apply(normalize)

    ref: dict = {}
    ambiguous: set = set()
    for code in REGION_SLUGS:
        with open(GEO / f"communes-{code}.geojson", encoding="utf-8") as f:
            gj = json.load(f)
        for feat in gj["features"]:
            k = (code, normalize(feat["properties"]["nom"]))
            if k in ref and ref[k] != feat["properties"]["code"]:
                ambiguous.add(k)
            ref[k] = feat["properties"]["code"]
    for k in ambiguous:
        del ref[k]

    def lookup(row):
        k = (row["region_code"], row["_key"])
        return MANUAL_CODES.get(k) or ref.get(k)

    df["code_insee"] = df.apply(lookup, axis=1)
    matched = df["code_insee"].notna().sum()
    print(f"Appariées : {matched:,}/{len(df):,} ({matched / len(df) * 100:.1f} %)")
    print(f"Homonymes intra-région exclus de l'automatique : {len(ambiguous)}")

    df.drop(columns=["_key"]).to_csv(DST, index=False, encoding="utf-8")
    print(f"Écrit : {DST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
