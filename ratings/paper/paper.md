---
title: "Ratings Without Exit: Online Reputation and the Option to Switch in a Credence Goods Market"
subtitle: "Evidence from hearing-aid centres in France"
author: "Nathan Soussan"
date: "Working paper · version 1.0 · 3 September 2026"
abstract: |
  Public rating systems discipline expert sellers in credence goods markets because consumers can take their custom elsewhere. Laboratory evidence establishes this mechanism in markets where every consumer chooses among four experts; field markets do not hold the choice set constant. This paper uses the geography of a credence goods market, hearing-aid provision in France, to observe what a rating system looks like when the option to switch varies from nothing to plenty. I rebuild the 8,421 hearing-aid centres in the country from the public professional register, measure for each the number of competing centres within 10 km, and collect Google ratings through the official API for a stratified sample of 2,999 centres that includes every centre with fewer than three competitors. Three facts emerge. Rating activity rises steeply with the local choice set: the median centre with no competitor within 10 km has 9 reviews, the median centre with ten or more has 34, a gradient that survives controls for commune population and income and holds within national chains and within independents. Rating content does not: the mean rating lies between 4.76 and 4.82 in every competition band, close to the score that laboratory subjects assign after a good experience, and it does not respond to competition. Where no alternative exists the signal is not lower but thinner and more compressed: among well-reviewed centres, the cross-site dispersion of ratings roughly doubles from local monopoly to dense competition. National chains collect more reviews than independents in every market and within the same commune, consistent with systematic solicitation. Price transparency on providers' websites is a brand policy that neither follows local competition nor earns better ratings. The results are descriptive; they suggest that in the field the activity of a rating system, rather than its content, is what tracks the exit option on which its disciplining power rests.
geometry: margin=2.6cm
fontsize: 11pt
mainfont: "TeX Gyre Pagella"
linestretch: 1.15
numbersections: true
---

*Keywords:* credence goods, rating systems, reputation, competition, healthcare, hearing aids. *JEL:* D82, I11, L15, D83.

# Introduction

In a credence goods market the seller knows what the buyer needs and the buyer cannot verify, even after the fact, whether what was sold was what was needed (Darby and Karni, 1973; Dulleck and Kerschbamer, 2006). Healthcare is the canonical case. A recent laboratory experiment by Angerer, Glätzle-Rützler, Mimra, Rittmannsberger and Waibel (2026) shows that a five-star public rating system, of the kind that Google and Yelp have made ubiquitous, goes a long way towards solving the problem: in markets of four experts and four consumers, introducing ratings cuts undertreatment from 52 % to 7 % of interactions and overcharging from 86 % to 44 %, and raises market efficiency from 77 % to 97 %. The mechanism the authors identify is reputation through choice. Consumers punish a bad outcome with zero stars and reward a good one with five, and in the next period they visit the best-rated expert; the probability of changing expert rises from 0.25 after a good outcome to 0.80 after a detected bad one. Ratings discipline because consumers can leave.

The experiment holds one thing fixed that field markets do not: the choice set. Every consumer in every period picks from a list of four experts. The paper is explicit that its design maintains competition throughout and does not study what happens when fewer alternatives exist, and its concluding sentence calls for research on the resilience of rating platforms in the face of noise and declining reliability. This paper takes the choice set as the variable of interest. It asks a simple question that the laboratory cannot: what does a public rating system look like, in a real credence goods market, when the number of alternatives available to the consumer ranges from none to dozens?

The market is hearing-aid provision in France. It is a credence good in the strict sense: the practitioner (the *audioprothésiste*) tests, selects, fits and sells the device, and follows the patient over years; the patient, typically elderly, cannot judge whether a different device, a different setting or no device at all would have served as well. It is also a market with a documented geography. A companion study (Soussan, 2026) measures accessibility for all 34,900 French communes: 560 towns of more than 5,000 inhabitants have no practitioner, one town of 54,000 lies 146 km from the nearest one, and potential accessibility ranges from 11 professionals per 100,000 residents aged 65 and over in French Guiana to more than 90 in the Paris region. The choice set that the laboratory fixes at four here runs from zero to more than fifty within 10 km.

I rebuild the population of hearing-aid centres from the public extraction of the national register of health professionals (RPPS): 8,421 retail sites with address, trade name and staff, each attached to the accessibility measures of the companion study and to the number of other centres within 10, 20 and 30 km. For a stratified sample of 2,999 sites, which includes every site with fewer than three competitors within 10 km, I collect through the official Google Places API the rating, the number of reviews, the website and the business status of the matching Google listing. Coverage is not the problem it was for Zurich dentists in 2016, when Gottschalk, Mimra and Waibel (2020) could not construct a reputation measure from online ratings: 99.9 % of the sites have a listing, 98.9 % match on name, type and location, and 93.3 % of matched sites carry at least one review.

