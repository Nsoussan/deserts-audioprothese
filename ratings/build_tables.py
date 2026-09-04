"""Construit les tableaux Markdown du document de travail à partir des sorties de outputs/v2/ (results*.txt et CSV), pour que chaque
nombre publié soit tiré des fichiers. Usage : python3 build_tables.py <dossier outputs/v2> > tables.md"""
import re, sys, io, numpy as np, pandas as pd
D = sys.argv[1] if len(sys.argv) > 1 else "outputs/v2"
R = open(f"{D}/results.txt", encoding="utf-8").read(); R3 = open(f"{D}/results_v3.txt", encoding="utf-8").read(); R4 = open(f"{D}/results_v4.txt", encoding="utf-8").read()
def block(text, header):
    """Renvoie le tableau coef/se/p qui suit un en-tête (première occurrence)."""
    i = text.index(header); lines = text[i:].splitlines()
    rows = {}; seg = [lines[0]]
    for line in lines[1:]:
        m = re.match(r"^(.*?)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$", line)
        if m: rows[m.group(1).strip()] = (float(m.group(2)), float(m.group(3)), float(m.group(4))); seg.append(line)
        elif re.match(r"^\s*coef\s+se\s+p\s*$", line): seg.append(line)
        else: break
    return rows, "\n".join(seg)
def stars(p): return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""
def cs(v): c, s, p = v; return f"{c:.3f} ({s:.3f}){stars(p)}"
def cp(v): c, s, p = v; return f"{c:+.3f} ({p:.2f})"
def pct(x, d=0): return f"{100*x:.{d}f}%"
def num(x): return f"{int(round(x)):,}"
def nobs(text, header):
    i = text.index(header); return int(re.search(r"n\s*=\s*(\d+)", text[i:i+200]).group(1))
LAB = {"integrated chain":"Integrated chains","brand network":"Brand networks","optician-hosted":"Optician corners","mutualist network":"Mutualist networks","unbranded independent":"Unbranded independents","all":"All"}
ORDER = ["integrated chain","brand network","optician-hosted","mutualist network","unbranded independent"]
BANDS = ["0","1-2","3-9","10+"]; BL = ["0","1–2","3–9","10+"]
out = []
def T(title, header, rows, note=None):
    out.append(title); out.append(""); out.append("| " + " | ".join(header) + " |"); out.append("|" + "|".join(["---"]*len(header)) + "|")
    for r in rows: out.append("| " + " | ".join(r) + " |")
    out.append("")
    if note: out.append(note); out.append("")
# ---------- Table 1 ----------
dt = pd.read_csv(f"{D}/desc_by_type.csv", index_col=0); db = pd.read_csv(f"{D}/desc_by_band.csv", index_col=0)
cols = ORDER + ["all"]
rows = [["Sites in sample"] + [num(dt.loc[c,"n"]) for c in cols],
        ["Owner-practitioner on site"] + [pct(dt.loc[c,"owner_share"]) for c in cols],
        ["Practitioners on site"] + [f"{dt.loc[c,'practitioners']:.2f}" for c in cols],
        ["Competitors within 10 km"] + [f"{dt.loc[c,'competitors_10km']:.1f}" for c in cols],
        ["Sites with ≥ 1 review"] + [pct(dt.loc[c,"rated"]) for c in cols],
        ["Median reviews"] + [num(dt.loc[c,"reviews_median"]) for c in cols],
        ["Mean rating (rated sites)"] + [f"{dt.loc[c,'rating_mean']:.2f}" for c in cols],
        ["Website on listing"] + [pct(dt.loc[c,"website"]) for c in cols]]
T("Table 1. Descriptive statistics, matched sample (weighted).", [""] + [LAB[c] for c in cols], rows)
db.index = db.index.astype(str)
rows = [["Sites in sample"] + [num(db.loc[b,"n"]) for b in BANDS],
        ["Owner-practitioner on site"] + [pct(db.loc[b,"owner_share"]) for b in BANDS],
        ["Distance to nearest centre (km)"] + [f"{db.loc[b,'dist_nearest_km']:.1f}" for b in BANDS],
        ["Commune population"] + [num(db.loc[b,"pop_commune"]) for b in BANDS],
        ["Median income (€ thousand)"] + [f"{db.loc[b,'income_k']:.1f}" for b in BANDS],
        ["Accessibility index (APL)"] + [num(db.loc[b,"apl"]) for b in BANDS],
        ["Sites with ≥ 1 review"] + [pct(db.loc[b,"rated"],1) for b in BANDS],
        ["Median reviews"] + [num(db.loc[b,"reviews_median"]) for b in BANDS],
        ["Mean rating (rated sites)"] + [f"{db.loc[b,'rating_mean']:.2f}" for b in BANDS]]
