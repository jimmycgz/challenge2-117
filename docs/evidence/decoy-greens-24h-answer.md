<!-- markdownlint-disable MD001 MD009 MD022 MD029 MD030 MD031 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: A grocer has 8 crates of fresh salad greens and spinach that must stay cold; they can hold it in their cooler for 24 hours.

Captured 14:14 EDT on 2026-10-20. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "Spinach", "storage_state": "refrigerated"})
find_matches({"search_text": "fresh salad greens spinach cold storage produce small pantry crate load", "needs_cold": true, "pallets": 0.25, "needs_frozen": false, "hours_remaining": 24, "donor_description": "A local grocer", "load_description": "8 crates of fresh salad greens and spinach"})
```

---

Fresh salad greens and spinach, so it must stay cold; 8 crates is roughly 0.25 pallets (about a quarter of a pallet). FoodKeeper lists "Bagged greens (leaf, spinach, lettuce, etc.)" at 120 hours refrigerated, but the donor's 24-hour cooler deadline sets the clock.

**1. Who, and why**
Maple Street Produce Alliance, an invented teaching case (Chicago, IL). Fit: "Fresh produce hub with walk-in refrigeration and our own reefer truck. Roughly 600 households weekly, and perishables move through us in under two days."

**2. What they can actually take**
Profile on file indicates walk-in cold storage (no freezer) with a capacity of up to 10 pallets and a loading dock, which easily accommodates this 0.25-pallet load. Operational details are generated, so confirm by phone before the truck moves.

**3. The clock**
The food has 24 hours remaining (capped by the donor's cooler limit). The recipient's collection lead time is 12 hours, leaving a comfortable margin of 12 hours. They have refrigerated transport on file, so no separate driver is needed.

**4. Whose neighborhood it helps**
Serves the general public (~600 households weekly). Nearest census tract figures: 9% of residents below the poverty line, 11% of households without a vehicle, and 12% receiving food or cash assistance (ZIP-level approximation).

**5. The outreach message**
Hello Maple Street Produce Alliance team,

A local grocer has 8 crates of fresh salad greens and spinach. It is still good but has to move soon. From what we have on file you have the storage for it. The food needs to leave by about 24 hours from now, which leaves you roughly 12 hours of slack to collect. You are set up to collect it yourselves.

Can you take it? If you can, tell us the time you can collect and a phone number for pickup. If not, a quick no helps us move to the next place.

Thank you,  
[Coordinator name]

**6. The next two options**
- Option 2: Cedar Street Produce Alliance, an invented teaching case (Chicago, IL) — walk-in cold storage, takes up to 10 pallets, collects within 12h (12h margin).
- Option 3: Chicago Food Rescue (2426 W Dakin St 2, Chicago, IL 60618) — vehicle cold storage, takes up to 2 pallets, collects within 8h (16h margin).

Close semantic matches removed by filters:
- Greenline Community Pantry (an invented teaching case): ranked 1st by meaning, removed: no cold storage.
- Care & Care: ranked 15th by meaning, removed: capacity 0 pallets, load is 0.25.
- Martha & Me Inc Nfp: ranked 17th by meaning, removed: capacity 0 pallets, load is 0.25.
