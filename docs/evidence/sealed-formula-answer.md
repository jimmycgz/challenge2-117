<!-- markdownlint-disable MD001 MD009 MD022 MD029 MD030 MD031 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: 48 cases of sealed infant formula with 8 months to expiry from a distributor in Chicago, 2 pallets, can sit at room temperature.

Captured 14:14 EDT on 2026-10-20. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "infant formula", "storage_state": "pantry"})
lookup_shelf_life({"storage_state": "pantry", "product_name": "baby formula"})
lookup_shelf_life({"product_name": "formula", "storage_state": "pantry"})
find_matches({"search_text": "infant formula, baby formula, sealed baby food, pantry storage, families with infants, maternal child nutrition", "pallets": 2, "needs_cold": false, "donor_description": "A distributor in Chicago", "hours_remaining": 5760, "needs_frozen": false, "load_description": "48 cases (2 pallets) of sealed infant formula"})
```

---

Sealed infant formula is shelf-stable and can sit at room temperature, so it does not need cold storage; 48 cases is given directly by the donor as 2 pallets (24 cases per pallet), with 8 months (approximately 5,760 hours) to expiry setting the clock over FoodKeeper's 1-hour open-container figure.

1. Who, and why
Maple Street Produce Alliance, an invented teaching case in the challenge data, Chicago, IL. The match was selected because the profile on file indicates walk-in cold storage, an ability to take up to 10 pallets, and collection within 12 hours. (Relevant profile excerpt: "Roughly 600 households weekly, and perishables move through us in under two days.") Note: As this is an invented teaching case, operational details should be verified before arranging transit.

2. What they can actually take
The profile on file lists a capacity of up to 10 pallets against this 2-pallet load, with walk-in storage and a loading dock. Note that operational capacity details are generated, so confirm by phone before dispatching.

3. The clock
The food has 5,760 hours remaining based on the donor's 8-month expiry. Maple Street Produce Alliance has a collection lead time of 12 hours on file, leaving a margin of roughly 5,748 hours. They have transport on file, so no external driver is needed.

4. Whose neighborhood it helps
The organization serves the general public (roughly 600 households weekly on file). Nearest census tract figures: 9% of residents below the poverty line, 11% of households without a vehicle, and 12% receiving food or cash assistance.

5. The outreach message
Hello Maple Street Produce Alliance team,

A distributor in Chicago has 48 cases (2 pallets) of sealed infant formula with 8 months remaining until expiry. It does not require refrigeration and can sit at room temperature. From what we have on file, you have the capacity to take this load. Can you take it? If you can, please let us know when you can collect and a good contact phone number for the pickup. If not, a quick no helps us move to the next recipient.

Thank you,  
[Coordinator name]

6. The next two options
- Option 2: Feeding America, 161 N Clark St Ste 700, Chicago, IL 60601 (margin: 5,732 hours; takes up to 24 pallets, collects within 28 hours; profile details generated).
- Option 3: Faces Of Change, 310 Busse Hwy, Park Ridge, IL 60068 (margin: 5,738 hours; takes up to 3 pallets, collects within 22 hours; profile details generated).

Rejected close matches:
- Jm Foundation: ranked 1st by meaning, removed: capacity 1 pallet, load is 2.
- Mano A Mano Unidos Ltd: ranked 2nd by meaning, removed: capacity 1 pallet, load is 2.
- Second Faith Temple Community Outreach: ranked 4th by meaning, removed: capacity 1 pallet, load is 2.
