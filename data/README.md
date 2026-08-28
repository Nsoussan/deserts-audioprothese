# Provenance des données

## Jeu publié

`processed/communes_scoring.csv` — 34 965 lignes (une par commune, COG INSEE
millésime 2021), 10 colonnes, 345 980 valeurs renseignées. Agrégé à la maille
communale : aucune donnée nominative, aucune adresse individuelle.

| Colonne | Description | Source primaire | Millésime |
|---|---|---|---|
| commune | Nom de la commune | INSEE COG | 2021 |
| region | Département / région d'appartenance | INSEE COG | 2021 |
| population | Population municipale | INSEE Recensement | 2021 |
| part_65_plus_pct | Part des 65 ans et plus (%) | INSEE Recensement | 2021 |
| densite_hab_km2 | Densité de population | INSEE | 2021 |
| revenu_median_uc | Revenu médian disponible par unité de consommation (€) | INSEE FILOSOFI | ~2021 ⚠️ à confirmer |
| loyer_m2 | Loyer d'annonce au m², parc privé (€) | Observatoire des loyers ⚠️ source exacte à confirmer | ~2022 |
| nb_audioprothesistes_2022 | Audioprothésistes installés | Annuaire Santé (ADELI, pré-bascule RPPS) | 2022 |
| hab_par_audio | Habitants par audioprothésiste | dérivé | — |
| nb_orl_liberaux_2022 | ORL libéraux | Annuaire Santé (ADELI) | 2022 |

## ⚠️ Vérifications à faire AVANT publication (checklist)

- [ ] Confirmer le millésime FILOSOFI exact utilisé lors de la collecte (2019 ? 2021 ?)
- [ ] Identifier la source exacte des loyers (CLAMEUR ? Observatoires locaux ?) et sa licence
- [ ] Vérifier pour chaque source le droit de redistribuer un jeu dérivé
      (INSEE et Annuaire Santé : Licence Ouverte 2.0, redistribution du dérivé permise
      avec mention de la source — à confirmer pour les loyers)
- [ ] Consigner ici le résultat de chaque vérification avec la date

## Note sur les données professionnelles

Les effectifs d'audioprothésistes et d'ORL ont été collectés en 2022, avant la
bascule de ces professions dans le répertoire RPPS (juin 2024). Ils
correspondent donc à l'ère ADELI / Annuaire Santé. Voir docs/limites.md, §2.

## Données brutes

Le répertoire `raw/` n'est pas versionné : la collecte d'origine (2022) a été
réalisée manuellement à partir des portails publics listés ci-dessus. Le jeu
`processed/` en est la consolidation. Toute mise à jour devra documenter son
protocole de collecte ici.

## Référentiel géographique (data/geo/)

Contours communaux par région, issus du projet
[france-geojson](https://github.com/gregoiredavid/france-geojson) (dérivé
OpenStreetMap / Etalab, licence ouverte). Utilisés par `src/join_codes.py`
pour l'appariement aux codes INSEE et par `src/make_map.py` pour la carte.
Le référentiel étant antérieur à certaines fusions de communes, une table de
corrections manuelles (documentée dans `src/join_codes.py`) traite les
communes nouvelles concernées.

`processed/communes_scoring_geo.csv` = jeu principal + colonnes `region_code`
et `code_insee` (appariement ~95 % ; les homonymes intra-région non résolus
restent sans code plutôt que d'être devinés).
