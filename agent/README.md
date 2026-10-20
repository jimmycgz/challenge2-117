# Food broker agent: teammate setup

The agent, its design and its results are in [food_broker/README.md](food_broker/README.md). This page gets you running
the same agent, with the same settings, as everyone else on the team. The challenge brief that was here before is kept
at the bottom.

## Everyone uses the same settings

[lab.env](lab.env) is the one shared source: lab project, project number, model (`gemini-3.8-flash`, low thinking),
region (`global`), dataset and metro. `setup.sh` copies it to `agent/.env`, and ADK reads that file on start. Nobody
edits the project values. The only thing that differs per person is their own student login
(`student-00-...@qwiklabs.net`). After every pull, run `bash agent/setup.sh` again: it overwrites `agent/.env` with the current `lab.env`, so a change to the shared settings (the model, for one) reaches you and any line you added to `.env` by hand is lost. `.env` is not tracked by git.

## Setup, in order

```bash
git clone https://github.com/jimmycgz/challenge2-117.git && cd challenge2-117
bash agent/setup.sh                      # venv in agent/.venv, requirements, agent/.env, offline selfcheck
cd agent && .venv/bin/adk web .          # then open the page ADK prints
```

- **Cloud Shell:** nothing else. You are already signed in as your student login and Cloud Shell supplies the
  credentials.
- **Laptop:** sign in once with the lab student account, not a personal or work one:

  ```bash
  gcloud auth login                      # the student-00-...@qwiklabs.net account
  gcloud auth application-default login  # same account; the agent's code uses these credentials
  gcloud config set project qwiklabs-gcp-04-6c7101c1dba1
  ```

- Use Python 3.12. Python 3.14 silently installs an old ADK because one dependency has no wheel for it.
- The agent refuses to start on any other project or account. That is the identity guard, working as intended.

## Verify and debug: eight read-only checks

Run them in order from `agent/`, after `set -a; source lab.env; set +a`. Each changes nothing. The first one that
does not match the healthy result is where the problem is.

| # | Check | Command | Healthy result |
|---|---|---|---|
| 1 | Identity | `gcloud config get-value account; gcloud config get-value project` | `student-00-...@qwiklabs.net`, then `qwiklabs-gcp-04-6c7101c1dba1` |
| 2 | Roles | `gcloud projects get-iam-policy $GOOGLE_CLOUD_PROJECT --flatten='bindings[].members' --filter="bindings.members:user:$(gcloud config get-value account)" --format='value(bindings.role)'` | includes `roles/owner` |
| 3 | APIs | `gcloud services list --enabled --filter='name:(bigquery.googleapis.com OR aiplatform.googleapis.com OR run.googleapis.com OR cloudbuild.googleapis.com)' --format='value(name)'` | four lines, one per API |
| 4 | What the code sees | `.venv/bin/python -c "import google.auth; c,p=google.auth.default(); print(p)"` | `qwiklabs-gcp-04-6c7101c1dba1` |
| 5 | BigQuery | `bq query --project_id=$GOOGLE_CLOUD_PROJECT --nouse_legacy_sql --format=csv 'SELECT COUNT(*) AS n FROM a4i_food.recipients'` | `192` |
| 6 | One Vertex call | `.venv/bin/python -c "import os; from google import genai; c=genai.Client(vertexai=True, project=os.environ['GOOGLE_CLOUD_PROJECT'], location=os.environ['GOOGLE_CLOUD_LOCATION']); print(c.models.generate_content(model=os.environ['A4I_MODEL'], contents='Reply with the single word ready').text)"` | `ready` |
| 7 | The guard alone | `.venv/bin/python -W ignore -m food_broker.identity_guard` | `identity ok: user student-00-...@qwiklabs.net in project qwiklabs-gcp-04-6c7101c1dba1` |
| 8 | Offline selfcheck | `.venv/bin/python -m food_broker.selfcheck` | `selfcheck passed: 5 candidates, 3 viable for spinach` |

Where a failure points: 1 or 2, you are signed in as the wrong account or the account has no role on the project;
3, an API is off (ask in the team channel before enabling anything); 4, the credentials name a different project, so
check `GOOGLE_CLOUD_PROJECT` and, on a laptop, run `gcloud auth application-default login` again; 5, the tables are
missing or you are on the wrong project; 6, the model or region is wrong (`gemini-3.8-flash` exists only in
`global`, so `GOOGLE_CLOUD_LOCATION=us-central1` fails here); 7, the guard refuses, and its message says why.

## If the guard refused you in Cloud Shell

Earlier versions of the identity guard judged Cloud Shell and Workbench credentials as a service account, because
those credentials report the person's address through the metadata server. A student login was then refused with a
service-account message. This is fixed in this pull request: a credential is a service account only if its address
ends in `.gserviceaccount.com`, and a test in `food_broker/selfcheck.py` fails on the old code. The
`A4I_SA_ALLOWLIST` workaround (adding your address to that setting) is needed only on an older checkout; on this one,
pull and run `setup.sh` again instead.

## The challenge brief (original text)

This folder was empty when the hackathon started. The brief follows.

We built the on-ramp: real organizations, an honest recipient corpus, a shelf-life clock, a
need signal, and a validation suite that tells you plainly whether any of it is wrong. We did
not build the vehicle. The design decisions in your agent are what you'll be judged on.

## What has to be true of what you build here

- **An ADK agent**, in Python.
- **At least one tool you built yourself.** A Python function tool, or one you defined in MCP
  Toolbox—either counts. The obvious candidate wraps your match query, but the more valuable
  one holds the logic that isn't a single query: composing the search string, applying the
  constraint filter, assembling the Match Brief. Consuming only prebuilt generic tools and
  calling that your design does not count.
- **At least one Google-managed MCP server, consumed.** Don't author your own—use BigQuery's
  built-in server or the [MCP Toolbox for Databases](https://github.com/googleapis/mcp-toolbox).
- **Deployed to Google Cloud**—Agent Runtime or Cloud Run, your choice.
- **Your required differentiator: BigQuery vector search.** Your agent must genuinely *call*
  the semantic search. Filtering on categories or `LIKE '%spinach%'` does not count, and it is
  the most common way a team misses the point while appearing to hit it.

## The thing worth remembering while you build

Vector search is a **candidate generator, not an answer**. There is at least one organization
in your corpus that semantically looks like a perfect match and physically cannot store the
food. What you do *after* the search—storage compatibility, pallet capacity, the pickup window
against the clock—is where this agent becomes useful instead of merely clever.

See Section 14 of [`notebooks/c2_01_load_explore.ipynb`](../notebooks/c2_01_load_explore.ipynb)
for the query shape and the four syntax traps (it reads fine on GitHub without running).
