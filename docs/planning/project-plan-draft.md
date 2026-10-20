# Project Plan & 6-Person Team Allocation: Chicago Track 1

**Planning draft, written before the build.** What is deployed is described in [DESIGN.md](../DESIGN.md), which lists where it differs from this draft and the decisions the team still has to make. Kept as the record of the plan; where the two disagree, DESIGN.md is right.


**Scenario Statement (Write this on a whiteboard now):**
> *"We coordinate food rescue in Chicago. A local retail grocer has just offered us 10 crates of fresh spinach, and it has to move within 6 hours. Here is who we'd have to call, and here is what we don't know about them."*

---

## 👥 6-Person Team Roster & Lane Assignments

Because you have **6 people**, here is the optimal split so nobody steps on anyone else's toes in Git or BigQuery. Everyone works on their own Git branch (`data`, `agent`, `frontend`, `story`) and merges to `main` at the top of each hour.

| Role / Person | Lane | Git Branch | Primary Responsibility (What You Own) |
| :--- | :--- | :--- | :--- |
| **Person 1** | **Data Lead** | `data` | Runs `c2_01_load_explore.ipynb`, creates the `recipients_embedded` table (`AI.EMBED`), and validates data. |
| **Person 2** | **SQL & Audit Engineer** | `data` | Writes the multi-stage SQL query (`VECTOR_SEARCH` + Track 1 Constraints + `ST_DISTANCE` + Decoy log) & runs the 10-posting Equity Audit. |
| **Person 3** | **Agent Tool Dev** | `agent` | Builds the Python ADK tools (`check_shelf_life` and `find_viable_matches`) wrapping Person 2's SQL queries. |
| **Person 4** | **Prompt & Orchestration Lead** | `agent` | Writes the System Instruction (7-part Match Brief, "They said no" fallback, Load Splitter, Refusal logic) and tests all 7 Coordinator Qs. |
| **Person 5** | **Frontend & Cloud Run Lead** | `frontend` | Spins up `adk web`, deploys the agent to Cloud Run (`--min-instances=1`), and optionally builds a clean Coordinator Queue UI wrapper. |
| **Person 6** | **Team Lead & Story Owner** | `story` | Owns the GitHub repo, keeps time, builds the Pitch Deck (including "Real vs. Generated" & Equity Audit slides), and records the demo video. |

---

## 🔗 Critical Handoff & Dependency Map (Who Blocks Whom)

```text
[Minute 0-30]
Person 1 (Data) ──(Creates `recipients_embedded` table)──> UNBLOCKS Person 2 & Person 3
Person 6 (Lead) ──(Creates GitHub Repo & adds 5 teammates)──> UNBLOCKS Everyone's Git push

[Minute 30-90]
Person 2 (SQL)  ──(Hands working Hybrid SQL Query)───────> UNBLOCKS Person 3 (Python Tool)
Person 4 (Prompt)─(Hands System Prompt + Tool Stubs)─────> UNBLOCKS Person 5 (Local `adk web` test)

[Minute 90-150]
Person 3 + 4    ──(Working `agent/` folder merged)───────> UNBLOCKS Person 5 (Cloud Run Deploy)
Person 2 + 3    ──(Runs all 10 `surplus_postings`)───────> UNBLOCKS Person 6 (Equity Audit Slide)
```

---

## ⏱️ Hour-by-Hour Execution Checklist

### 📍 Hour 1: Setup, Data Load & Embeddings (Minutes 0–60)
**Goal:** Repo exists, Chicago data is in BigQuery, embeddings are materialized, and `adk web` runs locally with dummy tools.

* [ ] **Person 6 (Team Lead):** Click "Use this template" on GitHub, create public repo, add Persons 1–5 as collaborators.
* [ ] **All 6 Members:** Open Cloud Shell (`>_`), clone repo, checkout your lane branch (`git checkout -b data`, etc.).
* [ ] **Person 1 (Data Lead):** Open Colab Enterprise, import `c2_01_load_explore.ipynb`, set `METRO = "chicago"`, and run top-to-bottom. *(Fallback if Colab hangs: run `bash scripts/load.sh chicago` in Cloud Shell).*
* [ ] **Person 1 (Data Lead - CRITICAL):** Run the BigQuery SQL to generate vector embeddings on `a4i_food.recipients` (`profile_text`) and save as table `a4i_food.recipients_embedded`. **Announce to the team the second this finishes!**
* [ ] **Person 2 (SQL Engineer):** Inspect the 4 tables (`recipients`, `surplus_postings`, `shelf_life`, `tract_demographics`). Start drafting the SQL constraint filter (`has_cold_storage`, `pallet_capacity`, `pickup_window_hours`, `refrigerated_transport`).
* [ ] **Person 3 & 4 (Agent Lane):** Initialize the Python ADK structure inside the `agent/` folder (`agent.py`, `requirements.txt`, `.env`).
* [ ] **Person 5 (Frontend/Deploy):** Spin up `adk web` in Cloud Shell preview to confirm the basic ADK chat interface loads.
* [ ] **Person 6 (Story Lead):** Create the slide deck skeleton (Title, Problem/Scenario, Architecture, Demo placeholder, Real vs. Generated Data, Equity Audit results, Honest Limitations).

