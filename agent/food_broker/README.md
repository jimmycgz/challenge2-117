# Food broker agent

Navigation: this page is the agent's entry point. Response shape: [API.md](API.md). Audit: [EQUITY-AUDIT.md](EQUITY-AUDIT.md).
Code: [agent.py](agent.py), [tools.py](tools.py), [identity_guard.py](identity_guard.py), [selfcheck.py](selfcheck.py),
[demo_tracks.py](demo_tracks.py), [deploy.sh](../deploy.sh). Challenge brief: [main README](../../README.md).

## The problem

A coordinator gets a surplus offer with hours to live and needs to know who can take it, whether they can collect
before it spoils, and what to send them. One corpus of recipients has to serve all three tracks: small perishable
retail offers, very large farm loads, and essentials such as infant formula. We built for retail and grocer rescue;
the same matcher ran the farm and essentials postings in the equity audit.

## How it works

An ADK agent on Gemini reads the posting (product, amount in pallets, whether it must stay cold, the donor's
deadline) and looks up the USDA FoodKeeper shelf life. The clock is the smaller of the shelf life and the donor's
deadline. Then it calls one tool, `find_matches`, which does the rest in code:

1. **Retrieve wide on meaning.** BigQuery `VECTOR_SEARCH` over `recipient_embeddings`, with the posting embedded
   by `AI.EMBED`. The pool is the 80 nearest recipients by default.
2. **Apply the hard filters.** A recipient is dropped, with the reason kept, when the food must stay cold and it
   has no cold storage (or only a household fridge for more than one pallet), when its `max_pallets` is below the
   load, or when its collection lead time is longer than the hours the food has.
3. **Rank what is left.** A comfortable margin (at least 2 hours and a quarter of the clock) comes first, then
   sturdier cold storage, then the recipient's own refrigerated transport, then semantic distance.
4. **Describe the neighborhood.** The top match's nearest census tract goes into the brief. Tract figures are
   never used to rank.

Follow-ups in the same conversation use two more behaviours. When a recipient says no, the agent calls
`find_matches` again with the names of everyone who declined (`exclude_names`), so the next brief is for the next
viable recipient and each one keeps its original rank by meaning. When someone asks why a named organization was not
chosen, `explain_candidate` re-runs the search and reports that organization's rank by meaning and why it was removed,
or where it ranked among the viable ones. Questions about a match already given (can they collect it themselves, whose
neighborhood) are answered from the earlier brief with no new search.

For questions that are not a posting, such as how many recipients have a walk-in cooler, the agent also uses
Google's managed BigQuery MCP server (`execute_sql`, `get_table_info`, `list_table_ids`), read-only and told which
dataset to stay in. It is on in the deployed service. Matching a posting always goes through `find_matches`, never
through free-form SQL, so the filters cannot be skipped.

### Why a plain top-k search is not enough

Semantic search finds organizations whose profiles read like a good fit. It cannot see whether they have a walk-in
cooler or can collect by tonight, and most close matches fail one of those checks. On the Chicago corpus of 192
recipients, a 6-hour spinach offer left this many viable recipients after the filters:

| Semantic pool (`top_k`) | Viable after the filters |
|---|---|
| 15 | 1 |
| 40 | 3 |
| 80 | 12 |

A pool of 15 leaves one viable recipient and no fallback. Forty is enough to find the best matches (the nearest three viable
recipients are the same at 40 and at 80); 80 is what gives a coordinator nine more to call when the first ones decline.
The closest recipients by meaning are often the wrong ones. For that spinach offer the three nearest were all
removed: two could not collect in time, and Greenline Community Pantry (an invented case in the challenge corpus)
wrote that its families ask for fresh greens and that it has no refrigeration of any kind. The nearest recipient
that passes the filters is 11th by meaning. The three the ranking puts first sit at 50th, 54th and 63rd, because the
ranking prefers sturdier cold storage and a comfortable margin over closeness. That is deliberate: the nearest passing
recipient (Deborahs Place) has a household fridge and one hour of slack, and the agent's picks have two or three hours and,
for the first, a refrigerated vehicle. Closeness by meaning measures how a profile reads, not whether the food arrives
safely, so the ranking spends it last. [pool-study.txt](../../docs/evidence/pool-study.txt)
and [demo-tracks.txt](../../docs/evidence/demo-tracks.txt) show it with each recipient's rank by meaning (searched with the raw
posting text). So the pool is wide and the filters do the narrowing. The challenge brief warns that at least one organization looks
perfect and cannot store the food; the offline selfcheck plants that decoy and fails if it gets through.

