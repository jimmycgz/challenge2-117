<!-- markdownlint-disable MD029 MD030 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: A farm south of Chicago has 5 tons of potatoes still in the field. They can load pallets if someone collects within 3 days.

Captured 2026-10-20 11:29 EDT. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "pantry", "product_name": "Potatoes"})
find_matches({"needs_cold": false, "load_description": "5 tons of potatoes", "hours_remaining": 72, "donor_description": "A farm south of Chicago", "pallets": 5})
```

---

Anso Child Development is the top match for 5 tons of potatoes.

1.  **Who, and why** - Anso Child Development, 9101 S WESTERN AVE STE 9, CHICAGO, IL 60643. Their profile shows they have walk-in cold storage, can take up to 7 pallets, and collect within 19 hours.
2.  **What they can actually take** - Anso Child Development has walk-in cold storage and can take up to 7 pallets, which covers this load of 5 pallets. They also have a loading dock and refrigerated transport, according to their profile.
3.  **The clock** - The food has 72 hours remaining. Anso Child Development's stated collection lead time is 19 hours, which leaves a comfortable margin of 53 hours. They have refrigerated transport, so a driver is not needed from us.
4.  **Whose neighborhood it helps** - This organization serves Families with children, and reaches 668 households per week. The nearest census tract indicates 6% of residents are below the poverty line, 7% of households are without a vehicle, and 6% are on food or cash assistance.
5.  **The outreach message** -
    Hello Anso Child Development team,

    A farm south of Chicago has 5 tons of potatoes. It is still good but has to move soon. From what we have on file you have the storage for it. The food needs to leave by about 72 hours from now, which leaves you roughly 53 hours of slack to collect. You are set up to collect it yourselves.

    Can you take it? If you can, tell us the time you can collect and a phone number for pickup. If not, a quick no helps us move to the next place.

    Thank you,
    [Coordinator name]

6.  **The next two options** -
    *   **Feeding America**, 161 N CLARK ST STE 700, CHICAGO, IL 60601 (walk-in cold storage, takes up to 24 pallets, collects within 28h)
    *   **Greater Chicago Food Depository**, 4100 W ANN LURIE PL, CHICAGO, IL 60632 (walk-in cold storage, takes up to 23 pallets, collects within 36h)

    Rejected close matches:
    *   Chicago Food Rescue, ranked 2nd by meaning, removed: capacity 2 pallets, load is 5
    *   Burrito Brigade Chicago, ranked 4th by meaning, removed: capacity 3 pallets, load is 5
    *   Women Of Esther Ministries, ranked 5th by meaning, removed: capacity 0 pallets, load is 5
