# Deck outline: RescueBroker — Turning 45 Minutes of Phone Tag into a 15-Second Food Rescue Dispatch

Navigation: [visual slide deck (HTML/PDF)](pitch-deck.html) · [demo script](DEMO-SCRIPT.md) ·
[submission checklist](SUBMISSION.md) · [agent README](../agent/food_broker/README.md) ·
[equity audit](../agent/food_broker/EQUITY-AUDIT.md) · [design notes](DESIGN.md).

Eight slides written in plain, human language for food rescue coordinators, operations leaders, and judges. Every
mandatory judge check is on the slides below—including the actual 6-Part Spinach Match Brief on Slide 2 and the 6-turn
afternoon user journey on Slide 3.

---

## 1. Thursday, 2:10 PM: Why Good Food Goes to the Compactor

> *"We coordinate food rescue in Chicago. A grocer has just offered ten crates of fresh spinach that must leave their
> loading dock within six hours and stay cold. Here is who we would call—and what we do not know about them."*

- **Today's Reality (45 Minutes of Phone Tag):** A coordinator sits with a ringing phone, a spreadsheet of 183 real
  Chicago charities, and a group text of volunteer drivers. Before sending a van, they must answer **four questions in
  the same minute**: *Who needs fresh greens? Who actually has a working cooler? Can they collect before 8 PM? Do they
  have a refrigerated van, or do we send a volunteer?* By the time a human calls down the list, the dock closes.
- **With RescueBroker (A Verified Match Brief in ~16 Seconds):** The coordinator pastes the grocer's text (or snaps a
  photo of the pallet tag) and gets a ranked recommendation, a safety buffer check, a ready-to-send text message, and
  backup pantries ready to call.
- **Transparent Data Provenance (Judge Check #1):** **183 real IRS-registered Chicago charities** (names, addresses,
  NTEE codes, reported income) plus **9 built-in safety test decoys** planted by the challenge; USDA shelf life and US
  Census neighborhood data are real; every charity's cooler type, pallet capacity, and pickup window are generated.

---

## 2. What the Coordinator Actually Sees: The Command Center + The 6-Part Match Brief

When you are juggling expiring food offers at 4 PM, scrolling through a developer chat log is a liability. We built the
**RescueBroker Dispatch Console** (`frontend/index.html`) around the actual **6-Part Match Brief** a coordinator acts on:

- **Left & Center Workspace:**
  1. **Live Countdown Queue & Chicago Pantry Map:** Sorts offers by clock urgency (**Red $\le 2$h**, **Amber $\le 6$h**),
     plots the **183 real Chicago charities** on the map (clearly separating and labelling the 9 planted test cases),
     and checks live **openFDA recalls**.
  2. **One-Click "They Said No" & "Why Not X?":** Clicking **"Recipient Declined — Next Option"** immediately promotes
     Backup #2 with a fresh SMS. Asking *"Why not the big food bank downtown?"* explains the exact constraint they failed.
  3. **Side-by-Side AI Copilot:** Connected live to Cloud Run for text, voice dictation, crate-label photo scanning,
     and city-wide database questions.
- **Right on the Slide — Live Output for the 10 Crates of Spinach (`docs/evidence/spinach-answer.md`):**
  1. **Who & Why:** **Habibi Care** (or **Shakespear Rose Community Table**), *4845 N Washtenaw Ave, Chicago, IL 60625*.
  2. **What They Can Take:** Domestic cold storage · Takes up to **1 pallet** (offer is 0.5 pallets). *Confirm by phone
     before the truck rolls.*
  3. **The Clock & Driver Action:** **6h remaining** · Collects within **3h** = **+3h safety buffer**. **⚠️ Needs
     Volunteer Driver** (no refrigerated transport).
  4. **Whose Neighborhood It Helps:** Serves 165 households/wk (Families w/ children) · Nearest census tract: **13%
     poverty, 5% no-vehicle, 12% assistance**.
  5. **Ready-to-Send SMS:** *"Hello Habibi Care team, A grocer in Chicago has ten crates of spinach... leaves you
     roughly 3 hours of slack to collect. We can arrange a driver, since it has to stay cold. Can you take it?"*
  6. **Next Two Backups + Rejected Decoy Caught:** **#2 Love Of Angels** (4h pickup, +2h buffer) · **#3 Good Food
     Pantry** (3h pickup, +3h buffer) · **Rejected Decoy:** **Greenline Community Pantry** (*Ranked #3 by meaning —
     removed: no cold storage; needs 12h vs 6h clock*).

---

## 3. A Real Afternoon Workflow: Answering All 7 Coordinator Questions Across Follow-Up Calls

A tool that only gives a single match is a search box. RescueBroker stays with the coordinator across every follow-up
phone call until the food is claimed (`docs/evidence/follow-ups-transcript.md`):

