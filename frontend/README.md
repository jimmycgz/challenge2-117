# Chicago Food Rescue — Coordinator Dispatch Console (`frontend/`)

Staff-facing operational web console for the **Chicago Food Rescue Broker** (`food_broker` ADK agent), built for **[Issue #17](https://github.com/jimmycgz/challenge2-117/issues/17)** and **[Issue #14](https://github.com/jimmycgz/challenge2-117/issues/14)**.

---

## Quick Start

Run the local static server + Cloud Run CORS proxy from the repository root:

```bash
python3 frontend/serve.py
```

Then open **`http://localhost:8090`** in your browser.
* `serve.py` serves `frontend/index.html` and `frontend/recipients_data.js` locally and transparently proxies `/apps/*`, `/run`, `/run_sse`, `/list-apps`, and `/health` to the deployed Cloud Run service (`https://food-broker-817377390808.us-east1.run.app`).
* If you uncheck **Call Live Cloud Run (`/run`)** in the header (or if offline), the console runs in **Instant Replay Mode** using the verified Cloud Run outputs cached in `frontend/recipients_data.js`.

---

## Features Implemented

1. **⏱️ Ticking-Clock Surplus Queue ([Issue #14](https://github.com/jimmycgz/challenge2-117/issues/14)):**
   * Displays all 10 `a4i_food.surplus_postings` rows plus the 1-hour bakery cream-pastries refusal case, sorted by urgency (`hours_remaining ASC`) with `🔴 <= 2h`, `🟡 <= 6h`, and `🟢 > 6h` badges and 1-click dispatch.
2. **📷 Multimodal Crate / Tag Photo Intake ([Issue #14](https://github.com/jimmycgz/challenge2-117/issues/14)):**
   * Supports uploading/dropping produce crate or pallet label photos (`inlineData` base64 image sent to ADK's `POST /run`) + includes a 1-click **`[ 🥬 Load Sample Crate Tag ]`** generator for reproducible live demos.
3. **🎙️ Push-to-Talk Voice Dictation:**
   * Built-in `SpeechRecognition` / `webkitSpeechRecognition` microphone button (`🎙️ Speak`) for hands-free coordinator intake and follow-up commands.
4. **🛡️ Live openFDA Food Recall & Safety Gate ([Issue #11](https://github.com/jimmycgz/challenge2-117/issues/11)):**
   * Automatically queries the public-domain (CC0) US Government `api.fda.gov/food/enforcement.json` endpoint for ongoing recalls matching the active food commodity, with a 1-click **`[ 🛑 Halt Load: Flag Recall / Spoilage ]`** safety lock.
5. **🗺️ Interactive Chicago Dispatch Map (Leaflet.js + Real 192 IRS Coordinates) & Honest Data Badge:**
   * Plots the Donor Origin (`🏪`), Primary Match (`🏆 #1` green marker + dashed route line + straight-line miles), Next Two Backups (`🔵 #2/#3`), and Rejected Semantic Decoys (`🔴` red markers with `semantic_rank` and exact failure reasons).
   * Displays the **Architectural Honesty Badge** noting that recipient coordinates are IRS ZIP-code centroids and distances use straight-line `ST_DISTANCE`.
6. **⚡ Delivery & Expiry Timeline + Unexpected Delay Re-Router:**
   * Visualizes `Now (0h)` → `Collection Lead Time` → `Spoilage / Dock Deadline` with slack margin coloring.
   * Clicking **`[ 🚨 +3.5h Delay (At Risk → Auto Re-Route) ]`** shrinks the remaining clock, flags when the active recipient's lead time exceeds the remaining hours, and dispatches an automatic re-route turn to the agent.
7. **🔒 Pallet Reservation Lock ([Issue #12](https://github.com/jimmycgz/challenge2-117/issues/12)), Pantry Onboarding ([Issue #10](https://github.com/jimmycgz/challenge2-117/issues/10)) & 3-Tier Problem Reporting:**
   * **`[ 🔒 Claim & Lock Pallets ]`** tracks daily claimed pallet capacity per recipient.
   * **`[ ⚠️ Cooler Broken ]` / `[ ⚠️ Capacity Full ]` / `[ ⚠️ Closed Today ]`** logs ground-truth profile corrections in the **Live Discrepancy, Lock & Safety Log** (exportable as JSON) and triggers an automatic re-match (`exclude_names`).
   * **`[ 🐛 Report System Bug ]`** opens a pre-populated GitHub Issue on `jimmycgz/challenge2-117` with session context attached.
