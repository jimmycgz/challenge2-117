# Step-by-Step Demo Walkthrough & Click-by-Click Recording Script (~2:40)

Navigation: [Submission Package](SUBMISSION-PACKAGE.md) · [Visual Slide Deck (HTML/PDF)](pitch-deck.html) · [Deck Outline](DECK-OUTLINE.md) · [Short 2:33 Video Plan](VIDEO-SCRIPT-3MIN.md) · [Submission Checklist](SUBMISSION.md) · [Equity Audit](../agent/food_broker/EQUITY-AUDIT.md) · [Captured Evidence](evidence/README.md).

This guide provides **exact step-by-step mouse click instructions**, **on-screen visual cues**, **copy-paste prompts**, and **spoken narration** so you can record a smooth, under-3-minute demo video (or run a live judge walkthrough) without guessing what to click next.

---

## 🛠️ Pre-Flight Setup (Do This 1 Minute Before Recording)

You do **not** need to start anything locally — the Coordinator Dispatch Console is live on Cloud Run!

1. **Open the Live Cloud Run Coordinator Dispatch Console:**
   - **`https://food-broker-ui-817377390808.us-east1.run.app`**
2. **Open Supporting Tabs in the Same Browser Window (Left to Right):**
   - **Tab 1 — Visual Pitch Deck:** [`docs/pitch-deck.html`](pitch-deck.html)
   - **Tab 2 — Live Coordinator Dispatch Console (Cloud Run):** `https://food-broker-ui-817377390808.us-east1.run.app` (starts on the **RescueBroker Splash Screen**).
   - **Tab 3 — Live Cloud Run ADK Dev UI (Optional backup view):** `https://food-broker-817377390808.us-east1.run.app/dev-ui/` (select `food_broker`).
   - **Tab 4 — Captured Evidence & Equity Audit:** [`agent/food_broker/EQUITY-AUDIT.md`](../agent/food_broker/EQUITY-AUDIT.md) and [`docs/evidence/pool-study.txt`](evidence/pool-study.txt).
3. **Choose Your Timing Mode in Tab 2 (`https://food-broker-ui-817377390808.us-east1.run.app`):**
   - **Live Cloud Run Mode (Default):** Keep **`Live Matching`** checked in the top bar. Each live call to `gemini-3.8-flash` (low thinking) takes **`~20 seconds`** on Cloud Run — talk over the first 10–12 seconds and trim the remaining wait in your video editor.
   - **Instant Saved-Run Mode (Zero Wait):** Uncheck **`Live Matching`** in the top bar when switching between Spinach, Potatoes, Sealed Formula, and Cream Pastries to display the authentic captured Cloud Run Match Briefs instantaneously (`<50ms`).

---

## 🎬 Minute-by-Minute Click-by-Click Walkthrough (`2:40` Total)

### Beat 1 — The Problem & Entering the Dispatch Console (`0:00 – 0:20` | 20s)

#### 🖱️ Exact Click Instructions
1. Start recording on **Tab 2 (`https://food-broker-ui-817377390808.us-east1.run.app`)** showing the **RescueBroker Splash Overlay** with the 3 Persona Entry Cards (*Rescue Coordinator*, *Pantry Manager*, *Driver & Route Planner*).
2. At **`0:08`**, click the green button **`[ Launch as Rescue Coordinator → ]`** (or **`[ Launch Live Dispatch → ]`** at the top right).
3. Move your cursor across the 3 workspace columns:
   - **Left Column:** *Donations Waiting (`11`)* sorted by urgency (`1.0h` red to `10d` green).
   - **Center Column:** *Chicago Pantry & Driver Map* + *Match Recommendation Card*.
   - **Right Column:** *Assistant Chat, FAQ & Get Help*.

#### 🗣️ What to Say Out Loud
> *"Hi, I'm [Your Name]. Our primary track is Retail and Grocer Rescue in metro Chicago. It's Thursday afternoon, and a grocer has ten crates of fresh spinach that must leave their loading dock within six hours and stay cold. Normally, finding who needs greens, who has working cooler space, and who can pick up in time takes 45 minutes of phone tag—so we built RescueBroker."*

---

### Beat 2 — The Spinach Offer & The 6-Part Match Brief (`0:20 – 0:55` | 35s)

#### 🖱️ Exact Click Instructions
1. In the left **Donations Waiting** list, click the 3rd item: **`10 Crates Fresh Spinach · 6h left · 0.5 pallet · Needs Cooler`**.
   - *(If demonstrating a live call in the Right Assistant panel: click **`[ Send ↵ ]`** to send the pre-filled prompt:)*
     ```text
     A grocer in Chicago has ten crates of spinach, harvested yesterday, that must leave the dock within 6 hours and stay cold.
     ```
