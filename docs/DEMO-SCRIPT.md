# Step-by-Step Demo Walkthrough & Exact UI Click Script (~2:40)

Navigation: [Complete Submission Package](SUBMISSION-PACKAGE.md) · **[14-Slide Pitch Deck PDF (`RescueBroker-Pitch-Deck.pdf`)](RescueBroker-Pitch-Deck.pdf)** · [HTML Slide Deck](pitch-deck.html) · [Short 2:33 Video Plan](VIDEO-SCRIPT-3MIN.md) · [Submission Checklist](SUBMISSION.md) · [Equity Audit](../agent/food_broker/EQUITY-AUDIT.md) · [Captured Evidence](evidence/README.md).

Every button, tab, chip, and menu name in this walkthrough matches **the exact on-screen labels** in the live Cloud Run Coordinator Dispatch Console (**`https://food-broker-ui-817377390808.us-east1.run.app`**) and pairs beat-by-beat with the 14-slide PDF deck ([`docs/RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf)).

---

## 🛠️ Pre-Flight Setup (1 Minute Before Recording)

Nothing needs to be started locally — everything is live in the cloud:

1. **Tab 1 — 14-Slide Pitch Deck PDF:** Open [`docs/RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf).
2. **Tab 2 — Live Coordinator Dispatch Console:**
   👉 **`https://food-broker-ui-817377390808.us-east1.run.app`**
3. **Timing Tip for Tab 2 (`Live Matching` checkbox in the top-right header bar):**
   - **Checked (Default):** Sends live requests to `gemini-3.8-flash` on Cloud Run (`~20s` per response; talk over the first 10–12s and trim the remaining wait in your video edit).
   - **Unchecked (Instant Saved-Run Mode):** Clicking **10 Crates Fresh Spinach**, **5 Pallets Russet Potatoes**, **48 Cases Sealed Infant Formula**, or **40 Trays Cream Pastries** in the **`Incoming Food Offers`** column loads their saved Cloud Run Match Briefs in `<50ms` with zero wait.

---

## 🎬 Minute-by-Minute Click-by-Click Walkthrough (`2:40` Total)

### Beat 1 — The Problem & Splash Screen (`0:00 – 0:20` | 20s)
*Pairs with **Slides 1–3** of [`RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) ("RescueBroker · Table 17" & "A matching problem under a clock")*

#### 🖱️ Exact UI Clicks
1. Start on **`https://food-broker-ui-817377390808.us-east1.run.app`** (the **RescueBroker Splash Screen**).
   - Point briefly to the **Live Food Rescue Chatbot** embedded right on the splash screen (with its quick-chips **`🥬 10 crates spinach · 6h left`**, **`🔄 They said no — who's next?`**, **`❓ Why not Greenline?`**, **`❄️ Walk-in coolers in Chicago?`**, **`🫐 Split 10-pallet blueberries`**) and the 4 role cards at the bottom (**`Dispatch Coordinator`**, **`Pantry / Agency Manager`**, **`Driver & Route Planner`**, **`Safety & Program Director`**).
2. Click the green hero button **`[ Open Live Dispatch → ]`** (or click the **`Dispatch Coordinator — Match & Dispatch Donations`** card at the bottom left).
3. You are now inside **`Live Dispatch`**. Sweep your cursor across:
   - **Left Menu (`#leftNavRail`):** `Live Dispatch (11)`, `AI Broker Chat (Live)`, `Pantry Locations (188)`, `Route Planner (3)`, `Food Safety & Recalls (2)`, `Community Impact`.
   - **Incoming Food Offers column (`#queueSidebar`):** 11 offers sorted *Soonest first* (`1.0h` to `10d`).
   - **Center Stage:** *Most Urgent Decisions Right Now* + *Best Match Card* + *Map & Delivery Schedule*.
   - **Right Sidebar:** *Assistant* | *FAQ* | *Get Help*.

#### 🗣️ What to Say Out Loud
> *"Hi, I'm [Name] from Table 17. Our track is Retail and Grocer Rescue in Chicago. A grocer has ten crates of fresh spinach with six hours left on the clock. Four questions hit in the same minute: what just became available, who could use it, what can they store, and how long does it have? By the time a coordinator answers them by phone, the food is gone—so we built RescueBroker."*

---

### Beat 2 — The Spinach Offer & The 6-Part Match Brief (`0:20 – 0:55` | 35s)
*Pairs with **Slides 3, 4 & 6** of [`RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) ("From a text message to a call-ready brief" & "From 80 candidates to one call")*

#### 🖱️ Exact UI Clicks
1. In the **`Incoming Food Offers`** column on the left (or in the **Most Urgent Decisions Right Now** strip at the top), click **`10 Crates Fresh Spinach (6.0h Left)`**.
   - *(Or, to run it live in the right-hand **Assistant** panel, click **`[ Send ↵ ]`** where the spinach prompt is pre-filled.)*
2. Point to the **Best Match Card (`Habibi Care`)** in the center of the screen:
   - **Header:** `Best Match · Recommended #1` — **`Habibi Care`** (`4845 N Washtenaw Ave, Chicago, IL 60625`), with top-right badge **`80 pantries checked · 12 fit`**.
   - **4 Metric Boxes across the middle:**
     1. **`Cooler Type`:** `Standard Fridge (Confirm by phone)`
     2. **`Space Needed`:** `0.5 of 1 pallet`
     3. **`Pickup Timing`:** `6h left · 3h pickup` (`+3h cushion`)
     4. **`Pickup Driver`:** `Needs Driver (Send volunteer van)`
   - **Bottom Left (`Why This Pantry Is a Great Fit`):** Profile summary + `Surrounding neighborhood: 13% poverty · 5% households without a car · 12% receiving assistance`.
   - **Bottom Right (`Text Message Ready to Send`):** Point to the ready-to-send outreach message.
3. Click **`[ 1. Copy Text ]`** and then click **`[ ✓ 2. Confirm Delivery ]`** in the top-right corner of the Match Card:
   - A green confirmation banner appears (`Step 2/3 · On the Way — Delivery confirmed with Habibi Care`), and **`[ 📦 3. Mark Delivered ]`** unlocks.

#### 🗣️ What to Say Out Loud
> *"RescueBroker checks the food's clock, pulls the 80 closest Chicago recipients by meaning using BigQuery vector search, applies hard filters for cold storage, pallet room, and pickup time, and ranks the survivors with a safe margin first.*
> *Recipient names and addresses are real IRS records—except nine invented teaching cases in the challenge data—while storage, capacity, and pickup times are generated. Here on the card is the six-part Match Brief: who to call and why, cooler and pallet room, the 6-hour clock with a 3-hour cushion, a flag to send a volunteer driver, neighborhood context, and a text message ready to send."*

---

### Beat 3 — Why Meaning Alone Picks the Wrong Pantry (`0:55 – 1:35` | 40s)
*Pairs with **Slide 5** of [`RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) ("Meaning alone picks the wrong pantry: Top 15 → 1 viable | Top 40 → 3 viable | Top 80 → 12 viable")*

#### 🖱️ Exact UI Clicks
1. Directly below the Match Card, look at the 4 sub-tabs:
   **`[ Map & Delivery Schedule ]` · `[ Backup Pantries (5) ]` · `[ Reserved Space & Declines ]` · `[ Activity History ]`**
2. Click the 2nd sub-tab: **`[ Backup Pantries (5) ]`**.
3. Point to the two columns that open:
   - **Left column (`Next Available Backup Pantries`):** `Love Of Angels` and `Good Food Pantry`.
   - **Right column (`Nearby Pantries Skipped (Why They Couldn't Take It)`):**
     - Point to **`Greenline Community Pantry (invented teaching case)`** — ranked **#1/#3 by meaning**, skipped because **`no cold storage; needs 12h to collect, food has 6h`**.
     - Point to **`Tca Health Inc Nfp`** (`needs 18h to collect, food has 6h`) and **`Go Forth International`** (`needs 21h to collect, food has 6h`).
4. Click back to the 1st sub-tab **`[ Map & Delivery Schedule ]`** for 3 seconds to show the green (`Best Match`), blue (`Backup Pantries`), and red (`Couldn't Take Load`) pins on the Chicago map + the **`Pickup & Spoilage Schedule`** bar (`+3.0h cushion`).

#### 🗣️ Plain-English Narration
> *"Click **Backup Pantries** to see why searching by meaning alone picks the wrong pantry: in our saved spinach run, the three closest matches by meaning were all removed. Two needed 12 to 21 hours to collect when the spinach only has six—and the decoy, **Greenline Community Pantry** (one of the nine invented teaching cases), writes that its families ask most for fresh greens, yet it has **no refrigerator at all**.*
> *The closest pantry that passes the hard filters is 11th by meaning. Searching only the top 15 left just 1 viable pantry, top 40 left 3, and top 80 left 12. And instead of stopping at a tight 1-hour margin, our ranking picks a pantry with 2 to 3 hours to spare. We also enforce an automated test in `selfcheck.py` that caught a decoy-sorting bug in our first build."*

---

### Beat 4 — When a Pantry Says No, the Next Call Is Ready (`1:35 – 1:58` | 23s)
*Pairs with **Slide 7** of [`RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) ("When a pantry says no, the next call is ready")*

#### 🖱️ Exact UI Clicks
1. On the top-right of the Match Card, click the red-outlined button **`[ ✗ Can't Deliver / Backup ▾ ]`**.
2. A 4-button recovery bar opens right inside the card:
   - **`[ 🔄 1. Try Next Backup Pantry ]`**
   - **`[ ⏱️ 2. Ask Donor for +1.5h ]`**
   - **`[ 🏢 3. Send to Large Cooler Hub ]`**
   - **`[ ♻️ 4. Decline Safely / Divert ]`**
3. Click **`[ 🔄 1. Try Next Backup Pantry ]`** (or click the **`They said no`** chip above the right-hand Assistant input box).
   - Point to the Match Card updating to the next backup pantry and the **`Reserved Space & Declines`** tab counter incrementing.
4. Optional: Click the **`Why not Greenline?`** chip above the right-hand Assistant input box to show `explain_candidate`.

#### 🗣️ What to Say Out Loud
> *"When a pantry can't take the delivery, clicking **Can't Deliver / Backup** and **Try Next Backup Pantry** records the refusal, skips everyone who declined, and prepares the next Match Brief and text message right away."*

---

### Beat 5 — One Pipeline Across All Surplus + Read-Only Data Questions (`1:58 – 2:20` | 22s)
*Pairs with **Slides 8, 9 & 10** of [`RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) ("One pipeline for every kind of surplus" & "What the agent decides for itself")*

#### 🖱️ Exact UI Clicks
1. *(Uncheck `Live Matching` in the top-right bar if you want instant zero-wait transitions across these 3 items in the left **`Incoming Food Offers`** column:)*
   - Click **`5 Pallets Russet Potatoes (3d left)`** in **`Incoming Food Offers`** → point to **`St. Moses the Black Parish Food Pantry`** (a household kitchen fridge is capped at 1 pallet, so 5 pallets go to a pantry with loading-dock room).
   - Click **`48 Cases Sealed Infant Formula (7d left)`** in **`Incoming Food Offers`** → point to **`Care For Friends`** (the agent ignores the 1-hour opened-bottle table figure and trusts the donor's 8-month sealed expiry).
   - Click **`40 Trays Cream Pastries (1.0h left)`** at the top of **`Incoming Food Offers`** → point to **`No Safe Pantry Match`** (1 hour is shorter than the fastest 2-hour pickup, so the agent refuses safely and shows the 4 recovery options).
2. In the left navigation menu (`#leftNavRail`), click **`Food Safety & Recalls`** for 3 seconds to show the live US FDA recall check and the **Coordinator 3-Point Dock Safety Checklist**.

#### 🗣️ What to Say Out Loud
> *"With no rulebook per track, the same pipeline routes five tons of farm potatoes to a pantry with multi-pallet room because a household fridge is capped at one pallet; trusts the donor's 8-month expiry on sealed infant formula instead of a 1-hour opened-bottle table figure; and safely refuses 40 trays of cream pastries with 1 hour left because nobody can collect in time.*
> *And when a coordinator asks a data question—like how many real recipients have a walk-in cooler—it runs through Google's managed BigQuery MCP server in read-only mode: six out of 183."*

---

### Beat 6 — Community Impact (10-Offer Equity Audit), Limits & Next Steps (`2:20 – 2:40` | 20s)
*Pairs with **Slides 11 & 12** of [`RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) ("Per offer, close to the corpus; big loads, less assistance" & "Limits today, and what is next")*

#### 🖱️ Exact UI Clicks
1. In the left navigation menu (`#leftNavRail`), click **`Community Impact`**.
2. Point to the 4 KPI cards at the top (`21.9% vs 15.3%` poverty, `29.7% vs 19.7%` no-car households, `8 Distinct Orgs`, `14 Dock Orgs`) and the summary table comparing all 183 verified pantries against the 1,004 Chicago census tracts.
3. Click the segmented toggle **`[ 183 Verified Orgs (Default) ]` ↔ `[ With 9 Sample Cases (192) ]`** once to show the 10-Posting Geographic & Tract Breakdown below.
4. Click **`Route Planner`** in the left navigation menu for 3 seconds to show **Split Large Farm Loads Across Multiple Pantries (`10 Pallets Fresh Blueberries`)** — our interactive UI prototype of Slide 12's **"Next: Split a big load"**.

#### 🗣️ What to Say Out Loud
> *"Finally, clicking **Community Impact** shows our 10-offer equity audit across the 183 real recipients: counted per offer, matches sit close to the corpus at 22% poverty and 19% assistance. Counted per unique recipient, they sit lower at 16% and 15%, because one fast pantry won three retail offers. And weighted by pallets, assistance drops to 9% against 19%, because big farm loads can only fit in the 14 pantries with 5-plus pallet room. Ten offers can't separate a real skew from noise.*
> *We're upfront about our limits: storage and pickup times are generated, locations are ZIP-level, and shelf life is consumer guidance—and in **Route Planner** and **Reserved Space**, we've already prototyped the next two steps: splitting a 10-pallet farm load and remembering who received food."*