Three findings organise the paper. First, rating *activity* follows the choice set. The median site with no competitor within 10 km has 9 reviews and 87.5 % of such sites are rated at all; with ten or more competitors, the median is 34 and 94.8 % are rated. The gradient is monotonic, survives controls for commune population and median income, and holds separately within national chains and within independents. Second, rating *content* does not follow the choice set. The mean rating is 4.82 where there is no competitor and 4.77 where there are ten or more; no competition band differs from any other once site type is controlled. The level itself is telling: it is almost exactly the 4.76 stars that the laboratory subjects of Angerer et al. (2026) assign after an experience they can identify as good. In the field the patient cannot identify a bad one. Third, where the choice set is empty the signal is not lower but thinner and more compressed. Among sites with at least thirty reviews, the cross-site standard deviation of ratings is 0.15 under local monopoly and 0.27 under dense competition, and the share of ratings below 4.5 rises from 3.5 % to 8.3 %. The rating system exists everywhere; it discriminates between providers only where providers can be chosen between.

Two further results speak to the supply side of the reputation mechanism. National chains collect more reviews than independents at every level of competition, and they do so within the same commune: in the 406 sampled communes where a chain and an independent coexist, the independent has 18 % fewer reviews, is four points less likely to be rated at all, and is rated 0.07 higher. This is the pattern one expects when review volume reflects a solicitation policy rather than patient flow. Centres that opened after 2022 in towns that previously had none accumulate reviews at the same rate as incumbents once competition is controlled: online reputation does not appear to protect incumbents against entry in this market. And the information that providers themselves put online, coded from 2,702 websites, does not follow the choice set at all: price display, the marker that Gottschalk, Mimra and Waibel (2020) found to separate well-behaved dentists, is here a policy of national brands, flat across competition bands among independents, and unrewarded by ratings.

The paper is descriptive and says so. The number of competitors within 10 km is not exogenous; it is largely a measure of urban density, and although population and income are controlled, unobserved local factors are not. Reviews are self-selected and, for chains, solicited. A Google rating measures reported satisfaction, not the appropriateness of the treatment, which is precisely the dimension the credence-goods problem hides; a satisfied patient may have been over-fitted. Section 7 lists these limits. What the paper offers is the field counterpart of a laboratory result: the variable the experiment held constant is the one that, in the market, governs the mechanism.

The paper relates to three strands of work. It follows the credence goods literature on institutions that mitigate expert opportunism, from the theory of Dulleck and Kerschbamer (2006) and the experiments of Dulleck, Kerschbamer and Sutter (2011) to the review by Balafoutas and Kerschbamer (2020), and in particular the experimental result of Mimra, Rasch and Waibel (2016) that price competition undermines reputation building. It adds field evidence to the small literature on online ratings in expert markets, where Kerschbamer, Neururer and Sutter (2023) find in a field experiment on computer repair that better-rated shops charge lower prices, and where systematic reviews find at best a weak relationship between physician ratings and clinical outcomes (Hong et al., 2019; Saifee et al., 2020). And it builds on the field experiment of Gottschalk, Mimra and Waibel (2020), who sent a test patient to 180 Zurich dentists and found that overtreatment recommendations were unrelated to the density of dentists but strongly related to a dentist's spare capacity, and that patients of lower socio-economic status were overtreated more. Their density result concerned a canton where the minimum was zero competitors within 500 metres; the present data extend the range to markets where the nearest competitor is tens of kilometres away.

# The market

Hearing aids in France are dispensed by *audioprothésistes*, a regulated profession that requires a state diploma and a medical prescription for each fitting. The practitioner performs the audiometric assessment, selects and programmes the device, sells it, and provides follow-up adjustments over the life of the device. The patient is on average old, often hard of hearing in ways that impair the very conversation in which the sale is made, and rarely in a position to compare alternatives. Since 2021 a reform known as *100 % Santé* has made a defined class of devices (class I) available without out-of-pocket cost, while class II devices retain a residual charge. The companion study documents the consequences for supply: the number of registered activities rose from 6,682 in 2022 to 11,018 in August 2026, an increase that the study treats as an upper bound on real growth because the two vintages come from different registers and count activities rather than full-time practitioners, but whose direction is not in doubt.

Supply is organised in three ways. National chains and brand networks (Amplifon, Audika, Audition Santé, Audilab, Audition Conseil, Sonance and others, together with the hearing-aid corners of optical chains such as Optical Center, Krys and Alain Afflelou) account for 3,816 of the 8,481 sites in the register. Mutualist networks (Écouter Voir, VYV3 and regional *mutualités*) account for 525. The remaining 4,140 sites are independents or small regional groups. The distinction matters for the reputation mechanism in two ways. Chains run centralised marketing, including the systematic solicitation of Google reviews after each visit, so that review volume partly reflects policy rather than patient flow. And the practitioner in a chain is usually a salaried employee, whereas the independent is the residual claimant of the sale, the distinction that Gottschalk, Mimra and Waibel (2020) found to matter for overtreatment.

Geography completes the picture. The companion study computes, for every commune, a two-step floating catchment area measure of potential accessibility (APL) with demand restricted to residents aged 65 and over and distance bands of 10, 20 and 30 km. It finds that 560 towns of more than 5,000 inhabitants have no practitioner, that most of them lie within a few kilometres of a served town, but that a residual set of communes, concentrated overseas and in rural areas with old and poor populations, has no practitioner within reach at all. This paper uses the finer of the two facts: for a given centre, how many other centres a patient could reach within 10 km.

