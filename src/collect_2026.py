"""
Collecte des données 2026 — v8 (fix codes DOM).
Corrections : code commune DEP+CODCOM, URL RP 2022 (8581696),
FILOSOFI 2021 (le millésime 2022 n'a jamais été produit par l'INSEE),
encodage latin-1 des loyers.

    python3 collect_2026.py
"""

import io
import sys
import zipfile
from pathlib import Path

import pandas as pd
import requests

WORK = Path("collecte_2026")
WORK.mkdir(exist_ok=True)
OUT = Path("communes_2026.csv")
UA = {"User-Agent": "deserts-audioprothese-v2 (contact: nsoussan0@gmail.com)"}


def dl(url, dest, label):
    if dest.exists() and dest.stat().st_size > 0:
        print(f"  [cache] {label} : {dest.name} ({dest.stat().st_size/1e6:.0f} Mo)")
        return dest
    print(f"  [téléchargement] {label} …")
    r = requests.get(url, headers=UA, stream=True, timeout=900)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(chunk_size=1 << 20):
            f.write(chunk)
    print(f"    → {dest.name} ({dest.stat().st_size/1e6:.1f} Mo)")
    return dest


def open_maybe_zip(path: Path):
    if zipfile.is_zipfile(path):
        z = zipfile.ZipFile(path)
        name = z.namelist()[0]
        return io.TextIOWrapper(z.open(name), encoding="utf-8", errors="replace")
    return open(path, encoding="utf-8", errors="replace")


# ══════════════ 1. RPPS ══════════════
def collect_rpps():
    print("\n[1/5] RPPS — audioprothésistes et ORL par commune")
    act_path = WORK / "rpps.zip"
    if not act_path.exists():
        print("  ⚠️ collecte_2026/rpps.zip absent.")
        return None
    audio_pairs, orl_pairs = set(), set()
    n_rows = 0
    print("  lecture Personne_activite (2 à 5 min)…")
    with open_maybe_zip(act_path) as f:
        for chunk in pd.read_csv(f, sep="|", dtype=str, chunksize=200_000,
                                 on_bad_lines="skip", low_memory=False):
            if n_rows == 0:
                cols = {c.strip().lower(): c for c in chunk.columns}
                col_id = cols.get("identifiant pp")
                col_prof = cols.get("libellé profession") or cols.get("libelle profession")
                col_sf = cols.get("libellé savoir-faire") or cols.get("libelle savoir-faire")
                col_com = cols.get("code commune (coord. structure)")
                col_mode = cols.get("libellé mode exercice") or cols.get("libelle mode exercice")
                if not all([col_id, col_prof, col_com]):
                    print(f"  ⚠️ colonnes manquantes — envoie à Claude :\n{list(chunk.columns)}")
                    return None
            n_rows += len(chunk)
            prof = chunk[col_prof].fillna("").str.lower()
            com_ok = chunk[col_com].fillna("").str.strip() != ""
            is_audio = prof.str.contains("audio") & prof.str.contains("proth")
            for i, c in zip(chunk.loc[is_audio & com_ok, col_id],
                            chunk.loc[is_audio & com_ok, col_com]):
                audio_pairs.add((i, c))
            if col_sf is not None:
                sf = chunk[col_sf].fillna("").str.lower()
                is_orl = prof.str.contains("médecin") & sf.str.contains("oto-rhino")
                if col_mode is not None:
                    is_orl = is_orl & chunk[col_mode].fillna("").str.lower().str.startswith("lib")
                for i, c in zip(chunk.loc[is_orl & com_ok, col_id],
                                chunk.loc[is_orl & com_ok, col_com]):
                    orl_pairs.add((i, c))
    agg_audio, agg_orl = {}, {}
    for _, c in audio_pairs:
        agg_audio[c] = agg_audio.get(c, 0) + 1
    for _, c in orl_pairs:
        agg_orl[c] = agg_orl.get(c, 0) + 1
    df = pd.DataFrame({"code_insee": sorted(set(agg_audio) | set(agg_orl))})
    df["nb_audioprothesistes_2026"] = df["code_insee"].map(agg_audio).fillna(0).astype(int)
    df["nb_orl_liberaux_2026"] = df["code_insee"].map(agg_orl).fillna(0).astype(int)
    print(f"  → {len(audio_pairs):,} audioprothésistes · {len(orl_pairs):,} ORL libéraux "
          f"· {len(df):,} communes couvertes")
    return df


