<!-- markdownlint-disable MD030 MD032 MD036 -->
<!-- The answer below is the model's output verbatim, so it keeps its own list spacing. -->

# Answer to: How many recipients in the corpus have walk-in cold storage, and what share of all recipients is that?

Captured 2026-10-20 10:49 EDT. The recipient names and addresses are real (IRS data). Their cold storage, pallet capacity and pickup times are generated, as the README says; nothing here is a claim about what a real organization has.

Tool calls, in order:

```text
execute_sql({"query": "SELECT COUNT(*) FROM `<lab-project-id>.a4i_food.recipients` WHERE cold_storage = 'walk-in'", "projectId": "<lab-project-id>"})
execute_sql({"query": "SELECT COUNT(*) FROM `<lab-project-id>.a4i_food.recipients`", "projectId": "<lab-project-id>"})
```

---

There are 13 recipients with walk-in cold storage, which is 6.77% of all recipients.
