"""
Carte des communes prioritaires — métropole + encarts DOM.

Entrées : data/processed/communes_scoring_geo.csv (via join_codes.py)
          data/geo/communes-XX.geojson (référentiel france-geojson)
Sorties : outputs/maps/deserts_prioritaires.png (300 dpi)
          outputs/maps/deserts_prioritaires.svg (vectoriel)

Fond de carte : contours départementaux obtenus par dissolution des polygones
communaux (préfixe du code INSEE). Les 331 communes prioritaires sont figurées
par leur centroïde, taille proportionnelle à la population.
"""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
GEO = ROOT / "data" / "geo"
OUT = ROOT / "outputs" / "maps"

METRO = ["11", "24", "27", "28", "32", "44", "52", "53", "75", "76", "84", "93", "94"]
DOM = [("01", "Guadeloupe"), ("02", "Martinique"), ("03", "Guyane"),
       ("04", "La Réunion"), ("06", "Mayotte")]

COL_FOND = "#E8E6E1"
COL_TRAIT = "#FFFFFF"
COL_POINT = "#C0392B"


def load_region(code: str) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(GEO / f"communes-{code}.geojson")
    gdf["dep"] = gdf["code"].str[:2].where(~gdf["code"].str.startswith("97"),
                                           gdf["code"].str[:3])
    return gdf


def compute_prioritaires() -> pd.DataFrame:
    df = pd.read_csv(ROOT / "data" / "processed" / "communes_scoring_geo.csv",
                     dtype={"code_insee": str})
    audio = df["nb_audioprothesistes_2022"].fillna(0)
    revenu = df["revenu_median_uc"].fillna(25000)

    def norm(s, invert=False):
        s = pd.to_numeric(s, errors="coerce").fillna(0)
        mn, mx = s.min(), s.max()
        r = (s - mn) / (mx - mn) * 1000
        return (1000 - r) if invert else r

    pers = df["population"] * df["part_65_plus_pct"] / 100 * 0.65
    taux_eq = np.where(pers > 0, audio / (pers / 100), 0)
    p100 = np.clip((25000 - revenu) / 15000 * 100, 0, 100)
    score = (3 * norm(df["population"]) + 10 * norm(df["part_65_plus_pct"])
             + 5 * norm(df["densite_hab_km2"], True) + 8 * norm(revenu)
             + 2 * norm(df["loyer_m2"].fillna(0)) + 14 * norm(audio, True)
             + 9 * norm(df["hab_par_audio"].fillna(0).clip(upper=50000))
             + 5 * norm(df["nb_orl_liberaux_2022"].fillna(0))
             + 10 * norm(pd.Series(taux_eq, index=df.index), True)
             + 7 * norm(pd.Series(p100, index=df.index)))
    mask = (df["population"] >= 5000) & (audio == 0) & (score >= score.quantile(0.85))
    return df.loc[mask, ["commune", "region", "population", "code_insee"]].copy()


def main() -> None:
    prio = compute_prioritaires()
    assert len(prio) == 331, f"Attendu 331 prioritaires, trouvé {len(prio)}"

    fig = plt.figure(figsize=(11, 12))
    gs = fig.add_gridspec(2, 5, height_ratios=[4.2, 1.0], hspace=0.04, wspace=0.06)
    ax_metro = fig.add_subplot(gs[0, :])
    axes_dom = [fig.add_subplot(gs[1, i]) for i in range(5)]

    def size(pop):
        return 8 + (pop / 40000) * 55

    # ── Métropole ──
    metro_frames = [load_region(c) for c in METRO]
    metro = pd.concat(metro_frames, ignore_index=True)
    deps = metro.dissolve(by="dep")
    deps.plot(ax=ax_metro, color=COL_FOND, edgecolor=COL_TRAIT, linewidth=0.5)

    codes_metro = set(metro["code"])
    cent = metro.set_index("code").geometry.centroid
    pts = prio[prio["code_insee"].isin(codes_metro)]
    ax_metro.scatter(
        [cent[c].x for c in pts["code_insee"]],
        [cent[c].y for c in pts["code_insee"]],
        s=[size(p) for p in pts["population"]],
        color=COL_POINT, alpha=0.75, edgecolors="white", linewidths=0.4, zorder=5)
    ax_metro.set_axis_off()
    ax_metro.set_title(
        "Les déserts de l'audioprothèse : 331 communes prioritaires\n"
        "Communes de plus de 5 000 habitants sans audioprothésiste, "
        "classées dans le top 15 % du score d'opportunité",
        fontsize=13, pad=12)

    # ── Encarts DOM ──
    for ax, (code, nom) in zip(axes_dom, DOM):
        gdf = load_region(code)
        gdf.dissolve(by="dep").plot(ax=ax, color=COL_FOND,
                                    edgecolor=COL_TRAIT, linewidth=0.5)
        cent_d = gdf.set_index("code").geometry.centroid
        pts_d = prio[prio["code_insee"].isin(set(gdf["code"]))]
        if len(pts_d):
            ax.scatter([cent_d[c].x for c in pts_d["code_insee"]],
                       [cent_d[c].y for c in pts_d["code_insee"]],
                       s=[size(p) for p in pts_d["population"]],
                       color=COL_POINT, alpha=0.75,
                       edgecolors="white", linewidths=0.4, zorder=5)
        ax.set_axis_off()
        ax.set_title(f"{nom} ({len(pts_d)})", fontsize=8)

    # ── Légende & sources ──
    for pop, lbl in [(5000, "5 000 hab"), (15000, "15 000"), (35000, "35 000")]:
        ax_metro.scatter([], [], s=size(pop), color=COL_POINT, alpha=0.75,
                         edgecolors="white", linewidths=0.4, label=lbl)
    ax_metro.legend(title="Population", loc="lower left", frameon=False,
                    fontsize=8, title_fontsize=8)
    fig.text(0.5, 0.015,
             "Sources : INSEE Recensement 2021 (COG 2021) · Annuaire Santé (ADELI) 2022 · "
             "INSEE FILOSOFI — Traitement : N. Soussan, 2026 — Fond : france-geojson (OSM/Etalab)",
             ha="center", fontsize=7, color="#666666")

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "deserts_prioritaires.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUT / "deserts_prioritaires.svg", bbox_inches="tight")
    print(f"Cartes écrites dans {OUT.relative_to(ROOT)} — {len(prio)} communes figurées")


if __name__ == "__main__":
    main()
