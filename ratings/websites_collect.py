"""Collecte du contenu des sites web des centres (pages publiques, lecture seule, rythme lent).

Deux niveaux : (1) la page exacte référencée par la fiche Google de chaque site ; (2) pour chaque domaine, la page d'accueil
et jusqu'à trois pages internes dont l'adresse ou le libellé évoque les tarifs, le 100 % Santé ou l'essai.
Usage (Terminal du Mac) :  python3 websites_collect.py [--limit N]
Sorties : websites_pages.jsonl (une ligne par page lue : url, statut, texte normalisé tronqué à 60 000 caractères)
Reprise automatique. Respecte un délai de 0,7 s entre requêtes et ignore les domaines dont robots.txt interdit tout.
"""
import argparse, json, os, re, sys, time, unicodedata, html
from urllib.parse import urlparse, urljoin
import pandas as pd, requests

UA = {"User-Agent": "Mozilla/5.0 (compatible; etude-accessibilite-audioprothese/1.0; contact: nsoussan0@gmail.com)"}
KEYS = re.compile(r"tarif|prix|price|100[- ]?sante|100-?%|classe|offre|essai|garantie|rembours|remboursement|devis|aide|financ", re.I)
SKIP_DOM = ("facebook.com","instagram.com","linkedin.com","google.","business.site","pagesjaunes.fr")

def norm_text(s):
    s = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", s, flags=re.S|re.I)
    s = re.sub(r"<[^>]+>", " ", s); s = html.unescape(s)
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().lower()
    return re.sub(r"\s+", " ", s).strip()

def links(htmltext, base):
    out = []
    for m in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', htmltext, flags=re.S|re.I):
        href, label = m.group(1), re.sub(r"<[^>]+>"," ",m.group(2))
        if href.startswith(("mailto:","tel:","javascript:","#")): continue
        u = urljoin(base, href)
        if urlparse(u).netloc.replace("www.","") != urlparse(base).netloc.replace("www.",""): continue
        if KEYS.search(u) or KEYS.search(label or ""): out.append(u.split("#")[0])
    seen=set(); res=[]
    for u in out:
        if u not in seen: seen.add(u); res.append(u)
    return res[:3]

def fetch(session, url):
    try:
        r = session.get(url, headers=UA, timeout=15, allow_redirects=True)
        ct = r.headers.get("content-type","")
        if "html" not in ct and "text" not in ct: return {"status": r.status_code, "final_url": r.url, "html": ""}
        return {"status": r.status_code, "final_url": r.url, "html": r.text[:600000]}
    except Exception as e:
        return {"status": None, "final_url": None, "html": "", "error": str(e)[:200]}

def robots_ok(session, base):
    try:
        r = session.get(urljoin(base, "/robots.txt"), headers=UA, timeout=10)
        if r.status_code != 200: return True
        block = False
        for line in r.text.splitlines():
            l = line.strip().lower()
            if l.startswith("user-agent:"): block = l.split(":",1)[1].strip() == "*"
            elif block and l.startswith("disallow:") and l.split(":",1)[1].strip() == "/": return False
        return True
    except Exception:
        return True

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--limit", type=int, default=0); ap.add_argument("--sleep", type=float, default=0.7)
    a = ap.parse_args()
    d = pd.read_csv("outputs/sites_ratings_sample.csv", dtype={"site_id":str})
    d = d[d["match_ok"].astype(bool) & d["website"].notna()].copy()
    d["url"] = d["website"].map(lambda u: u if str(u).startswith("http") else "http://"+str(u))
    d["domain"] = d["url"].map(lambda u: urlparse(u).netloc.lower().replace("www.",""))
    d = d[~d["domain"].str.contains("|".join(map(re.escape, SKIP_DOM)))]
    done = set()
    if os.path.exists("websites_pages.jsonl"):
        for line in open("websites_pages.jsonl", encoding="utf-8"):
            try: done.add(json.loads(line)["key"])
            except Exception: pass
    out = open("websites_pages.jsonl", "a", encoding="utf-8"); s = requests.Session()
    def rec(key, kind, site_id, domain, url, r):
        text = norm_text(r.get("html","")) if r.get("html") else ""
        out.write(json.dumps({"key": key, "kind": kind, "site_id": site_id, "domain": domain, "url": url, "status": r.get("status"),
                              "final_url": r.get("final_url"), "error": r.get("error"), "n_chars": len(text), "text": text[:60000]}, ensure_ascii=False)+"\n"); out.flush()
    # 1. Pages des sites
    todo = d[~("site:"+d["site_id"]).isin(done)]
    if a.limit: todo = todo.head(a.limit)
    print(f"{len(d)} sites avec site web · {len(todo)} pages de site à lire")
    robots = {}
    t0=time.time()
    for k,(_, r) in enumerate(todo.iterrows(),1):
        base = f"{urlparse(r['url']).scheme}://{urlparse(r['url']).netloc}/"
        if r["domain"] not in robots: robots[r["domain"]] = robots_ok(s, base); time.sleep(a.sleep/2)
        if not robots[r["domain"]]:
            rec("site:"+r["site_id"], "site", r["site_id"], r["domain"], r["url"], {"status": None, "error": "robots disallow"}); continue
        rec("site:"+r["site_id"], "site", r["site_id"], r["domain"], r["url"], fetch(s, r["url"])); time.sleep(a.sleep)
        if k % 100 == 0: print(f"  sites {k}/{len(todo)} · {time.time()-t0:.0f}s")
    # 2. Domaines : accueil + jusqu'à 3 pages clés
    doms = d.drop_duplicates("domain")
    todo = doms[~("dom:"+doms["domain"]).isin(done)]
    if a.limit: todo = todo.head(a.limit)
    print(f"{len(doms)} domaines · {len(todo)} à lire")
    for k,(_, r) in enumerate(todo.iterrows(),1):
        base = f"{urlparse(r['url']).scheme}://{urlparse(r['url']).netloc}/"
        if r["domain"] not in robots: robots[r["domain"]] = robots_ok(s, base)
        if not robots[r["domain"]]:
            rec("dom:"+r["domain"], "home", None, r["domain"], base, {"status": None, "error": "robots disallow"}); continue
        h = fetch(s, base); rec("dom:"+r["domain"], "home", None, r["domain"], base, h); time.sleep(a.sleep)
        for u in links(h.get("html",""), base):
            rec("dom:"+r["domain"]+"|"+u, "key", None, r["domain"], u, fetch(s, u)); time.sleep(a.sleep)
        if k % 50 == 0: print(f"  domaines {k}/{len(todo)} · {time.time()-t0:.0f}s")
    out.close(); print("terminé : websites_pages.jsonl")

if __name__ == "__main__":
    main()
