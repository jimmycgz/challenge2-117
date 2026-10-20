<!-- markdownlint-disable MD001 MD009 MD022 MD029 MD030 MD031 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: A farm south of Chicago has 5 tons of potatoes still in the field. They can load pallets if someone collects within 3 days.

Captured 14:40 EDT on 2026-10-20. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "pantry", "product_name": "Potatoes"})
find_matches({"donor_description": "A farm south of Chicago", "load_description": "5 tons of potatoes", "needs_frozen": false, "search_text": "large scale dry storage pantry hardy produce root vegetables bulk potatoes 5 pallets", "hours_remaining": 72, "pallets": 5, "needs_cold": false})
```

---

Potatoes do not require cold storage; 5 tons is about 5 pallets at roughly a ton per pallet, and the donor's 3-day deadline (72 hours) sets the clock against the 1,440-hour pantry shelf life (FoodKeeper shelf life for "Potatoes" is consumer guidance, not a cold-chain guarantee).

1. **Who, and why**  
   Maple Street Produce Alliance (Chicago, IL), an invented teaching case in the challenge data. Profile excerpt: *"Fresh produce hub with walk-in refrigeration and our own reefer truck. Roughly 600 households weekly, and perishables move through us in under two days."*

2. **What they can actually take**  
   Their profile on file indicates a capacity of up to 10 pallets (this load is 5 pallets), a loading dock, and walk-in cold storage (suggest confirming by phone before the truck moves).

3. **The clock**  
   The food has 72 hours remaining (donor deadline). Their collection lead time on file is 12 hours, leaving a comfortable margin of 60 hours. They have refrigerated transport on file, so no external driver is needed.

4. **Whose neighborhood it helps**  
   Serves the general public (~600 households weekly). Nearest census tract figures: 9% poverty rate, 11% no-vehicle rate, and 12% assistance rate.

5. **The outreach message**  
   Hello Maple Street Produce Alliance team,

   A farm south of Chicago has 5 tons of potatoes. They can load pallets if collected within 3 days. From what we have on file, you have the storage and capacity for it. The pickup deadline is 72 hours from now, which leaves roughly 60 hours of slack to collect.

   Can you take it? If you can, tell us the time you can collect and a phone number for pickup. If not, a quick no helps us move to the next place.

   Thank you,  
   [Coordinator name]

6. **The next two options**  
   - Option 2: Anso Child Development (9101 S WESTERN AVE STE 9, CHICAGO, IL 60643) — takes up to 7 pallets, collects within 19 hours (53 hours margin).  
   - Option 3: Cedar Street Produce Alliance (Chicago, IL), an invented teaching case — takes up to 10 pallets, collects within 12 hours (60 hours margin).  

   *Close semantic matches that were rejected:*  
   - Boys To Men Nfp Inc: ranked 3rd by meaning, removed: needs 77h to collect, food has 72h  
   - Burrito Brigade Chicago: ranked 9th by meaning, removed: capacity 3 pallets, load is 5  
   - Loop Da Loop Nfp: ranked 10th by meaning, removed: needs 103h to collect, food has 72h
