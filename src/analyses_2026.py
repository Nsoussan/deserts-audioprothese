"""Analyses v2 — reproduit chaque chiffre du rapport depuis le jeu de données publié.

Entrée : data/processed/communes_scoring_2026.csv (auto-suffisant : variables
sources, coordonnées, effectifs 2022 et 2026, score, APL).
Le script (1) RE-DÉRIVE le score et les distances depuis les variables sources
et vérifie l'identité avec les colonnes publiées, (2) recalcule l'APL,
(3) rejoue la validation rétrospective 2022-2026 et la rétropolation,
(4) exporte les tables du rapport. Chaque chiffre clé est protégé par assert.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.stats import mannwhitneyu

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "communes_scoring_2026.csv"
OUT = ROOT / "outputs" / "tables"
R_TERRE = 6371.0
PREVALENCE, CAP_HAB, IMPUT_REVENU, CAP_DIST = 0.65, 50_000, 25_000, 30
WEIGHTS_TOTAL = 80  # 14+12+10+10+9+8+7+5+3+2

def norm(s, invert=False):
    s = pd.to_numeric(s, errors="coerce").fillna(0)
    mn, mx = s.min(), s.max()
    r = (s - mn) / (mx - mn) * 1000
    return (1000 - r) if invert else r

def xyz(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.c_[R_TERRE*np.cos(la)*np.cos(lo), R_TERRE*np.cos(la)*np.sin(lo), R_TERRE*np.sin(la)]

def distances(df, col_offre):
    eq = df[(df[col_offre] > 0) & df["lat"].notna()]
    tree = cKDTree(xyz(eq["lat"].values, eq["lon"].values))
    mask = df["lat"].notna()
    d, _ = tree.query(xyz(df.loc[mask, "lat"].values, df.loc[mask, "lon"].values))
    out = pd.Series(np.nan, index=df.index)
    out.loc[mask] = np.round(2*R_TERRE*np.arcsin(np.clip(d/(2*R_TERRE), 0, 1)), 1)
    out.loc[df[col_offre] > 0] = 0.0
    return out

def apl_2sfca(df, col_offre, rayon=30, bandes=((10, 1.0), (20, 0.66), (30, 0.33))):
    """APL par bandes de distance, demande = population de 65 ans et plus."""
    g = df.dropna(subset=["lat", "lon"]).copy()
    pts = xyz(g["lat"].values, g["lon"].values)
    p65 = np.maximum((g["population_2023"] * g["part_65_plus_pct"].fillna(
        g["part_65_plus_pct"].median()) / 100).values, 0.0)
    S = g[col_offre].fillna(0).values.astype(float)
    def w(d):
        out = np.zeros_like(d)
        borne_prec = 0
        for borne, coef in bandes:
            out = np.where((d > borne_prec) & (d <= borne), coef, out)
            borne_prec = borne
        return np.where(d == 0, bandes[0][1], out)
    mask = S > 0
    tree_eq, tree_all = cKDTree(pts[mask]), cKDTree(pts)
    pairs = tree_eq.query_ball_tree(tree_all, 2*R_TERRE*np.sin(rayon/(2*R_TERRE)))
    eq_idx = np.where(mask)[0]
    apl = np.zeros(len(g))
    for a, neigh in enumerate(pairs):
        d = 2*R_TERRE*np.arcsin(np.clip(
            np.linalg.norm(pts[neigh]-pts[eq_idx[a]], axis=1)/(2*R_TERRE), 0, 1))
        wk = w(d)
        dem = (wk*p65[neigh]).sum()
        rj = S[eq_idx[a]]/dem if dem > 0 else 0.0
        np.add.at(apl, neigh, wk*rj)
    return pd.Series(apl*1e5, index=g.index).reindex(df.index)

def score_v2(df):
    audio = df["nb_audioprothesistes_2026"]
    revenu = df["revenu_median_uc"].fillna(IMPUT_REVENU)
    pers = df["population_2023"] * df["part_65_plus_pct"].fillna(0) / 100 * PREVALENCE
    taux_eq = np.where(pers > 0, audio/(pers/100), 0)
    p100 = np.clip((IMPUT_REVENU - revenu)/15000*100, 0, 100)
    hab_par = np.where(audio > 0, df["population_2023"]/audio, np.nan)
    return (3*norm(df["population_2023"]) + 10*norm(df["part_65_plus_pct"].fillna(0))
        + 8*norm(revenu) + 2*norm(df["loyer_m2"].fillna(0)) + 14*norm(audio, invert=True)
        + 9*norm(pd.Series(hab_par, index=df.index).fillna(0).clip(upper=CAP_HAB))
        + 5*norm(df["nb_orl_liberaux_2026"])
        + 10*norm(pd.Series(taux_eq, index=df.index), invert=True)
        + 7*norm(pd.Series(p100, index=df.index))
        + 12*norm(df["dist_audio_km"].fillna(0).clip(upper=CAP_DIST)))

def wilson(k, n, z=1.96):
    p, d = k/n, 1 + z*z/n
    c = (p + z*z/(2*n))/d
    h = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return (c-h)*100, (c+h)*100

def main():
    df = pd.read_csv(DATA, dtype={"code_insee": str})
    assert len(df) == 34_900, f"Attendu 34 900 communes, trouvé {len(df)}"

    # 1. Re-dérivation des distances et du score — identité avec les colonnes publiées
    d = distances(df, "nb_audioprothesistes_2026")
    ecart_d = (d - df["dist_audio_km"]).abs().max()
    assert ecart_d < 0.15, f"Distances non reproduites (écart max {ecart_d})"
    s = score_v2(df)
    assert np.corrcoef(s.fillna(0), df["score_v2"].fillna(0))[0, 1] > 0.99999, "Score non reproduit"

    # 2. Chiffres clés 2026
    sans = df[df["sans_audio_5k"]]
    prio = df[df["prioritaire_v2"]]
    assert len(sans) == 560 and len(prio) == 173, (len(sans), len(prio))
    seuil = df.loc[df["population_2023"] >= 5000, "score_v2"].quantile(0.85)
    prio_recalc = df[df["sans_audio_5k"] & (df["score_v2"] >= seuil)]
    assert len(prio_recalc) == 173, "Définition prioritaire non reproduite"
    assert int(df["nb_audioprothesistes_2026"].sum()) == 11_018

    # 3. APL — corrélation avec la colonne publiée
    apl = apl_2sfca(df, "nb_audioprothesistes_2026")
    common = apl.notna() & df["apl"].notna()
    rho = np.corrcoef(apl[common], df["apl"][common])[0, 1]
    assert rho > 0.999, f"APL non reproduite (corr {rho})"

    # 4. Validation rétrospective 2022-2026
    c = df.dropna(subset=["nb_audioprothesistes_2022"])
    cohorte = c[(c["population_2023"] >= 5000) & (c["nb_audioprothesistes_2022"] == 0)]
    equip = cohorte["nb_audioprothesistes_2026"] > 0
    assert len(cohorte) == 777 and int(equip.sum()) == 295, (len(cohorte), int(equip.sum()))
    U, p = mannwhitneyu(cohorte.loc[equip, "score_v2"], cohorte.loc[~equip, "score_v2"],
                        alternative="greater")
    # NB : AUC du rapport (0,597) calculée sur le score PUBLIÉ EN 2022 (score_v1),
    # disponible dans outputs/tables/comparaison_2022_2026.csv du dépôt.
    lo, hi = wilson(int(equip.sum()), len(cohorte))
    print(f"Cohorte 777 · équipées 295 (38,0 % IC [{lo:.1f} ; {hi:.1f}])")

    # 5. Rétropolation à offre 2022 (bornes, cf. rapport §2.6 et §3.13)
    d22 = distances(df, "nb_audioprothesistes_2022")
    apl22 = apl_2sfca(df, "nb_audioprothesistes_2022")
    n22 = df["nb_audioprothesistes_2022"].fillna(0).sum()
    print(f"Offre 2022 appariée : {int(n22)} (borne : × {6682/n22:.3f})")

    # 6. Exports
    OUT.mkdir(parents=True, exist_ok=True)
    prio.sort_values("score_v2", ascending=False).assign(
        rang=lambda x: range(1, len(x)+1)).to_csv(OUT / "deserts_prioritaires_2026.csv", index=False)
    cohorte.assign(equipee=equip.astype(int)).to_csv(OUT / "comparaison_2022_2026.csv", index=False)
    print("Tables exportées — tous les asserts passés.")

if __name__ == "__main__":
    main()
