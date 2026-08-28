# Limites

Ce document liste ce que le modèle ne dit pas, les biais connus des sources, et les hypothèses fragiles. Il fait partie intégrante du travail.

## 1. La maille communale ignore les bassins de vie

C'est la limite principale. Une commune sans audioprothésiste peut être à dix minutes d'un centre installé dans la commune voisine : elle apparaîtra comme un « désert » alors que l'accès réel y est correct. Symétriquement, le modèle ne capte pas les zones où un unique centre dessert un bassin très étendu.

Un raffinement naturel serait de raisonner en temps d'accès au professionnel le plus proche (isochrones) ou par bassin de vie INSEE. Ce n'est pas fait dans cette version : les 331 communes prioritaires doivent donc se lire comme des **candidates à vérifier**, pas comme des zones blanches certifiées.

## 2. Millésimes hétérogènes et données professionnelles pré-RPPS

Les effectifs d'audioprothésistes et d'ORL datent de **2022**, avant la bascule des audioprothésistes dans le répertoire RPPS (juin 2024). Le secteur ayant connu une croissance rapide du nombre de centres depuis, certaines communes identifiées sans professionnel en 2022 ont pu être équipées depuis. Les données démographiques (2021) et de revenus ont leurs propres millésimes. Le score mélange donc des photographies prises à des dates légèrement différentes.

Une mise à jour sur données RPPS post-2024 est l'amélioration prioritaire de ce travail.

## 3. La prévalence à 65 % est un ordre de grandeur

La « population concernée » repose sur l'hypothèse que 65 % des 65 ans et plus présentent un trouble auditif. La littérature donne des fourchettes variables selon la définition retenue (perte mesurée vs gêne déclarée, seuils audiométriques). Ce paramètre affecte le taux d'équipement local mais pas le classement relatif des communes entre elles, la même hypothèse s'appliquant partout.

## 4. Les pondérations sont en partie normatives

Les poids ne sont pas estimés économétriquement : ils traduisent une hiérarchisation raisonnée (voir `methodologie.md`, §3). L'analyse de sensibilité montre une robustesse correcte à des variations modérées, mais un jeu de poids différent, tout aussi défendable, produirait un classement partiellement différent.

## 5. Imputations

Les revenus manquants (secret statistique des petites communes) sont imputés à 25 000 € ; l'imputation à la médiane observée donne 322 communes prioritaires au lieu de 331. Les effectifs professionnels manquants sont traités comme zéro, ce qui peut confondre « absence de professionnel » et « absence de donnée ».

## 6. Ce que le modèle ne mesure pas

- La concurrence des enseignes d'optique-audio et des corners, mal captée par les répertoires professionnels.
- La qualité de l'emplacement (visibilité, stationnement, flux) qui conditionne la réussite réelle d'un centre.
- Les dynamiques démographiques : le score est une photographie, pas une projection.
- L'offre itinérante et les permanences, qui desservent certaines zones sans y être domiciliées.

## 7. Risque de ré-identification

Le jeu publié est agrégé à la commune, sans nom ni adresse. Dans les communes à effectif de 1, le comptage peut indirectement désigner un professionnel dont l'installation est par ailleurs publique (annuaires professionnels). Aucune information au-delà de ce comptage public n'est diffusée.
