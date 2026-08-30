"""Rapport scientifique v2 — format académique (IMRaD, Times 12, TOC paginée)."""
import json
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                 Spacer, PageBreak, Table, TableStyle, Image)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
_LIB = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Serif", _LIB + "LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", _LIB + "LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Italic", _LIB + "LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Serif-BoldItalic", _LIB + "LiberationSerif-BoldItalic.ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold",
                              italic="Serif-Italic", boldItalic="Serif-BoldItalic")

NB = "\u00a0"
INK = colors.HexColor("#111111")
RULE = colors.HexColor("#444444")
S = getSampleStyleSheet()
BODY = ParagraphStyle('BODY', parent=S['Normal'], fontName='Serif', fontSize=12,
                      leading=18.0, alignment=TA_JUSTIFY, spaceAfter=10, textColor=INK)
H1S = ParagraphStyle('H1S', parent=BODY, fontName='Serif-Bold', fontSize=14, leading=17,
                     spaceBefore=20, spaceAfter=8, alignment=0)
H2S = ParagraphStyle('H2S', parent=BODY, fontName='Serif-Bold', fontSize=12, leading=15,
                     spaceBefore=15, spaceAfter=6, alignment=0)
H3S = ParagraphStyle('H3S', parent=BODY, fontName='Serif-Italic', fontSize=12, leading=15,
                     spaceBefore=9, spaceAfter=4, alignment=0)
SM = ParagraphStyle('SM', parent=BODY, fontSize=9.5, leading=12.5)
CAPF = ParagraphStyle('CAPF', parent=BODY, fontSize=10, leading=12.8, alignment=TA_CENTER,
                      spaceBefore=3, spaceAfter=12, fontName='Serif-Italic')
CAPT = ParagraphStyle('CAPT', parent=CAPF, spaceBefore=10, spaceAfter=4)
TI = ParagraphStyle('TI', parent=BODY, fontName='Serif-Bold', fontSize=17, leading=22,
                    alignment=TA_CENTER)
SUB = ParagraphStyle('SUB', parent=BODY, fontSize=12, alignment=TA_CENTER, spaceAfter=4)
CELL = ParagraphStyle('CELL', parent=S['Normal'], fontName='Serif', fontSize=9,
                      leading=11, textColor=INK)
CELLH = ParagraphStyle('CELLH', parent=CELL, fontName='Serif-Bold')
REF = ParagraphStyle('REF', parent=BODY, fontSize=10.5, leading=13.5, spaceAfter=4,
                     leftIndent=0.9*cm, firstLineIndent=-0.9*cm)

import re as _re
def P(txt, style=BODY):
    txt = _re.sub(r"\b(figures?|tableaux?|annexes?|sections?) (?=\d|[A-K]\b)",
                  lambda m: m.group(1) + NB, txt)
    return Paragraph(txt.replace(" :", NB+":").replace(" ;", NB+";")
                        .replace(" %", NB+"%").replace(" €", NB+"€")
                        .replace(" ?", NB+"?").replace("« ", "«"+NB).replace(" »", NB+"»"), style)

def fr(n):
    return f"{n:,.0f}".replace(",", NB)

def dc(x, nd=1):
    return f"{x:.{nd}f}".replace('.', ',')

def tab(rows, widths, fs=9, align_right=None):
    c = ParagraphStyle('c', parent=CELL, fontSize=fs, leading=fs+2)
    ch = ParagraphStyle('ch', parent=CELLH, fontSize=fs, leading=fs+2)
    cr = ParagraphStyle('cr', parent=c, alignment=2)
    def cell(x, header, j):
        st = ch if header else (cr if (align_right and j in align_right) else c)
        s = str(x)
        if len(s) > 14 and not s[:1].isdigit():
            s = s.replace("-", "-\u200b")
        return Paragraph(s, st)
    data = [[cell(x, True, j) for j, x in enumerate(rows[0])]] + \
           [[cell(x, False, j) for j, x in enumerate(r)] for r in rows[1:]]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 0.9, RULE),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, RULE),
        ('LINEBELOW', (0, -1), (-1, -1), 0.9, RULE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.6), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.6),
        ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4)]))
    return t

class H1(Paragraph):
    def __init__(self, text, toc_text=None):
        super().__init__(text.replace(" :", NB+":"), H1S)
        self._toc = (0, toc_text or text)
class H2(Paragraph):
    def __init__(self, text):
        super().__init__(text.replace(" :", NB+":"), H2S)
        self._toc = (1, text)

class Doc(BaseDocTemplate):
    def afterFlowable(self, fl):
        if hasattr(fl, '_toc'):
            level, text = fl._toc
            self.notify('TOCEntry', (level, text, self.page))

def on_page(canvas, doc):
    if doc.page == 1:
        return
    canvas.saveState()
    canvas.setFont('Serif', 9)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(2.5*cm, A4[1]-1.5*cm, "L'accessibilité de l'audioprothèse en France — N. Soussan")
    canvas.drawRightString(A4[0]-2.5*cm, A4[1]-1.5*cm, str(doc.page))
    canvas.setLineWidth(0.4)
    canvas.setStrokeColor(colors.HexColor("#AAAAAA"))
    canvas.line(2.5*cm, A4[1]-1.62*cm, A4[0]-2.5*cm, A4[1]-1.62*cm)
    canvas.restoreState()

doc = Doc("/home/claude/rapport_v2_sci.pdf", pagesize=A4)
frame = Frame(2.5*cm, 2.3*cm, A4[0]-5*cm, A4[1]-4.5*cm, id='f')
doc.addPageTemplates([PageTemplate(id='p', frames=[frame], onPage=on_page)])

# Données
stats = json.load(open('stats_rapport.json'))
gini = json.load(open('gini.json'))['gini_apl']
apl_dec = json.load(open('apl_deciles.json'))
t_reg = pd.read_csv('t_regional.csv')
t_dep = pd.read_csv('t_departemental.csv', dtype={'dep': str})
t_prio = pd.read_csv('t_prioritaires.csv', dtype={'code_insee': str})
t_dp = pd.read_csv('t_doublepeine.csv')
t_eqx = pd.read_csv('t_equite.csv')
t_qi = pd.read_csv('t_quintiles_ic.csv')
t_str = pd.read_csv('t_strates.csv')
t_dom44 = pd.read_csv('t_dom44.csv')
t_n64 = pd.read_csv('t_nouveaux64.csv')
t_e295 = pd.read_csv('t_eq295.csv')
t_z88 = pd.read_csv('t_apl0.csv')
t_sens = pd.read_csv('sensibilite_poids.csv')
t_eq10 = pd.read_csv('t_equipees.csv')
t_pe10 = pd.read_csv('t_persistants.csv')
t_s560 = pd.read_csv('t_s560.csv', dtype={'code_insee': str})
t_dpd = pd.read_csv('t_dp_dep.csv', dtype={'dep': str})
t_corrm = pd.read_csv('t_corr.csv', index_col=0)
t_logit = pd.read_csv('t_logit.csv')
t_aplv = pd.read_csv('t_aplvar.csv')
t_rdec = pd.read_csv('t_retro_dec.csv')
t_rreg = pd.read_csv('t_retro_reg.csv')

E = []
# ═══ Page de titre ═══
E.append(Spacer(1, 4.2*cm))
E.append(P("L'accessibilité de l'audioprothèse en France", TI))
E.append(Spacer(1, 0.3*cm))
E.append(P("Mesure communale de l'accès et de l'opportunité d'implantation,\n"
           "confrontée à la dynamique du marché 2022-2026", SUB))
E.append(Spacer(1, 2.2*cm))
E.append(P("Nathan Soussan", ParagraphStyle('au', parent=SUB, fontSize=13)))
E.append(P("Audioprothésiste diplômé d'État", SUB))
E.append(Spacer(1, 1.6*cm))
E.append(P("Version 2.0", SUB))
E.append(P("Août 2026", SUB))
E.append(Spacer(1, 2.8*cm))
E.append(P("Rapport d'étude — diffusion publique", ParagraphStyle('df', parent=SUB, fontSize=10.5)))
E.append(P("Code source : DOI 10.5281/zenodo.22146816 — Données : DOI 10.5281/zenodo.22146965",
           ParagraphStyle('dg', parent=SUB, fontSize=10)))
E.append(PageBreak())

# ═══ Résumé (150-250 mots) ═══
E.append(H1("Résumé"))
E.append(P("L'accessibilité territoriale de l'audioprothèse est mesurée à l'échelle des 34"+NB+"900 "
    "communes françaises (hors Mayotte), à partir de sources publiques arrêtées au 30 août 2026. "
    "Deux indicateurs sont construits : une accessibilité potentielle localisée (APL), adaptée "
    "pour la première fois à cette profession, et un score d'opportunité d'implantation à dix "
    "critères. La mesure est ensuite confrontée à la dynamique réelle du marché entre 2022 et "
    "2026, période de croissance de 65 % de l'offre recensée. Trois résultats principaux se "
    "dégagent. Le score publié sur données 2022 prédit significativement les implantations "
    "ultérieures : le taux d'équipement des communes initialement dépourvues d'offre croît de "
    "30,8 % à 54,5 % entre les quintiles extrêmes du score (aire sous la courbe ROC de 0,597 ; "
    "p"+NB+"&lt;"+NB+"10<super>-5</super>). L'expansion s'est dirigée vers les communes les plus peuplées, sans lien "
    "détectable avec leur vieillissement ni leur revenu. Enfin, 560 communes de plus de 5"+NB+"000 "
    "habitants restent sans audioprothésiste, dont 173 classées prioritaires ; l'écart "
    "d'accessibilité entre l'Hexagone et les départements d'outre-mer atteint un facteur deux, et "
    "un facteur sept pour la Guyane, tandis que 2"+NB+"992 communes cumulent accès faible, population "
    "âgée et revenus modestes. Les comptages sont validés par recoupement de deux chaînes "
    "administratives indépendantes, concordantes à 99 %. Données, code et méthodes sont "
    "intégralement publiés.", BODY))
E.append(Spacer(1, 0.35*cm))
E.append(P("<i>Mots-clés</i> : audioprothèse ; accessibilité aux soins ; accessibilité potentielle "
    "localisée ; déserts médicaux ; 100 % Santé ; analyse communale ; données ouvertes.", SM))
E.append(PageBreak())

# ═══ Table des matières ═══
E.append(H1("Table des matières"))
toc = TableOfContents()
toc.levelStyles = [
    ParagraphStyle('t0', parent=BODY, fontName='Serif-Bold', fontSize=11.5, leading=15, spaceBefore=6),
    ParagraphStyle('t1', parent=BODY, fontSize=11, leading=14, leftIndent=0.8*cm),
]
E.append(toc)
E.append(PageBreak())

# ═══ Liste des abréviations ═══
E.append(H1("Liste des abréviations"))
ab_rows = [["Sigle", "Développement"]]
for sg, dv in [
    ("ADELI", "Automatisation des listes (répertoire des professions paramédicales, remplacé par le RPPS)"),
    ("ANS", "Agence du Numérique en Santé"),
    ("APL", "Accessibilité potentielle localisée"),
    ("AUC", "Aire sous la courbe ROC (area under the curve)"),
    ("BPE", "Base permanente des équipements (Insee)"),
    ("COG", "Code officiel géographique"),
    ("DOM", "Départements d'outre-mer"),
    ("DREES", "Direction de la recherche, des études, de l'évaluation et des statistiques"),
    ("IC 95 %", "Intervalle de confiance à 95 %"),
    ("Insee", "Institut national de la statistique et des études économiques"),
    ("Irdes", "Institut de recherche et documentation en économie de la santé"),
    ("ORL", "Oto-rhino-laryngologiste"),
    ("ROC", "Receiver operating characteristic"),
    ("RP", "Recensement de la population"),
    ("RPPS", "Répertoire partagé des professionnels intervenant dans le système de santé"),
    ("UC", "Unité de consommation"),
    ("2SFCA", "Two-step floating catchment area (méthode des zones de desserte flottantes en deux étapes)"),
]:
    ab_rows.append([sg, dv])
E.append(tab(ab_rows, [2.6*cm, 13.4*cm], fs=10))
E.append(PageBreak())

# ═══ 1. INTRODUCTION ═══
E.append(H1("1. Introduction"))
E.append(P("Depuis le 1<super>er</super> janvier 2021, la réforme dite du 100 % Santé garantit à tout assuré "
    "un équipement auditif de classe I intégralement pris en charge. Ce dispositif a levé ce qui "
    "constituait, de l'avis général, le premier obstacle à l'appareillage : son coût, de l'ordre de "
    "1"+NB+"500 € par oreille avant réforme, resté très largement à la charge des ménages. La contrainte "
    "financière desserrée, la question de l'accès se déplace vers sa dimension géographique. "
    "L'appareillage auditif n'est pas une délivrance ponctuelle mais un suivi au long cours : "
    "adaptation initiale, réglages répétés, entretien, renouvellement, autant de rendez-vous dont la "
    "régularité conditionne l'observance, pour une patientèle âgée dont la mobilité décroît "
    "précisément quand le besoin augmente. La distance au professionnel est donc un déterminant du "
    "succès de l'appareillage, et non un simple désagrément."))
E.append(P("La connaissance publique de la répartition de l'offre reste pourtant grossière. Les "
    "effectifs de la profession sont suivis aux échelles nationale et départementale, mailles "
    "auxquelles la couverture du territoire paraît convenable ; l'échelon communal, seul pertinent "
    "pour une question d'accès de proximité, n'est pas documenté. Les travaux de la statistique "
    "publique sur l'accessibilité aux soins, fondés sur l'accessibilité potentielle localisée (APL) "
    "développée par la DREES et l'Irdes [2] et sur les réflexions méthodologiques associées à la "
    "notion de désert médical [3], portent sur les médecins généralistes et quelques professions de "
    "premier recours ; aucune déclinaison n'en existait, à notre connaissance, pour "
    "l'audioprothèse."))
