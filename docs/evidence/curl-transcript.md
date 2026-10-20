# Live service transcript

Captured 2026-10-20 10:49 EDT from the deployed Cloud Run service. The recipient names and addresses are real (IRS data). Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

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
find_matches({"needs_cold": true, "donor_description": "A grocer in Chicago", "pallets": 1, "hours_remaining": 6, "load_description": "ten crates of spinach"})
```

The structured brief is in [spinach-brief.json](spinach-brief.json) and the written answer in [spinach-answer.md](spinach-answer.md).

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
lookup_shelf_life({"storage_state": "pantry", "product_name": "Infant formula"})
find_matches({"donor_description": "a distributor in Chicago", "pallets": 2, "load_description": "two pallets of infant formula", "hours_remaining": 5760, "needs_cold": false})
```

The structured brief is in [sealed-formula-brief.json](sealed-formula-brief.json) and the written answer in [sealed-formula-answer.md](sealed-formula-answer.md).
