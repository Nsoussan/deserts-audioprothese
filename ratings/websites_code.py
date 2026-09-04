"""Codage automatique du contenu des sites web (à partir de websites_pages.jsonl). Version 2 (v2.3 du document de travail).
Variables par site (page du site ∪ pages du domaine) :
  web_ok            page lue (statut 200 et texte non vide)
  prix_affiche      information de prix : au moins un montant en euros pour des aides auditives dans un contexte de prix (prix, fourchette
                    ou fourchette indicative), hors remboursement, financement, franchise d'assurance et lunetterie
                    (le plafond réglementaire de 950 € et les bases/plafonds 240, 300, 350, 400, 840, 1 100, 1 300, 1 400, 1 700 €
                    ne comptent que dans un contexte explicite « nos prix / à partir de / nos tarifs »)
  grille_tarifs     page « tarifs / prix » lue sur le domaine, parlant d'audition et non de lunettes
  sante100          mention 100 % Santé / classe I / sans reste à charge, à proximité d'un mot d'audition
  classe2           mention classe II / classe 2
  essai_gratuit     essai gratuit / période d'essai, à proximité d'un mot d'audition, hors contexte d'emploi ou de lentilles
  bilan_gratuit     bilan ou test auditif gratuit
  rdv_en_ligne      prise de rendez-vous en ligne (Doctolib, réservation ou agenda en ligne) ; l'invitation à appeler ne compte pas
  devis             devis (normalisé, gratuit)
  marques           nombre de marques d'aides auditives citées
  garantie_suivi    garantie / suivi / réglages illimités, à proximité d'un mot d'audition
Changements par rapport à la version 1 (3 septembre 2026) : montants à virgule décimale lus ; 950 € et les anciens plafonds traités comme
montants réglementaires ; « jusqu'à » retiré des exclusions ; proximité d'un mot d'audition exigée pour 100 % Santé, essai et garantie ;
rendez-vous en ligne restreint aux prises de rendez-vous effectivement en ligne. Version 2.1 (après validation manuelle de 100 codages) : un montant n'est retenu que si un mot d'audition figure à proximité et hors contextes de facilités de paiement, de franchise d'assurance, de lunetterie et d'énoncés de marché (« en moyenne », « en France », « peut atteindre ») ; 710 euros ajouté aux montants réglementaires.
"""
import json, re, sys, pandas as pd, numpy as np
import os
SRC = sys.argv[1:] if len(sys.argv) > 1 else [f for f in ("websites_pages_v2.jsonl", "websites_pages_v2_dom.jsonl") if os.path.exists(f)]
AUDIO = r"audi|proth|appareil|aide auditive|aides auditives|entend|oreille|surdit|acoustic"
P = {
 "prix_montant": re.compile(r"(?<![\d,.])(\d{1,2}[ .]?\d{3}|[1-9]\d{2})(?:,\d{2})?\s?(?:€|euros?)(?!\s*(?:de\s+)?reste)"),
 "sante100": re.compile(r"100\s?%\s?sante|classe\s?(?:i|1)\b|sans reste a charge|zero reste a charge|0\s?€\s?de reste a charge|reste a charge (?:zero|nul|0)"),
 "classe2": re.compile(r"classe\s?(?:ii|2)\b"),
 "essai_gratuit": re.compile(r"essais? gratuits?|essais? (?:d'?appareils?|d'?aides?)[^.]{0,60}gratuit|gratuit[^.]{0,40}essais?|essayer gratuitement|essayez gratuitement|periode d'?essai|\d+ (?:jours|semaines|mois) d'?essai|essai (?:d'?un|de)? ?\d+ (?:jours|semaines|mois)|a l'?essai|essais? sans engagement"),
 "bilan_gratuit": re.compile(r"(?:bilan|test|depistage|controle) (?:auditif |de l'?audition |d'?audition )?gratuit"),
 "rdv_en_ligne": re.compile(r"rendez-?vous en ligne|doctolib|reserv(?:er|ez) (?:un |votre )?(?:creneau|rendez-?vous)|reservation en ligne|agenda en ligne|prise de rendez-?vous en ligne|prendre rendez-?vous en ligne|prenez rendez-?vous en ligne|rendez-?vous (?:sur|depuis) (?:notre |le )?site|services en ligne[^.]{0,80}rendez-?vous|demande de rendez-?vous"),
 "devis": re.compile(r"devis"),
 "garantie_suivi": re.compile(r"garantie|suivi (?:illimite|gratuit|a vie)|reglages? (?:illimite|gratuit)"),
 "tarifs_mot": re.compile(r"\btarifs?\b|\bprix\b|grille tarifaire"),
}
MARQUES = ["phonak","oticon","signia","widex","starkey","resound","bernafon","unitron","philips hearing","audio service","sonic","rexton","beltone"]
CTX = re.compile(r"a partir de|nos (?:prix|tarifs)|(?:prix|tarifs?) (?:de nos|des|de l'?|de la|du|d'?un) (?:appareil|aide|prothese|audioprothese|solution|equipement|paire)|par appareil|par oreille|la paire|l'?appareil|classe (?:i|ii|1|2)\b|grille tarifaire|nos offres|pack|forfait|entre \d|de \d[\d .]* (?:€|euros?) a \d", re.I)
OWN = re.compile(r"nos (?:prix|tarifs)|a partir de|notre grille|nos offres|tarifs? (?:du centre|pratiques?)", re.I)
EXCL = re.compile(r"rembours|securite sociale|assurance maladie|mutuelle|prise en charge|base de|plafon|prix limite|complementaire|allocation|aide financiere|credit d'?impot|mdph|agefiph|caf\b|ticket moderateur|reste a charge|en moyenne|du marche|sur le marche|peut grimper|peut atteindre|peut aller", re.I)
EXCL_WIDE = re.compile(r"franchise|paiement|mensualit|financement|credit|evenement garanti|garanti(?:e|es)? (?:casse|perte|vol)|assurance (?:casse|perte|vol)|lunette|monture|verres", re.I)
FIRST = re.compile(r"\bj'?ai\b|\bje\b|\bon m'?|\bma \b|\bmon \b|\bmes \b|\bmerci\b|\bavis\b|\bnous avons\b|recommande|\bil y a\b", re.I)
REG = {240, 300, 350, 400, 710, 840, 950, 1100, 1300, 1400, 1700}
EMPLOI = re.compile(r"contrat|cdi|cdd|recrut|emploi|candidat|poste|salari|lentille", re.I)
AUD = re.compile(AUDIO, re.I)
def near(t, m, span=150, pat=AUD):
    return bool(pat.search(t[max(0, m.start()-span):m.end()+span]))
