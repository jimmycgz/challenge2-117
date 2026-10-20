<!-- markdownlint-disable MD030 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: A farm south of Chicago has 5 tons of potatoes still in the field. They can load pallets if someone collects within 3 days.

Captured 2026-10-20 10:53 EDT. The recipient names and addresses are real (IRS data). Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "Potatoes", "storage_state": "pantry"})
find_matches({"donor_description": "A farm south of Chicago", "load_description": "5 tons of potatoes", "hours_remaining": 72, "needs_cold": false, "pallets": 5})
```

---

Top match: Feeding America for 5 tons of potatoes.

1.  **Who, and why**: Feeding America at 161 N CLARK ST STE 700, CHICAGO, IL 60601. Their profile on file states they have a 40,000 square foot warehouse with racked storage and temperature-controlled bays, dock-height receiving, and can send a reefer for cold chain items. They can take up to 24 pallets and collect within 28 hours.
2.  **What they can actually take**: Their profile indicates they have walk-in cold storage, frozen storage, a loading dock, and refrigerated transport. They can accept up to 24 pallets; this load is 5 pallets (based on 1 ton = 1 pallet). They typically serve on Tuesday and Thursday.
3.  **The clock**: The potatoes must be collected within 72 hours. Feeding America's stated collection lead time is 28 hours, leaving a margin of 44 hours. They have their own refrigerated transport, so a driver is not needed.
4.  **Whose neighborhood it helps**: They serve 3563 households weekly, primarily Families with children. The nearest census tract has 13% of residents below the poverty line, 54% of households without a vehicle, and 0% on food or cash assistance (ACS; recipient location is ZIP-level, so this is the area, not the exact block).
5.  **The outreach message**:
    Hello Feeding America team,

    A farm south of Chicago has 5 tons of potatoes. It is still good but has to move soon. From what we have on file you have the capacity and storage for it. The food needs to leave by about 72 hours from now, which leaves you roughly 44 hours of slack to collect. You are set up to collect it yourselves.

    Can you take it? If you can, tell us the time you can collect and a phone number for pickup. If not, a quick no helps us move to the next place.

    Thank you,
    [Coordinator name]

6.  **The next two options**:
    *   Greater Chicago Food Depository (4100 W ANN LURIE PL, CHICAGO, IL 60632): has walk-in cold storage, takes up to 23 pallets, collects within 36 hours (36 hours margin).
    *   Beyond Hunger (848 LAKE ST, OAK PARK, IL 60301): has walk-in cold storage, takes up to 22 pallets, collects within 45 hours (27 hours margin).

    Rejected but close:
    *   Chicago Health Initiative: capacity 0 pallets, load is 5
    *   Lolas Community Kitchen: capacity 0 pallets, load is 5
    *   Love Lifted Me Community Shelter: capacity 0 pallets, load is 5
