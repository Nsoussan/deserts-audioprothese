# Ratings Without Exit: Online Reputation and the Option to Switch in a Credence Goods Market

**Working paper, version 2.2, 4 September 2026** · Nathan Soussan · doi:[10.5281/zenodo.22286005](https://doi.org/10.5281/zenodo.22286005) (all versions; resolves to the latest) · companion to *L'accessibilité de l'audioprothèse en France* (v2.0, report doi:10.5281/zenodo.22177322, data doi:10.5281/zenodo.22177338, code doi:10.5281/zenodo.22177296).

- Paper: [`paper/Soussan_2026_Ratings_Without_Exit_WP_v2_2.pdf`](paper/Soussan_2026_Ratings_Without_Exit_WP_v2_2.pdf) (source `paper/paper_v2.md`, built with pandoc and xelatex).
- Earlier versions, superseded: v2.1 (3 September 2026, `paper/Soussan_2026_Ratings_Without_Exit_WP_v2.pdf`, Zenodo 10.5281/zenodo.22286120 and 10.5281/zenodo.22286008), v1.0 (3 September 2026, `paper/Soussan_2026_Ratings_Without_Exit_WP.pdf`). The paper's version number follows the minor version of the repository; repository patch releases do not change the paper.
- Data protection notice: [`DATA-PROTECTION.md`](DATA-PROTECTION.md).
- Licences: paper CC BY 4.0; scripts MIT; `sites_public_v2.csv` and the tables in `outputs/` Licence Ouverte 2.0 (derived from the RPPS public extraction, Agence du Numérique en Santé, August 2026).

## What the paper does

Public rating systems discipline expert sellers in credence goods markets through the choices of prospective consumers, which presupposes that alternatives exist. The paper observes a rating system across the full range of the choice set. It rebuilds the population of 8,421 hearing-aid centres in France from the RPPS public extraction, counts the competing centres within 10 km of each, and collects Google ratings through the official Places API for a stratified sample of 2,999 centres that includes every centre with fewer than three competitors, together with the content of 2,702 provider websites and, as a benchmark, the ratings of 2,574 hairdressers in 879 of the same communes.

Main results (all descriptive): rating activity follows the choice set (median reviews 9 with no competitor within 10 km, 34 with ten or more; robust to commune population, income, demand per centre and clustering by commune, and twice as steep as the hairdressers' in the same communes); rating levels sit near the ceiling everywhere, for centres and hairdressers alike; among the quarter of centres with the most reviews within each competition band, the standard deviation of ratings across centres is 0.14 to 0.15 with two or fewer competitors and 0.25 to 0.30 with three or more, a difference that survives a fixed window of review counts and a bootstrap by commune and that hairdressers do not show; established centres in thin markets are rated higher, not lower; centres whose practitioner is registered as practice holder collect 31% fewer reviews than centres with salaried practitioners, conditional on competition and form; price information on provider websites is set nationally by the chains, does not vary with local competition among independents, and is unrelated to ratings.

## Pipeline

Scripts run from `ratings/`. Steps marked (not scripted) were one-off operations whose result is fixed by the published files.

| Step | Script | Input | Output |
|---|---|---|---|
| 1. Site layer | `build_sites.py` | `rpps_audio_lignes.csv` (rows of *Personne_activite* filtered on the profession label; filtering not scripted; not redistributed), `villes_centroides.json`, `../data/processed/communes_scoring_2026.csv` (the script expects the repository at `~/mnt/deserts-audioprothese`) | `sites_audio_2026.csv` (8,481 sites; not redistributed: names, addresses, telephone numbers). Arrondissements of Paris, Lyon and Marseille are attached to the city centroid for the competition measures |
| 2. Sample | stratified draw by competition band × group, all retail sites with 0 to 2 competitors plus a proportional draw elsewhere (not scripted) | site layer | `sample_3000.csv` (2,999 sites; not redistributed). The drawn sites, their stratum and weight are identified in `sites_public_v2.csv`, columns `strate` and `poids`, which fix the sample |
| 3. Google collection | `collect_places.py`, `requery_mismatches.py` | sample, `PLACES_API_KEY` | `places_raw.jsonl`, `places_matches.csv` (not redistributed, Google Maps Platform terms). Match validation and flattening into `outputs/sites_ratings_sample.csv` are done by `analyze_ratings.py` (v1.0 script) |
| 4. Website reading and coding | `websites_collect.py`, `websites_code.py` | `outputs/sites_ratings_sample.csv` | `websites_pages.jsonl`, `outputs/websites_coded.csv` (not redistributed: domains); merged into `outputs/sites_ratings_sample_web.csv` by `analyze_websites.py` (v1.0 script) |
| 5. Organisational form, practice-holder flag, alternatives, entrants, demand per site, APL v2.1 | `build_v2_vars.py` | `sites_audio_2026.csv`, `sites_retail_alternatives.csv` (alternatives, same-brand sites, 2022 counts, entrant flag; not scripted), `../data/processed/communes_scoring_2026_v21.csv` | `sites_v2.csv` (not redistributed); `sites_public_v2.csv` is the minimised layer derived from it (column list below; minimisation step not scripted) |
| 6. Hairdresser benchmark | `collect_benchmark.py` | `outputs/v2/sample_analysis_v2.csv` (written by `analysis_v2.py`, so step 7 runs once before step 6), `PLACES_API_KEY` | `benchmark_raw.jsonl`, flattened into `outputs/v2/benchmark_coiffeurs.csv` (not redistributed) |
| 7. Analysis | `analysis_v2.py`, `analysis_v3.py` | steps 3 to 6 | `outputs/v2/results.txt`, `outputs/v2/results_v3.txt`, aggregated CSV tables |
| 8. Figures | `figures_v2.py` | step 7 | `outputs/v2/fig0_map.png` (Figure 1), `fig1_activity.png` (Figure 2), `fig2_content.png` (Figure 3); 95% intervals recomputed at run time (seed 11, 200 replications) |

`analyze_ratings.py`, `analyze_extended.py`, `analyze_websites.py` and the published files in `outputs/` outside `v2/` belong to version 1.0 and are kept for traceability; two of them (`analyze_ratings.py`, `analyze_websites.py`) are still used in steps 3 and 4. Seeds: benchmark commune draw 2026; residual-dispersion bootstrap 7 (300 replications); round-two bootstraps 21 (500); figure intervals 11 (200). The seed of the sample draw is not available.

Tables 2, 3 and A1 of the paper are available as text in `outputs/v2/results.txt` and `results_v3.txt`; `outputs/v2/benchmark_by_band.csv` and `outputs/v2/brand_classification.csv` were written from the printed output of `analysis_v2.py` and `build_v2_vars.py`.

## Published data

`sites_public_v2.csv` is the minimised site layer described in Sections 3.1 and 3.6 of the paper: one row per RPPS structure (8,481), with the register's structure identifier (`rpps_structure_id`), the commune codes and name, the retail flag (`retail`; the 60 excluded structures are the rows with `retail = False`), organisational form (`type5`), brand for chains and networks, practice-holder flag (`owner_on_site`), number of registered practitioners top-coded at 4, competition measures at 10, 20 and 30 km, alternatives within 10 km, distance to the nearest other site, population and population aged 65 and over within 10 km, demand per site, APL v2.1, entrant flag, sampling stratum and weight (`strate`, `poids`; labels `enseigne nationale` = branded, `indépendant` = unbranded independent, `mutualiste` = mutualist), and the coded website variables. It contains no name, address, registration number, telephone number or Google field. Because the structure identifier is public, the file is linkable to the register; see `DATA-PROTECTION.md`.

`outputs/v2/brand_classification.csv` gives, for each brand, the number of sites, the share with a practice holder and the resulting class. The keyword rules and legal-name mapping are the `RULES` list of `build_sites.py`.

The aggregated tables behind Figures 2 and 3 and Tables 1, 4, A2 and A4 to A7 are in `outputs/v2/`. Site-level Google fields (place identifiers, ratings, review counts, websites) and the raw website pages are not redistributed, because the Google Maps Platform terms do not permit the redistribution of Places content and because of the data-minimisation choices set out in `DATA-PROTECTION.md`.

## Replication

Anyone with a Google Places API key can re-run steps 3 and 6 with `PLACES_API_KEY` set in the environment (two-step design: Text Search returning identifiers only, then Place Details; about 3,200 Place Details calls for the centres including re-queries, and about 880 Text Search plus 2,600 Place Details calls for the benchmark). Ratings and review counts move with time; the paper's figures are a snapshot of 3 September 2026. The author's working copies of the API responses are kept only for the duration stated in `DATA-PROTECTION.md`.

Python 3.11 with pandas, numpy, scipy, statsmodels, matplotlib and requests (versions used: see `../requirements.txt`).