# ══════════════ 2. Populations de référence 2023 ══════════════
def collect_population():
    print("\n[2/5] Populations de référence 2023 (INSEE)")
    zpath = WORK / "pop2023.zip"
    try:
        dl("https://www.insee.fr/fr/statistiques/fichier/8680726/ensemble.zip",
           zpath, "populations de référence (csv)")
    except Exception as e:
        print(f"  ⚠️ échec ({e}).")
        return None
    with zipfile.ZipFile(zpath) as z:
        name = next((n for n in z.namelist() if "commune" in n.lower() and n.lower().endswith(".csv")),
                    next(n for n in z.namelist() if n.lower().endswith(".csv")))
        with z.open(name) as f:
            pop = pd.read_csv(f, sep=";", dtype=str)
    cols = {c.upper(): c for c in pop.columns}
    def build_code(dep, com):
        dep = dep.strip()
        com = com.strip()
        return dep + com.zfill(2) if len(dep) == 3 else dep + com.zfill(3)
    if "DEP" in cols and "CODCOM" in cols:
        pop["code_insee"] = [build_code(d, c) for d, c in
                             zip(pop[cols["DEP"]].astype(str), pop[cols["CODCOM"]].astype(str))]
    elif "CODDEP" in cols and "CODCOM" in cols:
        pop["code_insee"] = [build_code(d, c) for d, c in
                             zip(pop[cols["CODDEP"]].astype(str), pop[cols["CODCOM"]].astype(str))]
    elif "DEPCOM" in cols:
        pop["code_insee"] = pop[cols["DEPCOM"]].str.strip()
    elif "CODGEO" in cols:
        pop["code_insee"] = pop[cols["CODGEO"]].str.strip()
    else:
        print(f"  ⚠️ structure inattendue : {list(pop.columns)}")
        return None
    pmun = cols.get("PMUN")
    if pmun is None:
        print(f"  ⚠️ colonne PMUN introuvable : {list(pop.columns)}")
        return None
    pop["population_2023"] = pd.to_numeric(pop[pmun], errors="coerce")
    df = pop[["code_insee", "population_2023"]].dropna().drop_duplicates("code_insee")
    print(f"  → {len(df):,} communes (France hors Mayotte — recensement mahorais reporté post-Chido)")
    return df


# ══════════════ 3. Structure par âge RP 2022 ══════════════
def collect_age():
    print("\n[3/5] Structure par âge — RP 2022")
    zpath = WORK / "age2022.zip"
    urls = [
        "https://www.insee.fr/fr/statistiques/fichier/8581696/base-cc-evol-struct-pop-2022_csv.zip",
        "https://www.insee.fr/fr/statistiques/fichier/8581696/base-cc-evol-struct-pop-2022_CSV.zip",
    ]
    got = zpath.exists() and zpath.stat().st_size > 0
    for u in urls:
        if got:
            break
        try:
            dl(u, zpath, "base évolution et structure RP 2022")
            got = True
        except Exception:
            if zpath.exists():
                zpath.unlink()
    if not got:
        print("  ⚠️ échec — page insee.fr/fr/statistiques/8581696 → télécharge la base commune (csv)\n"
              "     → pose le zip dans collecte_2026/age2022.zip, relance. Étape sautée.")
        return None
    with zipfile.ZipFile(zpath) as z:
        name = next(n for n in z.namelist() if n.lower().endswith(".csv") and "meta" not in n.lower())
        with z.open(name) as f:
            age = pd.read_csv(f, sep=";", dtype=str)
    cols = {c.upper(): c for c in age.columns}
    c_geo = cols.get("CODGEO", list(age.columns)[0])
    c_pop = cols.get("P22_POP")
    c_h65 = cols.get("P22_H65P")
    c_f65 = cols.get("P22_F65P")
    if all([c_pop, c_h65, c_f65]):
        for c in [c_pop, c_h65, c_f65]:
            age[c] = pd.to_numeric(age[c].astype(str).str.replace(",", "."), errors="coerce")
        age["part_65_plus_pct_2022"] = ((age[c_h65] + age[c_f65]) / age[c_pop] * 100).round(2)
        note = "65+ EXACT (H65P + F65P)"
    else:
        c_6074 = cols.get("P22_POP6074")
        c_7589 = cols.get("P22_POP7589")
        c_90 = cols.get("P22_POP90P")
        if not all([c_pop, c_6074, c_7589, c_90]):
            print(f"  ⚠️ colonnes d'âge inattendues : {list(age.columns)[:30]}")
            return None
        for c in [c_pop, c_6074, c_7589, c_90]:
            age[c] = pd.to_numeric(age[c].astype(str).str.replace(",", "."), errors="coerce")
        age["part_65_plus_pct_2022"] = ((age[c_6074] * 2 / 3 + age[c_7589] + age[c_90]) / age[c_pop] * 100).round(2)
        note = "65+ estimé (2/3 de 60-74 + 75-89 + 90+)"
    df = age[[c_geo, "part_65_plus_pct_2022"]].rename(columns={c_geo: "code_insee"}).drop_duplicates("code_insee")
    print(f"  → {len(df):,} communes ({note})")
    return df


