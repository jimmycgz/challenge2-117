<!-- markdownlint-disable MD029 MD030 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: 48 cases of sealed infant formula with 8 months to expiry from a distributor in Chicago, 2 pallets, can sit at room temperature.

Captured 2026-10-20 11:29 EDT. The recipient names and addresses are real (IRS data). Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "infant formula", "storage_state": "pantry"})
find_matches({"donor_description": "a distributor in Chicago", "load_description": "48 cases of infant formula", "needs_cold": false, "hours_remaining": 5760, "pallets": 2})
```

---

2 pallets of sealed infant formula from a distributor in Chicago.

1.  **Who, and why**
    Feeding America, 161 N CLARK ST STE 700, CHICAGO, IL 60601. Their profile says: "County-wide food bank operating a 40,000 square foot warehouse. Racked warehouse with temperature-controlled bays and a monitored freezer. Dock-height receiving, and we can send a reefer for anything that needs the cold chain." They have walk-in cold storage, can take up to 24 pallets, and collect within 28 hours.

2.  **What they can actually take**
    Their profile indicates they have walk-in cold storage and can take up to 24 pallets. They have a loading dock and refrigerated transport. This is sufficient for your 2-pallet load.

3.  **The clock**
    The food has 5760 hours remaining. Feeding America's collection lead time is 28 hours, leaving a margin of 5732 hours. They are set up to collect it themselves, so no driver is needed.

4.  **Whose neighborhood it helps**
    They serve 3563 households per week, primarily Families with children. The nearest census tract shows 13% of residents below the poverty line, 54% of households without a vehicle, and 0% on food or cash assistance.

5.  **The outreach message**
    Hello Feeding America team,

    a distributor in Chicago has 48 cases of infant formula. It is still good but has to move soon. From what we have on file you have the storage for it. The food needs to leave by about 5760 hours from now, which leaves you roughly 5732 hours of slack to collect. You are set up to collect it yourselves.

    Can you take it? If you can, tell us the time you can collect and a phone number for pickup. If not, a quick no helps us move to the next place.

    Thank you,
    [Coordinator name]

6.  **The next two options**
    *   Faces Of Change, 310 BUSSE HWY, PARK RIDGE, IL 60068 (commercial cold storage, takes up to 3 pallets, collects within 22h)
    *   Top Box Foods, 222 MERCHANDISE MART PLZ, CHICAGO, IL 60654 (walk-in cold storage, takes up to 17 pallets, collects within 14h)

    **Rejected but close matches:**
    *   Second Faith Temple Community Outreach, ranked 1st by meaning, removed: capacity 1 pallet, load is 2
    *   Mano A Mano Unidos Ltd, ranked 4th by meaning, removed: capacity 1 pallet, load is 2
    *   Khaan Foundation, ranked 5th by meaning, removed: capacity 1 pallet, load is 2
