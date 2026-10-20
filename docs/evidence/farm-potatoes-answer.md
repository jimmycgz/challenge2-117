<!-- markdownlint-disable MD001 MD009 MD022 MD029 MD030 MD031 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: A farm south of Chicago has 5 tons of potatoes still in the field. They can load pallets if someone collects within 3 days.

Captured 14:14 EDT on 2026-10-20. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "Potatoes", "storage_state": "pantry"})
find_matches({"search_text": "large capacity warehouse pantry food bank able to take 5 pallets of fresh potatoes shelf stable hardy produce bulk root vegetables", "needs_frozen": false, "needs_cold": false, "top_k": 80, "donor_description": "A farm south of Chicago", "pallets": 5, "hours_remaining": 72, "load_description": "5 tons of potatoes"})
```

---

Potatoes are whole root vegetables, so they do not need cold storage; 5 tons is about 5 pallets at roughly a ton per pallet, and the donor's 3-day window (72 hours) sets the clock over the FoodKeeper pantry shelf life (1,440 hours).

1. **Who, and why**
   - **Organization:** Greater Chicago Food Depository (4100 W Ann Lurie Pl, Chicago, IL 60632)
   - **Why:** "Regional hub. We are the first call when a distributor has a full truckload to move. Refrigerated and frozen storage on site. Dock receiving; we can take full pallets." (Note: Operational details are generated from the profile on file; confirm by phone before dispatch).

2. **What they can actually take**
   - **Capacity:** Can take up to 23 pallets (profile on file); load is 5 pallets.
   - **Storage & Infrastructure:** Walk-in cold storage, frozen storage, loading dock, and refrigerated transport on file. Service days: Monday, Wednesday, Friday.

3. **The clock**
   - **Hours food has:** 72 hours (donor's 3-day deadline set the clock).
   - **Collection lead time:** 36 hours.
   - **Margin:** 36 hours.
   - **Driver needed:** No, they have transport on file.

4. **Whose neighborhood it helps**
   - **Service scale & population:** Serves ~3,486 households per week; general public, no proof of residence required.
   - **Tract figures:** Nearest census tract has 15% of residents below the poverty line, 12% of households without a vehicle, and 16% on food or cash assistance (ACS; ZIP-level approximation).

5. **The outreach message**
   Hello Greater Chicago Food Depository team,

   A farm south of Chicago has 5 tons of potatoes. It is still good but has to move soon. From what we have on file you have the storage and dock capacity for it. The food needs to leave by about 72 hours from now, which leaves you roughly 36 hours of slack to collect. You are set up to collect it yourselves.

   Can you take it? If you can, tell us the time you can collect and a phone number for pickup. If not, a quick no helps us move to the next place.

   Thank you,  
   [Coordinator name]

6. **The next two options**
   - **Option 2:** Feeding America (161 N Clark St Ste 700, Chicago, IL 60601) – Walk-in cold storage, takes up to 24 pallets, collects within 28 hours (44h margin).
   - **Option 3:** Top Box Foods (222 Merchandise Mart Plz, Chicago, IL 60654) – Walk-in cold storage, takes up to 17 pallets, collects within 14 hours (58h margin).

   *Close semantic matches removed by filters:*
   - Ridgeway Avenue Food Ministry (an invented teaching case): ranked 3rd by meaning, removed: capacity 3 pallets, load is 5.
   - Lolas Community Kitchen: ranked 5th by meaning, removed: capacity 0 pallets, load is 5.
   - Boys To Men Nfp Inc: ranked 9th by meaning, removed: needs 77h to collect, food has 72h.
