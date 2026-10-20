# Product Requirements Document (PRD): Chicago Food Rescue Agent (Track 1)

**Planning draft, written before the build.** What is deployed is described in [DESIGN.md](../DESIGN.md), which lists where it differs from this draft and the decisions the team still has to make. Kept as the record of the plan; where the two disagree, DESIGN.md is right.


## 1. Product Vision & Problem Statement

**The Problem:** Perfectly good retail food (produce, dairy, prepared meals) is thrown away because making a match requires knowing—in the same minute—what just became available, who could use it, what they can physically store, how it will get there, and how long the food has left. By the time a human manually cross-references spreadsheets to answer this, the food is spoiled.
**The Vision:** An AI-powered Food Rescue Coordinator Agent built on Google's Agent Development Kit (ADK). It ingests messy, unstructured donation offers, calculates shelf life, semantically matches recipients, enforces strict Track 1 physical/delivery constraints via SQL, ranks viable options by neighborhood equity need, and outputs an actionable **Match Brief** in seconds.

---

## 2. User Personas & Ecosystem Actors

To justify our front-end choice (ADK Web / Gemini Enterprise as an internal console) to the judges, we explicitly define who directly uses the application versus who interacts with its outputs:

### Primary Direct User: The Food Rescue Coordinator (Internal Staff)
* **Role:** Operations dispatcher at a Chicago food rescue organization.
* **Environment:** Sitting at a desk at 4:00 PM on a Thursday with multiple tabs open, fielding phone calls/texts from grocery store managers, with a group text of volunteer drivers waiting for dispatch instructions.
* **Pain Point:** High cognitive load under a ticking clock. Cannot afford to send 10 crates of spinach to a pantry whose fridge is broken or closed, or volunteers will quit and food will spoil.

### Secondary Direct User (Optional Add-On): The Pantry Manager (Onboarding)
* **Role:** Director of a neighborhood soup kitchen or church pantry.
* **Pain Point:** Doesn't have time to fill out 50-field standardized capability forms, which is why operational data doesn't exist publicly. Needs a quick, conversational way to tell the system what they can handle.

### Indirect Actors (Touchpoints Outside the UI)
* **The Retail Donor (Supply Side):** Store manager at a Chicago grocer. Texts messy offers (*"10 crates of spinach, dock closes at 8pm"*).
* **The Volunteer Driver (Logistics Side):** Receives the Coordinator's copy-pasted SMS dispatch instructions when a recipient lacks their own `refrigerated_transport`.

---

## 3. Epics & User Stories (The Complete End-to-End Coverage)

These user stories directly map to the **7 Coordinator Questions** and **Track 1 Edge Cases** required by the challenge rubric:

| ID | User Story | Acceptance Criteria (How We Prove It Works) |
| :--- | :--- | :--- |
| **US-1: Unstructured Intake & Match** | *As a Coordinator, I want to paste a messy text from a grocer and immediately see the top viable recipient so I don't waste time parsing spreadsheets.* | Agent extracts item, qty, storage need, and deadline, runs Vector Search + SQL Filter, and renders the 7-part **Match Brief**. |
| **US-2: Decoy Explainability** | *As a Coordinator, I want to ask "Why them and not the big food bank downtown?" so I can trust the agent isn't missing obvious partners.* | Agent references the `notable_rejections` log and explains the exact constraint failure (e.g., *"Pantry X matched 92% on produce, but lacks cold storage"*). |
| **US-3: Graceful Fallback ("They Said No")** | *As a Coordinator, when my #1 pantry doesn't answer the phone, I want to type "They said no, who's next?" and get an instant pivot.* | Agent reads Runner-Up #2 from conversation memory, promotes them to Primary, and drafts a new customized outreach SMS in $< 2$ seconds. |
| **US-4: Biological vs. Donor Clock** | *As a Coordinator, I need to know how long the food actually lasts vs. when the loading dock closes.* | Agent queries `shelf_life` (USDA), compares it against the donor's deadline, uses `MIN(donor_hrs, usda_hrs)`, and displays the exact safety margin. |
| **US-5: Transport & Driver Dispatch** | *As a Coordinator, I need to know if the pantry can pick up the food themselves or if I must dispatch a volunteer driver.* | Agent checks `refrigerated_transport`. If `FALSE`, flags **"⚠️ Dispatch Volunteer Driver"** and includes straight-line mileage (`ST_DISTANCE`). |
| **US-6: Neighborhood Equity Audit** | *As a Coordinator, I want to ensure food goes to high-need areas rather than just big warehouses with loading docks.* | Agent joins `tract_demographics` and prioritizes tracts with high `no_vehicle_rate` ($> 20\%$ Chicago baseline) and `poverty_rate`. |
| **US-7: Load Splitting / Refusal** | *As a Coordinator, if a load exceeds any single pantry's fridge (or if no one is open), I want the agent to propose a split or safely refuse.* | If `pallets > max(pallet_capacity)`, agent proposes splitting across Top 2 viable pantries. If 0 viable matches exist, agent refuses rather than guessing. |

