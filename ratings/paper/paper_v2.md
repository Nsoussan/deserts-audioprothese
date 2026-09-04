---
title: "Ratings Without Exit: Online Reputation and the Option to Switch in a Credence Goods Market"
subtitle: "Evidence from hearing-aid centres in France"
author: "Nathan Soussan"
date: "Working paper · version 2.3 · 4 September 2026 · doi:10.5281/zenodo.22286005"
abstract: |
  In the French hearing-aid market, online rating activity and the spread of ratings across providers follow the number of alternatives a patient has within 10 km; the level of ratings does not. Public rating systems discipline expert sellers in credence goods markets through the choices of prospective consumers, a mechanism that presupposes that alternatives exist and that laboratory evidence establishes in markets of four experts. This paper observes a rating system across the full range of the choice set. I rebuild the population of 8,421 hearing-aid centres in France from the public register of health professionals, count the competing centres within 10 km of each, and collect Google ratings through the official API for a stratified sample of 2,999 centres that includes every centre with fewer than three competitors, together with the content of 2,706 provider websites and, as a benchmark, the ratings of 2,574 hairdressers in 879 of the same communes. The median centre with no competitor within 10 km has 9 reviews and the median centre with ten or more has 34, a gradient that survives controls for commune population, income and demand per centre and is twice as steep as the hairdressers'. Rating levels sit near the ceiling everywhere, as they do for hairdressers. Among the quarter of centres with the most reviews within each competition band, the standard deviation of ratings across centres is 0.14 to 0.15 where a centre has two or fewer competitors and 0.25 to 0.30 where it has three or more, a difference that survives a fixed window of review counts and a bootstrap by commune; hairdressers in the same communes show no comparable compression. Where the choice set is thin, established centres are rated both higher and more alike, in part because they sit closer to the top of the scale. Owner-operated centres, those whose practitioner is registered as the practice holder, collect 31% fewer reviews than centres with salaried practitioners, conditional on competition and organisational form, and price information on provider websites is set nationally by the chains, is twice as frequent among independents with three or more competitors as among those with two or fewer, a difference the sample does not estimate precisely, and is unrelated to ratings. The results are descriptive.
geometry: margin=2.6cm
papersize: a4
fontsize: 11pt
mainfont: "TeX Gyre Pagella"
linestretch: 1.15
numbersections: true
subject: "Working paper, version 2.3, doi:10.5281/zenodo.22286005"
keywords: [credence goods, rating systems, reputation, competition, healthcare, hearing aids]
header-includes:
  - \usepackage{etoolbox}
  - \AtBeginEnvironment{longtable}{\small}
  - \widowpenalty=10000
  - \clubpenalty=10000
---

*Keywords:* credence goods, rating systems, reputation, competition, healthcare, hearing aids. *JEL:* D82, I11, L15, D83.

*Author:* state-registered *audioprothésiste*; student, Université Paris-Panthéon-Assas. nsoussan0@gmail.com. Comments welcome. Conflict-of-interest statement in the Declarations.

# Introduction

In a credence goods market the seller knows what the buyer needs and the buyer cannot verify, even after the fact, whether what was sold was what was needed (Darby and Karni, 1973; Dulleck and Kerschbamer, 2006). Healthcare is the canonical case. Angerer, Glätzle-Rützler, Mimra, Rittmannsberger and Waibel (2026) show in the laboratory that a public rating system on a zero-to-five scale reduces the problem sharply: in markets of four experts and four consumers, ratings cut undertreatment from 52% to 7% of interactions and overcharging from 86% to 44%. The mechanism is reputation through choice. Consumers rate the outcomes they can observe, and in the next period they tend to visit the best-rated expert. An expert who cannot lose a consumer has little to fear from a rating beyond the consumer's outside option.

The experiment holds fixed what field markets vary: the choice set. Every consumer in every period picks from a list of four experts, and the authors note that their design maintains competition throughout. This paper takes the choice set as the variable of interest. In Hirschman's (1970) terms, a rating is voice, and its disciplining power in these models comes from the exit it enables, or more precisely from the selection it allows the next consumer to make. Where the nearest other provider is a long drive away, voice has little exit to lean on. The title is a shorthand: the choice set observed here is thin rather than empty, since the centre without a competitor within 10 km has its nearest competitor 13.6 km away at the median (Section 3.1). The question is what a public rating system then looks like: whether consumers still rate, whether ratings still differ across providers, and whether providers still respond.

The market is hearing-aid provision in France, a credence good in the strict sense: the practitioner, the *audioprothésiste*, assesses the hearing loss, selects and programmes the device, sells it and adjusts it over years, and the patient, typically elderly, cannot tell whether a different device, a different setting or no device would have served as well. It is also a market with a documented geography. A companion study (Soussan, 2026) measures accessibility for all 34,900 French communes and finds 560 towns of more than 5,000 inhabitants without a practitioner, alongside cities where dozens of centres compete within a few kilometres. The choice set that the laboratory fixes at four here runs from zero to more than fifty within 10 km.

I rebuild the population of hearing-aid centres from the public extraction of the national register of health professionals: 8,421 retail sites, each attached to the accessibility measures of the companion study and to the number of other centres within 10 km. For a stratified sample of 2,999 sites that includes every site with fewer than three competitors, I collect through the official Google Places API the rating, the number of reviews, the website and the business status of the matching listing; I read and code the content of 2,706 provider websites; and, to hold the place, the platform and the population of reviewers constant, I collect the ratings of 2,574 hairdressers in 879 of the same communes.

The main results are as follows. Rating activity follows the choice set. The median centre with no competitor within 10 km has 9 reviews and 87.5% of such centres are rated at all; with ten or more competitors, the median is 34 and 94.8% are rated. The gradient survives controls for commune population, income, older population per centre and staff, with standard errors clustered by commune, and it is twice as steep as the one hairdressers display in the same communes. The rating of the typical centre does not follow the choice set, and this is not specific to the credence good: hearing-aid centres average 4.77 stars and hairdressers 4.74, and neither level varies with the local choice set. What competition changes is the variation of ratings across providers. Among the quarter of centres with the most reviews within each competition band, the standard deviation of ratings across centres is 0.14 to 0.15 where a centre has two or fewer competitors and 0.25 to 0.30 where it has three or more; the difference holds within a fixed window of review counts, with or without the optician corners, and under a bootstrap by commune, and it appears only among centres with twenty or more reviews, where the noise of the mean is small; part of it is the bounded scale, since the top quarter of the thin bands sits closer to the maximum. Two things go with it. Established centres in thin markets are rated higher, not lower: weighting ratings by the number of reviews a patient reads gives 4.87 where a centre has no competitor and 4.60 where it has ten or more. And the low tail is thinner where the choice set is thin, five of the 236 most-reviewed centres with two or fewer competitors being rated below 4.5 against 56 of the 459 with three or more, a contrast that the review count and the composition of the top quarter account for once they are held constant (Section 5.4). Hairdressers in the same communes show a spread of 0.21 to 0.25 and a low tail of one salon in ten at every level of competition.

On the supply side, a centre whose practitioner is registered in the register as the practice holder (*titulaire de cabinet*, hereafter an owner-operated centre) collects 31% fewer reviews than a centre staffed by salaried practitioners, conditional on local competition and organisational form, and the gap does not vary with competition; the differences between chains and independents that appear in raw comparisons largely reduce to this. And the information that providers put on their own websites, price information in particular, is set nationally by the chains; among independents it is twice as frequent where the centre has three or more competitors, an imprecise difference, and it is unrelated to ratings.

The paper is descriptive. The number of competitors within 10 km is not exogenous; it is largely a measure of urban density, and the hairdresser benchmark controls for the place but not for the patient. Reviews are self-selected and, in chains, solicited. A rating measures reported satisfaction, not the appropriateness of the treatment, which no observational dataset in this market contains. Section 7 lists these limits. What the paper offers is a field counterpart of a laboratory result: the variable the experiment held constant is the one along which, in the market, the activity of the rating system and its variation across providers move.

The paper relates to three strands of work. It follows the literature on institutions that mitigate expert opportunism in credence goods markets, from Dulleck and Kerschbamer (2006) and Dulleck, Kerschbamer and Sutter (2011) to the review by Balafoutas and Kerschbamer (2020), and in particular the result of Mimra, Rasch and Waibel (2016) that price competition undermines reputation building, which bears on a market where one class of devices is price-capped and the other is not (Section 2). It relates to the evidence that online ratings drift towards the top of the scale on many platforms (Nosko and Tadelis, 2015; Filippas, Horton and Golden, 2022), one reason to compare the credence good with an experience good rated on the same platform. It adds to the small field literature on online ratings in expert markets: Kerschbamer, Neururer and Sutter (2023) find in a field experiment on computer repair that better-rated shops charge lower prices, while systematic reviews find at best a weak relationship between physician ratings and clinical outcomes (Hong et al., 2019; Saifee et al., 2020). And it builds on Gottschalk, Mimra and Waibel (2020), who sent a test patient to 180 Zurich dentists and found that unnecessary treatment recommendations were unrelated to the density of dentists but related to a dentist's spare capacity, to the patient's socio-economic status, and, by about sixteen points, to whether the dentist displayed the legally required price information. Their density variable ranged from zero to sixty competitors within 500 metres; the present data extend the range to markets where the nearest competitor is tens of kilometres away.

# The market

Hearing aids in France are dispensed by *audioprothésistes*, a regulated profession that requires a state diploma. A medical prescription is required for a first fitting, from an ear, nose and throat specialist or a general practitioner with otological training; renewals, after four years, may be prescribed by any physician (Assurance Maladie, 2026). In the taxonomy of Dulleck and Kerschbamer (2006), the prescription verifies the need for a device, not the choice of device, its price or its programming, which remain the practitioner's; the credence-good problem concerns these.