E.append(P("Mesurer l'accès à une offre de soins n'a rien d'univoque, et trois familles "
    "d'indicateurs coexistent dans la littérature comme dans le débat public. Le comptage des "
    "professionnels par territoire, le plus répandu, est aveugle aux débordements entre unités "
    "administratives : une commune sans professionnel jouxtant une ville équipée y apparaît "
    "identique à une commune isolée. La distance ou le temps d'accès au professionnel le plus "
    "proche corrige ce défaut mais ignore la saturation : être à cinq minutes d'un cabinet "
    "débordé n'est pas un accès. Les indicateurs gravitaires, dont l'APL est le représentant "
    "français de référence, combinent les deux dimensions en rapportant une offre pondérée par "
    "la distance à une demande pondérée de même, au prix de conventions de portée et de "
    "pondération qui doivent être explicites et testées [2, 3]. La présente étude mobilise les "
    "trois familles, précisément parce que leurs divergences sont instructives : la section 4.3 "
    "montre que le choix de l'indicateur renverse le diagnostic dans des cas aussi importants "
    "que l'Île-de-France ou la Guyane."))
E.append(P("Une première version de la présente étude [1], construite sur les effectifs 2022 du "
    "répertoire ADELI, avait recensé 742 communes de plus de 5"+NB+"000 habitants sans "
    "audioprothésiste et proposé un score d'opportunité d'implantation. Elle présentait deux "
    "faiblesses assumées : des pondérations en partie normatives, et l'absence de validation "
    "externe. La présente version les traite toutes deux. Elle adosse d'abord le diagnostic à un "
    "indicateur standard de la statistique publique, l'APL, adapté à la profession. Elle exploite "
    "ensuite une configuration rare : quatre années séparent les deux photographies du marché, "
    "années au cours desquelles 4"+NB+"336 activités se sont créées, ce qui permet de tester la valeur "
    "prédictive du classement de 2022 sur des décisions d'implantation prises par des acteurs qui "
    "l'ignoraient. Elle soumet enfin l'ensemble à une analyse de sensibilité systématique et à une "
    "validation croisée par une seconde source administrative indépendante."))
E.append(P("La période étudiée constitue par ailleurs une fenêtre d'observation peu commune. "
    "Entre la solvabilisation complète de la classe I en 2021 et l'arrêté des données en août "
    "2026, la profession a connu une phase d'expansion dont l'ampleur, 65 % d'activités "
    "recensées en plus en quatre ans, dépasse tout ce que ses répertoires avaient enregistré ; "
    "observer où cette vague s'est déposée, et où elle ne s'est pas déposée malgré elle, "
    "renseigne sur les déterminants de l'implantation avec une netteté qu'un régime de "
    "croisière n'offrirait pas. C'est cette conjoncture qui donne à la validation "
    "rétrospective de la section 3.7 et au bilan d'accessibilité de la section 3.13 leur "
    "valeur d'expérience naturelle."))
E.append(P("La contribution de ce travail est donc quadruple : premier calcul d'une APL pour "
    "l'audioprothèse, sur l'intégralité du territoire couvert par les données publiques ; "
    "première validation rétrospective d'un score d'implantation de cette profession sur une "
    "dynamique de marché observée ; identification, par croisement de l'accès, de l'âge et du "
    "revenu, des territoires où la levée de la barrière financière ne peut suffire ; et "
    "publication intégrale, code et données, de l'ensemble de la chaîne. Le tout repose "
    "exclusivement sur des sources ouvertes, ce qui en garantit la reproductibilité mais en "
    "fixe aussi les limites, discutées en section 4.8."))
E.append(P("Trois questions structurent l'étude. Où l'accès à l'audioprothèse manque-t-il, une fois "
    "pris en compte le partage de l'offre entre communes voisines ? Le score d'opportunité publié "
    "en 2022 a-t-il prédit la localisation des implantations de la période 2022-2026, et quelles "
    "caractéristiques communales cette expansion a-t-elle suivies ? Quels territoires cumulent "
    "enfin un accès faible, un besoin démographique élevé et des ressources modestes, configuration "
    "où la levée de la barrière financière ne peut suffire ? La section 2 décrit les matériels et "
    "méthodes, la section 3 expose les résultats, la section 4 les discute et en établit les "
    "limites, la section 5 conclut."))

# ═══ 2. MATÉRIELS ET MÉTHODES ═══
E.append(H1("2. Matériels et méthodes"))
E.append(H2("2.1. Sources de données"))
E.append(P("Cinq sources publiques, toutes diffusées sous licence ouverte, ont été mobilisées dans "
    "leur millésime le plus récent disponible au 30 août 2026, date d'arrêté de la collecte ; une "
    "sixième sert exclusivement à la validation croisée. Le tableau 1 en donne la synthèse."))
E.append(P("Tableau 1 — Sources mobilisées, producteurs, millésimes et usage.", CAPT))
E.append(tab([
    ["Source", "Producteur", "Millésime", "Usage"],
    ["Annuaire Santé, extraction du RPPS, fichier Personne_activite [4]", "ANS", "août 2026", "Effectifs d'audioprothésistes et d'ORL libéraux par commune"],
    ["Populations de référence [5]", "Insee", "2023", "Population municipale ; seuil des 5 000 habitants"],
    ["RP, base « Évolution et structure de la population » [6]", "Insee", "2022", "Part des 65 ans et plus"],
    ["Base du dossier complet, format harmonisé [7]", "Insee", "2023", "Médiane de niveau de vie par UC"],
    ["Carte des loyers, complétée par l'édition 2022 [8]", "MTE / ANIL", "2024", "Loyer d'annonce au m²"],
    ["Contours communaux france-geojson [9]", "communauté", "2025", "Centroïdes, distances, cartes"],
    ["Base permanente des équipements [10]", "Insee", "2025", "Validation croisée (audioprothèse libérale)"],
], [6.4*cm, 2.2*cm, 1.9*cm, 5.5*cm], fs=9))
E.append(P("Les effectifs professionnels proviennent de l'extraction quotidienne en libre accès du "
    "Répertoire partagé des professionnels intervenant dans le système de santé (RPPS), auquel les "
    "audioprothésistes, antérieurement suivis par le répertoire ADELI, ont été intégrés courant "
    "2024. Le fichier d'activités exploité comprend 2,28 millions de lignes toutes professions "
    "confondues. Les audioprothésistes ont été repérés par le libellé de profession du répertoire "
    "(« Audio-Prothésiste », code 26), sans restriction de mode d'exercice, les centres salariés "
    "recevant les patients au même titre que les cabinets indépendants ; les ORL ont été repérés "
    "parmi les médecins par le savoir-faire « oto-rhino-laryngologie », restreints à l'exercice "
    "libéral afin de correspondre à la population des prescripteurs de ville. Un même professionnel "
    "pouvant exercer sur plusieurs sites, les lignes d'activité ont été dédoublonnées en couples "
    "uniques identifiant × commune : l'unité de compte est l'activité communale, non l'équivalent "
    "temps plein. Ont ainsi été dénombrées 11"+NB+"030 activités d'audioprothésistes, dont 11"+NB+"018 rattachées à une commune du champ, le solde de douze correspondant à Mayotte, aux collectivités d'outre-mer et à des codes communaux absorbés par des fusions, et 1"+NB+"379 "
    "activités d'ORL libéraux."))
E.append(P("Comme tout répertoire administratif, le RPPS enregistre des inscriptions et des "
    "déclarations d'activité, non une présence effective : une cessation tardivement déclarée "
    "ou un site secondaire peu actif y demeurent comptés. Ce biais joue dans le sens d'une "
    "surestimation de l'offre, et donc d'une lecture conservatrice des manques : une commune "
    "classée sans audioprothésiste l'est au sens le plus robuste, aucune activité n'y étant "
    "même déclarée. La validation croisée de la section 3.10 confirme que ce comptage "
    "prudent coïncide presque exactement avec celui d'une chaîne administrative distincte."))
E.append(P("Les populations municipales sont les populations de référence du millésime 2023, "
    "authentifiées par décret et entrées en vigueur au 1<super>er</super> janvier 2026 [5] ; elles sont "
    "diffusées dans la géographie communale du 1<super>er</super> janvier 2025, qui définit le périmètre "
    "d'étude (34"+NB+"900 communes, France hors Mayotte). La part des 65 ans et plus a été calculée à "
    "partir des effectifs exacts par sexe du recensement 2022 (variables P22_H65P et P22_F65P) [6]. "
    "La médiane de niveau de vie par unité de consommation provient du millésime 2023 diffusé dans "
    "la base du dossier complet de l'Insee [7] ; le dispositif antérieur n'ayant jamais produit de "
    "millésime 2022, du fait de la suppression de la taxe d'habitation, ce millésime 2023 est le "
    "plus récent existant. Les 4"+NB+"109 communes couvertes par le secret statistique ont été imputées "
    "à 25"+NB+"000 €, valeur proche de la médiane nationale ; la sensibilité des résultats à cette "
    "imputation est examinée en section 3.10. Le loyer d'annonce au m² provient de la Carte des "
    "loyers, édition 2024, complétée par l'édition 2022 pour les communes non couvertes [8]."))
E.append(P("Mayotte est exclue du champ : le recensement de 2025 y a été reporté après le cyclone "
    "Chido, un recensement exhaustif a été conduit fin 2025-début 2026, et les populations qui en "
    "résulteront ne seront authentifiées que fin 2026 ; aucune population de référence n'était donc "
    "disponible à la date de l'étude."))
E.append(P("Le passage à la géographie du 1<super>er</super> janvier 2025 emporte une conséquence "
    "pratique qui explique une part des écarts de comptage entre millésimes : les fusions de "
    "communes absorbent des codes géographiques, et des activités rattachées à un code disparu "
    "ne peuvent plus l'être qu'après recodage. Toutes les sources de l'étude étant diffusées "
    "dans la même géographie 2025, ces recompositions sont neutralisées à l'intérieur du "
    "millésime 2026 ; elles ne le sont qu'imparfaitement dans les comparaisons avec 2022, ce "
    "que la section 2.6 précise."))
E.append(H2("2.2. Construction de la base et mesures de distance"))
E.append(P("Les sept variables sources ont été appariées par le code officiel géographique à cinq "
    "caractères. Les centroïdes communaux ont été calculés à partir des contours du projet "
    "france-geojson [9] (34"+NB+"844 communes appariées sur 34"+NB+"900, les manquantes correspondant à des "
    "communes nouvelles dont les contours n'étaient pas consolidés dans le fonds utilisé). Les "
    "distances intercommunales sont des distances orthodromiques entre centroïdes (formule de "
    "haversine) ; la distance d'une commune équipée à elle-même est nulle. La distance de chaque "
    "commune au professionnel le plus proche a été obtenue par recherche du plus proche voisin dans "
    "un arbre k-dimensionnel construit sur les coordonnées cartésiennes tridimensionnelles des "
    "communes équipées. La distance entre centroïdes est une double approximation : elle "
    "ignore le réseau routier et résume chaque commune en un point. Les deux effets sont "
    "faibles dans le tissu communal dense de l'Hexagone, substantiels dans les grandes "
    "communes peu denses, ce qui justifie le plafonnement à 30 km utilisé par le score et la "
    "discussion spécifique de l'outre-mer en section 4.4."))
E.append(H2("2.3. Accessibilité potentielle localisée"))
E.append(P("L'APL [2] appartient à la famille des méthodes de zones de desserte flottantes en deux "
    "étapes (2SFCA). Elle se calcule ici comme suit. Première étape : pour chaque commune équipée "
    "<i>j</i>, le ratio d'offre R<sub>j</sub>"+NB+"="+NB+"S<sub>j</sub>"+NB+"/"+NB+"Σ<sub>i</sub>"+NB+"w(d<sub>ij</sub>)"+NB+"·"+NB+"P<sub>i</sub> "
    "rapporte son offre S<sub>j</sub> (nombre d'activités d'audioprothésistes) à la demande "
    "pondérée susceptible de l'atteindre, où P<sub>i</sub> désigne la population de 65 ans et plus "
    "de la commune <i>i</i> et w une fonction décroissante de la distance. Seconde étape : "
    "l'accessibilité de chaque commune <i>i</i> est la somme des ratios accessibles, "
    "APL<sub>i</sub>"+NB+"="+NB+"Σ<sub>j</sub>"+NB+"w(d<sub>ij</sub>)"+NB+"·"+NB+"R<sub>j</sub>. L'offre de chaque commune "
    "équipée est ainsi partagée entre l'ensemble des populations qui s'y adressent."))
E.append(P("Trois adaptations ont été retenues pour la profession. La demande est restreinte à la "
    "population de 65 ans et plus, qui concentre l'essentiel de la presbyacousie appareillable ; "
    "une APL rapportée à la population totale diluerait le signal dans des classes d'âge peu "
    "concernées. La pondération est définie par bandes de distance à vol d'oiseau, en l'absence de "
    "distancier routier homogène couvrant l'outre-mer : coefficient de 1 jusqu'à 10 km, de 0,66 de "
    "10 à 20 km, de 0,33 de 20 à 30 km, nul au-delà, structure décroissante analogue dans son "
    "principe aux bandes de temps des travaux de la DREES [2, 3]. Le rayon de 30 km correspond à "
    "l'ordre de grandeur d'un déplacement compatible avec un suivi répété pour une patientèle "
    "âgée ; cette convention est discutée en section 4.8. L'indicateur est exprimé en "
    "professionnels accessibles pour 100"+NB+"000 habitants de 65 ans et plus."))
E.append(P("La sensibilité de l'indicateur à ces conventions est examinée en section 3.12 au "
    "moyen de trois variantes : une portée réduite à 20 km (coefficients 1 puis 0,5), une "
    "portée étendue à 40 km (1 ; 0,75 ; 0,5 ; 0,25) et une pondération continue gaussienne "
    "d'écart-type 15 km, portée 45 km."))
E.append(H2("2.4. Score d'opportunité d'implantation"))
E.append(P("Le second indicateur répond à une question distincte : parmi les communes non couvertes, "
    "lesquelles réunissent les conditions démographiques et économiques d'une implantation "
    "pertinente ? Dix critères sont normalisés de 0 à 1"+NB+"000 par transformation min-max sur "
    "l'ensemble des communes, les critères « en creux » étant inversés, puis agrégés par somme "
    "pondérée sur un total de 80 points ; l'échelle est sans signification absolue, seul le "
    "classement importe. Le tableau 2 définit chaque critère, sa direction et son poids. La "
    "hiérarchie des poids procède d'un raisonnement professionnel et non d'une estimation "
    "économétrique ; sa part normative est quantifiée par l'analyse de sensibilité "
    "(section 3.10)."))
