"""Étape 2 : plan de sondage. Prend tous les sites retail à 0 à 2 concurrents à 10 km et tire, dans les bandes 3-9 et 10+, un
échantillon proportionnel par groupe (enseigne nationale / indépendant / mutualiste), pour un total cible de 3 000 sites, avec des
poids égaux à l'inverse du taux de sondage de la strate.

Le tirage du 3 septembre 2026 a été fait avec ce plan mais sa graine n'a pas été conservée ; l'échantillon effectivement collecté est
fixé par les colonnes `strate` et `poids` de sites_public_v2.csv (2 999 sites). Ce script documente le plan et permet un nouveau tirage
(graine 2026 par défaut) ; avec --check, il vérifie que l'échantillon publié respecte le plan (strates exhaustives complètes,
tailles et poids des strates tirées)."""
import sys, numpy as np, pandas as pd
SEED = 2026; TARGET = 3000
s = pd.read_csv("sites_audio_2026.csv", dtype={"code_insee":str,"site_id":str})
r = s[s["retail"] & s["concurrents_10km"].notna()].copy()
r["bande10"] = pd.cut(r["concurrents_10km"], [-1, 0, 2, 9, 1e9], labels=["0","1-2","3-9","10+"]).astype(str)
r["strate"] = r["bande10"] + " | " + r["type"]
exhaustive = r[r["bande10"].isin(["0","1-2"])]
rest = r[~r["bande10"].isin(["0","1-2"])]
frac = (TARGET - len(exhaustive)) / len(rest)
if "--check" in sys.argv:
    pub = pd.read_csv("sites_public_v2.csv", dtype={"rpps_structure_id":str})
    smp = pub[pub["strate"].notna()]
    print("échantillon publié :", len(smp), "sites ;", "strates exhaustives complètes :",
          set(exhaustive["site_id"]) <= set(smp["rpps_structure_id"]))
    pop = r.groupby("strate").size(); n = smp.groupby("strate").size(); w = smp.groupby("strate")["poids"].first()
    t = pd.DataFrame({"population": pop, "sample": n, "weight": w, "pop/sample": (pop / n).round(3)}); print(t.to_string())
    print("taux de sondage des strates tirées :", round(frac, 4))
else:
    rng = np.random.default_rng(SEED); parts = [exhaustive]
    for st, g in rest.groupby("strate"):
        parts.append(g.sample(n=int(round(frac * len(g))), random_state=int(rng.integers(1e9))))
    smp = pd.concat(parts); pop = r.groupby("strate").size(); n = smp.groupby("strate").size()
    smp["poids"] = smp["strate"].map(pop / n)
    smp = smp.sample(frac=1, random_state=SEED)   # ordre de collecte aléatoire
    smp.to_csv("sample_new.csv", index=False); print(len(smp), "sites tirés dans sample_new.csv (ne remplace pas sample_3000.csv)")
