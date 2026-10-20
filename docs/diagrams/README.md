# Diagrams

Navigation: [repository index](../../README.md) · [design as built](../DESIGN.md) · [agent README](../../agent/food_broker/README.md)

Each diagram is an SVG with its text as real text, next to a PNG render of it. All are our own drawings: no Google logos or product icons.

| Diagram | Files | What it shows |
|---|---|---|
| System architecture | [architecture.svg](architecture.svg), [architecture.png](architecture.png) | The coordinator, the identity guard, the `food_broker` agent on Gemini inside Cloud Run, its three tools, the BigQuery MCP server, the BigQuery tables, and the steps inside `find_matches`. Colours: blue agent path, violet data, green result, red the filters that remove recipients |
| System architecture, deck version | [architecture-deck-copy.svg](architecture-deck-copy.svg), [architecture-deck-copy.png](architecture-deck-copy.png) | The same diagram as used in the pitch deck: retitled, no model version, no "reads only" label, and the recipients table labelled "192 (9 invented)" |
| Line icons | [icons-sheet.svg](icons-sheet.svg), [icons-sheet.png](icons-sheet.png), [icons/](icons/) | Eleven icons in one style (64 by 64, stroke width 3): cart, tractor, baby bottle, clock, fridge, van, phone message, map pin, shield, check, cross |
| Logo | [logo-A.svg](logo-A.svg), [logo-A.png](logo-A.png) | A clock and a leaf |

The deck itself is [docs/RescueBroker-Pitch-Deck.pdf](../RescueBroker-Pitch-Deck.pdf).

## Where the architecture comes from

The diagram follows the code and the design file, not the other way round. Where the two disagree, the diagram shows the code:

- The freezer filter is in `apply_constraints` in [tools.py](../../agent/food_broker/tools.py); [DESIGN.md](../DESIGN.md) does not list it.
- The model and thinking level come from [lab.env](../../agent/lab.env), which [deploy.sh](../../agent/deploy.sh) passes to Cloud Run. The code's own default model is a different one.
- The BigQuery MCP tool the agent loads is `execute_sql_readonly`, set in [agent.py](../../agent/food_broker/agent.py). See [the write probe](../evidence/readonly-mcp-write-probe.md) for what that does and does not enforce. The service still runs as the project's default compute account.
- The chat page is at `/dev-ui/` on the Cloud Run address.
