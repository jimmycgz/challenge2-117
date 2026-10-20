<!-- markdownlint-disable MD029 MD030 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: A farm south of Chicago has 5 tons of potatoes still in the field. They can load pallets if someone collects within 3 days.

Captured 13:52 EDT on 2026-10-20. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "pantry", "product_name": "Potatoes"})
find_matches({"donor_description": "A farm south of Chicago", "load_description": "5 tons of potatoes", "needs_cold": false, "pallets": 5, "hours_remaining": 72})
```

---

5 tons of potatoes is about 5 pallets at roughly a ton a pallet; potatoes are hardy whole root vegetables, so they do not require cold storage, and the donor's 72-hour deadline sets the clock (USDA FoodKeeper pantry shelf life is 1,440 hours, which is consumer guidance, not a cold-chain guarantee).

1. Who, and why - Maple Street Produce Alliance, Chicago, IL (note: an invented teaching case in the challenge data). "Fresh produce hub with walk-in refrigeration and our own reefer truck."
2. What they can actually take - Profile on file indicates capacity for up to 10 pallets (load is 5 pallets), walk-in storage, and a loading dock (confirm operational details by phone before dispatch).
3. The clock - Food has 72 hours remaining; recipient collection lead time is 12 hours, giving a comfortable margin of 60 hours. They have refrigerated transport on file, so no separate driver is needed.
4. Whose neighborhood it helps - Serves roughly 600 households weekly (general public). Nearest census tract figures: 9% poverty rate, 11% no-vehicle rate, 12% on assistance.
5. The outreach message -
Hello Maple Street Produce Alliance team,

A farm south of Chicago has 5 tons of potatoes on 5 pallets. The farm can load pallets if collected within 3 days (72 hours). From what we have on file, you have the capacity to handle this load, which leaves roughly 60 hours of slack to collect.

Can you take this load? If yes, please let us know when you can collect and a phone number for pickup. If not, a quick no helps us move to the next recipient.

Thank you,
[Coordinator name]

6. The next two options -
- Option 2: Anso Child Development, 9101 S WESTERN AVE STE 9, CHICAGO, IL 60643 (takes up to 7 pallets, collects within 19 hours, 53 hours margin).
- Option 3: Dion S Chicago Dream Inc Nfp, 6235 S HOMAN AVE, CHICAGO, IL 60629 (takes up to 11 pallets, collects within 9 hours, 63 hours margin).

Rejected close matches:
- Boys To Men Nfp Inc: ranked 1st by meaning, removed: needs 77h to collect, food has 72h.
- Loop Da Loop Nfp: ranked 11th by meaning, removed: needs 103h to collect, food has 72h.
- Burrito Brigade Chicago: ranked 12th by meaning, removed: capacity 3 pallets, load is 5.