Since 2019, devices have been divided into two classes. Class I devices are price-capped at 950 euros per ear for adults and, since 2021, are covered in full by the combination of statutory insurance and a complementary contract of the regulated *responsable* type or the means-tested public complementary cover, so that patients with such cover pay nothing; the statutory insurer alone pays 240 euros. Class II devices are freely priced and reimbursed on the same statutory base of 400 euros, of which 60% is paid by the statutory insurer (more for exempted patients), the rest falling on complementary insurance, whose reimbursement of class II devices is capped under *responsable* contracts, and on the patient. All listed devices, in both classes, carry a four-year guarantee. Every sale must be preceded by a standardised quote that separates the device from the fitting services and presents a class I offer alongside any class II device, and by a free trial period of at least thirty days (Assurance Maladie, 2026; Institut national de la consommation, 2026). The class I cap removes price competition on that segment, the condition under which Mimra, Rasch and Waibel (2016) find that reputation can be built; class II leaves it open. The data do not separate the two segments. The reform changed the supply side: the companion study counts 6,682 registered activities in 2022 and 11,018 in August 2026, a figure it treats as an upper bound on real growth because the two vintages come from different registers and count activities rather than practitioners, but whose direction is not in doubt.

The profession has no professional council (no *ordre*), and advertising is permitted within the limits set for medical devices; the largest chains advertise on television. Supply is organised in five ways, and the register provides a proxy for the distinction. National chains such as Amplifon, Audika and Audition Santé operate integrated networks (integrated chains, in the tables) in which the practitioner is a salaried employee: 6% or fewer of their sites have a practitioner registered as practice holder (*titulaire de cabinet*, the register's role for a practitioner exercising on his own account, hereafter the owner-practitioner). A second group of brands, among them Audition Conseil, Entendre, Sonance and Audio 2000, consists of networks of independent owners trading under a common name (brand networks): between roughly half and three quarters of their sites have an owner-practitioner. Audilab (272 sites), owned since 2019 by the Demant group, which also owns Audika (Autorité de la concurrence, 2019), associates its practitioners with the capital of local companies; 49% of its sites have an owner-practitioner and the classification rule places it among brand networks, a borderline case noted in Section 7. A third group consists of hearing-aid corners inside optician shops (optician corners: Optical Center, Krys, Alain Afflelou, Atol and others; Table A5), whose Google listing is usually the shop's; the group is heterogeneous, from salaried corners inside the shop to franchised centres with a listing of their own. Mutualist networks (the Écouter Voir brand, operated by VYV3 and regional mutualist unions) employ salaried practitioners. The rest are unbranded independents, two thirds of them owner-operated. The distinction matters for the reputation mechanism in two ways. Integrated chains run centralised marketing, which in the author's experience within one of them includes the solicitation of Google reviews after the fitting, a practice the data do not observe; and the owner-practitioner is the residual claimant of the sale, the position that Gottschalk, Mimra and Waibel (2020) found, at the 10% level, to go with more overtreatment.

The companion study describes the geography. It computes, for every commune, a two-step floating catchment measure of potential accessibility with demand restricted to residents aged 65 and over and distance bands of 10, 20 and 30 km, and finds that most of the 560 unserved towns lie within a few kilometres of a served one, while a residual set of communes, overseas and in rural areas with old and poor populations, has no practitioner within reach. This paper uses a finer measure: for a given centre, the number of other centres a patient could reach within 10 km.

# Data

## The site layer

The public extraction of the RPPS (*Répertoire partagé des professionnels intervenant dans le système de santé*, Agence du Numérique en Santé, August 2026 vintage, 2.28 million activity rows) lists each practitioner's activities with the identifier, legal name, trade name, address and sector of the site, and the practitioner's mode of practice. Filtering on the profession code (12,893 activity rows for 7,366 practitioners at 8,508 structures; the companion study's 11,018 activities count practitioner-commune pairs) and keeping the structures that carry a commune code yields 8,481 sites at which at least one *audioprothésiste* is registered; 60 of them are hospitals, dental centres and institutes where *audioprothésistes* are employed but no retail activity takes place, leaving 8,421 retail sites. Each site carries the number of registered practitioners (1.3 on average), whether at least one of them is registered in the role of practice holder (the owner flag; the register records roles and modes of practice, not the ownership of companies), and a classification into the five organisational forms of Section 2. The classification applies a list of keyword rules to the trade name and the legal name (SOGECA for Audika, Sonova for Audition Santé), published with the code; the trade name is declarative and often missing, so that members of networks who did not declare it are counted as unbranded independents, which understates the networks, and the manual check of Section 3.3 found three optician corners and one franchised centre among the independents it drew. A brand is counted as a network of independents when at least 45% of its sites have an owner-practitioner, a threshold that falls in a gap of the distribution of that share across brands (28% to 49%; Table A5). Sites are located at the centroid of their commune, using the coordinates of the companion study; the arrondissements of Paris, Lyon and Marseille, which that study had left without coordinates, are attached to the city centroid for the competition measures and to their own centroids for the accessibility index and the population within 10 km. All three cities lie in the ten-or-more band under either convention; recomputing the competition measures with the arrondissement centroids moves 22 of the 8,421 sites, 8 of them in the sample, down one band.

Each site inherits its commune's population (2023), share of residents aged 65 and over (2022 census), median income per consumption unit (2023, missing for the arrondissements of the three cities and for the overseas departments, 152 sampled sites, where it is imputed at 25,000 euros with an indicator) and accessibility index, and receives the competition measures: the number of other retail sites within 10 km of great-circle distance between centroids, the distance to the nearest other site, the number of distinct alternatives within 10 km (a brand's several sites counting once), and the population aged 65 and over within 10 km divided by the number of sites there, a measure of demand per centre. The 10 km radius is the one that discriminates: within 30 km, 97% of retail sites have ten or more competitors, whereas within 10 km 291 retail sites have none, 754 have one or two, 1,903 have three to nine and 5,473 have ten or more. Among the 291 centres without a competitor within 10 km, the nearest other centre is 13.6 km away at the median and 20.7 km at the ninetieth percentile; 35 have none within 20 km and 5 none within 30 km. "Without exit" therefore describes a thin choice set, not an empty one. Counting distinct alternatives rather than sites moves 58 matched sites across bands and changes no coefficient by more than 0.02 (Table A1); counting Audika and Audilab, two brands of the same group, as one alternative moves 23 more and changes nothing either. Figure 1 maps the four groups.

![Hearing-aid centres in mainland France by local competition, August 2026. Sites at commune centroids; grey dots are the 34,900 communes. Overseas departments (78 sites) are not shown; the legend counts are national. Source: RPPS public extraction, August 2026.](fig0_map.png)

## Sample and weights

The sample takes every retail site with zero to two competitors within 10 km (1,045 sites) and a random draw, proportional by organisational form, from the two other bands, for a total of 2,999 sites. Sampling weights, equal to 1 in the exhaustive strata and about 3.8 in the others, restore national proportions in every table and figure. Table A3 gives the design. The draw was made without a recorded seed and cannot be re-run; the drawn sites, their stratum and weight are recorded in the published site layer, which fixes the sample for replication, and a published script checks that sample against the design.

## Google ratings

Ratings were collected on 3 September 2026 through the Google Places API (New), in two calls per site: a text search on the site's name and address, biased towards the commune centroid and returning only a place identifier, then a place-details call returning the display name, address, coordinates, rating, number of reviews, website, business status and place type. A match was accepted when the returned location lay within 10 km of the commune centroid, the place type was compatible with a retail centre and at least one word of more than three letters of the register name appeared in the listing name, and 225 doubtful matches were re-queried with the brand name followed by *audioprothésiste* and the commune. In the end 2,966 sites (98.9%) had a validated match, in 1,782 communes; 2,768 of the matched sites (93.3%) carried at least one review, and 31 (1.0%) were flagged by Google as closed, with no relation to competition; they are kept. The 33 unmatched sites are more frequent where there is no competitor (11 of 291, against 12 of 1,450 with ten or more); they are treated as missing in the main tables and as unrated in a robustness check that slightly strengthens the activity gradient (Table A1). The 2,966 matches point to 2,880 distinct listings: 171 register structures share a listing with another, typically a change of legal entity at the same address or a corner and its host; they are kept as separate structures, which overstates local competition by one where a legal entity changed, and keeping one structure per listing changes no result (Table A1).

A manual check of 100 matches drawn at random classed 78 as certain (same name and address), 13 as plausible (same brand in the same commune at another address, or the listing of the optician shop hosting a corner), 5 as doubtful and 4 as wrong (a different business at another address, in one case the chain's head office). Six of the nine doubtful or wrong matches concern unbranded independents whose legal name carries no information (6 of the 48 drawn), the other three an integrated chain, a brand network and a mutualist site, so that the error rate is between 4 and 9% overall and about 12% among unbranded independents. A wrong match attaches a neighbouring business's reviews to a centre; the doubtful and wrong matches are kept, and their share bounds the noise this introduces. The same draw showed that four of the 48 sites classed as unbranded independents were a corner of an optician chain (three) or a franchised centre (one), which the keyword rules cannot see; they are kept as classified, and four in 48 bounds the share of corners and franchises hidden among the independents at about 8%.

All Google fields are a snapshot of what the API returned on that day. Listings, ratings and review counts change continuously, so a later collection will not reproduce the figures exactly. Only the fields listed above were requested: no review text and no information about reviewers. The coordinates returned by the API were used solely to validate the match; every distance and competition measure rests on commune centroids. The Google Maps Platform terms of service restrict the storage and redistribution of Places content; accordingly no site-level Google field is redistributed and none appears in this paper, which reports only statistics aggregated over groups of sites. The collection script, field mask and matching rules are published with the code; re-running the collection requires an API key, incurs charges at the rates in force, and returns the platform's state at the time of the run.

## Website content variables

For each matched site with a website in its listing (2,778 sites, 639 distinct domains), the page referenced by the listing was read once per site. The domain's home page and up to three internal pages whose address or link text refers to prices, the *100% Santé* scheme or a free trial were read once per domain. A first reading, on 3 September 2026, decoded each page with the character encoding assumed by the client library, which dropped the euro sign and mangled accented characters on part of the pages, so that amounts were detected only where the word *euros* was spelled out; The coding rules were revised at the same time: the variable now counts price ranges and indicative ranges as well as stated prices, excludes financing terms and eyewear, and counts the regulatory mentions only near a word referring to hearing. The variable is therefore broader than the one used in earlier versions of this paper, whose figures are superseded. The reading used here took place on 4 September 2026 with an identified user agent naming the study and a contact address, with a pause of a quarter of a second between requests in each of two parallel readers, reading each page in its declared encoding, applying the path rules of each domain's robots.txt, and reading price pages first among the internal pages. The text was coded automatically for price information (an amount between 100 and 20,000 euros for hearing aids in a price context, whether a price, a range or an indicative range, excluding reimbursement explanations, the regulatory amounts, financing terms, insurance excess, eyewear and quoted customer reviews), a page dedicated to hearing-aid prices, a mention of the fully reimbursed class I devices and of class II devices, of a free trial, of a free hearing test, of online booking (a booking module, an online agenda or a request form, not an invitation to call), of a quote and of guarantee or follow-up terms; the mentions of the regulated offer, the trial and the guarantee are counted only near a word referring to hearing. A manual check of 100 sites, 50 coded as carrying price information and 50 not, found no false positive and one false negative for price information, no error for the class I mention and the free trial, and, for online booking, no false positive and six false negatives, all on the pages of one optician chain; the 50 positive sites span six domains, so the check says more about the chains' pages than about the independents'. The raw text was retained only for coding and is not redistributed. Chain websites are national, so for chains these variables describe the brand; for independents they describe the centre. In all, 2,706 sites (91% of matched sites) have a readable website; the 72 that do not are dead links, time-outs or domains that exclude automated readers.

## A benchmark that is not a credence good

To hold the place, the platform and the population of reviewers constant, the same collection was run for hairdressers. In 880 communes of the sample, all 280 in which the hearing-aid centre has no competitor and 200 drawn at random from each other band, a text search for *coiffeur* biased towards the commune centroid returned up to three salons, whose rating, number of reviews and status were collected in the same way; 879 communes returned at least one salon, and 2,574 salons within 10 km of the centroid and not flagged as closed enter the benchmark. Hairdressing is an experience good, local, frequent, delivered to the same population by small firms and, in the same communes, rated by the same reviewers. A hairdresser has competitors in every commune of the sample, so the benchmark cannot separate the nature of the good from the existence of an exit option; it controls for the place, the platform and the reviewers, nothing more. The three salons are those the text search ranks first, which favours listings with many reviews: in a small commune they are the population of salons, in a large one the top of a much larger set. This selection inflates the hairdressers' activity gradient and, if anything, compresses their low tail in dense markets; both work against the contrasts reported below. No measure of competition among salons was built; the hairdressers' figures are reported on the hearing-aid competition bands, which stand in for the size of the local market.

## Data protection

The register extraction is released under the Licence Ouverte 2.0 and contains the names and professional addresses of registered practitioners. Names were used only to classify sites by brand. The published site layer carries the register's public structure identifier and is therefore linkable to the register: for a structure with a single registered practitioner, a row describes that practitioner's professional activity. It contains no name, registration number, street address or Google field, and no variable that is not derived from a public source or from the study design; it locates sites at the commune, the resolution used throughout. It carries the structure identifier, the commune code, the organisational form, the brand for chains and networks, the owner flag, the number of registered practitioners, the competition measures, the sampling stratum and weight and the coded website variables. Google ratings were linked to sites only in a working file held by the author, retained until the final version of this paper for replication requests answered by re-analysis, and are not shared in any site-level form. The processing serves research purposes on the basis of the author's legitimate interest (GDPR, Article 6(1)(f)) with the safeguards of Article 89(1); the persons concerned are informed through the data-protection notice published with the repository, which states the retention periods; no restricted-access data were used and no patient or practitioner was contacted.

# Empirical approach and expectations

The analysis is descriptive throughout: weighted means and medians by competition band with bootstrap intervals resampled by commune, weighted least squares with standard errors clustered by commune (by domain for the website regressions), a Poisson pseudo-maximum-likelihood regression for review counts, and commune fixed effects for the comparison of organisational forms within a market. The competition band is the number of other retail sites within 10 km in four classes: none, one to two, three to nine, ten or more. Controls are the log of commune population, median income, the log of the older population per centre within 10 km, the share of residents aged 65 and over, the number of practitioners on site, the owner flag and the organisational form.

The laboratory result of Angerer et al. (2026) suggests four expectations, which are mine and not the authors'. Rating activity, the share of centres rated and the number of reviews per centre, should rise with the number of alternatives, because rating is part of a choice process that has no object where there is nothing to choose between; but review volume is the product of patient flow, the propensity to review, solicitation and the age of the listing, and only the first and last are partly controlled (H1). The level of ratings should be high everywhere, because the outcomes a hearing-aid patient observes are those of a good experience and the outcomes that would justify a low rating are those the credence good hides; the hairdresser benchmark tells whether the level is a property of the good or of the platform (H2). If ratings carry any information about providers, their dispersion across providers should be larger where consumers compare providers, either because comparison makes reviews more discriminating or because heterogeneous providers coexist only in denser markets; the hairdresser benchmark tells whether the dispersion is a property of the place (H3). And the owner-practitioner, whose centre has no centralised marketing to solicit reviews and who has less to gain from volume than a network that advertises nationally, should show lower rating activity than the salaried practitioner of an integrated chain, whatever the local competition (H4).

# Results

## Descriptive statistics

Table 1 describes the matched sample by organisational form and by competition band. Organisational forms differ in review volume and rating level: integrated chains and optician corners have the most reviews and the lowest ratings, brand networks and unbranded independents the fewest reviews and the highest ratings. And the competition bands differ in almost everything: a centre with no competitor within 10 km sits in a commune of 3,700 inhabitants on average, 15 km from the nearest other centre, with an accessibility index of 54; a centre with ten or more competitors sits in a commune of 61,000, 300 metres from the nearest other centre, with an index of 97. The share of owner-operated centres is higher in the first band (52%) than in the others (43 to 44%).

Table 1. Descriptive statistics, matched sample (weighted).

|  | Integrated chains | Brand networks | Optician corners | Mutualist networks | Unbranded independents | All |
|---|---|---|---|---|---|---|
| Sites in sample | 649 | 354 | 325 | 171 | 1,467 | 2,966 |
| Owner-practitioner on site | 6% | 62% | 41% | 3% | 64% | 44% |
| Practitioners on site | 1.45 | 1.45 | 1.26 | 1.34 | 1.29 | 1.34 |
| Competitors within 10 km | 78.9 | 45.6 | 72.3 | 25.1 | 86.9 | 75.1 |
| Sites with ≥ 1 review | 98% | 96% | 96% | 96% | 91% | 94% |
| Median reviews | 29 | 24 | 150 | 27 | 23 | 28 |
| Mean rating (rated sites) | 4.70 | 4.86 | 4.69 | 4.76 | 4.81 | 4.77 |
| Website on listing | 99% | 100% | 99% | 96% | 88% | 94% |

|  | 0 competitors | 1–2 | 3–9 | 10+ |
|---|---|---|---|---|
| Sites in sample | 280 | 746 | 502 | 1,438 |
| Owner-practitioner on site | 52% | 43% | 44% | 44% |
| Distance to nearest centre (km) | 14.9 | 1.6 | 0.6 | 0.3 |
| Commune population | 3,735 | 5,807 | 14,452 | 61,278 |
| Median income (€ thousand) | 24.0 | 24.4 | 24.4 | 26.1 |
| Accessibility index (APL) | 54 | 61 | 69 | 97 |
| Sites with ≥ 1 review | 87.5% | 92.6% | 93.4% | 94.8% |
| Median reviews | 9 | 16 | 25 | 34 |
| Mean rating (rated sites) | 4.82 | 4.76 | 4.79 | 4.77 |

*Source: author's calculations from the RPPS public extraction (Agence du Numérique en Santé, August 2026, Licence Ouverte 2.0) and the Google Places API (New), collected 3 September 2026; aggregated statistics only. Weighted by sampling weights. Median reviews count unrated sites as zero.*

## Rating activity follows the choice set

Figure 2 shows the first result. The median number of reviews rises from 9 with no competitor to 16, 25 and 34 across the bands (panel A), and the share of sites with at least one review from 87.5% to 94.8% (panel B). The gradient is present within integrated chains and within unbranded independents; in the specification of Table 2, the interactions between the bands and the independent indicator are −0.25, −0.24 and −0.02 (standard errors 0.18 to 0.21), and a Wald test does not reject equality of the gradients (p = 0.19). The hairdressers of the same communes, plotted as the dashed line, are rated in 99.5 to 100% of cases in every band, and their median review count rises from 51 to 122.

![Review activity by local competition. Weighted medians and shares with 95% intervals from a bootstrap by commune (200 replications). Hairdressers, unweighted: up to three salons per commune in 879 communes of the sample. Source: RPPS public extraction and Google Places API (New), 3 September 2026; aggregated statistics only.](fig1_activity.png)

Table 2 reports the regression counterpart. In a weighted regression of log(1 + reviews) on the competition bands, the organisational form, the owner flag, the number of practitioners, log population, median income, the log of the older population per centre and the share of residents aged 65 and over, with standard errors clustered by commune, the band coefficients are 0.33, 0.59 and 0.72 relative to sites with no competitor, all significant at the 1% level. Log population adds 0.12 per log point; the demand-per-centre measure adds nothing once the bands are in. A Poisson regression on the count of reviews gives band effects of 0.48, 1.04 and 1.30. Replacing the bands by continuous measures, the log of one plus the number of competitors enters at 0.11 (s.e. 0.04) and the log of the distance to the nearest centre at −0.17 (s.e. 0.05). The probability of having at least one review follows the same pattern, with band effects of 6 to 8 points. Excluding optician corners, recoding unmatched sites as unrated, counting distinct alternatives instead of sites, keeping one structure per Google listing, classing Audilab as an integrated chain or measuring competition within 20 km instead of 10, which halves the precision of the band coefficients without changing their order, leaves these results in place (Tables A1 and A10); the log of the count within 20 km adds nothing once the 10 km bands are in (0.05, s.e. 0.04), so that the 10 km count carries the gradient.

Table 2. Rating activity and content: weighted least squares, standard errors clustered by commune.

|  | log(1 + reviews) | ≥ 1 review | Rating (if ≥ 1 review) |
|---|---|---|---|
| 1–2 competitors | 0.329 (0.110)*** | 0.057 (0.024)** | -0.060 (0.038) |
| 3–9 competitors | 0.588 (0.142)*** | 0.068 (0.028)** | -0.025 (0.039) |
| 10+ competitors | 0.721 (0.151)*** | 0.081 (0.028)*** | -0.053 (0.043) |
| Brand network | 0.117 (0.098) | -0.025 (0.014)* | 0.130 (0.023)*** |
| Optician corner | 1.164 (0.110)*** | -0.025 (0.013)* | -0.033 (0.025) |
| Mutualist network | 0.015 (0.109) | -0.015 (0.016) | 0.062 (0.035)* |
| Unbranded independent | -0.017 (0.080) | -0.074 (0.012)*** | 0.078 (0.021)*** |
| Owner-practitioner on site | -0.368 (0.077)*** | 0.004 (0.012) | 0.059 (0.018)*** |
| Practitioners on site | 0.241 (0.038)*** | 0.021 (0.005)*** | -0.034 (0.013)*** |
| log commune population | 0.120 (0.035)*** | -0.002 (0.005) | -0.005 (0.008) |
| log older population per centre | 0.071 (0.094) | 0.026 (0.016)* | -0.037 (0.022)* |
| Share aged 65+ (points) | -0.010 (0.005)* | -0.001 (0.001) | 0.000 (0.001) |
| Median income (€ thousand) | 0.017 (0.007)** | 0.003 (0.001)*** | 0.003 (0.002) |
| Observations | 2,966 | 2,966 | 2,768 |
| R² | 0.136 | 0.029 | 0.042 |

*Reference: integrated chain with no competitor within 10 km. Column 2 is a linear probability model. Sampling weights; standard errors clustered by commune (1,782 clusters). \*\*\* p < 0.01, \*\* p < 0.05, \* p < 0.10.*

The hairdresser benchmark puts the gradient in perspective. In the 879 communes of the benchmark, with the same bands and controls for population and income only, the hearing-aid centres' review counts rise by 0.34, 0.74 and 0.68 log points across the bands and the hairdressers' by 0.09, 0.26 and 0.34; the log population coefficient is 0.21 for the centres and 0.33 for the salons. Both regressions control for town size; for the centres the bands measure competition among centres, for the salons they are only a coarser proxy for the local market, so that any band effect on salons is an upper bound on what the place alone produces. On that comparison, review volume for the credence good rises with the number of alternatives well beyond what the size of the town explains.

## Rating levels sit near the ceiling for everyone

The third column of Table 2 and panel A of Figure 3 show the second result. The mean rating among rated centres is 4.82, 4.76, 4.79 and 4.77 across the bands; no band coefficient is distinguishable from zero. Hairdressers in the same communes average 4.74, 4.73, 4.74 and 4.73, with a band effect of −0.05 in the densest band (p = 0.04) once population and income are controlled. The near-ceiling level is therefore not specific to the credence good: an experience good rated on the same platform by the same population of reviewers sits at the same level, and neither level moves with the local choice set by more than a few hundredths. The rating column of Table 2 is conditional on being rated, a selection that varies from 87.5% to 94.8% across bands.

![Rating content by local competition. A: weighted mean rating among rated sites, and among sites with at least ten reviews; hairdressers in the same communes. B and C: among the quarter of sites with the most reviews within each band, the standard deviation of ratings across sites and the share of sites rated below 4.5. 95% intervals from a bootstrap by commune (200 replications); hairdressers unweighted. Source: RPPS public extraction and Google Places API (New), 3 September 2026; aggregated statistics only.](fig2_content.png)

Conditioning on an established score changes the picture slightly and in one direction. Among centres with at least ten reviews, those with three or more competitors are rated 0.07 to 0.09 lower than those with none (p = 0.01 to 0.02); among centres with at least thirty reviews, 0.07 lower (p = 0.04 to 0.05). Weighting each centre's rating by its number of reviews, which approximates the rating an arriving patient reads, gives 4.87 and 4.84 in the two thin bands against 4.64 and 4.60 in the two competitive ones (4.87, 4.84, 4.64 and 4.58 without the optician corners). Thin markets are not rated lower; their established providers are rated higher, and the review-weighted gap of a quarter of a point is the largest level difference in the paper.

The excess of perfect scores in thin markets is a review-count artefact. Exactly 5.0 is the rating of 50.6% of rated sites with no competitor and 34.9% of those with ten or more, but a site with three reviews is far more likely to sit at 5.0 than a site with eighty; conditional on the review-count bin, the band coefficients in a regression of the perfect-score indicator are zero (Table A2). Two supply-side differences survive that control: unbranded independents are 24 points more likely to carry a perfect score, and owner-operated centres 10 points more.

## Ratings are twice as dispersed across providers where there is choice

What competition changes is the spread of ratings across providers. Because the dispersion of a mean rating falls mechanically with the number of reviews, and because review counts rise with competition, comparing all rated sites would confound the two. Panels B and C of Figure 3 therefore compare, within each band, the quarter of sites with the most reviews, which selects the same share of sites in every band: 62 centres with at least 29 reviews where there is no competitor, 341 with at least 87 where there are ten or more (Table A2). The sampling noise of the mean works against the result: a mean of 29 ratings is noisier than a mean of 87, so dispersion should, on this account alone, be larger in the thin bands. The bounded scale works the other way: the top quarter of the thin bands sits closer to the maximum (4.86 to 4.88 against 4.73 to 4.75), and part of any compression near a ceiling is mechanical; the paper reports the dispersion measures and the level together for that reason.

The dispersion is smaller by half in the thin bands. Among these well-reviewed centres the standard deviation of ratings across sites is 0.150 with no competitor, 0.139 with one or two, 0.248 with three to nine and 0.298 with ten or more. The difference between the two thin and the two competitive bands, a grouping chosen after inspection of the four, is 0.145, with a 95% interval from 0.095 to 0.200 obtained by a bootstrap by commune; a Levene-type regression of the absolute deviation from the band median on the bands and the organisational form, with standard errors clustered by commune, rejects equality across the four bands (p = 0.001) and gives a linear trend of 0.023 per band (p = 0.006). The pattern holds within a fixed window of 30 to 90 reviews, where the noise of the mean is comparable across bands: the standard deviations are 0.16, 0.13, 0.23 and 0.25 (interval for the difference, 0.05 to 0.17), and the mean ratings differ by 0.05 only (4.86 and 4.87 against 4.81 and 4.81), so that the ceiling has less room to act in the window than in the top quarter. The window matters because, within the top quarter, review counts and bands are almost collinear (the quarter starts at 29 reviews in the first band and at 87 in the last): adding the log review count to the Levene regression of the top quarter leaves band coefficients that are small and negative (−0.03 each; p = 0.46 for the four), and the deviation rises with the count (0.06 per log point) because the large listings carry the lower ratings. The share of exact 5.0 scores in the top quarter falls from 36% and 25% in the thin bands to 14% and 19% in the competitive ones (Table A2): part of the compression is the bounded scale, in a proportion the paper does not estimate.

The compression is a property of established listings. Among sites with fewer than twenty reviews the standard deviation of ratings does not differ across bands (0.27, 0.28, 0.32 and 0.31 at 10 to 19 reviews), and over all rated sites the residual dispersion is larger in the thin bands, where means of a handful of reviews are noisy; the compression appears at 20 to 49 reviews (0.19, 0.21, 0.21 and 0.30) and is widest at 50 or more (0.09, 0.13, 0.25 and 0.27; Table A2). The optician corners, whose listings are the shop's, carry part but not all of it: without them, the top-quarter standard deviations are 0.15, 0.13, 0.21 and 0.30 (interval 0.06 to 0.22), the four-band Levene test weakens (p = 0.09, linear trend 0.019 per band, p = 0.03), and the linear-probability model of the low tail described below turns negative (−0.07, s.e. 0.03): at a given review count and composition, competitive markets then have fewer poorly rated centres. The band with one or two competitors is indistinguishable from the band with none in the spread of ratings, while its review volume has already risen by a third of a log point: one or two alternatives within 10 km raise rating activity without widening the differences between providers.

The low tail tells the same story descriptively and a more cautious one formally. Of the 236 most-reviewed centres with two or fewer competitors, five are rated below 4.5 (3.2% and 1.7% in the two bands); of the 459 with three or more, 56 are (13.6% and 11.7%). The tenth percentile of ratings is 4.70 to 4.71 in the thin bands and 4.37 to 4.40 in the competitive ones. But in a linear probability model of the below-4.5 indicator on the bands, the organisational form, the owner flag and the log of the review count, with standard errors clustered by commune, the band coefficients are zero: the low tail is accounted for by the review count (7 points per log point) and by composition, optician corners (+13 points) and unbranded independents (+7 points) being over-represented in it. The review count is itself the outcome of Section 5.2, so this specification closes the channel through which competition raises volume and, with it, the frequency of lower ratings; it says that competitive markets do not have more poorly rated providers at a given review count and composition, not that competition leaves the low tail unchanged. The positive coefficient on the review count also says that it is the large listings, not the small ones, that carry the lower ratings.

The hairdressers of the same communes show no comparable compression. Among their most-reviewed quarter, the standard deviation is 0.21, 0.22, 0.22 and 0.25 across the bands, a difference of about 0.02 between the same groups of bands (Brown-Forsythe p = 0.11) against 0.145 for the centres, and the share rated below 4.5 is 9%, 12%, 12% and 13%; their top quarter starts at 82 to 223 reviews, so their higher dispersion is measured with less noise than the centres', which strengthens the contrast. In the 30 to 90 window the salons' spread is 0.19, 0.20, 0.21 and 0.25 (p = 0.87 for the two-band split), against 0.16, 0.13, 0.23 and 0.25 for the centres. Stacking the most-reviewed centres and salons of the 558 communes that have both, with commune fixed effects, the interaction between the credence-good indicator and the competitive bands is 0.06 (s.e. 0.05) for the absolute deviation and 0.08 (s.e. 0.09) for the below-4.5 indicator: the direction is the one the descriptive comparison shows; the precision is not there to reject equality. The benchmark is a descriptive contrast within the same places between a good whose ratings spread out everywhere and a good whose ratings spread out twice as much where the patient could have gone elsewhere.

The pattern is carried by independents. Among the most-reviewed unbranded independents the standard deviation goes from 0.17 and 0.14 to 0.25 and 0.35; among the most-reviewed integrated chains, whose cells hold 9 to 50 sites, ratings are compressed at every level of competition (0.08 to 0.14). A standardised service rated by solicited patients leaves little to vary; an independent's rating varies across centres only where the patient could have chosen another.

## Ownership and organisation

Table 2 also shows the fourth result. Once the owner flag is in the regression, the organisational form has no effect on the log of review volume: the brand-network, mutualist and unbranded-independent coefficients are all within a tenth of zero, while an owner-practitioner on site is associated with 31% fewer reviews (0.37 log points, s.e. 0.08). In the Poisson specification, which weights the heavy upper tail of review counts, the form coefficients are large and positive (brand networks 0.55, unbranded independents 0.97, optician corners 1.70; Table A1) and the owner coefficient is −0.55: the statement about forms concerns the typical site, not the mean. The gap does not vary with competition: the interactions between the owner flag and the bands are 0.13, −0.10 and 0.11 (standard errors 0.18 to 0.20; Wald test p = 0.44). It does vary with the form: the owner effect is −0.22 in brand networks and −0.25 among unbranded independents, it is not identified within integrated chains, where owners are too few (−0.08, s.e. 0.17), and it is much larger in optician corners (−1.07; Wald test of equal effects across forms, p = 0.002). The corners are two populations (Table A8). At Optical Center, Acuitis, Générale d'Optique, Lissac, Atol and Optic 2000 the matched listing is the optician shop's, with a median of 59 to 417 reviews and a rating 0.11 below the integrated chains'; at Alain Afflelou Acousticien and Krys Audition the centre has a listing of its own, with a median of 12 to 17 reviews, like an independent's, and a rating 0.10 above. With the corners split, shop-listing corners collect seven times the reviews of an integrated chain (1.98 log points), own-listing corners the same volume (−0.04), the owner effect over the whole sample falls to −0.27 (23% fewer reviews), and the −1.07 is the own-listing corners' alone (−1.01, s.e. 0.38): the practitioner who owns a franchised centre collects fewer reviews than the salaried corner of a shop whose listing counts the shop's customers. That the owner effect is as large within brand networks and among unbranded independents as in the pooled sample says that it is not only the chains' solicitation machinery: at equal form, the practitioner who holds the practice collects fewer reviews. The differences between chains and independents that appear in raw comparisons are, to this extent, differences between salaried and owner-operated practices. Each additional practitioner on site adds 0.24 log points, the patient-flow component of volume. On the rating level, the pattern reverses: brand networks are rated 0.13 higher than integrated chains, unbranded independents 0.08 higher, and owner-operated sites 0.06 higher.

Table 3 restricts the comparison to the 684 sampled communes with at least two matched sites and adds commune fixed effects, so that forms are compared within the same local market. The owner effect on volume shrinks by two fifths and loses precision (−0.23 against −0.37, p = 0.12, 20% fewer reviews); the rating premium of brand networks (+0.16, p = 0.001) and of unbranded independents (+0.08, p = 0.07) holds, and unbranded independents remain five points less likely to be rated and eleven points less likely to list a website. These are comparisons between neighbours; they are not comparisons between the same practitioner under two forms of ownership, and the direction of selection into ownership is unknown.

Table 3. Organisational form within the same commune (commune fixed effects, 684 communes, 1,868 sites).

| Dependent variable | Owner-practitioner on site | Brand network | Optician corner | Unbranded independent | Practitioners | N |
|---|---|---|---|---|---|---|
| log(1 + reviews) | -0.226 (0.147) | 0.115 (0.197) | 1.050 (0.202)*** | -0.086 (0.151) | 0.217 (0.072)*** | 1,868 |
| ≥ 1 review | 0.004 (0.022) | -0.016 (0.030) | -0.008 (0.024) | -0.047 (0.022)** | 0.021 (0.013) | 1,868 |
| Rating (if ≥ 1 review) | 0.064 (0.040) | 0.162 (0.048)*** | -0.005 (0.048) | 0.084 (0.046)* | -0.055 (0.031)* | 1,758 |
| Website on listing | -0.007 (0.027) | 0.004 (0.023) | 0.020 (0.019) | -0.114 (0.024)*** | 0.013 (0.015) | 1,868 |

*Reference: integrated chain. Weighted least squares with commune fixed effects; standard errors clustered by commune. Sites in the same commune share the competition band and hence, up to rounding, the sampling weight, so the weighted estimates are close to unweighted ones. The mutualist-network coefficients (−0.073, −0.005, 0.050, −0.023, none significant) are omitted for space. By construction no site of the no-competitor band enters this table (bands 1–2, 3–9 and 10+: 579, 278 and 1,011 sites); the within-commune comparison of forms is therefore made outside thin markets. \*\*\* p < 0.01, \*\* p < 0.05, \* p < 0.10.*

## Income and entry

Two further cuts are reported for completeness. Across terciles of commune median income, with the competition bands and all other controls held constant, the top tercile has about 15% more reviews than the bottom (p = 0.08), two points more sites with any review (p = 0.09) and a rating higher by 0.04 (p = 0.09); the thinnest signal in the country is that of the poorest single-centre communes, with 8 reviews at the median and 87% of sites rated (Table A4). The gradient is small. Sites located in communes that had no registered practitioner in 2022, 445 in the matched sample, are recent entrants into a commune previously without a practitioner. Conditional on the competition band and the controls (2,761 sites with a known 2022 status), they have 7% fewer reviews than other sites, with a 95% confidence interval from −24% to +15%, and no difference in the probability of being rated or in the rating level. The estimate is imprecise, and the data say nothing about the incumbents of neighbouring communes. Accessibility as the companion study measures it adds no ordered pattern once the 10 km count is in. Within each band, the terciles of the accessibility index do not order review activity consistently (Table A9; the upper terciles of the no-competitor band hold 42 sites); added to the regression of Table 2, the middle tercile has 17% fewer reviews than the bottom (p = 0.02) and the top tercile is indistinguishable from it, the share rated does not move, and the rating is higher by 0.04 in the upper terciles (p = 0.08 and 0.16), or by 0.08 per log point of the index (p = 0.02). The count of alternatives within 10 km, not the supply per older resident within 30 km, is the measure that rating activity follows.

## Website content

The provider's website is the other information device that Gottschalk, Mimra and Waibel (2020) observed. In their Zurich sample, dentists who complied with the legal obligation to display their price level recommended unnecessary treatment about sixteen points less often, and an informative website went with more overtreatment only among recently licensed dentists. The two variables differ in status: in Zurich price display was a legal obligation and non-display a breach; in France the regulation requires a standardised quote before the sale, not an online price list, so that display on a website is a voluntary marketing choice and its absence carries no compliance signal. Table 4 reports what French hearing-aid centres display on their own sites. Price information is decided at brand level. Among integrated chains, 92% of sites belong to a brand whose website gives prices or price ranges for hearing aids and 94% to a brand with a page dedicated to hearing-aid prices; the figures are 22% and 26% for brand networks, 21% and 25% for optician corners, 11% and 15% for unbranded independents, and under 1% for mutualist networks, whose listings point to a directory. What the chains give is a range, not a list (Table A5): Amplifon and Audika state the class I cap and a range or a floor for class II devices, Audition Santé gives a price range for each manufacturer it carries, Alain Afflelou a recommended price for its own device; Audition Conseil, a network of independent owners, gives prices on 68% of its sites, the only brand within which the practice varies from centre to centre. Mentions of the fully reimbursed class I devices, of the free trial and of online booking are most frequent among integrated chains and least frequent among unbranded independents and mutualist sites, with one exception: the optician corners, half of which do not mention the regulated hearing-aid offer at all.

Table 4. Website content by organisational form (weighted; conditional on a readable website).

|  | Integrated chains | Brand networks | Optician corners | Mutualist networks | Unbranded independents |
|---|---|---|---|---|---|
| Price information displayed | 91.7% | 22.1% | 21.2% | 0.8% | 10.9% |
| Page dedicated to prices | 94.2% | 26.4% | 24.9% | 0.8% | 14.6% |
| Mentions class I (fully reimbursed) | 99.7% | 95.1% | 47.2% | 5.9% | 58.7% |
| Mentions class II | 94.9% | 69.8% | 41.6% | 2.6% | 34.3% |
| Free trial | 99.2% | 86.4% | 87.9% | 78.8% | 57.6% |
| Free hearing test | 99.3% | 86.5% | 88.8% | 79.5% | 59.1% |
| Online booking | 79.2% | 58.8% | 34.6% | 7.5% | 37.4% |
| Quote | 95.9% | 73.8% | 67.6% | 79.2% | 41.1% |
| Guarantee or follow-up terms | 98.4% | 84.8% | 83.6% | 6.1% | 56.9% |
| Sites with readable website | 640 | 350 | 322 | 163 | 1,231 |

For the question of this paper the relevant population is the unbranded independents, whose websites are their own. Among them, 6% give price information where the centre has two or fewer competitors and 11 to 12% where it has three or more, and 61% and 58% mention the class I devices; conditional on the controls, the two competitive bands are 5 to 6 points higher on price information than the band with no competitor, with p-values of 0.14 and 0.23, and the other variables do not move (Table A6). The doubling is suggestive and imprecise, and the share with a page dedicated to prices does not move (12 to 16% in every band); on this sample, the information an independent chooses to put on its website is at most weakly related to the local choice set. Owner-operated independents mention the free trial and the free test eight to nine points less often than salaried ones, and online booking nine points more often.

Nor is it related to ratings. Across all readable sites, with the bands, the organisational form and the controls held constant and standard errors clustered by domain (Table A7), price information is unrelated to the number of reviews (coefficient −0.13, s.e. 0.36) and to the rating (−0.01, s.e. 0.04); a price page is likewise unrelated to either. Two content variables are associated with the rating. The mention of the class I devices goes with a rating higher by 0.12 (s.e. 0.03) and the mention of class II devices with a rating higher by 0.08 (s.e. 0.03); since nearly every chain site mentions them, the coefficients are identified among independents, optician corners and mutualist sites, and say that an independent that presents the regulated offer on its site is rated higher than one that does not; they say nothing about price information. No content variable is associated with the number of reviews at the 5% level. The marker that separated well-behaved dentists in Zurich is, in this market, set nationally by the chains and chosen locally by one independent in ten, and no association between it and ratings is detected.

# Interpretation

The results fit a reading of the reputation mechanism that keeps close to what the data show. In the laboratory, a rating system works through three links: consumers rate, ratings reflect outcomes, and the next consumer chooses on ratings. The third link is what gives the first two their force. The field data show the first link scaling with the precondition of the third, the existence of alternatives; whether the next patient actually chooses on ratings is not observed. The benchmark shows that this is not an effect of the place: hairdressers in the same communes are rated everywhere, with a gradient half as steep that follows the size of the town.

The second link is where the two goods differ, with the reservation that a hairdresser always has competitors, so that the benchmark cannot tell the nature of the good from the presence of an exit option. Rating levels are near the ceiling for hairdressers and hearing-aid centres alike; the platform, not the good, sets the level. But the hairdresser's rating spreads across salons in every commune, with one salon in ten rated below 4.5 whether the town has one hearing-aid centre or fifty. The hearing-aid centre's rating spreads across centres twice as much where the centre has competitors. Three mechanisms are consistent with this and the data do not separate them. One is on the demand side: a patient who has compared providers, or who knows that others can, writes a more discriminating review than a patient who has nowhere else to go and will see the same practitioner for the next four years. The second is on the supply side: heterogeneous providers coexist only where the market has room for them, and the sole provider of a small town is, by selection, a survivor of a different kind. The third is in the generation of reviews: where volume is low, only the delighted write, and every centre sits at five; where solicitation and volume are high, the lukewarm write too, and a four-star review pulls a listing down. The third mechanism requires neither comparison nor heterogeneity, and the review-weighted levels of Section 5.3 fit it. Whichever mechanism operates, the variation across providers that a rating system needs in order to guide the next consumer's choice is compressed by half where the exit option is thin.

The comparison with the laboratory rating levels should be made with care, and in the opposite direction from the obvious one. Laboratory subjects rate on a scale from zero to five, give five stars to an outcome they have verified to be good, zero to a detected undertreatment, and, with wide dispersion, a median of three to the ambiguous case in which they may have been overcharged. The hearing-aid patient is, informationally, in the ambiguous case: he cannot tell whether the device, the setting or the price were the right ones. That he rates like the laboratory's satisfied consumer rather than like its ambiguous one is consistent with a field rating that records the experience the patient observes rather than the outcome he cannot; the data cannot say more.

The supply side adds two observations. Review volume is partly a decision of the provider: owner-operated practices collect 23% to 31% fewer reviews than practices with salaried practitioners, conditional on competition and form (the lower figure with the optician corners split by listing type), and 20% fewer within the same commune, where the estimate is imprecise; the pattern is consistent with the review-solicitation practices of integrated chains, which the data do not observe. The marketing devices on provider websites, price information first, are set at brand level for the chains; among independents, price information is twice as frequent where the centre has three or more competitors, a difference too imprecise to rest on. In the Zurich dental market, price display was a legal obligation and marked a type of dentist; in the French hearing-aid market it is a voluntary choice that marks a type of firm, and patients' ratings do not reward it.

None of this shows that ratings are useless in this market, or that providers in thin markets behave worse. It shows that the observable part of the rating system, its activity and its variation across providers, tracks the option to switch, and that its level is indistinguishable from that of an experience good on the same platform, so that nothing in it identifies the dimension that defines the credence good.

# Limitations

The competition measure is not exogenous. The number of centres within 10 km is largely a measure of urban density, and although population, income, demand per centre and the age structure are controlled, and the hairdresser benchmark holds the place constant, unobserved local factors, among them the digital habits of older patients, are not. The benchmark controls for the place but not for the patient, since hairdressers serve all ages, and it cannot separate the nature of the good from the presence of competitors, since a hairdresser always has some. The paper makes no causal claim. The dispersion result is measured on a bounded scale rounded to one decimal, and the top quarter of the thin bands sits closer to the maximum; a ceiling effect accounts for part of the compression, in a proportion the paper does not estimate.

Reviews are self-selected and, in integrated chains, presumably solicited. The number of reviews is a measure of rating activity, not of patient flow; the regressions control for the number of practitioners on site but not for turnover or for the age of the listing, so that part of the competition gradient may reflect older listings in older markets. The rating measures reported satisfaction, not the appropriateness of the treatment; a satisfied patient may have been over-fitted, and no observational dataset in this market contains the counterfactual. Ratings are returned rounded to one decimal, so the dispersion measures rest on rounded values, and review counts include ratings without text and are affected by Google's undisclosed removal of reviews.

Google is one platform. The match between register structures and listings is automatic: 1.1% of sites are unmatched, and the manual check of 100 matches found 4 wrong and 5 doubtful, almost all among unbranded independents whose legal name carries no information. Distances are straight lines between commune centroids and treat every site in a commune as located at its centre. The organisational classification is keyword-based and data-driven; the trade name in the register is declarative and often missing, so that members of networks are under-counted and counted as independents, small regional groups are counted as independents, the keyword rules, tightened after a manual check, may still capture unrelated names, and Audilab, a Demant subsidiary with practitioner shareholders, sits at the threshold of the rule. The owner flag records the register's role of practice holder, declared by the practitioner, not the ownership of the company: an independent who runs his centre through a company as its salaried manager is not flagged, and a franchisee is. The register counts structures: a centre whose legal entity changed may appear under two identifiers and overstate local competition by one.

The website variables are coded by rules applied to at most five pages per site. Prices displayed in images or by client-side scripts are missed; a domain that excludes automated readers drops all of its sites at once; the manual check of Section 3.4 validates the coding mainly on the chains' pages; on the independents' own pages, where the variation of interest lies, it rests on the 50 negative draws and on the rules themselves. The price variable records price information, whether a list, a floor or an indicative range; it does not measure what the centre charges. The sample over-represents thin markets by design and is re-weighted; the exhaustive strata are the ones that carry the results. Finally, the Google data are a snapshot that cannot be archived or shared at the site level, so that the results can be verified only by re-collection, which returns a later state of the platform.

# Conclusion

A public rating system in a credence goods market rests on the consumer's option to leave. This paper observes such a system across the full range of that option, from hearing-aid centres with no competitor within 10 km to centres with dozens of competitors, and finds that its activity and its variation across providers follow the option while its level does not. Ratings are near the ceiling everywhere, for hearing-aid centres as for the hairdressers of the same towns; they are thin, high and compressed where the patient has nowhere else to go nearby, and thick and dispersed where he has. Owner-operated practices collect 31% fewer reviews than practices with salaried practitioners in every kind of market, and the price information on providers' websites is set by the chains, is twice as frequent, imprecisely, among independents with three or more competitors, and goes with no better rating.

Two questions follow. The natural experiment that the companion study documents, the entry of several thousand centres between 2022 and 2026 into a market whose reimbursement rules had just changed, offers a way to observe the rating system of a provider from its first review onwards and to ask whether the arrival of a competitor changes what an incumbent's patients say. And the review texts themselves, which this paper deliberately did not collect, would tell what patients in thin and competitive markets write about, and whether the dimension that the credence good hides ever surfaces in what they say.

# Declarations {-}

The author is a state-registered *audioprothésiste* who practised for nearly four years in centres of the kind studied here, at a public hospital and, as a salaried practitioner and centre manager, in a centre of Audika, one of the integrated chains named in this paper, before returning to study economics. He is not employed by, and holds no financial interest in, any provider, manufacturer or distributor in the sector, and has no ongoing contractual relationship with his former employer. No site was treated differently from any other; the classification is mechanical. The study received no funding, was not commissioned, and was not shown to any actor in the sector before circulation; API charges were paid by the author. It uses only publicly available data and involved no interaction with patients or providers. Statements attributed to the author's experience of the profession draw on that employment and are not observed in the data. This working paper is released under a Creative Commons Attribution 4.0 licence.

# Data and code {-}

The code for every step (register extraction and classification, competition measures and alternatives, sample design, Google collection, website reading and coding, public layer, benchmark, analysis, figures and the generation of every table of this paper from the output files) is available at <https://github.com/Nsoussan/deserts-audioprothese>, directory `ratings/`, release v2.3.0; this paper is deposited on Zenodo under doi:10.5281/zenodo.22286005, which resolves to the latest version. The repository contains the site layer described in Sections 3.1 and 3.6, in which the 2,999 sampled sites are identified by their stratum and weight and the 60 excluded structures by the retail flag, the keyword rules and legal-name mapping used for classification, the seeds of the benchmark draw and of the bootstraps, the list of the 879 benchmark communes, and the aggregated tables underlying the figures and the appendix; the sample draw of 3 September 2026 is documented by a script that checks the published sample against the design (its seed was not kept), and the intermediate files that carry names, addresses or Google fields are not distributed. Ratings, review counts and listing websites are Google Maps Platform content collected through the official API and used here only in aggregated form; no site-level Google field is redistributed. Inputs: RPPS public extraction, Agence du Numérique en Santé, file *Personne_activite*, August 2026, Licence Ouverte 2.0; commune-level variables and coordinates from the companion study (report doi:10.5281/zenodo.22177322, data doi:10.5281/zenodo.22177338, code doi:10.5281/zenodo.22177296).

# References {-}

Angerer, S., Glätzle-Rützler, D., Mimra, W., Rittmannsberger, T. and Waibel, C. (2026). The value of rating systems in credence goods markets. *The Economic Journal*, advance access, doi:10.1093/ej/ueag011.

Assurance Maladie (2026). *Aides auditives : quelle prise en charge ?* ameli.fr, accessed 3 September 2026.

Autorité de la concurrence (2019). Décision 19-DCC-244 du 11 décembre 2019 relative à la prise de contrôle exclusif de la société Audilab par le groupe Demant.

Balafoutas, L. and Kerschbamer, R. (2020). Credence goods in the literature: What the past fifteen years have taught us about fraud, incentives, and the role of institutions. *Journal of Behavioral and Experimental Finance*, 26, 100285.

Darby, M. R. and Karni, E. (1973). Free competition and the optimal amount of fraud. *The Journal of Law and Economics*, 16(1), 67–88.

Dulleck, U. and Kerschbamer, R. (2006). On doctors, mechanics, and computer specialists: The economics of credence goods. *Journal of Economic Literature*, 44(1), 5–42.

Dulleck, U., Kerschbamer, R. and Sutter, M. (2011). The economics of credence goods: An experiment on the role of liability, verifiability, reputation, and competition. *American Economic Review*, 101(2), 526–555.

Filippas, A., Horton, J. J. and Golden, J. (2022). Reputation inflation. *Marketing Science*, 41(4), 733–745.

Gottschalk, F., Mimra, W. and Waibel, C. (2020). Health services as credence goods: A field experiment. *The Economic Journal*, 130(629), 1346–1383.

Hirschman, A. O. (1970). *Exit, Voice, and Loyalty: Responses to Decline in Firms, Organizations, and States*. Cambridge, MA: Harvard University Press.

Hong, Y. A., Liang, C., Radcliff, T. A., Wigfall, L. T. and Street, R. L. (2019). What do patients say about doctors online? A systematic review of studies on patient online reviews. *Journal of Medical Internet Research*, 21(4), e12521.

Institut national de la consommation (2026). *Vous achetez un appareil auditif*. inc-conso.fr, accessed 3 September 2026.

Kerschbamer, R., Neururer, D. and Sutter, M. (2023). Credence goods markets, online information and repair prices: A natural field experiment. *Journal of Public Economics*, 222, 104891.

Mimra, W., Rasch, A. and Waibel, C. (2016). Price competition and reputation in credence goods markets: Experimental evidence. *Games and Economic Behavior*, 100, 337–352.

Nosko, C. and Tadelis, S. (2015). The limits of reputation in platform markets: An empirical analysis and field experiment. NBER Working Paper 20830.

Saifee, D. H., Zheng, Z., Bardhan, I. R. and Lahiri, A. (2020). Are online reviews of physicians reliable indicators of clinical outcomes? A focus on chronic disease management. *Information Systems Research*, 31(4), 1282–1300.

Soussan, N. (2026). *L'accessibilité de l'audioprothèse en France : mesure communale de l'accès et de l'opportunité d'implantation, confrontée à la dynamique du marché 2022–2026*. Version 2.0, doi:10.5281/zenodo.22177322.

# Appendix {-}

Table A1. Robustness of the activity gradient (dependent variable log(1 + reviews) unless stated; all controls of Table 2; standard errors clustered by commune).

| Specification | 1–2 competitors | 3–9 competitors | 10+ competitors | N |
|---|---|---|---|---|
| Baseline (Table 2) | 0.329 (0.110)*** | 0.588 (0.142)*** | 0.721 (0.151)*** | 2,966 |
| Without demand and age controls | 0.299 (0.097)*** | 0.545 (0.111)*** | 0.696 (0.123)*** | 2,966 |
| Poisson on review count | 0.475 (0.207)** | 1.034 (0.389)*** | 1.299 (0.390)*** | 2,966 |
| Distinct alternatives instead of sites | 0.322 (0.110)*** | 0.608 (0.141)*** | 0.707 (0.152)*** | 2,966 |
| Distinct alternatives, Audika and Audilab merged | 0.329 (0.110)*** | 0.604 (0.141)*** | 0.719 (0.153)*** | 2,966 |
| Excluding optician corners | 0.335 (0.110)*** | 0.567 (0.147)*** | 0.743 (0.157)*** | 2,641 |
| ≥ 1 review, unmatched sites as unrated | 0.086 (0.026)*** | 0.102 (0.030)*** | 0.107 (0.030)*** | 2,999 |
| One structure per Google listing | 0.311 (0.110)*** | 0.562 (0.142)*** | 0.687 (0.152)*** | 2,880 |
| Audilab classed as an integrated chain | 0.330 (0.110)*** | 0.586 (0.142)*** | 0.719 (0.151)*** | 2,966 |
| Bands of competitors within 20 km (a) | 0.355 (0.239) | 0.570 (0.228)** | 0.652 (0.225)*** | 2,966 |
| Hearing-aid centres, benchmark communes (b) | 0.341 (0.114)*** | 0.743 (0.134)*** | 0.683 (0.182)*** | 1,346 |
| Hairdressers, benchmark communes (b) | 0.093 (0.053)* | 0.261 (0.064)*** | 0.337 (0.079)*** | 2,574 |

*(a) Bands of the number of competitors within 20 km, same cut-offs. (b) 879 communes; population and income controls only. Poisson form coefficients: brand network 0.55 (0.13), optician corner 1.70 (0.10), mutualist 0.18 (0.12), unbranded independent 0.97 (0.18), owner −0.55 (0.17).*

Table A2. Rating level and dispersion by competition band.

|  | 0 | 1–2 | 3–9 | 10+ |
|---|---|---|---|---|
| Rated sites | 245 | 691 | 469 | 1,363 |
| Mean rating | 4.82 | 4.76 | 4.79 | 4.77 |
| Rated exactly 5.0 | 50.6% | 40.1% | 32.2% | 34.9% |
| Review-weighted mean rating | 4.87 | 4.84 | 4.64 | 4.60 |
| Sites with ≥ 10 reviews: mean rating | 4.83 | 4.82 | 4.77 | 4.77 |
| Band effect on rating, ≥ 10 reviews (ref. 0) |  | -0.031 (0.21) | -0.074 (0.02) | -0.086 (0.01) |
| Top quarter by reviews within band: sites | 62 | 174 | 118 | 341 |
| Top quarter: minimum reviews | 29 | 40 | 66 | 87 |
| Top quarter: mean rating | 4.88 | 4.86 | 4.73 | 4.75 |
| Top quarter: rated exactly 5.0 | 35.5% | 25.3% | 14.4% | 18.8% |
| Top quarter: S.D. across sites | 0.150 | 0.139 | 0.248 | 0.298 |
| Top quarter: rated below 4.5 (sites) | 3.2% (2) | 1.7% (3) | 13.6% (16) | 11.7% (40) |
| Top quarter: rated below 4.7 | 8.1% | 6.9% | 28.8% | 22.9% |
| Top quarter: tenth percentile of ratings | 4.71 | 4.70 | 4.37 | 4.40 |
| Top quarter without optician corners: S.D. | 0.150 | 0.133 | 0.211 | 0.297 |
| Top quarter without optician corners: below 4.5 | 3.2% | 2.0% | 8.3% | 7.1% |
| Sites with 10 to 19 reviews: S.D. across sites | 0.268 | 0.283 | 0.316 | 0.310 |
| Sites with 20 to 49 reviews: S.D. across sites | 0.187 | 0.210 | 0.212 | 0.305 |
| Sites with ≥ 50 reviews: S.D. across sites | 0.091 | 0.133 | 0.252 | 0.274 |
| Hairdressers rated (salons) | 802 | 587 | 583 | 595 |
| Hairdressers, top quarter: S.D. across salons | 0.206 | 0.215 | 0.215 | 0.249 |
| Hairdressers, top quarter: rated below 4.5 | 8.8% | 12.2% | 12.2% | 12.8% |
| Sites with 30 to 90 reviews: S.D. across sites | 0.159 | 0.129 | 0.226 | 0.246 |
| Hairdressers with 30 to 90 reviews: S.D. | 0.194 | 0.202 | 0.211 | 0.245 |
| Perfect score, band effect conditional on review-count bin |  | -0.016 (0.64) | -0.009 (0.80) | 0.049 (0.19) |

*Weighted, except hairdressers; p-values in parentheses. Top quarter: quarter of sites with the most reviews within each band. Difference in top-quarter standard deviation between the two competitive and the two thin bands: 0.145, 95% interval from a bootstrap by commune 0.095 to 0.200 (without optician corners 0.064 to 0.218; 30 to 90 reviews 0.049 to 0.165). Levene-type regression on the four bands with form controls and commune clusters: p = 0.001, linear trend 0.023 per band (p = 0.006); without optician corners p = 0.09, trend 0.019 (p = 0.03). Linear probability model of the below-4.5 indicator, three or more against two or fewer competitors, with form, owner and log review count: −0.005 (s.e. 0.027); without optician corners −0.067 (s.e. 0.028). Hairdressers, unclustered Brown-Forsythe on the two-band split: p = 0.11.*

Table A3. Sample design.

| Competitors within 10 km | Organisational form (2026 classification) | Population | Sample | Weight |
|---|---|---|---|---|
| 0 | branded (chains, networks, opticians) | 105 | 105 | 1.00 |
| 0 | unbranded independent | 177 | 177 | 1.00 |
| 0 | mutualist | 9 | 9 | 1.00 |
| 1–2 | branded | 345 | 348 | 1.00 |
| 1–2 | unbranded independent | 367 | 364 | 1.00 |
| 1–2 | mutualist | 42 | 42 | 1.00 |
| 3–9 | branded | 940 | 250 | 3.77 |
| 3–9 | unbranded independent | 793 | 209 | 3.78 |
| 3–9 | mutualist | 170 | 45 | 3.80 |
| 10+ | branded | 2,412 | 641 | 3.77 |
| 10+ | unbranded independent | 2,778 | 732 | 3.77 |
| 10+ | mutualist | 283 | 77 | 3.78 |

*The sample was drawn on 3 September 2026 on a three-way classification (branded, mutualist, independent); the five-way classification of Section 2 and the tightening of the keyword rules in version 2.3 (26 sites reclassified, which is why the population and sample columns of the exhaustive strata differ by three) were introduced afterwards and do not affect the weights.*

Table A4. Rating activity by competition band and commune income tercile (weighted).

| Competitors within 10 km | Income tercile | Sites | ≥ 1 review | Median reviews | Mean rating |
|---|---|---|---|---|---|
| 0 | bottom | 132 | 87.1% | 8 | 4.85 |
| 0 | middle | 114 | 86.8% | 10 | 4.76 |
| 0 | top | 34 | 91.2% | 9 | 4.86 |
| 1–2 | bottom | 322 | 90.1% | 15 | 4.72 |
| 1–2 | middle | 260 | 95.8% | 17 | 4.79 |
| 1–2 | top | 164 | 92.7% | 15 | 4.81 |
| 3–9 | bottom | 228 | 91.2% | 23 | 4.78 |
| 3–9 | middle | 163 | 95.7% | 30 | 4.79 |
| 3–9 | top | 111 | 94.6% | 26 | 4.80 |
| 10+ | bottom | 390 | 94.6% | 36 | 4.74 |
| 10+ | middle | 475 | 93.9% | 34 | 4.75 |
| 10+ | top | 573 | 95.6% | 31 | 4.79 |

*Tercile cut-offs at 23,750 and 26,100 euros of median income per consumption unit; the 152 sites with imputed income fall in the middle tercile.*

Table A5. Brands: share of sites with an owner-practitioner (register), classification, and website price information (sites with a readable website).

| Brand | Sites (register) | Owner-practitioner | Classification | Price information displayed | Price page |
|---|---|---|---|---|---|
| Amplifon | 694 | 2% | integrated chain | 100% | 100% |
| Audika | 645 | 3% | integrated chain | 99% | 99% |
| Solusons | 35 | 6% | integrated chain | 0% | 0% |
| Audition Santé (Sonova) | 288 | 6% | integrated chain | 96% | 97% |
| Benoit Audition | 59 | 14% | integrated chain | 0% | 0% |
| Audition Marc Boulet | 49 | 16% | integrated chain | 100% | 100% |
| Manéo Audition | 22 | 23% | integrated chain | 0% | 0% |
| GrandAudition | 50 | 28% | integrated chain | 0% | 100% |
| Audilab | 272 | 49% | brand network | 2% | 2% |
| Audition Conseil | 177 | 51% | brand network | 68% | 68% |
| VivaSon | 57 | 58% | brand network | 100% | 0% |
| Audio 2000 | 100 | 59% | brand network | 2% | 14% |
| Idéal Audition | 23 | 61% | brand network | 0% | 0% |
| Audio pour tous | 19 | 68% | brand network | 0% | 0% |
| Sonance Audition | 108 | 69% | brand network | 2% | 98% |
| Entendre | 128 | 73% | brand network | 4% | 9% |
| Optician corners (eight brands, see note) | 1,076 | 21%–89% | optician corner | 0%–98% | 0%–100% |
| Écouter Voir, VYV3, mutualités | 504 | 3% | mutualist network | 1% | 1% |
| No brand | 4,115 | 63% | unbranded independent | 11% | 15% |

*Optician corners: Optical Center, Krys, Alain Afflelou, Atol, Optic 2000, Acuitis, Lissac, Générale d'Optique. Owner-practitioner: share of sites with at least one practitioner registered as practice holder. Audilab belongs to the Demant group, owner of Audika, and associates practitioners with the capital of local companies; the rule classifies it by its 49% share. What the integrated chains display is the class I cap and a range or a floor for class II devices, counted as price information (Section 5.7).*

Table A6. Website content of unbranded independents and local competition (weighted least squares, independents with a readable website, n = 1,231; controls of Table 2; standard errors clustered by commune).

| Dependent variable | 1–2 competitors | 3–9 competitors | 10+ competitors | Owner on site |
|---|---|---|---|---|
| Price information displayed | +0.006 (0.83) | +0.058 (0.14) | +0.050 (0.23) | +0.006 (0.75) |
| Page dedicated to prices | -0.006 (0.89) | -0.003 (0.95) | +0.022 (0.69) | +0.019 (0.39) |
| Mentions class I (fully reimbursed) | +0.027 (0.63) | +0.032 (0.66) | +0.082 (0.27) | +0.027 (0.40) |
| Mentions class II | -0.003 (0.95) | +0.004 (0.96) | -0.029 (0.71) | -0.014 (0.65) |
| Free trial | -0.014 (0.81) | +0.042 (0.56) | -0.014 (0.85) | -0.078 (0.01) |
| Free hearing test | -0.050 (0.39) | +0.021 (0.76) | -0.044 (0.55) | -0.086 (0.01) |
| Online booking | -0.031 (0.57) | +0.037 (0.59) | +0.098 (0.19) | +0.094 (0.00) |
| Quote | -0.034 (0.55) | +0.057 (0.42) | +0.007 (0.93) | -0.077 (0.02) |
| Guarantee or follow-up terms | +0.017 (0.77) | +0.042 (0.57) | -0.013 (0.87) | -0.079 (0.02) |

*Reference: unbranded independent with no competitor within 10 km; p-values in parentheses.*

Table A7. Website content and ratings (all readable sites; each row a separate regression with the controls of Table 2; standard errors clustered by domain).

| Content variable | log(1 + reviews) | Rating (if ≥ 1 review) |
|---|---|---|
| Price information displayed | -0.131 (0.358) | -0.006 (0.037) |
| Page dedicated to prices | -0.197 (0.315) | 0.013 (0.036) |
| Mentions class I (fully reimbursed) | -0.556 (0.310)* | 0.121 (0.029)*** |
| Mentions class II | -0.192 (0.293) | 0.082 (0.030)*** |
| Free trial | -0.012 (0.171) | 0.045 (0.025)* |
| Free hearing test | -0.008 (0.178) | 0.041 (0.026) |
| Online booking | -0.252 (0.208) | 0.004 (0.029) |
| Quote | 0.420 (0.256) | -0.038 (0.034) |
| Guarantee or follow-up terms | -0.050 (0.144) | 0.039 (0.027) |

*N = 2,706 (reviews) and 2,576 (rating). \*\*\* p < 0.01, \*\* p < 0.05, \* p < 0.10.*

Table A8. Optician corners: listing of the shop or listing of their own (matched sample).

| Brand | Sites | Listing | Owner-practitioner | Median reviews | Mean rating |
|---|---|---|---|---|---|
| Générale d'Optique | 3 | shop | 67% | 417 | 4.80 |
| Lissac | 2 | shop | 100% | 287 | 4.75 |
| Optical Center | 140 | shop | 24% | 240 | 4.55 |
| Acuitis | 11 | shop | 27% | 150 | 4.87 |
| Atol | 13 | shop | 54% | 65 | 4.87 |
| Optic 2000 | 9 | shop | 56% | 59 | 4.78 |
| Alain Afflelou Acousticien | 66 | own | 68% | 17 | 4.77 |
| Krys Audition | 81 | own | 48% | 12 | 4.90 |

*Regression of Table 2 with the corners split: shop-listing corners 1.979 (0.092)\*\*\* on log(1 + reviews), 0.017 (0.007)\*\* on being rated, -0.113 (0.028)\*\*\* on the rating; own-listing corners -0.042 (0.180), -0.087 (0.028)\*\*\* and 0.098 (0.031)\*\*\*; owner-practitioner -0.267 (0.075)\*\*\* on log(1 + reviews). Owner effect by form: own-listing corners -1.006 (0.381)\*\*\* relative to integrated chains, shop-listing corners 0.110 (0.241).*

Table A9. Rating activity by competition band and tercile of the accessibility index (APL, weighted).

| Competitors within 10 km | APL tercile | Sites | ≥ 1 review | Median reviews | Mean rating |
|---|---|---|---|---|---|
| 0 | bottom | 238 | 85.7% | 8 | 4.81 |
| 0 | middle | 37 | 100.0% | 12 | 4.82 |
| 0 | top | 5 | 80.0% | 16 | 5.00 |
| 1–2 | bottom | 575 | 92.0% | 17 | 4.75 |
| 1–2 | middle | 138 | 96.4% | 11 | 4.79 |
| 1–2 | top | 33 | 87.9% | 12 | 4.82 |
| 3–9 | bottom | 309 | 93.5% | 27 | 4.78 |
| 3–9 | middle | 165 | 93.3% | 22 | 4.79 |
| 3–9 | top | 28 | 92.9% | 28 | 4.88 |
| 10+ | bottom | 213 | 95.3% | 36 | 4.72 |
| 10+ | middle | 527 | 94.7% | 29 | 4.79 |
| 10+ | top | 698 | 94.7% | 35 | 4.77 |

*Tercile cut-offs at 72.4 and 98.9 accessible professionals per 100,000 residents aged 65 and over. Regressions of Table 2 with the APL terciles added (middle and top tercile against the bottom): log(1 + reviews), -0.192 (p = 0.02) and -0.072 (p = 0.47); rated, +0.005 (p = 0.70) and -0.006 (p = 0.70); rating, +0.037 (p = 0.08) and +0.037 (p = 0.16). With log(1 + APL) instead of the terciles: -0.158 (s.e. 0.116, p = 0.17), -0.014 (s.e. 0.018, p = 0.43) and +0.076 (s.e. 0.032, p = 0.02); the band coefficients move by less than 0.03.*

Table A10. Competition within 20 km (matched sample).

| Competitors within 20 km | 0 | 1–2 | 3–9 | 10+ |
|---|---|---|---|---|
| Sites in sample | 33 | 173 | 493 | 2,267 |
| Sites with ≥ 1 review | 78.8% | 89.6% | 92.4% | 94.4% |
| Median reviews | 7 | 14 | 21 | 30 |
| Mean rating (rated sites) | 4.83 | 4.68 | 4.77 | 4.77 |

*Adding the log of one plus the number of competitors within 20 km to the 10 km bands of Table 2: +0.049 (s.e. 0.035); the 10 km band coefficients become 0.316, 0.566 and 0.645.*
