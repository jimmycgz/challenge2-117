# Deck outline: RescueBroker — Turning 45 Minutes of Phone Tag into a 15-Second Food Rescue Dispatch

Navigation: [visual slide deck (HTML/PDF)](pitch-deck.html) · [demo script](DEMO-SCRIPT.md) ·
[submission checklist](SUBMISSION.md) · [agent README](../agent/food_broker/README.md) ·
[equity audit](../agent/food_broker/EQUITY-AUDIT.md) · [design notes](DESIGN.md).

Eight slides written in plain, human language for operations leaders and judges. Every required judge check is on the
slides below without burying the story in developer jargon.

---

## 1. Thursday, 2:10 PM: Why Good Food Goes to the Compactor

> *"We coordinate food rescue in Chicago. A grocer has just offered ten crates of fresh spinach that must leave their
> loading dock within six hours and stay cold. Here is who we would call—and what we do not know about them."*

- **Today's Reality (45 Minutes of Phone Tag):** A coordinator sits with a ringing phone, a spreadsheet of 192
  charities, and a group text of volunteer drivers. Before sending a van, they must answer **four questions in the same
  minute**: *Who needs fresh greens? Who actually has a working cooler? Can they collect before 8 PM? Do they have a
  refrigerated van, or do we send a volunteer?* By the time a human calls down the list, the dock closes.
- **With RescueBroker (A Verified Match Brief in About 20 Seconds):** The coordinator pastes the grocer's text (or snaps a
  photo of the pallet tag) and gets a ranked recommendation, a safety buffer check, a ready-to-send text message, and two
  backup pantries ready to call.
- **What Is Real vs. Estimated Up Front:** **183 Chicago charity names, addresses, and tax incomes** are real IRS
  records (plus **9 invented teaching cases** added by the challenge); USDA shelf life and Census neighborhood data are
  real; every charity's cooler type, pallet capacity, and pickup window are generated.

---

## 2. Built for Dispatchers, Not Software Engineers: The Coordinator Command Center

When a dispatcher is juggling 11 expiring food offers at 4 PM, scrolling through a chatbot is a liability. We built the
**RescueBroker Coordinator Console** (`frontend/index.html`) around how a real rescue desk operates:

1. **The Live Countdown Queue:** Every incoming donation is sorted by urgency (**Red: under 2 hours left**, **Amber:
   under 6 hours**). Coordinators can type, dictate by voice, or upload a photo of a crate label.
2. **The 6-Part Match Brief Card:** No wall of prose. One glance shows: *Who to call & why*, *Cooler & pallet room*,
   *Time buffer on the clock*, *Whether to dispatch a volunteer driver*, *Neighborhood need*, and a *1-click SMS*.
3. **One-Click "They Said No" Pivot:** Pantries are run by busy volunteers who miss calls. Clicking **"Recipient
   Declined — Next Option"** immediately promotes the #2 backup pantry and writes a fresh text message.
4. **Chicago Pantry Map & FDA Recall Check:** Plots the **183 real Chicago charities** alongside an automatic **FDA
   recall check** so staff never dispatch recalled food.