# Data

## The site layer

The public extraction of the RPPS (*Répertoire partagé des professionnels de santé*, August 2026 vintage, 2.28 million activity rows) lists each practitioner's activities with the identifier, legal name, trade name and address of the site. Filtering on the profession label and deduplicating on the site identifier yields 8,481 sites at which at least one *audioprothésiste* is registered. Sixty of them are hospitals, dental centres, institutes for the hearing-impaired and similar structures where audiologists are employed but no retail activity takes place; they are excluded, leaving 8,421 retail sites in the "medical devices" sector. Each site carries the number of registered practitioners (1.3 on average, 1 at the median), their employment status, and a classification by trade name and legal name into national chain, mutualist network or independent. The classification is keyword-based; the legal names of the largest chains (SOGECA for Audika, Sonova for Audition Santé, Amplifon France) are mapped to their brands. Sites hosted in an optician's shop are flagged separately, because their Google listing is the shop's.

Sites are located at the centroid of their commune, using the coordinates of the companion study; the arrondissements of Paris, Lyon and Marseille, which that study left without coordinates, are attached to their own centroids from the national administrative gazetteer. Each site inherits the commune's population (2023), share of residents aged 65 and over (2022 census), median income per consumption unit (2023), and APL, and receives three competition measures: the number of other retail sites within 10, 20 and 30 km of great-circle distance between centroids, the number of *distinct* alternatives within 10 km (a chain's several sites counting once, each independent counting once), and the distance to the nearest other site.

The 10 km radius is the one that discriminates. Within 30 km, about 90 % of sites in France have ten or more competitors, so the radius that the companion study uses for accessibility says little about local choice. Within 10 km, 291 sites have no competitor, 754 have one or two, 1,903 have three to nine and 5,473 have ten or more. Counting distinct alternatives rather than sites moves 63 sampled sites across bands and changes no result; chains rarely place two sites within 10 km of each other without an independent in between.

## Sample and weights

Collecting ratings for every site would have cost about four times more than the design below for no gain in precision where it matters. The sample takes every retail site with zero to two competitors within 10 km (1,045 sites) and a random draw, proportional by site type, from the two remaining bands, for a total of 2,999 sites. Sampling weights, equal to 1 in the exhaustive strata and about 3.8 in the others, restore national proportions in every table and figure. The order of collection was randomised so that any interruption would leave a balanced sub-sample.

## Google ratings

Ratings were collected on 3 September 2026 through the Google Places API (New), in two calls per site: a text search on the site's name and address, biased towards the commune centroid, returning only a place identifier, and a place-details call returning the display name, address, coordinates, rating, number of reviews, website, business status and place type. A match was accepted when the returned location lay within 10 km of the commune centroid, the place type was compatible with a retail centre, and the name matched on at least one significant word or the type was unambiguously a store. The 225 doubtful matches were re-queried with the brand name followed by *audioprothésiste* and the commune. In the end 2,997 sites had a listing and 2,966 (98.9 %) a validated match; 2,768 of these (93.3 %) carried at least one review. The Places terms of service do not allow site-level ratings to be redistributed; the aggregated tables and the site layer without Google fields are published with the code, and the collection can be re-run by anyone with an API key in about an hour.

## Website content

For each matched site with a website in its Google listing (2,778 sites, 640 distinct domains), the page referenced by the listing was read, together with the domain's home page and up to three internal pages whose address or link text refers to prices, the *100 % Santé* scheme or a free trial. The text was coded automatically for the presence of the provider's own displayed prices (an amount between 100 and 20,000 euros in a price context, excluding reimbursement explanations, regulatory amounts and quoted customer reviews), a page dedicated to prices, a mention of the fully reimbursed class I devices, a free trial, a free hearing test, online appointment booking, a quote, and guarantee or follow-up terms. Chain websites are national, so for chains these variables describe the brand; for independents they describe the centre. In all, 2,702 sites (91 % of matched sites) have a readable website.

# Empirical approach and hypotheses

The analysis is descriptive throughout: weighted means and medians by competition band with bootstrap intervals, weighted least squares with heteroskedasticity-robust standard errors, and, for the chain-versus-independent comparison, commune fixed effects with standard errors clustered by commune. The competition band is the number of other retail sites within 10 km, in four classes: none, one to two, three to nine, ten or more. Controls are the log of commune population, median income (or its terciles), site type, and the optician-shop flag.