E.append(P("Tableau 2 — Critères du score d'opportunité, définition, direction et pondération.", CAPT))
E.append(tab([
    ["Critère (poids)", "Définition et justification"],
    ["Absence de concurrence (14)", "Nombre d'activités présentes, inversé. Le premier entrant d'une zone de chalandise capte une patientèle sans alternative locale, avantage durable compte tenu de la fidélisation propre au suivi audioprothétique."],
    ["Distance au plus proche professionnel (12)", "Distance orthodromique à la plus proche commune équipée, plafonnée à 30 km. Distingue la commune de périphérie, couverte de fait, de la commune isolée ; au-delà du plafond, l'éloignement supplémentaire ne modifie plus la situation du patient."],
    ["Taux d'équipement local (10)", "Activités rapportées à la population appareillable estimée (population × part des 65 ans et plus × prévalence conventionnelle de 65 %), inversé. La prévalence, conventionnelle, multiplie identiquement toutes les communes et n'affecte aucun classement relatif."],
    ["Part des 65 ans et plus (10)", "Demande structurelle ; critère le plus stable dans le temps."],
    ["Intensité du sous-équipement (9)", "Habitants par professionnel dans les communes équipées, plafonné à 50 000 ; nul par construction dans les communes sans offre, où le critère de concurrence prend le relais."],
    ["Revenu médian (8)", "Médiane de niveau de vie par UC. La classe II, hors 100 % Santé, conserve un reste à charge : la solvabilité locale demeure un paramètre du modèle économique."],
    ["Potentiel 100 % Santé (7)", "Part de la population orientée vers la classe I sans reste à charge, approchée par une fonction décroissante du revenu médian. Compense le critère précédent : les deux valorisent les deux modèles économiques observés dans la profession."],
    ["Prescripteurs ORL (5)", "Nombre d'ORL libéraux. La primo-prescription étant médicale, leur présence alimente le flux de patients adressés."],
    ["Population municipale (3)", "Taille brute du marché, volontairement peu pondérée : déjà présente en creux dans le taux d'équipement."],
    ["Niveau des loyers (2)", "Loyer d'annonce au m², signal de dynamisme local. Critère le plus discutable, traité comme tel : poids minimal, retrait testé en annexe C."],
], [4.6*cm, 11.4*cm], fs=9))
E.append(P("Le critère de densité de population de la première version a été retiré, la superficie "
    "communale n'étant pas disponible de façon fiable dans la géographie 2025 au moment de la "
    "collecte et son information étant largement redondante avec la population et la distance."))
E.append(P("Le choix de la transformation min-max, qui préserve la forme des distributions, "
    "expose en principe le score à l'influence des valeurs extrêmes ; l'alternative usuelle, la "
    "normalisation par rangs, la neutralise au prix d'un écrasement des écarts réels. Les deux "
    "options ont été calculées et leur concordance est rapportée en section 3.12. Quant au "
    "seuil de 5"+NB+"000 habitants qui délimite la population des « villes » de l'étude, il est "
    "hérité de la première version [1] et correspond à l'ordre de grandeur en deçà duquel une "
    "implantation à titre principal devient rare dans la profession ; il ne prétend à aucune "
    "valeur normative et les données publiées permettent de le déplacer. Le centile du seuil "
    "prioritaire, fixé à 85, procède du même pragmatisme : il retient un ordre de grandeur "
    "d'environ 170 communes, compatible avec un usage opérationnel de la liste, là où un "
    "seuil plus généreux la diluerait et un seuil plus strict la réduirait aux seuls cas "
    "extrêmes ultramarins ; les effectifs aux centiles 80 et 90 sont donnés en "
    "section 3.10."))
E.append(H2("2.5. Définition des communes prioritaires"))
E.append(P("Est dite prioritaire toute commune cumulant trois conditions : population municipale "
    "d'au moins 5"+NB+"000 habitants, aucune activité d'audioprothésiste, et score dans les 15 % "
    "supérieurs de la strate des communes de 5"+NB+"000 habitants et plus (n"+NB+"="+NB+"2"+NB+"276). Le "
    "référentiel de strate remplace le seuil calculé sur l'ensemble des communes qu'utilisait la "
    "première version : l'introduction du critère de distance a rendu ce dernier dégénéré, des "
    "milliers de très petites communes isolées saturant le haut de la distribution nationale du "
    "score au point qu'un seuil national n'aurait retenu que 14 communes. Les effectifs "
    "prioritaires des deux versions (331 puis 173) ne sont donc pas directement comparables ; la "
    "comparaison temporelle pertinente porte sur les communes sans offre (section 3.7). La "
    "sensibilité au centile retenu est donnée en section 3.10, et l'annexe K récapitule l'ensemble des évolutions méthodologiques entre les deux versions."))
E.append(H2("2.6. Dispositif de validation rétrospective"))
E.append(P("La cohorte de validation est constituée des communes de plus de 5"+NB+"000 habitants "
    "(population 2023) sans activité d'audioprothésiste dans les effectifs 2022 de la première "
    "version, appariées entre les deux millésimes par le code géographique : n"+NB+"="+NB+"777. L'issue, "
    "binaire, est la présence d'au moins une activité dans l'extraction d'août 2026. Le prédicteur "
    "est le score d'opportunité tel que publié en 2022, sans réajustement. Les décisions "
    "d'implantation de la période ayant été prises par des acteurs qui ignoraient l'existence du "
    "score, toute concordance mesure la capacité du modèle à capter les déterminants réels de ces "
    "décisions, et non un effet de prophétie autoréalisatrice."))
E.append(P("Le même appariement permet une rétropolation : recalculer distances et APL en ne "
    "retenant que l'offre de 2022, à demande constante (populations 2023), pour isoler l'effet "
    "propre de l'expansion de l'offre sur l'accessibilité. Les 6"+NB+"682 activités du millésime "
    "2022 ne se rattachent toutefois qu'à hauteur de 5"+NB+"907 (88 %) à la géographie 2025 ; "
    "l'accessibilité 2022 ainsi calculée est donc une borne basse, et chaque résultat de la "
    "section 3.13 est encadré par une borne haute obtenue en rehaussant uniformément l'offre "
    "appariée du facteur 6"+NB+"682/5"+NB+"907. L'amélioration mesurée est réelle si elle subsiste "
    "aux deux bornes."))
E.append(H2("2.7. Analyses statistiques"))
E.append(P("Les taux d'équipement sont assortis d'intervalles de confiance à 95 % calculés par la "
    "méthode de Wilson. La discrimination du score est mesurée par l'aire sous la courbe ROC, "
    "estimée par la statistique U de Mann-Whitney et testée par le test unilatéral correspondant. "
    "Les comparaisons de distributions entre groupes utilisent le test de Mann-Whitney bilatéral, "
    "les corrélations sont des corrélations de rang de Spearman ; le seuil de signification retenu "
    "est α"+NB+"="+NB+"0,05. La concentration de l'accessibilité est résumée par un indice de type Gini "
    "calculé sur la courbe de concentration de l'APL, pondérée par la population de 65 ans et "
    "plus. Les traitements ont été réalisés en Python 3 (bibliothèques pandas, NumPy, SciPy, "
    "GeoPandas, Matplotlib). Trois analyses complètent le dispositif principal. La concordance "
    "entre indicateurs (APL, distance, score, population, âge, revenu) est décrite par leur "
    "matrice de corrélations de rang. La capacité de prédicteurs simples (population, âge, "
    "revenu) à reproduire la performance du score composite est comparée par leurs aires sous "
    "la courbe ROC respectives. Enfin, une régression logistique multivariée de l'équipement "
    "2022-2026 sur la population (en logarithme), la part des 65 ans et plus, le revenu médian "
    "et le score 2022, tous centrés-réduits, fournit des rapports de cotes avec leurs "
    "intervalles de confiance ; l'apport marginal du score y est testé par rapport de "
    "vraisemblance. Ces analyses figurent en section 3.11. L'ensemble des tests est de nature descriptive et "
    "exploratoire ; aucune correction de multiplicité n'est appliquée, et les valeurs de p "
    "s'interprètent en conséquence."))
E.append(H2("2.8. Validation croisée et reproductibilité"))
E.append(P("La figure 1 schématise l'ensemble de la chaîne de traitement, des sources aux "
    "analyses."))
E.append(Image("/home/claude/fig_pipeline.png", width=14.6*cm, height=9.5*cm, kind='proportional'))
E.append(P("Figure 1 — Chaîne de traitement de l'étude, des sources aux analyses.", CAPF))
E.append(P("Les comptages RPPS ont été confrontés à deux sources. D'une part le répertoire ADELI du "
    "millésime 2022 [1], pour la cohérence temporelle inter-répertoires ; d'autre part la Base "
    "permanente des équipements de l'Insee, millésime 2025 [10], qui recense l'audioprothèse "
    "d'exercice libéral par une chaîne de production distincte, le type d'équipement pertinent "
    "ayant été identifié par corrélation spatiale avec la distribution RPPS puis vérifié par son "
    "volume national. L'intégralité de la chaîne de traitement (collecte, assemblage, calculs, "
    "figures, présent rapport) est publiée dans le dépôt de l'étude avec les jeux de données "
    "produits ; chaque chiffre du rapport est reconstructible par un tiers ; le dictionnaire des variables du jeu de données figure en annexe D."))

# ═══ 3. RÉSULTATS ═══
E.append(H1("3. Résultats"))
E.append(H2("3.1. L'offre et son absence en 2026"))
E.append(P("Au 30 août 2026, 11"+NB+"018 activités d'audioprothésistes sont rattachées à une commune du "
    "champ. En regard, 560 communes de plus de 5"+NB+"000 habitants n'en comptent aucune ; elles "
    "totalisent 4"+NB+"522"+NB+"768 habitants. Parmi elles, 173 sont classées prioritaires au sens de la "
    "section 2.5, pour 1"+NB+"415"+NB+"508 habitants dont 403"+NB+"934 dans les départements d'outre-mer ; les "
    "DOM comptent 44 des 560 communes sans offre et 32 des 173 prioritaires. La distance médiane au "
    "professionnel le plus proche, pour l'ensemble des communes non équipées, est de 8,1 km. La "
    "figure 2 localise les communes prioritaires ; leur liste intégrale figure en annexe A, "
    "et l'inventaire exhaustif des 560 communes sans offre en annexe I."))
E.append(Image("/home/claude/carte_v2.png", width=14.6*cm, height=15.6*cm, kind='proportional'))
E.append(P("Figure 2 — Les 173 communes prioritaires. La surface des points est proportionnelle à "
    "la population municipale 2023. Sources : RPPS août 2026 [4], Insee [5], fond "
    "france-geojson [9].", CAPF))
E.append(P("La répartition par strate de taille (tableau 3) montre la structure du phénomène : la "
    "part de communes sans offre décroît de 99,8 % dans les communes de moins de 1"+NB+"000 habitants "
    "à 0,8 % au-delà de 50"+NB+"000, tandis que l'APL moyenne pondérée croît de 57 à 93. Une seule "
    "commune de plus de 50"+NB+"000 habitants est dépourvue d'audioprothésiste sur l'ensemble du "
    "champ : Saint-Laurent-du-Maroni (Guyane), dont le professionnel le plus proche se situe à "
    "146,5 km."))
E.append(P("Tableau 3 — Offre et accessibilité par strate de population communale.", CAPT))
str_rows = [["Strate (habitants)", "Communes", "Part sans audioprothésiste", "APL pondérée", "Distance médiane des communes sans offre (km)"]]
for _, r in t_str.iterrows():
    str_rows.append([str(r['strate']), fr(r['n']), dc(r['part_sans'])+" %", f"{r['apl_pond']:.0f}",
                     dc(r['dist_med'])])
E.append(tab(str_rows, [3.4*cm, 2.0*cm, 3.6*cm, 2.4*cm, 4.6*cm], fs=9, align_right={1,2,3,4}))

E.append(H2("3.2. Distribution et concentration de l'accessibilité"))
E.append(P("L'APL nationale s'établit à 77 professionnels accessibles pour 100"+NB+"000 habitants de 65 "
    "ans et plus en moyenne pondérée par la population concernée ; la médiane communale est de 59. "
    "La distribution communale (figure 3) est étalée vers le bas ; ses déciles figurent au "
    "tableau 4. Quatre-vingt-huit communes présentent une APL nulle, aucun professionnel n'étant "
    "accessible à moins de 30 km : 180"+NB+"234 habitants, dont 17"+NB+"206 de 65 ans et plus, sont dans "
    "cette situation, et sept de ces communes dépassent 5"+NB+"000 habitants, toutes situées "
    "outre-mer (liste en annexe H). La courbe de concentration (figure 4) résume l'inégalité de la "
    "distribution : l'indice de concentration, pondéré par la population de 65 ans et plus, "
    "s'établit à 0,19 ; la moitié la moins bien desservie de la population âgée n'accède qu'à "
    "environ un tiers de l'offre pondérée."))
E.append(P("La partition entre l'Hexagone et l'outre-mer traverse toute la distribution : "
    "l'APL moyenne pondérée s'établit à 77 en métropole contre 38 dans les quatre DOM (médianes "
    "communales de 59 contre 23), et les valeurs des quatre territoires ultramarins sont "
    "détaillées en section 3.3."))
E.append(Image("/home/claude/fig_apl_hist.png", width=13.6*cm, height=6.4*cm, kind='proportional'))
E.append(P("Figure 3 — Distribution communale de l'APL (valeurs tronquées à 200 pour la "
    "lisibilité). La ligne verticale marque la médiane.", CAPF))
E.append(P("Tableau 4 — Déciles de la distribution communale de l'APL.", CAPT))
dec_rows = [["", "D1", "D2", "D3", "D4", "D5 (médiane)", "D6", "D7", "D8", "D9"],
            ["APL"] + [f"{apl_dec[f'd{k}']:.0f}" for k in range(10, 100, 10)]]
E.append(tab(dec_rows, [1.5*cm] + [1.42*cm]*4 + [2.25*cm] + [1.42*cm]*4, fs=9, align_right=set(range(1,10))))
E.append(Image("/home/claude/fig_lorenz.png", width=10.6*cm, height=10.2*cm, kind='proportional'))
E.append(P("Figure 4 — Courbe de concentration de l'APL, population de 65 ans et plus classée par "
    "accessibilité croissante.", CAPF))

