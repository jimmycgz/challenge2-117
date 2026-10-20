# Design: the food broker as built

Navigation: [test cases](TEST-CASES.md) · [agent README](../agent/food_broker/README.md) · [API](../agent/food_broker/API.md) ·
[equity audit](../agent/food_broker/EQUITY-AUDIT.md) · [captured evidence](evidence/README.md) · the planning
documents this compares against: [high-level design](planning/high-level-design-draft.md),
[product requirements](planning/product-requirements-draft.md), [project plan](planning/project-plan-draft.md).

This describes what is deployed, so the team can agree it, change it through a pull request, or overrule it. Section 8
lists every place it differs from the planning documents, with the reason and a default. Section 9 lists the decisions
that are the team's to make.

## 1. What it does

A coordinator pastes a messy surplus offer. The agent returns a Match Brief with six parts: who and why, what they can
take, the clock and the margin, whose neighborhood it helps, a message ready to send, and the next two options. It
refuses when nobody can take the load, and it keeps a conversation going: "they said no", "why not X", "can they collect
it themselves".

## 2. Architecture

One ADK agent (`food_broker`, Gemini on Vertex AI) with two Python tools, one more for explanations, and Google's managed
BigQuery MCP server. One agent, not several: passing 80 candidate rows between model calls made each call take 76 to 86
seconds, so the rows stay inside one tool.

```text
Coordinator (ADK chat page, or POST /run)
        |
   food_broker agent (Gemini)  -- parses the offer, writes the answer
        |-- lookup_shelf_life ------> BigQuery shelf_life (USDA FoodKeeper)
        |-- find_matches -----------> 1 VECTOR_SEARCH on recipient_embeddings (80 nearest by meaning)
        |                             2 hard filters: cold storage, pallets, collection time vs the clock
        |                             3 rank the survivors
        |                             4 nearest census tract of the top match (tract_demographics)
        |                             5 build the Match Brief (and the rejected list with rank by meaning)
        |-- explain_candidate ------> same search and filters, reports where a named organization came out
        '-- BigQuery MCP (read-only)-> free-form questions about the tables ("how many have a walk-in cooler")
```

The identity guard runs before every agent run, BigQuery client and MCP toolset, and again in `deploy.sh`. It refuses
any credentials that are not the lab's.

## 3. Data (BigQuery dataset `a4i_food`, Chicago)

| Table | Rows | Real or generated |
|---|---|---|
| `recipients` | 192 | Names, addresses, NTEE codes, reported income real (IRS). Storage, capacity, pickup times, profile text generated |
| `recipient_embeddings` | 192 | `profile_text` embedded once with `gemini-embedding-2` (3072 dimensions) |
| `surplus_postings` | 10 | Synthetic offers across three tracks |
| `shelf_life` | 661 | USDA FoodKeeper, consumer guidance |
| `tract_demographics` | 1004 | ACS, no race or ethnicity columns |

## 4. The pipeline inside `find_matches`

1. **Search wide.** `VECTOR_SEARCH`, brute force, 80 nearest recipients by meaning. Each gets its rank by meaning.
2. **Hard filters.** A recipient is removed, with the reason kept, when the food must stay cold and it has no cold storage
   (or only a household fridge for more than one pallet), when its room is below the load, or when its collection time is
   longer than the hours the food has.
3. **Rank.** A comfortable margin (at least 2 hours and a quarter of the clock) first, then sturdier cold storage, then the
   recipient's own refrigerated transport, then closeness by meaning. Tract data is not used to rank.
4. **Neighborhood.** The nearest census tract to the top match's ZIP-level point, for the brief only.
5. **Brief.** Six parts, up to three ranked options, and up to three rejections: the closest by meaning, always including
   one that failed on cold storage when there is one.

Follow-ups: `find_matches` takes `exclude_names`, so after "they said no" the next brief skips everyone who declined.
`explain_candidate` answers "why not X". Questions about a match already given are answered from the earlier brief.

## 5. Why these choices (each is measured)

- **Pool of 80, not 20.** For a 6-hour spinach offer on this corpus, a pool of 15 left 1 viable recipient, 40 left 3, 80
  left 12. The three nearest by meaning were all removed, the nearest one that passes is 11th by meaning, and the ranking's top three sit at 50th, 54th and 63rd
  ([pool study](evidence/pool-study.txt)).
- **One agent.** Latency fell from over 3 minutes to about 13 to 22 seconds.
- **No tract data in the ranking.** The audit then measures the matcher instead of what the ranking was told to favor.
- **Tools never skipped.** Matching a posting always goes through `find_matches`, so the filters cannot be talked around.
  The MCP server answers data questions only.
