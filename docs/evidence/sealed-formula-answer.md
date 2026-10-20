<!-- markdownlint-disable MD030 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: 48 cases of sealed infant formula with 8 months to expiry from a distributor in Chicago, 2 pallets, can sit at room temperature.

Captured 2026-10-20 10:53 EDT. The recipient names and addresses are real (IRS data). Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "infant formula", "storage_state": "pantry"})
find_matches({"pallets": 2, "needs_cold": false, "hours_remaining": 5760, "load_description": "48 cases of infant formula", "donor_description": "a distributor in Chicago"})
```

---

Here's the Match Brief for the infant formula:

**Summary:** Feeding America is the top match for the 2 pallets of infant formula, with plenty of time to collect.

1.  **Who, and why**
    Feeding America, 161 N CLARK ST STE 700, CHICAGO, IL 60601. They were matched because they have walk-in cold storage (though not needed for this item), can take up to 24 pallets, and collect within 28 hours.

2.  **What they can actually take**
    Their profile on file states they have a walk-in cold storage and a monitored freezer. They have a loading dock and refrigerated transport. They can take up to 24 pallets. This load is 2 pallets. They are available for service on Tuesdays and Thursdays. (Please confirm these details by phone before the truck moves.)

3.  **The clock**
    The infant formula has 5760 hours remaining (the donor's 8-month deadline, as it is sealed). Feeding America's stated collection lead time is 28 hours, leaving a margin of 5732 hours. They have refrigerated transport and can collect themselves, so a driver is not needed from our side.

4.  **Whose neighborhood it helps**
    This organization serves Families with children. The nearest census tract to their location has 13% of residents below the poverty line, 54% of households without a vehicle, and 0% on food or cash assistance (ACS data; recipient location is ZIP-level, so this is the area, not the exact block). They serve approximately 3563 households per week.

5.  **The outreach message**

    Hello Feeding America team,

    a distributor in Chicago has 48 cases of infant formula. It is still good but has to move soon. From what we have on file you have the storage for it. The food needs to leave by about 5760 hours from now, which leaves you roughly 5732 hours of slack to collect. You are set up to collect it yourselves.

    Can you take it? If you can, tell us the time you can collect and a phone number for pickup. If not, a quick no helps us move to the next place.

    Thank you,
    [Coordinator name]

6.  **The next two options**
    *   Faces Of Change, 310 BUSSE HWY, PARK RIDGE, IL 60068: commercial cold storage, takes up to 3 pallets, collects within 22h.
    *   Top Box Foods, 222 MERCHANDISE MART PLZ, CHICAGO, IL 60654: walk-in cold storage, takes up to 17 pallets, collects within 14h.

    Rejected but close:
    *   Second Faith Temple Community Outreach: capacity 1 pallet, load is 2
    *   Khaan Foundation: capacity 1 pallet, load is 2
    *   Mano A Mano Unidos Ltd: capacity 1 pallet, load is 2