5. **Side-by-Side AI Copilot:** Lets coordinators ask natural follow-up questions (*"Why didn't we call the big food
   bank downtown?"* or *"How many pantries in Chicago actually have a walk-in cooler?"*).

---

## 3. How It Works in Plain English (Five Steps in About 20 Seconds)

Every charity describes itself differently—one says *"fresh greens for families,"* another says *"refrigerated
produce."* Keyword search misses them. RescueBroker reads for meaning, then checks physical reality:

1. **Check the Food Clock:** Compares the grocer's dock deadline against USDA food-safety guidance.
2. **Search by Meaning:** Finds the **80 closest charities** in Chicago whose mission and dietary needs fit the offer.
3. **Enforce Hard Reality:** Eliminates anyone without the right cooler, enough pallet room, or enough time to collect.
4. **Rank for Safety Buffer:** Prioritizes charities with at least 2 hours of breathing room and sturdy refrigeration
   before raw text similarity.
5. **Deliver the Actionable Brief:** Adds neighborhood need from the US Census and drafts the exact pickup message.

*Why it's fast and reliable:* Passing 80 charities between multiple AI chatbots took over a minute. Keeping the safety
rules in offline-tested code, with Google's Gemini 3.8 Flash at low thinking, delivers answers in **about 20 seconds** on
the live service (one sample each: 19.9, 22.5 and 20.3 s). We chose that model for correctness, not speed: it passed 41 of 42
test checks against 38 for the older model, which was quicker on Cloud Run (about 13 s) and ran SQL it should have refused
in one of three runs.

---

## 4. Why Smart Search Alone Spoils Food—and How We Catch the Decoy

If an AI sends ten crates of perishable spinach to a pantry with no refrigerator, the food spoils and the coordinator
never trusts the tool again. Look at what happened on our 6-hour spinach offer:

- **The Top 3 "Best" Matches by Meaning Were All Wrong:** All three needed **12 to 21 hours** to collect against a
  6-hour clock. **Ranked #3 by meaning (`Greenline Community Pantry` — one of the 9 planted teaching cases)** wrote
  passionately that its families ask most for *"fresh greens"*—and has **no refrigeration of any kind**.
- **Why We Search 80 Charities Instead of 15:** Because physical rules eliminate most matches, searching only the top
  15 charities left just **1 viable option** (and 40 left **3**). Searching **80** gives the coordinator **12 viable
  pantries**—so when the first two decline, ten backups are ready.
- **Why We Pick Safe Buffer Over a 1-Hour Squeeze:** The closest charity that technically passed (#11) only had a
  **household kitchen fridge** and **1 hour of slack**. RescueBroker passes over thin margins to pick charities (#50,
  #54, #63) with **2–3 hours of breathing room** and a **refrigerated van**.

---

## 5. One System for Every Kind of Surplus (Grocer, Farm, and Family Clinic)

Coordinators don't want three separate tools for grocery stores, farms, and family shelters. Because RescueBroker
matches on meaning and physical capacity, one workflow handles all three:

| Type of Donation | What the Donor Offered | What Makes It Hard | How RescueBroker Handled It |
|---|---|---|---|
| 🛒 **Neighborhood Grocer** | **10 crates of fresh spinach** (0.5 pallets, 6h left, cold) | Hours, not days; most pantries lack a van. | Found **12 viable pantries**; picked a fast responder (3–4h pickup), flagged volunteer driver need, and rejected the no-cooler decoy. |
| 🚜 **Regional Farm** | **5 tons of potatoes in the field** (~5 pallets, 3 days left) | Almost no neighborhood pantry fits 5 pallets. | Filtered out 169 small pantries and routed to one of the **10 large operations** with warehouse room and a loading dock. |
| 🍼 **Critical Supplies** | **48 cases of sealed infant formula** (2 pallets, 8 months left) | Strict safety rules and specialized clinics. | Matched to child-development & family programs while catching a misleading 1-hour database rule (Slide 6). |
| 🛑 **Impossible Clock** | **40 trays of cream pastries** (Must leave dock in **1 hour**) | A bad tool guesses and wastes a driver trip. | **Safely refused to guess.** Told the coordinator nobody can collect in 1 hour and showed the closest kitchens (which need 2+ hours). |

---

## 6. Four Real-World Mistakes Our System Catches So Coordinators Don't Get Burned

1. **Knowing Sealed Infant Formula Lasts 8 Months—Not 1 Hour:** The federal shelf-life table lists infant formula at
   **1 hour**—because that is the rule for an *already-opened bottle warmed for a baby*! A naive tool rejects 48 sealed
   cases with 8 months left on the box. RescueBroker detects suspiciously short table numbers ($\le 2$ hours) and uses
   the donor's sealed expiration date.
2. **A Kitchen Fridge Is Not a Walk-In Cooler:** Many church pantries list "domestic cold storage"—a standard household
   refrigerator. Other tools see "has cold storage" and try to send them 4 pallets of produce. We cap household fridges
   at **1 pallet max**.
3. **Trusting Verified Pickup Hours Over Vague Bio Text:** In charity profiles, the written bio sometimes says *"we can
   be there within a couple of hours"* while their operational record requires **19 hours notice**. RescueBroker strips
   vague timing claims from bios and strictly enforces the numeric pickup window.
4. **Instant City-Wide Answers:** When a coordinator asks, *"Excluding the 9 test cases, how many real Chicago pantries
   actually have a walk-in cooler?"*, RescueBroker checks the live database and answers in seconds: **only 6 out of 183
   (3.3%)**.

---

## 7. Auditing Our Impact: Did Food Go Where the Need Is, or Where the Loading Docks Are?

We never use neighborhood demographics to score who "deserves" food. Instead, we ran all 10 surplus offers across the
**183 real Chicago organizations** (excluding the 9 invented teaching cases) and audited where the food landed:

| How We Count the Matches | Count | Neighborhood Poverty (Avg / Med) | Households w/o a Car (Avg / Med) | On Food/Cash Assistance (Avg / Med) |
|---|---|---|---|---|
| **Chicago Metro Overall** (pop-weighted) | 1,004 tracts | **15%** / — | **20%** / — | **18%** / — |
| **All 183 Real Chicago Charities** | 183 charities | **19%** / 16% | **28%** / 27% | **19%** / 12% |
| **View 1: Counted Per Donation Offer** | 10 offers | **22%** / 16% | **30%** / 23% | **19%** / 11% |
| **View 2: Counted Per Unique Charity Reached** | 8 charities | **16%** / 10% | **24%** / 20% | **15%** / 6% |
| **View 3: Weighted by Pallets of Food Moved** | 37.5 pallets | **14%** / — | **32%** / — | **9%** / — |

- **Discovery #1 (One Fast Pantry Won 3 Times):** Looking only at View 1 (*Per Offer*), it looks like our matches beat
  the city average on poverty (`22%`) and carless households (`30%`). When we audited ourselves cold, we saw why: **one
  well-equipped pantry** in a high-need neighborhood (*Shakespear Rose*, `45%` poverty / `52%` no car) won 3 short-clock
  grocery offers. Counting each charity once (View 2), the averages sit slightly below the directory.
- **Discovery #2 (Big Farm Loads Follow Loading Docks):** Farm offers make up **30 of the 37.5 pallets**. Weighted by
  volume (View 3), public assistance drops from `19%` to **`9%`**—because only **14 charities in Chicago** have room for
  5+ pallets (and only 10 can take 10+ pallets), and big warehouses sit in more industrial areas.

---

## 8. Honest Limits Today & Three Practical Upgrades for Day Two

- **Four Honest Realities Today:**
  1. **Who Is Real vs. What Is Estimated:** The **183 charity names, addresses, and tax incomes** are real IRS records
     (plus **9 invented teaching cases**). However, every pantry's **cooler type, pallet room, and pickup hours are
     generated** because no public national database exists—so RescueBroker always reminds staff to confirm by phone.
  2. **Home Storage Guidance:** USDA shelf-life numbers reflect home storage, not commercial cold-chain guarantees.
  3. **ZIP-Code Neighborhoods:** Charity locations are ZIP-code center points, describing the surrounding area rather
     than the exact block.
  4. **No Memory of Yesterday's Deliveries Yet:** Without delivery history, the fastest well-equipped pantry gets called
     first on repeated short-clock offers.
- **Three Practical Upgrades Next:**
  1. **Fair Rotation & Delivery Memory:** Remember who received food earlier today so one fast pantry isn't called three
     times in a row.
  2. **Automatic Load Splitting for Big Farm Offers:** Split 5-ton farm loads across 2–3 nearby pantries when no single
     cooler has room.
  3. **2-Minute Pantry Self-Check-In:** Let pantry managers text or talk to RescueBroker to update their real cooler
     space and pallet-jack access.
