"""Codage automatique du contenu des sites web (à partir de websites_pages.jsonl).
Variables par site (page du site ∪ pages du domaine) :
  web_ok            page lue (statut 200 et texte non vide)
  prix_affiche      au moins un montant en euros >= 100 hors mention « 0 € »/« reste à charge »
  grille_tarifs     page ou lien « tarifs / prix » lu sur le domaine
  sante100          mention 100 % Santé / classe I / sans reste à charge
  classe2           mention classe II / classe 2
  essai_gratuit     essai gratuit / période d'essai
  bilan_gratuit     bilan ou test auditif gratuit
  rdv_en_ligne      prise de rendez-vous en ligne (ou Doctolib)
  devis             devis (normalisé, gratuit)
  marques           nombre de marques d'aides auditives citées
  garantie_suivi    garantie / suivi / réglages illimités
"""
import json, re, pandas as pd, numpy as np
from urllib.parse import urlparse
P = {
 "prix_montant": re.compile(r"(?<![\d,.])(\d{1,2}[ .]?\d{3}|[1-9]\d{2})\s?(?:€|euros?)(?!\s*(?:de\s+)?reste)"),
 "prix_apartir": re.compile(r"a partir de\s*\d"),
 "sante100": re.compile(r"100\s?%\s?sante|classe\s?(?:i|1)\b|sans reste a charge|zero reste a charge|0\s?€\s?de reste a charge|reste a charge (?:zero|nul|0)"),
 "classe2": re.compile(r"classe\s?(?:ii|2)\b"),
 "essai_gratuit": re.compile(r"essai(?:s)? gratuit|essayer gratuitement|essayez gratuitement|periode d'?essai|\d+ jours d'?essai|a l'?essai"),
 "bilan_gratuit": re.compile(r"(?:bilan|test|depistage|controle) (?:auditif |de l'?audition |d'?audition )?gratuit"),
 "rdv_en_ligne": re.compile(r"rendez-?vous en ligne|prendre rendez-?vous|prenez rendez-?vous|doctolib|reserver un (?:creneau|rendez)"),
 "devis": re.compile(r"devis"),
 "garantie_suivi": re.compile(r"garantie|suivi (?:illimite|gratuit|a vie)|reglages? (?:illimite|gratuit)"),
 "tarifs_mot": re.compile(r"\btarifs?\b|\bprix\b|grille tarifaire"),
}
MARQUES = ["phonak","oticon","signia","widex","starkey","resound","bernafon","unitron","philips hearing","audio service","sonic","rexton","beltone"]
CTX = re.compile(r"a partir de|nos (?:prix|tarifs)|(?:prix|tarifs?) (?:de nos|des|de l'?|de la|du|d'?un) (?:appareil|aide|prothese|audioprothese|solution|equipement|paire)|par appareil|par oreille|la paire|l'?appareil|classe (?:i|ii|1|2)\b|grille tarifaire|nos offres|pack|forfait", re.I)
EXCL = re.compile(r"rembours|securite sociale|assurance maladie|mutuelle|prise en charge|base de|plafond|complementaire|jusqu'?a|allocation|aide financiere|credit d'?impot|mdph|agefiph|caf\b", re.I)
FIRST = re.compile(r"\bj'?ai\b|\bje\b|\bon m'?|\bma \b|\bmon \b|\bmes \b|\bmerci\b|\bavis\b|\bnous avons\b|recommande|\bil y a\b", re.I)
def code_text(t):
    if not t: return None
    montants = []
    for m in P["prix_montant"].finditer(t):
        v = int(m.group(1).replace(" ","").replace(".",""))
        if not (100 <= v <= 20000) or v in (240, 400, 840, 1400, 1700): continue  # montants réglementaires de remboursement
        ctx = t[max(0,m.start()-90):m.end()+60]
        if CTX.search(ctx) and not EXCL.search(ctx) and not FIRST.search(t[max(0,m.start()-160):m.end()+40]):
            montants.append(v)
    return {"prix_affiche": int(len(montants)>0), "n_montants": len(montants),
            "prix_min": min(montants) if montants else np.nan,
            "sante100": int(bool(P["sante100"].search(t))), "classe2": int(bool(P["classe2"].search(t))),
            "essai_gratuit": int(bool(P["essai_gratuit"].search(t))), "bilan_gratuit": int(bool(P["bilan_gratuit"].search(t))),
            "rdv_en_ligne": int(bool(P["rdv_en_ligne"].search(t))), "devis": int(bool(P["devis"].search(t))),
            "garantie_suivi": int(bool(P["garantie_suivi"].search(t))), "tarifs_mot": int(bool(P["tarifs_mot"].search(t))),
            "marques": sum(1 for m in MARQUES if m in t), "n_chars": len(t)}
site_pages, dom_pages = {}, {}
for line in open("websites_pages.jsonl", encoding="utf-8"):
    r = json.loads(line)
    ok = r.get("status")==200 and r.get("n_chars",0)>200
    if r["kind"]=="site": site_pages[r["site_id"]] = (ok, r.get("text","") if ok else "", r["domain"])
    else:
        dom_pages.setdefault(r["domain"], {"ok": False, "text": "", "n_key": 0, "tarifs_page": 0})
        if ok:
            dom_pages[r["domain"]]["ok"] = True; dom_pages[r["domain"]]["text"] += " " + r.get("text","")
            if r["kind"]=="key":
                dom_pages[r["domain"]]["n_key"] += 1
                if re.search(r"tarif|prix", r["url"], re.I) and re.search(r"auditi|audio|appareil|proth", r.get("text",""), re.I) and not re.search(r"lunette|optique|solaire", r["url"], re.I): dom_pages[r["domain"]]["tarifs_page"] = 1
rows = []
for sid, (ok, text, dom) in site_pages.items():
    dp = dom_pages.get(dom, {"ok": False, "text": "", "n_key": 0, "tarifs_page": 0})
    web_ok = ok or dp["ok"]
    cs = code_text(text) if ok else None; cd = code_text(dp["text"]) if dp["ok"] else None
    row = {"site_id": sid, "domain": dom, "web_ok": int(web_ok), "site_page_ok": int(ok), "domain_ok": int(dp["ok"]), "grille_tarifs": dp["tarifs_page"], "n_pages_domaine": dp["n_key"]}
    for k in ["prix_affiche","sante100","classe2","essai_gratuit","bilan_gratuit","rdv_en_ligne","devis","garantie_suivi","tarifs_mot"]:
        vals = [c[k] for c in (cs, cd) if c]
        row[k] = max(vals) if vals else np.nan
        row[k+"_page"] = cs[k] if cs else np.nan   # sur la page du site seule
    row["marques"] = max([c["marques"] for c in (cs, cd) if c], default=np.nan)
    row["prix_min"] = np.nanmin([c["prix_min"] for c in (cs, cd) if c and c["prix_min"]==c["prix_min"]] or [np.nan])
    row["n_chars_total"] = sum(c["n_chars"] for c in (cs, cd) if c)
    rows.append(row)
w = pd.DataFrame(rows); w.to_csv("outputs/websites_coded.csv", index=False)
print(len(w), "sites codés ·", int(w["web_ok"].sum()), "lisibles")
print(w[["prix_affiche","grille_tarifs","sante100","classe2","essai_gratuit","bilan_gratuit","rdv_en_ligne","devis","garantie_suivi"]].mean().round(3))