E.append(H2("3.3. Géographie régionale et départementale"))
E.append(P("L'APL moyenne pondérée par région est représentée en figure 5 ; le tableau 5 rassemble "
    "les indicateurs régionaux et l'annexe E leur déclinaison pour les 100 départements du champ. "
    "En métropole, l'amplitude régionale va de 64 (Normandie) à 92 (Île-de-France). Les quatre "
    "départements-régions d'outre-mer occupent trois des quatre dernières places : 60 à La "
    "Réunion, 27 en Martinique, 25 en Guadeloupe, 11 en Guyane. Les trois APL départementales les "
    "plus faibles de France sont ultramarines, et l'écart interdépartemental extrême est d'un "
    "facteur dix (annexe E). La distance médiane des communes non équipées au professionnel le "
    "plus proche se situe entre 5 et 10 km dans toutes les régions métropolitaines ; elle atteint "
    "105 km en Guyane."))
E.append(Image("/home/claude/fig_apl_regions.png", width=13.2*cm, height=9.5*cm, kind='proportional'))
E.append(P("Figure 5 — APL moyenne pondérée par région, classée par valeur croissante ; en rouge, "
    "les régions dont l'APL est inférieure à 45.", CAPF))
E.append(P("Tableau 5 — Indicateurs par région, classés par APL croissante. La distance médiane "
    "porte sur les communes non équipées.", CAPT))
reg_rows = [["Région", "Communes", "≥ 5 000 hab. sans audioprothésiste", "Prioritaires", "APL pondérée", "Distance médiane (km)", "Activités"]]
for _, r in t_reg.iterrows():
    reg_rows.append([str(r['region']).split(' - ')[-1], fr(r['communes']), fr(r['sans_audio_5k']),
                     fr(r['prioritaires']), f"{r['apl_pond']:.0f}", dc(r['dist_med']), fr(r['activites'])])
E.append(tab(reg_rows, [4.2*cm, 1.8*cm, 2.9*cm, 1.9*cm, 1.9*cm, 2.0*cm, 1.5*cm], fs=8.6,
             align_right={1,2,3,4,5,6}))
E.append(P("La carte départementale (figure 6) précise cette géographie : outre le décrochage "
    "ultramarin, les valeurs basses métropolitaines dessinent le Massif central et ses marges, "
    "ainsi que plusieurs départements normands et du Centre-Val de Loire ; les valeurs hautes "
    "suivent les littoraux urbanisés et les grandes aires urbaines. Les six départements "
    "métropolitains les moins bien desservis sont la Creuse (APL pondérée de 33), les "
    "Alpes-de-Haute-Provence (38), la Haute-Marne (41), l'Indre et les Hautes-Alpes (44) et "
    "l'Allier (45) : la diagonale intérieure, de la Champagne méridionale aux Préalpes, où se "
    "combinent faible densité, vieillissement marqué et éloignement des pôles équipés."))
E.append(Image("/home/claude/carte_apl_dep.png", width=14.2*cm, height=14.3*cm, kind='proportional'))
E.append(P("Figure 6 — APL moyenne pondérée par département ; les quatre DOM sont représentés à la "
    "même échelle de couleur.", CAPF))

E.append(H2("3.4. L'outre-mer"))
E.append(P("Les 44 communes ultramarines de plus de 5"+NB+"000 habitants sans audioprothésiste sont "
    "recensées au tableau 6. La Guyane en compte 9 sur les 22 communes du département, pour des "
    "distances au professionnel le plus proche comprises entre 26 et 283 km ; les sept premières "
    "communes du classement national d'opportunité sont guyanaises (Kourou, "
    "Saint-Laurent-du-Maroni, Mana, Maripasoula, Grand-Santi, Apatou, Papaichton). "
    "Saint-Laurent-du-Maroni, deuxième ville du département avec 54"+NB+"429 habitants, se situe à "
    "146,5 km à vol d'oiseau des deux activités recensées dans l'agglomération de Cayenne ; "
    "Maripasoula et Papaichton, à 283 et 193 km, ne sont pas accessibles par voie routière. Les "
    "Antilles comptent 14 communes concernées en Guadeloupe et 11 en Martinique, à des distances "
    "de 5 à 30 km des pôles équipés ; la part des 65 ans et plus y atteint des niveaux élevés "
    "(29,3 % au Lorrain, Martinique). La Réunion compte 10 communes concernées, dont des bourgs "
    "enclavés des cirques et de la côte au vent (Salazie, Cilaos, Sainte-Rose)."))
E.append(P("Tableau 6 — Les 44 communes d'outre-mer de plus de 5 000 habitants sans "
    "audioprothésiste, par territoire puis population décroissante.", CAPT))
dom_rows = [["Commune", "Territoire", "Population", "Distance (km)", "APL", "Prioritaire"]]
for _, r in t_dom44.iterrows():
    aplv = "0" if (pd.isna(r['apl']) or r['apl'] == 0) else f"{r['apl']:.0f}"
    dom_rows.append([str(r['commune']), str(r['reg_c']), fr(r['population_2023']),
                     dc(r['dist_audio_km']), aplv, "oui" if r['prioritaire_v2'] else "non"])
E.append(tab(dom_rows, [4.4*cm, 2.7*cm, 2.1*cm, 2.1*cm, 1.5*cm, 2.0*cm], fs=8.4,
             align_right={2,3,4}))
E.append(H2("3.5. Le cas francilien"))
E.append(P("L'Île-de-France concentre 105 des 560 communes de plus de 5"+NB+"000 habitants sans "
    "audioprothésiste, l'effectif régional le plus élevé de France ; son APL pondérée, 92, est "
    "simultanément la plus haute. La distance médiane des communes franciliennes non équipées au "
    "professionnel le plus proche est de 5,2 km, la plus faible de toutes les régions. Treize "
    "communes franciliennes figurent néanmoins dans la liste prioritaire. Leur profil est "
    "instructif : à une exception près, il s'agit de communes périurbaines de l'ouest "
    "parisien de 5"+NB+"000 à 8"+NB+"000 habitants et vieillissantes (L'Étang-la-Ville, "
    "Bois-le-Roi, Limours, Saint-Arnoult-en-Yvelines, Louveciennes, Chevreuse), où une "
    "patientèle âgée dense reste captive de pôles voisins ; l'exception, Grigny (26"+NB+"842 "
    "habitants, 9,5 % de 65 ans et plus), doit sa présence aux critères de revenu et de "
    "potentiel 100 % Santé, illustration de ce que le score agrège deux modèles économiques "
    "distincts."))
E.append(H2("3.6. Le classement d'opportunité"))
E.append(P("La distribution du score parmi les 2"+NB+"276 communes de 5"+NB+"000 habitants et plus, et le "
    "seuil du 85<super>e</super> centile qui définit la liste prioritaire, sont représentés en figure 7. "
    "Les trente premières communes du classement figurent au tableau 7 ; huit des neuf premières "
    "sont ultramarines, puis alternent communes antillaises et réunionnaises, bourgs-centres de "
    "l'ouest (Ombrée d'Anjou, Noyant-Villages) et communes enclavées de montagne "
    "(Chamonix-Mont-Blanc, 8"+NB+"705 habitants, 23,0 % de 65 ans et plus, premier professionnel à "
    "14 km)."))
E.append(Image("/home/claude/fig_score_hist.png", width=12.8*cm, height=6.2*cm, kind='proportional'))
E.append(P("Figure 7 — Distribution du score d'opportunité parmi les communes de 5 000 habitants "
    "et plus ; la ligne verticale marque le seuil prioritaire (85<super>e</super> centile).", CAPF))
E.append(P("La liste se décompose en trois profils d'effectifs très inégaux : 32 communes "
    "ultramarines, dont l'ensemble du haut du classement ; 3 communes métropolitaines "
    "distantes de plus de 15 km de toute offre, isolats véritables ; et 138 communes "
    "métropolitaines situées à moins de 15 km d'un professionnel, dont la part médiane de 65 "
    "ans et plus atteint 21,3 % — des marchés de proximité insuffisamment servis plutôt que "
    "des déserts au sens propre. Cette composition importe pour l'interprétation : hors "
    "outre-mer, la priorité désigne rarement le vide, presque toujours l'interstice."))
E.append(P("Tableau 7 — Les trente premières communes prioritaires (liste intégrale en annexe A).", CAPT))
top_rows = [["Rang", "Commune", "Région", "Population", "65 ans et + (%)", "Distance (km)", "APL"]]
for _, r in t_prio.head(30).iterrows():
    p65 = "n. d." if pd.isna(r['part_65_plus_pct']) else dc(r['part_65_plus_pct'])
    aplv = "0" if (pd.isna(r['apl']) or r['apl'] == 0) else f"{r['apl']:.0f}"
    top_rows.append([int(r['rang']), str(r['commune']), str(r['reg_c']), fr(r['population_2023']),
                     p65, dc(r['dist_audio_km']), aplv])
E.append(tab(top_rows, [1.1*cm, 4.2*cm, 3.3*cm, 2.0*cm, 2.0*cm, 1.9*cm, 1.3*cm], fs=8.4,
             align_right={0,3,4,5,6}))
E.append(H2("3.7. Dynamique 2022-2026 et validation rétrospective"))
E.append(P("Entre les millésimes 2022 et 2026, le nombre d'activités recensées est passé de 6"+NB+"682 "
    "à 11"+NB+"018 (+65 %), pour un solde net de 4"+NB+"118 créations sur les communes appariées. Sur les "
    "777 communes de la cohorte de validation (section 2.6), 295 ont accueilli au moins une "
    "activité (38,0 % ; IC 95 % [34,6 ; 41,4]), 482 sont restées sans offre, et 64 communes hors "
    "cohorte ont perdu leur dernière activité ou franchi le seuil de population sans en disposer "
    "(liste en annexe F ; celle des 295 communes équipées figure en annexe G). Le taux d'équipement croît avec le quintile du score 2022, de 30,8 % à "
    "54,5 % (figure 8 et tableau 8) ; les communes classées prioritaires par la version 2022 ont "
    "été équipées à 46,3 % (150/324 ; IC 95 % [40,9 ; 51,7]) contre 32,0 % pour les autres "
    "(145/453 ; IC 95 % [27,9 ; 36,4]) ; les intervalles des deux groupes sont disjoints, et l'écart de 14 points correspond à un taux relatif de 1,45. L'aire sous la courbe ROC est de 0,597 "
    "(p"+NB+"="+NB+"3,0"+NB+"×"+NB+"10<super>-6</super>, test de Mann-Whitney unilatéral, n"+NB+"="+NB+"777). À l'échelle de "
    "l'ensemble des communes, 48 % des créations nettes se concentrent dans les deux déciles "
    "supérieurs du score 2022, le dixième décile en absorbant 1"+NB+"148 quand le premier en perd 49 "
    "(figure 9)."))
E.append(Image("/home/claude/fig_quintiles.png", width=12.4*cm, height=6.2*cm, kind='proportional'))
E.append(P("Figure 8 — Taux d'équipement 2022-2026 des communes de la cohorte, par quintile du "
    "score 2022 (n = 777).", CAPF))
E.append(P("Tableau 8 — Taux d'équipement par quintile du score 2022, avec intervalles de "
    "confiance de Wilson à 95 %.", CAPT))
qi_rows = [["Quintile du score 2022", "n", "Communes équipées", "Taux (%)", "IC 95 %"]]
for _, r in t_qi.iterrows():
    qi_rows.append([str(r['quintile']), int(r['n']), int(r['k']), dc(r['taux']),
                    "["+dc(r['ic_lo'])+" ; "+dc(r['ic_hi'])+"]"])
E.append(tab(qi_rows, [3.6*cm, 1.6*cm, 2.6*cm, 2.0*cm, 3.4*cm], fs=9, align_right={1,2,3,4}))
E.append(Image("/home/claude/fig_flux_deciles.png", width=13.4*cm, height=6.3*cm, kind='proportional'))
E.append(P("Figure 9 — Créations nettes d'activités 2022-2026 par décile du score 2022, ensemble "
    "des communes appariées.", CAPF))
E.append(H2("3.8. Caractéristiques des communes équipées et non équipées"))
E.append(P("Le tableau 9 compare les 295 communes équipées entre 2022 et 2026 aux 482 restées sans "
    "offre. Les communes équipées sont plus peuplées (médianes de 8"+NB+"191 contre 6"+NB+"540 habitants ; "
    "p"+NB+"&lt;"+NB+"0,001) ; aucune différence significative n'apparaît sur la part des 65 ans et plus "
    "(p"+NB+"="+NB+"0,69) ni sur le revenu médian (p"+NB+"="+NB+"0,27). La distance médiane des communes restées "
    "sans offre au professionnel le plus proche est de 3,6 km (intervalle interquartile "
    "[2,5 ; 5,7]). Les quinze plus grandes communes de chaque groupe figurent aux tableaux 10 "
    "et 11."))
E.append(P("Tableau 9 — Caractéristiques comparées des communes équipées entre 2022 et 2026 et des "
    "communes restées sans offre (médiane [Q1 ; Q3] ; test de Mann-Whitney bilatéral).", CAPT))
eqx_rows = [["Variable", "Équipées (n = 295)", "Restées sans offre (n = 482)", "p"]]
for _, r in t_eqx.iterrows():
    f1 = fr(r['eq_med']) if r['eq_med'] > 1000 else dc(r['eq_med'])
    q1a, q3a = (fr(r['eq_q1']), fr(r['eq_q3'])) if r['eq_q1'] > 1000 else (dc(r['eq_q1']), dc(r['eq_q3']))
    f2 = fr(r['pe_med']) if r['pe_med'] > 1000 else dc(r['pe_med'])
    q1b, q3b = (fr(r['pe_q1']), fr(r['pe_q3'])) if r['pe_q1'] > 1000 else (dc(r['pe_q1']), dc(r['pe_q3']))
    pv = "&lt; 0,001" if r['p'] < 0.001 else dc(r['p'], 2)
    eqx_rows.append([str(r['variable']), f"{f1} [{q1a} ; {q3a}]", f"{f2} [{q1b} ; {q3b}]", pv])
E.append(tab(eqx_rows, [5.6*cm, 4.0*cm, 4.4*cm, 1.6*cm], fs=8.8, align_right={3}))
E.append(P("Tableau 10 — Les quinze plus grandes communes équipées entre 2022 et 2026.", CAPT))
eq_rows = [["Commune", "Région", "Population", "Activités 2026"]]
for _, r in t_eq10.head(15).iterrows():
    eq_rows.append([str(r['commune']), str(r['reg_c']), fr(r['population_2023']),
                    int(r['nb_audioprothesistes_2026'])])
