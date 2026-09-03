"""Benchmark hors bien de confiance : notes Google des salons de coiffure dans les communes de l'échantillon.
Pour chaque commune retenue : Text Search « coiffeur » (IDs only, gratuit) biaisé sur le centroïde, 3 premiers résultats, puis Place Details.
Usage : python3 collect_benchmark.py [--limit N]   (clé dans PLACES_API_KEY). Sortie : benchmark_raw.jsonl"""
import argparse, json, os, sys, time, pandas as pd, numpy as np, requests
from collect_places import SEARCH, DETAILS, FIELDS_DETAILS, call, hav
ap = argparse.ArgumentParser(); ap.add_argument("--limit", type=int, default=0); ap.add_argument("--per_commune", type=int, default=3); a = ap.parse_args()
key = os.environ.get("PLACES_API_KEY") or sys.exit("PLACES_API_KEY absente")
s = pd.read_csv("outputs/v2/sample_analysis_v2.csv", dtype={"code_insee":str})
com = s.groupby("code_insee").agg(lat=("lat","first"), lon=("lon","first"), bande10=("bande10","first"), commune=("commune_rpps","first")).reset_index()
rng = np.random.default_rng(2026); parts=[com[com["bande10"]=="0"]]
for b in ["1-2","3-9","10+"]:
    g = com[com["bande10"]==b]; parts.append(g.sample(n=min(200, len(g)), random_state=int(rng.integers(1e9))))
todo = pd.concat(parts); done=set()
if os.path.exists("benchmark_raw.jsonl"):
    for line in open("benchmark_raw.jsonl", encoding="utf-8"): done.add(json.loads(line)["code_insee"])
todo = todo[~todo["code_insee"].isin(done)]
if a.limit: todo = todo.head(a.limit)
print(f"{len(com)} communes dans l'échantillon · {len(parts[0])} à 0 concurrent + 200 par autre bande · {len(todo)} à faire")
sess = requests.Session(); out = open("benchmark_raw.jsonl","a",encoding="utf-8"); t0=time.time()
for k,(_, r) in enumerate(todo.iterrows(),1):
    body = {"textQuery": f"coiffeur {r['commune']}", "languageCode":"fr", "regionCode":"FR", "pageSize": a.per_commune,
            "locationBias":{"circle":{"center":{"latitude":float(r["lat"]),"longitude":float(r["lon"])},"radius":3000}}}
    places=[]; raw={}
    try:
        res = call(sess,"POST",SEARCH,key,"places.id",body); raw["search"]=res
        for p0 in res.get("places",[])[:a.per_commune]:
            p = call(sess,"GET",DETAILS.format(id=p0["id"]),key,FIELDS_DETAILS); loc=p.get("location",{})
            dist = hav(float(r["lat"]),float(r["lon"]),loc["latitude"],loc["longitude"]) if loc else None
            places.append({"place_id":p0["id"],"name":p.get("displayName",{}).get("text"),"rating":p.get("rating"),"user_rating_count":p.get("userRatingCount"),
                           "primary_type":p.get("primaryType"),"business_status":p.get("businessStatus"),"dist_km": round(dist,2) if dist is not None else None})
    except Exception as e:
        raw["error"]=str(e); print("  !!", r["code_insee"], e)
    out.write(json.dumps({"code_insee":r["code_insee"],"commune":r["commune"],"bande10":r["bande10"],"collected_at":time.strftime("%Y-%m-%dT%H:%M:%S"),"places":places,"raw":raw}, ensure_ascii=False)+"\n"); out.flush()
    if k%50==0 or k==len(todo): print(f"  {k}/{len(todo)} · {time.time()-t0:.0f}s")
    time.sleep(0.05)
print("terminé : benchmark_raw.jsonl")
