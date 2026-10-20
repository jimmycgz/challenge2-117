# Evidence from the live service

The demo ran in a temporary lab project that will be deleted. These files were captured from the deployed Cloud Run
service and from the lab's BigQuery tables on 2026-10-20, with the lab identifiers replaced by placeholders.

The recipient names and addresses are real (IRS data). Their cold storage, pallet capacity and pickup times are
generated, as the [agent README](../../agent/food_broker/README.md) says. Nothing here is a claim about what a real
organization has.

| File | What it shows |
|---|---|
| [curl-transcript.md](curl-transcript.md) | The service answering with no credentials: health check, chat page redirect, the tool calls for two questions |
| [spinach-answer.md](spinach-answer.md), [spinach-brief.json](spinach-brief.json) | A full answer for ten crates of spinach, and the structured Match Brief behind it |
| [sealed-formula-answer.md](sealed-formula-answer.md), [sealed-formula-brief.json](sealed-formula-brief.json) | The sealed infant formula case: the agent used the donor's 8-month expiry, not the 1-hour table figure |
| [demo-tracks.txt](demo-tracks.txt) | A retail, a farm and an essentials posting through the same corpus and search, with what the filters removed and why |
| [selfcheck.txt](selfcheck.txt) | The offline check passing |

Screenshots or a recording of the chat page are not here yet; the team's pitch video covers them.
