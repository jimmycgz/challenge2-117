# Equity audit

Navigation: [agent README](README.md) for the design; [equity_audit.py](equity_audit.py) produced every number
here; [API.md](API.md) for the response shape.

The challenge asks: **did the food go where the need is, or where the loading docks are?** The answer depends on how
the matches are counted, so this page counts them three ways and says what each one can and cannot show.

## Method

1. Run the matcher (wide semantic search, then the hard filters, then ranking; no language model) over the ten
   postings in the `surplus_postings` table. The Chicago corpus has 192 rows: 183 real organizations and nine invented
   teaching cases that the challenge plants (no street or ZIP, coordinates placed by formula at the metro centre). The
   audit leaves the nine out of the corpus and out of the matches, so it describes 183 recipients.
2. For each top match, find the census tract whose internal point is nearest the recipient's ZIP-level location. That
   is often not the tract the building is in, so read the figures as the surrounding area.
3. Compare poverty rate, share of households without a vehicle and share on food or cash assistance (ACS, from the
   `tract_demographics` table) across: the metro; every recipient in the corpus; the recipients with a loading dock
   or room for 5 or more pallets against the rest; and the top matches.

The metro row weights each tract by its population; every other row is a plain mean or median per recipient or per
posting. The baselines therefore differ in kind: the metro row asks where people live, the recipient rows ask where
recipients are. Race and ethnicity are not in the data and are not used. The matcher never uses tract figures to
rank; they are looked up after the match.

Inputs that are estimates, all visible in the output below:

- The nine invented teaching cases are excluded (Greenline Community Pantry, Harborview Neighbors Trust, Cedar Street Produce
  Alliance, Maple Street Produce Alliance, Ridgeway Avenue Food Ministry, Southline Neighbors Pantry, Third Ward Community
  Table, Brookfield Family Resource Center, Lakeshore Mutual Aid Collective). The first version of this page included them:
  one of them, Cedar Street Produce Alliance, was posting 3's top match, with tract figures that described the metro
  centre, not a neighborhood. The last section shows both versions.
- The table has no load size, so pallets per posting are guesses (`PALLETS` in `equity_audit.py`).
- Posting 8 (sealed infant formula, 8 months to expiry) has a clock of 1 hour in the table, because the loader took
  FoodKeeper's opened-container figure. The audit uses the posting's own pickup deadline from the table (168 hours, the
  `hours_available` field), which is shorter than the product's 8-month expiry, and prints both. The live agent, given a
  typed posting that states only the expiry, used the 8 months.
- The audit searches with the raw posting text. The deployed agent searches with a rewrite the language model writes,
  so this audits the matcher, not that exact query.

## Results

Per posting. "Posting" is the start of the offer's text, so the products can be checked without the lab tables. "Viable" is
how many of the 80 semantic matches passed the filters; the rest of the row is the top match. The nine invented teaching
cases are left out.

| # | Track | Posting | Table clock (h) | Clock used (h) | Pallets (est.) | Viable | Top match | Cold | Pallets of room | Collects in (h) | Tract poverty | No vehicle | Assistance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | RETAIL | 10 crates of spinach, harvested yesterday, nee | 6.0 | 6.0 | 0.5 | 12 | Shakespear Rose Community Ta | vehicle | 3 | 4 | 45% | 52% | 38% |
| 2 | RETAIL | mixed dairy - about 60 gallons of milk and som | 8.0 | 8.0 | 1 | 23 | Shakespear Rose Community Ta | vehicle | 3 | 4 | 45% | 52% | 38% |
| 3 | RETAIL | roughly 200 loaves of day-old bread and pastri | 24.0 | 24.0 | 2 | 11 | Burrito Brigade Chicago | vehicle | 3 | 8 | 6% | 7% | 6% |
| 4 | RETAIL | prepared sandwiches and salads from the deli c | 4.0 | 4.0 | 0.5 | 6 | Shakespear Rose Community Ta | vehicle | 3 | 4 | 45% | 52% | 38% |
| 5 | FARM | 5 tons of potatoes still in the field, we can  | 72.0 | 72.0 | 5 | 10 | Anso Child Development | walk-in | 7 | 19 | 6% | 7% | 6% |
| 6 | FARM | half a truckload of blueberries, picked this m | 12.0 | 12.0 | 10 | 1 | Dion S Chicago Dream Inc Nfp | walk-in | 11 | 9 | 19% | 18% | 16% |
| 7 | FARM | surplus winter squash, about 30 bins, no refri | 120.0 | 120.0 | 15 | 5 | Feeding America | walk-in | 24 | 28 | 13% | 54% | 0% |
| 8 | ESSENTIALS | 48 cases of sealed infant formula, 8 months to | 1.0 | 168 | 2 | 22 | Chicago Food Rescue | vehicle | 2 | 8 | 7% | 12% | 5% |
| 9 | ESSENTIALS | pallet of diapers and wipes, sizes 1 through 4 | 720.0 | 720.0 | 1 | 46 | Beyond Hunger | walk-in | 22 | 45 | 4% | 23% | 1% |
| 10 | ESSENTIALS | temperature-sensitive nutritional supplements  | 8.0 | 8.0 | 0.5 | 16 | Word Faith Believers Ministr | vehicle | 3 | 5 | 27% | 24% | 46% |

Metro: 1004 tracts in the loaded area. Corpus: 183 recipients on 68 distinct tracts.