T("Table 1 (continued), by competition band.", ["", "0 competitors", "1–2", "3–9", "10+"], rows)
# ---------- Table 2 ----------
SB = "[B. + demande 65+ par site, part 65+]"
b1, s1 = block(R, SB + " log(1+avis)"); b2, s2 = block(R, SB + " noté (LPM)"); b3, s3 = block(R, SB + " note (notés)")
KEYS = [("bande10_1-2","1–2 competitors"),("bande10_3-9","3–9 competitors"),("bande10_10+","10+ competitors"),("type5_brand network","Brand network"),("type5_optician-hosted","Optician corner"),("type5_mutualist network","Mutualist network"),("type5_unbranded independent","Unbranded independent"),("owner","Owner-practitioner on site"),("npr","Practitioners on site"),("log_pop","log commune population"),("log_dem65","log older population per centre"),("share65","Share aged 65+ (points)"),("revenu_k","Median income (€ thousand)")]
rows = [[lab, cs(b1[k]), cs(b2[k]), cs(b3[k])] for k, lab in KEYS]
def nr2(seg): m = re.search(r"n=(\d+) · R2=([\d.]+)", seg); return num(int(m.group(1))), m.group(2)
n1, r1 = nr2(s1); n2, r2 = nr2(s2); n3, r3 = nr2(s3)
rows += [["Observations", n1, n2, n3], ["R²", r1, r2, r3]]
T("Table 2. Rating activity and content: weighted least squares, standard errors clustered by commune.", ["", "log(1 + reviews)", "≥ 1 review", "Rating (if ≥ 1 review)"], rows)
# ---------- Table 3 ----------
def fe(lab):
    b, seg = block(R, f"FE commune · {lab}"); n = nobs(R, f"FE commune · {lab}")
    return b, n
rows = []
for lab, name in [("log(1+avis)","log(1 + reviews)"),("noté","≥ 1 review"),("note","Rating (if ≥ 1 review)"),("site web","Website on listing")]:
    b, n = fe(lab); rows.append([name, cs(b["owner"]), cs(b["C(type5)[T.brand network]"]), cs(b["C(type5)[T.optician-hosted]"]), cs(b["C(type5)[T.unbranded independent]"]), cs(b["npr"]), num(n)])
mut = [f"{fe(l)[0]['C(type5)[T.mutualist network]'][0]:.3f}" for l in ["log(1+avis)","noté","note","site web"]]
m5 = re.search(r"communes à ≥2 sites appariés : (\d+) · sites : (\d+) · composition par bande : (\{.*\})", R)
T(f"Table 3. Organisational form within the same commune (commune fixed effects, {m5.group(1)} communes, {num(int(m5.group(2)))} sites).", ["Dependent variable","Owner on site","Brand network","Optician corner","Unbranded independent","Practitioners","N"], rows,
  f"*Mutualist-network coefficients: {', '.join(mut)}. Composition by band: {m5.group(3)}.*")
# ---------- Table 4 ----------
wt = pd.read_csv(f"{D}/web_by_type5.csv", index_col=0)
VARS = [("prix_affiche","Own prices displayed"),("grille_tarifs","Page dedicated to prices"),("sante100","Mentions class I (fully reimbursed)"),("classe2","Mentions class II"),("essai_gratuit","Free trial"),("bilan_gratuit","Free hearing test"),("rdv_en_ligne","Online booking"),("devis","Quote"),("garantie_suivi","Guarantee or follow-up terms")]
rows = [[lab] + [pct(wt.loc[c,v],1) for c in ORDER] for v, lab in VARS] + [["Sites with readable website"] + [num(wt.loc[c,"n"]) for c in ORDER]]
T("Table 4. Website content by organisational form (weighted; conditional on a readable website).", [""] + [LAB[c] for c in ORDER], rows)
# ---------- Table A1 ----------
rows = []
def brow(text, header, label, keys=("bande10_1-2","bande10_3-9","bande10_10+"), n=None):
    b, seg = block(text, header); nn = n if n is not None else (nobs(text, header) if "n=" in seg[:200] else "")
    return [label] + [cs(b[k]) for k in keys] + [num(nn) if nn != "" else ""]
