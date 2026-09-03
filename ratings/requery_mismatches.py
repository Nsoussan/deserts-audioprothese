"""Seconde passe : re-interroge les sites dont l'appariement est douteux, avec une requête reformulée
(nom de l'enseigne ou du groupe + « audioprothésiste » + commune). Même sortie, lignes ajoutées à places_raw.jsonl
(la dernière ligne d'un site fait foi dans l'analyse)."""
import json, os, sys, time, math, unicodedata, re, pandas as pd, requests
from collect_places import SEARCH, DETAILS, FIELDS_DETAILS, norm, hav, call
NONSTORE = {"local_government_office","hospital","dental_clinic","dentist","general_hospital","association_or_organization","corporate_office","medical_clinic","health"}
key = os.environ.get("PLACES_API_KEY") or sys.exit("PLACES_API_KEY absente")
s = pd.read_csv("sample_3000.csv", dtype={"code_insee":str,"code_postal":str,"siret":str})
last = {}
for line in open("places_raw.jsonl", encoding="utf-8"):
    rec = json.loads(line); last[rec["site_id"]] = rec
def doubtful(rec):
    b = rec.get("best")
    if not b: return True
    if (b.get("dist_centroide_km") or 99) > 10: return True
    if b.get("primary_type") in NONSTORE: return True
    if not b.get("name_match") and b.get("primary_type") not in {"store","electronics_store","doctor","medical_supply_store"}: return True
    return False
todo = s[s["site_id"].isin([k for k,v in last.items() if doubtful(v) and not v.get("requery")])]
print(f"{len(todo)} sites à re-interroger")
sess = requests.Session(); out = open("places_raw.jsonl","a",encoding="utf-8"); n_ok=0
for k,(_, r) in enumerate(todo.iterrows(),1):
    brand = r["groupe"] if r["groupe"]!="Indépendant / autre" else r["nom_site"]
    brand = re.sub(r"\(.*?\)", "", str(brand)).strip()
    text = f"{brand} audioprothésiste {r['commune_rpps']}"
    radius = 3000 if str(r["code_insee"])[:3] in ("751","693","132") else 8000
    body = {"textQuery": text, "languageCode":"fr", "regionCode":"FR", "pageSize":1,
            "locationBias":{"circle":{"center":{"latitude":float(r["lat"]),"longitude":float(r["lon"])},"radius":radius}}}
    best=None; raw={}
    try:
        res = call(sess,"POST",SEARCH,key,"places.id",body); raw["search"]=res
        if res.get("places"):
            pid = res["places"][0]["id"]; p = call(sess,"GET",DETAILS.format(id=pid),key,FIELDS_DETAILS); raw["details"]=p
            loc = p.get("location",{}); dist = hav(float(r["lat"]),float(r["lon"]),loc["latitude"],loc["longitude"]) if loc else None
            gname = p.get("displayName",{}).get("text","")
            name_ok = any(w in norm(gname) for w in norm(brand).split() if len(w)>3) or "AUDIO" in norm(gname) or "AUDITION" in norm(gname)
            best = {"place_id":pid,"g_name":gname,"g_address":p.get("formattedAddress"),"g_lat":loc.get("latitude"),"g_lon":loc.get("longitude"),
                    "rating":p.get("rating"),"user_rating_count":p.get("userRatingCount"),"website":p.get("websiteUri"),"business_status":p.get("businessStatus"),
                    "primary_type":p.get("primaryType"),"types":"|".join(p.get("types",[])),"dist_centroide_km":round(dist,2) if dist is not None else None,"name_match":bool(name_ok)}
            n_ok+=1
    except Exception as e:
        raw["error"]=str(e); print("  !!", r["site_id"], e)
    out.write(json.dumps({"site_id":r["site_id"],"query":text,"collected_at":time.strftime("%Y-%m-%dT%H:%M:%S"),"best":best,"raw":raw,"requery":True}, ensure_ascii=False)+"\n"); out.flush()
    if k%50==0 or k==len(todo): print(f"  {k}/{len(todo)} · trouvés {n_ok}")
    time.sleep(0.05)
print("terminé")
