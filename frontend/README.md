# Chicago Food Rescue — Coordinator Dispatch Console (`frontend/`)

Staff-facing operational web console for the **Chicago Food Rescue Broker** (`food_broker` ADK agent), built for **[Issue #17](https://github.com/jimmycgz/challenge2-117/issues/17)** and **[Issue #14](https://github.com/jimmycgz/challenge2-117/issues/14)**.

---

## Quick Start

Run the local static server + Cloud Run CORS proxy from the repository root:

```bash
python3 frontend/serve.py
```

Then open **`http://127.0.0.1:8090`** in your browser.

* `serve.py` listens on `127.0.0.1` only, serves `frontend/index.html` and `frontend/recipients_data.js`, and proxies `/apps/*`, `/run`, `/run_sse`, `/list-apps`, and `/health` to the deployed Cloud Run service (`https://food-broker-817377390808.us-east1.run.app`).
* If you uncheck **Live Agent** in the header, nothing is sent to the agent. Four postings (spinach, potatoes, infant formula and the bakery case) have a saved Cloud Run answer in `frontend/recipients_data.js`, shown only for its own posting and labelled as saved. For any other posting, or when a live call fails, the page says that no live answer is available and does not show a saved answer from a different posting.

---

## Features Implemented

1. **⏱️ Ticking-Clock Surplus Queue ([Issue #14](https://github.com/jimmycgz/challenge2-117/issues/14)):**
   * Displays all 10 `a4i_food.surplus_postings` rows plus the 1-hour bakery cream-pastries refusal case, sorted by urgency (`hours_remaining ASC`) with `🔴 <= 2h`, `🟡 <= 6h`, and `🟢 > 6h` badges and 1-click dispatch.
2. **📷 Multimodal Crate / Tag Photo Intake ([Issue #14](https://github.com/jimmycgz/challenge2-117/issues/14)):**
   * Supports uploading/dropping produce crate or pallet label photos (`inlineData` base64 image sent to ADK's `POST /run`) + includes a 1-click **`[ 🥬 Load Sample Crate Tag ]`** generator for reproducible live demos.
3. **🎙️ Push-to-Talk Voice Dictation:**
   * Built-in `SpeechRecognition` / `webkitSpeechRecognition` microphone button (`🎙️ Speak`) for hands-free coordinator intake and follow-up commands.
4. **🛡️ Live openFDA Food Recall & Safety Gate ([Issue #11](https://github.com/jimmycgz/challenge2-117/issues/11)):**
   * Automatically queries the public-domain (CC0) US Government `api.fda.gov/food/enforcement.json` endpoint for ongoing recalls matching the active food commodity, with a 1-click **`[ 🛑 Halt Load: Flag Recall / Spoilage ]`** safety lock. If the request fails or times out, the strip says "not checked", never "clear".
5. **🗺️ Interactive Chicago Dispatch Map (Leaflet.js; 183 real organizations plus nine invented teaching cases, all ZIP-level):**
   * Plots the Primary Match (green), Next Two Backups (blue), and Rejected Semantic Decoys (red, with `semantic_rank` and the reason each was removed).
   * The donor pin is illustrative: an invented point, because the postings have no donor location. There are no route lines and no distances.
   * Invented teaching cases (`profile_source` is `"planted"`, or the ZIP is empty) are labelled "(invented teaching case)" and are not plotted; names not found in the location lookup are listed under the map without a pin.
6. **⚡ Delivery & Expiry Timeline + Unexpected Delay Re-Router:**
   * Visualizes `Now (0h)` → `Collection Lead Time` → `Spoilage / Dock Deadline` with slack margin coloring.
   * Clicking **`[ 🚨 +3.5h Delay (At Risk → Auto Re-Route) ]`** shrinks the remaining clock, flags when the active recipient's lead time exceeds the remaining hours, and dispatches an automatic re-route turn to the agent.
7. **🔒 Pallet Reservation Lock ([Issue #12](https://github.com/jimmycgz/challenge2-117/issues/12)), Pantry Onboarding ([Issue #10](https://github.com/jimmycgz/challenge2-117/issues/10)) & 3-Tier Problem Reporting:**
   * **`[ 🔒 Claim & Lock Pallets ]`** tracks daily claimed pallet capacity per recipient.
   * **`[ ⚠️ Cooler Broken ]` / `[ ⚠️ Capacity Full ]` / `[ ⚠️ Closed Today ]`** logs ground-truth profile corrections in the **Live Discrepancy, Lock & Safety Log** (exportable as JSON) and triggers an automatic re-match (`exclude_names`).
   * **`[ 🐛 Report System Bug ]`** opens a pre-populated GitHub Issue on `jimmycgz/challenge2-117` with session context attached.
8. **Next match:** **They said no — who's next?** and **Next Match** send "They said no. Who's next?" to the same agent session through `/run` and show the agent's own answer.
9. **Equity Study:** a summary of the current figures (183 recipients, the nine invented cases left out) with a link to [`agent/food_broker/EQUITY-AUDIT.md`](../agent/food_broker/EQUITY-AUDIT.md).
