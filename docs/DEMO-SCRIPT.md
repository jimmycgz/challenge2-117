# Demo script for the pitch video (~3 minutes)

Navigation: [deck outline](DECK-OUTLINE.md) · [submission checklist](SUBMISSION.md) ·
[agent README](../agent/food_broker/README.md) · [equity audit](../agent/food_broker/EQUITY-AUDIT.md) ·
[captured evidence](evidence/README.md) · [design & benchmarks](DESIGN.md).

Plan for **three minutes** of screen share with one person narrating. Judges watch the recording asynchronously after
the event with no live Q&A, so every differentiator, UX choice, and mandatory judge check below is explicitly shown on
screen and spoken out loud.

---

## Before you record (Two-Tab Setup)

1. **Tab 1 — RescueBroker Coordinator Dispatch Console (`frontend/index.html`):**
   - Serve locally (`python3 frontend/serve.py`, then open `http://127.0.0.1:8080`) or open the deployed console.
   - Start on the **Splash Screen** so your opening click launches the **Live Dispatch Queue** (showing the 11 ticking
     clocks, openFDA Recall Banner, 4-KPI Capacity Bar, Spatial Map of the 183 real recipients, and the collapsible
     Right Agent Copilot).
2. **Tab 2 — Live Cloud Run ADK Endpoint (`https://food-broker-817377390808.us-east1.run.app/dev-ui/`):**
   - Pick the `food_broker` agent and keep it ready to show the raw ADK tool trace (`lookup_shelf_life` $\rightarrow$
     `find_matches` $\rightarrow$ `explain_candidate` $\rightarrow$ `execute_sql`), or use the **Right Agent Copilot
     Drawer** directly inside Tab 1 (which calls the exact same Cloud Run `/run` endpoint).
3. **Keep [`docs/evidence/`](evidence/README.md) open in a background tab** in case a live Cloud Run call takes >15s.

---

## 1. The Hook & Why We Built a Dispatch Console, Not Just a Chat Box (0:00 – 0:25 | 25s)

**On screen:** Start on the **RescueBroker Splash Page**, click **Launch Live Dispatch**, and sweep the cursor across
the **Ticking-Clock Surplus Queue** on the left and the **Chicago Pantry Map** on the right.

**Say out loud:**
> *"We coordinate food rescue in Chicago. It is Thursday afternoon, and a grocer has just offered us ten crates of
> fresh spinach that must leave their dock within six hours and stay cold. Here is who we would call, and what we don't
> know about them.*
> *Most teams stop at a developer chat box. Our user is an internal dispatch coordinator juggling eleven expiring
> offers under a ticking clock—so we built RescueBroker: a Coordinator Dispatch Console connected live to our ADK agent
> on Cloud Run, combining a ticking-clock queue, spatial map, openFDA recall gate, and conversational Copilot."*

---

## 2. Posting 1: Retail Spinach, The `top_k=80` Pool & The Rank #3 Decoy (0:25 – 1:15 | 50s)

**On screen:** Select **Posting #1 (10 Crates of Spinach — 6h left)** in the queue, or send the prompt in the Agent
Copilot / `/dev-ui/`:

```text
A grocer in Chicago has ten crates of spinach, harvested yesterday, that must leave the dock within 6 hours and stay cold.
```

**Point at, in this order:**
1. **The Scannable 6-Part Match Brief & 4-KPI Bar:** Named organization, real IRS street address, **Domestic/Vehicle Cold
   Storage**, **0.5 of 1 pallet**, **6h clock vs. 3h pickup (+3h safety buffer)**, and the **⚠️ Dispatch Volunteer Driver**
   flag.
2. **Why `top_k=80` & Why Meaning Alone Fails (`80 searched → 12 viable` badge + Rejected Decoys list):**
   - Slow down here—this is the signature moment of the pitch.
   - **Say out loud:**
     > *"Under the hood, our agent calls `lookup_shelf_life`, then `find_matches`, which runs BigQuery `VECTOR_SEARCH`
     > over 192 recipient profiles with a wide pool of 80. Why 80? We measured it: for this spinach offer, a pool of 15
     > leaves only 1 viable recipient, 40 leaves 3, and 80 leaves 12.*
     > *Look at the rejected matches at the bottom: the top three semantic matches by meaning were all wrong—all three
     > needed 12 to 21 hours to collect against a 6-hour clock, and **Greenline Community Pantry**, ranked 3rd by
     > meaning (one of nine invented teaching cases in the challenge data), writes that its families ask most for fresh
     > greens while having **zero refrigeration of any kind**.*
     > *Even the nearest candidate that passes hard filters at rank 11 only has a household fridge and 1 hour of slack—so
     > our tiered ranking picks ranks 50, 54, and 63, prioritizing a comfortable 2-to-3 hour safety buffer and sturdy
     > cold storage over raw embedding distance."*

---

## 3. Multi-Turn Follow-Ups: "They Said No" & "Why Not the Big Food Bank Downtown?" (1:15 – 1:45 | 30s)

**On screen:** Click **"Recipient Declined — Next Option"** in the console (or type in the same session):

```text
They said no. Who's next?
```

Then immediately ask:

```text
Why them and not the big food bank downtown?
```

