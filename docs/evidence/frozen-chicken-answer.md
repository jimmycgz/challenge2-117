<!-- markdownlint-disable MD001 MD009 MD022 MD029 MD030 MD031 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: A grocer in Chicago has 6 cases of frozen chicken, stored at minus 18, that must be collected within 24 hours.

Captured 14:40 EDT on 2026-10-20. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "Chicken", "storage_state": "refrigerated"})
find_matches({"donor_description": "A grocer in Chicago", "needs_frozen": true, "hours_remaining": 24, "search_text": "frozen chicken meat poultry freezer storage small load 6 cases", "pallets": 0.1, "load_description": "6 cases of frozen chicken", "needs_cold": true})
```

---

Frozen chicken, so it must stay cold and stay frozen; 6 cases is roughly 0.1 pallets (estimating ~60 cases per full pallet). FoodKeeper lists refrigerated/frozen chicken shelf life well beyond this (~336 hours), so the donor's 24-hour deadline set the clock (consumer guidance, not a cold-chain guarantee).

1. **Who, and why**  
   **Top Box Foods**  
   222 MERCHANDISE MART PLZ, CHICAGO, IL 60654  
   *Why they fit:* Profile highlights: "Central warehouse and redistribution center for 20 member pantries. Racked warehouse with temperature-controlled bays and a monitored freezer." (Note: Top Box Foods is a real organization, but operational details like storage, capacity, and pickup times are generated, not verified—confirm by phone before moving).

2. **What they can actually take**  
   According to their profile on file, they have walk-in cold storage and freezer storage, a capacity of up to 17 pallets (this load is 0.1 pallets / 6 cases), a loading dock, and active service days Monday through Friday.

3. **The clock**  
   - Food has: 24 hours remaining  
   - Recipient collection lead time: 14 hours  
   - Margin: 10 hours of slack  
   - Driver needed: No driver needed (profile indicates they have refrigerated transport).

4. **Whose neighborhood it helps**  
   Serves the general public (~3,162 households per week). Nearest census tract figures: 4% poverty rate, 32% of households without a vehicle, and 0% on food/cash assistance (tract figures reflect the broader ZIP area, not the exact block).

5. **The outreach message**  
   Hello Top Box Foods team,

   A grocer in Chicago has 6 cases of frozen chicken stored at -18°C. It is in good condition but needs to be collected within 24 hours. From what we have on file, you have monitored freezer storage for it. A pickup within your 14-hour window leaves roughly 10 hours of margin, and your profile indicates you can collect directly.

   Can you take it? If so, please let us know what time you can collect and a phone number for pickup. If not, a quick no helps us move to the next recipient.

   Thank you,  
   [Coordinator name]

6. **The next two options**  
   - **Option 2:** Harborview Neighbors Trust (Chicago, IL; profile_source is planted—an invented teaching case in the challenge data, not a real organization): walk-in cold storage, takes up to 6 pallets, collects within 12 hours (12 hours margin, needs driver).  
   - **Option 3:** Tca Health Inc Nfp (1029 E 130TH ST, CHICAGO, IL 60628): medical cold storage, takes up to 2 pallets, collects within 18 hours (6 hours margin, needs driver).  

   *Close semantic matches that were rejected:*  
   - Ranked 2nd by meaning, removed: capacity 0 pallets, load is 0.1; needs 62h to collect, food has 24h (Earth Angels Ministry Of Helps)  
   - Ranked 3rd by meaning, removed: no freezer (Chicago Food Rescue)  
   - Ranked 23rd by meaning, removed: no cold storage; no freezer (Lakeshore Mutual Aid Collective)
