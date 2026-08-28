#!/usr/bin/env bash
# Reproduit l'ensemble des résultats depuis le jeu de données publié.
set -euo pipefail
cd "$(dirname "$0")"
python3 src/score.py         # scores, 742/331, tables
python3 src/join_codes.py    # codes INSEE (référentiel dans data/geo/)
python3 src/make_map.py      # carte PNG + SVG
echo ""
echo "Terminé. Sorties :"
ls -1 outputs/tables/ outputs/maps/