**Point at & say out loud:**
> *"Coordinators live in a world where pantries don't answer the phone. When the primary match declines, our tool
> re-runs with `exclude_names`, promotes the runner-up with a fresh SMS, and queues the next backup.*
> *And when the coordinator asks 'Why not the big food bank downtown?', our `explain_candidate` tool searches the
> 80-candidate pool by name and reports its exact semantic rank and why it was eliminated—for example, Americas Food
> Bank at rank 29, removed because it needs 41 hours to collect against a 6-hour clock."*

---

## 4. Three Tracks Through One Corpus + Two Data Traps We Caught (1:45 – 2:25 | 40s)

**On screen:** Click **5 Tons of Potatoes (Farm)**, **48 Cases of Sealed Infant Formula (Essentials)**, and **40 Trays
of Cream Pastries (1h Bakery Refusal)** (or show the **Route Optimizer** / transcripts):

```text
A farm south of Chicago has 5 tons of potatoes still in the field. They can load pallets if someone collects within 3 days.
```
```text
48 cases of sealed infant formula with 8 months to expiry from a distributor in Chicago, 2 pallets, can sit at room temperature.
```
```text
A bakery has 40 trays of cream-filled pastries that must stay refrigerated and leave their dock within 1 hour.
```

**Point at & say out loud:**
> *"The exact same corpus and pipeline handle all three tracks with zero track-specific rulebooks:*
> *Five tons of farm potatoes—about 5 pallets—filters out small pantries and household fridges (which we cap at 1
> pallet) to route to a high-capacity warehouse with a loading dock.*
> *On the 48 cases of sealed infant formula, we caught a real data trap in USDA FoodKeeper: the table lists infant
> formula at **1 hour**—which is the figure for a prepared, opened bottle, not sealed cases with 8 months left. Our
> `lookup_shelf_life` tool triggers a `_shelf_caution` warning on any figure under 2 hours and honors the donor's
> 8-month expiry.*
> *And on the 1-hour bakery offer, zero organizations can collect in time. Instead of guessing, the agent safely refuses
> and shows the closest rejections."*

---

## 5. Google Managed BigQuery MCP: Only 6 of 183 Real Walk-In Coolers (2:25 – 2:40 | 15s)

**On screen:** Show the free-form MCP question:

```text
Not counting the invented teaching cases (profile_source 'planted'), how many recipients have walk-in cold storage, and what share is that?
```

**Point at & say out loud:**
> *"For free-form questions outside a posting, the agent queries Google's Managed BigQuery MCP server in read-only
> mode. Excluding the 9 planted teaching cases, only **6 of the 183 real recipients (3.3%)** have a walk-in cooler—and
> posting matches never touch free-form SQL so our safety filters can never be bypassed."*

---

## 6. The 3-Lens Equity Audit & Honest Limitations Close (2:40 – 3:00 | 20s)

**On screen:** Click the **Equity & Impact** view in the left navigation rail (or show the table in
[`EQUITY-AUDIT.md`](../agent/food_broker/EQUITY-AUDIT.md)).

**Say out loud:**
> *"Finally, did the food go where the need is, or where the loading docks are? We excluded the 9 invented teaching
> cases and audited all 10 postings across the 183 real IRS recipients three ways:*
> *Counted **per posting**, matches sit near or slightly above the corpus (22% poverty, 30% no-vehicle)—but our cold
> review proved that's because **one fast pantry** in a high-need tract won three short-clock postings. Counted **once
> per distinct recipient**, matches sit lower on all three measures. And **weighted by pallets**, public assistance
> drops from 19% to **9%**, because 30 of the 37.5 pallets are farm loads that can only go to the few recipients with
> 5-plus pallet capacity.*
> *Our boundaries are explicit: 183 recipient names and addresses are real IRS records (plus 9 planted cases), while all
> storage, capacity, and pickup times are generated; shelf life is consumer guidance; and locations are ZIP-level. Next,
> we're adding persistent delivery memory so one pantry isn't called three times a day, and backend load splitting for
> oversized farm offers."*

---

## Fallback Links (If Live Cloud Run Is Slow During Recording)

All pre-captured live outputs are committed in [`docs/evidence/`](evidence/README.md):
- Spinach + Decoy Rank #3: [`spinach-answer.md`](evidence/spinach-answer.md) & [`spinach-brief.json`](evidence/spinach-brief.json)
- 6-Turn Follow-Up ("They said no" + "Why not X?"): [`follow-ups-transcript.md`](evidence/follow-ups-transcript.md)
- Sealed Infant Formula (1h table trap vs 8-month expiry): [`sealed-formula-answer.md`](evidence/sealed-formula-answer.md)
- Farm 5-Ton Potatoes: [`farm-potatoes-answer.md`](evidence/farm-potatoes-answer.md)
- 1-Hour Bakery Safe Refusal: [`no-match-bakery-answer.md`](evidence/no-match-bakery-answer.md)
- Managed BigQuery MCP (`6 of 183` walk-in coolers): [`mcp-walk-in-answer.md`](evidence/mcp-walk-in-answer.md)
- Pool Study (`top_k` 15 $\rightarrow$ 1, 40 $\rightarrow$ 3, 80 $\rightarrow$ 12): [`pool-study.txt`](evidence/pool-study.txt)

