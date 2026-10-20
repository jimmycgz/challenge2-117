<!-- markdownlint-disable MD001 MD009 MD022 MD029 MD030 MD031 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: A grocer in Chicago has 6 cases of frozen chicken, stored at minus 18, that must be collected within 24 hours.

Captured 14:14 EDT on 2026-10-20. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "refrigerated", "product_name": "Chicken"})
find_matches({"needs_cold": true, "donor_description": "A grocer in Chicago", "load_description": "6 cases of frozen chicken", "hours_remaining": 24, "pallets": 0.25, "needs_frozen": true, "search_text": "frozen poultry chicken raw meat cold storage freezer capacity small batch distribution"})
```

---

Frozen chicken, so it must stay cold and frozen; 6 cases is roughly 0.25 pallets (assuming ~24 cases per pallet). The donor's 24-hour deadline sets the clock (USDA FoodKeeper guidance indicates 336 hours refrigerated/frozen for chicken).

1. Who, and why
New Hope House Northwest (6125 W FOSTER AVE, CHICAGO, IL 60630). Fit: "Congregate lunch and home-delivered meals for adults 60 and over. Reach-in coolers, a freezer, and a chilling cabinet for portioning."

2. What they can actually take
According to their profile on file (generated, confirm by phone), they have commercial cold storage, freezer capacity, can take up to 2 pallets (this load is ~0.25 pallets), and possess refrigerated transport.

3. The clock
The food has 24 hours remaining. New Hope House Northwest has a collection lead time of 15 hours, leaving a margin of 9 hours. No external driver is needed since they have their own refrigerated transport. Note that shelf life figures are consumer guidance, not a cold-chain guarantee.

4. Whose neighborhood it helps
Serves approximately 320 households weekly ("General public, no proof of residence required"). Nearest census tract figures: 7% below the poverty line, 21% without a vehicle, and 12% receiving food or cash assistance.

5. The outreach message
Hello New Hope House Northwest team,

A grocer in Chicago has 6 cases of frozen chicken stored at -18°C. It is in good condition but needs to be moved quickly. From what we have on file, you have the freezer storage to handle it. The food must be collected within 24 hours from now, which leaves roughly 9 hours of slack for pickup. Our records show you are equipped to collect it directly.

Can you take this load? If so, please let us know your estimated collection time and a pickup contact phone number. If not, a quick decline will help us reach out to the next recipient promptly.

Thank you,
[Coordinator name]

6. The next two options
- Option 2: On 3Rd Affordable Food Outreach Service Truck (11057 S FAIRFIELD AVE STE A, CHICAGO, IL 60655) — commercial cold storage, takes up to 1 pallet, collects within 12h (12h margin).
- Option 3: Top Box Foods (222 MERCHANDISE MART PLZ, CHICAGO, IL 60654) — walk-in cold storage, takes up to 17 pallets, collects within 14h (10h margin).

Close semantic matches that were rejected:
- Chicago Food Rescue: ranked 2nd by meaning, removed: no freezer.
- Maple Street Produce Alliance (an invented teaching case): ranked 3rd by meaning, removed: no freezer.
- Lakeshore Mutual Aid Collective (an invented teaching case): ranked 7th by meaning, removed: no cold storage; no freezer.
