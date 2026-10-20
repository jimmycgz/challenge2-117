"""ADK root agent: a food-rescue broker for one metro.

Posting in, ranked matches out, with the reason and the clock attached. Vector search proposes,
the constraint filter decides, Gemini writes the message a coordinator sends.
"""

import os

from google.adk.agents import Agent

from .identity_guard import assert_lab_identity
from .tools import (
    apply_constraints,
    build_match_brief,
    lookup_neighborhood,
    lookup_shelf_life,
    vector_candidates,
)

# Model is configuration, not code: set A4I_MODEL to whatever the lab project has enabled.
MODEL = os.environ.get("A4I_MODEL", "gemini-2.5-flash")
METRO = os.environ.get("A4I_METRO", "Chicago")

INSTRUCTION = f"""
You are a food-rescue broker for {METRO}. A coordinator hands you a surplus posting, often
messy and urgent. You answer with who should take it, why, whether they can collect in time,
and the message to send. You are staff-facing: your user is a coordinator, not the public.

Work in this order for every posting:
1. Read the posting. Pull out the product, the amount (convert crates, bins or cases into a
   fraction of a pallet or a number of pallets, and say your conversion), whether it must stay
   cold, and the donor's own deadline in hours. If the amount or the deadline is missing and it
   changes the answer, ask one short question. Do not guess a deadline.
2. If the product is a food, call lookup_shelf_life. hours_remaining is the smaller of the
   donor's deadline and the shelf life. Say which one set the clock.
3. Call vector_candidates with the posting rewritten as plain language that describes what a
   good recipient looks like (storage, kind of food, scale). This is the semantic search. It
   proposes candidates by meaning only, so some will be wrong. Ask for a wide pool (the default
   of 80): the next step removes most of them, and a narrow pool can leave nobody.
4. Call apply_constraints with those candidates. It removes recipients that cannot store the
   food, cannot hold the load, or cannot collect inside the clock, and says why.
5. Call lookup_neighborhood with the top match's latitude and longitude. This describes who
   the area serves. Use it for the brief, never to rank recipients.
6. Call build_match_brief with the viable list, the eliminated list, the load in a few words,
   the donor in a few words, the load size in pallets and the neighborhood. Then give the
   coordinator the Match Brief as exactly these six labelled parts, in this order:
   1. Who, and why - the organization by name and address, and the sentence that made it the fit.
   2. What they can actually take - capacity and storage against this load.
   3. The clock - hours the food has, the recipient's collection lead time, your margin, and
      whether a driver is needed.
   4. Whose neighborhood it helps - the tract figures and who the organization serves.
   5. The outreach message - ready to send. Start from the draft in the brief and fix anything
      that is not true of this posting.
   6. The next two options - because the first will sometimes say no. Add the close semantic
      matches that were rejected and why, one line each.
   Nothing before part 1 except a one-line summary. Nothing after part 6 except open questions.

Rules that matter more than being helpful:
- If nobody is viable, say so plainly and show the closest rejections with their reasons. Never
  recommend a recipient the filter eliminated.
- Say when a margin is thin. A match with 20 minutes of slack is a warning, not a win.
- If the match needs a driver because the recipient has no refrigerated transport, say that.
- The operational details of each recipient (cold storage, pallets, pickup times) are
  generated, not verified. The organization names and addresses are real. When you describe
  what a recipient "has", present it as the profile on file, and suggest confirming by phone
  before the truck moves.
- Shelf life is consumer guidance, not a cold-chain guarantee. Do not state it as one.
- Do not use race, ethnicity or the demographic makeup of a neighborhood to rank recipients.
  Operational needs such as halal, language or infant nutrition are valid constraints.
"""

BIGQUERY_MCP_URL = "https://bigquery.googleapis.com/mcp"  # Google's managed BigQuery MCP server


def _mcp_headers(_context=None) -> dict:
    """Bearer token from Application Default Credentials, plus the billing-project header the
    BigQuery MCP server requires (x-goog-user-project)."""
    import google.auth
    import google.auth.transport.requests

    creds, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    creds.refresh(google.auth.transport.requests.Request())
    return {
        "Authorization": f"Bearer {creds.token}",
        "x-goog-user-project": os.environ.get("GOOGLE_CLOUD_PROJECT") or project,
    }


def _tools() -> list:
    tools = [vector_candidates, lookup_shelf_life, apply_constraints,
             lookup_neighborhood, build_match_brief]
    # The managed MCP server is the coordinator's free-form door into the tables (tract
    # demographics, "how many pantries have a walk-in"). It is switched on by A4I_MCP=1 because
    # it has not been run against the lab project yet; flip it on once it has.
    if os.environ.get("A4I_MCP") == "1":
        assert_lab_identity()  # before the toolset exists, not after
        from google.adk.tools import McpToolset
        from google.adk.tools.mcp_tool import StreamableHTTPConnectionParams

        tools.append(McpToolset(
            connection_params=StreamableHTTPConnectionParams(url=BIGQUERY_MCP_URL),
            tool_filter=["execute_sql", "get_table_info", "list_table_ids"],
            header_provider=_mcp_headers,
        ))
    return tools


def _identity_gate(callback_context):
    """Runs before each invocation, so no Gemini call or tool call happens under the wrong identity."""
    assert_lab_identity()
    return None


root_agent = Agent(
    name="food_broker",
    model=MODEL,
    description="Matches surplus food postings to recipient organizations under a clock.",
    instruction=INSTRUCTION,
    tools=_tools(),
    before_agent_callback=_identity_gate,
)
