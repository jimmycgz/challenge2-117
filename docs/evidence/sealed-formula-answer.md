<!-- markdownlint-disable MD029 MD030 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: 48 cases of sealed infant formula with 8 months to expiry from a distributor in Chicago, 2 pallets, can sit at room temperature.

Captured 13:52 EDT on 2026-10-20. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "pantry", "product_name": "Infant formula"})
lookup_shelf_life({"storage_state": "pantry", "product_name": "Baby food"})
find_matches({"pallets": 2, "donor_description": "A distributor in Chicago", "load_description": "48 cases of sealed infant formula (2 pallets)", "hours_remaining": 5760, "needs_cold": false})
```

---

Sealed infant formula can sit at room temperature, so it does not need cold storage; 48 cases across 2 pallets is 24 cases per pallet; donor specifies 8 months to expiry (roughly 5,760 hours), which sets the clock over FoodKeeper guidance.

### 1. Who, and why
**Beyond Hunger**  
848 Lake St, Oak Park, IL 60301  
Fit: *"Central warehouse and redistribution point for 21 member agencies. Racked warehouse with temperature-controlled bays and a monitored freezer. Forklifts, pallet jacks, and a crew who can turn a truck in under an hour. Anything at scale."*

### 2. What they can actually take
- **Capacity:** Takes up to 22 pallets on file (this load is 2 pallets).
- **Storage & Facilities:** Walk-in cold storage, frozen storage, and a loading dock on file. (Operational details are generated; confirm by phone before dispatch).

### 3. The clock
- **Hours food has:** 5,760 hours (8 months donor expiry).
- **Lead time:** 45 hours collection lead time on file.
- **Margin:** 5,715 hours of margin.
- **Driver needed:** No driver needed; recipient has transport on file.

### 4. Whose neighborhood it helps
- **Populations served:** Serves approximately 3,205 households per week; focuses on residents of the surrounding school district.
- **Tract demographics:** Nearest census tract has 4% of residents below the poverty line, 23% of households without a vehicle, and 1% receiving food or cash assistance (ACS ZIP-level data).

### 5. The outreach message
Hello Beyond Hunger team,

A distributor in Chicago has 48 cases of sealed infant formula (2 pallets) with 8 months until expiration. It can sit at room temperature. From what we have on file, you have the capacity and equipment to receive this scale. 

Can you take this load? If so, please let us know what pickup window works for your team and provide a primary phone number for pickup coordination. If not, a quick pass helps us redirect to the next agency immediately.

Thank you,  
[Coordinator name]

### 6. The next two options
- **Option 2:** Feeding America — 161 N Clark St Ste 700, Chicago, IL 60601 (Takes up to 24 pallets, collects within 28h).
- **Option 3:** Faces Of Change — 310 Busse Hwy, Park Ridge, IL 60068 (Takes up to 3 pallets, collects within 22h).

**Close matches removed by filters:**
- Ranked 1st by meaning, removed: capacity 1 pallet, load is 2 (Second Faith Temple Community Outreach)
- Ranked 2nd by meaning, removed: capacity 1 pallet, load is 2 (Jm Foundation)
- Ranked 5th by meaning, removed: capacity 1 pallet, load is 2 (Khaan Foundation)
