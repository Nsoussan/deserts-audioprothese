# Ratings Without Exit: Online Reputation and the Option to Switch in a Credence Goods Market

**Working paper, version 2.1, 3 September 2026** · Nathan Soussan · companion to *L'accessibilité de l'audioprothèse en France* (v2.0, report doi:10.5281/zenodo.22177322, data doi:10.5281/zenodo.22177338, code doi:10.5281/zenodo.22177296).

- Paper: [`paper/Soussan_2026_Ratings_Without_Exit_WP_v2.pdf`](paper/Soussan_2026_Ratings_Without_Exit_WP_v2.pdf) (source `paper/paper_v2.md`, built with pandoc and xelatex).
- Earlier versions: `paper/Soussan_2026_Ratings_Without_Exit_WP.pdf` (v1.0, 3 September 2026, superseded).
- Data protection note: [`DATA-PROTECTION.md`](DATA-PROTECTION.md).

## What the paper does

Public rating systems discipline expert sellers in credence goods markets through the choices of prospective consumers, which presupposes that alternatives exist. The paper observes a rating system across the full range of the choice set. It rebuilds the 8,421 hearing-aid centres in France from the RPPS public extraction, measures the number of competing centres within 10 km of each, and collects Google ratings through the official Places API for a stratified sample of 2,999 centres that includes every centre with fewer than three competitors, together with the content of 2,702 provider websites and, as a benchmark, the ratings of 2,574 hairdressers in 879 of the same communes.

Main results (all descriptive): rating activity follows the choice set (median reviews 9 with no competitor within 10 km, 34 with ten or more; gradient robust to commune population, income, demand per centre, clustering by commune, and twice as steep as the hairdressers' in the same communes); rating levels sit near the ceiling everywhere, for centres and hairdressers alike; among the best-reviewed quarter of centres in each market, the cross-provider standard deviation of ratings is 0.14 to 0.15 with two or fewer competitors and 0.25 to 0.30 with three or more, a difference that survives a fixed window of review counts and a cluster bootstrap, and that hairdressers do not display; owner-operated centres collect 31 % fewer reviews than salaried ones conditional on competition and organisational form; price transparency on provider websites is a brand policy unrelated to local competition and to ratings.

## Pipeline

| Step | Script | Input | Output |
|---|---|---|---|
| 1. Site layer | `build_sites.py` | RPPS `PS_LibreAcces_Personne_activite` (August 2026), `../data/processed/communes_scoring_2026.csv`, `villes_centroides.json` | `sites_audio_2026.csv` (8,481 sites, not redistributed: names and addresses) |
| 2. Sample | stratified draw by competition band × group (all retail sites with 0 to 2 competitors, proportional draw elsewhere) | site layer | `sample_3000.csv` (2,999 sites; not redistributed, but the sampled sites, their stratum and weight are identified in `sites_public_v2.csv`, columns `strate` and `poids`) |
| 3. Google collection | `collect_places.py`, `requery_mismatches.py` | sample, `PLACES_API_KEY` | `places_raw.jsonl`, `places_matches.csv` (not redistributed, Google terms) |
| 4. Website reading and coding | `websites_collect.py`, `websites_code.py` | matched websites | `websites_pages.jsonl` (not redistributed), coded variables merged into the site layer |
| 5. Organisational form, owner flag, demand per site, APL v2.1 | `build_v2_vars.py` | site layer, `../data/processed/communes_scoring_2026_v21.csv` | `sites_v2.csv` (not redistributed), `sites_public_v2.csv` (published) |
| 6. Hairdresser benchmark | `collect_benchmark.py` | commune list, `PLACES_API_KEY` | `benchmark_raw.jsonl` (not redistributed) |
| 7. Analysis | `analysis_v2.py`, `analysis_v3.py` | steps 3 to 6 | `outputs/v2/results.txt`, `outputs/v2/results_v3.txt`, aggregated CSV tables |
| 8. Figures | `figures_v2.py` | step 7 | `outputs/v2/fig0_map.png`, `fig1_activity.png`, `fig2_content.png` |

`analyze_ratings.py`, `analyze_extended.py`, `analyze_websites.py` and the files in `outputs/` outside `v2/` belong to version 1.0 and are kept for traceability.

## Published data

`sites_public_v2.csv` is the minimised site layer described in Section 3.6 of the paper: one row per RPPS structure (8,481), with the commune codes, organisational form (`type5`), brand for chains and networks, owner flag, number of registered practitioners top-coded at 4, competition measures at 10, 20 and 30 km, alternatives within 10 km, population and population aged 65 and over within 10 km, demand per site, APL v2.1, entrant flag, sampling stratum and weight, and the coded website variables. It contains no name, address, registration number, telephone number or Google field.

`outputs/v2/brand_classification.csv` gives the keyword rules used to classify sites by brand and the five-way organisational typology (unbranded independent, brand network, integrated chain, optician-hosted, mutualist network).

Every aggregated table underlying the figures and the appendix is in `outputs/v2/`. Site-level Google fields (place identifiers, ratings, review counts, websites) and the raw website pages are not redistributed, in line with the Google Maps Platform terms and the data-minimisation choices set out in `DATA-PROTECTION.md`.

## Replication

Anyone with a Google Places API key can re-run steps 3 and 6 with `PLACES_API_KEY` set in the environment (two-step design: Text Search with IDs only, then Place Details; about 3,000 plus 2,600 Place Details calls). Ratings and review counts move with time; the paper's figures are a snapshot of 3 September 2026. The sample is fixed by the `strate` and `poids` columns of `sites_public_v2.csv`; the seeds of the benchmark draw and of the bootstraps are fixed in the scripts.

Python 3.11 with pandas, numpy, scipy, statsmodels and matplotlib.