E.append(tab(eq_rows, [5.2*cm, 4.2*cm, 2.6*cm, 2.6*cm], fs=8.8, align_right={2,3}))
E.append(P("Tableau 11 — Les quinze plus grandes communes restées sans audioprothésiste.", CAPT))
pe_rows = [["Commune", "Région", "Population", "Distance (km)"]]
for _, r in t_pe10.head(15).iterrows():
    pe_rows.append([str(r['commune']), str(r['reg_c']), fr(r['population_2023']),
                    dc(r['dist_audio_km'])])
E.append(tab(pe_rows, [5.2*cm, 4.2*cm, 2.6*cm, 2.6*cm], fs=8.8, align_right={2,3}))
E.append(H2("3.9. Cumul d'accès faible, de besoin élevé et de revenus modestes"))
E.append(P("Sont dénombrées les communes appartenant simultanément au tiers inférieur de la "
    "distribution de l'APL, au tiers supérieur de la part des 65 ans et plus et au tiers "
    "inférieur du revenu médian : 2"+NB+"992 communes répondent à cette triple condition, totalisant "
    "2"+NB+"194"+NB+"149 habitants dont 715"+NB+"915 de 65 ans et plus ; leur APL médiane est de 34, contre "
    "59 pour l'ensemble des communes. Leur localisation (figure 10) couvre principalement la "
    "Nouvelle-Aquitaine (891 communes), Auvergne-Rhône-Alpes (483), l'Occitanie (468), la "
    "Bourgogne-Franche-Comté (291) et le Centre-Val de Loire (235). Trente-sept dépassent 5"+NB+"000 "
    "habitants (liste en annexe B) ; les quinze premières par population âgée figurent au "
    "tableau 12, parmi lesquelles Montluçon (33"+NB+"147 habitants ; 28 % de 65 ans et plus ; revenu "
    "médian de 21"+NB+"980 € ; APL de 49), Vierzon, Aurillac, Montceau-les-Mines, Digne-les-Bains et "
    "Fécamp."))
E.append(Image("/home/claude/carte_doublepeine.png", width=13.6*cm, height=12.4*cm, kind='proportional'))
E.append(P("Figure 10 — Localisation des 2 992 communes cumulant accès faible, part élevée de 65 "
    "ans et plus et revenus modestes (métropole ; surface des points proportionnelle à la "
    "population de 65 ans et plus).", CAPF))
E.append(P("Tableau 12 — Les quinze premières communes de plus de 5 000 habitants du cumul, "
    "classées par population de 65 ans et plus décroissante (liste complète en annexe B).", CAPT))
dp_rows = [["Commune", "Région", "Population", "65 ans et + (%)", "Revenu médian (€/UC)", "APL"]]
for _, r in t_dp.head(15).iterrows():
    dp_rows.append([str(r['commune']), str(r['reg_c']), fr(r['population_2023']),
                    f"{r['part_65_plus_pct']:.0f}", fr(r['revenu_median_uc']), f"{r['apl']:.0f}"])
E.append(tab(dp_rows, [3.9*cm, 3.3*cm, 2.0*cm, 2.1*cm, 2.6*cm, 1.2*cm], fs=8.6,
             align_right={2,3,4,5}))
E.append(H2("3.10. Sensibilité et validation croisée des comptages"))
E.append(P("La perturbation de chacun des dix poids du score de ±20 % (vingt configurations) "
    "laisse la liste prioritaire quasi inchangée : recouvrement médian de 99,4 % avec la liste de "
    "référence, minimum de 84,4 % (détail en annexe C). Le retrait complet d'un critère est plus "
    "discriminant : sans la distance, le recouvrement tombe à 18 % ; sans l'absence de "
    "concurrence, à 71 % ; sans le revenu, à 75 % ; les autres critères pèsent marginalement un à "
    "un. La variation du centile du seuil produit des listes de 234 (80<super>e</super>), 173 "
    "(85<super>e</super>) et 125 communes (90<super>e</super>) ; l'imputation des revenus manquants, testée "
    "par retrait du critère, est sans effet notable. Sur la cohérence des sources : les comptages "
    "ADELI 2022 et RPPS 2026 présentent, sur les 2"+NB+"959 communes couvertes par au moins un des "
    "deux répertoires, une corrélation de rang de 0,53 (p"+NB+"&lt;"+NB+"10<super>-217</super>), et 83,5 % des "
    "communes équipées en 2022 le sont encore en 2026. La Base permanente des équipements "
    "(millésime 2025, exercice libéral, 3"+NB+"005 équipements sur 1"+NB+"542 communes) confirme 98,8 % "
    "des communes qu'elle recense comme équipées, 99,1 % des 560 communes sans offre du présent "
    "travail et 98,8 % des 173 communes prioritaires ; les cinq divergences portent chacune sur "
    "un ou deux équipements. La corrélation de rang entre les deux comptages est de 0,50 "
    "(p"+NB+"&lt;"+NB+"10<super>-169</super>)."))
E.append(H2("3.11. Concordance des indicateurs et analyse multivariée de l'implantation"))
E.append(P("La matrice des corrélations de rang entre les six variables centrales (figure 11 et "
    "tableau 13) précise l'architecture de la mesure. Le score est très fortement associé à la "
    "distance (0,90), qui en est le critère structurant, et modérément, en négatif, à l'APL "
    "(-0,46) : les deux indicateurs se recoupent sans se confondre, ce qui était leur cahier "
    "des charges. L'APL est corrélée positivement à la population (0,35) et au revenu (0,31), "
    "négativement à la part des 65 ans et plus (-0,27) : l'accessibilité est meilleure là où la "
    "population est nombreuse, aisée et jeune, configuration inverse de celle du besoin. La "
    "distance et la population sont négativement associées (-0,52), rappel que l'éloignement "
    "est d'abord un phénomène de petites communes."))
E.append(Image("/home/claude/fig_corr.png", width=12.6*cm, height=10.2*cm, kind='proportional'))
E.append(P("Figure 11 — Corrélations de rang de Spearman entre les six variables centrales "
    "(34"+NB+"900 communes ; toutes significatives à p"+NB+"&lt;"+NB+"0,001).", CAPF))
E.append(P("Tableau 13 — Matrice des corrélations de rang (valeurs de la figure 11).", CAPT))
cm_rows = [[""] + list(t_corrm.columns)]
for idx, row in t_corrm.iterrows():
    cm_rows.append([idx] + [dc(v, 2) for v in row.values])
E.append(tab(cm_rows, [3.0*cm] + [2.15*cm]*6, fs=8.6, align_right=set(range(1, 7))))
E.append(P("La concentration de l'offre par commune reste modérée : les 100 communes les mieux "
    "dotées portent 22,0 % des activités, la moitié de l'offre nationale est atteinte à la "
    "405<super>e</super> commune, et le premier centile des 2"+NB+"706 communes équipées n'en "
    "concentre que 9,1 %. Le réseau de l'audioprothèse est donc un réseau de villes moyennes "
    "davantage qu'un réseau métropolitain, ce qui rend la question des interstices non couverts "
    "d'autant plus tranchante."))
E.append(P("La comparaison des pouvoirs discriminants (figure 12) apporte le résultat le plus "
    "important de cette section : la population seule prédit l'équipement 2022-2026 avec une "
    "AUC de 0,645 (p"+NB+"="+NB+"4,8"+NB+"×"+NB+"10<super>-12</super>), supérieure à celle du score composite "
    "(0,597) ; la part des 65 ans et plus (0,508) et le revenu (0,476) sont, seuls, sans aucun "
    "pouvoir prédictif. La régression logistique multivariée (tableau 14) décompose ce "
    "constat : à variables centrées-réduites, un écart-type de population (en logarithme) "
    "multiplie la cote d'équipement par 2,22 (IC 95 % [1,69 ; 2,92] ; p"+NB+"&lt;"+NB+"0,001) et, à "
    "taille contrôlée, un écart-type de part des 65 ans et plus la multiplie par 1,36 "
    "([1,13 ; 1,64] ; p"+NB+"="+NB+"0,001), tandis que le revenu reste sans effet (p"+NB+"="+NB+"0,87). Le "
    "score 2022 n'apporte aucun signal supplémentaire une fois ses composantes contrôlées "
    "(rapport de cotes 0,82 ; p"+NB+"="+NB+"0,17 ; test du rapport de vraisemblance "
    "p"+NB+"="+NB+"0,17), ce qui est attendu d'un indice construit à partir d'elles ; l'ajout de "
    "l'âge et du revenu à la population seule améliore en revanche significativement "
    "l'ajustement (p"+NB+"="+NB+"0,011). Les pseudo-R<super>2</super> restent faibles (0,05 à 0,06 selon "
    "le modèle ; n"+NB+"="+NB+"730), à la mesure du bruit propre aux décisions individuelles "
    "d'implantation."))
E.append(Image("/home/claude/fig_roc.png", width=10.8*cm, height=10.4*cm, kind='proportional'))
E.append(P("Figure 12 — Courbes ROC de la prédiction de l'équipement 2022-2026 par le score "
    "2022 et par la population seule (cohorte, n"+NB+"="+NB+"777).", CAPF))
E.append(P("Tableau 14 — Régression logistique de l'équipement 2022-2026 (modèle complet ; "
    "variables centrées-réduites ; n"+NB+"="+NB+"730 communes aux quatre variables renseignées).", CAPT))
lg_rows = [["Variable", "Rapport de cotes", "IC 95 %", "p"]]
for _, r in t_logit.iterrows():
    pv = "&lt; 0,001" if r['p'] < 0.001 else dc(r['p'], 3)
    lg_rows.append([str(r['variable']), dc(r['or'], 2),
                    "["+dc(r['lo'], 2)+" ; "+dc(r['hi'], 2)+"]", pv])
E.append(tab(lg_rows, [5.4*cm, 3.2*cm, 4.0*cm, 2.2*cm], fs=9, align_right={1,2,3}))
E.append(P("La déclinaison régionale de la validation (figure 13) montre enfin que le "
    "rattrapage n'a pas été homogène : le taux d'équipement des communes de la cohorte va de "
    "50,0 % en Bretagne et 44,7 % en Auvergne-Rhône-Alpes à 23,2 % dans le Grand Est, les "
    "effectifs régionaux restant modestes (16 à 138 communes). Les 64 communes du mouvement "
    "inverse (annexe F) présentent le profil des périphéries : population médiane de 7"+NB+"182 "
    "habitants, part des 65 ans et plus médiane de 19,9 %, et surtout distance médiane de "
    "4,3 km au professionnel le plus proche, signature de fermetures ou de transferts vers un "
    "pôle voisin plutôt que d'apparitions d'isolats."))
E.append(Image("/home/claude/fig_vreg.png", width=12.8*cm, height=8.8*cm, kind='proportional'))
E.append(P("Figure 13 — Taux d'équipement 2022-2026 des communes de la cohorte par région "
    "(régions d'au moins 15 communes de cohorte).", CAPF))
E.append(H2("3.12. Variantes méthodologiques : portée de l'APL, normalisation, définition du cumul"))
E.append(P("Les trois variantes de la fonction de pondération de l'APL annoncées en section 2.3 "
    "sont confrontées à la version de référence au tableau 15. Les classements communaux sont "
    "stables : corrélations de rang de 0,81 avec la portée courte de 20 km, de 0,89 avec la "
    "portée de 40 km et de 0,95 avec la pondération gaussienne ; la moyenne nationale pondérée "
    "est insensible au choix (75,7 dans les trois cas, contre 77 pour la référence). Seule la "
    "part de communes d'accessibilité nulle réagit fortement, par construction, à la portée : "
    "3,3 % à 20 km contre moins de 0,1 % à 40 km ou en pondération continue. Les constats de "
    "l'étude ne dépendent donc pas du rayon retenu, à l'exception du dénombrement des communes "
    "à APL nulle, qui doit se lire comme relatif à la convention des 30 km."))
E.append(P("Tableau 15 — Variantes de la fonction de pondération de l'APL, comparées à la "
    "référence (bandes 1 ; 0,66 ; 0,33 ; portée 30 km).", CAPT))
av_rows = [["Variante", "Corrélation de rang avec la référence", "Communes d'APL nulle (%)", "Moyenne pondérée"]]
for _, r in t_aplv.iterrows():
    av_rows.append([str(r['variante']), dc(r['spearman_vs_base'], 2),
                    dc(r['pct_apl_nulle'], 1), dc(r['moy_pond'], 1)])
E.append(tab(av_rows, [5.6*cm, 4.0*cm, 3.2*cm, 2.6*cm], fs=8.8, align_right={1,2,3}))
E.append(P("La normalisation par rangs, substituée à la transformation min-max toutes choses "
    "égales par ailleurs, produit une liste prioritaire recouvrant 88,4 % de la liste de "
    "référence : l'écrasement des écarts extrêmes déplace quelques communes en lisière de "
    "seuil sans toucher la tête du classement. Enfin, resserrer la définition du cumul de la "
    "section 3.9 des tertiles aux quartiles (quart inférieur d'APL, quart supérieur de part "
    "des 65 ans et plus, quart inférieur de revenu) réduit l'effectif de 2"+NB+"992 à 2"+NB+"076 "
    "communes, pour 1"+NB+"398"+NB+"774 habitants dont 475"+NB+"250 de 65 ans et plus : l'ordre de "
    "grandeur, deux millions de personnes autour, résiste au choix du découpage. Prises ensemble, les variantes de cette section et de la "
    "précédente dessinent la hiérarchie des fragilités méthodologiques de l'étude : les "
    "classements et les ordres de grandeur sont stables sous toutes les perturbations "
    "testées ; les dénombrements absolus qui dépendent d'un seuil (communes d'APL nulle, "
    "effectif exact du cumul, taille de la liste prioritaire) sont les seules quantités "
    "sensibles aux conventions, et doivent se citer accompagnés des leurs."))
E.append(H2("3.13. Ce que quatre années ont changé : rétropolation à offre 2022"))
E.append(P("Le recalcul des indicateurs d'accessibilité avec la seule offre de 2022, à demande "
    "constante et selon le dispositif d'encadrement de la section 2.6, dresse le bilan propre "
    "de l'expansion. L'APL moyenne pondérée passe de 43,6 [borne haute : 49,3] à 75,7, soit un "
    "gain de 54 à 74 % ; la médiane communale, de 37,8 [42,7] à 58,6. Le tableau 16 met en "
    "regard les déciles des deux distributions : l'ensemble de la distribution s'est déplacé "
    "vers le haut, le premier décile passant de 20 [23] à 30. Surtout, la population âgée en "
    "situation d'accessibilité faible s'est contractée massivement : 2,44 [1,70] millions de "
    "personnes de 65 ans et plus résidaient en 2022 dans une commune d'APL inférieure à 30 ; "
    "elles sont 0,50 million en 2026, une division par 3,4 à 4,9 qui subsiste aux deux bornes "
    "et constitue, en termes d'accès, le principal acquis de la période. La population "
    "résidant à moins de 10 km d'une commune équipée est passée de 57,3 à 59,1 millions, de "
    "88,8 à 91,6 % du champ ; la distance médiane des villes de plus de 5"+NB+"000 habitants "
    "sans offre au premier professionnel, elle, n'a presque pas bougé (4,2 puis 3,8 km, la "
    "valeur 2022 étant elle-même surestimée par construction) : l'expansion a résorbé des "
    "communes proches de l'offre existante, elle n'a pas déplacé la frontière des isolats, ce "
    "que la figure 14 visualise par les fonctions de répartition des deux millésimes."))