The laboratory results of Angerer et al. (2026) suggest what to look for. In their markets, ratings work because (i) consumers rate almost every interaction (95 %), (ii) the rating reflects the outcome the consumer can observe, from zero stars after detected undertreatment to five after a good experience, and (iii) consumers then choose the best-rated expert. Translated to a field market where the choice set varies, this yields four expectations. Rating activity, the share of sites rated and the number of reviews per site, should increase with the number of alternatives, since the act of rating is part of a choice process that has no object when there is nothing to choose between (H1). The level of ratings should be high everywhere, because the outcomes a hearing-aid patient can observe (was I received well, does the device work) are those of a good experience, and the outcomes that would trigger a low rating (was I sold a device I did not need, at a price I need not have paid) are exactly those the credence good hides (H2). If ratings carry any information about providers, their dispersion across providers should be larger where consumers compare providers, either because comparison makes ratings more discriminating or because more heterogeneous providers survive in denser markets (H3). And chains, which solicit reviews, should show higher rating activity than independents at any level of competition, including within the same commune (H4).

# Results

## Coverage

Table 1 gives the coverage figures by competition band. A Google listing exists for 99.7 % of the sites without competitors and for practically all others; validated matches range from 96.2 % to 99.6 %. Among matched sites, the share with at least one review rises from 87.5 % under local monopoly to 94.8 % under dense competition. Coverage of the reputation mechanism, in the sense of the existence of a public score, is therefore near-universal in this market, in contrast to the Zurich dental market of 2016 where most practices had no online rating at all.

Table 1. Coverage and rating activity by local competition (weighted).

| Competitors within 10 km | Sites | Google listing | Validated match | ≥ 1 review | Median reviews | Mean reviews | Website |
|---|---|---|---|---|---|---|---|
| 0 | 291 | 99.7 % | 96.2 % | 87.5 % | 9 | 20.6 | 92.1 % |
| 1–2 | 754 | 100 % | 98.9 % | 92.6 % | 16 | 33.9 | 94.6 % |
| 3–9 | 504 | 100 % | 99.6 % | 93.4 % | 25 | 69.1 | 95.0 % |
| 10+ | 1,450 | 99.9 % | 99.2 % | 94.8 % | 34 | 97.4 | 93.0 % |

## Rating activity follows the choice set

Figure 1 shows the first result. The median number of reviews rises from 9 with no competitor to 16, 25 and 34 across the bands (panel A), and the share of sites with at least one review from 87.5 % to 94.8 % (panel B). Both gradients are present within national chains and within independents, with chains above independents throughout. A Kruskal-Wallis test rejects equality of review counts across bands at any conventional level.

![Review activity by local competition. Weighted medians and shares with 95 % bootstrap intervals. Mutualist networks are included in "all sites" only.](fig1_review_activity.png)

Table 2 reports the regression counterpart. In a weighted regression of log(1 + reviews) on the competition bands, site type, log population, median income and the optician flag, the band coefficients are 0.32, 0.57 and 0.68 relative to sites with no competitor, all significant at the 1 % level; the gradient is thus not an artefact of city size, although log population adds 0.16 per log point on its own. Independents have 17 % fewer reviews than chains and optician-hosted sites three times more, the latter because their listing is the shop's. The probability of having at least one review follows the same pattern, with band effects of four to six points. Replacing the count of sites by the count of distinct alternatives leaves every coefficient within a hundredth of its value.

Table 2. Rating activity and content: weighted least squares.

| | log(1 + reviews) | ≥ 1 review | Rating (if ≥ 1 review) |
|---|---|---|---|
| 1–2 competitors | 0.318 (0.097)*** | 0.046 (0.022)** | −0.046 (0.033) |
| 3–9 competitors | 0.566 (0.114)*** | 0.052 (0.024)** | −0.005 (0.031) |
| 10+ competitors | 0.678 (0.125)*** | 0.061 (0.023)*** | −0.032 (0.034) |
| Mutualist network | 0.010 (0.107) | −0.009 (0.016) | 0.013 (0.034) |
| Independent | −0.187 (0.062)*** | −0.063 (0.010)*** | 0.069 (0.016)*** |
| log population | 0.162 (0.033)*** | 0.001 (0.005) | −0.006 (0.007) |
| Median income (k€) | 0.018 (0.007)*** | 0.003 (0.001)*** | 0.003 (0.002) |
| Optician-hosted | 1.092 (0.115)*** | −0.017 (0.014) | −0.059 (0.022)*** |
| Observations | 2,814 | 2,814 | 2,625 |
| R² | 0.118 | 0.023 | 0.020 |

*Reference: sites with no competitor within 10 km, national chain. Sampling weights; HC1 standard errors in parentheses. \*\*\* p < 0.01, \*\* p < 0.05.*

## Rating content does not

The third column of Table 2 and panel A of Figure 2 show the second result. The mean rating among rated sites is 4.82, 4.76, 4.79 and 4.77 across the four bands; no band coefficient is distinguishable from zero, and the point estimates are negative. The only systematic differences are by type: independents are rated 0.07 higher than chains, optician-hosted sites 0.06 lower. The level is worth pausing on. In the laboratory of Angerer et al. (2026), the predicted rating after an interaction the consumer can identify as good is 4.76 stars, and 89.8 % of such interactions receive five stars. The French hearing-aid market rates at 4.77 on average. On the face of it, patients report the experience of consumers who have received the appropriate treatment at the appropriate price; the laboratory's other cases, the zero stars after detected undertreatment and the dispersed three stars after a possibly overcharged outcome, require an observation the hearing-aid patient does not have.

