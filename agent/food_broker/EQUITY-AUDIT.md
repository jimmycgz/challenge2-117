# Equity audit

Navigation: [agent README](README.md) for the design; [equity_audit.py](equity_audit.py) produced every number
here; [API.md](API.md) for the response shape.

The challenge asks: **did the food go where the need is, or where the loading docks are?** The answer depends on how
the matches are counted, so this page counts them three ways and says what each one can and cannot show.

## Method

1. Run the matcher (wide semantic search, then the hard filters, then ranking; no language model) over the ten
   postings in the `surplus_postings` table, Chicago corpus, 192 recipients.
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

- The table has no load size, so pallets per posting are guesses (`PALLETS` in `equity_audit.py`).
- Posting 8 (sealed infant formula, 8 months to expiry) has a clock of 1 hour in the table, because the loader took
  FoodKeeper's opened-container figure. The audit uses the posting's own pickup deadline from the table (168 hours, the
  `hours_available` field), which is shorter than the product's 8-month expiry, and prints both. The live agent, given a
  typed posting that states only the expiry, used the 8 months.
- The audit searches with the raw posting text. The deployed agent searches with a rewrite the language model writes,
  so this audits the matcher, not that exact query.

## Results

Per posting. "Posting" is the start of the offer's text, so the products can be checked without the lab tables. "Viable" is
how many of the 80 semantic matches passed the filters; the rest of the row is the top match.

| # | Track | Posting | Table clock (h) | Clock used (h) | Pallets (est.) | Viable | Top match | Cold | Pallets of room | Collects in (h) | Tract poverty | No vehicle | Assistance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | RETAIL | 10 crates of spinach, harvested yesterday, nee | 6.0 | 6.0 | 0.5 | 12 | Shakespear Rose Community Ta | vehicle | 3 | 4 | 45% | 52% | 38% |
| 2 | RETAIL | mixed dairy - about 60 gallons of milk and som | 8.0 | 8.0 | 1 | 23 | Shakespear Rose Community Ta | vehicle | 3 | 4 | 45% | 52% | 38% |
| 3 | RETAIL | roughly 200 loaves of day-old bread and pastri | 24.0 | 24.0 | 2 | 16 | Cedar Street Produce Allianc | walk-in | 10 | 12 | 14% | 16% | 16% |
| 4 | RETAIL | prepared sandwiches and salads from the deli c | 4.0 | 4.0 | 0.5 | 6 | Shakespear Rose Community Ta | vehicle | 3 | 4 | 45% | 52% | 38% |
| 5 | FARM | 5 tons of potatoes still in the field, we can  | 72.0 | 72.0 | 5 | 13 | Anso Child Development | walk-in | 7 | 19 | 6% | 7% | 6% |
| 6 | FARM | half a truckload of blueberries, picked this m | 12.0 | 12.0 | 10 | 3 | Dion S Chicago Dream Inc Nfp | walk-in | 11 | 9 | 19% | 18% | 16% |
| 7 | FARM | surplus winter squash, about 30 bins, no refri | 120.0 | 120.0 | 15 | 5 | Feeding America | walk-in | 24 | 28 | 13% | 54% | 0% |
| 8 | ESSENTIALS | 48 cases of sealed infant formula, 8 months to | 1.0 | 168 | 2 | 26 | Chicago Food Rescue | vehicle | 2 | 8 | 7% | 12% | 5% |
| 9 | ESSENTIALS | pallet of diapers and wipes, sizes 1 through 4 | 720.0 | 720.0 | 1 | 50 | Beyond Hunger | walk-in | 22 | 45 | 4% | 23% | 1% |
| 10 | ESSENTIALS | temperature-sensitive nutritional supplements  | 8.0 | 8.0 | 0.5 | 16 | Word Faith Believers Ministr | vehicle | 3 | 5 | 27% | 24% | 46% |

Metro: 1004 tracts in the loaded area. Corpus: 192 recipients on 76 distinct tracts.

| Group | n | Poverty | No vehicle | Assistance |
|---|---|---|---|---|
| Metro, tracts weighted by population | 1004 tracts | 15% | 20% | 18% |
| All recipients, mean | 192 | 19% | 27% | 20% |
| All recipients, median | 192 | 15% | 25% | 12% |
| Recipients with a dock or 5+ pallets, mean | 17 | 16% | 27% | 17% |
| Recipients with a dock or 5+ pallets, median | 17 | 13% | 23% | 16% |
| All other recipients, mean | 175 | 20% | 27% | 20% |
| All other recipients, median | 175 | 16% | 25% | 12% |
| Top matches, once per posting, mean | 10 | 22% | 31% | 20% |
| Top matches, once per posting, median | 10 | 17% | 23% | 16% |
| Top matches, once per distinct recipient, mean | 8 | 17% | 26% | 16% |
| Top matches, once per distinct recipient, median | 8 | 14% | 20% | 11% |
| Top matches, weighted by estimated pallets (37.5 total) | 10 | 15% | 32% | 9% |

Weighted figures are compared with the corpus as means; the medians are in the rows above.

## What the numbers say

- **Counted per posting, the matches have more poverty than the corpus and the other two measures are mixed; counted per
  recipient, they sit below the corpus on all three.** Per posting the means are 22%, 31% and 20% against the corpus's
  19%, 27% and 20% (more poverty, fewer cars, assistance level). The medians are 17%, 23% and 16% against 15%, 25% and
  12% (more poverty and assistance, but fewer households without a vehicle, 23% against 25%). One recipient (Shakespear Rose
  Community Table) was ranked first for postings 1, 2 and 4, in a tract with 45% poverty and 52% of households
  without a vehicle. Counting each recipient once, the medians are 14%, 20% and 11%, below the corpus on all three
  measures. The per-posting gap comes from that one recipient.
- **Weighted by volume, the matches sit in tracts with much less assistance.** The three farm postings are 30 of the
  37.5 estimated pallets. Weighted by pallets, the matches are at 15% poverty, 32% on vehicle access and 9% on
  assistance, against a mean of 20% on assistance for the corpus and 18% for the metro (the corpus median is 12%).
- **The loading-dock question has a partial answer.** Only 17 of the 192 recipients have a dock or room for 5 or more
  pallets, and a large load can only go to them. They sit in tracts with somewhat less poverty (mean 16% against 20%
  for the rest) and less assistance (17% against 20%), with the same vehicle access (27%). That is consistent with the
  capacity filter, not the ranking, steering the large loads toward lower-need areas. It is an association in 17
  recipients, not a finding about the matcher.
- **The effective sample is small.** The 192 recipients sit on 76 distinct tracts, because recipients in one ZIP get
  the same nearest tract. There are ten postings, eight distinct top matches, and no confidence interval. The audit
  cannot tell a real skew from noise.
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

## Limits

One metro, ten postings, top match only, estimated load sizes, ZIP-level locations, and operational profiles that
were generated, so any pattern in who passes the filters is partly a property of the generator. The tract figures
are descriptive and carry the survey's own margins of error. The comparisons above are associations; none shows a
cause.
