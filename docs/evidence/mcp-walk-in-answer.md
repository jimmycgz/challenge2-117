<!-- markdownlint-disable MD029 MD030 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: Not counting the invented teaching cases (profile_source 'planted'), how many recipients have walk-in cold storage, and what share is that?

Captured 13:52 EDT on 2026-10-20. The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the corpus, which have no real street or ZIP. Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
execute_sql({"projectId": "<lab-project-id>", "query": "SELECT\n  COUNTIF(cold_storage = 'walk-in') AS walk_in_count,\n  COUNT(*) AS total_real_recipients,\n  ROUND(COUNTIF(cold_storage = 'walk-in') / COUNT(*) * 100, 1) AS walk_in_pct\nFROM `<lab-project-id>.a4i_food.recipients`\nWHERE profile_source != 'planted'"})
```

---

Leaving out the 9 invented teaching cases (`profile_source = 'planted'`), there are **6 recipients** with walk-in cold storage out of 183 real organizations, which is **3.3%**.

*(Note: Recipient cold storage and capacity details are generated, not verified.)*

**Query executed:**
```sql
SELECT
  COUNTIF(cold_storage = 'walk-in') AS walk_in_count,
  COUNT(*) AS total_real_recipients,
  ROUND(COUNTIF(cold_storage = 'walk-in') / COUNT(*) * 100, 1) AS walk_in_pct
FROM `<lab-project-id>.a4i_food.recipients`
WHERE profile_source != 'planted'
```
