# Chicago Food Rescue — Coordinator Dispatch Console (`frontend/`)

Staff-facing operational web console for the **Chicago Food Rescue Broker** (`food_broker` ADK agent), built for **[Issue #17](https://github.com/jimmycgz/challenge2-117/issues/17)** and **[Issue #14](https://github.com/jimmycgz/challenge2-117/issues/14)**.

---

## Quick Start

Run the local static server + Cloud Run CORS proxy from the repository root:

```bash
python3 frontend/serve.py
```

Then open **`http://127.0.0.1:8090`** in your browser.

* `serve.py` listens on `127.0.0.1` only, serves `frontend/index.html` and `frontend/recipients_data.js`, provides transactional state endpoints (`/api/state`, `/api/state/claim`, `/api/state/decline`, `/api/state/release`, `/api/state/onboard`), and proxies `/apps/*`, `/run`, `/run_sse`, `/list-apps`, and `/health` to the deployed Cloud Run service (`https://food-broker-817377390808.us-east1.run.app`).
* If you uncheck **Live Agent** in the header, nothing is sent to the agent. Four postings (spinach, potatoes, infant formula and the bakery case) have a saved Cloud Run answer in `frontend/recipients_data.js`, shown only for its own posting and labelled as saved. For any other posting, or when a live call fails, the page says that no live answer is available and does not show a saved answer from a different posting.

---

## Features Implemented

1. **⏱️ Ticking-Clock Surplus Queue ([Issue #14](https://github.com/jimmycgz/challenge2-117/issues/14)):**
   * Displays all 10 `a4i_food.surplus_postings` rows plus the 1-hour bakery cream-pastries refusal case, sorted by urgency (`hours_remaining ASC`) with `🔴 <= 2h`, `🟡 <= 6h`, and `🟢 > 6h` badges and 1-click dispatch.
2. **📷 Multimodal Crate / Tag Photo Intake ([Issue #14](https://github.com/jimmycgz/challenge2-117/issues/14)):**
   * Supports uploading/dropping produce crate or pallet label photos (`inlineData` base64 image sent to ADK's `POST /run`) + includes a 1-click **`[ 🥬 Load Sample Crate Tag ]`** generator for reproducible live demos.
3. **🎙️ Push-to-Talk Voice Dictation:**
   * Built-in `SpeechRecognition` / `webkitSpeechRecognition` microphone button (`🎙️ Speak`) for hands-free coordinator intake and follow-up commands.
4. **🛡️ Live openFDA Food Recall & Safety Gate + 3-Point Dock Checklist ([Issue #11](https://github.com/jimmycgz/challenge2-117/issues/11)):**
   * Automatically queries the public-domain (CC0) US Government `api.fda.gov/food/enforcement.json` endpoint for ongoing recalls matching the active food commodity, with a 1-click **`[ 🛑 Halt Load: Flag Recall / Spoilage ]`** safety lock and 3-point Coordinator Dock Safety Checklist sign-off. If the request fails or times out, the strip says "not checked", never "clear".
5. **🗺️ Interactive Chicago Dispatch Map (Leaflet.js + Google Maps JS SDK; 183 real organizations plus nine invented teaching cases, all ZIP-level):**
   * Plots the Primary Match (green), Next Two Backups (blue), and Rejected Semantic Decoys (red, with `semantic_rank` and the reason each was removed).
   * The donor pin is illustrative: an invented point, because the postings have no donor location. There are no route lines and no distances.
   * Invented teaching cases (`profile_source` is `"planted"`, or the ZIP is empty) are labelled "(invented teaching case)" and are not plotted; names not found in the location lookup are listed under the map without a pin.
6. **📦 Multi-Recipient Load Splitter ([Issue #6](https://github.com/jimmycgz/challenge2-117/issues/6)):**
   * Splits large 5–15 pallet farm offers (e.g., 10p Blueberries, 15p Squash, 5p Potatoes) across 2–4 verified Chicago recipients whose combined open pallet capacity covers the full load before the pickup clock expires, with individualized Split Outreach SMS drafts and 1-click pallet reservation locking.
7. **🔒 Stateful Pallet Reservation Lock, `HTTP 409` Concurrency Guard ([Issue #12](https://github.com/jimmycgz/challenge2-117/issues/12)) & Conversational Pantry Onboarding ([Issue #10](https://github.com/jimmycgz/challenge2-117/issues/10)):**
   * Transactional local state engine (`/api/state/*`) tracks daily claimed pallet capacity per recipient, returns `HTTP 409 LOCK_CONFLICT` on competing coordinator/driver claims, persists `"They Said No"` declines (`exclude_names`), and stores verified pantries with Track 1/2 unloading disambiguation.
8. **⚖️ Interactive 10-Posting Equity Study & Counterfactual Explorer ([Issue #13](https://github.com/jimmycgz/challenge2-117/issues/13)):**
   * Compares the 183 real Chicago organizations against the 192-row counterfactual (with the 9 planted teaching cases) across all 10 official postings and track filters (`Retail`, `Farm`, `Essentials`, `Repeat`), matching [`agent/food_broker/EQUITY-AUDIT.md`](../agent/food_broker/EQUITY-AUDIT.md).
