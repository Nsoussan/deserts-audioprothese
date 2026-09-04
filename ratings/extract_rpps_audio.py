"""Étape 0 : filtre l'extraction publique du RPPS (fichier Personne_activite, séparateur |) sur la profession
« Audioprothésiste » et écrit rpps_audio_lignes.csv (une ligne par activité ; non redistribué : noms et adresses).
Usage : python3 extract_rpps_audio.py [chemin du fichier RPPS]  (défaut : ../collecte_2026/rpps.zip, texte brut malgré l'extension).
Le filtre est fait ligne à ligne (le fichier pèse 800 Mo) ; la colonne « Libellé profession » est vérifiée ensuite."""
import sys, io, pandas as pd
src = sys.argv[1] if len(sys.argv) > 1 else "../collecte_2026/rpps.zip"
with open(src, encoding="utf-8", errors="replace") as f:
    header = f.readline()
    keep = [l for l in f if "|Audio-Prothésiste|" in l]
d = pd.read_csv(io.StringIO(header + "".join(keep)), sep="|", dtype=str, quoting=3, on_bad_lines="skip")
d = d[d["Libellé profession"].fillna("").str.strip().str.lower() .isin(["audio-prothésiste","audioprothésiste"])]
d.to_csv("rpps_audio_lignes.csv", index=False)
print(len(d), "lignes d'activité audioprothésiste ;", d["Identifiant PP"].nunique(), "professionnels ;", d["Identifiant technique de la structure"].nunique(), "structures")
