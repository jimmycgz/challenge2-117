# Evidence from the live service

The demo ran in a temporary lab project that will be deleted. These files were captured from the deployed Cloud Run
service and from the lab's BigQuery tables on 2026-10-20, with the lab identifiers replaced by placeholders.

The recipient names and addresses are real (IRS data), except nine invented teaching cases the challenge adds to the
corpus, which have no real street or ZIP; Greenline Community Pantry and Maple Street Produce Alliance are two of them.
Everyone's cold storage, pallet capacity and pickup times are generated, as the
[agent README](../../agent/food_broker/README.md) says. Nothing here is a claim about what a real
organization has.

| File | What it shows |
|---|---|
| [curl-transcript.md](curl-transcript.md) | The service answering with no credentials: health check, chat page redirect, the tool calls for two questions |
| [spinach-answer.md](spinach-answer.md), [spinach-brief.json](spinach-brief.json) | A full answer for ten crates of spinach, and the structured Match Brief behind it |
| [sealed-formula-answer.md](sealed-formula-answer.md), [sealed-formula-brief.json](sealed-formula-brief.json) | The sealed infant formula case: the agent used the donor's 8-month expiry, not the 1-hour table figure |
| [farm-potatoes-answer.md](farm-potatoes-answer.md), [farm-potatoes-brief.json](farm-potatoes-brief.json) | Five tons of potatoes: a farm-track load handled by the same corpus |
| [no-match-bakery-answer.md](no-match-bakery-answer.md) | Cream-filled pastries that must leave in one hour: the agent says nobody can take them and shows why |
| [demo-tracks.txt](demo-tracks.txt) | A retail, a farm and an essentials posting through the same corpus and search, with what the filters removed and why |
| [mcp-walk-in-answer.md](mcp-walk-in-answer.md) | A free-form data question answered through Google's managed BigQuery MCP server on the live service: two `execute_sql` calls. Captured from the live service, revision `food-broker-00010-9jc`, after the agent was told to leave the invented cases out; it shows the SQL filtering on `profile_source`. The real figure is 6 of 183 |
| [follow-ups-transcript.md](follow-ups-transcript.md) | One conversation, six turns: a match, "they said no" twice (the next recipients are briefed), "why not" a named organization and the big food bank, and a question answered from the earlier brief |
| [validation.txt](validation.txt) | The notebook's 25 validation checks run on the loaded tables: 23 pass, 2 fail, with the failing rows and what our agent does about each. One check shown able to fail |
| [decoy-greens-24h-answer.md](decoy-greens-24h-answer.md) | A 24-hour greens offer: the decoy (Greenline, a pantry with no cold storage that reads like a perfect match) is removed for storage alone, not for the clock. Show the rejected list (part 6), not the top match: this run's top match is an invented teaching case. The 6-hour spinach capture has a real organization as its pick |
| [frozen-chicken-answer.md](frozen-chicken-answer.md) | Frozen chicken: only recipients with a freezer are matched |
| [invariants.txt](invariants.txt) | The invariant check on all ten postings: every recommended recipient meets every hard constraint, nothing lost (0 violations) |
| [selfcheck.txt](selfcheck.txt) | The offline check passing |

Screenshots or a recording of the chat page are not here yet; the team's pitch video covers them.
