<!-- markdownlint-disable MD030 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: A grocer in Chicago has ten crates of spinach, harvested yesterday, that must leave the dock within 6 hours and stay cold.

Captured 2026-10-20 10:53 EDT. The recipient names and addresses are real (IRS data). Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "refrigerated", "product_name": "Spinach"})
find_matches({"needs_cold": true, "hours_remaining": 6, "load_description": "ten crates of spinach", "donor_description": "A grocer in Chicago", "pallets": 1})
```

---

Here's the match brief for the ten crates of spinach:

**1. Who, and why**
Shakespear Rose Community Table Incorporated, 6200 S VERNON AVE APT 1B, CHICAGO, IL 60637. This organization is a good fit because they have vehicle cold storage, can take up to 3 pallets, and can collect within 4 hours.

**2. What they can actually take**
Their profile on file indicates they have vehicle cold storage (not frozen), can handle up to 3 pallets, and have refrigerated transport. They do not have a loading dock.
*(These are generated figures; please confirm with the recipient by phone.)*

**3. The clock**
The food has 6 hours remaining (donor's deadline). Their collection lead time is 4 hours, leaving a 2-hour margin. They are set up to collect themselves, so a driver is not needed.

**4. Whose neighborhood it helps**
The nearest census tract to Shakespear Rose Community Table Incorporated shows 45% of residents below the poverty line, 52% of households without a vehicle, and 38% on food or cash assistance (ACS; recipient location is ZIP-level, so this is the area, not the exact block). They serve "Anyone who walks in", with 413 households per week.

**5. The outreach message**
Hello Shakespear Rose Community Table Incorporated team,

A grocer in Chicago has ten crates of spinach. It is still good but has to move soon. From what we have on file you have the storage for it. The food needs to leave by about 6 hours from now, which leaves you roughly 2 hours of slack to collect. You are set up to collect it yourselves.

Can you take it? If you can, tell us the time you can collect and a phone number for pickup. If not, a quick no helps us move to the next place.

Thank you,
[Coordinator name]

**6. The next two options**
*   Habibi Care (4845 N WASHTENAW AVE, CHICAGO, IL 60625): domestic cold storage, takes up to 1 pallet, collects within 3h (margin: 3 hours). Needs a driver.
*   Word Faith Believers Ministries (8736 S WINCHESTER AVE, CHICAGO, IL 60620): vehicle cold storage, takes up to 3 pallets, collects within 5h (margin: 1 hour). Does not need a driver.

**Rejected but close:**
*   Chicago Food Rescue: needs 8h to collect, food has 6h
*   Anso Child Development: needs 19h to collect, food has 6h
*   Maple Street Produce Alliance: needs 12h to collect, food has 6h
