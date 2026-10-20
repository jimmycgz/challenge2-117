# Live service transcript

Captured 2026-10-20 11:00 EDT from the deployed Cloud Run service. The recipient names and addresses are real (IRS data). Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

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
find_matches({"load_description": "ten crates of spinach", "needs_cold": true, "donor_description": "A grocer in Chicago", "hours_remaining": 6, "pallets": 0.25})
```

The structured brief is in [spinach-brief.json](spinach-brief.json) and the written answer in [spinach-answer.md](spinach-answer.md).

## Question: A farm south of Chicago has 5 tons of potatoes still in the field. They can load pallets if someone collects within 3 days.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "Potatoes", "storage_state": "pantry"})
find_matches({"donor_description": "A farm south of Chicago", "hours_remaining": 72, "pallets": 5, "load_description": "five tons of potatoes", "needs_cold": false})
```

The structured brief is in [farm-potatoes-brief.json](farm-potatoes-brief.json) and the written answer in [farm-potatoes-answer.md](farm-potatoes-answer.md).

## Question: A bakery has 40 trays of cream-filled pastries that must stay refrigerated and leave their dock within 1 hour.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "refrigerated", "product_name": "cream-filled pastries"})
find_matches({"hours_remaining": 1, "needs_cold": true, "load_description": "40 trays of cream-filled pastries", "pallets": 0.5, "donor_description": "A bakery"})
```

The structured brief is in [no-match-bakery-brief.json](no-match-bakery-brief.json) and the written answer in [no-match-bakery-answer.md](no-match-bakery-answer.md).

## Question: How many recipients in the corpus have walk-in cold storage, and what share of all recipients is that?

Tool calls, in order:

```text
execute_sql({"query": "SELECT COUNT(*) as total_recipients, SUM(CASE WHEN cold_storage = 'walk-in' THEN 1 ELSE 0 END) as walk_in_cold_storage_recipients FROM `<lab-project-id>.a4i_food.recipients`", "projectId": "<lab-project-id>"})
```

The written answer is in [mcp-walk-in-answer.md](mcp-walk-in-answer.md).

## Question: 48 cases of sealed infant formula with 8 months to expiry from a distributor in Chicago, 2 pallets, can sit at room temperature.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "pantry", "product_name": "infant formula"})
find_matches({"hours_remaining": 5760, "load_description": "48 cases of sealed infant formula", "needs_cold": false, "donor_description": "a distributor in Chicago", "pallets": 2})
```

The structured brief is in [sealed-formula-brief.json](sealed-formula-brief.json) and the written answer in [sealed-formula-answer.md](sealed-formula-answer.md).
