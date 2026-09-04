"""Prépare la validation manuelle du codage des sites web : tire 100 sites lisibles (50 codés « prix affiché », 50 non), et extrait pour
chacun les fenêtres de texte autour des montants en euros et des mots-clés (100 % santé, rendez-vous, essai), pour jugement humain.
Écrit validation/web_sample_100.json (privé, non redistribué)."""
import json, re, numpy as np, pandas as pd
w = pd.read_csv("outputs/websites_coded.csv", dtype={"site_id":str}); w = w[w["web_ok"]==1]
rng = np.random.default_rng(2026)
a = w[w["prix_affiche"]==1].sample(n=min(50, int((w["prix_affiche"]==1).sum())), random_state=2026); b = w[w["prix_affiche"]==0].sample(n=50, random_state=2026)
sel = pd.concat([a, b]); ids = set(sel["site_id"]); doms = set(sel["domain"])
texts = {}
import os
seen = set()
def lines():
    for f in ("websites_pages_v2.jsonl", "websites_pages_v2_dom.jsonl"):
        if os.path.exists(f):
            for line in open(f, encoding="utf-8"): yield line
for line in lines():
    r = json.loads(line)
    if r["key"] in seen: continue
    seen.add(r["key"])
    if r.get("status") != 200 or not r.get("text"): continue
    if r["kind"] == "site" and r["site_id"] in ids: texts.setdefault(("site", r["site_id"]), []).append((r["url"], r["text"]))
    elif r["kind"] != "site" and r["domain"] in doms: texts.setdefault(("dom", r["domain"]), []).append((r["url"], r["text"]))
AMT = re.compile(r"(?<![\d,.])(\d{1,2}[ .]?\d{3}|[1-9]\d{2})(?:,\d{2})?\s?euros?")
KEY = re.compile(r"100 ?% ?sante|classe (?:i|1)\b|rendez-?vous|doctolib|essai")
def windows(text, rx, span=160, maxn=8):
    out = []
    for m in rx.finditer(text):
        out.append(text[max(0, m.start()-span):m.end()+span])
        if len(out) >= maxn: break
    return out
rows = []
for _, r in sel.iterrows():
    pages = texts.get(("site", r["site_id"]), []) + texts.get(("dom", r["domain"]), [])
    amt, key = [], []
    for url, t in pages:
        amt += [f"[{url}] …{x}…" for x in windows(t, AMT)]; key += [f"[{url}] …{x}…" for x in windows(t, KEY, span=100, maxn=4)]
    rows.append({"site_id": r["site_id"], "domain": r["domain"], "coded_prix_affiche": int(r["prix_affiche"]), "coded_sante100": int(r["sante100"]) if r["sante100"]==r["sante100"] else None,
                 "coded_rdv_en_ligne": int(r["rdv_en_ligne"]) if r["rdv_en_ligne"]==r["rdv_en_ligne"] else None, "coded_essai_gratuit": int(r["essai_gratuit"]) if r["essai_gratuit"]==r["essai_gratuit"] else None,
                 "n_pages": len(pages), "amount_windows": amt[:12], "keyword_windows": key[:8]})
json.dump(rows, open("validation/web_sample_100.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(rows), "sites ;", sum(1 for r in rows if r["amount_windows"]), "avec fenêtres de montants")