2. When the **Best Match Card** appears in the center column:
   - Point your mouse at **Part 1 (`#1 Best Match: Habibi Care`, 3843 W Lawrence Ave, 60625)**.
   - Point to **Part 2 & 3** in the 4-box summary grid:
     - **Cooler & Space:** `Domestic Fridge (0.5 of 2 pallets)`
     - **Pickup Timing:** `4h notice needed → +2.0h safe buffer before 6h deadline`
     - **Driver / Van:** `Needs Volunteer Driver`
   - Point to **Part 4 (`Ready-to-Send Text Message`)** and click **`[ Copy Text ]`**, then click **`[ ✓ 2. Confirm Delivery ]`** to show the pallet reservation lock (`Step 2/3 · On the Way`).

#### 🗣️ What to Say Out Loud
> *"The agent pulls the 80 closest Chicago recipients by meaning using BigQuery `VECTOR_SEARCH`, then removes anyone who can't keep the food cold, take the pallet size, or collect before the deadline. Recipient names and addresses are real IRS records—except nine invented teaching cases planted in the challenge data—while storage, capacity, and pickup windows are generated.*
> *Every recommendation is a six-part Match Brief: who to call and why, what they can take, the clock and safety buffer, whether we need a volunteer driver, neighborhood need, and a ready-to-send text message."*

---

### Beat 3 — Catching the Semantic Decoy (`Greenline`) & Why `top_k = 80` (`0:55 – 1:35` | 40s)

#### 🖱️ Exact Click Instructions
1. Scroll slightly down on the center Match Card and click the toggle bar:
   **`▶ Show Backup Pantries & Why Others Were Skipped (2 backups · 3 skipped)`**
2. Point to the right-hand list (**`Why Close Matches Were Skipped`**):
   - Highlight **`Greenline Community Pantry (Semantic Rank #3)`** — point to its red pill: **`no refrigeration, pickup takes 12h, only 6h left`**.
   - Highlight **` Pilsen Neighborhood Food Hub (#1)`** and **`Southwest Families Feeding Network (#2)`** — skipped because their pickup windows (`12h` and `21h`) exceed `6h`.
3. Click the red decoy marker on the **Chicago Map** (or switch briefly to **`docs/evidence/pool-study.txt`**) to show the pool-size numbers (`k=15 → 1 viable`, `k=40 → 3 viable`, `k=80 → 12 viable`).

#### 🗣️ What to Say Out Loud
> *"Here is why semantic search alone is dangerous for perishable food: in our saved spinach run, the top three matches by meaning were all eliminated. **Greenline Community Pantry**—an invented teaching case in the challenge data—ranked third by meaning because its profile says families ask most for fresh greens, yet it has **no refrigeration of any kind** and needs 12 hours notice.*
> *The nearest recipient that actually passes every constraint is **11th by meaning**. In our pool study, fetching only 15 candidates left just 1 viable pantry, 40 left 3, and 80 left 12. And instead of stopping at the 11th rank—which only has 1 hour of slack—our ranking promotes safer recipients with 2 to 3 hours of breathing room. We even enforce a unit test in `selfcheck.py` that fails if a cold-storage rejection isn't surfaced—which caught a sorting bug in our first build."*

---

### Beat 4 — Multi-Turn Re-Routing: `"They Said No"` & `"Why Not the Food Bank?"` (`1:35 – 1:58` | 23s)

#### 🖱️ Exact Click Instructions
1. On the Match Card action bar, click **`[ ✗ 3. Pantry Said No ]`** (or click the **`They said no`** quick-chip above the right-hand Assistant input box):
   ```text
   They said no. Who's next?
   ```
2. In the amber recovery bar that opens on the card, click **`[ Switch to Backup #2 Now ]`** (or let the live Assistant reply finish). Point to the updated Best Match card and the **`Reserved Space & Declines (1)`** tab badge incrementing.
3. Optional follow-up chip: click **`Why not Greenline?`** in the right Assistant bar to show `explain_candidate`.

#### 🗣️ What to Say Out Loud
> *"When a volunteer-run pantry doesn't answer or turns the load down, one click records the decline, locks them out of today's repeat calls, and re-runs the search with `exclude_names` to brief the next viable pantry immediately."*

---

### Beat 5 — Cross-Track Generalization & Stretch UX (`1:58 – 2:20` | 22s)