![Rating content by local competition. A: weighted mean rating among sites with at least one review. B: weighted standard deviation of ratings across sites with 30 or more reviews. 95 % bootstrap intervals.](fig2_rating_content.png)

The share of perfect scores deserves a caveat. Exactly 5.0 is the rating of 50.6 % of rated sites with no competitor and of 34.9 % of those with ten or more, and of 48 % of independents against 23 % of chains. Almost all of this is a review-count effect: a site with three reviews is far more likely to sit at 5.0 than a site with eighty. Conditional on the log of the review count, the band coefficients in a regression of the perfect-score indicator are zero (Table A1), and among sites with at least ten reviews the shares are 33.6 % and 28.8 %. The excess of perfect scores where competition is absent is the thinness of the signal, not its content.

## Dispersion follows the choice set

What does vary with competition is the spread of ratings across providers (Figure 2, panel B). Among sites with at least thirty reviews, the number at which a Google rating stabilises, the weighted standard deviation of ratings across sites is 0.15 with no competitor, 0.14 with one or two, 0.24 with three to nine and 0.27 with ten or more. The share of such sites rated below 4.5 goes from 3.5 % to 8.3 %. Both patterns appear within chains and within independents. A rating system that produces 4.9 for everyone conveys nothing about anyone; the market where the system discriminates between providers is the market where providers can be chosen between. The data cannot say whether this is because comparison shoppers write more discriminating reviews, because heterogeneous providers coexist only where there is room for them, or simply because larger review counts reveal a dispersion that small counts hide; the third mechanism is partly addressed by the thirty-review threshold, the first two are not separable here.

## Chains and independents in the same market

The chain-versus-independent differences in Table 2 could reflect where chains locate rather than what they do. Table 3 restricts the comparison to the 406 sampled communes in which at least one chain site and one independent site were both matched, and adds commune fixed effects, so that the comparison is between neighbours in the same local market. The differences survive: the independent has 18 % fewer reviews (p = 0.08), is four points less likely to have any review (p = 0.02), is rated 0.07 higher (p = 0.04), and is eleven points less likely to have a website on its listing (p < 0.001). Sites with more registered practitioners have more reviews (0.17 log points per additional practitioner), which is the patient-flow component of review volume; the chain premium is what remains once it is controlled.

Table 3. Chains versus independents within the same commune (commune fixed effects, 406 communes, 1,240 sites).

| Dependent variable | Independent | Optician-hosted | Practitioners on site | N |
|---|---|---|---|---|
| log(1 + reviews) | −0.198 (0.112)* | 1.041 (0.135)*** | 0.171 (0.077)** | 1,240 |
| ≥ 1 review | −0.040 (0.018)** | 0.004 (0.032) | 0.017 (0.014) | 1,240 |
| Rating (if ≥ 1 review) | 0.066 (0.032)** | −0.046 (0.057) | −0.061 (0.034)* | 1,164 |
| Website on listing | −0.112 (0.019)*** | 0.034 (0.025) | 0.015 (0.016) | 1,240 |

*Weighted least squares with commune fixed effects; standard errors clustered by commune. \*\*\* p < 0.01, \*\* p < 0.05, \* p < 0.10.*

The reading is that review volume in this market is, to a substantial degree, a supply-side choice. Chains solicit reviews as a matter of policy; independents do so unevenly. The higher rating of independents, 0.07 on a scale where everyone sits above 4.7, is consistent with the smaller and more self-selected set of patients who review them, and possibly with a closer relationship; the data cannot distinguish the two.

## Income

Gottschalk, Mimra and Waibel (2020) found that the patient of lower socio-economic status was the one most likely to receive an unnecessary treatment recommendation, and closed on the possibility of supply-side effects in the socio-economic gradient of health. If the rating system is the patient's instrument, one may ask whether it is thinner where the patient is more exposed. It is, but only mildly. Table 4 and Figure 3 cross the competition band with terciles of the commune's median income. Within each band the differences across terciles are small and not always monotonic; in the regression with all controls, the top tercile has about 15 % more reviews than the bottom (0.14 log points, p = 0.08), two points more sites with any review (p = 0.07) and a rating higher by 0.04 (p = 0.08). The thinnest signal in the country is that of the poorest communes without a competitor: 8 reviews at the median and 87 % of sites rated. The result is modest and is reported as such; what it rules out is a rating system that compensates, by being more active where patients have less choice and less income.

Table 4. Rating activity by local competition and commune income tercile (weighted).

| Competitors within 10 km | Income tercile | Sites | ≥ 1 review | Median reviews | Mean rating |
|---|---|---|---|---|---|
| 0 | bottom | 132 | 87.1 % | 8 | 4.85 |
| 0 | middle | 114 | 86.8 % | 10 | 4.76 |
| 0 | top | 34 | 91.2 % | 9 | 4.86 |
| 1–2 | bottom | 322 | 90.1 % | 15 | 4.72 |
| 1–2 | middle | 260 | 95.8 % | 17 | 4.79 |
| 1–2 | top | 164 | 92.7 % | 15 | 4.81 |
| 3–9 | bottom | 228 | 91.2 % | 23 | 4.78 |
| 3–9 | middle | 163 | 95.7 % | 30 | 4.79 |
| 3–9 | top | 111 | 94.6 % | 26 | 4.80 |
| 10+ | bottom | 390 | 94.6 % | 36 | 4.74 |
| 10+ | middle | 475 | 93.9 % | 34 | 4.75 |
| 10+ | top | 573 | 95.6 % | 31 | 4.79 |

