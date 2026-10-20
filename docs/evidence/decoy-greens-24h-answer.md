<!-- markdownlint-disable MD001 MD009 MD022 MD029 MD030 MD031 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: A grocer has 8 crates of fresh salad greens and spinach that must stay cold; they can hold it in their cooler for 24 hours.

Captured 14:40 EDT on 2026-10-20. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "Spinach", "storage_state": "refrigerated"})
find_matches({"needs_frozen": false, "load_description": "8 crates of fresh salad greens and spinach", "search_text": "Fresh salad greens and spinach requiring refrigeration, small scale fresh produce load for immediate distribution", "hours_remaining": 24, "needs_cold": true, "donor_description": "A local grocer", "pallets": 0.25})
```

---

Fresh salad greens and spinach, so they must stay cold; 8 crates convert to approximately 0.25 pallets (assuming ~32 standard produce crates per pallet). FoodKeeper lists "Bagged greens (leaf, spinach, lettuce, etc.)" at 120 hours refrigerated shelf life (consumer guidance, not a cold-chain guarantee), so the donor's 24-hour deadline sets the clock.

1. **Who, and why**
   Maple Street Produce Alliance, Chicago, IL (an invented teaching case in the challenge data). Fitted by its profile: "Fresh produce hub with walk-in refrigeration and our own reefer truck. Roughly 600 households weekly, and perishables move through us in under two days."

2. **What they can actually take**
   Profile on file indicates walk-in cold storage with a maximum capacity of 10 pallets, which easily accommodates this 0.25-pallet load. Operational details are generated, so confirm by phone before dispatching.

3. **The clock**
   The food has 24 hours remaining. Maple Street Produce Alliance has a collection lead time of 12 hours, giving a comfortable margin of 12 hours. They have refrigerated transport on file, so no external driver is needed.

4. **Whose neighborhood it helps**
   Serves roughly 600 households weekly (general public). In the nearest census tract, 9% of residents live below the poverty line, 11% of households lack a vehicle, and 12% receive food or cash assistance.

5. **The outreach message**
   Hello Maple Street Produce Alliance team,

   A local grocer has 8 crates of fresh salad greens and spinach. It is still good but has to move soon. From what we have on file you have the storage for it. The food needs to leave by about 24 hours from now, which leaves you roughly 12 hours of slack to collect. You are set up to collect it yourselves.

   Can you take it? If you can, tell us the time you can collect and a phone number for pickup. If not, a quick no helps us move to the next place.

   Thank you,
   [Coordinator name]

6. **The next two options**
   - Option 2: Chicago Food Rescue (2426 W DAKIN ST 2, CHICAGO, IL 60618) – vehicle cold storage, takes up to 2 pallets, collects within 8 hours (16-hour margin).
   - Option 3: Cedar Street Produce Alliance, Chicago, IL (an invented teaching case) – walk-in cold storage, takes up to 10 pallets, collects within 12 hours (12-hour margin).

   *Rejected close matches:*
   - Ranked 2nd by meaning, removed: no cold storage (Greenline Community Pantry)
   - Ranked 19th by meaning, removed: capacity 0 pallets, load is 0.25 (One Patient - Global Health Initiative Ltd)
   - Ranked 21st by meaning, removed: capacity 0 pallets, load is 0.25 (Mercy To Mankind Clinic Nfp)
