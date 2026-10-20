<!-- markdownlint-disable MD030 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: 48 cases of sealed infant formula with 8 months to expiry from a distributor in Chicago, 2 pallets, can sit at room temperature.

Captured 2026-10-20 11:00 EDT. The recipient names and addresses are real (IRS data). Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "pantry", "product_name": "infant formula"})
find_matches({"hours_remaining": 5760, "load_description": "48 cases of sealed infant formula", "needs_cold": false, "donor_description": "a distributor in Chicago", "pallets": 2})
```

---

Feeding America is the best match.

1.  **Who, and why**
    Feeding America, 161 N CLARK ST STE 700, CHICAGO, IL 60601, because they have walk-in cold storage (which indicates suitable general storage), take up to 24 pallets, and collect within 28 hours.

2.  **What they can actually take**
    The profile on file for Feeding America indicates they have walk-in cold storage (please confirm by phone), have frozen storage (please confirm by phone), can take up to 24 pallets (please confirm by phone), have a loading dock (please confirm by phone), and have refrigerated transport (please confirm by phone). They service on Tuesday and Thursday.

3.  **The clock**
    The infant formula has 5760 hours remaining. Feeding America's collection lead time is 28 hours, leaving a margin of 5732 hours. A driver is not needed as they are set up for self-collection.

4.  **Whose neighborhood it helps**
    Feeding America serves families with children, reaching 3563 households per week. The nearest census tract has 13% of residents below the poverty line, 54% of households without a vehicle, and 0% on food or cash assistance (ACS; recipient location is ZIP-level, so this is the area, not the exact block).

5.  **The outreach message**
    Hello Feeding America team,

    a distributor in Chicago has 48 cases of sealed infant formula. It is still good and shelf-stable, but has to move soon. From what we have on file you have the storage for it. The food needs to leave by about 5760 hours from now, which leaves you roughly 5732 hours of slack to collect. You are set up to collect it yourselves.

    Can you take it? If you can, tell us the time you can collect and a phone number for pickup. If not, a quick no helps us move to the next place.

    Thank you,
    [Coordinator name]

6.  **The next two options**
    *   Faces Of Change, 310 BUSSE HWY, PARK RIDGE, IL 60068: commercial cold storage, takes up to 3 pallets, collects within 22h. (5738 hours margin)
    *   Chicago Food Rescue, 2426 W DAKIN ST 2, CHICAGO, IL 60618: vehicle cold storage, takes up to 2 pallets, collects within 8h. (5752 hours margin)