- **2:10 PM — The Offer Arrives:** Coordinator pastes *"10 crates of spinach, harvested yesterday, dock closes in 6
  hours, needs cold."* $\rightarrow$ RescueBroker checks USDA shelf life, filters 192 charities, and briefs **Habibi
  Care** (+3h buffer, needs volunteer driver).
- **2:14 PM — "They Said No. Who's Next?" (and "They Said No Too!"):** First pantry doesn't answer the phone.
  Coordinator clicks decline (or types *"They said no"*). $\rightarrow$ RescueBroker skips declined pantries, promotes
  **Love Of Angels** (#2) and then **Good Food Pantry** (#3) with fresh SMS messages.
- **2:18 PM — "Why Them and Not the Big Food Bank Downtown?":** Coordinator asks why a major food bank wasn't picked.
  $\rightarrow$ RescueBroker looks up **Americas Food Bank** (ranked 29th by meaning) and explains it was removed
  because it has 0 pallets room and needs **41 hours notice** against a 6-hour clock.
- **Why It Responds in ~16 Seconds:** Early prototypes that passed 80 charities between multiple AI chatbots took
  **76–86 seconds per step**. Keeping the physical safety rules in fast, offline-tested code and using Google's fastest
  reasoning model (verified across 42 test runs: **41/42 passed**, zero prompt-injection leaks) delivers complete
  answers in **15.6 to 17.2 seconds**.

---

## 4. Why Smart Search Alone Spoils Food—and How We Catch the Decoy (Judge Check #2)

If an AI sends ten crates of perishable spinach to a pantry with no refrigerator, the food spoils and the coordinator
never trusts the tool again. Look at what happened inside our 6-hour spinach search:

- **The Top 3 "Best" Matches by Meaning Were All Wrong:** All three closest matches by meaning needed **12 to 21 hours**
  to collect when the spinach only had 6 hours. **3rd Closest by Meaning (`Greenline Community Pantry`)** is a built-in
  test decoy whose bio begs for *"fresh greens"*—while having **no refrigeration of any kind**.
- **Why We Search 80 Charities Instead of 15 (`docs/evidence/pool-study.txt`):** Because physical rules eliminate most
  matches, searching only the top 15 charities left just **1 viable option** (and 40 left **3**). Searching the top
  **80** gives the coordinator **12 viable pantries**—leaving 9 backups when pantries don't answer the phone.
- **Why a Van & 3h Buffer Beats a 1h Squeeze (`docs/evidence/demo-tracks.txt`):** The closest charity by meaning that
  passed the filters (11th) only had a **household kitchen fridge** and **1 hour of slack**. RescueBroker passes over
  thin margins to pick charities (50th, 54th, 63rd) with **2–3 hours of breathing room** and **sturdy commercial/vehicle
  cooling**.
- **Verified by an Automated "Broken Filter" Test:** Our offline test suite (`selfcheck.py`) includes a check that
  intentionally switches off the cooler rule to prove the test catches the decoy (which caught a real sorting bug in our
  first build).

---

## 5. One System Across Every Type of Donation (Grocer, Farm, and Family Clinic)

Coordinators don't want three separate tools for grocery stores, farms, and family shelters. Because RescueBroker
matches on meaning and physical capacity, one system handles all three tracks with zero custom rulebooks:

| Type of Donation | What the Donor Offered | What Makes It Hard | How RescueBroker Handled It (From 80 Candidates) |
|---|---|---|---|
| 🛒 **Neighborhood Grocer** | **10 crates of fresh spinach** (0.5 pallets, 6h left, cold) | Hours, not days; most pantries lack a van. | **12 viable matches:** Picked **Habibi Care / Shakespear Rose** (3–4h pickup, +2–3h buffer), flagged volunteer driver need, and rejected the no-cooler decoy. |
| 🚜 **Regional Farm** | **5 tons of potatoes in the field** (~5 pallets, 3 days left) | Almost no neighborhood pantry fits 5 pallets. | **10 viable matches:** Filtered out 169 small pantries and routed to **Lakeview Pantry / Anso Child Development** (7–12 pallets room + loading dock). |
| 🍼 **Critical Supplies** | **48 cases of sealed infant formula** (2 pallets, 8 months left) | Strict safety rules and specialized clinics. | **26 viable matches:** Routed to child/family programs while overriding a misleading 1-hour database rule (Slide 6). |
| 🛑 **Impossible Clock** | **40 trays of cream pastries** (Must leave dock in **1 hour**) | A bad tool guesses and wastes a driver trip. | **0 viable matches (Safe Refusal):** Refused to guess; told the coordinator nobody can collect in 1 hour and listed the closest kitchens (which need 2+ hours). |

---

## 6. Four Real-World Mistakes Our System Catches So Coordinators Don't Get Burned

1. **Knowing Sealed Formula Lasts 8 Months—Not 1 Hour:** The federal shelf-life table lists infant formula at **1
   hour**—because that is the figure for *prepared formula in an opened bottle*! A naive tool rejects 48 sealed cases
   with 8 months left on the box. RescueBroker warns on any table figure under 2 hours and uses the donor's sealed
   expiration date.
2. **A Kitchen Fridge Is Not a Walk-In Cooler:** Many church pantries list "domestic cold storage"—a standard household
   refrigerator. Other tools see "has cold storage" and try to send them 4 pallets of produce. We cap household fridges
   at **1 pallet max** and reserve multi-pallet cold loads for commercial coolers.
3. **Trusting Verified Pickup Hours Over Vague Bio Text:** Because charity bios were generated independently from
   numeric columns, a written bio can claim *"we can be there within a couple of hours"* while its operational record
   requires **19 hours notice**. RescueBroker strips timing claims from bio quotes and strictly enforces the numeric
   pickup window.
4. **Instant City-Wide Answers:** When a coordinator asks a general question—*"Not counting the 9 invented teaching
   cases, how many recipients have walk-in cold storage?"*—RescueBroker queries the live database in read-only mode and
   answers: **only 6 out of 183 real charities (3.3%)**.

---

## 7. Auditing Our Impact: Did Food Go Where the Need Is—or Where the Loading Docks Are? (Judge Check #3)

We never use neighborhood demographics to rank who "deserves" food. Instead, we excluded the **9 invented teaching
cases** (placed at the city center by formula) and audited all 10 offers across the **183 real IRS charities** (on 68
census tracts) three ways ([`EQUITY-AUDIT.md`](../agent/food_broker/EQUITY-AUDIT.md)):

| How We Count the Matches | Count | Neighborhood Poverty (Mean / Med) | Households w/o a Car (Mean / Med) | On Food/Cash Assistance (Mean / Med) |
|---|---|---|---|---|
| **Chicago Metro Overall** (pop-weighted) | 1,004 tracts | **15%** / — | **20%** / — | **18%** / — |
| **All 183 Real Chicago Charities in Directory** | 183 charities | **19%** / 16% | **28%** / 27% | **19%** / 12% |
| **View 1: Counted Once Per Donation Offer** | 10 offers | **22%** / 16% | **30%** / 23% | **19%** / 11% |
| **View 2: Counted Per Unique Charity Reached** | 8 charities | **16%** / 10% | **24%** / 20% | **15%** / 6% |
| **View 3: Weighted by Pallets of Food Moved** | 37.5 pallets | **14%** / — | **32%** / — | **9%** / — |
| **Charities w/ a Dock or 5+ Pallets Room** | 14 charities | **17%** / 14% | **29%** / 27% | **16%** / 14% |

- **Discovery #1 (One Fast Pantry Won 3 Times):** Counted per offer (View 1), matches sit close to the directory (higher
  mean poverty at `22%` and no-car at `30%`, slightly lower medians)—because **one fast pantry** in a high-need area
  (*Shakespear Rose*, `45%` poverty / `52%` no car) won 3 short-clock grocery offers. Counted once per unique charity
  (View 2), matches sit lower on all three measures.
