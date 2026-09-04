"""Remplace le corps (en-tête + lignes) de chaque tableau du papier par celui généré par build_tables.py, sur la base de la ligne de
titre « Table X. ». Les notes sous les tableaux restent celles du papier. Usage : python3 apply_tables.py paper.md tables.md"""
import re, sys
paper, tables = sys.argv[1], sys.argv[2]
P = open(paper, encoding="utf-8").read(); T = open(tables, encoding="utf-8").read()
def split_tables(text):
    """Renvoie {id: (caption_line, body_lines)} où id est 'Table 2', 'Table A1', 'Table 1 (continued)'..."""
    out = {}; lines = text.split("\n"); i = 0
    while i < len(lines):
        m = re.match(r"^(Table (?:A?\d+)(?: \(continued\))?)\.", lines[i])
        if m:
            cap = lines[i]; j = i + 1
            while j < len(lines) and not lines[j].startswith("|"): j += 1
            body = []
            while j < len(lines) and lines[j].startswith("|"): body.append(lines[j]); j += 1
            out[m.group(1)] = (cap, body); i = j
        else: i += 1
    return out
new = split_tables(T)
lines = P.split("\n"); i = 0; replaced = []
while i < len(lines):
    m = re.match(r"^(Table (?:A?\d+)(?: \(continued\))?)\.", lines[i])
    if m and m.group(1) in new:
        j = i + 1
        while j < len(lines) and not lines[j].startswith("|"): j += 1
        k = j
        while k < len(lines) and lines[k].startswith("|"): k += 1
        cap, body = new[m.group(1)]
        lines[j:k] = body; replaced.append(m.group(1)); i = j + len(body)
        if m.group(1) == "Table 1" and "Table 1 (continued)" in new:
            j2 = i
            while j2 < len(lines) and not lines[j2].startswith("|"): j2 += 1
            k2 = j2
            while k2 < len(lines) and lines[k2].startswith("|"): k2 += 1
            body2 = new["Table 1 (continued)"][1]; lines[j2:k2] = body2; replaced.append("Table 1 (continued)"); i = j2 + len(body2)
    else: i += 1
open(paper, "w", encoding="utf-8").write("\n".join(lines))
print("remplacés :", replaced); print("non trouvés dans le papier :", [k for k in new if k not in replaced])