---

## 4. End-to-End User Flow: Ingestion to Consumption

1. **The Trigger (External Supply):** A local Chicago grocer calls or texts: *"We are pulling 10 crates of spinach off the shelf. Harvested yesterday, needs cold storage, has to leave our dock by 8 PM."*
2. **Data Entry (Ingestion):** The Coordinator pastes this exact text into the Agent UI (or selects one of the 10 test rows from `surplus_postings`).
3. **Agent Extraction (NLP):** Gemini parses the text into structured parameters: `item="spinach"`, `qty_crates=10` (converts to $\approx 1$ pallet), `storage_req="cold"`, `donor_deadline_hours=6`, `donor_zip="60601"`.
4. **Tool Execution (The Pipeline):** The agent checks USDA shelf-life, generates 20 semantic candidates via Vector Search, filters out "decoys" using hard SQL constraints, and ranks the survivors by equity and distance.
5. **Output Consumption (Action):** The Coordinator reads the formatted **Match Brief** on their screen, sees whether the pantry can self-collect or needs a volunteer driver, and copies/pastes the pre-drafted SMS directly to the pantry or driver group text.
6. **Iterative Resolution (Follow-ups):** The Coordinator asks follow-up questions (*"Why not X?"* or *"They declined"*) until the food is claimed.

---

## 5. Core Requirements: The "Four Questions" + Delivery Logistics

### Q1: What just became available? (NLP Parsing)
* **Requirement:** Extract operational variables from messy free-text postings, including converting retail units (crates/boxes/pounds) into standard pallet estimates (`1 pallet ≈ 10-12 crates` or `500 lbs`).

### Q2: Who could use it? (Semantic Vector Search)
* **Requirement:** Match the *meaning* of the food (e.g., "spinach" $\rightarrow$ "fresh greens/produce") and respect dietary/cultural constraints embedded in profiles (e.g., halal, kosher, infant-only) using `VECTOR_SEARCH` on `recipients_embedded`.

### Q3: What can they physically store & how does it get there? (Track 1 Hard Constraints)
* **Requirement:** Eliminate semantic matches that fail physical reality (The "Decoy" Trap). For **Track 1 (Retail Rescue)**, the SQL filter must enforce:
  1. **Storage Compatibility:** `has_cold_storage = TRUE` (for perishable retail rescue).
  2. **Volume Capacity:** `pallet_capacity >= offered_pallets`.
  3. **Operating Hours:** `service_days` includes today's day of the week, and `pickup_window_hours <= effective_clock`.
  4. **Transport / Delivery Mode:** Check `refrigerated_transport`. If `TRUE`, the recipient can collect it themselves. If `FALSE`, the agent flags that the **Coordinator must dispatch a volunteer driver**.

### Q4: How long does the food have left? (The Ticking Clock)
* **Requirement:** Query the `shelf_life` (USDA FoodKeeper) table to get biological expiration in hours.
* **Logic:** $\text{Effective Clock} = \min(\text{donor\_deadline\_hours}, \text{usda\_shelf\_life\_hours})$. Calculate the safety margin: $\text{Effective Clock} - \text{recipient\_pickup\_window\_hours}$.

---

## 6. Matching & Ranking Logic (How We Pick the "Best" Match)