def any_near(t, rx, span=150, excl=None):
    for m in rx.finditer(t):
        win = t[max(0, m.start()-span):m.end()+span]
        if AUD.search(win) and not (excl and excl.search(win)): return 1
    return 0
def code_text(t):
    if not t: return None
    montants = []
    for m in P["prix_montant"].finditer(t):
        v = int(m.group(1).replace(" ","").replace(".",""))
        if not (100 <= v <= 20000): continue
        ctx = t[max(0,m.start()-90):m.end()+60]; wide = t[max(0,m.start()-160):m.end()+80]
        if v in REG and not OWN.search(ctx): continue          # montants réglementaires : seulement en contexte de prix propre
        if CTX.search(ctx) and not EXCL.search(ctx) and not EXCL_WIDE.search(wide) and not FIRST.search(t[max(0,m.start()-160):m.end()+40]) and AUD.search(t[max(0,m.start()-200):m.end()+120]):
            montants.append(v)
    return {"prix_affiche": int(len(montants)>0), "n_montants": len(montants),
            "prix_min": min(montants) if montants else np.nan,
            "sante100": any_near(t, P["sante100"]), "classe2": int(bool(P["classe2"].search(t))),
            "essai_gratuit": any_near(t, P["essai_gratuit"], excl=EMPLOI), "bilan_gratuit": int(bool(P["bilan_gratuit"].search(t))),
            "rdv_en_ligne": int(bool(P["rdv_en_ligne"].search(t))), "devis": int(bool(P["devis"].search(t))),
            "garantie_suivi": any_near(t, P["garantie_suivi"]), "tarifs_mot": int(bool(P["tarifs_mot"].search(t))),
            "marques": sum(1 for m in MARQUES if m in t), "n_chars": len(t)}
site_pages, dom_pages, seen = {}, {}, set()
def lines():
    for f in SRC:
        for line in open(f, encoding="utf-8"): yield line
for line in lines():
    r = json.loads(line)
    if r["key"] in seen: continue   # une page lue deux fois (collectes parallèles) compte une fois
    seen.add(r["key"])
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
        row[k+"_page"] = cs[k] if cs else np.nan
    row["marques"] = max([c["marques"] for c in (cs, cd) if c], default=np.nan)
    row["prix_min"] = np.nanmin([c["prix_min"] for c in (cs, cd) if c and c["prix_min"]==c["prix_min"]] or [np.nan])
    row["n_chars_total"] = sum(c["n_chars"] for c in (cs, cd) if c)
    rows.append(row)
w = pd.DataFrame(rows); w.to_csv("outputs/websites_coded.csv", index=False)
print(len(w), "sites codés ·", int(w["web_ok"].sum()), "lisibles")
print(w[["prix_affiche","grille_tarifs","sante100","classe2","essai_gratuit","bilan_gratuit","rdv_en_ligne","devis","garantie_suivi"]].mean().round(3))
