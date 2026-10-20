<!-- markdownlint-disable MD029 MD030 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: A bakery has 40 trays of cream-filled pastries that must stay refrigerated and leave their dock within 1 hour.

Captured 2026-10-20 11:29 EDT. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Lakeshore Mutual Aid Collective, below, is one of them. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "cream-filled pastries", "storage_state": "refrigerated"})
find_matches({"donor_description": "A bakery", "load_description": "40 trays of cream-filled pastries", "needs_cold": true, "pallets": 0.25, "hours_remaining": 1})
```

---

No viable recipient found for the 40 trays of cream-filled pastries.

The closest rejections were:
* Open Door Outreach Center, ranked 1st by meaning, removed: needs 8h to collect, food has 1h
* Willis House Of Refuge Nfp, ranked 2nd by meaning, removed: needs 8h to collect, food has 1h
* Lakeshore Mutual Aid Collective, ranked 19th by meaning, removed: no cold storage; needs 12h to collect, food has 1h