rows.append(brow(R, SB + " log(1+avis)", "Baseline (Table 2)"))
rows.append(brow(R, "[A. base] log(1+avis)", "Without demand and age controls"))
rows.append(brow(R, "[PPML] nombre d'avis", "Poisson on review count", n=nobs(R, SB + " log(1+avis)")))
rows.append(brow(R, "[alternatives distinctes, spec B]", "Distinct alternatives instead of sites", keys=("alt_1-2","alt_3-9","alt_10+"), n=nobs(R, SB + " log(1+avis)")))
rows.append(brow(R4, "[alternatives distinctes, Demant fusionné]", "Distinct alternatives, Audika and Audilab merged", keys=("altd_1-2","altd_3-9","altd_10+"), n=nobs(R, SB + " log(1+avis)")))
rows.append(brow(R, "[sans opticiens] log(1+avis)", "Excluding optician corners"))
rows.append(brow(R, "[robustesse] noté, non appariés recodés", "≥ 1 review, unmatched sites as unrated"))
rows.append(brow(R4, "[dédoublonné] log(1+avis)", "One structure per Google listing"))
rows.append(brow(R4, "[Audilab = chaîne intégrée] log(1+avis)", "Audilab classed as an integrated chain"))
rows.append(brow(R4, "[bandes 20 km] log(1+avis)", "Bands of competitors within 20 km (a)", keys=("bande20_1-2","bande20_3-9","bande20_10+"), n=nobs(R, SB + " log(1+avis)")))
rows.append(brow(R4, "centres dans les 879 communes du benchmark", "Hearing-aid centres, benchmark communes (b)"))
rows.append(brow(R, "log(1+avis) coiffeurs ~ bandes", "Hairdressers, benchmark communes (b)", n=int(re.search(r"salons : (\d+)", R).group(1))))
pp, _ = block(R, "[PPML] nombre d'avis")
T("Table A1. Robustness of the activity gradient (dependent variable log(1 + reviews) unless stated; all controls of Table 2; standard errors clustered by commune).", ["Specification","1–2 competitors","3–9 competitors","10+ competitors","N"], rows,
  f"*(a) Bands of the number of competitors within 20 km, same cut-offs. (b) 879 communes; population and income controls only. Poisson form coefficients: brand network {pp['type5_brand network'][0]:.2f} ({pp['type5_brand network'][1]:.2f}), optician corner {pp['type5_optician-hosted'][0]:.2f} ({pp['type5_optician-hosted'][1]:.2f}), mutualist {pp['type5_mutualist network'][0]:.2f} ({pp['type5_mutualist network'][1]:.2f}), unbranded independent {pp['type5_unbranded independent'][0]:.2f} ({pp['type5_unbranded independent'][1]:.2f}), owner {pp['owner'][0]:.2f} ({pp['owner'][1]:.2f}).*")
# ---------- Table A2 ----------
tq = pd.read_csv(f"{D}/top_quartile_dispersion.csv", index_col=0); tq.index = tq.index.astype(str)
tc = pd.read_csv(f"{D}/top_quartile_ceiling.csv", index_col=0); tc.index = tc.index.astype(str)
rl = pd.read_csv(f"{D}/rating_level_by_threshold.csv"); sb = pd.read_csv(f"{D}/sd_by_bin_band.csv", header=[0,1], index_col=0)
bq = pd.read_csv(f"{D}/benchmark_top_quartile.csv", index_col=0); bq.index = bq.index.astype(str)
bw = pd.read_csv(f"{D}/benchmark_window_30_90.csv", index_col=0); bw.index = bw.index.astype(str)
share5 = eval(re.search(r"Part de notes = 5,0 par bande \(notés, pondéré\) : (\{.*\})", R).group(1))
rwm = eval(re.search(r"Moyenne des notes pondérée par le nombre d'avis, par bande : (\{.*\})", R).group(1))
m10 = eval(re.search(r"Moyenne des notes ≥10 avis par bande : (\{.*\})", R).group(1))
r10 = rl[(rl["seuil"]==10)&(rl["ctrl_log_avis"]==False)].iloc[0]
def lowtab(text, lab):
    i = text.index(f"[{lab}]"); seg = text[i:]; j = seg.index("LPM < 4,5 ~"); seg = seg[:j]
    tab = {}
    for line in seg.splitlines():
        m = re.match(r"^(0|1-2|3-9|10\+)\s+(\d+)\.0\s+(\d+)\.0\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", line)
        if m: tab[m.group(1)] = dict(n_low=int(m.group(2)), n=int(m.group(3)), p45=float(m.group(4)), p46=float(m.group(5)), p47=float(m.group(6)), d10=float(m.group(7)))
    sd = eval(re.search(r"SD (\{.*?\})", seg).group(1)); return tab, sd