#### 🖱️ Exact Click Instructions
1. *(Uncheck `Live Matching` in the top header if you want instant zero-wait transitions across these 3 cards:)*
   - In the left **Donations Waiting** queue, click **`5 Pallets Russet Potatoes (3d left · 5p · Dry OK)`** → point to **`St. Moses the Black Parish Food Pantry`** (loading dock, 8-pallet capacity).
   - Click **`48 Cases Sealed Infant Formula (7d left · 0.5p)`** → point to the **`Sealed Package Rule`** note (`168h` donor clock honored instead of the `1h` opened-bottle USDA figure).
   - Click **`40 Trays Cream Pastries (1.0h left · 0.25p)`** → point to the red **`No Safe Pantry Match`** alert (`1.0h < 2.0h fastest pickup`) and the 3 recovery buttons (*Ask Donor for +1.5h*, *Route to Walk-In Cooler Hub*, *Divert to Meal Kitchen*).
2. In the far-left navigation rail, click **`Split Loads`** (`view-routes`) for 3 seconds to show the **10-Pallet Farm Blueberry Load Splitter (`#6`)**, and click **`FDA Recalls`** (`view-safety`) to show the **live openFDA check + 3-Point Dock Safety Checklist (`#11`)**.

#### 🗣️ What to Say Out Loud
> *"With zero per-track code changes, the same pipeline routes five tons of farm potatoes to a loading dock, catches a 1-hour opened-bottle USDA trap on sealed infant formula, and safely refuses a 1-hour bakery offer that no pantry can collect in time—while giving coordinators a multi-recipient load splitter for 10-pallet farm harvests and a live openFDA recall check."*

---

### Beat 6 — Managed BigQuery MCP (`6 of 183`), 10-Posting Equity Study & Honest Close (`2:20 – 2:40` | 20s)

#### 🖱️ Exact Click Instructions
1. In the far-left navigation rail, click **`Impact Study`** (`view-equity`).
2. Point to the top KPI cards and the 5-row **Community Impact & Neighborhood Reach** table (`1,004 tracts`, `183 verified pantries`, `14 dock orgs`, `169 neighborhood pantries`, `10 postings`).
3. Click the segmented toggle **`[ 183 Verified Orgs (Default) ]` ↔ `[ With 9 Sample Cases (192) ]`** once to show the counterfactual explorer (`#13`), and point to the 10-Posting table below.
4. *(If showing the BigQuery MCP query, click **`🏢 Walk-In Coolers (MCP)`** in the top header bar or show `docs/evidence/mcp-walk-in-answer.md`: `6 of 183 real recipients = 3.28%`).*

#### 🗣️ What to Say Out Loud
> *"Ad-hoc data questions run read-only through Google's managed BigQuery MCP toolset: excluding the nine planted cases, six of the 183 real recipients have a walk-in cooler.*
> *And in our 10-posting equity study across 1,004 Chicago census tracts: counted per posting, our top matches sit at 22% poverty versus 15% citywide—but counted per unique recipient they sit slightly below the corpus mean because one fast pantry won three retail offers, and weighted by pallets public assistance is 9% versus 19% because 30 of the 37.5 pallets are bulk farm loads restricted to the 14 loading-dock orgs. Ten postings can't separate a real skew from noise.*
> *Because profiles are generated, shelf life is consumer guidance, and coordinates are ZIP-level, the brief always reminds staff to confirm by phone before rolling a truck."*

---

## 📋 Quick Copy-Paste Prompts Cheat Sheet

| Turn / Scenario | Prompt to Paste (or Click in Queue) |
| :--- | :--- |
| **1. Primary Retail (Spinach)** | `A grocer in Chicago has ten crates of spinach, harvested yesterday, that must leave the dock within 6 hours and stay cold.` |
| **2. Follow-Up: Declined** | `They said no. Who's next?` |
| **3. Follow-Up: Explain Decoy** | `Why didn't you pick Greenline Community Pantry?` |
| **4. Follow-Up: Explain Big Food Bank** | `Why them and not Greater Chicago Food Depository?` |
| **5. Track 2 Farm (5p Potatoes)** | `A farm outside Chicago has 5 pallets of russet potatoes in 50-lb sacks (dry storage is fine) available for pickup over the next 3 days.` |
| **6. Track 3 Essentials (Sealed Formula)** | `A distributor in Chicago has 48 cases of sealed powdered infant formula, 8 months before printed expiration, ready to move this week (7 days).` |
| **7. Safe Refusal (1h Cream Pastries)** | `A bakery has 40 trays of cream-filled pastries that must stay refrigerated and leave their dock within 1 hour.` |
| **8. Managed BigQuery MCP Query** | `Not counting the invented teaching cases (profile_source 'planted'), how many recipients have walk-in cold storage, and what share is that?` |