E.append(P("Tableau 16 — Déciles de la distribution communale de l'APL, offre 2022 (bornes "
    "basse et haute) et offre 2026, à demande constante.", CAPT))
rt_rows = [["Quantile", "10 %", "30 %", "Médiane", "70 %", "90 %"]]
rd = t_rdec.set_index('q')
rt_rows.append(["APL, offre 2022 (borne basse)"] + [f"{rd.loc[q,'apl22']:.0f}" for q in [0.1,0.3,0.5,0.7,0.9]])
rt_rows.append(["APL, offre 2022 (borne haute)"] + [f"{rd.loc[q,'apl22']*1.131:.0f}" for q in [0.1,0.3,0.5,0.7,0.9]])
rt_rows.append(["APL, offre 2026"] + [f"{rd.loc[q,'apl26']:.0f}" for q in [0.1,0.3,0.5,0.7,0.9]])
E.append(tab(rt_rows, [5.6*cm, 1.9*cm, 1.9*cm, 2.1*cm, 1.9*cm, 1.9*cm], fs=8.8,
             align_right={1,2,3,4,5}))
E.append(Image("/home/claude/fig_retro_ecdf.png", width=12.6*cm, height=7.4*cm, kind='proportional'))
E.append(P("Figure 14 — Fonction de répartition de la distance au professionnel le plus "
    "proche, communes de plus de 5"+NB+"000 habitants sans offre, millésimes 2022 et 2026.", CAPF))
E.append(P("La structure du réseau s'est enfin transformée dans les deux sens à la fois : le "
    "nombre de communes équipées est passé de 2"+NB+"244 (offre appariée) à 2"+NB+"661, extension "
    "de la couverture, tandis que l'indice de Gini du nombre d'activités par commune équipée "
    "montait de 0,45 à 0,51, épaississement simultané des implantations existantes. "
    "L'expansion n'a donc pas été qu'un essaimage : près de la moitié des créations "
    "(section 3.7) a densifié des communes déjà servies, cohérente avec la logique de taille "
    "mise en évidence par l'analyse multivariée."))
E.append(P("La déclinaison régionale du bilan (tableau 17 et figure 15) montre enfin où ces "
    "quatre années ont porté. En retenant par prudence la borne haute de 2022, les "
    "progressions relatives les plus fortes reviennent à La Réunion (24 à 60, soit +151 %), à "
    "la Martinique (+143 %) et à l'Île-de-France (+84 %), les plus faibles à la "
    "Bourgogne-Franche-Comté (+23 %) et à la Corse (+30 %) ; la Guyane, partie d'une offre "
    "appariée nulle, ne se prête pas au calcul d'un taux. L'expansion a donc resserré une "
    "partie de l'écart ultramarin, à partir de niveaux si bas que les quatre DOM demeurent, "
    "en 2026, aux quatre derniers rangs ; et elle a simultanément creusé l'avance "
    "francilienne, illustration régionale de la logique de densification décrite plus haut."))
E.append(P("Tableau 17 — APL moyenne pondérée par région, offre 2022 (deux bornes) et offre "
    "2026, à demande constante ; classement par APL 2026 croissante.", CAPT))
rr_rows = [["Région", "2022, borne basse", "2022, borne haute", "2026", "Gain minimal (%)"]]
for _, r in t_rreg.iterrows():
    gain = "n. a." if r['apl22_haut'] < 1 else dc((r['apl26']/r['apl22_haut']-1)*100, 0)
    rr_rows.append([str(r['region']), dc(r['apl22_bas'], 0), dc(r['apl22_haut'], 0),
                    dc(r['apl26'], 0), gain])
E.append(tab(rr_rows, [4.6*cm, 2.6*cm, 2.6*cm, 1.9*cm, 2.7*cm], fs=8.6, align_right={1,2,3,4}))
E.append(Image("/home/claude/fig_retro_reg.png", width=13.4*cm, height=10.6*cm, kind='proportional'))
E.append(P("Figure 15 — APL moyenne pondérée par région, 2022 (borne haute) et 2026, à "
    "demande constante (valeurs du tableau 17).", CAPF))
E.append(P("Le tableau 18 rassemble, pour conclure cette section, les principaux indicateurs "
    "nationaux des deux millésimes ; les valeurs 2022 issues de la rétropolation y sont "
    "données sous leurs deux bornes."))
E.append(P("Tableau 18 — Synthèse nationale des deux millésimes. Les valeurs 2022 marquées "
    "d'un astérisque sont rétropolées et données en bornes basse et haute (section 2.6).", CAPT))
sy_rows = [["Indicateur", "2022", "2026"],
    ["Activités recensées", "6"+NB+"682 (ADELI)", "11"+NB+"018 (RPPS)"],
    ["Communes équipées", "2"+NB+"244 (appariées)", "2"+NB+"661"],
    ["Communes de plus de 5 000 habitants sans offre", "777 (cohorte appariée)", "560"],
    ["APL moyenne pondérée*", "43,6 - 49,3", "75,7"],
    ["APL médiane communale*", "37,8 - 42,7", "58,6"],
    ["65 ans et plus sous APL 30 (millions)*", "2,44 - 1,70", "0,50"],
    ["Population à moins de 10 km d'une offre (millions)*", "57,3", "59,1"],
    ["Distance médiane des villes sans offre (km)*", "4,2", "3,8"],
    ["Gini du nombre d'activités par commune équipée*", "0,45", "0,51"],
]
E.append(tab(sy_rows, [8.2*cm, 4.0*cm, 3.0*cm], fs=8.8, align_right={1,2}))
E.append(P("Aucune de ces évolutions ne doit toutefois occulter la constante de la période : "
    "la géographie des isolats, guyanaise au premier chef, est identique dans les deux "
    "millésimes, et c'est précisément ce que quatre années du régime de croissance le plus "
    "favorable n'ont pas entamé qui définit le périmètre irréductible de l'action publique."))

# ═══ 4. DISCUSSION ═══
E.append(H1("4. Discussion"))
E.append(H2("4.1. Portée de la validation rétrospective"))
E.append(P("Le résultat central de cette étude est la concordance entre le classement publié sur "
    "données 2022 et la localisation effective des implantations de la période 2022-2026. Un "
    "gradient monotone des taux d'équipement par quintile, un rapport de 1,45 entre communes "
    "désignées prioritaires et les autres, et la concentration de 48 % des créations nettes dans "
    "les deux déciles supérieurs établissent que le score capte des déterminants réels des "
    "décisions d'implantation. L'AUC de 0,597 en fixe la limite : le score capte une partie du "
    "signal, non la décision individuelle, dont le bruit tient aux opportunités immobilières, aux "
    "successions et aux stratégies d'enseigne. Trois circonstances renforcent la portée de ce "
    "résultat : il est obtenu hors échantillon au sens le plus strict, sur des décisions "
    "postérieures à la publication du modèle et prises par des acteurs qui l'ignoraient ; le "
    "gradient ne présente aucune inversion ; et il résiste à la variation des pondérations "
    "(section 3.10). Pour l'usage revendiqué, hiérarchiser des territoires, cette validité "
    "suffit ; pour prédire l'implantation commune par commune, elle ne suffirait pas, et l'étude "
    "ne le revendique pas."))
E.append(P("L'analyse multivariée de la section 3.11 précise ce que le score capte, et ce "
    "qu'il ne cherche pas à capter. La population seule prédit l'équipement mieux que le score "
    "composite (AUC de 0,645 contre 0,597) : le marché est encore plus « taille-dépendant » "
    "que l'indice, qui ne consacre que 3 points sur 80 à la population brute, précisément pour "
    "ne pas recommander ce que le marché fait sans aide. Un score conçu pour prévoir les "
    "implantations aurait donc surpondéré la taille ; celui-ci hiérarchise le besoin et "
    "l'opportunité non servis, ce qui est un autre objet. Que ses cibles aient malgré cela été "
    "équipées à des taux croissant régulièrement avec le score établit qu'il n'est pas "
    "orthogonal à la réalité du marché ; qu'il n'ajoute aucun signal une fois ses composantes "
    "contrôlées (tableau 14) rappelle qu'il n'est rien de plus, mais rien de moins, que leur "
    "agrégation raisonnée. Deux précautions bornent enfin la lecture de ces comparaisons : "
    "l'issue équipée/non équipée agrège quatre années sans distinguer la date ni l'ampleur "
    "des ouvertures, et la cohorte, bornée aux communes de plus de 5"+NB+"000 habitants sans "
    "offre initiale, tronque précisément la variable de taille dont elle mesure l'effet ; "
    "l'AUC de la population y est donc, s'il fallait la préciser, plutôt sous-estimée que "
    "surestimée, ce qui renforce le constat."))
E.append(H2("4.2. Ce que la dynamique du marché révèle"))
E.append(P("La composition de l'expansion est aussi instructive que son ampleur. Les communes "
    "équipées entre 2022 et 2026 se distinguent des communes restées sans offre par leur seule "
    "population ; ni le vieillissement ni le revenu ne diffèrent significativement entre les deux "
    "groupes (tableau 9). L'interprétation la plus parcimonieuse est que l'expansion a suivi une "
    "logique de taille de bassin : un comportement de conquête de parts de marché, conforme à "
    "ce qu'on attend d'acteurs privés en phase de croissance. L'analyse multivariée nuance "
    "utilement la lecture bivariée : à taille de commune contrôlée, le vieillissement local "
    "augmente bien la probabilité d'implantation (rapport de cotes de 1,36 par écart-type ; "
    "tableau 14), signal que masquait la comparaison brute des médianes parce que les communes "
    "âgées de la cohorte sont aussi les plus petites. Le marché n'est donc pas aveugle à l'âge "
    "à taille donnée ; il l'est au revenu, et il reste dominé par la taille. Le bilan agrégé n'en est pas moins "
    "substantiel : la rétropolation de la section 3.13 montre que l'expansion, si mal ciblée "
    "soit-elle au regard du besoin, a divisé par plus de trois la population âgée en situation "
    "d'accessibilité faible. Un marché qui croît de 65 % améliore l'accès presque partout, y "
    "compris là où il ne visait rien ; ce qu'il laisse intact, la frontière des isolats et les "
    "territoires de la section 3.9, n'en ressort que plus nettement comme le domaine propre de "
    "l'action publique. Il s'en déduit une délimitation utile au débat "
    "public : ce que quatre années d'expansion exceptionnelle n'ont pas rémunéré, un régime de "
    "croisière le rémunérera moins encore ; les territoires du cumul décrit en section 3.9 et "
    "l'intérieur ultramarin ne seront pas équipés par le seul jeu concurrentiel."))
E.append(H2("4.3. Compter les communes vides ou mesurer l'accès"))
E.append(P("Deux résultats convergent pour disqualifier le comptage communal comme mesure d'accès. "
    "Les communes restées sans audioprothésiste se situent à 3,6 km en médiane du premier "
    "professionnel : la grande majorité des « communes sans offre » sont des communes de "
    "périphérie, couvertes de fait par un pôle limitrophe. Le cas francilien pousse la logique à "
    "son terme : la région cumule le plus grand nombre de communes sans offre et la meilleure "
    "accessibilité de France, la maille communale y étant simplement plus fine que la maille "
    "réelle des déplacements. Le comptage majore ainsi le manque partout où les communes sont "
    "petites et le minore où elles sont vastes, la Guyane en étant le cas extrême inverse. La Creuse fournit la contre-épreuve "
    "métropolitaine : aucune de ses communes de plus de 5"+NB+"000 habitants n'est dépourvue "
    "d'audioprothésiste, si bien que le comptage n'y signale rien, alors que son APL pondérée "
    "de 33 en fait le département le moins bien desservi de métropole, l'essentiel de sa "
    "population rurale et très âgée résidant loin des douze activités que comptent ses "
    "quelques villes. L'APL "
    "corrige les deux biais et devrait constituer la mesure de référence de l'accès à "
    "l'audioprothèse ; le comptage conserve une valeur de communication, le score d'opportunité "
    "une valeur opérationnelle, et les trois lectures sont publiées dans le même jeu de "
    "données. La matrice de la section 3.11 donne à ce constat sa forme quantitative : "
    "corrélée à -0,46 au score et à -0,47 à la distance, l'APL mesure bien autre chose que ce "
    "que mesurent le comptage et l'éloignement, et la configuration de ses corrélats — "
    "positive avec la population et le revenu, négative avec l'âge — décrit une accessibilité "
    "structurellement disposée à l'inverse du besoin."))
E.append(H2("4.4. L'outre-mer, un problème d'équipement sanitaire du territoire"))
E.append(P("Le facteur sept qui sépare la Guyane de l'Hexagone, la présence des sept premières "
    "communes du classement dans ce seul département et l'existence d'une ville de 54"+NB+"000 "
    "habitants à 146 km de toute offre changent la nature de la question posée. À ces échelles, "
    "il ne s'agit plus d'optimiser une implantation commerciale mais d'équiper un territoire, ce "
    "qui relève des mêmes registres que l'accès aux autres soins spécialisés dans ces zones : "
    "consultations avancées, équipes mobiles, télé-audiologie pour ce qui peut l'être, aide au "
    "transport pour ce qui ne le peut pas. Les distances à vol d'oiseau utilisées ici minorent "
    "de surcroît la réalité guyanaise, où plusieurs communes du classement ne sont accessibles "
    "que par voie fluviale ou aérienne ; les chiffres publiés constituent donc des bornes "
    "inférieures du problème. Les Antilles et La Réunion appellent une réponse différente de "
    "la Guyane : les distances y sont de l'ordre de la desserte périurbaine (5 à 30 km), mais "
    "elles se combinent à un vieillissement rapide, à des revenus médians parmi les plus "
    "faibles du pays et à des réseaux de transport en commun limités, si bien que la même "
    "distance n'y a pas le même coût qu'en métropole. Le maillage y progresse : la Guadeloupe "
    "et La Réunion figurent parmi les régions dont les communes de la cohorte ont été le plus "
    "équipées entre 2022 et 2026 (40,0 et 44,4 %, figure 13) ; les 25 communes antillaises et "
    "réunionnaises de la liste prioritaire indiquent où ce mouvement a la plus forte valeur "
    "sanitaire à se poursuivre."))
