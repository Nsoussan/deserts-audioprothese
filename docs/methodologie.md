# Méthodologie

## 1. Périmètre

L'analyse couvre les **34 965 communes** françaises (métropole et départements d'outre-mer) du Code officiel géographique INSEE, **millésime 2021**. Ce millésime est nommé explicitement car le nombre de communes varie chaque année au gré des fusions.

## 2. Variables et construction

Dix variables entrent dans le score. Chacune est normalisée en score 0–1000 par min-max sur l'ensemble des communes :

`n(x) = (x - min) / (max - min) × 1000`, inversé (`1000 - n`) lorsque la valeur faible traduit une opportunité.

Deux variables sont dérivées :

- **Population concernée** = population × part des 65 ans et plus × 65 %. Le taux de 65 % correspond à un ordre de grandeur de la prévalence des troubles auditifs chez les 65 ans et plus ; c'est une hypothèse simplificatrice, discutée dans `limites.md`.
- **Taux d'équipement local** = nombre d'audioprothésistes / (population concernée / 100). Mesure la saturation réelle du marché, indépendamment de la population totale.
- **Potentiel 100 % Santé** = (25 000 − revenu médian) / 15 000 × 100, borné à [0, 100]. Proxy de la part de population susceptible de relever du panier sans reste à charge, croissante quand le revenu diminue.

**Imputation des valeurs manquantes.** Les revenus médians manquants (petites communes sous secret statistique) sont imputés à 25 000 €, ordre de grandeur de la médiane nationale. Ce choix est testé en sensibilité (voir `limites.md`). Les effectifs professionnels manquants sont traités comme zéro. Le ratio habitants/audioprothésiste est écrêté à 50 000 pour limiter le poids des valeurs extrêmes.

## 3. Pondérations et justification

Le score final est la somme pondérée des dix scores normalisés (73 points de pondération). Les poids traduisent une hiérarchie assumée entre trois familles de critères : la concurrence (14 + 10 + 9 + 5 = 38 pts), la demande (10 + 3 = 13 pts) et la solvabilité (8 + 7 + 2 = 17 pts), plus l'écosystème de prescription (5 pts).

| Critère | Poids | Justification |
|---|---|---|
| Nb audioprothésistes (inversé) | 14 | Critère principal : l'absence de concurrence directe est la condition première d'une implantation. Poids le plus élevé du modèle. |
| Part des 65 ans et plus | 10 | La prévalence des troubles auditifs croît fortement avec l'âge ; la structure d'âge prédit mieux la demande que la population brute. |
| Taux d'équipement local (inversé) | 10 | Complète le critère précédent : distingue une commune sans professionnel mais au marché minuscule d'une commune réellement sous-équipée. |
| Habitants par audioprothésiste | 9 | Intensité du sous-équipement là où des professionnels existent déjà. |
| Revenu médian | 8 | Capacité de financement du reste à charge (équipements de classe II). |
| Potentiel 100 % Santé | 7 | Depuis 2021, le panier sans reste à charge solvabilise les revenus modestes : un revenu faible n'exclut plus la demande, il en change la composition. |
| Densité (inversé) | 5 | À population donnée, une densité faible signale un bassin captif plus large autour de la commune. |
| ORL libéraux | 5 | Prescripteurs et partenaires de parcours de soins. Poids modéré : la primo-prescription peut aussi venir du généraliste. |
| Population | 3 | Taille absolue du marché ; poids faible car largement redondante avec les critères précédents. |
| Loyer au m² | 2 | Signal indirect du coût d'exploitation. Poids minimal : donnée partielle et ambivalente (un loyer élevé signale aussi une zone commerçante active). |

**Ces pondérations comportent une part normative.** Elles ne résultent pas d'une estimation économétrique mais d'une hiérarchisation raisonnée, informée par la pratique du secteur. L'analyse de sensibilité (section 5) montre que les résultats principaux sont robustes à des variations modérées des poids.

## 4. Définition des communes prioritaires

Une commune est classée **prioritaire** si elle satisfait trois conditions cumulatives :

1. population ≥ 5 000 habitants ;
2. aucun audioprothésiste installé ;
3. score dans le **top 15 %** national (≥ 85e percentile).

Sur ce critère : **742 communes** de plus de 5 000 habitants n'ont aucun audioprothésiste, dont **331 prioritaires**.

Le seuil de 5 000 habitants correspond à un ordre de grandeur en deçà duquel une implantation dédiée est rarement viable en propre (des solutions itinérantes ou mutualisées relevant d'un autre modèle). Le seuil du top 15 % est un choix de sélectivité, pas un seuil de viabilité démontré.

## 5. Sensibilité

Deux tests documentés :

- **Imputation des revenus** : imputer à la médiane observée plutôt qu'à 25 000 € donne 322 communes prioritaires au lieu de 331 (écart de 2,7 %). Les 300 premières communes du classement sont inchangées à plus de 95 %.
- **Pondérations** : une variation de ±20 % sur chacun des trois poids principaux (14, 10, 10) modifie la composition du top 331 de moins de 8 %.

## 6. Ce que le score n'est pas

Le score ordonne des opportunités relatives ; il ne constitue ni une prévision de chiffre d'affaires, ni une garantie de viabilité, ni une recommandation d'investissement. Toute décision d'implantation suppose une étude de terrain (bassin de vie réel, locaux, concurrence des communes limitrophes) que le modèle ne remplace pas.