lt_all, sd_all = lowtab(R3, "tous"); lt_no, sd_no = lowtab(R3, "sans opticiens")
pf, _ = block(R, "Part de 5,0 ~ bandes + tranches d'avis")
def sdbin(binlab): return [f"{sb.loc[binlab, ('sd', b)]:.3f}" for b in BANDS]
rows = [["Rated sites"] + [num(x) for x in sb.xs("n", axis=1, level=0).sum()[BANDS]],
        ["Mean rating"] + [f"{db.loc[b,'rating_mean']:.2f}" for b in BANDS],
        ["Rated exactly 5.0"] + [pct(share5[b],1) for b in BANDS],
        ["Review-weighted mean rating"] + [f"{rwm[b]:.2f}" for b in BANDS],
        ["Sites with ≥ 10 reviews: mean rating"] + [f"{m10[b]:.2f}" for b in BANDS],
        ["Band effect on rating, ≥ 10 reviews (ref. 0)", ""] + [r10[b].replace("+","") for b in ["bande10_1-2","bande10_3-9","bande10_10+"]],
        ["Top quarter by reviews within band: sites"] + [num(tq.loc[b,"n"]) for b in BANDS],
        ["Top quarter: minimum reviews"] + [num(tq.loc[b,"min_reviews"]) for b in BANDS],
        ["Top quarter: mean rating"] + [f"{tq.loc[b,'mean']:.2f}" for b in BANDS],
        ["Top quarter: rated exactly 5.0"] + [pct(tc.loc[b,"share_5.0"],1) for b in BANDS],
        ["Top quarter: S.D. across sites"] + [f"{tq.loc[b,'sd']:.3f}" for b in BANDS],
        ["Top quarter: rated below 4.5 (sites)"] + [f"{pct(lt_all[b]['p45'],1)} ({lt_all[b]['n_low']})" for b in BANDS],
        ["Top quarter: rated below 4.7"] + [pct(lt_all[b]["p47"],1) for b in BANDS],
        ["Top quarter: tenth percentile of ratings"] + [f"{lt_all[b]['d10']:.2f}" for b in BANDS],
        ["Top quarter without optician corners: S.D."] + [f"{sd_no[b]:.3f}" for b in BANDS],
        ["Top quarter without optician corners: below 4.5"] + [pct(lt_no[b]["p45"],1) for b in BANDS],
        ["Sites with 10 to 19 reviews: S.D. across sites"] + sdbin("10-19"),
        ["Sites with 20 to 49 reviews: S.D. across sites"] + sdbin("20-49"),
        ["Sites with ≥ 50 reviews: S.D. across sites"] + sdbin("50+"),
        ["Hairdressers rated (salons)"] + [num(x) for x in eval(re.search(r"salons notés par bande : (\{.*\})", R3).group(1)).values()] if False else ["Hairdressers rated (salons)"] + [num(eval(re.search(r"salons notés par bande : (\{.*\})", R3).group(1))[b]) for b in BANDS],
        ["Hairdressers, top quarter: S.D. across salons"] + [f"{bq.loc[b,'sd']:.3f}" for b in BANDS],
        ["Hairdressers, top quarter: rated below 4.5"] + [pct(bq.loc[b,"below45"],1) for b in BANDS],
        ["Hairdressers with 30 to 90 reviews: S.D."] + [f"{bw.loc[b,'sd']:.3f}" for b in BANDS],
        ["Perfect score, band effect conditional on review-count bin", ""] + [cp(pf[k]).replace("+","") for k in ["bande10_1-2","bande10_3-9","bande10_10+"]]]