E.append(H2("4.5. Le cumul accès-âge-revenus et la limite du levier financier"))
E.append(P("Les 2"+NB+"992 communes de la section 3.9 délimitent la population pour laquelle la "
    "logique du 100 % Santé rencontre sa limite : le reste à charge y est nul, mais l'offre est "
    "distante et la population concernée est celle qui se déplace le moins. Que trente-sept "
    "villes de plus de 5"+NB+"000 habitants, de Montluçon à Fécamp, figurent dans cette liste "
    "indique que le phénomène ne se réduit pas au rural isolé : il touche des villes moyennes "
    "dont l'offre existante, rapportée à une population âgée nombreuse, reste insuffisante. Les "
    "instruments pertinents y sont connus des autres professions de santé : zonages "
    "conventionnels incitatifs, permanences en maison de santé, contractualisation locale. La "
    "liste communale publiée en annexe B en fournit la cible directement utilisable. L'exemple de la Creuse fixe l'ordre de "
    "grandeur du phénomène dans sa forme extrême : 150 de ses 255 communes, soit 59 % du "
    "département, appartiennent au cumul, dans un territoire dont 31,4 % de la population a "
    "65 ans ou plus ; à cette échelle, le cumul n'est plus une collection de cas communaux "
    "mais la condition ordinaire du département, et c'est l'échelle départementale "
    "(annexe J) qui devient la maille pertinente de l'intervention."))
E.append(H2("4.6. Généralisation de la méthode"))
E.append(P("La chaîne construite ici ne mobilise rien de spécifique à l'audioprothèse : un "
    "répertoire professionnel géolocalisé, des populations, une structure d'âge, un revenu et "
    "des distances. La même démarche, validation rétrospective comprise dès lors que deux "
    "millésimes existent, s'appliquerait aux orthophonistes, aux pédicures-podologues, aux "
    "opticiens ou aux sages-femmes ; seule la table des critères économiques du score demande "
    "une adaptation par profession. La publication intégrale du code vise explicitement cette "
    "réutilisation. Elle vise aussi la millésimation : le RPPS étant publié quotidiennement "
    "et les sources socio-démographiques annuellement, la chaîne peut être ré-exécutée à "
    "chaque millésime pour un coût marginal, transformant une étude ponctuelle en suivi "
    "longitudinal ; la comparaison 2022-2026 du présent rapport, avec ses précautions "
    "d'appariement, en constitue la première itération et le gabarit. Une réserve de transposition mérite "
    "d'être notée : la validation rétrospective exige que la profession considérée connaisse "
    "une dynamique d'implantation observable sur la période, condition que remplissait "
    "l'audioprothèse post-2021 mieux qu'aucune autre ; pour une profession à effectifs "
    "stables, seuls les volets descriptifs (APL, cumul) se transposent directement."))
E.append(P("Cette généralité rapproche le présent travail des usages établis de l'APL par la "
    "statistique publique : la DREES et l'Irdes l'appliquent aux médecins généralistes et aux "
    "professions de premier recours pour asseoir les zonages d'intervention [2, 3]. Les valeurs "
    "produites ici ne sont pas comparables en niveau à celles de ces travaux, la demande, la "
    "pondération et l'unité d'offre différant ; c'est la structure spatiale des écarts, et non le "
    "niveau, qui se prête à la comparaison, et elle retrouve pour l'audioprothèse les traits "
    "connus des professions étudiées, gradient urbain-rural et décrochage ultramarin, dans des "
    "proportions plus marquées."))
E.append(H2("4.7. Implications pour la profession et pour l'action publique"))
E.append(P("Pour un porteur de projet, indépendant ou enseigne, la lecture opérationnelle des "
    "résultats tient en trois règles. La liste de l'annexe A hiérarchise des communes où "
    "l'absence d'offre coexiste avec une demande démontrable ; les taux d'équipement observés "
    "sur la période (jusqu'à 54,5 % dans le quintile supérieur) indiquent que ces cibles sont "
    "effectivement investissables, et à quel rythme la concurrence les investit. La typologie de la "
    "section 3.6 précise la nature de ces cibles : hors outre-mer, il s'agit le plus "
    "souvent de communes à moins de 15 km d'une offre existante, où le pari n'est pas "
    "l'absence de concurrence à l'horizon mais la captation d'une patientèle âgée et "
    "nombreuse que la distance, même modeste, détourne aujourd'hui de l'appareillage ou "
    "du suivi ; les zones de chalandise véritablement vierges sont l'exception, "
    "ultramarine pour l'essentiel. Enfin, le cas des 64 communes redevenues sans offre "
    "(annexe F) rappelle que l'implantation en périphérie immédiate d'un pôle équipé est la "
    "position la plus fragile du réseau : c'est là que se concentrent les disparitions. Pour les jeunes diplômés enfin, dont "
    "l'orientation vers le salariat d'enseigne est aujourd'hui le débouché dominant, la "
    "liste prioritaire documente l'alternative : des marchés locaux identifiés, quantifiés "
    "et durablement non servis, où une première installation indépendante rencontre les "
    "conditions démographiques de sa viabilité."))
E.append(P("Pour la puissance publique, les résultats délimitent trois niveaux "
    "d'intervention. Le premier est documentaire et ne coûte presque rien : intégrer "
    "l'audioprothèse au suivi standard de l'accessibilité aux soins, ce que la présente "
    "chaîne, automatisée de la collecte au rapport, rend réplicable à chaque millésime. Le "
    "deuxième est incitatif : les 37 villes de l'annexe B et les départements de tête de "
    "l'annexe J fournissent une cible directement utilisable pour des dispositifs analogues "
    "aux zonages conventionnels d'autres professions, dont l'audioprothèse est aujourd'hui "
    "absente. Le troisième est structurel et concerne l'outre-mer : aux distances guyanaises, "
    "l'initiative privée ne peut être l'unique réponse, et les instruments pertinents — "
    "consultations avancées adossées aux centres hospitaliers, équipes mobiles, prise en "
    "charge du transport — relèvent de l'organisation des soins, non du marché."))
E.append(P("Pour la profession enfin, prise collectivement, ces résultats documentent un "
    "argument et une responsabilité. L'argument : la croissance 2022-2026 dément l'image d'un "
    "secteur immobile, et la résorption de 295 manques en quatre ans est à mettre à son "
    "crédit. La responsabilité : ce que le rythme actuel laissera durablement de côté est "
    "désormais connu, commune par commune, et publié ; l'écart entre la carte de 2026 et "
    "celle du prochain millésime dira ce que la profession et les pouvoirs publics auront "
    "fait de cette connaissance."))
E.append(H2("4.8. Limites"))
E.append(P("Huit limites principales sont identifiées, par ordre d'importance décroissante. "
    "Premièrement, les distances à vol d'oiseau entre centroïdes : acceptables dans l'Hexagone, "
    "elles sous-estiment l'isolement réel des communes enclavées, au premier chef en Guyane ; un "
    "distancier multimodal homogène couvrant l'outre-mer serait nécessaire pour lever cette "
    "limite, et n'existe pas à notre connaissance. Deuxièmement, l'unité de compte : l'activité "
    "communale n'est pas un équivalent temps plein, un professionnel multi-sites comptant dans "
    "chacune de ses communes d'exercice ; l'offre est de ce fait surestimée là où le multi-sites "
    "est fréquent, dans une proportion que les données publiques ne permettent pas de chiffrer, "
    "et l'APL en hérite. Troisièmement, l'hétérogénéité de la comparaison temporelle : deux "
    "répertoires (ADELI puis RPPS), deux recensements et deux géographies communales ; la "
    "cohérence inter-répertoires mesurée en section 3.10 autorise une lecture en ordre de "
    "grandeur, non une série homogène. Quatrièmement, les conventions de l'APL (rayon de 30 km, "
    "bandes de pondération) et du score (pondérations, prévalence de 65 %, imputation des "
    "revenus manquants) : leurs effets sont quantifiés en section 3.10 et l'essentiel des "
    "classements y est insensible, mais elles demeurent des choix raisonnés, non des paramètres "
    "estimés. Cinquièmement, l'absence de l'offre itinérante, des permanences et des projets "
    "d'ouverture en cours, invisibles des répertoires. Sixièmement, la rétropolation de la section 3.13, construite sur la fraction appariée "
    "de l'offre 2022 (88 %) : présentée pour cette raison sous forme de bornes, elle n'a "
    "pas, pour 2022, la précision des niveaux 2026. Septièmement, ce rapport est l'œuvre d'un auteur unique et n'avait, au moment de sa diffusion, pas fait l'objet d'une relecture par les pairs ; la publication intégrale du code et des données vise précisément à rendre cette vérification externe possible, et les erreurs qui y seraient trouvées seront corrigées en versions successives. Huitièmement, le caractère statique de la "
    "photographie : l'étude décrit un état daté et un intervalle passé, non une projection."))

# ═══ 5. CONCLUSION ═══
E.append(H1("5. Conclusion"))
E.append(P("Les trois questions posées en introduction reçoivent une réponse. L'accès à "
    "l'audioprothèse manque d'abord outre-mer, où l'écart avec l'Hexagone se mesure en "
    "multiples, et dans un ensemble identifié de communes rurales et de villes moyennes "
    "vieillissantes ; il ne manque pas, en revanche, dans la majorité des communes que le simple "
    "comptage désigne, situées à quelques kilomètres d'une offre réelle. Le score publié en 2022 "
    "a prédit de façon significative la localisation des implantations de la période, ce qui "
    "établit sa validité d'instrument de hiérarchisation ; l'expansion qu'il anticipait s'est "
    "toutefois dirigée vers la taille des bassins, non vers le besoin. Enfin, 2"+NB+"992 communes "
    "cumulent accès faible, population âgée et revenus modestes : c'est la carte de ce que la "
    "solvabilisation ne suffit pas à atteindre. La suite du travail est tracée : substituer des "
    "temps d'accès aux distances, raisonner en équivalents temps plein quand le répertoire le "
    "permettra, intégrer Mayotte dès l'authentification de ses populations, et suivre, millésime "
    "après millésime, si la carte des manques se referme ou se déplace. À cet égard, la période qui s'ouvre "
    "sera le véritable test : la phase d'expansion exceptionnelle documentée ici touche "
    "mécaniquement à sa fin, et c'est en régime de croisière que l'on verra si les "
    "interstices identifiés se comblent, stagnent ou s'élargissent."))

# ═══ RÉFÉRENCES ═══
E.append(H1("Remerciements"))
E.append(P("Ce travail n'existerait pas sans la politique française d'ouverture des données "
    "publiques : que soient remerciés les producteurs des sources mobilisées, l'Agence du "
    "Numérique en Santé pour l'extraction quotidienne du RPPS, l'Insee pour l'ensemble de "
    "l'appareil statistique communal, le ministère de la Transition écologique et l'ANIL pour "
    "la Carte des loyers, ainsi que les contributeurs d'OpenStreetMap et du projet "
    "france-geojson pour les fonds géographiques. Les éventuelles erreurs d'interprétation de "
    "ces sources n'engagent que l'auteur."))
E.append(H1("Disponibilité des données et du code"))
E.append(P("L'intégralité du code de collecte, d'assemblage et d'analyse, les jeux de données "
    "produits (scoring des 34"+NB+"900 communes, liste prioritaire, table de comparaison "
    "2022-2026) et le présent rapport sont publiés en accès ouvert : dépôt "
    "github.com/Nsoussan/deserts-audioprothese ; code archivé sous DOI 10.5281/zenodo.22146816 ; "
    "données sous DOI 10.5281/zenodo.22146965 ; jeu de données référencé sur data.gouv.fr sous "
    "licence ouverte 2.0. Les sources mobilisées sont toutes publiques et citées en "
    "références ; aucune donnée d'accès restreint n'a été utilisée. Citation suggérée : "
    "Soussan N., « L'accessibilité de l'audioprothèse en France », version 2.0, août 2026, "
    "doi"+NB+":"+NB+"10.5281/zenodo.22146893."))
E.append(H1("Déclaration de liens d'intérêts et financement"))
E.append(P("L'auteur est audioprothésiste diplômé d'État en exercice ; l'étude porte donc sur sa "
    "propre profession, ce qui a guidé le choix des critères du score et constitue à la fois une "
    "source d'expertise et un lien d'intérêt qu'il appartient au lecteur d'apprécier. L'étude "
    "n'a bénéficié d'aucun financement et n'a été commanditée par aucun acteur du secteur ; les "
    "choix méthodologiques, les résultats et leur interprétation n'engagent que l'auteur."))
E.append(H1("Références"))
for i, ref in enumerate([
    "Soussan N. Les déserts de l'audioprothèse en France, version 1.0. 2026. Code : doi:10.5281/zenodo.22146816 ; rapport : doi:10.5281/zenodo.22146893 ; données : doi:10.5281/zenodo.22146965.",
    "Barlet M., Coldefy M., Collin C., Lucas-Gabrielli V. L'accessibilité potentielle localisée (APL) : une nouvelle mesure de l'accessibilité aux soins appliquée aux médecins généralistes libéraux en France. Paris : DREES ; 2012. Document de travail, série Études et recherche, n° 124.",
    "Vergier N., Chaput H., avec la collaboration de Lefebvre-Hoang I. Déserts médicaux : comment les définir ? Comment les mesurer ? Paris : DREES ; 2017. Les Dossiers de la DREES, n° 17.",
    "Agence du Numérique en Santé. Annuaire Santé : extraction en libre accès des professionnels intervenant dans le système de santé (RPPS), fichier Personne_activite. Extraction du mois d'août 2026. data.gouv.fr, licence ouverte 2.0.",
    "Insee. Populations de référence 2023, authentifiées par le décret n° 2025-1362 du 26 décembre 2025, en vigueur au 1er janvier 2026.",
    "Insee. Recensement de la population 2022, base « Évolution et structure de la population », géographie au 1er janvier 2025.",
    "Insee. Base du dossier complet, édition du 22 juillet 2026, format harmonisé ; médiane de niveau de vie, millésime 2023.",
    "Ministère de la Transition écologique, ANIL. Carte des loyers : indicateurs de loyers d'annonce par commune. Éditions 2024 et 2022. data.gouv.fr.",
    "Projet france-geojson. Contours des communes françaises, dérivés d'OpenStreetMap et des publications Etalab.",
    "Insee. Base permanente des équipements, millésime 2025 : dénombrement des équipements par commune, format harmonisé ; type d'équipement « audioprothésiste » (exercice libéral).",
], start=1):
    E.append(P(f"[{i}]  {ref}", REF))

