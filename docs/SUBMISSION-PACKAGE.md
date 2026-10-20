# Chicago Food Rescue Broker — Complete AngelHack Submission Package

Navigation: [Step-by-Step Demo Walkthrough](DEMO-SCRIPT.md) · [Short 2:33 Video Script](VIDEO-SCRIPT-3MIN.md) · [Visual Slide Deck (HTML/PDF)](pitch-deck.html) · [12-Slide Deck Outline](DECK-OUTLINE.md) · [Submission Checklist](SUBMISSION.md) · [Equity Audit](../agent/food_broker/EQUITY-AUDIT.md) · [Captured Evidence](evidence/README.md).

This document bundles **everything required for the Challenge 2 (Food Rescue & Redistribution Broker) final submission** at **`http://goo.gle/A4I-Submission`** (`https://portal.angelhack.com/a4i-console`).

---

## 📦 1. The 4 AngelHack Portal Submission Fields (Ready to Copy-Paste)

| # | Portal Field | Value to Paste / Upload | Verification Status |
| :--- | :--- | :--- | :--- |
| **1** | **GitHub Repository Link** | `https://github.com/jimmycgz/challenge2-117` *(Tagged `submission` on `main`)* | ✅ Public / Judge-Accessible |
| **2** | **Environment / Live Application Link** | - **Live Coordinator Dispatch Console (Cloud Run):** `https://food-broker-ui-817377390808.us-east1.run.app`<br/>- **Live Cloud Run ADK Dev UI:** `https://food-broker-817377390808.us-east1.run.app/dev-ui/`<br/>- **Qwiklabs Lab Environment Link:** *(Paste the active Qwiklabs student lab URL from the Skills console)* | ✅ Both Deployed (`food-broker-ui-00006-xbm` & `food-broker-00012-jhq`) |
| **3** | **Pitch Deck (PDF / Link)** | - **Ready-to-Upload 14-Slide PDF Deck (Table 17):** [`docs/RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) *(GitHub link: `https://github.com/jimmycgz/challenge2-117/blob/main/docs/RescueBroker-Pitch-Deck.pdf`)*<br/>- **Alternative HTML Deck / Outline:** [`docs/pitch-deck.html`](pitch-deck.html) · [`docs/DECK-OUTLINE.md`](DECK-OUTLINE.md) | ✅ Complete 14-Slide PDF Ready to Upload |
| **4** | **Pitch / Demo Video (≤ 3 Minutes)** | - **Click-by-Click Walkthrough Script:** [`docs/DEMO-SCRIPT.md`](DEMO-SCRIPT.md)<br/>- **Timed 2:33 Video Script:** [`docs/VIDEO-SCRIPT-3MIN.md`](VIDEO-SCRIPT-3MIN.md)<br/>- **Video Link:** *(Upload MP4 / YouTube Unlisted / Loom / Drive link before 16:59 EDT)* | ⏳ Record & Paste Link |

### Copy-Paste Project Summary (For Portal Description / Notes Field)
```text
Chicago Food Rescue Broker (Track 1: Retail & Grocer Rescue, generalizing across Track 2 Farm & Track 3 Essentials without per-track code changes).
A coordinator describes a perishable surplus offer (text, voice, or crate label photo), and the agent retrieves the 80 closest Chicago recipients by meaning using BigQuery VECTOR_SEARCH (gemini-embedding-001, COSINE), deterministically filters out recipients that cannot store the cold/frozen load, handle the pallet count, or collect before the expiry clock, and returns a 6-part Match Brief with a ready-to-send outreach SMS, 2 backups, and explicit semantic decoy rejection reasons.
Includes a full Coordinator Dispatch Console (frontend/index.html + frontend/serve.py), Google's managed BigQuery MCP toolset for read-only analytical queries, live openFDA recall checks, multi-recipient farm load splitting, stateful pallet locking, and a 3-way 10-posting equity audit across 1,004 Chicago census tracts.
```

---

## 📋 2. Verbatim 6-Part Match Brief Package (Primary Spinach + Cross-Track Proofs)

All live JSON and Markdown captures are stored in [`docs/evidence/`](evidence/README.md). Below is the verbatim **Primary Track 1 (Retail Spinach) 6-Part Match Brief** captured from the live service:

### A. Primary Track 1 — Retail Spinach (`docs/evidence/spinach-answer.md` & `spinach-brief.json`)

**Coordinator Input:**
> `A grocer in Chicago has ten crates of spinach, harvested yesterday, that must leave the dock within 6 hours and stay cold.`

**Tool Calls Executed:**
```text
lookup_shelf_life({"product_name": "Spinach", "storage_state": "refrigerated"})
find_matches({"hours_remaining": 6, "pallets": 0.5, "needs_cold": true, "donor_description": "A grocer in Chicago", "load_description": "ten crates of spinach"})
```

**Verbatim 6-Part Match Brief Output:**
> **1. Who, and why**
> Habibi Care, 4845 N WASHTENAW AVE, CHICAGO, IL 60625. They have domestic cold storage, can take up to 1 pallet, and collect within 3 hours.
>
> **2. What they can actually take**
> Their profile indicates they have domestic cold storage and can take up to 1 pallet. They do not have a loading dock or refrigerated transport. This is based on their profile on file; please confirm by phone.
>
> **3. The clock**
> The food has 6 hours remaining. Habibi Care's collection lead time is 3 hours, leaving a margin of 3 hours. A driver is needed as the food must stay cold and Habibi Care does not have refrigerated transport.
>
> **4. Whose neighborhood it helps**
> Habibi Care serves 165 households per week, primarily Families with children. The nearest census tract indicates 13% of residents are below the poverty line, 5% of households are without a vehicle, and 12% are on food or cash assistance.
>
> **5. The outreach message**
> Hello Habibi Care team,
> A grocer in Chicago has ten crates of spinach. It is still good but has to move soon. From what we have on file you have the storage for it. The food needs to leave by about 6 hours from now, which leaves you roughly 3 hours of slack to collect. We can arrange a driver, since it has to stay cold on the way.
> Can you take it? If you can, tell us the time you can collect and a phone number for pickup. If not, a quick no helps us move to the next place.
> Thank you, [Coordinator name]
>
> **6. The next two options & Rejected close matches**
> - **Backup #2:** Love Of Angels (4966 N KOLMAR AVE, CHICAGO, IL 60630) — domestic cold storage, takes up to 1 pallet, collects within 4h (+2h slack).
> - **Backup #3:** Good Food Pantry (808 SEELEY AVE, PARK RIDGE, IL 60068) — domestic cold storage, takes up to 1 pallet, collects within 3h (+3h slack).
> - **Rejected but close matches:**
>   - `Greenline Community Pantry` (invented teaching case), ranked **1st by meaning**, removed: `no cold storage; needs 12h to collect, food has 6h`
>   - `Tca Health Inc Nfp`, ranked **2nd by meaning**, removed: `needs 18h to collect, food has 6h`
>   - `Go Forth International`, ranked **3rd by meaning**, removed: `needs 21h to collect, food has 6h`

### B. Additional Captured Match Briefs & Transcripts in `docs/evidence/`

| Scenario | Markdown Answer | Raw JSON Brief | Key Proof Demonstrated |
| :--- | :--- | :--- | :--- |
| **Track 1 — Retail Spinach (`6h`, `0.5p`, Cold)** | [`spinach-answer.md`](evidence/spinach-answer.md) | [`spinach-brief.json`](evidence/spinach-brief.json) | 6-part Match Brief, `Greenline` no-cooler decoy caught, +3h slack buffer |
| **Track 2 — Farm Potatoes (`72h`, `5p`, Dry)** | [`farm-potatoes-answer.md`](evidence/farm-potatoes-answer.md) | [`farm-potatoes-brief.json`](evidence/farm-potatoes-brief.json) | Household fridges & 1–4p pantries filtered out; routed to loading dock |
| **Track 3 — Sealed Infant Formula (`168h`, `0.5p`)** | [`sealed-formula-answer.md`](evidence/sealed-formula-answer.md) | [`sealed-formula-brief.json`](evidence/sealed-formula-brief.json) | Catches USDA `1.0h` opened-bottle shelf-life trap; honors `168h` sealed clock |
| **Safe Refusal — Bakery Pastries (`1.0h`, `0.25p`)** | [`no-match-bakery-answer.md`](evidence/no-match-bakery-answer.md) | [`no-match-bakery-brief.json`](evidence/no-match-bakery-brief.json) | Zero pantries can collect in 1h (fastest is 2h); refuses safely without guessing |
| **6-Turn Coordinator Follow-Up Conversation** | [`follow-ups-transcript.md`](evidence/follow-ups-transcript.md) | — | *"They said no"*, *"Why not Greenline?"*, *"Why not Food Depository?"*, *"Can we split 10p?"* |
| **Managed BigQuery MCP Query (`6 of 183`)** | [`mcp-walk-in-answer.md`](evidence/mcp-walk-in-answer.md) | — | Read-only BigQuery MCP query filtering `profile_source != 'planted'` (`6 / 183 = 3.28%`) |
| **Vector Pool Size Ablation (`k=15, 40, 80`)** | [`pool-study.txt`](evidence/pool-study.txt) | — | Proves why `top_k=80` is required (`k=15` leaves 1 viable; `k=80` leaves 12 viable) |
| **Automated Test Suite & Timings** | [`test-suite.txt`](evidence/test-suite.txt) · [`validation.txt`](evidence/validation.txt) | [`model-call-timings.txt`](evidence/model-call-timings.txt) | `15/15` behavior checks on `gemini-3.8-flash` (low thinking), `~20s` Cloud Run latency |

---

## 🖥️ 3. Slide Deck Package ([`docs/RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) & [`docs/pitch-deck.html`](pitch-deck.html))

### Primary Ready-to-Upload PDF Deck (`docs/RescueBroker-Pitch-Deck.pdf` — 14 Slides, Table 17)
The official Google Cloud *Agents for Impact · Build with Gemini* 14-slide PDF deck is saved at [`docs/RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) and maps to every judging question:

- **Slide 1:** Title (`RescueBroker — Surplus food to the right pantry, under a clock · Table 17 · Challenge 2 · Track 1, retail and grocer rescue, Chicago`).
- **Slide 2:** *A matching problem under a clock* (10 crates of spinach, 6 hours left: What just became available, Who could use it, What can they store, How long does it have).
- **Slide 3:** *From a text message to a call-ready brief* (`Food clock → Search by meaning (80 closest) → Hard filters (Cold · room · time) → Rank (Safe margin first) → Match Brief (Message ready to send)`).
- **Slide 4:** *How the pieces fit* (Cloud Run `food_broker` ADK agent, Identity guard, `lookup_shelf_life`, `find_matches`, `explain_candidate`, Google-managed BigQuery MCP, and BigQuery `a4i_food` with `192 (9 invented)` recipients).
- **Slide 5 (Mandatory Check — Semantic Decoy & Pool Study):** *Meaning alone picks the wrong pantry* (3 closest by meaning eliminated including the no-fridge decoy; `Top 15 → 1 viable | Top 40 → 3 viable | Top 80 → 12 viable`).
- **Slide 6:** *From 80 candidates to one call* (`80 Closest by meaning → 12 Pass hard filters → 3 Ranked options → 1 Message ready to send`).
- **Slide 7:** *When a pantry says no, the next call is ready* (`Brief sent → They say no → Search again (Skips everyone who declined) → Next brief`).
- **Slide 8 (Mandatory Check — Cross-Track Generalization):** *One pipeline for every kind of surplus* (`Grocer produce: 10 crates spinach`, `Farm surplus: 5 tons potatoes`, `Family essentials: 48 cases sealed formula`, `No match: 40 trays cream pastries in 1 hour`).
- **Slide 9:** *Ten offers, how many pantries can take each?* (Bar chart across all 10 offers: `1 to 46 pantries can take an offer — blueberries: 1, diapers: 46`).
- **Slide 10 (Mandatory Check — Edge Cases & Read-Only MCP):** *What the agent decides for itself* (`Nobody can take it? It says so`, `Sealed formula is not a 1-hour item`, `A kitchen fridge is not a cooler (≤ 1 pallet)`, `Data questions use a read-only tool (SELECT only)`).
- **Slide 11 (Mandatory Check — 10-Posting Equity Audit):** *Per offer, close to the corpus; big loads, less assistance* (`All 183 recipients` vs `Per offer (10)` vs `Per recipient (8)` vs `Weighted by pallets: 9% assistance against 19%`).
- **Slide 12 (Mandatory Check — Honest Limits & Next Steps):** *Limits today, and what is next* (Real names except 9 invented test cases, generated storage/pickup times, ZIP-level locations, consumer shelf-life guidance, `23/25` notebook validation checks, and Next: *Remember who got food* & *Split a big load*).
- **Slide 13 & Slide 14:** *Thank you* + *Backup: the full diagram* (including `Inside find_matches` sub-pipeline).

*(Note: [`docs/pitch-deck.html`](pitch-deck.html) is also included in `docs/` as an interactive HTML companion that embeds the verbatim 6-part Spinach Match Brief text and UI screenshots.)*

---

## 🗂️ 4. Code Repository & Architecture Package (`jimmycgz/challenge2-117`)

| Component | Path in Repository | Purpose |
| :--- | :--- | :--- |
| **Root Overview & Quickstart** | [`README.md`](../README.md) | Judge entry point linking architecture, audit, evidence, and setup |
| **ADK Agent & System Prompt** | [`agent/food_broker/agent.py`](../agent/food_broker/agent.py) | `food_broker` agent (`gemini-3.8-flash`, `low` thinking), identity guard, and managed BigQuery MCP integration |
| **Deterministic Tool Pipeline** | [`agent/food_broker/tools.py`](../agent/food_broker/tools.py) | `find_matches`, `explain_candidate`, `lookup_shelf_life`, `apply_constraints`, `build_match_brief` |
| **Offline Self-Check & Invariants** | [`agent/food_broker/selfcheck.py`](../agent/food_broker/selfcheck.py) | Automated unit & regression tests (decoy rejection, sealed formula guard, freezer filter, identity guard) |
| **Functional Test Suite** | [`agent/food_broker/test_suite.py`](../agent/food_broker/test_suite.py) · [`test_questions.json`](../agent/food_broker/test_questions.json) | 7 coordinator stress-test questions & live verification runner |
| **10-Posting Equity Study** | [`agent/food_broker/EQUITY-AUDIT.md`](../agent/food_broker/EQUITY-AUDIT.md) · [`equity_audit.py`](../agent/food_broker/equity_audit.py) | Reproducible 3-way demographic & capacity bottleneck audit over 183 real orgs + 9 planted cases |
| **Coordinator Dispatch Console** | [`frontend/index.html`](../frontend/index.html) · [`frontend/serve.py`](../frontend/serve.py) | 5-view operational web console + local CORS proxy & transactional `/api/state/*` reservation engine |
| **Engineering Design Document** | [`docs/DESIGN.md`](DESIGN.md) | Full system design, failure taxonomy, and `gemini-3.8-flash` vs `gemini-2.5-flash` evaluation |

---

## 🚀 5. Final Pre-Submission Freeze Commands (Run Before Submitting)

```bash
# 1. From the repository root, ensure main is up to date
git checkout main && git pull origin main

# 2. Run the offline self-check (must pass in <2 seconds)
PYTHONPATH=agent python3 -m food_broker.selfcheck

# 3. Tag the final submission commit and push the tag
git tag -f submission
git push origin main --tags --force
```