| Group | n | Poverty | No vehicle | Assistance |
|---|---|---|---|---|
| Metro, tracts weighted by population | 1004 tracts | 15% | 20% | 18% |
| All recipients, mean | 183 | 19% | 28% | 19% |
| All recipients, median | 183 | 16% | 27% | 12% |
| Recipients with a dock or 5+ pallets, mean | 14 | 17% | 29% | 16% |
| Recipients with a dock or 5+ pallets, median | 14 | 14% | 27% | 14% |
| All other recipients, mean | 169 | 20% | 27% | 20% |
| All other recipients, median | 169 | 16% | 27% | 12% |
| Top matches, once per posting, mean | 10 | 22% | 30% | 19% |
| Top matches, once per posting, median | 10 | 16% | 23% | 11% |
| Top matches, once per distinct recipient, mean | 8 | 16% | 24% | 15% |
| Top matches, once per distinct recipient, median | 8 | 10% | 20% | 6% |
| Top matches, weighted by estimated pallets (37.5 total) | 10 | 14% | 32% | 9% |

Weighted figures are compared with the corpus as means; the medians are in the rows above.

## What the numbers say

- **Counted per posting, the matches are close to the corpus and there is no consistent direction; counted per recipient,
  they sit below it on all three measures.** Per posting, poverty is higher on the mean (22% against 19%) and level on
  the median (16% against 16%); households without a vehicle are higher on the mean (30% against 28%) and lower on the
  median (23% against 27%); assistance is level (mean 19% against 19%, median 11% against 12%). Per distinct recipient
  the means are 16%, 24% and 15% against 19%, 28% and 19%, and the medians 10%, 20% and 6% against 16%, 27% and 12%. One
  recipient (Shakespear Rose Community Table) was ranked first for postings 1, 2 and 4, in a tract with 45% poverty and
  52% of households without a vehicle; counting it three times is what lifts the per-posting means.
- **Weighted by volume, the matches sit in tracts with much less assistance.** The three farm postings are 30 of the
  37.5 estimated pallets. Weighted by pallets, the matches are at 14% poverty, 32% of households without a vehicle and 9% on
  assistance, against a corpus mean of 19% on assistance (corpus median 12%, metro 18%).
- **The loading-dock question has at most a hint of an answer.** Only 14 of the 183 recipients have a dock or room for 5
  or more pallets, and a large load can only go to them. Their tracts have a lower mean poverty (17% against 20% for
  the rest) and assistance (16% against 20%), with a similar share of households without a vehicle (29% against 27%). The medians are about
  level (poverty 14% against 16%, assistance 14% against 12%, no vehicle 27% against 27%). With 14 recipients,
  that is not evidence about the matcher.
- **The effective sample is small.** The 183 recipients sit on 68 distinct tracts, because recipients in one ZIP get the
  same nearest tract. There are ten postings, eight distinct top matches, and no confidence interval. The audit cannot
  tell a real skew from noise.
- **One recipient was ranked first three times.** Shakespear Rose has a refrigerated vehicle, room for 3 pallets and
  collects in 4 hours; the three postings had clocks of 6, 8 and 4 hours, and 12, 23 and 6 recipients passed the
  filters. The ranking tiers the margin, then prefers sturdier cold storage and the recipient's own refrigerated
  transport, then semantic closeness. The output does not show which of those decided it. For posting 4 the margin
  is zero. The matcher keeps no record of who received food recently, so nothing spreads offers across recipients.
  That needs a place to store who received what, and is not built.
- **Some tract figures describe the ZIP point, not the people served.** Posting 7's top match (Feeding America, room
  for 24 pallets) is in a tract with 54% of households without a vehicle and 0% on assistance. The output does not
  show why: it could be missing data or a tract with few households.
- **The filters cannot judge fit beyond what the profile fields say.** Posting 10 (clinic cold-chain supplements,
  half a pallet) went to an organization whose generated profile has a refrigerated vehicle and room for 3 pallets.
  Whether a ministry should receive clinical supplies is a human check, and the agent's instructions say to confirm
  by phone before the truck moves.

## Both versions

The first version of this page included the nine invented teaching cases (192 recipients). It changed one top match
(posting 3: Cedar Street Produce Alliance, an invented case, became Burrito Brigade Chicago) and the group rows below.

| Group | With the nine (192) | Without (183, this page) |
|---|---|---|
| All recipients, mean | 19% / 27% / 20% | 19% / 28% / 19% |
| All recipients, median | 15% / 25% / 12% | 16% / 27% / 12% |
| Top matches per posting, mean | 22% / 31% / 20% | 22% / 30% / 19% |
| Top matches per posting, median | 17% / 23% / 16% | 16% / 23% / 11% |
| Top matches per distinct recipient, mean | 17% / 26% / 16% | 16% / 24% / 15% |
| Top matches per distinct recipient, median | 14% / 20% / 11% | 10% / 20% / 6% |
| Top matches weighted by pallets | 15% / 32% / 9% | 14% / 32% / 9% |
| Recipients with a dock or 5+ pallets, mean | 16% / 27% / 17% (n=17) | 17% / 29% / 16% (n=14) |

Each cell is poverty, no vehicle, assistance.

## Limits

One metro, ten postings, top match only, estimated load sizes, ZIP-level locations, and operational profiles that
were generated, so any pattern in who passes the filters is partly a property of the generator. Nine of the 192 rows
were invented teaching cases and are excluded here. The tract figures are descriptive and carry the survey's own margins
of error. The comparisons above are associations; none shows a cause.