Once the SQL Constraint Filter drops incapable organizations from the Top 20 semantic candidates, we use a **Defensible Multi-Factor Tie-Breaker** in SQL:
1. **Primary Filter (Hard Gate):** Must pass 100% of storage, capacity, and time window constraints.
2. **Primary Rank (The Equity Signal - 40% Weight):** Joined with `tract_demographics`. We prioritize census tracts with the highest `no_vehicle_rate` and `poverty_rate`. In Chicago ($20\%$ baseline no-vehicle rate), routing fresh produce to neighborhoods without cars maximizes impact.
3. **Secondary Rank (Semantic Fit - 40% Weight):** Cosine similarity score ($1 - \text{distance}$) from BigQuery `VECTOR_SEARCH`.
4. **Tertiary Rank (Proximity / Logistics - 20% Weight):** Calculated using BigQuery `ST_DISTANCE` between the donor's coordinates and the recipient's coordinates. Shorter distances preserve cold-chain integrity.

---

## 7. Output Specification: The "Match Brief" Artifact

The agent is strictly prompted to output a structured Markdown **Match Brief** containing these 7 mandatory elements:

```markdown
### 🚨 MATCH BRIEF: [Item Summary]

**1. Primary Recipient:** [Org Name] — [Full Address]
**2. Why Them (Semantic Fit):** [1 sentence quoting their profile_text, e.g., "Explicitly requests fresh leafy greens for their Tuesday family distribution."]
**3. Capacity & Logistics Check:** 
   - **Storage:** Verified Walk-in Cooler (`has_cold_storage = True`)
   - **Volume:** Can take [X] crates (Max capacity: [Y] pallets)
   - **Transport Action:** [Either "They have a refrigerated van and can self-collect" OR "⚠️ No vehicle—Coordinator must dispatch a volunteer driver"]
   - **Distance:** [X.X] miles from donor (`ST_DISTANCE`)
**4. The Clock:** 
   - **Donor Deadline:** [X] hours | **USDA Shelf Life:** [Y] hours
   - **Pickup Window:** Open today, can receive within [Z] hours. **Safety Margin: [X-Z] hours.**
**5. Equity Impact (Who It Helps):** Located in Census Tract [ID] — **[X]% No-Vehicle Households** (Chicago avg: 20%) and **[Y]% Poverty Rate**.
**6. Ready-to-Send Outreach Message:**
   > *"Hi [Org Name] team, Chicago Food Rescue has [Qty] of [Item] available from [Donor]. Needs pickup/delivery before [Time]. Our records show your cooler can fit this load. Reply YES to claim, and let us know if you need a volunteer driver!"*

---
**7. Backup Options & Rejected Decoys:**
* **Runner-Up (#2):** [Org Name] ([Distance] mi away | [X]% No-Vehicle Tract) — *Reason/Capacity summary*
* **Third Option (#3):** [Org Name] ([Distance] mi away | [X]% No-Vehicle Tract) — *Reason/Capacity summary*
* **Notable Decoy Filtered Out:** [Decoy Org Name] (Matched semantically, but eliminated because: `[Exact Failed SQL Constraint]`)
```

---

## 8. Technical Stack & Out-of-Scope Justification

* **Frontend:** ADK Web UI (Framed as an internal dispatch console for staff coordinators).
* **Orchestration:** Python ADK + Gemini 2.5 Flash/Pro.
* **Database & Search:** BigQuery (`a4i_food` dataset) + BigQuery Vector Search (`AI.EMBED` / `ML.GENERATE_EMBEDDING`) via MCP Toolbox.

### Out of Scope (Architectural Guardrails)
* **Public Donor Portal:** Our user is the internal coordinator fielding calls.
* **Live Turn-by-Turn Traffic:** Coordinates are ZIP-centroids; `ST_DISTANCE` straight-line calculation is the mathematically honest approach for this data granularity.
* **Transactional Pallet Locking:** BigQuery is an OLAP analytics warehouse, not an OLTP database (like Firestore/Cloud SQL). Building row-level concurrency locks for driver claims in BigQuery is an anti-pattern.

---

## 9. Success Metrics & KPIs
* **0% Decoy Failure Rate:** The agent never recommends a top semantic match that lacks cold storage or capacity.
* **Equity Audit Lift:** Across all 10 test postings in `surplus_postings`, matched recipients sit in tracts with an average `no_vehicle_rate` higher than the $20\%$ Chicago baseline.