### The Match Brief

Six labelled parts, in the challenge sheet's order: who and why; what they can take against this load; the clock
(hours left, collection lead time, margin, whether a driver is needed); whose neighborhood it helps; a draft outreach
message; the next two options. `ranked` holds up to three options and `rejected_but_close` lists close matches the
filters removed, with reasons. When nobody can take the load the six parts are empty and `refusal` says so. Gemini
writes the final answer from this brief and corrects anything in the draft message that does not fit the posting.

### Identity guard

The machine this was built on has default credentials that can belong to a different organization, and falling back
to them would run every query and model call in the wrong cloud. So [identity_guard.py](identity_guard.py) checks
the credentials before each agent run, the first BigQuery client and the MCP toolset. It refuses when:

- `A4I_EXPECTED_PROJECT` or `A4I_EXPECTED_PRINCIPAL_SUFFIX` is not set;
- the credentials resolve to a different project;
- a person's account does not end in the expected suffix;
- a service account is not the project's own address, the project's default compute account, or on
  `A4I_SA_ALLOWLIST`. A service account is judged by its email address, because `GOOGLE_CLOUD_PROJECT` can make
  any credential resolve to the lab project;
- the credentials are impersonated, always, since the account doing the impersonating is not checked.

`deploy.sh` runs the same check first (`python -m food_broker.identity_guard`, which exits 2 on a refusal).

## Speed

When the 80 candidate rows passed through the language model, each model call took 76 to 86 seconds and a full answer
ran past 3 minutes. `find_matches` runs the search, the filters and the brief inside the code, so the rows never
reach the model. A full answer now takes about 22 seconds locally and about 13 on Cloud Run (one measurement each).

## Results and limits

[EQUITY-AUDIT.md](EQUITY-AUDIT.md) runs the matcher over the ten postings and counts the result three ways, because the
answer changes with the count. Per posting, the matches are close to the corpus with no consistent direction. Per distinct
recipient they sit lower on all three measures, because one pantry was the top match for three of the four retail offers (spinach, dairy,
deli). Weighted by estimated volume they sit in tracts with much less assistance (9%, against a corpus mean of 19%),
because the large loads can only go to the 14 recipients with room. With ten postings and eight distinct recipients the
audit cannot separate a real skew from noise, and it searches with the raw posting text where the live agent searches
with a rewrite. It does not show why that one pantry won three times; the matcher keeps no record of who received food
recently.

Known limits:

- Recipient names and addresses are real (IRS records), except nine invented teaching cases the challenge adds to the
  corpus, which have no real street or ZIP. Everyone's cold storage, pallet capacity and pickup times are generated. The
  agent presents them as the profile on file and suggests confirming by phone.
- Shelf life is USDA consumer guidance, not a cold-chain guarantee.
- Locations are ZIP-level, so the tract figures describe the surrounding area.
- The deployed service is open and the agent has Google's BigQuery tool, which runs read-only SQL as the service's
  account. Anyone with the address can ask it questions about the project's data, including the project id and table
  names, which the agent is given. The instructions confine it to the one dataset, but that is an instruction, not a
  permission. The project is a temporary lab project and holds only this data.
- The generated profile text and the numeric fields were produced separately and can disagree: one wholesale-style
  recipient's profile says it can be there "within a couple of hours" while its collection-time number is 19 hours.
  The filters use the numbers, and the agent is told not to repeat what a profile says about timing.
- `pickup_window_hours` is read as the lead time a recipient needs to collect. The data fits that reading (small
  pantries 2 to 6 hours, regional food banks 14 to 45), but the generator does not define it.
- The shelf-life table gave sealed infant formula a 1-hour shelf life, an opened-container figure. The shelf-life
  lookup now adds a caution at 2 hours or less, and the agent then uses the donor's own figure.

## How to run

From the `agent` folder:

```bash
python -m food_broker.selfcheck          # offline: filters, brief shape, identity decisions; no credentials
adk api_server --port 8765 .             # local server; set the settings below first
python -m food_broker.demo_tracks        # one posting per track through search and filters; needs the lab tables
```

To deploy, run `bash agent/deploy.sh` from the repository root. It checks the gcloud account and project and runs
the identity guard, then Cloud Build builds the [Dockerfile](../Dockerfile) in the cloud and deploys it to Cloud Run.
The service is open to unauthenticated requests, by the team's decision, so that anyone can try it. ADK's API server
has no authentication of its own, so spend is bounded by the deploy flags (one instance, 8 concurrent requests,
a 120-second timeout); `OPEN=0` puts it behind authentication instead. It is one instance on purpose: ADK keeps chat
sessions in the instance's memory, so a second instance would lose a follow-up question. ADK's chat page is served at the service
root (`NO_UI=1` turns it off). A browser page on another origin needs `A4I_ALLOW_ORIGINS` set at deploy time. How to
call the server and what comes back: [API.md](API.md).

