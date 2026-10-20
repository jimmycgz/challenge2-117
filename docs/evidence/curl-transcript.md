# Live service transcript

Captured 2026-10-20 11:29 EDT from the deployed Cloud Run service. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

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
lookup_shelf_life({"product_name": "Spinach", "storage_state": "refrigerated"})
find_matches({"hours_remaining": 6, "pallets": 0.5, "needs_cold": true, "donor_description": "A grocer in Chicago", "load_description": "ten crates of spinach"})
```

The structured brief is in [spinach-brief.json](spinach-brief.json) and the written answer in [spinach-answer.md](spinach-answer.md).

## Question: A farm south of Chicago has 5 tons of potatoes still in the field. They can load pallets if someone collects within 3 days.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "pantry", "product_name": "Potatoes"})
find_matches({"needs_cold": false, "load_description": "5 tons of potatoes", "hours_remaining": 72, "donor_description": "A farm south of Chicago", "pallets": 5})
```

The structured brief is in [farm-potatoes-brief.json](farm-potatoes-brief.json) and the written answer in [farm-potatoes-answer.md](farm-potatoes-answer.md).

## Question: A bakery has 40 trays of cream-filled pastries that must stay refrigerated and leave their dock within 1 hour.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "cream-filled pastries", "storage_state": "refrigerated"})
find_matches({"donor_description": "A bakery", "load_description": "40 trays of cream-filled pastries", "needs_cold": true, "pallets": 0.25, "hours_remaining": 1})
```

The structured brief is in [no-match-bakery-brief.json](no-match-bakery-brief.json) and the written answer in [no-match-bakery-answer.md](no-match-bakery-answer.md).

## Question: How many recipients in the corpus have walk-in cold storage, and what share of all recipients is that?

Tool calls, in order:

```text
execute_sql({"query": "SELECT COUNT(*) FROM `<lab-project-id>.a4i_food.recipients` WHERE cold_storage = 'walk-in'", "projectId": "<lab-project-id>"})
execute_sql({"query": "SELECT COUNT(*) FROM `<lab-project-id>.a4i_food.recipients`", "projectId": "<lab-project-id>"})
```

The written answer is in [mcp-walk-in-answer.md](mcp-walk-in-answer.md).

## Question: 48 cases of sealed infant formula with 8 months to expiry from a distributor in Chicago, 2 pallets, can sit at room temperature.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "infant formula", "storage_state": "pantry"})
find_matches({"donor_description": "a distributor in Chicago", "load_description": "48 cases of infant formula", "needs_cold": false, "hours_remaining": 5760, "pallets": 2})
```

The structured brief is in [sealed-formula-brief.json](sealed-formula-brief.json) and the written answer in [sealed-formula-answer.md](sealed-formula-answer.md).