- **One Cloud Run instance.** ADK keeps sessions in the instance's memory, so a second instance would lose a follow-up.

## 6. Safety and honesty

The agent refuses when nobody is viable and shows the closest rejections. It presents recipient details as the profile
on file and suggests confirming by phone, because storage, capacity and pickup times are generated. It does not repeat
what a profile says about timing, because the generated text and the number can disagree. It warns when a shelf-life
figure is 2 hours or less (the table gave sealed infant formula 1 hour, an opened-container figure) and trusts the donor's
expiry then.

## 7. Deployment

`bash agent/deploy.sh`: Cloud Build builds the Dockerfile in the cloud, Cloud Run serves it (one instance, 8 concurrent
requests, 120-second timeout, minimum one instance so there is no cold start). The service is open to unauthenticated
requests by the team's decision. ADK's chat page is at `/dev-ui/`, the API at `/run` and `/run_sse`.

## 8. Where this differs from the planning documents

| Planning documents say | As built | Why | Default |
|---|---|---|---|
| Top 20 semantic candidates | 80 | A pool of 15 left 1 viable recipient; 80 left 12 | Keep 80 |
| Score = 0.4 meaning + 0.4 no-vehicle rate + 0.2 distance | Margin tier, cold-storage strength, own transport, meaning. No tract data | Keeps the audit independent; tract figures are nearest-to-ZIP and noisy | Keep, see decision D1 |
| `ST_DISTANCE` donor to recipient in the brief | Not built | `surplus_postings` has no donor location | Say so in the limits, see D3 |
| Recipient's `service_days` must include today | Shown in the brief, not enforced | The offer says "hours from now", so the agent does not know the weekday | Keep showing, see D4 |
| Load splitter (US-7) | Not built; refuses when nobody has room | Not enough time to do it safely before the freeze | Keep, see D2 |
| Tools `check_shelf_life`, `find_viable_matches`, `run_equity_audit` | `lookup_shelf_life`, `find_matches`, `explain_candidate`; the audit is an offline script | The audit is analysis, not a coordinator action | Keep |
| "They said no": read runner-up #2 from memory | Search again with `exclude_names` | Works after any number of refusals, and each keeps its rank by meaning | Keep |
| Top 2 rejected decoys | Up to 3, always one cold-storage rejection, with rank by meaning; `explain_candidate` for any named organization | Makes the search's mistakes visible | Keep |
| 7-element brief with distance and a quoted profile | Six parts from the challenge sheet; no distance; profile not quoted for timing | See the limits above | Keep |
| Table `recipients_embedded` | `recipient_embeddings` | Already built and live | Keep, do not rebuild |
| KPI: matches sit above the 20% no-vehicle baseline | Per posting yes (mean 31%, median 23%); per distinct recipient mean 26%, median 20% | One pantry won three postings | Report all counts, see the audit |
| "1 pallet is about 10 to 12 crates" | The model estimates, and varies (ten crates came out at 0.2 to 1 pallet) | Not pinned in the instructions | Pin it, see D5 |
| Exact product name for shelf life | Exact name only, so "spinach" finds nothing (it is listed as "Bagged greens" and "Lettuce") | A bug found while writing the tests | Fix in its own pull request |

## 9. Decisions for the team

| ID | Decision | My recommendation, and what changes |
|---|---|---|
| D1 | Rank by need (no-vehicle rate) or keep tract data out of the ranking? | Keep it out for submission. If wanted, use need only as the last tie-break, say so, and run the audit both ways (issue 13). The challenge brief allows a tie-break on the need profile |
| D2 | Build the load splitter? | No before the freeze. It changes the agent and the demo script says it is not built |
| D3 | Add distance? | Only if the coordinator supplies a donor ZIP; then show miles and use it as a tie-break |
| D4 | Enforce service days? | No: show them. The weekday is not in the offer and the generated days are coarse |
| D5 | Pin the crate-to-pallet conversion? | Yes, in the instructions (one constant, tested), because capacity filtering depends on it |
| D6 | Who deploys, and when does the service freeze? | One person, from `main`, before 16:00; no redeploys after unless broken |

## 10. Known limits

Recipient names and addresses are real; storage, capacity and pickup times are generated. Locations are ZIP-level, so
tract figures describe the surrounding area. Shelf life is consumer guidance. One metro, ten postings. The open service can
run read-only SQL on the project's data. The audit searches with the raw posting text, while the live agent searches with
a rewrite the model writes.
