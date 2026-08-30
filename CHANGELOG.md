# Journal des versions

## v2.0.0 — 30 août 2026

Refonte complète sur données 2026 ; le rapport (81 p) documente chaque point, l'annexe K en donne le tableau synthétique.

- **Sources** : bascule ADELI 2022 → RPPS (extraction août 2026, dédoublonnage identifiant × commune) ; populations de référence 2023 ; RP 2022 (effectifs exacts 65+) ; niveau de vie 2023 ; loyers 2024 ; géographie COG 2025 (34 900 communes, hors Mayotte — recensement reporté).
- **Nouveaux indicateurs** : APL (2SFCA) adaptée à la profession ; critère de distance au plus proche professionnel (poids 12, plafond 30 km) ; retrait du critère de densité ; seuil prioritaire calculé sur la strate ≥ 5 000 hab.
- **Validation** : rétrospective 2022-2026 (777 communes, AUC 0,597, p < 10⁻⁵) ; sensibilité systématique (±20 %, retraits, variantes d'APL, normalisation par rangs) ; croisement BPE 2025 (concordance 99 %) ; rétropolation à offre 2022 encadrée par bornes.
- **Données** : `communes_scoring_2026.csv` auto-suffisant (17 variables dont coordonnées, effectifs 2022 et APL) ; `analyses_2026.py` re-dérive et vérifie chaque chiffre par assertion.
- Chiffres clés : 742 → **560** communes ≥ 5 000 hab sans audioprothésiste ; 331 → **173** prioritaires (définitions non comparables, voir rapport §2.5).

## v1.0.0 — 28 août 2026

Version initiale : scoring à 10 critères sur données ADELI 2022, 34 965 communes (COG 2021), 742 communes ≥ 5 000 hab sans audioprothésiste dont 331 prioritaires.