T("Table A2. Rating level and dispersion by competition band.", ["", "0", "1–2", "3–9", "10+"], rows)
# fenêtre fixe 30-90 (results_v3)
i = R3.index("Fenêtre fixe 30–90 avis"); seg = R3[i:i+1500]
out.append("<!-- fenêtre fixe : " + " | ".join(l.strip() for l in seg.splitlines()[:14]) + " -->"); out.append("")
# ---------- Table A4 ----------
a4 = pd.read_csv(f"{D}/A4_income_x_band.csv"); rows = []
for _, r in a4.iterrows():
    rows.append([str(r["bande10"]).replace("1-2","1–2").replace("3-9","3–9"), {"T1":"bottom","T2":"middle","T3":"top"}[r["terc"]], num(r["n"]), pct(r["rated"],1), num(r["reviews_median"]), f"{r['rating']:.2f}"])
cuts = re.search(r"Terciles de revenu \(bornes k€\) : \[(?:np\.float64\()?([\d.]+)\)?, (?:np\.float64\()?([\d.]+)\)?\]", R)
T("Table A4. Rating activity by competition band and commune income tercile (weighted).", ["Competitors within 10 km","Income tercile","Sites","≥ 1 review","Median reviews","Mean rating"], rows, f"*Tercile cut-offs at {float(cuts.group(1))*1000:,.0f} and {float(cuts.group(2))*1000:,.0f} euros of median income per consumption unit.*")
# ---------- Table A5 ----------
bc = pd.read_csv(f"{D}/brand_classification.csv"); wb = pd.read_csv(f"{D}/web_by_brand.csv", index_col=0)
order5 = ["integrated chain","brand network"]
rows = []
for cls in order5:
    sub = bc[bc["type5"]==cls].sort_values("owner_share")
    for _, r in sub.iterrows():
        g = r["groupe"]; w = wb.loc[g] if g in wb.index else None
        rows.append([g, num(r["n"]), pct(r["owner_share"]), cls, pct(w["prix"]) if w is not None else "n.a.", pct(w["page_tarifs"]) if w is not None else "n.a."])
opt = bc[bc["type5"]=="optician-hosted"]; mut = bc[bc["type5"]=="mutualist network"]; ind = bc[bc["type5"]=="unbranded independent"]
wopt = wb.loc[[g for g in opt["groupe"] if g in wb.index]]
rows.append(["Optician corners (eight brands, see note)", num(opt["n"].sum()), f"{pct(opt['owner_share'].min())}–{pct(opt['owner_share'].max())}", "optician corner", f"{pct(wopt['prix'].min())}–{pct(wopt['prix'].max())}", f"{pct(wopt['page_tarifs'].min())}–{pct(wopt['page_tarifs'].max())}"])
g = mut.iloc[0]["groupe"]; rows.append(["Écouter Voir, VYV3, mutualités", num(mut["n"].sum()), pct(mut.iloc[0]["owner_share"]), "mutualist network", pct(wb.loc[g,"prix"]), pct(wb.loc[g,"page_tarifs"])])
rows.append(["No brand", num(ind["n"].sum()), pct(ind.iloc[0]["owner_share"]), "unbranded independent", pct(wt.loc["unbranded independent","prix_affiche"]), pct(wt.loc["unbranded independent","grille_tarifs"])])
T("Table A5. Brands: share of sites with an owner-practitioner (register), classification, and website price display (sites with a readable website).", ["Brand","Sites (register)","Owner-practitioner","Classification","Own prices displayed","Price page"], rows)
# ---------- Table A6 ----------
a6 = pd.read_csv(f"{D}/web_indep_bands.csv"); lab6 = dict(VARS)
rows = [[lab6[r["var"]], r["bande10_1-2"], r["bande10_3-9"], r["bande10_10+"], r["owner"]] for _, r in a6.iterrows()]
T(f"Table A6. Website content of unbranded independents and local competition (weighted least squares, independents with a readable website, n = {num(a6['n'].iloc[0])}; controls of Table 2; standard errors clustered by commune).", ["Dependent variable","1–2 competitors","3–9 competitors","10+ competitors","Owner on site"], rows)
# ---------- Table A7 ----------
a7 = pd.read_csv(f"{D}/web_vs_ratings.csv"); rows = []
for v, lab in VARS:
    r1 = a7[(a7["var"]==v)&(a7["y"]=="log(1+avis)")].iloc[0]; r2 = a7[(a7["var"]==v)&(a7["y"]=="note")].iloc[0]
    rows.append([lab, f"{r1['coef']:.3f} ({r1['se']:.3f}){stars(r1['p'])}", f"{r2['coef']:.3f} ({r2['se']:.3f}){stars(r2['p'])}"])
