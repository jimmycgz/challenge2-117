# Deliverables, Team Roster & Judging Rubric Reference

## 1. Team GitHub Handles & Self-Pickup Workflow

Teammates pick up open issues (`needs-pickup` or `optional-pickup`) themselves. Only work already committed to the repo is pre-credited; all open tasks carry `assignee: unassigned` until claimed.

| GitHub Handle | Completed / Claimed Work |
| :--- | :--- |
| `@jimmycgz` | **Completed in PR #1:** Data & Equity Audit (`#5`), Core Agent Tools (`#6` core), Prompt & 6-turn Follow-Up Eval (`#7`), Cloud Run Service (`food-broker-00007-4sm`) |
| `@k0d3r3d` | **Completed in PR #2:** PRD, HLD, Project Plan Checklist (`docs/`) & Issue Board Setup |
| `@f1mahesh` | Available to self-assign any `needs-pickup` (`#4`, `#8`, `#9`) or `optional-pickup` (`#6`, `#10`–`#14`) issue |
| `@kkeremkurt` | Available to self-assign any `needs-pickup` (`#4`, `#8`, `#9`) or `optional-pickup` (`#6`, `#10`–`#14`) issue |
| `@mb-misha` | Available to self-assign any `needs-pickup` (`#4`, `#8`, `#9`) or `optional-pickup` (`#6`, `#10`–`#14`) issue |

---

## 2. The 4 AngelHack Portal Deliverables (`https://portal.angelhack.com/a4i-console`)

| # | Portal Field | Required Value / Artifact | Status |
| :--- | :--- | :--- | :--- |
| 1 | **GitHub Repository Link** | `https://github.com/jimmycgz/challenge2-117` (with PR #1 merged to `main` and tagged `submission`) | 🟡 Needs PR #1 merge |
| 2 | **Google Skills / GCP Project Link** | Lab link for `qwiklabs-gcp-04-6c7101c1dba1` (Project Number `817377390808`) | 🟢 Live |
| 3 | **Pitch Deck** | 8-slide deck built from `docs/DECK-OUTLINE.md` | 🔴 Needs slide deck file/link |
| 4 | **Pitch Video** | ~3-minute screen recording following `docs/DEMO-SCRIPT.md` on `https://food-broker-817377390808.us-east1.run.app/dev-ui/` | 🔴 Needs video recording |

---

## 3. The 4 Mandatory Judge Checks (Verify Before Submitting Deck & Video)

1. **Real vs. Generated Data:**
   * **REAL:** IRS 990 recipient names/addresses (`recipients`), USDA FoodKeeper shelf life (`shelf_life`), US Census ACS tract demographics (`tract_demographics`).
   * **GENERATED:** Cold storage (`cold_storage`), pallet capacity (`max_pallets`), pickup lead time (`pickup_window_hours`), refrigerated transport (`refrigerated_transport`), and `surplus_postings`.
2. **Genuine Vector Search + Why Top-K Alone Fails:**
   * BigQuery `VECTOR_SEARCH` + `AI.EMBED` on `a4i_food.recipient_embeddings` (`top_k=80`).
   * For the 6-hour spinach offer on 192 Chicago recipients: `top_k=15` leaves **1** viable match; `top_k=40` leaves **3**; `top_k=80` leaves **12**.
   * The top 3 closest semantic matches are all eliminated by hard constraints—including *Greenline Community Pantry* at semantic rank #3 (`cold_storage = "none"`). The first viable recipients sit at semantic ranks **50, 54, and 63**.
3. **10-Posting Equity Audit (`agent/food_broker/EQUITY-AUDIT.md`):**
   * **Metro Baseline (1,004 tracts, pop-weighted):** `15%` poverty, `20%` no-vehicle, `18%` assistance.
   * **All Recipients Corpus (192 orgs on 76 tracts):** Mean `19%` poverty, `27%` no-vehicle, `20%` assistance.
   * **Top Matches Per Posting (n=10):** Mean `22%` poverty, `31%` no-vehicle, `20%` assistance (driven by *Shakespear Rose Community Table* winning 3 short-clock retail offers in a `45%` poverty / `52%` no-vehicle tract).
   * **Top Matches Per Distinct Recipient (n=8):** Mean `17%` poverty, `26%` no-vehicle, `16%` assistance.
   * **Top Matches Weighted by Pallets (37.5 pallets):** Mean `15%` poverty, `32%` no-vehicle, `9%` assistance (only 17 of 192 recipients have a dock or 5+ pallet capacity for farm loads).
4. **Honest Limitations & Caught Data Bug:**
   * USDA FoodKeeper gave sealed infant formula `1 hour` (an opened-container figure); `_shelf_caution` warns on `<= 2h` figures and uses the donor's 8-month expiry.
   * Recipient coordinates are ZIP-level centroids (`ST_DISTANCE` to nearest tract internal point).
   * No delivery history store (fastest collector wins repeated short-clock offers) and no multi-recipient load splitting built yet.
