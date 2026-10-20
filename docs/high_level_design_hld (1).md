# High-Level Design (HLD): Chicago Food Rescue Agent (Track 1)

## 1. End-to-End Ecosystem & User Touchpoints

To ensure complete end-to-end coverage, this diagram shows how external actors (Grocers, Pantries, Volunteer Drivers) interact with our primary user (**The Coordinator**) and how the system handles both live brokering and batch auditing.

```text
  [EXTERNAL SUPPLY]                 [PRIMARY USER]                 [EXTERNAL LOGISTICS & DEMAND]
+-------------------+           +--------------------+           +-------------------------------+
|  Retail Grocer    | --Call--> |                    | --SMS---> | 1. Viable Pantry (Recipient)  |
| (Unstructured     |   or      |   Food Rescue      |           |    (Claims load via text)     |
|  Surplus Offer)   | --Text--> |   Coordinator      |           +-------------------------------+
+-------------------+           |  (Internal Staff)  |           | 2. Volunteer Driver Pool      |
                                +--------------------+           |    (Dispatched if pantry      |
                                          ^                      |     lacks refrigerated van)   |
                                          |                      +-------------------------------+
                                          | Pastes Offer / Asks Follow-ups
                                          v
+------------------------------------------------------------------------------------------------+
|                                  ADK WEB DISPATCH CONSOLE                                      |
|  - Renders 7-Part Match Brief   - Handles "They Said No" Pivots   - Explains Rejected Decoys   |
+------------------------------------------------------------------------------------------------+
                                          ^
                                          |
                                          v
+------------------------------------------------------------------------------------------------+
|                             GEMINI ORCHESTRATOR (Python ADK)                                   |
|  - NLP Parameter Extraction     - Context Memory (Backups)        - Load Split / Refusal Logic |
+------------------------------------------------------------------------------------------------+
         |                                |                                       |
         | Tool 1:                        | Tool 2:                               | Tool 3 (Add-on):
         | `check_shelf_life`             | `find_viable_matches`                 | `run_equity_audit`
         v                                v                                       v
+------------------------------------------------------------------------------------------------+
|                              BIGQUERY (`a4i_food` Dataset)                                     |
|  - `shelf_life` (USDA)          - `recipients_embedded` (Vector+SQL)  - `tract_demographics`   |
+------------------------------------------------------------------------------------------------+
```

---

## 2. End-to-End Sequence Diagram: Happy Path & Follow-Up Q&A

This diagram shows how the raw supplier offer is transformed into a ranked, delivery-ready recommendation, and how the Coordinator interacts with it across all 7 required questions.

```text
Coordinator          Gemini Agent             Tool 1: ShelfLife        Tool 2: Vector + SQL + Equity
    |                     |                           |                              |
    | 1. "10 crates of    |                           |                              |
    |    spinach, dock    |                           |                              |
    |    by 8pm (6 hrs)"  |                           |                              |
    |-------------------->|                           |                              |
    |                     | 2. Parse NLP Variables:   |                              |
    |                     | - food: "spinach"         |                              |
    |                     | - semantic_q: "fresh      |                              |
    |                     |   leafy greens produce"   |                              |
    |                     | - pallets_est: 1          |                              |
    |                     | - needs_cold: TRUE        |                              |
    |                     | - max_hours: 6            |                              |
    |                     |                           |                              |
    |                     | 3. Query USDA FoodKeeper  |                              |
    |                     |-------------------------->|                              |
    |                     |<--------------------------|                              |
    |                     | Returns: 72 hrs (Cold)    |                              |
    |                     | Effective Clock = MIN(6,72) = 6 hrs                      |
    |                     |                           |                              |
    |                     | 4. Execute Hybrid Search & Ranking Pipeline              |
    |                     |--------------------------------------------------------->|
    |                     |                           |   [Step A: Vector Search]    |
    |                     |                           |   Embeds query -> Top 20 IDs |
    |                     |                           |   (Includes Decoys!)         |
    |                     |                           |                              |
    |                     |                           |   [Step B: Hard SQL Filter]  |
    |                     |                           |   - has_cold_storage = TRUE  |
    |                     |                           |   - pallet_capacity >= 1     |
    |                     |                           |   - pickup_window <= 6 hrs   |
    |                     |                           |   - service_days = Today     |
    |                     |                           |   (Drops 15 Decoys -> 5 left)|
    |                     |                           |                              |
    |                     |                           |   [Step C: Geo & Equity Join]|
    |                     |                           |   - ST_DISTANCE (Donor->Org) |
    |                     |                           |   - JOIN tract_demographics  |
    |                     |                           |   - Score & Rank Top 3       |
    |                     |<---------------------------------------------------------|
    |                     | Returns JSON:                                            |
    |                     | - `viable_matches` (Top 3)                               |
    |                     | - `rejected_decoys` (Top 2 failed semantic hits)         |
    |                     |                           |                              |
    | 5. Render Formatted |                           |                              |
    |    MATCH BRIEF      |                           |                              |
    |<--------------------|                           |                              |
    |                     |                           |                              |
    | 6a. "Why not the    | (Reads `rejected_decoys` from tool output:               |
    |   downtown pantry?" |  "They matched 94% on produce, but has_cold_storage=0")  |
    |-------------------->|                           |                              |
    |<--------------------|                           |                              |
    |                     |                           |                              |
    | 6b. "Primary said   | (Reads Runner-Up #2 from context memory;                 |
    |   no. Who's next?"  |  promotes #2 to Primary & drafts new SMS instantly)      |
    |-------------------->|                           |                              |
    |<--------------------|                           |                              |
```

