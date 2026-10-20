# Step-by-Step Demo Walkthrough & Click-by-Click Recording Script (~2:40)

Navigation: [Complete Submission Package](SUBMISSION-PACKAGE.md) · **[14-Slide Pitch Deck PDF (`RescueBroker-Pitch-Deck.pdf`)](RescueBroker-Pitch-Deck.pdf)** · [HTML Slide Deck](pitch-deck.html) · [Short 2:33 Video Plan](VIDEO-SCRIPT-3MIN.md) · [Submission Checklist](SUBMISSION.md) · [Equity Audit](../agent/food_broker/EQUITY-AUDIT.md) · [Captured Evidence](evidence/README.md).

This guide pairs **every slide of the 14-slide Table 17 Pitch Deck ([`docs/RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf))** with **exact step-by-step mouse click instructions** on the live Cloud Run Coordinator Dispatch Console (**`https://food-broker-ui-817377390808.us-east1.run.app`**), written in clear, plain language for outside users and judges.

---

## 🛠️ Pre-Flight Setup (1 Minute Before Recording)

You do **not** need to start anything locally — both the Coordinator Dispatch Console and the ADK Agent are live on Cloud Run:

1. **Tab 1 — 14-Slide Pitch Deck PDF:** Open [`docs/RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) (or `https://github.com/jimmycgz/challenge2-117/blob/main/docs/RescueBroker-Pitch-Deck.pdf`).
2. **Tab 2 — Live Coordinator Dispatch Console (Cloud Run):**
   👉 **`https://food-broker-ui-817377390808.us-east1.run.app`**
3. **Tab 3 — Live ADK Agent Chat UI (Optional Backup View):**
   👉 **`https://food-broker-817377390808.us-east1.run.app/dev-ui/`** (select `food_broker`).
4. **Choose Your Timing Mode in Tab 2 (`https://food-broker-ui-817377390808.us-east1.run.app`):**
   - **Live Cloud Run Mode (Default):** Keep **`Live Matching`** checked in the top bar. Each live call takes **`~20 seconds`** on Cloud Run — talk over the first 10–12 seconds and trim the remaining wait in your video editor.
   - **Instant Saved-Run Mode (Zero Wait):** Uncheck **`Live Matching`** in the top bar when switching between Spinach, Potatoes, Sealed Formula, and Cream Pastries to show the saved Cloud Run Match Briefs immediately (`<50ms`).

---

## 🎬 Minute-by-Minute Click-by-Click Walkthrough (`2:40` Total)

### Beat 1 — The Problem Under a Clock (`0:00 – 0:20` | 20s)
*Pairs with **Slides 1–3** of [`RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) ("RescueBroker · Table 17" → "A matching problem under a clock")*

#### 🖱️ Exact Click Instructions
1. Start on **Tab 1 (`RescueBroker-Pitch-Deck.pdf` Slide 1 & Slide 2)** for 5 seconds, then switch to **Tab 2 (`https://food-broker-ui-817377390808.us-east1.run.app`)**.
2. On the Splash screen, click the green button **`[ Launch as Rescue Coordinator → ]`**.
3. Sweep your mouse across the three panels:
   - **Left:** *Donations Waiting (`11`)* sorted by time left on the clock.
   - **Center:** *Chicago Pantry Map* + *Match Brief*.
   - **Right:** *Assistant Chat*.

#### 🗣️ Plain-English Narration
> *"Hi, I'm [Name] from Table 17. Our track is Retail and Grocer Rescue in Chicago. A grocer has ten crates of fresh spinach with six hours left on the clock. Four questions hit at the same minute: what just became available, who could use it, what can they store, and how long does it have? By the time a coordinator answers them by phone, the food is gone—so we built RescueBroker."*

---

### Beat 2 — From a Text Message to a Call-Ready 6-Part Match Brief (`0:20 – 0:55` | 35s)
*Pairs with **Slides 3, 4 & 6** of [`RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) ("From a text message to a call-ready brief" & "From 80 candidates to one call") — **Fills the #1 thing not pictured in the PDF: showing the actual 6-part Match Brief & ready-to-send SMS!***

#### 🖱️ Exact Click Instructions
1. In the left **Donations Waiting** list, click **`10 Crates Fresh Spinach · 6h left · 0.5 pallet · Needs Cooler`** (or click **`[ Send ↵ ]`** in the right-hand Assistant box to run it live).
2. On the **Best Match Card** in the center of the screen, point to each of the 6 parts:
   - **1. Who & Why:** `Habibi Care` (real street address in Chicago `60625`).
   - **2. What They Can Store:** `Refrigerator space for up to 1–2 pallets` (reminding staff to confirm by phone).
   - **3. The Clock & Safe Margin:** `6 hours left` vs `3–4 hours pickup notice` = **`2 to 3 hours to spare`**, plus a clear **`Needs Volunteer Driver`** badge.
   - **4. Whose Neighborhood It Helps:** Nearest Census tract poverty, no-vehicle households, and food/cash assistance.
   - **5. Ready-to-Send Message:** Click **`[ Copy Text ]`** and **`[ ✓ 2. Confirm Delivery ]`** to reserve the cooler space.

#### 🗣️ Plain-English Narration
> *"RescueBroker checks the food's clock, pulls the 80 closest Chicago recipients by meaning using BigQuery vector search, applies hard filters for cold storage, pallet room, and pickup time, and ranks the survivors with a safe margin first.*
> *Recipient names and addresses are real IRS records—except nine invented teaching cases in the challenge data—while storage, capacity, and pickup times are generated. In one step, the coordinator gets a six-part Match Brief with a message ready to send."*

---

### Beat 3 — Why Meaning Alone Picks the Wrong Pantry (`0:55 – 1:35` | 40s)
*Pairs with **Slide 5** of [`RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) ("Meaning alone picks the wrong pantry: Top 15 → 1 viable | Top 40 → 3 viable | Top 80 → 12 viable")*

#### 🖱️ Exact Click Instructions
1. On the bottom of the Match Card, click:
   **`▶ Show Backup Pantries & Why Others Were Skipped (2 backups · 3 skipped)`**
2. Point to the right-hand **`Why Close Matches Were Skipped`** list:
   - Highlight **`Greenline Community Pantry`** — point to its red reason badge: **`no refrigeration, needs 12h to collect, food has 6h`**.
   - Highlight the other two top semantic matches eliminated because they needed **12 to 21 hours** to collect when the spinach only has **6 hours**.
3. Point to the red decoy pin on the Chicago map (or flash **Slide 5** of the PDF showing `Top 15 → 1 viable | Top 40 → 3 viable | Top 80 → 12 viable`).

#### 🗣️ Plain-English Narration
> *"Here is why searching by meaning alone fails: in our saved spinach run, the three closest pantries by meaning were all wrong. Two needed 12 to 19 hours to collect when the spinach only has six—and the decoy, **Greenline Community Pantry** (one of the nine invented teaching cases), writes that its families ask most for fresh greens, yet it has **no refrigerator at all**.*
> *The closest pantry that passes the hard filters is 11th by meaning. Searching only the top 15 left just 1 viable pantry, top 40 left 3, and top 80 left 12. And instead of picking a tight 1-hour margin, our ranking picks a pantry with 2 to 3 hours to spare. We even enforce an automated check in `selfcheck.py` that caught a decoy-sorting bug in our first build."*

---

### Beat 4 — When a Pantry Says No, the Next Call Is Ready (`1:35 – 1:58` | 23s)
*Pairs with **Slide 7** of [`RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) ("When a pantry says no, the next call is ready")*

#### 🖱️ Exact Click Instructions
1. Click **`[ ✗ 3. Pantry Said No ]`** on the Match Card (or click the **`They said no`** chip above the right-hand Assistant input box: `They said no. Who's next?`).
2. Click **`[ Switch to Backup #2 Now ]`** in the amber banner (or let the live Assistant return the next brief).
3. Optional: Click the **`Why not Greenline?`** chip (or ask `Why didn't you pick Greater Chicago Food Depository?`) to show `explain_candidate`.

#### 🗣️ Plain-English Narration
> *"Pantries are busy. When the first choice says no, one click skips everyone who declined, searches again, and prepares the next Match Brief and text message immediately."*

---

### Beat 5 — One Pipeline for Every Surplus + What the Agent Decides for Itself (`1:58 – 2:20` | 22s)
*Pairs with **Slides 8, 9 & 10** of [`RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) ("One pipeline for every kind of surplus" & "What the agent decides for itself")*

#### 🖱️ Exact Click Instructions
1. *(Uncheck `Live Matching` in the top header if you want instant zero-wait switching across these 3 items in the left queue:)*
   - Click **`5 Pallets Russet Potatoes (3d left · 5p)`** → shows a kitchen fridge is capped at 1 pallet, routing 5 tons of potatoes to a pantry with pallet room (`St. Moses the Black Parish Food Pantry`).
   - Click **`48 Cases Sealed Infant Formula (7d left)`** → shows the agent ignoring the 1-hour opened-bottle table figure and trusting the donor's 8-month sealed expiry (`Care For Friends`).
   - Click **`40 Trays Cream Pastries (1.0h left)`** → shows **`No Safe Pantry Match`** (1 hour is shorter than the fastest 2-hour pickup; refuses safely and shows the closest rejections).
2. Click **`🏢 Walk-In Coolers (MCP)`** in the top header bar (or show [`docs/evidence/mcp-walk-in-answer.md`](evidence/mcp-walk-in-answer.md)) to show the read-only Google-managed BigQuery MCP query (`6 of 183 real recipients have a walk-in cooler`).

#### 🗣️ Plain-English Narration
> *"The same recipients, search, and filters handle every track with no custom rulebook: five tons of farm potatoes go to a pantry with room for pallets because a household kitchen fridge is capped at one pallet; sealed infant formula trusts the donor's 8-month expiry instead of a 1-hour opened-bottle figure; and 40 trays of cream pastries with 1 hour left are safely refused because nobody can collect in time.*
> *And when a coordinator asks a general data question, it runs through Google's managed BigQuery MCP server in read-only mode: excluding the nine invented cases, six of the 183 real recipients have a walk-in cooler."*

---

### Beat 6 — The 10-Offer Equity Audit, Honest Limits & Next Steps (`2:20 – 2:40` | 20s)
*Pairs with **Slides 11 & 12** of [`RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf) ("Per offer, close to the corpus; big loads, less assistance" & "Limits today, and what is next")*

#### 🖱️ Exact Click Instructions
1. In the far-left navigation rail, click **`Impact Study`** (`view-equity`) — or show **Slide 11 & Slide 12** of [`RescueBroker-Pitch-Deck.pdf`](RescueBroker-Pitch-Deck.pdf).
2. Point to the 3 ways matches were measured across the 183 real recipients:
   - **Per offer (10):** `22%` poverty, `30%` no vehicle, `19%` assistance (close to the `19% / 28% / 19%` corpus average).
   - **Per unique recipient (8):** `16%` poverty, `24%` no vehicle, `15%` assistance (because one fast pantry won three retail offers).
   - **Weighted by pallets:** **`9%`** assistance against **`19%`** across all 183 recipients (because bulk farm loads require the 14 loading-dock pantries).
3. Flash **`Split Loads`** (`view-routes`) and **`Reserved Space`** (`locksTab`) in the Dispatch Console UI as our interactive prototype of the two **"Next"** items on Slide 12 (*"Remember who got food"* and *"Split a big load"*).

#### 🗣️ Plain-English Narration
> *"Did the food go where the need is? Leaving out the nine invented cases across the 183 real recipients: counted per offer, our matches sit close to the corpus at 22% poverty and 19% assistance. Counted per unique recipient, they sit lower at 16% and 15%, because one fast pantry won three of the four retail offers. And weighted by estimated pallets, assistance drops to 9% against 19%, because big farm loads can only fit in the few pantries with multi-pallet room. Ten offers can't separate a real skew from noise.*
> *We're upfront about our limits: storage and pickup times are generated, locations are ZIP-level, and shelf life is consumer guidance—and in our Dispatch Console we've already begun prototyping the next two steps: remembering who received food and splitting big farm loads."*
