<!-- markdownlint-disable MD001 MD009 MD022 MD029 MD030 MD031 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: 48 cases of sealed infant formula with 8 months to expiry from a distributor in Chicago, 2 pallets, can sit at room temperature.

Captured 14:40 EDT on 2026-10-20. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "pantry", "product_name": "Infant formula"})
lookup_shelf_life({"storage_state": "pantry", "product_name": "Baby food"})
find_matches({"needs_cold": false, "load_description": "48 cases of sealed infant formula (2 pallets)", "pallets": 2, "hours_remaining": 5840, "needs_frozen": false, "search_text": "pantry shelf-stable infant formula baby formula infant nutrition families with infants toddlers children 2 pallets ambient storage", "donor_description": "A distributor in Chicago"})
```

---

Infant formula is shelf-stable and sealed, so it does not need cold storage; 48 cases are given as 2 pallets (24 cases per pallet), with an 8-month donor expiry (~5,840 hours) setting the clock since FoodKeeper has no specific entry for infant formula and the posting specifies sealed product with its own expiry.

### 1. Who, and why
**Feeding America**  
161 N CLARK ST STE 700, CHICAGO, IL 60601  
Profile fit: *"County-wide food bank operating a 40,000 square foot warehouse. Racked warehouse with temperature-controlled bays and a monitored freezer."*

### 2. What they can actually take
The profile on file indicates capacity for up to 24 pallets (load is 2 pallets), walk-in cold storage, freezer capacity, and a loading dock. Since operational details are generated, please confirm availability by phone before dispatching.

### 3. The clock
* Food shelf life / donor deadline remaining: 5,840 hours (8 months)
* Recipient lead time: 28 hours
* Margin: 5,812 hours of slack
* Driver needed: No; profile indicates they have their own transport capability.

### 4. Whose neighborhood it helps
* Populations served: Families with children (3,563 households served weekly on file).
* Nearest census tract figures: 13% poverty rate, 54% no-vehicle rate, 0% assistance rate (ZIP-level approximate area).

### 5. The outreach message
```text
Hello Feeding America team,

A distributor in Chicago has 48 cases of sealed infant formula (2 pallets, room temperature storage). The product has 8 months remaining until expiry. From what we have on file, you have the warehouse capacity to receive this load. 

Can you take it? If you can, please let us know when you can collect and provide a phone number for pickup coordination. If not, a quick pass helps us reroute promptly.

Thank you,
[Coordinator name]
```

### 6. The next two options
* **Greater Chicago Food Depository** (Option 2) – 4100 W ANN LURIE PL, CHICAGO, IL 60632; walk-in cold storage, takes up to 23 pallets, collects within 36 hours (5,804 hours margin).
* **Faces Of Change** (Option 3) – 310 BUSSE HWY, PARK RIDGE, IL 60068; commercial cold storage, takes up to 3 pallets, collects within 22 hours (5,818 hours margin).

**Rejected close semantic matches:**
* Second Faith Temple Community Outreach – ranked 1st by meaning, removed: capacity 1 pallet, load is 2
* Jm Foundation – ranked 2nd by meaning, removed: capacity 1 pallet, load is 2
* Khaan Foundation – ranked 3rd by meaning, removed: capacity 1 pallet, load is 2