*Tercile cut-offs at 23,750 and 26,100 euros of median income per consumption unit.*

![Review activity by local competition and commune income tercile. Weighted medians and shares with 95 % bootstrap intervals.](fig3_income_gradient.png)

## Entrants

The companion study identifies 295 towns of more than 5,000 inhabitants that had no practitioner in 2022 and at least one in 2026. Sites located in communes that had no registered practitioner in 2022, 456 in the sample, are entrants on a previously empty market. Unconditionally they have fewer reviews than incumbents (13 against 24 at the median for independents, 22 against 33 for chains), which is what four years or less of existence implies. Conditional on the competition band and the controls, the difference is 9 % and insignificant (p = 0.37), and there is no difference in the probability of being rated or in the rating level. Entrants reach the rating activity of incumbents within the period; in this market, online reputation does not appear to be a barrier that protects the installed provider.

## Website content

The website is the other information device that Gottschalk, Mimra and Waibel (2020) observed, and the one on which they found the sharpest type marker: dentists who displayed their price level as the law required recommended far less unnecessary treatment. Table 5 reports what French hearing-aid centres display. A website is listed on 99 % of chain sites, 97 % of mutualist sites and 88 % of independents. Price transparency is a chain policy: 27.5 % of chain sites belong to a brand whose website displays its own prices and 53.7 % to a brand with a page dedicated to prices, against 5.3 % and 11.4 % of independents; mutualist sites, whose listings point to a network directory, display neither. Mentions of the fully reimbursed class I devices (85 % of chains, 64 % of independents), of a free trial (92 % against 55 %) and of online booking (98 % against 79 %) follow the same ordering.

Table 5. Website content by site type (weighted; content variables conditional on a readable website).

| | National chains | Mutualist networks | Independents |
|---|---|---|---|
| Website listed on Google | 99.3 % | 96.5 % | 87.9 % |
| Own prices displayed | 27.5 % | 0.8 % | 5.3 % |
| Page dedicated to prices | 53.7 % | 0.8 % | 11.4 % |
| Mentions fully reimbursed class I | 85.0 % | 7.4 % | 63.6 % |
| Free trial | 92.4 % | 93.6 % | 54.8 % |
| Free hearing test | 93.1 % | 78.9 % | 58.9 % |
| Online booking | 97.6 % | 93.6 % | 79.3 % |
| Sites with readable website | 1,318 | 164 | 1,220 |

For the question of this paper, the relevant test is on independents, whose websites are their own. Figure 4 shows their content by competition band. Nothing moves. Own prices are displayed by 4.3 % of independents without a competitor and 6.0 % of those with ten or more; the class I mention, the free trial and online booking are flat within sampling error; in regressions with population, income and staff controls, no band coefficient is significant for any of the six content variables (Table A4). The information that a provider chooses to put on its own website does not follow the local choice set, in contrast to the rating activity of its patients.

![Website content of independent centres by local competition. Weighted shares with 95 % bootstrap intervals, independents with a readable website (n = 1,220).](fig4_websites_independents.png)

Nor does price transparency relate to rating activity. Across all readable sites, with competition, type and controls held constant, displaying one's own prices is unrelated to the number of reviews (+0.05 log points, p = 0.51) and associated with a rating lower by 0.04 (p = 0.02); a page dedicated to prices is likewise unrelated to review counts and associated with a rating lower by 0.05. The marker that separated well-behaved dentists in Zurich is, in this market, a feature of national brands, and it does not earn them better ratings.

# Interpretation

The results fit a simple reading of the reputation mechanism in the field. In the laboratory, a public rating system works through a chain of three links: consumers rate, ratings reflect outcomes, and consumers choose on ratings. The third link is what gives the first two their force; an expert who cannot lose a consumer has no reason to fear a rating. The field data show the first link scaling with the third: where patients can choose among many providers, nearly every provider is rated and the median provider has dozens of reviews; where the patient has no alternative within 10 km, one provider in eight has no rating and the median has nine. The second link, in contrast, is close to inert. Ratings sit at the top of the scale everywhere, at the level the laboratory associates with an outcome the consumer has verified to be good, and they do not move with competition. This is what one expects in a credence good: the outcomes that would generate a low rating are the ones the patient cannot see.

What competition does change is the dispersion of ratings across providers. In dense markets the rating system, though anchored near the ceiling, separates providers; in captive markets it does not. Whether this is because comparison produces more informative reviews or because heterogeneous providers coexist only where consumers can sort between them, the practical consequence is the same. The disciplining value of a rating system, in the sense of Angerer et al. (2026), is available where the exit option is, and thin where it is not. The gradient is not compensating: the patients with the least choice, in the poorest communes without a competitor, face the thinnest signal.

