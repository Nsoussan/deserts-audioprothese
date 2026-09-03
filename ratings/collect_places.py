"""Collecte des notes Google (Places API New) pour un échantillon de sites d'audioprothèse, en deux temps.

  1. Text Search, masque « places.id » seul (SKU IDs only)          -> identifiant du lieu
  2. Place Details, masque complet (SKU Place Details Enterprise)    -> nom, adresse, note, nb d'avis, site web, statut

Usage (Terminal du Mac, clé dans PLACES_API_KEY) :
    python3 collect_places.py --sample sample_3000.csv --limit 20     # test
    python3 collect_places.py --sample sample_3000.csv                # tout, reprise automatique

Sorties : places_raw.jsonl (réponses brutes + diagnostics), places_matches.csv (table plate).
API officielle, aucun scraping. Vérifier la grille tarifaire avant lancement complet.
"""
import argparse, json, os, sys, time, math, unicodedata, re
import pandas as pd, requests

SEARCH = "https://places.googleapis.com/v1/places:searchText"
DETAILS = "https://places.googleapis.com/v1/places/{id}"
FIELDS_DETAILS = ("id,displayName,formattedAddress,location,rating,userRatingCount,websiteUri,"
                  "businessStatus,primaryType,types")

def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii","ignore").decode().upper()
    return re.sub(r"[^A-Z0-9 ]+", " ", s)

def hav(lat1, lon1, lat2, lon2):
    R=6371.0; p=math.pi/180
    a = math.sin((lat2-lat1)*p/2)**2 + math.cos(lat1*p)*math.cos(lat2*p)*math.sin((lon2-lon1)*p/2)**2
    return 2*R*math.asin(math.sqrt(a))

def call(session, method, url, key, mask, body=None):
    h = {"Content-Type": "application/json", "X-Goog-Api-Key": key, "X-Goog-FieldMask": mask}
    for attempt in range(5):
        r = session.post(url, headers=h, json=body, timeout=30) if method=="POST" else session.get(url, headers=h, timeout=30)
        if r.status_code == 200: return r.json()
        if r.status_code in (429, 500, 502, 503, 504): time.sleep(2*(attempt+1)); continue
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")
    raise RuntimeError("trop de tentatives")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", default="sample_3000.csv")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--sleep", type=float, default=0.05)
    a = ap.parse_args()
    key = os.environ.get("PLACES_API_KEY")
    if not key: sys.exit("PLACES_API_KEY absente de l'environnement")
    sites = pd.read_csv(a.sample, dtype={"code_insee":str,"code_postal":str,"siret":str})
    done = set()
    if os.path.exists("places_raw.jsonl"):
        for line in open("places_raw.jsonl", encoding="utf-8"):
            try: done.add(json.loads(line)["site_id"])
            except Exception: pass
    todo = sites[~sites["site_id"].isin(done)]
    if a.limit: todo = todo.head(a.limit)
    print(f"{len(sites)} sites dans l'échantillon, {len(done)} déjà collectés, {len(todo)} à faire")
    s = requests.Session(); out = open("places_raw.jsonl", "a", encoding="utf-8")
    n_ok = n_none = n_err = 0; t0 = time.time()
    for k, (_, r) in enumerate(todo.iterrows(), 1):
        text = f"{r['nom_site']} {r['adresse']} {r['code_postal']} {r['commune_rpps']}".strip()
        radius = 3000 if str(r["code_insee"])[:3] in ("751","693","132") else 8000
        body = {"textQuery": text, "languageCode": "fr", "regionCode": "FR", "pageSize": 1,
                "locationBias": {"circle": {"center": {"latitude": float(r["lat"]), "longitude": float(r["lon"])}, "radius": radius}}}
        best = None; raw = {}
        try:
            res = call(s, "POST", SEARCH, key, "places.id", body); raw["search"] = res
            places = res.get("places", [])
            if places:
                pid = places[0]["id"]
                p = call(s, "GET", DETAILS.format(id=pid), key, FIELDS_DETAILS); raw["details"] = p
                loc = p.get("location", {})
                dist = hav(float(r["lat"]), float(r["lon"]), loc["latitude"], loc["longitude"]) if loc else None
                gname = p.get("displayName",{}).get("text","")
                name_ok = any(w in norm(gname) for w in norm(r["nom_site"]).split() if len(w) > 3)
                best = {"place_id": pid, "g_name": gname, "g_address": p.get("formattedAddress"),
                        "g_lat": loc.get("latitude"), "g_lon": loc.get("longitude"), "rating": p.get("rating"),
                        "user_rating_count": p.get("userRatingCount"), "website": p.get("websiteUri"),
                        "business_status": p.get("businessStatus"), "primary_type": p.get("primaryType"),
                        "types": "|".join(p.get("types", [])), "dist_centroide_km": round(dist,2) if dist is not None else None,
                        "name_match": bool(name_ok)}
                n_ok += 1
            else:
                n_none += 1
        except Exception as e:
            n_err += 1; raw["error"] = str(e); print(f"  !! {r['site_id']} {e}")
            if n_err >= 10 and n_ok == 0: sys.exit("10 erreurs d'affilée : vérifier la clé / la facturation")
        rec = {"site_id": r["site_id"], "query": text, "collected_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "best": best, "raw": raw}
        out.write(json.dumps(rec, ensure_ascii=False) + "\n"); out.flush()
        if k % 100 == 0 or k == len(todo):
            print(f"  {k}/{len(todo)} · trouvés {n_ok} · vides {n_none} · erreurs {n_err} · {time.time()-t0:.0f}s")
        time.sleep(a.sleep)
    out.close()
    rows = []
    for line in open("places_raw.jsonl", encoding="utf-8"):
        rec = json.loads(line); b = rec.get("best") or {}
        rows.append({"site_id": rec["site_id"], "query": rec["query"], "collected_at": rec["collected_at"], **b})
    pd.DataFrame(rows).to_csv("places_matches.csv", index=False)
    print("écrit : places_raw.jsonl, places_matches.csv")

if __name__ == "__main__":
    main()
