"""Collecte du contenu des sites web des centres (pages publiques, lecture seule, rythme lent). Version 2 (v2.3 du document de travail).

Deux niveaux : (1) la page exacte référencée par la fiche Google de chaque site ; (2) pour chaque domaine, la page d'accueil
et jusqu'à trois pages internes dont l'adresse ou le libellé évoque les tarifs, le 100 % Santé ou l'essai, les pages tarifs d'abord.
Usage (Terminal du Mac) :  python3 websites_collect.py [--limit N] [--sleep S] [--out websites_pages_v2.jsonl] [--sites-only | --domains-only]
Les deux niveaux peuvent être lus en parallèle dans deux fichiers de sortie, puis concaténés (le codeur dédoublonne par clé).
Sortie : une ligne par page lue (url, statut, texte normalisé tronqué à 60 000 caractères). Reprise automatique.
Changements par rapport à la version 1 (3 septembre 2026) : l'encodage de chaque page est lu dans son en-tête HTML ou détecté,
au lieu de l'encodage supposé par la bibliothèque, ce qui mangeait les accents et le signe € ; le signe € est conservé sous la forme
« euros » avant la normalisation ASCII ; robots.txt est interprété par urllib.robotparser (règles par chemin) ; les liens vers les
pages de prix sont lus en priorité.
"""
import argparse, json, os, re, sys, time, unicodedata, html
from urllib.parse import urlparse, urljoin
import urllib.robotparser as rp
import pandas as pd, requests

UA_STR = "Mozilla/5.0 (compatible; etude-accessibilite-audioprothese/2.0; contact: nsoussan0@gmail.com)"
UA = {"User-Agent": UA_STR}
KEYS = re.compile(r"tarif|prix|price|100[- ]?sante|100-?%|classe|offre|essai|garantie|rembours|remboursement|devis|financ", re.I)
PRIO = re.compile(r"tarif|prix|price", re.I)
SKIP_DOM = ("facebook.com","instagram.com","linkedin.com","google.","business.site","pagesjaunes.fr")

def decode(r):
    """Décodage : charset de l'en-tête HTTP s'il est explicite, sinon meta charset du HTML, sinon détection, sinon UTF-8."""
    raw = r.content
    ct = r.headers.get("content-type", "")
    m = re.search(r"charset=([\w-]+)", ct, re.I)
    enc = m.group(1) if m else None
    if not enc:
        m = re.search(rb'<meta[^>]+charset=["\']?\s*([\w-]+)', raw[:20000], re.I)
        enc = m.group(1).decode() if m else None
    if not enc:
        enc = r.apparent_encoding or "utf-8"
    try:
        return raw.decode(enc, errors="replace")
    except LookupError:
        return raw.decode("utf-8", errors="replace")

def norm_text(s):
    s = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", s, flags=re.S|re.I)
    s = re.sub(r"<[^>]+>", " ", s); s = html.unescape(s)
    s = s.replace("€", " euros ").replace("&euro;", " euros ").replace(" ", " ")
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().lower()
    return re.sub(r"\s+", " ", s).strip()

def links(htmltext, base):
    out = []
    for m in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', htmltext, flags=re.S|re.I):
        href, label = m.group(1), re.sub(r"<[^>]+>"," ",m.group(2))
        if href.startswith(("mailto:","tel:","javascript:","#")): continue
        u = urljoin(base, href)
        if urlparse(u).netloc.replace("www.","") != urlparse(base).netloc.replace("www.",""): continue
        if re.search(r"lunette|optique|solaire|lentille", u, re.I): continue
        if KEYS.search(u) or KEYS.search(label or ""):
            out.append((0 if (PRIO.search(u) or PRIO.search(label or "")) else 1, u.split("#")[0]))
    seen=set(); res=[]
    for _, u in sorted(out, key=lambda x: x[0]):
        if u not in seen: seen.add(u); res.append(u)
    return res[:3]

def fetch(session, url):
    try:
        r = session.get(url, headers=UA, timeout=15, allow_redirects=True)
        ct = r.headers.get("content-type","")
        if "html" not in ct and "text" not in ct: return {"status": r.status_code, "final_url": r.url, "html": ""}
        return {"status": r.status_code, "final_url": r.url, "html": decode(r)[:600000]}
    except Exception as e:
        return {"status": None, "final_url": None, "html": "", "error": str(e)[:200]}

