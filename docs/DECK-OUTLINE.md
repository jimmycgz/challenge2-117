# Deck outline: RescueBroker — Coordinator Dispatch Console & Food Equity Broker

Navigation: [demo script](DEMO-SCRIPT.md) · [submission checklist](SUBMISSION.md) ·
[agent README](../agent/food_broker/README.md) · [equity audit](../agent/food_broker/EQUITY-AUDIT.md) ·
[design & benchmarks](DESIGN.md).

Eight slides. Judges score the deck and the video asynchronously after the event with no Q&A, so every differentiator,
benchmark, and rigor check is stated directly on the slides below. Front-load it: assume nobody reaches the last slide.

---

## 1. The Thursday 2:10 PM Reality: Why Chatbots Fail a Ticking Clock

We coordinate food rescue in Chicago. A grocer has just offered **ten crates of fresh spinach** and it has to leave their
dock within **6 hours** and stay cold. Here is who we would call, and what we do not know about them.

- **The 4-Question Bottleneck:** Answering *what just arrived, who wants it, what they can physically store, and whether
  they can collect before the dock closes* takes a human coordinator 40 minutes of phone tag across spreadsheets.
- **Why We Built a Dispatch Console, Not Just a Chat Box:** Most teams stop at raw `adk web`. A staff dispatcher managing
  11 expiring offers cannot scroll through a developer chat log—they need a **Ticking-Clock Queue**, a **scannable 6-Part
  Match Brief**, **spatial map verification**, and **1-click SMS/decline workflows**.
