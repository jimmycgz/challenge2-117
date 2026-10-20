# Live service transcript

Captured 2026-10-20 10:42 EDT from the deployed Cloud Run service. The recipient names and addresses are real (IRS data). Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

## Health, with no credentials

```text
GET /health -> HTTP 200 {"status":"ok"}
```

## Root redirects to ADK's chat page

```text
GET / -> HTTP 307, location: /dev-ui/
```

## Question: A grocer in Chicago has ten crates of spinach, harvested yesterday, that must leave the dock within 6 hours and stay cold.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "refrigerated", "product_name": "Spinach"})
find_matches({"donor_description": "A grocer in Chicago", "hours_remaining": 6, "needs_cold": true, "load_description": "ten crates of spinach", "pallets": 0.5})
```

The structured brief is in [spinach-brief.json](spinach-brief.json) and the written answer in [spinach-answer.md](spinach-answer.md).

## Question: 48 cases of sealed infant formula with 8 months to expiry from a distributor in Chicago, 2 pallets, can sit at room temperature.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "pantry", "product_name": "Infant formula"})
find_matches({"hours_remaining": 5760, "needs_cold": false, "load_description": "48 cases of sealed infant formula", "pallets": 2, "donor_description": "A distributor in Chicago"})
```

The structured brief is in [sealed-formula-brief.json](sealed-formula-brief.json) and the written answer in [sealed-formula-answer.md](sealed-formula-answer.md).