class Robots:
    def __init__(self, session): self.s = session; self.cache = {}
    def get(self, base):
        if base in self.cache: return self.cache[base]
        p = rp.RobotFileParser()
        try:
            r = self.s.get(urljoin(base, "/robots.txt"), headers=UA, timeout=10)
            if r.status_code == 200: p.parse(r.text.splitlines())
            else: p.parse([])
        except Exception:
            p.parse([])
        self.cache[base] = p; return p
    def allowed(self, url):
        base = f"{urlparse(url).scheme}://{urlparse(url).netloc}/"
        p = self.get(base)
        try: return p.can_fetch(UA_STR, url) and p.can_fetch("*", url)
        except Exception: return True

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--limit", type=int, default=0); ap.add_argument("--sleep", type=float, default=0.3); ap.add_argument("--out", default="websites_pages_v2.jsonl"); ap.add_argument("--domains-only", action="store_true"); ap.add_argument("--sites-only", action="store_true")
    a = ap.parse_args()
    d = pd.read_csv("outputs/sites_ratings_sample.csv", dtype={"site_id":str})
    d = d[d["match_ok"].astype(bool) & d["website"].notna()].copy()
    d["url"] = d["website"].map(lambda u: u if str(u).startswith("http") else "http://"+str(u))
    d["domain"] = d["url"].map(lambda u: urlparse(u).netloc.lower().replace("www.",""))
    d = d[~d["domain"].str.contains("|".join(map(re.escape, SKIP_DOM)))]
    done = set()
    if os.path.exists(a.out):
        for line in open(a.out, encoding="utf-8"):
            try: done.add(json.loads(line)["key"])
            except Exception: pass
    out = open(a.out, "a", encoding="utf-8"); s = requests.Session(); robots = Robots(s)
    def rec(key, kind, site_id, domain, url, r):
        text = norm_text(r.get("html","")) if r.get("html") else ""
        out.write(json.dumps({"key": key, "kind": kind, "site_id": site_id, "domain": domain, "url": url, "status": r.get("status"),
                              "final_url": r.get("final_url"), "error": r.get("error"), "n_chars": len(text), "text": text[:60000],
                              "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S")}, ensure_ascii=False)+"\n"); out.flush()
    todo = d[~("site:"+d["site_id"]).isin(done)]
    if a.domains_only: todo = todo.head(0)
    if a.limit: todo = todo.head(a.limit)
    print(f"{len(d)} sites avec site web · {len(todo)} pages de site à lire")
    t0=time.time()
    for k,(_, r) in enumerate(todo.iterrows(),1):
        if not robots.allowed(r["url"]):
            rec("site:"+r["site_id"], "site", r["site_id"], r["domain"], r["url"], {"status": None, "error": "robots disallow"}); continue
        rec("site:"+r["site_id"], "site", r["site_id"], r["domain"], r["url"], fetch(s, r["url"])); time.sleep(a.sleep)
        if k % 100 == 0: print(f"  sites {k}/{len(todo)} · {time.time()-t0:.0f}s")
    doms = d.drop_duplicates("domain")
    todo = doms[~("dom:"+doms["domain"]).isin(done)]
    if a.sites_only: todo = todo.head(0)
    if a.limit: todo = todo.head(a.limit)
    print(f"{len(doms)} domaines · {len(todo)} à lire")
    for k,(_, r) in enumerate(todo.iterrows(),1):
        base = f"{urlparse(r['url']).scheme}://{urlparse(r['url']).netloc}/"
        if not robots.allowed(base):
            rec("dom:"+r["domain"], "home", None, r["domain"], base, {"status": None, "error": "robots disallow"}); continue
        h = fetch(s, base); rec("dom:"+r["domain"], "home", None, r["domain"], base, h); time.sleep(a.sleep)
        for u in links(h.get("html",""), base):
            if not robots.allowed(u):
                rec("dom:"+r["domain"]+"|"+u, "key", None, r["domain"], u, {"status": None, "error": "robots disallow"}); continue
            rec("dom:"+r["domain"]+"|"+u, "key", None, r["domain"], u, fetch(s, u)); time.sleep(a.sleep)
        if k % 50 == 0: print(f"  domaines {k}/{len(todo)} · {time.time()-t0:.0f}s")
    out.close(); print(f"terminé : {a.out}")

if __name__ == "__main__":
    main()