# ═══ ANNEXES ═══
TOC_COURTS = {
    "Annexe B": "Annexe B — Les 37 communes du cumul accès-âge-revenus",
    "Annexe F": "Annexe F — Les 64 communes redevenues sans audioprothésiste",
    "Annexe I": "Annexe I — Inventaire des 560 communes sans audioprothésiste",
}
def annexe(titre, intro=None):
    E.append(PageBreak())
    E.append(H1(titre, TOC_COURTS.get(titre[:8])))
    if intro:
        E.append(P(intro))

annexe("Annexe A — Les 173 communes prioritaires",
    "Liste intégrale, classée par score décroissant. « n. d. » : valeur non disponible "
    "(centroïde ou structure d'âge manquants dans les sources). L'ensemble des variables pour "
    "les 34"+NB+"900 communes figure dans le jeu de données publié.")
pa_rows = [["Rang", "Commune", "Code", "Région", "Population", "65 ans et + (%)", "Distance (km)", "APL"]]
for _, r in t_prio.iterrows():
    p65 = "n. d." if pd.isna(r['part_65_plus_pct']) else dc(r['part_65_plus_pct'])
    aplv = "n. d." if pd.isna(r['apl']) else f"{r['apl']:.0f}"
    dst = "n. d." if pd.isna(r['dist_audio_km']) else dc(r['dist_audio_km'])
    pa_rows.append([int(r['rang']), str(r['commune'])[:34], str(r['code_insee']), str(r['reg_c'])[:24],
                    fr(r['population_2023']), p65, dst, aplv])
E.append(tab(pa_rows, [1.0*cm, 4.3*cm, 1.3*cm, 3.3*cm, 1.9*cm, 1.75*cm, 1.6*cm, 1.1*cm],
             fs=7.8, align_right={0,4,5,6,7}))

annexe("Annexe B — Les 37 communes de plus de 5 000 habitants du cumul accès-âge-revenus",
    "Communes appartenant simultanément au tiers inférieur d'APL, au tiers supérieur de part "
    "des 65 ans et plus et au tiers inférieur de revenu médian ; classement par population de 65 "
    "ans et plus décroissante.")
pb_rows = [["Commune", "Région", "Population", "65 ans et + (%)", "Revenu médian (€/UC)", "APL"]]
for _, r in t_dp.iterrows():
    pb_rows.append([str(r['commune']), str(r['reg_c']), fr(r['population_2023']),
                    f"{r['part_65_plus_pct']:.0f}", fr(r['revenu_median_uc']), f"{r['apl']:.0f}"])
E.append(tab(pb_rows, [4.2*cm, 3.5*cm, 2.0*cm, 2.0*cm, 2.5*cm, 1.2*cm], fs=8.2,
             align_right={2,3,4,5}))

annexe("Annexe C — Analyse de sensibilité des pondérations",
    "Recouvrement de la liste prioritaire après perturbation de chaque poids de ±20 % puis "
    "retrait complet du critère, toutes choses égales par ailleurs. Le tableau reproduit les "
    "trente variations de la première passe de calcul (base des communes à centroïde "
    "renseigné) ; les valeurs de synthèse de la section 3.10 (médiane de 99,4 % ; minimum de "
    "84,4 %) proviennent du recalcul final sur la liste complète et confirment les mêmes ordres "
    "de grandeur.")
pc_rows = [["Variation", "Recouvrement (%)"]]
for _, r in t_sens.iterrows():
    pc_rows.append([str(r['variation']), dc(r['recouvrement %'])])
E.append(tab(pc_rows, [7.6*cm, 4.0*cm], fs=8.4, align_right={1}))

annexe("Annexe D — Dictionnaire des variables du jeu de données publié")
pdct_rows = [["Variable", "Définition", "Source, millésime"]]
for var, definition, src in [
    ("code_insee", "Code officiel géographique de la commune (cinq caractères)", "Insee, COG 2025"),
    ("commune", "Libellé de la commune", "Insee, COG"),
    ("region", "Code et libellé de la région", "Insee, COG"),
    ("population_2023", "Population municipale", "Populations de référence 2023 [5]"),
    ("part_65_plus_pct", "Part des 65 ans et plus, effectifs exacts hommes et femmes", "RP 2022 [6]"),
    ("revenu_median_uc", "Médiane de niveau de vie par unité de consommation (euros) ; valeurs manquantes imputées à 25 000", "Dossier complet, millésime 2023 [7]"),
    ("loyer_m2", "Loyer d'annonce prédit au m², appartements du parc privé", "Carte des loyers 2024, complétée 2022 [8]"),
    ("nb_audioprothesistes_2026", "Activités d'audioprothésistes (couples professionnel × commune)", "RPPS, extraction août 2026 [4]"),
    ("nb_orl_liberaux_2026", "Activités d'ORL en exercice libéral", "RPPS, extraction août 2026 [4]"),
    ("dist_audio_km", "Distance orthodromique au centroïde de la plus proche commune équipée (km) ; nulle si la commune est équipée", "calcul ; fonds [9]"),
    ("apl", "Accessibilité potentielle localisée, professionnels pour 100 000 habitants de 65 ans et plus", "calcul (section 2.3)"),
    ("score_v2", "Score d'opportunité d'implantation (section 2.4)", "calcul"),
    ("sans_audio_5k", "Population d'au moins 5 000 habitants et aucune activité", "calcul"),
    ("prioritaire_v2", "Commune prioritaire (section 2.5)", "calcul"),
]:
    pdct_rows.append([var, definition, src])
E.append(tab(pdct_rows, [4.1*cm, 7.7*cm, 4.2*cm], fs=8.2))

annexe("Annexe E — Indicateurs par département",
    "APL moyenne pondérée par la population de 65 ans et plus, communes de plus de 5"+NB+"000 "
    "habitants sans audioprothésiste, communes prioritaires et activités recensées, pour les 100 "
    "départements du champ.")
pe_rows = [["Département", "APL pondérée", "≥ 5 000 hab. sans audioprothésiste", "Prioritaires", "Activités"]]
for _, r in t_dep.iterrows():
    pe_rows.append([str(r['dep']), f"{r['apl_pond']:.0f}", fr(r['sans5k']), fr(r['prio']), fr(r['activites'])])
E.append(tab(pe_rows, [2.7*cm, 2.5*cm, 3.6*cm, 2.3*cm, 2.1*cm], fs=7.8, align_right={1,2,3,4}))

annexe("Annexe F — Les 64 communes redevenues ou devenues sans audioprothésiste",
    "Communes de plus de 5"+NB+"000 habitants comptant au moins une activité en 2022 et aucune en "
    "2026, ou ayant franchi le seuil de population entre les deux millésimes ; classement par "
    "population décroissante.")
pf_rows = [["Commune", "Région", "Population", "Distance (km)"]]
for _, r in t_n64.iterrows():
    pf_rows.append([str(r['commune']), str(r['reg_c']), fr(r['population_2023']),
                    dc(r['dist_audio_km'])])
E.append(tab(pf_rows, [5.0*cm, 4.2*cm, 2.3*cm, 2.0*cm], fs=8.0, align_right={2,3}))

annexe("Annexe G — Les 295 communes équipées entre 2022 et 2026",
    "Communes de plus de 5"+NB+"000 habitants sans activité en 2022 et en comptant au moins une en "
    "2026 ; classement par population décroissante.")
pg_rows = [["Commune", "Région", "Population", "Activités 2026"]]
for _, r in t_e295.iterrows():
    pg_rows.append([str(r['commune']), str(r['reg_c']), fr(r['population_2023']),
                    int(r['nb_audioprothesistes_2026'])])
E.append(tab(pg_rows, [5.0*cm, 4.2*cm, 2.3*cm, 2.2*cm], fs=7.8, align_right={2,3}))

annexe("Annexe H — Les 88 communes d'accessibilité nulle",
    "Communes dont aucun professionnel n'est accessible à moins de 30 km du centroïde "
    "(APL"+NB+"="+NB+"0) ; classement par population décroissante.")
ph_rows = [["Commune", "Région", "Population", "dont 65 ans et +", "Distance (km)"]]
for _, r in t_z88.iterrows():
    ph_rows.append([str(r['commune']) if pd.notna(r['commune']) else "(commune nouvelle, code seul)",
                    str(r['reg_c']), fr(r['population_2023']), fr(r['pop65']),
                    dc(r['dist_audio_km']) if pd.notna(r['dist_audio_km']) else "n. d."])
E.append(tab(ph_rows, [4.6*cm, 3.6*cm, 2.1*cm, 2.2*cm, 2.0*cm], fs=8.0, align_right={2,3,4}))

annexe("Annexe I — Inventaire des 560 communes de plus de 5 000 habitants sans audioprothésiste",
    "Inventaire exhaustif au 30 août 2026, classé par région puis population décroissante. La "
    "colonne « Prioritaire » renvoie au classement de l'annexe A ; les 173 communes prioritaires "
    "sont un sous-ensemble du présent inventaire.")
pi_rows = [["Commune", "Code", "Région", "Population", "65 ans et + (%)", "Distance (km)", "APL", "Prioritaire"]]
for _, r in t_s560.iterrows():
    p65 = "n. d." if pd.isna(r['part_65_plus_pct']) else dc(r['part_65_plus_pct'])
    aplv = "n. d." if pd.isna(r['apl']) else f"{r['apl']:.0f}"
    dst = "n. d." if pd.isna(r['dist_audio_km']) else dc(r['dist_audio_km'])
    nom = str(r['commune']) if pd.notna(r['commune']) else "(commune nouvelle, code seul)"
    pi_rows.append([nom[:34], str(r['code_insee']), str(r['reg_c'])[:22],
                    fr(r['population_2023']), p65, dst, aplv,
                    "oui" if r['prioritaire_v2'] else "—"])
E.append(tab(pi_rows, [4.15*cm, 1.3*cm, 2.9*cm, 1.85*cm, 1.75*cm, 1.6*cm, 1.1*cm, 1.6*cm],
             fs=7.6, align_right={3,4,5,6}))

annexe("Annexe J — Le cumul accès-âge-revenus agrégé par département",
    "Nombre de communes du cumul défini en section 3.9, population totale et population de 65 "
    "ans et plus concernées, par département ; classement par nombre de communes décroissant. "
    "Seuls figurent les départements comptant au moins une commune concernée.")
pj_rows = [["Département", "Communes", "Population", "dont 65 ans et +"]]
for _, r in t_dpd.iterrows():
    pj_rows.append([str(r['dep']), fr(r['nb']), fr(r['pop']), fr(r['pop65'])])
E.append(tab(pj_rows, [3.0*cm, 2.6*cm, 3.2*cm, 3.2*cm], fs=8.0, align_right={1,2,3}))

annexe("Annexe K — Évolutions méthodologiques entre les versions 1 et 2",
    "Synthèse des changements de sources et de méthode entre la version publiée sur données "
    "2022 et la présente version ; chaque changement est motivé dans le corps du rapport, à la "
    "section indiquée.")
pk_rows = [["Objet", "Version 1 (2022)", "Version 2 (2026)", "Section"],
    ["Répertoire professionnel", "ADELI, millésime 2022", "RPPS, extraction quotidienne (août 2026), dédoublonnage identifiant × commune", "2.1"],
    ["Populations", "RP 2021", "Populations de référence 2023 (en vigueur 01/01/2026)", "2.1"],
    ["Part des 65 ans et plus", "Estimation par tranches quinquennales", "Effectifs exacts par sexe, RP 2022", "2.1"],
    ["Revenus", "Filosofi 2019", "Millésime 2023 (dossier complet ; le millésime 2022 n'a jamais été produit)", "2.1"],
    ["Loyers", "Carte des loyers 2022", "Édition 2024, complétée 2022", "2.1"],
    ["Critère de distance", "absent", "Distance au plus proche professionnel, plafonnée à 30 km (poids 12)", "2.4"],
    ["Critère de densité", "présent (poids 5)", "retiré (superficie non fiable en géographie 2025 ; information redondante)", "2.4"],
    ["Seuil prioritaire", "Top 15 % du score, ensemble des communes", "Top 15 % du score, strate des communes de 5 000 habitants et plus", "2.5"],
    ["Indicateur d'accès", "absent", "APL (2SFCA), demande 65 ans et plus, bandes 0-10/10-20/20-30 km", "2.3"],
    ["Validation", "absente", "Rétrospective 2022-2026 ; sensibilité systématique ; croisement BPE", "2.6-2.8"],
    ["Champ", "France entière (COG 2021)", "France hors Mayotte (COG 2025 ; recensement mahorais reporté)", "2.1"],
]
E.append(tab(pk_rows, [3.1*cm, 4.1*cm, 6.5*cm, 1.4*cm], fs=8.0))

doc.multiBuild(E)

# Remap des références Helvetica (police par défaut du canvas, jamais dessinée)
# vers la sérif embarquée, pour un PDF 100 % polices embarquées sans tag orphelin.
import pikepdf
with pikepdf.open("/home/claude/rapport_v2_sci.pdf", allow_overwriting_input=True) as pdf:
    for page in pdf.pages:
        fonts = page.get("/Resources", {}).get("/Font", None)
        if fonts is None:
            continue
        target = None
        for k in fonts.keys():
            bf = str(fonts[k].get("/BaseFont", ""))
            if "LiberationSerif" in bf and "Bold" not in bf and "Italic" not in bf:
                target = fonts[k]
                break
        if target is None:
            for k in fonts.keys():
                if "LiberationSerif" in str(fonts[k].get("/BaseFont", "")):
                    target = fonts[k]
                    break
        if target is None:
            continue
        for k in [k for k in fonts.keys() if "Helvetica" in str(fonts[k].get("/BaseFont", ""))]:
            fonts[k] = target
    pdf.save("/home/claude/rapport_v2_sci.pdf")
print("Rapport scientifique construit")