# ══════════════ 4. Dossier complet INSEE (format long SDMX) ══════════════
def collect_dossier():
    print("\n[4/5] Dossier complet INSEE — revenus, pauvreté, superficie (format SDMX)")
    print("  (FILOSOFI 2022 n'a jamais été produit — 2021 = dernier millésime de revenus)")
    pq_path = WORK / "dossier_complet.parquet"
    if not (pq_path.exists() and pq_path.stat().st_size > 0):
        print("  ⚠️ collecte_2026/dossier_complet.parquet absent — étape sautée.")
        return None
    try:
        import pyarrow.parquet as papq
        import pyarrow.compute as pc
    except ImportError:
        print("  pyarrow manquant :  pip3 install pyarrow   puis relance.")
        return None

    pf = papq.ParquetFile(pq_path)
    cols = ["GEO_OBJECT", "GEO", "TIME_PERIOD", "TAB_MEASURE", "OBS_VALUE"]
    print(f"  streaming de {pf.metadata.num_rows/1e6:.0f} M de lignes (2 à 5 min)…")

    keep = []          # (geo, measure, period, value)
    measures_seen = set()
    for batch in pf.iter_batches(batch_size=1_000_000, columns=cols):
        d = batch.to_pandas()
        d = d[d["GEO_OBJECT"].astype(str).str.upper().eq("COM")]
        if d.empty:
            continue
        m = d["TAB_MEASURE"].astype(str).str.upper()
        mask = m.str.contains("MED") | m.str.startswith("TP60") | m.str.contains("SUPERF")
        sel = d[mask]
        if len(sel):
            keep.append(sel[["GEO", "TAB_MEASURE", "TIME_PERIOD", "OBS_VALUE"]])
        measures_seen.update(m.unique().tolist()[:500])
    if not keep:
        cand = sorted(x for x in measures_seen
                      if any(k in x for k in ("MED", "TP", "SUPERF", "REV", "PAUV")))[:40]
        print(f"  ⚠️ aucun indicateur MED/TP60/SUPERF trouvé au niveau commune.\n"
              f"     Codes candidats vus — envoie ça à Claude : {cand}")
        return None

    d = pd.concat(keep, ignore_index=True)
    d["TAB_MEASURE"] = d["TAB_MEASURE"].astype(str).str.upper()
    d["OBS_VALUE"] = pd.to_numeric(d["OBS_VALUE"], errors="coerce")

    def latest(mask):
        s = d[mask].copy()
        if s.empty:
            return None
        s["TIME_PERIOD"] = s["TIME_PERIOD"].astype(str)
        s = s.sort_values("TIME_PERIOD").drop_duplicates("GEO", keep="last")
        return s.set_index("GEO")["OBS_VALUE"], s["TIME_PERIOD"].max()

    out = pd.DataFrame({"code_insee": sorted(d["GEO"].astype(str).unique())}).set_index("code_insee")
    msg_parts = []
    r = latest(d["TAB_MEASURE"].str.contains("MED"))
    if r:
        out["revenu_median_uc"], per = r
        msg_parts.append(f"revenu (médiane, {per})")
    r = latest(d["TAB_MEASURE"].str.startswith("TP60"))
    if r:
        out["taux_pauvrete"], per = r
        msg_parts.append(f"pauvreté ({per})")
    r = latest(d["TAB_MEASURE"].str.contains("SUPERF"))
    if r:
        out["superficie_km2"], per = r
        msg_parts.append("superficie")
    out = out.reset_index()
    print(f"  → {len(out):,} communes · " + " · ".join(msg_parts))
    return out