The transparency devices on the provider's side behave differently. Price display and the mention of the fully reimbursed devices are decided at brand level for chains and vary little among independents; neither follows the choice set, and neither is rewarded by patients' ratings. In the Zurich dental market, price display marked a type of dentist; in the French hearing-aid market it marks a type of firm.

The supply side reinforces the point. Chains treat reviews as a marketing instrument and accumulate them regardless of local competition; within a given commune they out-review the independent next door. To the extent that review volume signals reputation to a patient, the signal is partly manufactured by the provider with the larger marketing budget, and it does not distinguish, at 4.7 versus 4.8, the salaried practitioner from the residual claimant whose incentives Gottschalk, Mimra and Waibel (2020) found to matter.

None of this shows that ratings are useless in this market, or that providers in captive markets behave worse. It shows that the observable part of the rating system, its activity and its informativeness, tracks the option to switch, and that its content is not informative about the dimension that defines the credence good. The laboratory establishes that ratings discipline when there is choice; the field shows how much of the rating system disappears when choice does.

# Limitations

The competition measure is not exogenous. The number of centres within 10 km is largely a function of urban density, and although population and income are controlled and the chain-versus-independent comparison is made within communes, the competition gradient itself is a comparison across places that differ in unobserved ways: demographics, mobility, the digital habits of older patients. The paper makes no causal claim.

Reviews are self-selected, and for chains solicited. The number of reviews is a measure of rating activity, not of patient flow; the regressions control for the number of practitioners on site, but not for turnover. The rating is a measure of reported satisfaction, not of the appropriateness of the treatment, which no observational dataset in this market contains; that gap is the credence-good problem, and the paper documents its footprint rather than filling it.

Google is one platform. Its dominance in France makes it the natural first choice, but a patient who reads other platforms, or none, is not observed. Distances are straight lines between commune centroids, which understates the isolation of enclosed communes and treats every site in a commune as located at its centre; for the three largest cities, sites are located at the arrondissement centroid. The sample over-represents low-competition sites by design and is re-weighted; the exhaustive strata are the ones that matter for the results, and the sampled strata are large.

Finally, the classification of sites into chains, mutualist networks and independents is keyword-based on the register's trade and legal names. It is accurate for the large chains and mutualist groups and approximate for small regional groups, which are counted as independents.

# Conclusion

A public rating system in a credence goods market rests on the consumer's option to leave. This paper observes such a system across the full range of that option, from hearing-aid centres that are the only one within 10 km to centres with dozens of competitors, and finds that its activity and its informativeness follow the option while its content does not. Ratings are near the ceiling everywhere, at the level that laboratory subjects give after a verified good experience; they are thin and compressed where the patient has nowhere else to go, and thick and dispersed where he has. Chains manufacture part of the signal; entrants catch up with incumbents within a few years; the poorest captive markets have the thinnest signal of all.

The provider's own information devices tell a complementary story. Price display, the marker that separated well-behaved dentists in the Zurich field experiment, is in this market a policy of national brands, present on a quarter of chain listings and one independent in twenty; it does not vary with local competition, and it does not earn better ratings. Whatever transparency the patient finds online is, for the most part, the brand's.

The natural experiment that the companion study documents, the entry of several thousand centres between 2022 and 2026 into a market whose reimbursement rules had just changed, offers the next step: observing the rating system of a provider from its first review onwards, and asking whether the arrival of a competitor changes what the incumbent's patients say.

# References

Angerer, S., Glätzle-Rützler, D., Mimra, W., Rittmannsberger, T. and Waibel, C. (2026). The value of rating systems in credence goods markets. *The Economic Journal*, advance access, doi:10.1093/ej/ueag011.

Balafoutas, L. and Kerschbamer, R. (2020). Credence goods in the literature: What the past fifteen years have taught us about fraud, incentives, and the role of institutions. *Journal of Behavioral and Experimental Finance*, 26, 100285.

Darby, M. R. and Karni, E. (1973). Free competition and the optimal amount of fraud. *The Journal of Law and Economics*, 16(1), 67–88.

Dulleck, U. and Kerschbamer, R. (2006). On doctors, mechanics, and computer specialists: The economics of credence goods. *Journal of Economic Literature*, 44(1), 5–42.

Dulleck, U., Kerschbamer, R. and Sutter, M. (2011). The economics of credence goods: An experiment on the role of liability, verifiability, reputation, and competition. *American Economic Review*, 101(2), 526–555.

Gottschalk, F., Mimra, W. and Waibel, C. (2020). Health services as credence goods: A field experiment. *The Economic Journal*, 130(629), 1346–1383.

Hong, Y. A., Liang, C., Radcliff, T. A., Wigfall, L. T. and Street, R. L. (2019). What do patients say about doctors online? A systematic review of studies on patient online reviews. *Journal of Medical Internet Research*, 21(4), e12521.

