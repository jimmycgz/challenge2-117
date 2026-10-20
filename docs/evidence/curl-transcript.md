# Live service transcript

Captured 14:40 EDT on 2026-10-20 from the deployed Cloud Run service. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

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
find_matches({"needs_frozen": false, "pallets": 0.5, "load_description": "ten crates of fresh spinach", "needs_cold": true, "donor_description": "A grocer in Chicago", "search_text": "Community pantry or soup kitchen needing fresh leafy greens, produce, spinach. Must have cold storage or walk-in cooler, able to accept partial pallet load and pickup quickly within 6 hours.", "hours_remaining": 6, "top_k": 80})
```

The structured brief is in [spinach-brief.json](spinach-brief.json) and the written answer in [spinach-answer.md](spinach-answer.md).

## Question: A farm south of Chicago has 5 tons of potatoes still in the field. They can load pallets if someone collects within 3 days.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "pantry", "product_name": "Potatoes"})
find_matches({"donor_description": "A farm south of Chicago", "load_description": "5 tons of potatoes", "needs_frozen": false, "search_text": "large scale dry storage pantry hardy produce root vegetables bulk potatoes 5 pallets", "hours_remaining": 72, "pallets": 5, "needs_cold": false})
```

The structured brief is in [farm-potatoes-brief.json](farm-potatoes-brief.json) and the written answer in [farm-potatoes-answer.md](farm-potatoes-answer.md).

## Question: A bakery has 40 trays of cream-filled pastries that must stay refrigerated and leave their dock within 1 hour.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "refrigerated", "product_name": "Pastries"})
find_matches({"donor_description": "A local bakery", "pallets": 0.5, "hours_remaining": 1, "needs_frozen": false, "needs_cold": true, "top_k": 80, "search_text": "Organization with cold storage or refrigeration capable of taking cream-filled pastries bakery surplus quickly within 1 hour", "load_description": "40 trays of cream-filled pastries"})
```

The structured brief is in [no-match-bakery-brief.json](no-match-bakery-brief.json) and the written answer in [no-match-bakery-answer.md](no-match-bakery-answer.md).

## Question: Not counting the invented teaching cases (profile_source 'planted'), how many recipients have walk-in cold storage, and what share is that?

Tool calls, in order:

```text
execute_sql_readonly({"projectId": "<lab-project-id>", "query": "SELECT\n  COUNTIF(cold_storage = 'walk-in') AS walk_in_count,\n  COUNT(*) AS total_real_recipients,\n  ROUND(COUNTIF(cold_storage = 'walk-in') * 100.0 / COUNT(*), 1) AS walk_in_pct\nFROM `<lab-project-id>.a4i_food.recipients`\nWHERE profile_source != 'planted'"})
```

The written answer is in [mcp-walk-in-answer.md](mcp-walk-in-answer.md).

## Question: A grocer has 8 crates of fresh salad greens and spinach that must stay cold; they can hold it in their cooler for 24 hours.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "Spinach", "storage_state": "refrigerated"})
find_matches({"needs_frozen": false, "load_description": "8 crates of fresh salad greens and spinach", "search_text": "Fresh salad greens and spinach requiring refrigeration, small scale fresh produce load for immediate distribution", "hours_remaining": 24, "needs_cold": true, "donor_description": "A local grocer", "pallets": 0.25})
```

The structured brief is in [decoy-greens-24h-brief.json](decoy-greens-24h-brief.json) and the written answer in [decoy-greens-24h-answer.md](decoy-greens-24h-answer.md).

## Question: A grocer in Chicago has 6 cases of frozen chicken, stored at minus 18, that must be collected within 24 hours.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "Chicken", "storage_state": "refrigerated"})
find_matches({"donor_description": "A grocer in Chicago", "needs_frozen": true, "hours_remaining": 24, "search_text": "frozen chicken meat poultry freezer storage small load 6 cases", "pallets": 0.1, "load_description": "6 cases of frozen chicken", "needs_cold": true})
```

The structured brief is in [frozen-chicken-brief.json](frozen-chicken-brief.json) and the written answer in [frozen-chicken-answer.md](frozen-chicken-answer.md).

## Question: 48 cases of sealed infant formula with 8 months to expiry from a distributor in Chicago, 2 pallets, can sit at room temperature.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "pantry", "product_name": "Infant formula"})
lookup_shelf_life({"storage_state": "pantry", "product_name": "Baby food"})
find_matches({"needs_cold": false, "load_description": "48 cases of sealed infant formula (2 pallets)", "pallets": 2, "hours_remaining": 5840, "needs_frozen": false, "search_text": "pantry shelf-stable infant formula baby formula infant nutrition families with infants toddlers children 2 pallets ambient storage", "donor_description": "A distributor in Chicago"})
```

The structured brief is in [sealed-formula-brief.json](sealed-formula-brief.json) and the written answer in [sealed-formula-answer.md](sealed-formula-answer.md).
