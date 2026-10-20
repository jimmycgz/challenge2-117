# Food broker: how to call it and what comes back

Navigation: [agent README](README.md) for settings and the identity guard; [tools.py](tools.py) for the code
behind every field below. This page is for the front end and story lanes.

The agent is served by ADK's API server, app name `food_broker`. Routes checked on a running server:

| Method and path | Use |
|---|---|
| `POST /apps/food_broker/users/{user_id}/sessions` | Create a session. The reply has an `id` |
| `POST /run` | Send a message, get all events back when the run finishes |
| `POST /run_sse` | Same, streamed as server-sent events |
| `GET /health` | `{"status": "ok"}` |

Locally: `adk api_server --port 8765 .` from the `agent/` folder, with the settings from the agent README.

## One call, step by step

```bash
SID=$(curl -s -X POST http://127.0.0.1:8765/apps/food_broker/users/coordinator/sessions \
  -H 'content-type: application/json' -d '{}' | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")

curl -s -X POST http://127.0.0.1:8765/run -H 'content-type: application/json' -d "{
  \"app_name\": \"food_broker\", \"user_id\": \"coordinator\", \"session_id\": \"$SID\",
  \"new_message\": {\"role\": \"user\", \"parts\": [{\"text\": \"A grocer in Chicago has ten crates of spinach, harvested yesterday, that must leave the dock within 6 hours and stay cold.\"}]}
}"
```

`/run` returns a JSON list of events. Two things in it matter to a UI:

- **The structured brief.** The event whose part has `functionResponse.name == "find_matches"`. Its
  `functionResponse.response` is the JSON below. Build the interface from this, not from the text.
- **The written answer.** The last event with a `text` part. It is the same brief as six labelled parts, for
  a chat view.

A full answer took about 22 seconds on a laptop (one measurement, on gemini-2.5-flash). On gemini-3.8-flash at low thinking, spinach took 15.6 to 17.2 s run alone ([timings](../../docs/DESIGN.md)). Use `/run_sse` if the interface should show progress.

## The Match Brief

The six parts from the challenge sheet are the first six keys. `ranked` lists up to three options in order.
This example is illustrative: its organizations are among the nine invented teaching cases the challenge adds to the
corpus, not real ones.

```json
{
  "organization_and_why": {
    "name": "Maple Street Produce Alliance",
    "address": "100 Example St, Chicago, IL 60601",
    "why": "walk-in cold storage, takes up to 10 pallets, collects within 3h",
    "profile_excerpt": "Illustrative profile text."
  },
  "what_they_can_take": {
    "load_pallets": 0.5,
    "max_pallets": 10,
    "cold_storage": "walk-in",
    "frozen_storage": false,
    "loading_dock": true,
    "refrigerated_transport": true,
    "service_days": "Monday, Wednesday, Friday"
  },
  "the_clock": {
    "hours_remaining": 6,
    "collection_lead_hours": 3,
    "margin_hours": 3,
    "needs_driver": false
  },
  "whose_neighborhood": {
    "households_per_week": 400,
    "populations_served": "General public",
    "tract": "Nearest census tract: 31% of residents below the poverty line, 22% of households without a vehicle, 18% on food or cash assistance (ACS; recipient location is ZIP-level, so this is the area, not the exact block)."
  },
  "outreach_message": "Hello Maple Street Produce Alliance team,\n\nA grocer on the north side has ten crates of spinach. It is still good but has to move soon. From what we have on file you have the storage for it. The food needs to leave by about 6 hours from now, which leaves you roughly 3 hours of slack to collect. You are set up to collect it yourselves.\n\nCan you take it? If you can, tell us the time you can collect and a phone number for pickup. If not, a quick no helps us move to the next place.\n\nThank you,\n[Coordinator name]",
  "next_two_options": [
    {
      "rank": 2,
      "name": "Third Ward Community Table",
      "address": "100 Example St, Chicago, IL 60601",
      "why": "domestic cold storage, takes up to 1 pallet, collects within 4h",
      "margin_hours": 2,
      "needs_driver": true
    },
    {
      "rank": 3,
      "name": "Southline Neighbors Pantry",
      "address": "100 Example St, Chicago, IL 60601",
      "why": "walk-in cold storage, takes up to 3 pallets, collects within 6h",
      "margin_hours": 0,
      "needs_driver": true
    }
  ],
  "ranked": [
    {
      "rank": 1,
      "name": "Maple Street Produce Alliance",
      "address": "100 Example St, Chicago, IL 60601",
      "why": "walk-in cold storage, takes up to 10 pallets, collects within 3h",
      "margin_hours": 3,
      "needs_driver": false
    },
    {
      "rank": 2,
      "name": "Third Ward Community Table",
      "address": "100 Example St, Chicago, IL 60601",
      "why": "domestic cold storage, takes up to 1 pallet, collects within 4h",
      "margin_hours": 2,
      "needs_driver": true
    },
    {
      "rank": 3,
      "name": "Southline Neighbors Pantry",
      "address": "100 Example St, Chicago, IL 60601",
      "why": "walk-in cold storage, takes up to 3 pallets, collects within 6h",
      "margin_hours": 0,
      "needs_driver": true
    }
  ],
  "rejected_but_close": [
    {
      "name": "Greenline Community Pantry",
      "because": "no cold storage; needs 12h to collect, food has 6h"
    },
    {
      "name": "Cedar Street Produce Alliance",
      "because": "needs 24h to collect, food has 6h"
    }
  ],
  "refusal": null,
  "search": {
    "candidates_searched": 5,
    "viable_after_filters": 3
  }
}
```

| Key | Meaning |
|---|---|
| `organization_and_why` | Top match: name, address, why it fits, an excerpt of its profile |
| `what_they_can_take` | Their capacity and storage against the load (`load_pallets` is the size of this load) |
| `the_clock` | Hours the food has, the recipient's collection lead time, the margin, whether a driver is needed |
| `whose_neighborhood` | Households served per week, populations served, and the nearest census tract's figures |
| `outreach_message` | A draft ready to send, ending in `[Coordinator name]` |
| `next_two_options` | Ranks 2 and 3, because the first will sometimes say no |
| `ranked` | Ranks 1 to 3 with the same card fields. Fewer than three if fewer survived the filters |
| `rejected_but_close` | Up to three semantic matches the filters removed, each with the reason and its rank by meaning (`semantic_rank`, 1 is closest). One that failed on cold storage is always included when there is one |
| `refusal` | `null`, or a sentence when nobody can take the load |
| `search` | `candidates_searched` and `viable_after_filters`: how wide the search was and how many survived |

## When nobody can take it

Not an error. The brief comes back with `refusal` set to a sentence, the six parts `null` (`next_two_options`
and `ranked` empty) and `rejected_but_close` filled in. Show the refusal and the reasons.

## When something fails

The `find_matches` response is `{"error": {"code": "...", "message": "..."}}` and nothing else.

| `code` | Meaning |
|---|---|
| `identity_refused` | The identity guard stopped the run: the credentials are not the lab's |
| `search_failed` | Any other failure, for example BigQuery unreachable. The message carries the exception |

The written answer then says plainly that it could not find a match.

## Who can call it

The deployed service is open: no credentials are needed, so a browser or `curl` can call it directly. ADK's chat page
is at the service root. ADK's API server has no authentication of its own, so the deploy limits spend (one
instance, 8 concurrent requests, a 300-second timeout). One instance on purpose: sessions live in its memory, so a
second instance would lose a follow-up question. A page served from a different origin than the service needs
CORS, which is off until `A4I_ALLOW_ORIGINS` is set when the service is deployed; ask the agent lane.