---

## 3. Deep Dive: The Matching, Delivery & Ranking Engine

To satisfy Track 1 requirements, our core BigQuery tool (`find_viable_matches`) computes operational viability, delivery logistics, decoy tracking, and equity scoring in a single multi-stage CTE query.

```text
+-------------------------------------------------------------------------+
| STAGE 1: SEMANTIC CANDIDATE GENERATION (The Meaning Layer)              |
| - Uses `VECTOR_SEARCH` on `recipients_embedded.embedding`               |
| - Captures dietary rules ("halal", "no pork") & need ("fresh greens")   |
| - Output: Top 20 Candidates (Ranked by cosine distance)                 |
+-------------------------------------------------------------------------+
                                    |
                   +----------------+----------------+
                   |                                 |
                   v (Passes Constraints)            v (Fails Constraints)
+-----------------------------------+   +---------------------------------+
| STAGE 2A: VIABLE SURVIVORS        |   | STAGE 2B: DECOY REJECTION LOG   |
| - `has_cold_storage = @needs_cold`|   | - Captures Top 2 semantic hits  |
| - `pallet_capacity >= @pallets`   |   |   that failed Stage 2A          |
| - `pickup_window <= @clock_hours` |   | - Tags exact failure reason:    |
| - `service_days` contains Today   |   |   e.g. "No Cold Storage" or     |
|                                   |   |   "Capacity < 1 Pallet"         |
+-----------------------------------+   +---------------------------------+
                   |                                 |
                   v                                 |
+-----------------------------------+                |
| STAGE 3: LOGISTICS & EQUITY RANK  |                |
| - Spatial: `ST_DISTANCE` (miles)  |                |
| - Census: `no_vehicle_rate`       |                |
| - Transport Flag:                 |                |
|   `refrigerated_transport` T/F    |                |
| - Composite Score:                |                |
|   `(0.4 * Semantic_Sim) +         |                |
|    (0.4 * No_Vehicle_Rate) +      |                |
|    (0.2 * Proximity_Score)`       |                |
+-----------------------------------+                |
                   |                                 |
                   +----------------+----------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| STAGE 4: PAYLOAD RETURN TO GEMINI AGENT                                 |
| - Returns `viable_matches` (Top 3) + `rejected_decoys` (Top 2)          |
+-------------------------------------------------------------------------+
```

---

## 4. Edge-Case Decision Tree (When Reality Breaks the Happy Path)

The README states: *"An agent that confidently recommends a recipient who can't store the food is worse than one that says 'nobody in range can take this.'"* Here is how our architecture handles the three edge cases end-to-end:

```text
                     [Tool 2 Executes: `find_viable_matches`]
                                        |
         +------------------------------+------------------------------+
         |                              |                              |
         v (3+ Viable Matches)          v (0 Viable: Capacity Too Low) v (0 Viable: Time/Cold)
+------------------+          +-------------------------+     +------------------------+
| CASE 1: STANDARD |          | CASE 2: LOAD SPLITTER   |     | CASE 3: SAFE REFUSAL   |
|   MATCH BRIEF    |          | (Triggered when donor   |     | (Triggered when clock  |
|                  |          |  offers 6 pallets, but  |     |  is < 1 hr or 0 orgs   |
| - Ranks Top 3    |          |  max pantry cap is 4)   |     |  have cold storage)    |
| - Drafts 1 SMS   |          |                         |     |                        |
| - Logs Decoys    |          | - Agent relaxes single- |     | - Agent DO NOT GUESS   |
+------------------+          |   org capacity filter   |     | - Outputs Refusal:     |
                              | - Selects Top 2 viable  |     |   "No org in Chicago   |
                              |   orgs whose combined   |     |   can safely collect   |
                              |   capacity >= 6 pallets |     |   before expiration."  |
                              | - Drafts 2 split SMS    |     | - Shows closest misses |
                              +-------------------------+     +------------------------+
```

---

## 5. How Output is Formatted and Consumed

### 1. Structured JSON from Tool to Agent
The Python tool returns a rich dictionary containing two arrays:
* `viable_matches`: The Top 3 ranked organizations with all columns (`name`, `address`, `profile_text`, `pallet_capacity`, `refrigerated_transport`, `pickup_window_hours`, `dist_miles`, `tract_no_vehicle_pct`, `tract_poverty_pct`).
* `rejected_decoys`: The top 2 organizations that scored high semantically in Stage 1 but were dropped in Stage 2 (including the exact reason they failed, e.g., `"failed_constraint": "has_cold_storage is FALSE"`).

### 2. Markdown Rendering in the UI (Consumption)
Gemini consumes that JSON and formats it into the **Match Brief** inside the ADK Web UI. 
* **Immediate Actionability:** The Coordinator doesn't have to look up phone numbers, calculate hours, or wonder if they need to call a volunteer driver. The **"Transport Action"** line tells them immediately if a volunteer driver is required, and the **Drafted SMS** is ready to copy-paste into their dispatch phone.
* **Instant Explainability:** Because the tool passes back `rejected_decoys`, when the Coordinator asks *"Why didn't we give the spinach to Pantry X?"*, the agent immediately answers without running a second query.