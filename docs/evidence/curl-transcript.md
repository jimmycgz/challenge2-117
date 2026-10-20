# Live service transcript

Captured 13:52 EDT on 2026-10-20 from the deployed Cloud Run service. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

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
lookup_shelf_life({"product_name": "spinach", "storage_state": "refrigerated"})
find_matches({"load_description": "ten crates of spinach", "donor_description": "A grocer in Chicago", "hours_remaining": 6, "needs_cold": true, "pallets": 0.25})
```

The structured brief is in [spinach-brief.json](spinach-brief.json) and the written answer in [spinach-answer.md](spinach-answer.md).

## Question: A farm south of Chicago has 5 tons of potatoes still in the field. They can load pallets if someone collects within 3 days.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "pantry", "product_name": "Potatoes"})
find_matches({"donor_description": "A farm south of Chicago", "load_description": "5 tons of potatoes", "needs_cold": false, "pallets": 5, "hours_remaining": 72})
```

The structured brief is in [farm-potatoes-brief.json](farm-potatoes-brief.json) and the written answer in [farm-potatoes-answer.md](farm-potatoes-answer.md).

## Question: A bakery has 40 trays of cream-filled pastries that must stay refrigerated and leave their dock within 1 hour.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "Pastries", "storage_state": "refrigerated"})
find_matches({"pallets": 0.5, "load_description": "40 trays of cream-filled pastries", "hours_remaining": 1, "needs_cold": true, "donor_description": "A local bakery"})
```

The structured brief is in [no-match-bakery-brief.json](no-match-bakery-brief.json) and the written answer in [no-match-bakery-answer.md](no-match-bakery-answer.md).

## Question: Not counting the invented teaching cases (profile_source 'planted'), how many recipients have walk-in cold storage, and what share is that?

Tool calls, in order:

```text
execute_sql({"projectId": "<lab-project-id>", "query": "SELECT\n  COUNTIF(cold_storage = 'walk-in') AS walk_in_count,\n  COUNT(*) AS total_real_recipients,\n  ROUND(COUNTIF(cold_storage = 'walk-in') / COUNT(*) * 100, 1) AS walk_in_pct\nFROM `<lab-project-id>.a4i_food.recipients`\nWHERE profile_source != 'planted'"})
```

The written answer is in [mcp-walk-in-answer.md](mcp-walk-in-answer.md).

## Question: 48 cases of sealed infant formula with 8 months to expiry from a distributor in Chicago, 2 pallets, can sit at room temperature.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "pantry", "product_name": "Infant formula"})
lookup_shelf_life({"storage_state": "pantry", "product_name": "Baby food"})
find_matches({"pallets": 2, "donor_description": "A distributor in Chicago", "load_description": "48 cases of sealed infant formula (2 pallets)", "hours_remaining": 5760, "needs_cold": false})
```

The structured brief is in [sealed-formula-brief.json](sealed-formula-brief.json) and the written answer in [sealed-formula-answer.md](sealed-formula-answer.md).