# ══════════════ 5. Carte des loyers ══════════════
def collect_loyers():
    print("\n[5/5] Carte des loyers — dernière édition")
    fpath = WORK / "loyers.csv"
    resources = None
    if not (fpath.exists() and fpath.stat().st_size > 0):
        for slug in [
            "carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2024",
            "carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2023",
        ]:
            try:
                r = requests.get(f"https://www.data.gouv.fr/api/1/datasets/{slug}/", headers=UA, timeout=60)
                r.raise_for_status()
                resources = r.json()["resources"]
                break
            except Exception:
                continue
        if not resources:
            print("  ⚠️ jeu introuvable — étape sautée.")
            return None
        def score_res(x):
            hay = (x.get("title", "") + " " + x.get("url", "")).lower()
            app = ("app" in hay) and ("maison" not in hay)
            size = x.get("filesize") or 0
            return (0 if app else 1, -size)
        res = sorted(resources, key=score_res)[0]
        print(f"  ressource choisie : {res.get('title', res['url'])[:80]} "
              f"({(res.get('filesize') or 0)/1e6:.1f} Mo)")
        try:
            dl(res["url"], fpath, "indicateurs loyers appartements")
        except Exception as e:
            print(f"  ⚠️ échec ({e}) — étape sautée.")
            return None
    loy = None
    for enc in ["latin-1", "utf-8"]:
        try:
            loy = pd.read_csv(fpath, sep=None, engine="python", dtype=str, encoding=enc)
            break
        except Exception:
            continue
    if loy is None:
        print("  ⚠️ lecture impossible — étape sautée.")
        return None
    cols_l = {c.lower(): c for c in loy.columns}
    c_geo = cols_l.get("insee_c") \
        or next((cols_l[k] for k in cols_l if "insee" in k), None) \
        or cols_l.get("codgeo") or list(loy.columns)[0]
    c_val = next((cols_l[k] for k in cols_l if "loypredm2" in k or "pred" in k or "loyer" in k), None)
    if c_val is None:
        print(f"  ⚠️ colonne loyer introuvable ({list(loy.columns)[:12]}) — étape sautée.")
        return None
    loy[c_val] = pd.to_numeric(loy[c_val].astype(str).str.replace(",", "."), errors="coerce")
    df = loy[[c_geo, c_val]].rename(columns={c_geo: "code_insee", c_val: "loyer_m2"})
    df = df.dropna(subset=["code_insee"]).drop_duplicates("code_insee")
    print(f"  → {len(df):,} communes")
    if len(df) < 10_000 and resources:
        print("  ℹ️ couverture faible — autres ressources du jeu (pour info Claude) :")
        for x in resources[:12]:
            print(f"     - {x.get('title','?')[:70]} · {(x.get('filesize') or 0)/1e6:.1f} Mo")
    return df


def main():
    parts = {
        "rpps": collect_rpps(),
        "pop": collect_population(),
        "age": collect_age(),
        "dossier": collect_dossier(),
        "loyers": collect_loyers(),
    }
    ok = {k: v for k, v in parts.items() if v is not None}
    ko = [k for k, v in parts.items() if v is None]

    if "pop" in ok:
        df = ok["pop"]
    elif "age" in ok:
        df = ok["age"][["code_insee"]].copy()
    else:
        sys.exit("\n⚠️  Ni populations ni âge — impossible de construire la base.")

    for k in ["age", "dossier", "loyers", "rpps"]:
        if k in ok and ok[k] is not df:
            df = df.merge(ok[k], on="code_insee", how="left")
    for c in ["nb_audioprothesistes_2026", "nb_orl_liberaux_2026"]:
        if c in df.columns:
            df[c] = df[c].fillna(0).astype(int)

    if "part_65_plus_pct_2023" in df.columns:
        # RP 2023 disponible : il devient la référence, le RP 2022 reste en secours
        df["part_65_plus_pct"] = df["part_65_plus_pct_2023"].fillna(df.get("part_65_plus_pct_2022"))
    elif "part_65_plus_pct_2022" in df.columns:
        df["part_65_plus_pct"] = df["part_65_plus_pct_2022"]
    if "superficie_km2" in df.columns and "population_2023" in df.columns:
        df["densite_2023"] = (df["population_2023"] / df["superficie_km2"]).round(2)
    df.to_csv(OUT, index=False, encoding="utf-8")
    print(f"\n✅ {OUT} écrit ({OUT.stat().st_size/1e6:.1f} Mo, {len(df):,} communes, {len(df.columns)} colonnes)")
    if ko:
        print(f"⚠️  Étapes manquantes : {ko}")
    if "pop" in ok and "rpps" in ok:
        sans = df[(df["population_2023"] >= 5000) & (df["nb_audioprothesistes_2026"] == 0)]
        print(f"Aperçu brut : communes ≥ 5 000 hab sans audioprothésiste (2026) : {len(sans)}")
    print("→ Envoie communes_2026.csv à Claude (+ la sortie du terminal).")


if __name__ == "__main__":
    main()
