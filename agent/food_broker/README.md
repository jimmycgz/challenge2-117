# Food broker agent

Navigation: this folder is the agent. Code: [agent.py](agent.py),
[tools.py](tools.py),
[identity_guard.py](identity_guard.py),
[selfcheck.py](selfcheck.py).
The challenge brief is the [main README](../../README.md).

An ADK agent for retail and grocer rescue. A posting goes in; a ranked, reasoned Match Brief comes out.
Vector search proposes candidates by meaning; the constraint filter decides who can really take the food.

## Tools

| Tool | Job |
|---|---|
| `vector_candidates` | BigQuery `VECTOR_SEARCH` over `recipient_embeddings`. Meaning only |
| `lookup_shelf_life` | USDA FoodKeeper hours for a product (consumer guidance, not cold-chain) |
| `apply_constraints` | Drops recipients with no cold storage, too little capacity, or a collection time past the clock; says why |
| `build_match_brief` | Top match, next two options, close-but-rejected, the clock; refuses when nobody is viable |
| BigQuery MCP (optional) | Google's managed MCP server, for free-form questions over the tables. Off until `A4I_MCP=1` |

## Settings

Set these in the shell before running. None has a default that grants access: a missing guard value
makes the agent refuse to run.

| Variable | Meaning |
|---|---|
| `GOOGLE_CLOUD_PROJECT` | The lab project id |
| `A4I_EXPECTED_PROJECT` | The only project the agent may run in. Same value as above |
| `A4I_EXPECTED_PRINCIPAL_SUFFIX` | Ends the lab student account, for a person running it (the lab's account domain) |
| `A4I_EXPECTED_PROJECT_NUMBER` | The project number, so the project's default compute service account is accepted on Cloud Run. Get it with `gcloud projects describe <project-id> --format='value(projectNumber)'` |
| `A4I_SA_ALLOWLIST` | Optional. Comma-separated service account emails that may run it |
| `A4I_DATASET` | BigQuery dataset, default `a4i_food` |
| `A4I_EMBED_ENDPOINT` | Embedding model, default `gemini-embedding-2`. Must match the model that built the table |
| `A4I_MODEL` | Gemini model for the agent. Use one the lab project has enabled |
| `A4I_METRO` | City named in the agent's instructions, default Chicago |
| `A4I_MCP` | `1` to add the BigQuery MCP toolset |

## Identity guard

Before any BigQuery client, MCP toolset or agent run, `identity_guard.py` reads who the credentials are and refuses
unless they belong to the lab:

- A person must end in `A4I_EXPECTED_PRINCIPAL_SUFFIX` and the credentials must resolve to `A4I_EXPECTED_PROJECT`.
- A service account is judged on its email, never on the project it resolved to, because `GOOGLE_CLOUD_PROJECT`
  can force that project for any credential. It passes only as the project's own
  `@<project>.iam.gserviceaccount.com` address, its default compute account, or an `A4I_SA_ALLOWLIST` entry.
- Impersonated credentials are refused outright.

Deploy scripts can run `python -m food_broker.identity_guard`; it exits 2 on the wrong identity.

## Check it without a cloud project

From the `agent` folder:

```bash
python -m food_broker.selfcheck
```

It runs the constraint filter against the planted teaching cases (the decoy with no cold storage, a pickup that
misses the clock, nobody viable) and the identity decisions. It needs no credentials.

## Known limits

- Recipient names and addresses are real; cold storage, pallets and pickup times are generated.
- `pickup_window_hours` is read as the lead time a recipient needs to collect. The data fits that reading
  (small pantries 2 to 6 hours, regional food banks 14 to 45) and the challenge brief compares it directly
  with the hours the food has left, but the generator does not define it in words.
- Shelf life is consumer guidance, not a guarantee. Locations are ZIP-level.
- The vector search, shelf-life, neighborhood and brief calls have run against the lab tables (Chicago, 192
  recipients). The MCP toolset and the deployed service have not.