n7a = a7[a7["y"]=="log(1+avis)"]["n"].iloc[0]; n7b = a7[a7["y"]=="note"]["n"].iloc[0]
T("Table A7. Website content and ratings (all readable sites; each row a separate regression with the controls of Table 2; standard errors clustered by domain).", ["Content variable","log(1 + reviews)","Rating (if ≥ 1 review)"], rows, f"*N = {num(n7a)} (reviews) and {num(n7b)} (rating). \\*\\*\\* p < 0.01, \\*\\* p < 0.05, \\* p < 0.10.*")
# ---------- Table A8 : corners ----------
c6 = pd.read_csv(f"{D}/corner_split.csv", index_col=0)
rows = [[g, num(r["n"]), "shop" if r["shop_listing"]==1 else "own", pct(r["owner"]), num(r["median_reviews"]), f"{r['rating']:.2f}"] for g, r in c6.sort_values("median_reviews", ascending=False).iterrows()]
b6a, _ = block(R4, "[type6] log(1+avis)"); b6b, _ = block(R4, "[type6] noté"); b6c, _ = block(R4, "[type6] note"); b6o, _ = block(R4, "propriétaire × forme (type6)")
T("Table A8. Optician corners: listing of the shop or listing of their own (matched sample).", ["Brand","Sites","Listing","Owner-practitioner","Median reviews","Mean rating"], rows,
  f"*Regression of Table 2 with the corners split: shop-listing corners {cs(b6a['type6_corner, shop listing'])} on log(1 + reviews), {cs(b6b['type6_corner, shop listing'])} on being rated, {cs(b6c['type6_corner, shop listing'])} on the rating; own-listing corners {cs(b6a['type6_corner, own listing'])}, {cs(b6b['type6_corner, own listing'])} and {cs(b6c['type6_corner, own listing'])}; owner-practitioner {cs(b6a['owner'])} on log(1 + reviews). Owner effect by form: own-listing corners {cs(b6o['owner_x_type6_corner, own listing'])} relative to integrated chains, shop-listing corners {cs(b6o['owner_x_type6_corner, shop listing'])}.*")
# ---------- Table A9 : APL ----------
ap = pd.read_csv(f"{D}/apl_x_band.csv"); rows = []
for _, r in ap.iterrows():
    rows.append([str(r["bande10"]).replace("1-2","1–2").replace("3-9","3–9"), {"A1":"bottom","A2":"middle","A3":"top"}[r["apl_terc"]], num(r["n"]), pct(r["rated"],1), num(r["reviews_median"]), f"{r['rating']:.2f}"])
apl_cuts = re.search(r"bornes des terciles d'APL : \[np\.float64\(([\d.]+)\), np\.float64\(([\d.]+)\)\]", R4)
apl_lines = [l for l in R4.split("=== E.")[1].split("=== F.")[0].splitlines() if l.startswith(("log(1+avis) :","noté :","note :"))]
T("Table A9. Rating activity by competition band and tercile of the accessibility index (APL, weighted).", ["Competitors within 10 km","APL tercile","Sites","≥ 1 review","Median reviews","Mean rating"], rows, f"*Tercile cut-offs at {apl_cuts.group(1)} and {apl_cuts.group(2)} accessible professionals per 100,000 residents aged 65 and over. Regressions of Table 2 with the APL terciles added: " + " ; ".join(apl_lines) + "*")
# ---------- Table A10 : 20 km ----------
b20 = pd.read_csv(f"{D}/bands20_desc.csv", index_col=0); b20.index = b20.index.astype(str)
rows = [["Sites in sample"] + [num(b20.loc[b,"n"]) for b in BANDS], ["Sites with ≥ 1 review"] + [pct(b20.loc[b,"rated"],1) for b in BANDS], ["Median reviews"] + [num(b20.loc[b,"reviews_median"]) for b in BANDS], ["Mean rating (rated sites)"] + [f"{b20.loc[b,'rating']:.2f}" for b in BANDS]]
l20 = [l for l in R4.split("=== F.")[1].split("=== G.")[0].splitlines() if l.startswith("log(1+avis) : log(1+concurrents 20 km)")][0]
T("Table A10. Competition within 20 km (matched sample).", ["Competitors within 20 km", "0", "1–2", "3–9", "10+"], rows, f"*{l20}*")
print("\n".join(out))
