# Demo Recording Teleprompter — Exact Click + Say (~2:35)

**Open URL:** `https://food-broker-ui-817377390808.us-east1.run.app`
**Tip before recording:** Uncheck **`Live Matching`** in the top-right header bar if you want every click to load instantly (`<50ms`), or leave it checked (`~20s` per live run) and cut the wait in your video edit.

---

## Step 1 — Open the Console (`0:00 – 0:15` | 15s)

* **CLICK:** On the Splash screen, click the green button **`[ Open Live Dispatch → ]`**.
* **SAY:**
  > "I'm [Name] from Table 17. Our track is Retail and Grocer Rescue in Chicago. A grocer has ten crates of spinach that must leave their dock within six hours and stay cold. Who can store it, and get there in time?"

---

## Step 2 — Match the Spinach Offer & Show the 6-Part Brief (`0:15 – 0:50` | 35s)

* **CLICK 1:** In the **`Incoming Food Offers`** column on the left, click **`10 Crates Fresh Spinach (6.0h)`**.
* **CLICK 2:** Point across the **`Habibi Care`** Match Card in the center, then click **`[ 1. Copy Text ]`** and **`[ ✓ 2. Confirm Delivery ]`**.
* **SAY:**
  > "RescueBroker pulls the 80 closest Chicago recipients by meaning using BigQuery vector search, then removes anyone who can't keep the food cold, take the pallet size, or collect in time.
  > Recipient names and addresses are real IRS records, except nine invented teaching cases in the challenge data; storage, capacity, and pickup times are generated.
  > Here is the six-part Match Brief: **Habibi Care** at #1, their fridge and pallet space, a 3-hour pickup leaving a 3-hour safety cushion, a flag to send a volunteer driver, neighborhood need, and a text message ready to send."

---

## Step 3 — Show the Semantic Decoy (`Greenline`) & Pool Study (`0:50 – 1:30` | 40s)

* **CLICK:** Directly under the Match Card, click the 2nd sub-tab: **`[ Backup Pantries (5) ]`**. Point to **`Greenline Community Pantry`** on the right under *Nearby Pantries Skipped*.
* **SAY:**
  > "Here is why searching by meaning alone fails. In our saved spinach run, the three closest matches by meaning were all removed.
  > **Greenline Community Pantry**—an invented teaching case in the challenge data—ranked first by meaning because its profile says families ask for fresh greens, yet it has **no refrigerator at all** and needs 12 hours to collect.
  > The closest pantry that passes the filters is **11th by meaning**. In our pool study, searching 15 candidates left just 1 viable pantry, 40 left 3, and 80 left 12. And instead of stopping at a 1-hour margin, our ranking picks a safer 2-to-3 hour cushion."

---

## Step 4 — "They Said No" Follow-Up (`1:30 – 1:48` | 18s)

* **CLICK:** At the top-right of the Match Card, click **`[ ✗ Can't Deliver / Backup ▾ ]`**, then click **`[ 🔄 1. Try Next Backup Pantry ]`**.
* **SAY:**
  > "When a pantry turns the load down, one click records the refusal, skips everyone who declined, and briefs the next backup pantry with a new text message."

---

## Step 5 — Farm Potatoes, Sealed Formula & 1-Hour Refusal (`1:48 – 2:10` | 22s)

* **CLICK:** In **`Incoming Food Offers`** on the left, click in order:
  1. **`5 Pallets Russet Potatoes (3d)`**
  2. **`48 Cases Sealed Infant Formula (7d)`**
  3. **`40 Trays Cream Pastries (1.0h)`**
* **SAY:**
  > "The same pipeline handles every track with no custom rules per track:
  > Five tons of farm potatoes go to a pantry with loading-dock room because a household fridge is capped at one pallet.
  > Sealed infant formula trusts the donor's 8-month expiry instead of a 1-hour opened-bottle table figure.
  > And 40 trays of cream pastries with 1 hour left are safely refused because the fastest pickup in Chicago is 2 hours."

---

## Step 6 — Data Question (`6 of 183`), Equity Audit & Honest Limits (`2:10 – 2:35` | 25s)

* **CLICK:** In the far-left menu, click **`Community Impact`**. Point to the summary table, then toggle **`[ 183 Verified Orgs (Default) ]` ↔ `[ With 9 Sample Cases (192) ]`**.
* **SAY:**
  > "Data questions run read-only through Google's managed BigQuery MCP server: excluding the nine invented cases, six of the 183 real recipients have a walk-in cooler.
  > In our 10-offer equity audit across the 183 real recipients: counted per offer, matches sit close to the corpus at 22% poverty and 19% assistance. Counted per unique recipient, they sit lower at 16% and 15%, because one fast pantry won three retail offers. Weighted by pallets, assistance drops to 9% against 19%, because big farm loads require the 14 pantries with 5-plus pallet room. Ten offers can't separate a real skew from noise.
  > Because storage and pickup times are generated, shelf life is consumer guidance, and locations are ZIP-level, the brief always reminds staff to confirm by phone before rolling a truck."