- **Data Provenance Up Front (Judge Check #1):**
  - **Real:** **183 IRS 990 tax-exempt organizations** in Chicago (names, addresses, NTEE codes, reported income),
    **USDA FoodKeeper** shelf life (661 products), and **US Census ACS** tract demographics (1,004 tracts).
  - **Invented / Generated:** **9 planted teaching cases** added by the challenge (`profile_source = 'planted'`, with no
    real street/ZIP), plus all operational fields (`cold_storage`, `max_pallets`, `pickup_window_hours`,
    `refrigerated_transport`).

---

## 2. User Experience: The RescueBroker SaaS Coordinator Console (`frontend/index.html`)

Built specifically for our primary persona (**Internal Dispatch Staff**) with **5 operational views + a collapsible Right
Agent Copilot** connected live to Cloud Run:

1. **Ticking-Clock Dispatch Queue & Match Brief Hero Card:**
   - Color-coded urgency pills (`🔴 <= 2h`, `🟡 <= 6h`, `🟢 > 6h`), **openFDA Recall Safety Strip**, **4-KPI Capacity &
     Buffer Bar**, ready-to-copy SMS, and a 1-click **"Recipient Declined — Next Option"** pivot button.
2. **Spatial Map & Multi-Stop Route / Load-Split Planner:**
   - Plots the **183 real IRS recipients** across Chicago (explicitly labelling the 9 invented teaching cases rather than
     plotting fake coordinates), plus corridor **Milk-Run grouping** and **multi-pantry load splitting** for oversized farm loads.
3. **Pantry Network Directory (192 Orgs) & Conversational Intake:**
   - Filters by walk-in cooler, loading dock, and refrigerated van, and includes a **Pantry Onboarding** workflow to close
     the loop on missing public operational data.
4. **openFDA Safety Gate & Driver Incident Log:**
   - Live CC0 federal recall check (`api.fda.gov`) + mid-route driver delay re-routing (`recalculateWithDelay`) and
     door-rejection reporting.
5. **Multimodal & Multi-Turn Agent Copilot Drawer (`food_broker`):**
   - Supports **Voice dictation**, **Pallet/Crate Tag Photo scanning**, and live multi-turn follow-ups (*"They said no"*,
     *"Why not X?"*, and free-form BigQuery MCP SQL queries).

---

## 3. Architecture & Our 42-Run Model Benchmark (`docs/DESIGN.md`)

**Why 1 Single ADK Root Agent + 4 Deterministic Tool Surfaces Beats a Multi-Agent Chain:**
Passing 80 candidate rows between LLM sub-agents took **76–86 seconds per hop (>3 minutes total)**. Keeping vector
candidate retrieval, hard constraint filtering, tiered ranking, and brief assembly inside deterministic Python functions
(`agent/food_broker/tools.py`) cuts response time to **about 20 seconds** on warm Cloud Run (`min-instances=1`; 19.9, 22.5 and 20.3 s on `gemini-3.8-flash` at low thinking, one sample each) and enables
100% offline unit verification (`selfcheck.py`).

- **`lookup_shelf_life`:** Queries `a4i_food.shelf_life` + injects `_shelf_caution` when `hours <= 2` (catching opened-container traps).
- **`find_matches`:** BigQuery `VECTOR_SEARCH` (`gemini-embedding-2`, `top_k=80`) $\rightarrow$ hard constraint filter $\rightarrow$ tiered safety ranking $\rightarrow$ `ST_DISTANCE` nearest census tract lookup $\rightarrow$ 6-part Match Brief + guaranteed cold-storage decoy log.
- **`explain_candidate`:** Searches the `top_k=80` pool for any named organization (*"Why not Greenline?"* / *"Why not the big food bank downtown?"*) and reports its exact `semantic_rank` and failed constraint.
- **Google's Managed BigQuery MCP Server (`https://bigquery.googleapis.com/mcp`):** Read-only `execute_sql` / `get_table_info` for ad-hoc coordinator questions outside a posting, guarded by `identity_guard.py`.
- **Empirical Model Selection (14 checks × 3 runs = 42 runs):** We benchmarked `gemini-3.8-flash` (low thinking: **41/42 checks**, no prompt-injection leaks, **15.6–17.2 s** for a full spinach answer run locally and alone, 22.5–28.5 s in later local runs) against `gemini-2.5-flash` (**38/42 checks, 17.8–20.0s**, leaked SQL on 1 of 3 prompt-injection tests).

---

## 4. Why Meaning Is Not Enough: The `top_k=80` Pool Study & Rank #3 Decoy (Judge Check #2)

For the 6-hour spinach offer across 192 Chicago recipients, **the three closest recipients by meaning were all wrong**:
- All three needed longer to collect than the food had (`12h–21h` vs. `6h`).
- **Ranked 3rd by meaning (`Greenline Community Pantry` — an invented teaching case in the challenge data):** Writes that
  its families *"ask most for fresh greens"*—and has **no refrigeration of any kind (`cold_storage = 'none'`)**.
- **Measured Candidate Pool Study ([`pool-study.txt`](evidence/pool-study.txt)):**
  - `top_k = 15` leaves **1** viable recipient | `top_k = 40` leaves **3** | `top_k = 80` leaves **12** (giving 9 backup options when pantries decline).
- **Why Our Tiered Ranking Picks Semantic Ranks #50, #54, and #63 Over Rank #11 ([`demo-tracks.txt`](evidence/demo-tracks.txt)):**
  - The nearest candidate by meaning that passes hard filters sits at **11th**, but only has a **household fridge (`domestic`)** and **1 hour of slack**.
  - Our ranking models slack as a **comfortable safety tier (`>= max(2h, 25% of clock)`)**, then prioritizes **sturdy commercial/vehicle cold storage (`REAL_COLD`)** and **own refrigerated transport** over raw embedding distance—picking **#50, #54, and #63** (which have 2–3 hours of buffer and, for #50, a refrigerated vehicle).
- **Mutation-Tested Filter:** `selfcheck.py` includes a test that disables the cold-storage rule to verify the test suite catches the decoy (which caught a real sorting bug in our v1 build).

---

## 5. One Corpus, Three Tracks — Zero Track-Specific Rulebooks

Retail spinach, five tons of farm potatoes, and sealed infant formula run through the exact same corpus, embedding search, and constraint pipeline (`docs/evidence/demo-tracks.txt`):

| Track | Posting | Viable (`top_k=80`) | How the Same Pipeline Adapts |
|---|---|---|---|
| 🛒 **Retail Rescue** | **10 crates of spinach** (`0.5 pallets`, `6h` clock, cold) | **12 of 80** | Eliminates no-fridge & slow-pickup decoys; selects fast neighborhood pantry (`3–4h` pickup) and flags volunteer driver dispatch. |
| 🚜 **Farm Surplus** | **5 tons of potatoes** (`~5 pallets`, `72h` clock, ambient) | **10 of 80** | Eliminates 169 small pantries; routes to high-capacity warehouse operation with `7–12 pallets` room and loading dock. |
| 🍼 **Critical Essentials** | **48 cases sealed infant formula** (`8 months` expiry, `2 pallets`) | **26 of 80** | Matches infant/family clinics while overriding the 1-hour prepared-formula FoodKeeper table artifact. |

---

## 6. Five Non-Obvious Engineering Safeguards We Built

1. **Catching the USDA FoodKeeper "1-Hour Formula" Trap (`_shelf_caution`):**
   - `a4i_food.shelf_life` gives `Infant formula` **1 hour** (a prepared/opened bottle figure). `lookup_shelf_life` warns on any figure `<= 2h` so the agent uses the donor's 8-month sealed expiry instead of falsely rejecting the load.
2. **Household Fridge ≠ Walk-In Cooler (`DOMESTIC_FRIDGE_PALLETS = 1`):**
   - Unlike boolean `cold_storage != 'none'` filters that route 4 pallets of produce to a church kitchen fridge, our filter caps `domestic` cold storage at **1 pallet max**.
3. **Sanitizing Contradictory Profile Timing Claims (`_excerpt` in `tools.py`):**
   - Because profiles are template-generated, a recipient's `profile_text` can claim *"we can be there within a couple of hours"* while its numeric `pickup_window_hours` column is `19h`. Both our code and prompt strip timing claims from prose excerpts so only the verified column governs the clock.
4. **Safe Refusal When Viable = 0 (`no-match-bakery-answer.md`):**
   - On **40 trays of cream-filled pastries with a 1-hour dock deadline**, `0 of 80` pass. The agent refuses to guess and lists the closest rejections with their exact time shortfall.
5. **Read-Only BigQuery MCP + Lab Identity Guard (`mcp-walk-in-answer.md`):**
   - Free-form SQL questions (*"Not counting the invented teaching cases, how many recipients have walk-in cold storage?"* $\rightarrow$ **`6 of 183 (3.3%)`**) run via Google's Managed BigQuery MCP server, strictly isolated from posting matches and locked to the lab GCP identity.

---

## 7. The 3-Lens Cold-Reviewed Equity Audit (Judge Check #3)

**Did the food go where the need is, or where the loading docks are?**
We excluded the **9 invented teaching cases** (whose coordinates sit at the metro center by formula) and audited all **10 `surplus_postings`** across the **183 real IRS recipients** (on 68 distinct census tracts) three ways ([`EQUITY-AUDIT.md`](../agent/food_broker/EQUITY-AUDIT.md)):

| Comparison Group (183 Real Chicago Recipients) | n | Poverty (Mean / Med) | No Vehicle (Mean / Med) | Assistance (Mean / Med) |
|---|---|---|---|---|
| **Chicago Metro Baseline** (pop-weighted) | 1,004 tracts | **15%** / — | **20%** / — | **18%** / — |
| **All Real Recipients Corpus** | 183 orgs | **19%** / 16% | **28%** / 27% | **19%** / 12% |
| **Lens 1: Top Matches — Once Per Posting** | 10 postings | **22%** / 16% | **30%** / 23% | **19%** / 11% |
| **Lens 2: Top Matches — Once Per Distinct Recipient** | 8 orgs | **16%** / 10% | **24%** / 20% | **15%** / 6% |
| **Lens 3: Top Matches — Weighted by Pallets** | 37.5 pallets | **14%** / — | **32%** / — | **9%** / — |
| **Recipients w/ Dock or 5+ Pallets** | 14 orgs | **17%** / 14% | **29%** / 27% | **16%** / 14% |

- **What Our Cold Review Caught (That a Simple Average Hides):**
  - **The Repeat-Winner Effect:** Counted per posting, matches sit above the corpus on mean poverty (`22% vs 19%`) and no-vehicle (`30% vs 28%`) only because **one fast pantry** (*Shakespear Rose Community Table*, in a `45% poverty / 52% no-vehicle` tract) won 3 short-clock retail postings. Counted once per distinct recipient (`n=8`), matches sit **lower on all three measures** (`16% / 24% / 15%`).
  - **The Volume / Loading-Dock Skew:** The 3 farm loads account for **30 of the 37.5 pallets**. Weighted by pallets, assistance drops to **9% vs. 19% corpus mean**, because large loads can only go to the **14 real recipients** with 5+ pallet capacity (10 have room for 10+ pallets).
  - **Responsible AI Separation:** Census tract figures are looked up *after* ranking (`lookup_neighborhood`) so demographic composition is never used to score who "deserves" food.

---

## 8. Honest Limitations & Production Roadmap (Judge Check #4)

- **Four Explicit Boundaries Today:**
  1. **Real vs. Generated Split:** 183 recipient names/addresses/income are real IRS records (plus 9 invented teaching cases); all storage, pallet capacity, and pickup windows are generated—so every brief instructs the coordinator to confirm by phone before rolling a truck.
  2. **Consumer Shelf-Life Guidance:** USDA FoodKeeper reflects home storage, not commercial cold-chain telemetry.
  3. **ZIP-Centroid Spatial Resolution:** Recipient coordinates are ZIP-level centroids matched to the nearest tract internal point (`ST_DISTANCE`), describing the surrounding area rather than the exact building block, and `surplus_postings` carries no donor coordinates.
  4. **Small Audit Sample & No Delivery Memory:** 10 postings across 68 tracts cannot separate statistical skew from noise, and without persistent delivery history one well-equipped pantry wins repeated short-clock offers.
- **What Comes Next:**
  - **Persistent Delivery Rotation & Pallet Locks (Firestore — Issue #12):** Track daily claims and declines so offers rotate across viable pantries.
  - **Backend Multi-Recipient Load Splitter (Issue #13):** Automatically split 5-ton farm loads across 2–3 pantries in `find_matches` when no single cooler can take the full volume.
  - **Live Pantry Self-Onboarding (Issue #10):** Replace synthetic operational profiles by interviewing pantry managers directly into BigQuery + `AI.EMBED`.

---

## Where Each Judging Dimension Is Answered

| Dimension | Weight | Answered On |
|---|---:|---|
| **Impact & Insight** | 30 | Slides 1–2 (Coordinator Console UX, Ticking-Clock Queue, 6-Part Match Brief, "They said no" & "Why not X?" flows) |
| **Technical Execution** | 30 | Slides 3–5 (Live Cloud Run service, `VECTOR_SEARCH` pool study `15->1, 40->3, 80->12`, 3 tracks through 1 corpus) |
| **Rigor & Judgment** | 25 | Slides 4, 6, 7 & 8 (Rank #3 decoy, 1h formula bug, domestic fridge cap, 3-lens equity audit, 183 vs 9 planted split, 42-run model benchmark) |
| **Craft & Communication** | 15 | Slide 2 & Video (SaaS Dispatch Console + live Cloud Run Agent Copilot + crisp 6-part card formatting) |
| **Bonus — Range** | +10 | Slides 2, 3 & 6 (Google Managed BigQuery MCP Server, Custom SaaS Dispatch Console w/ Google Maps & openFDA Recall Gate, Multimodal Voice/Photo Intake, Vertex AI + Cloud Run) |

