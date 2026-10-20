# Live service transcript

Captured 14:14 EDT on 2026-10-20 from the deployed Cloud Run service. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

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
find_matches({"load_description": "ten crates of spinach", "pallets": 0.2, "search_text": "A community pantry, shelter, or kitchen with refrigeration/cold storage that can take fresh leafy produce and perishable vegetables at a small scale.", "donor_description": "A grocer in Chicago", "needs_cold": true, "hours_remaining": 6})
```

The structured brief is in [spinach-brief.json](spinach-brief.json) and the written answer in [spinach-answer.md](spinach-answer.md).

## Question: A farm south of Chicago has 5 tons of potatoes still in the field. They can load pallets if someone collects within 3 days.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "Potatoes", "storage_state": "pantry"})
find_matches({"search_text": "large capacity warehouse pantry food bank able to take 5 pallets of fresh potatoes shelf stable hardy produce bulk root vegetables", "needs_frozen": false, "needs_cold": false, "top_k": 80, "donor_description": "A farm south of Chicago", "pallets": 5, "hours_remaining": 72, "load_description": "5 tons of potatoes"})
```

The structured brief is in [farm-potatoes-brief.json](farm-potatoes-brief.json) and the written answer in [farm-potatoes-answer.md](farm-potatoes-answer.md).

## Question: A bakery has 40 trays of cream-filled pastries that must stay refrigerated and leave their dock within 1 hour.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "Pastries", "storage_state": "refrigerated"})
find_matches({"pallets": 0.5, "top_k": 80, "donor_description": "A local bakery", "needs_cold": true, "search_text": "refrigerated dairy bakery items cream-filled pastries small load fast emergency pickup", "needs_frozen": false, "load_description": "40 trays of cream-filled pastries", "hours_remaining": 1})
```

The structured brief is in [no-match-bakery-brief.json](no-match-bakery-brief.json) and the written answer in [no-match-bakery-answer.md](no-match-bakery-answer.md).

## Question: Not counting the invented teaching cases (profile_source 'planted'), how many recipients have walk-in cold storage, and what share is that?

Tool calls, in order:

```text
execute_sql({"projectId": "<lab-project-id>", "query": "SELECT\n  COUNTIF(cold_storage = 'walk-in') AS walk_in_count,\n  COUNT(*) AS total_count,\n  ROUND(COUNTIF(cold_storage = 'walk-in') * 100.0 / COUNT(*), 1) AS walk_in_pct\nFROM `<lab-project-id>.a4i_food.recipients`\nWHERE profile_source != 'planted'"})
```

The written answer is in [mcp-walk-in-answer.md](mcp-walk-in-answer.md).

## Question: A grocer has 8 crates of fresh salad greens and spinach that must stay cold; they can hold it in their cooler for 24 hours.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "Spinach", "storage_state": "refrigerated"})
find_matches({"search_text": "fresh salad greens spinach cold storage produce small pantry crate load", "needs_cold": true, "pallets": 0.25, "needs_frozen": false, "hours_remaining": 24, "donor_description": "A local grocer", "load_description": "8 crates of fresh salad greens and spinach"})
```

The structured brief is in [decoy-greens-24h-brief.json](decoy-greens-24h-brief.json) and the written answer in [decoy-greens-24h-answer.md](decoy-greens-24h-answer.md).

## Question: A grocer in Chicago has 6 cases of frozen chicken, stored at minus 18, that must be collected within 24 hours.

Tool calls, in order:

```text
lookup_shelf_life({"storage_state": "refrigerated", "product_name": "Chicken"})
find_matches({"needs_cold": true, "donor_description": "A grocer in Chicago", "load_description": "6 cases of frozen chicken", "hours_remaining": 24, "pallets": 0.25, "needs_frozen": true, "search_text": "frozen poultry chicken raw meat cold storage freezer capacity small batch distribution"})
```

The structured brief is in [frozen-chicken-brief.json](frozen-chicken-brief.json) and the written answer in [frozen-chicken-answer.md](frozen-chicken-answer.md).

## Question: 48 cases of sealed infant formula with 8 months to expiry from a distributor in Chicago, 2 pallets, can sit at room temperature.

Tool calls, in order:

```text
lookup_shelf_life({"product_name": "infant formula", "storage_state": "pantry"})
lookup_shelf_life({"storage_state": "pantry", "product_name": "baby formula"})
lookup_shelf_life({"product_name": "formula", "storage_state": "pantry"})
find_matches({"search_text": "infant formula, baby formula, sealed baby food, pantry storage, families with infants, maternal child nutrition", "pallets": 2, "needs_cold": false, "donor_description": "A distributor in Chicago", "hours_remaining": 5760, "needs_frozen": false, "load_description": "48 cases (2 pallets) of sealed infant formula"})
```

The structured brief is in [sealed-formula-brief.json](sealed-formula-brief.json) and the written answer in [sealed-formula-answer.md](sealed-formula-answer.md).