Kerschbamer, R., Neururer, D. and Sutter, M. (2023). Credence goods markets, online information and repair prices: A natural field experiment. *Journal of Public Economics*, 222, 104891.

Mimra, W., Rasch, A. and Waibel, C. (2016). Price competition and reputation in credence goods markets: Experimental evidence. *Games and Economic Behavior*, 100, 337–352.

Saifee, D. H., Zheng, Z., Bardhan, I. R. and Lahiri, A. (2020). Are online reviews of physicians reliable indicators of clinical outcomes? A focus on chronic disease management. *Information Systems Research*, 31(4), 1282–1300.

Soussan, N. (2026). *L'accessibilité de l'audioprothèse en France : mesure communale de l'accès et de l'opportunité d'implantation, confrontée à la dynamique du marché 2022–2026*. Version 2.0, doi:10.5281/zenodo.22177322.

# Appendix

Table A1. Perfect scores and review counts (weighted least squares, dependent variable: rating equals 5.0, sites with at least one review).

| | Coefficient | S.E. |
|---|---|---|
| 1–2 competitors | −0.027 | 0.034 |
| 3–9 competitors | −0.020 | 0.037 |
| 10+ competitors | 0.048 | 0.037 |
| Independent | 0.236*** | 0.021 |
| Mutualist network | 0.060 | 0.040 |
| log(reviews) | −0.113*** | 0.006 |
| log population | −0.029*** | 0.009 |
| Optician-hosted | 0.116*** | 0.026 |
| Observations | 2,768 | |
| R² | 0.180 | |

Table A2. Distribution of ratings by competition band and minimum review count (weighted).

| Minimum reviews | Competitors | Sites | Rated 5.0 | Mean rating | S.D. across sites | Rated below 4.5 |
|---|---|---|---|---|---|---|
| 1 | 0 | 245 | 50.6 % | 4.82 | 0.41 | 9.8 % |
| 1 | 1–2 | 691 | 40.1 % | 4.76 | 0.51 | 10.1 % |
| 1 | 3–9 | 469 | 32.2 % | 4.79 | 0.27 | 10.0 % |
| 1 | 10+ | 1,363 | 34.9 % | 4.77 | 0.38 | 11.0 % |
| 10 | 0 | 140 | 33.6 % | 4.83 | 0.22 | 8.6 % |
| 10 | 1–2 | 470 | 28.3 % | 4.82 | 0.22 | 7.0 % |
| 10 | 3–9 | 379 | 24.8 % | 4.77 | 0.25 | 9.8 % |
| 10 | 10+ | 1,139 | 28.8 % | 4.77 | 0.29 | 10.0 % |
| 30 | 0 | 57 | 33.3 % | 4.88 | 0.15 | 3.5 % |
| 30 | 1–2 | 226 | 26.5 % | 4.87 | 0.14 | 1.3 % |
| 30 | 3–9 | 232 | 21.6 % | 4.77 | 0.24 | 10.3 % |
| 30 | 10+ | 767 | 25.0 % | 4.78 | 0.27 | 8.3 % |

Table A3. Sample design.

| Competitors within 10 km | Site type | Population | Sample | Weight |
|---|---|---|---|---|
| 0 | national chain | 105 | 105 | 1.00 |
| 0 | independent | 177 | 177 | 1.00 |
| 0 | mutualist | 9 | 9 | 1.00 |
| 1–2 | national chain | 348 | 348 | 1.00 |
| 1–2 | independent | 364 | 364 | 1.00 |
| 1–2 | mutualist | 42 | 42 | 1.00 |
| 3–9 | national chain | 943 | 250 | 3.77 |
| 3–9 | independent | 789 | 209 | 3.78 |
| 3–9 | mutualist | 171 | 45 | 3.80 |
| 10+ | national chain | 2,419 | 641 | 3.77 |
| 10+ | independent | 2,763 | 732 | 3.77 |
| 10+ | mutualist | 291 | 77 | 3.78 |

Table A4. Website content of independents and local competition (weighted least squares, independents with a readable website, n = 1,220; controls: log population, median income, practitioners on site).

| Dependent variable | 1–2 competitors | 3–9 competitors | 10+ competitors |
|---|---|---|---|
| Own prices displayed | −0.014 (p = 0.49) | 0.010 (p = 0.69) | 0.034 (p = 0.24) |
| Page dedicated to prices | −0.015 (p = 0.58) | 0.061 (p = 0.09) | 0.046 (p = 0.22) |
| Mentions class I | −0.008 (p = 0.87) | 0.035 (p = 0.54) | 0.035 (p = 0.55) |
| Free trial | −0.078 (p = 0.13) | −0.014 (p = 0.81) | −0.036 (p = 0.54) |
| Free hearing test | −0.060 (p = 0.24) | 0.006 (p = 0.91) | −0.066 (p = 0.26) |
| Online booking | −0.024 (p = 0.57) | 0.003 (p = 0.95) | 0.039 (p = 0.41) |

*Reference: independents with no competitor within 10 km. HC1 standard errors.*

Data and code: github.com/Nsoussan/deserts-audioprothese, directory `ratings/`. Site-level Google data are not redistributed.