## Reproduce it in your own project

The live demo ran in a temporary lab project that will be deleted, so here is how to rebuild it. Captured output from
the live service is in [docs/evidence](../../docs/evidence/README.md).

1. **A Google Cloud project** with the BigQuery, Vertex AI, Cloud Run, Cloud Build and Artifact Registry APIs enabled,
   and `gcloud` signed in to it. Use Python 3.12 (`pip install -r agent/requirements.txt`).
2. **Load the data.** Run the challenge notebook, or `bash scripts/load.sh chicago` from the repository root. Either
   creates the `a4i_food` dataset in the `US` location with `recipients`, `surplus_postings`, `shelf_life` and
   `tract_demographics`.
3. **Embed the recipients** once, in BigQuery:

   ```sql
   CREATE OR REPLACE TABLE `a4i_food.recipient_embeddings` AS
   SELECT * EXCEPT (embedded), embedded.result AS embedding
   FROM (SELECT r.*, AI.EMBED(r.profile_text, endpoint => 'gemini-embedding-2') AS embedded
         FROM `a4i_food.recipients` r)
   WHERE embedded.status = '';
   ```

4. **Change the project settings** at the top of `agent/lab.env` to your project id, project number and the ending of
   your account's address, then run `bash agent/deploy.sh`. If they do not match the account you are signed in as, the
   script refuses, by design.

Two things to know about the deployed service. ADK's chat page lists sessions, so anyone with the address can see
other people's test conversations: type nothing personal into it. And if a page on another origin will call the
service, set `A4I_ALLOW_ORIGINS` to that origin by name, not `*`.

## Settings

The values for the lab project are in [lab.env](../lab.env): no secrets, shared so anyone on the team can run or deploy.
Load them with `set -a; source agent/lab.env; set +a`; `deploy.sh` reads the file for anything you have not set.
The table below says what each one does.

| Variable | What it does | Default in code |
|---|---|---|
| `A4I_EXPECTED_PROJECT` | The only project the agent and deploy may run in, `<lab-project-id>` | None; required |
| `A4I_EXPECTED_PRINCIPAL_SUFFIX` | How a person's account must end, `@<lab-account-domain>` | None; required |
| `A4I_EXPECTED_PROJECT_NUMBER` | Lets the project's default compute account pass; `deploy.sh` sets it | None |
| `A4I_SA_ALLOWLIST` | Comma-separated service account addresses that may run it | Empty |
| `A4I_DATASET` | BigQuery dataset with the lab tables | `a4i_food` |
| `A4I_EMBED_ENDPOINT` | Embedding model for the search; must match the one that built `recipient_embeddings` | `gemini-embedding-2` |
| `A4I_MODEL` | Gemini model for the agent; use one the project has enabled | `gemini-2.5-flash` |
| `A4I_METRO` | City named in the agent's instructions | `Chicago` |
| `A4I_MCP` | `1` adds the BigQuery MCP toolset; `deploy.sh` sets it unless `NO_MCP=1` | Off |
| `GOOGLE_CLOUD_PROJECT` | Project for the BigQuery client, `<lab-project-id>`; `deploy.sh` sets it | None |
| `GOOGLE_GENAI_USE_VERTEXAI` | `1` sends Gemini calls to Vertex AI; `deploy.sh` sets it | Not set by this code |
| `GOOGLE_CLOUD_LOCATION` | Vertex AI region, `<region>`; `deploy.sh` sets it from `VERTEX_LOCATION` | Not set by this code |

## What is verified

| What | Status |
|---|---|
| Vector search, shelf-life, neighborhood and brief calls on the lab tables | Verified: ran |
| The agent end to end with Gemini on Vertex AI | Verified: ran |
| Cloud Run service, open to the public | Verified: deployed, answered full questions with no credentials, chat page loads |
| Offline selfcheck | Verified: passes |
| BigQuery MCP toolset | Verified: locally and on Cloud Run, a free-form question made two `execute_sql` calls and the agent's count matched a direct query. That first check counted all 192 rows (13 walk-in); seven of those are invented cases, so the real figure is 6 of 183 |
| A browser front end | Not verified: none has been run against the agent |
| Equity audit | Limited: one metro, ten postings |