- **Discovery #2 (Big Farm Loads Can Go to Only a Few Charities):** Farm offers make up **30 of the 37.5 pallets**.
  Weighted by volume (View 3), public assistance is **`9%` against a `19%` directory mean**—because big farm loads can
  go to only a few charities (only **14 of 183** have a dock or room for 5+ pallets, and only **10** have room for 10+
  pallets; their tracts show lower mean poverty and assistance and a similar share without a car, with medians about level).

---

## 8. Honest Limits Today & Three Practical Upgrades for Day Two (Judge Check #4)

- **Four Honest Realities of Today's System:**
  1. **Who Is Real vs. What Is Generated:** The **183 charity names, addresses, and tax incomes** are real IRS records
     (plus **9 invented teaching cases**). However, every pantry's **cooler type, pallet room, and pickup hours are
     generated** because no public national database exists—so RescueBroker always tells staff to confirm by phone.
  2. **Home Storage vs. Commercial Cold Chain:** USDA shelf-life numbers are consumer home guidance, not a commercial
     refrigeration guarantee.
  3. **ZIP-Code Center Points:** Charity locations are ZIP-level centroids (and postings have no donor address), so
     census figures describe the surrounding area rather than the exact block.
  4. **No Delivery Memory or Load Splitting Yet:** Without delivery history, one fast pantry wins repeated short-clock
     offers, and loads larger than any single cooler are safely refused rather than split.
- **Three Practical Upgrades for Day Two:**
  1. **Fair Rotation & Delivery Memory:** Record who received food earlier today so one fast pantry isn't called three
     times in a row while neighboring pantries wait.
  2. **Automatic Load Splitting for Big Farm Offers:** When a farmer offers 5 tons of produce and no single neighborhood
     pantry has a big enough cooler, automatically split the delivery across 2 or 3 pantries and draft separate texts.
  3. **2-Minute Pantry Self-Check-In:** Let local pantry managers text or talk to RescueBroker to update their real
     cooler space and pallet-jack access—replacing generated profiles with verified local knowledge.
