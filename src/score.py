"""
Scoring d'opportunité d'implantation en audioprothèse — 34 965 communes françaises.

Entrée  : data/processed/communes_scoring.csv
Sorties : outputs/tables/scores_communes.csv
          outputs/tables/deserts_prioritaires.csv
          outputs/tables/chiffres_cles.txt

Reproduit les chiffres clés du projet :
  - 34 965 communes analysées (COG INSEE, millésime 2021)
  - 742 communes de plus de 5 000 habitants sans aucun audioprothésiste
  - dont 331 classées prioritaires (top 15 % du score d'opportunité)
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "communes_scoring.csv"
OUT = ROOT / "outputs" / "tables"

# ── Pondérations (73 points au total) ────────────────────────────────────────
# La justification de chaque poids figure dans docs/methodologie.md.
WEIGHTS = {
    "n_population": 3,        # taille du marché
    "n_part_65": 10,          # structure d'âge — critère démographique central
    "n_densite_inv": 5,       # faible densité = moindre concurrence spatiale
    "n_revenu": 8,            # capacité de financement du reste à charge
    "n_loyer": 2,             # signal indirect du coût d'exploitation
    "n_nb_audio_inv": 14,     # concurrence directe — critère principal
    "n_hab_par_audio": 9,     # intensité du sous-équipement
    "n_orl": 5,               # présence de prescripteurs
    "n_taux_equip_inv": 10,   # saturation réelle du marché local
    "n_potentiel_100sante": 7 # part attendue de bénéficiaires du panier 100 % Santé
}

SEUIL_POP_DESERT = 5000       # « commune de plus de 5 000 habitants »
QUANTILE_PRIORITAIRE = 0.85   # top 15 % du score
PREVALENCE_65_PLUS = 0.65     # part des 65+ concernés par une perte auditive
CAP_HAB_PAR_AUDIO = 50000     # écrêtage du ratio pour limiter les valeurs extrêmes


def norm_minmax(s: pd.Series, invert: bool = False) -> pd.Series:
    """Normalisation min-max sur [0, 1000]. NaN traités comme 0 avant normalisation."""
    s = pd.to_numeric(s, errors="coerce").fillna(0)
    mn, mx = s.min(), s.max()
    if mx == mn:
        return pd.Series(np.zeros(len(s)), index=s.index)
    r = (s - mn) / (mx - mn) * 1000
    return (1000 - r) if invert else r


def main() -> None:
    df = pd.read_csv(DATA)
    assert len(df) == 34965, f"Attendu 34 965 communes, trouvé {len(df)}"

    audio = df["nb_audioprothesistes_2022"].fillna(0)
    # Imputation des revenus manquants à 25 000 € (ordre de grandeur de la médiane
    # nationale) — choix documenté dans docs/methodologie.md ; la sensibilité de ce
    # choix est discutée dans docs/limites.md (322 communes prioritaires avec une
    # imputation à la médiane observée, 331 avec 25 000 €).
    revenu = df["revenu_median_uc"].fillna(25000)

    # Variables dérivées
    pers_concernees = df["population"] * df["part_65_plus_pct"] / 100 * PREVALENCE_65_PLUS
    taux_equip = np.where(pers_concernees > 0, audio / (pers_concernees / 100), 0)
    potentiel_100sante = np.clip((25000 - revenu) / 15000 * 100, 0, 100)

    # Scores normalisés
    df["n_population"] = norm_minmax(df["population"])
    df["n_part_65"] = norm_minmax(df["part_65_plus_pct"])
    df["n_densite_inv"] = norm_minmax(df["densite_hab_km2"], invert=True)
    df["n_revenu"] = norm_minmax(revenu)
    df["n_loyer"] = norm_minmax(df["loyer_m2"])
    df["n_nb_audio_inv"] = norm_minmax(audio, invert=True)
    df["n_hab_par_audio"] = norm_minmax(df["hab_par_audio"].fillna(0).clip(upper=CAP_HAB_PAR_AUDIO))
    df["n_orl"] = norm_minmax(df["nb_orl_liberaux_2022"])
    df["n_taux_equip_inv"] = norm_minmax(pd.Series(taux_equip, index=df.index), invert=True)
    df["n_potentiel_100sante"] = norm_minmax(pd.Series(potentiel_100sante, index=df.index))

    # Score final
    df["score"] = sum(df[col] * w for col, w in WEIGHTS.items())
    df["rang"] = df["score"].rank(ascending=False, method="dense").astype(int)

    # Chiffres clés
    seuil_score = df["score"].quantile(QUANTILE_PRIORITAIRE)
    sans_audio_5000 = df[(df["population"] >= SEUIL_POP_DESERT) & (audio == 0)]
    prioritaires = sans_audio_5000[sans_audio_5000["score"] >= seuil_score]

    df["desert_5000"] = (df["population"] >= SEUIL_POP_DESERT) & (audio == 0)
    df["prioritaire"] = df["desert_5000"] & (df["score"] >= seuil_score)

    # Sorties
    OUT.mkdir(parents=True, exist_ok=True)
    cols_export = ["rang", "commune", "region", "population", "part_65_plus_pct",
                   "nb_audioprothesistes_2022", "score", "desert_5000", "prioritaire"]
    df.sort_values("score", ascending=False)[cols_export].to_csv(
        OUT / "scores_communes.csv", index=False, encoding="utf-8")
    prioritaires.sort_values("score", ascending=False)[
        ["commune", "region", "population", "part_65_plus_pct", "score"]
    ].to_csv(OUT / "deserts_prioritaires.csv", index=False, encoding="utf-8")

    lignes = [
        f"Communes analysées                                : {len(df):,}".replace(",", " "),
        f"Points de données du jeu publié (valeurs remplies) : {df[[c for c in df.columns if not c.startswith(('n_', 'score', 'rang', 'desert', 'prior'))]].notna().sum().sum():,}".replace(",", " "),
        f"Communes >= {SEUIL_POP_DESERT} hab sans audioprothésiste       : {len(sans_audio_5000)}",
        f"  dont prioritaires (top 15 % du score)           : {len(prioritaires)}",
    ]
    (OUT / "chiffres_cles.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print("\n".join(lignes))


if __name__ == "__main__":
    main()