---

### 🛠️ Hour 2: Core Machinery—SQL, Tools & Prompts (Minutes 60–120)
**Goal:** The agent genuinely calls `VECTOR_SEARCH`, filters out the no-fridge decoys, and formats the 7-part Match Brief.

* [ ] **Person 1 (Data Lead):** Run an embedding experiment: compare searching against `profile_text` alone vs. an enriched query string. Document findings in 2 bullet points for Person 6's "Rigor & Judgment" slide.
* [ ] **Person 2 (SQL Engineer):** Complete the hybrid SQL query that returns both:
  1. Top 3 **Viable Survivors** (ranked by `no_vehicle_rate`, semantic similarity, and `ST_DISTANCE`).
  2. Top 2 **Rejected Decoys** (high semantic similarity, failed `has_cold_storage` or `pallet_capacity`) with their failure reason.
* [ ] **Person 3 (Agent Tool Dev):** Wrap the `shelf_life` lookup into Tool 1 (`check_shelf_life`) and Person 2's hybrid query into Tool 2 (`find_viable_matches`). Test both functions in Python to confirm they return clean JSON/dicts.
* [ ] **Person 4 (Prompt Lead):** Finalize the Gemini System Prompt enforcing:
  * The 7-part **Match Brief** markdown format.
  * The **"⚠️ Dispatch Volunteer Driver"** flag when `refrigerated_transport = FALSE`.
  * Context memory for *"They said no, who's next?"*
  * Load-splitting logic when `offered_pallets > max(pallet_capacity)`.
* [ ] **Person 5 (Frontend/Deploy):** Write the `Dockerfile` / Cloud Run deployment script and test deploying the initial agent to Cloud Run with `--min-instances=1` (to prevent cold starts).

---

### 🧪 Hour 3: Integration, The 7 Questions & The Equity Audit (Minutes 120–180)
**Goal:** Break the agent on edge cases, run the 10-posting Equity Audit, and lock in the UI.

* [ ] **Person 3, 4 & 5 (Agent + Frontend):** Run the **Spinach Stress Test** in the UI and verify all **7 Coordinator Questions** work seamlessly in one conversation:
  1. *"10 crates of spinach, harvested yesterday, needs cold storage, dock closes in 6 hours."* (Checks Match Brief)
  2. *"Why them and not the big food bank downtown?"* (Checks Decoy log explanation)
  3. *"They said no. Who's next?"* (Checks instant pivot to Runner-Up #2 + new SMS)
  4. *"How long does spinach actually last once it leaves the store?"* (Checks USDA `shelf_life` vs. donor deadline)
  5. *"Can they collect it themselves, or do I need to send a driver?"* (Checks `refrigerated_transport` + mileage)
  6. *"Whose neighborhood does this actually help?"* (Checks `tract_demographics` stats)
  7. *"What if a grocer offers 8 pallets of yogurt?"* (Checks Load Splitter / Refusal edge case)
* [ ] **Person 1 & 2 (Data Lane - BONUS POINTS):** Run the **Equity Audit** across all 10 rows in `surplus_postings`. Calculate:
  * Average `no_vehicle_rate` of matched tracts vs. Chicago baseline ($20.0\%$).
  * Average `poverty_rate` of matched tracts vs. Chicago baseline.
  * Hand this exact table/chart to Person 6 for the pitch deck!
* [ ] **Person 5 (Frontend Lead):** Polish the UI presentation (either clean up the `adk web` framing or connect Gemini Enterprise / custom wrapper) and verify the live Cloud Run URL works on Person 6's laptop.

---

### 🎬 Hour 4: Pitch Polish, Video Recording & Submission (Minutes 180–240+)
**Goal:** Record a crisp, bug-free screen-share walkthrough and submit all 4 links before the buzzer.

* [ ] **All Lanes:** Merge all working branches (`data`, `agent`, `frontend`, `story`) into `main`. Verify `README.md` in your repo briefly explains how to run your agent.
* [ ] **Person 6 (Story Lead):** Verify the Pitch Deck explicitly answers the **4 Mandatory Judge Checks**:
  1. **Real vs. Generated:** IRS Orgs/Addresses/Income + USDA Shelf Life + ACS Census are **REAL**; Fridges/Pallet Capacity/Pickup Windows are **GENERATED**.
  2. **Genuine Vector Search:** Explain how `VECTOR_SEARCH` generated 20 semantic candidates, and SQL constraints caught the decoys.
  3. **Equity Audit Numbers:** Show the exact `% no-vehicle rate` of your matches vs. Chicago's $20\%$ average.
  4. **Honest Limitations:** Mention ZIP-centroid straight-line distance (`ST_DISTANCE`), USDA consumer home-storage limits, and why BigQuery isn't used for transactional pallet locking.
* [ ] **Person 4 & 6:** Record the **Pitch Video** (screen-share walkthrough showing the live Spinach match, the "Why not X?" decoy check, and the "They said no" fallback). Keep it tight and punchy!
* [ ] **Person 6 (Team Lead):** Upload the 4 deliverables to `https://portal.angelhack.com/a4i-console`:
  1. GitHub Repo Link
  2. Google Skills / GCP Project Link
  3. Pitch Deck
  4. Pitch Video