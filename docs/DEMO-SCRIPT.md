# Demo script for the pitch video (~3 minutes, Plain-English Coordinator Story)

Navigation: [visual slide deck (HTML/PDF)](pitch-deck.html) · [deck outline](DECK-OUTLINE.md) ·
[submission checklist](SUBMISSION.md) · [equity audit](../agent/food_broker/EQUITY-AUDIT.md) ·
[captured evidence](evidence/README.md).

Speak to the judges as **a food rescue coordinator showing a tool that saves your afternoon**—not a developer reading
code. Keep the language plain, warm, and focused on why a real dispatcher would keep this open all day.

---

## 1. The Thursday Afternoon Problem & The Command Center (0:00 – 0:25 | 25s)

**On screen:** Start on the **RescueBroker Splash Page** (`frontend/index.html`), click **Launch Live Dispatch**, and
point to the **Countdown Queue** on the left and the **Chicago Pantry Map** on the right.

**Say out loud:**
> *"We coordinate food rescue in Chicago. It's Thursday afternoon, and a grocer just called with ten crates of fresh
> spinach that must leave their loading dock within six hours and stay cold. Here is who we would call, and what we
> don't know about them.*
> *Normally, finding who needs fresh greens, who actually has a working cooler, who can collect before 8 PM, and whether
> we need to send a volunteer driver takes 45 minutes of phone tag. And when you're juggling eleven expiring donations, a
> plain chatbot isn't enough—so we built RescueBroker, a live Coordinator Command Center."*

---

## 2. The Spinach Call: Catching the No-Cooler Decoy & Building a Safe Buffer (0:25 – 1:15 | 50s)

**On screen:** Click **10 Crates of Spinach (6h left)** in the queue (or paste the grocer's text in the right-hand
Copilot / live chat page):

```text
A grocer in Chicago has ten crates of spinach, harvested yesterday, that must leave the dock within 6 hours and stay cold.
```

**Point at the Match Brief card & say out loud:**
> *"In about 15 seconds, RescueBroker gives me a complete Match Brief I can act on immediately: the charity's name and
> real street address, their cooler and pallet room, the time buffer on the clock, a clear flag that we need to send a
> volunteer driver, neighborhood need, and a ready-to-send text message.*
> *Here is why smart search alone fails without physical safety rules: RescueBroker searched the 80 closest charities in
> Chicago by meaning, because searching only 15 left just 1 viable option while 80 gives us 12 backups.*
> *Look at the 'Rejected' list at the bottom: the top three matches by meaning were all wrong! All three needed 12 to 21
> hours to collect when the spinach only has 6 hours—and **Greenline Community Pantry**, ranked 3rd by meaning (one of
> nine test cases planted in the challenge), wrote passionately that its families ask most for fresh greens, while
> having **no refrigeration of any kind**.*
> *Even the closest charity that technically passed at #11 only had a household kitchen fridge and one hour of slack—so
> RescueBroker skips thin margins and picks charities with 2 to 3 hours of breathing room."*

---

## 3. When Reality Happens: "They Said No" & "Why Not the Big Food Bank Downtown?" (1:15 – 1:45 | 30s)

**On screen:** Click **"Recipient Declined — Next Option"** (or type in the Copilot):

```text
They said no. Who's next?
```

Then ask:

```text
Why them and not the big food bank downtown?
```

**Say out loud:**
> *"Pantries are run by busy volunteers who often can't answer the phone. When our first choice says no, one click skips
> them, promotes our #2 backup pantry, and drafts a new text message.*
> *And if my director asks, 'Why didn't we call the big food bank downtown?', I just ask the Copilot. It checks that
> exact organization and tells me where it ranked and why it was ruled out—for example, needing 36 to 41 hours lead time
> for a 6-hour pickup."*

---

## 4. One Workflow Across Grocer, Farm & Family Clinics—Plus Two Traps We Caught (1:45 – 2:25 | 40s)

**On screen:** Click **5 Tons of Farm Potatoes**, **48 Cases of Sealed Infant Formula**, and **40 Trays of Cream
Pastries (1h left)** in the queue (or show the captured responses):

**Say out loud:**
> *"A coordinator shouldn't need three different tools for grocery stores, farms, and family shelters. The exact same
> system handles all three:*
> *When a farm offers **5 tons of potatoes**, it automatically filters out small storefronts and household fridges—which
> we cap at 1 pallet—and routes the load to a warehouse with a loading dock.*
> *When a distributor offers **48 cases of sealed infant formula with 8 months left**, RescueBroker catches a dangerous
> database trap: the federal shelf-life table lists infant formula at **1 hour**, because that's the rule for an opened
> bottle already warmed for a baby! Our system spots suspiciously short numbers under 2 hours and uses the donor's
> 8-month sealed expiration instead.*
> *And when a bakery offers **cream pastries that must leave in 1 hour**, nobody in Chicago can collect in time. Instead
> of guessing and wasting a driver's afternoon, RescueBroker safely refuses and shows why the closest kitchens missed."*

---

## 5. City-Wide Questions, The Equity Audit & Honest Next Steps (2:25 – 3:00 | 35s)

**On screen:** Show the walk-in cooler question (`6 of 183`) and click the **Equity & Impact** tab in the left sidebar.

**Say out loud:**
> *"If I need to ask a general question—like 'Excluding the 9 test cases, how many real Chicago pantries have a walk-in
> cooler?'—RescueBroker checks the live database and tells me: **only 6 out of 183 (3.3%)**.*
> *Finally, did the food go where the need is, or where the loading docks are? We excluded the 9 planted test cases and
> audited all 10 offers across the 183 real Chicago charities three ways: counted **per offer**, our matches sit in
> higher-poverty (22%) and lower-car-ownership (30%) areas than average—but our cold review showed that's because **one
> fast pantry** in a high-need neighborhood won three short-clock grocery offers. Counted **per unique charity**, the
> averages sit slightly lower; and **weighted by pallets**, public assistance drops from 19% to **9%**, because 30 of the
> 37.5 pallets are huge farm loads that can only fit in the 14 charities with 5-plus pallet room.*
> *We are completely upfront about our limits: the 183 charity names and addresses are real IRS records, while cooler
> sizes and pickup hours are generated, shelf life is home guidance, and locations are ZIP-code centers—so every brief
> reminds staff to confirm by phone. Next, we're adding delivery memory so one fast pantry isn't called three times in a
> row, automatic load splitting for big farm offers, and a 2-minute pantry self-check-in."*
