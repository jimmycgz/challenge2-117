# Chicago Food Rescue Broker — Complete AngelHack Submission Package

Navigation: [Step-by-Step Demo Walkthrough](DEMO-SCRIPT.md) · [Short 2:33 Video Script](VIDEO-SCRIPT-3MIN.md) · [Visual Slide Deck (HTML/PDF)](pitch-deck.html) · [12-Slide Deck Outline](DECK-OUTLINE.md) · [Submission Checklist](SUBMISSION.md) · [Equity Audit](../agent/food_broker/EQUITY-AUDIT.md) · [Captured Evidence](evidence/README.md).

This document bundles **everything required for the Challenge 2 (Food Rescue & Redistribution Broker) final submission** at **`http://goo.gle/A4I-Submission`** (`https://portal.angelhack.com/a4i-console`).

---

## 📦 1. The 4 AngelHack Portal Submission Fields (Ready to Copy-Paste)

| # | Portal Field | Value to Paste / Upload | Verification Status |
| :--- | :--- | :--- | :--- |
| **1** | **GitHub Repository Link** | `https://github.com/jimmycgz/challenge2-117` *(Tagged `submission` on `main`)* | ✅ Public / Judge-Accessible |
| **2** | **Environment / Live Application Link** | - **Qwiklabs Lab Environment Link:** *(Paste the active Qwiklabs student lab URL from the Skills console)*<br/>- **Live Cloud Run ADK Dev UI:** `https://food-broker-817377390808.us-east1.run.app/dev-ui/`<br/>- **Live Cloud Run Health Check:** `https://food-broker-817377390808.us-east1.run.app/health` | ✅ Deployed (`food-broker-00012-jhq`, `gemini-3.8-flash` low thinking) |
| **3** | **Pitch Deck (PDF / Link)** | - **Visual Slide Deck:** [`docs/pitch-deck.html`](pitch-deck.html) *(Open in Chrome → `Ctrl+P` → **Save as PDF** → Upload PDF)*<br/>- **Markdown Deck Outline:** [`docs/DECK-OUTLINE.md`](DECK-OUTLINE.md) | ✅ Answers all 4 Mandatory Judge Checks |
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

## 🖥️ 3. Slide Deck Package (`docs/pitch-deck.html` & `docs/DECK-OUTLINE.md`)

### How to Export the PDF Pitch Deck in 10 Seconds
1. Open [`docs/pitch-deck.html`](pitch-deck.html) in Google Chrome.
2. Press **`Ctrl+P`** (or **`Cmd+P`** on macOS).
3. Set **Destination** to **Save as PDF**, **Layout** to **Landscape**, **Margins** to **None**, and check **Background graphics**.
4. Save as `Chicago-Food-Rescue-Broker-Pitch-Deck.pdf` and upload to the AngelHack portal.

### How the 12 Slides Answer Every Judge Rubric & Mandatory Check
- **Slide 1:** Title, Track 1 (Retail & Grocer Rescue), & Live Cloud Run / Repo Links.
- **Slide 2:** The 2 PM Thursday Grocer Problem & Verbatim 6-Part Spinach Match Brief.
- **Slide 3:** 6-Turn Coordinator Workflow (*"They said no"*, *"Why not Greenline?"*, *"Why not the Food Depository?"*).
- **Slide 4 (Mandatory Check #1 — Semantic Decoy):** Why `Greenline Community Pantry` (#1/#3 by meaning, no cooler, 12h pickup) is rejected and why `top_k=80` is required (`k=15 → 1`, `k=40 → 3`, `k=80 → 12`).
- **Slide 5 (Mandatory Check #2 — Time-to-Expiry & Transport):** Effective clock formula (`min(donor_hours, shelf_life_if_>=2h)`), the `< 2.0h` USDA opened-formula trap guard, and volunteer driver vs. recipient refrigerated van flags.
- **Slide 6 (Mandatory Check #3 — Cross-Track Generalization):** Zero per-track code changes across Retail Spinach (`0.5p`), Farm Potatoes (`5p`), Sealed Infant Formula (`168h`), and 1-Hour Bakery Safe Refusal.
- **Slide 7:** Single-Agent Architecture (`gemini-3.8-flash` low thinking + deterministic Python constraint filter + managed BigQuery MCP toolset + identity guard).
- **Slide 8 (Mandatory Check #4 — 10-Posting Equity Audit):** 3-way analysis across 1,004 Chicago census tracts and 183 real recipients (per-posting `21.9%` poverty, per-unique-recipient `17.6%`, and pallet-weighted `9.0% vs 19.3%` public assistance due to the 14 loading-dock bottleneck).
- **Slide 9:** Coordinator Dispatch Console UI (`frontend/index.html`) — Ticking Queue, Chicago Map, Crate Tag Vision, Voice Dictation, and Delay Re-Router.
- **Slide 10:** Stretch Goals Built (#6 Multi-Recipient Farm Load Splitter, #10 Pantry Intake Wizard, #11 Live openFDA Recall Gate + 3-Point Dock Checklist, #12 Stateful Pallet Locking & `HTTP 409` Conflict Guard, #13 Interactive Equity Counterfactual Explorer).
- **Slide 11:** Model & Speed Benchmarks (`gemini-3.8-flash` low thinking `41/42` behavior score vs `gemini-2.5-flash` `38/42`, `~20s` measured on Cloud Run).
- **Slide 12:** Honest Limits (183 real IRS names/addresses + 9 labeled teaching cases, generated storage/lead times, consumer shelf-life guidance, ZIP-level coordinates) & Next Steps.

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
# 1. Ensure main is up to date
cd /home/krishanr/challenge2-117
git checkout main && git pull origin main

# 2. Run the offline self-check (must pass in <2 seconds)
PYTHONPATH=agent python3 -m food_broker.selfcheck

# 3. Tag the final submission commit and push the tag
git tag -f submission
git push origin main --tags --force
```
