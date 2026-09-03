#!/bin/bash
# Centres des 45 arrondissements municipaux (Paris, Lyon, Marseille) via l'API Découpage administratif (Etalab)
out="$(dirname "$0")/arrondissements_centroides.csv"
echo "code_insee,nom,code_ville,lat,lon" > "$out"
for ville in 75056 69123 13055; do
  url="https://geo.api.gouv.fr/communes?codeParent=$ville&type=arrondissement-municipal&fields=code,nom,centre&format=json"
  curl -sS -L -A "Mozilla/5.0" "$url" > /tmp/arr_$ville.json
  echo "--- $ville : $(head -c 200 /tmp/arr_$ville.json)"
  python3 -c "
import json,sys
d=json.load(open('/tmp/arr_$ville.json'))
for a in d: print(f\"{a['code']},{a['nom']},$ville,{a['centre']['coordinates'][1]},{a['centre']['coordinates'][0]}\")" >> "$out"
done
wc -l "$out"; head -4 "$out"
