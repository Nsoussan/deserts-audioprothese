# Journal des versions

## v2.2.0 — 4 septembre 2026

- **Document de travail v2.2** (`ratings/paper/Soussan_2026_Ratings_Without_Exit_WP_v2_2.pdf`, DOI toutes versions 10.5281/zenodo.22286005) après un troisième tour d'audit (dix relecteurs indépendants : referee, réplication chiffre par chiffre, juridique, reproductibilité, relecture anglaise, figures, métadonnées, expert du marché, lecteur hostile, destinataire). Principales corrections : le titre est défini comme un raccourci (le centre sans concurrent à 10 km a son plus proche confrère à 13,6 km en médiane) ; le résultat de dispersion est formulé comme une compression de moitié, non comme une absence, et rapporté avec le niveau pondéré par les avis, la dispersion par tranche d'avis et l'effet plafond ; les variantes sans opticiens (Levene p = 0,09, modèle de queue basse −0,07) et les coefficients de forme du PPML sont rapportés ; le drapeau « propriétaire » est redéfini comme le rôle RPPS « titulaire de cabinet » ; Audilab (groupe Demant) et l'hétérogénéité des corners opticiens sont signalés ; la page prix d'Amplifon, qui affiche le plafond de classe I et une fourchette de classe II non comptés par le codeur, corrige l'affirmation « aucun montant » ; la garantie de quatre ans vaut pour les deux classes et le reste à charge nul suppose un contrat responsable ; conversion « un tiers d'avis en plus » corrigée en 31 % de moins ; 639 domaines ; 880 communes interrogées pour 879 retenues ; ligne « une structure par fiche Google » retirée faute de sortie reproductible ; date de lecture des sites corrigée (3 septembre) ; section protection des données réécrite (la couche publique est joignable au registre) ; déclaration d'intérêts complétée ; affiliation et contact ; abstract raccourci ; tableaux et figure 3 relus pour la lisibilité ; DOI « toutes versions » dans l'en-tête.
- `ratings/DATA-PROTECTION.md` réécrit (responsable, base juridique, catégories, durées de conservation, droits, article 14). `ratings/README.md` : pipeline décrit avec ses étapes non scriptées. Licences précisées dans le README racine ; entrée BibTeX du document de travail.

## v2.1.1 — 3 septembre 2026

- DOI Zenodo du document de travail inséré dans le PDF, les README et ce journal. Aucun changement de code ni de données.

## v2.1.0 — 3 septembre 2026

- **Correction** : les 45 arrondissements municipaux de Paris, Lyon et Marseille (3,5 M d'habitants, environ 800 activités) n'avaient pas de centroïde en v2.0 et étaient absents du calcul 2SFCA, comme offre et comme demande. Ils sont géocodés (`data/geo/arrondissements_centroides.csv`, API Découpage administratif) et l'APL est recalculée (`src/apl_v21.py`, sortie `data/processed/communes_scoring_2026_v21.csv`). Classements inchangés (corrélation de rang 0,999 ; 560 communes sans offre et 88 communes à APL nulle identiques) ; APL pondérée Île-de-France 92 → 100, Paris 131, Lyon 134, Marseille 109 ; 413 communes bougent de plus de 5 points, surtout autour d'Aix-en-Provence (`outputs/tables/apl_v20_v21_comparaison.csv`).
- **Nouveau** : couche établissement (8 481 sites RPPS, dont 8 421 en appareillage médical) et étude des notes Google et du contenu des sites web selon la concurrence locale, dossier `ratings/` et document de travail *Ratings without exit* (`ratings/paper/`).
- **Document de travail v2.1** (`ratings/paper/Soussan_2026_Ratings_Without_Exit_WP_v2.pdf`, 27 p, DOI de version 10.5281/zenodo.22286120 ; première mise en ligne 10.5281/zenodo.22286008) : typologie organisationnelle en cinq formes issue du registre (part de titulaires), effet titulaire sur le volume d'avis, benchmark de 2 574 salons de coiffure dans 879 des mêmes communes, dispersion des notes parmi le quart des sites les plus commentés de chaque bande de concurrence (bootstrap par commune, fenêtre fixe d'avis), effets fixes commune, PPML, traçabilité des identifiants Google. Deux tours d'audit critique ; les résultats restent descriptifs.
- **Minimisation des données** : la couche établissement publiée est `ratings/sites_public_v2.csv` (identifiant de structure, commune, forme, enseigne, mesures de concurrence, strate et poids, variables de sites web codées ; aucun nom, adresse, numéro ni champ Google). Les fichiers de travail avec noms et adresses (`sites_audio_2026.csv`, `sample_3000.csv`, `sites_retail_alternatives.csv`, `outputs/websites_coded.csv`) ne sont plus versionnés (`.gitignore`) ; ils figurent dans l'historique des commits antérieurs à v2.1.0, voir `ratings/DATA-PROTECTION.md`.

## v2.0.0 — 30 août 2026

Refonte complète sur données 2026 ; le rapport (81 p) documente chaque point, l'annexe K en donne le tableau synthétique.

- **Sources** : bascule ADELI 2022 → RPPS (extraction août 2026, dédoublonnage identifiant × commune) ; populations de référence 2023 ; RP 2022 (effectifs exacts 65+) ; niveau de vie 2023 ; loyers 2024 ; géographie COG 2025 (34 900 communes, hors Mayotte — recensement reporté).
- **Nouveaux indicateurs** : APL (2SFCA) adaptée à la profession ; critère de distance au plus proche professionnel (poids 12, plafond 30 km) ; retrait du critère de densité ; seuil prioritaire calculé sur la strate ≥ 5 000 hab.
- **Validation** : rétrospective 2022-2026 (777 communes, AUC 0,597, p < 10⁻⁵) ; sensibilité systématique (±20 %, retraits, variantes d'APL, normalisation par rangs) ; croisement BPE 2025 (concordance 99 %) ; rétropolation à offre 2022 encadrée par bornes.
- **Données** : `communes_scoring_2026.csv` auto-suffisant (17 variables dont coordonnées, effectifs 2022 et APL) ; `analyses_2026.py` re-dérive et vérifie chaque chiffre par assertion.
- Chiffres clés : 742 → **560** communes ≥ 5 000 hab sans audioprothésiste ; 331 → **173** prioritaires (définitions non comparables, voir rapport §2.5).

## v1.0.0 — 28 août 2026

Version initiale : scoring à 10 critères sur données ADELI 2022, 34 965 communes (COG 2021), 742 communes ≥ 5 000 hab sans audioprothésiste dont 331 prioritaires.
