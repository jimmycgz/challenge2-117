<!-- markdownlint-disable MD029 MD030 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: Not counting the invented teaching cases (profile_source 'planted'), how many recipients have walk-in cold storage, and what share is that?

Captured 2026-10-20 12:41 EDT, from the agent running locally against the lab tables and Google's managed BigQuery MCP server, before the next deploy. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says.

SQL the agent ran through Google's managed BigQuery MCP server (read-only), in order:

```sql
SELECT COUNT(*) FROM `<lab-project-id>.a4i_food.recipients` WHERE profile_source != 'planted'
```

```sql
SELECT COUNT(*) FROM `<lab-project-id>.a4i_food.recipients` WHERE cold_storage = 'walk-in' AND profile_source != 'planted'
```

---

Not counting the 9 invented teaching cases, 6 recipients have walk-in cold storage, which is 3.3% of the total.
