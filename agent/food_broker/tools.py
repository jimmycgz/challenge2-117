"""Tools for the food-rescue broker.

Layout: the BigQuery calls are thin (`vector_candidates`, `lookup_shelf_life`); the judgment lives
in plain functions (`apply_constraints`, `build_match_brief`) that can be checked without a cloud
project. Vector search only proposes candidates. The constraint filter decides.

Configuration is by environment variable so the same code runs in Cloud Shell, Cloud Run and
locally: GOOGLE_CLOUD_PROJECT, A4I_DATASET, A4I_EMBED_ENDPOINT.
"""

import os
from typing import Optional

DATASET = os.environ.get("A4I_DATASET", "a4i_food")
EMBED_ENDPOINT = os.environ.get("A4I_EMBED_ENDPOINT", "gemini-embedding-2")

# cold_storage values the notebook generates. "domestic" is a household fridge.
REAL_COLD = {"walk-in", "commercial", "medical", "vehicle"}

# ASSUMPTION, to verify against the data: pickup_window_hours is read as the lead time the
# recipient needs to collect after being told. If the data means something else, change it here.
# A household fridge is treated as holding about one pallet's worth of cold product, no more.
DOMESTIC_FRIDGE_PALLETS = 1


def _client():
    # Imported here so the pure functions below load without google-cloud-bigquery installed.
    from google.cloud import bigquery

    from .identity_guard import assert_lab_identity

    assert_lab_identity()  # stops here if the credentials are not the lab's
    return bigquery.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))


def vector_candidates(posting_text: str, top_k: int = 80) -> list[dict]:
    """Semantic candidates for a posting: BigQuery VECTOR_SEARCH over recipient_embeddings.

    Meaning only. The result still includes organizations that cannot store the food; filter it
    with apply_constraints.

    Args:
        posting_text: The donor's offer as typed, e.g. "10 crates of spinach, harvested yesterday".
        top_k: How many nearest recipients to return before filtering. Keep it wide: on the
            Chicago corpus (192 recipients) a pool of 15 left 1 viable recipient for a 6-hour
            spinach offer, 40 left 3 and 80 left 12, because the filter removes most matches.

    Returns:
        Recipient rows (dicts) ordered by semantic distance, each with a `distance` field.
    """
    from google.cloud import bigquery

    sql = f"""
    SELECT
      base.recipient_id, base.name, base.street, base.city, base.state, base.zip_code,
      base.cold_storage, base.frozen_storage, base.loading_dock, base.refrigerated_transport,
      base.max_pallets, base.pickup_window_hours, base.weekly_households,
      base.populations_served, base.service_days, base.profile_text,
      base.latitude, base.longitude, distance
    FROM VECTOR_SEARCH(
      TABLE `{DATASET}.recipient_embeddings`, 'embedding',
      (SELECT AI.EMBED(@posting, endpoint => '{EMBED_ENDPOINT}').result AS embedding),
      top_k => @top_k,
      options => '{{"use_brute_force":true}}')
    ORDER BY distance
    """
    job = _client().query(
        sql,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("posting", "STRING", posting_text),
                bigquery.ScalarQueryParameter("top_k", "INT64", top_k),
            ]
        ),
    )
    return [dict(row) for row in job.result()]


def lookup_shelf_life(product_name: str, storage_state: str = "refrigerated") -> dict:
    """USDA FoodKeeper shelf life for a product, in hours (consumer guidance, not cold-chain science).

    Args:
        product_name: FoodKeeper product name, e.g. "Lettuce", "Milk", "Bread".
        storage_state: "refrigerated" or "pantry".

    Returns:
        {"product", "storage_state", "hours", "note"}; hours is None when FoodKeeper has no figure.
    """
    from google.cloud import bigquery

    column = "refrigerated_hours" if storage_state == "refrigerated" else "pantry_hours"
    note_column = "refrigerated_note" if storage_state == "refrigerated" else "pantry_note"
    sql = f"""
    SELECT product_name, {column} AS hours, {note_column} AS note
    FROM `{DATASET}.shelf_life`
    WHERE LOWER(product_name) = LOWER(@product)
    LIMIT 1
    """
    job = _client().query(
        sql,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("product", "STRING", product_name)]
        ),
    )
    rows = list(job.result())
    if not rows:
        return {"product": product_name, "storage_state": storage_state, "hours": None,
                "note": "product not in FoodKeeper under that name"}
    r = rows[0]
    return {"product": r.product_name, "storage_state": storage_state, "hours": r.hours,
            "note": r.note}


def apply_constraints(
    candidates: list[dict],
    hours_remaining: float,
    needs_cold: bool,
    pallets: float = 1,
) -> dict:
    """Split semantic candidates into viable matches (ranked) and eliminated ones, with reasons.

    Args:
        candidates: Rows from vector_candidates.
        hours_remaining: Hours the food has left, already capped by the donor's own deadline.
        needs_cold: True if the food must stay cold.
        pallets: Size of the load in pallets (a crate-sized load is a fraction of 1).

    Returns:
        {"viable": [...], "eliminated": [...]}. Viable rows carry `margin_hours` (time left after
        the recipient's collection lead time), `needs_driver` and `why_viable`. Eliminated rows
        carry `eliminated_because`. Viable is ordered by margin first, then semantic distance.
    """
    viable, eliminated = [], []
    for c in candidates:
        cold = c.get("cold_storage", "none")
        reasons = []

        if needs_cold:
            if cold == "none":
                reasons.append("no cold storage")
            elif cold == "domestic" and pallets > DOMESTIC_FRIDGE_PALLETS:
                reasons.append(
                    f"only a household fridge, load is {pallets:g} pallets"
                )
        if (c.get("max_pallets") or 0) < pallets:
            reasons.append(f"capacity {c.get('max_pallets')} pallets, load is {pallets:g}")
        lead = c.get("pickup_window_hours")
        margin = None if lead is None else hours_remaining - lead
        if margin is not None and margin < 0:
            reasons.append(f"needs {lead:g}h to collect, food has {hours_remaining:g}h")

        if reasons:
            eliminated.append({**c, "eliminated_because": "; ".join(reasons)})
            continue

        needs_driver = needs_cold and not c.get("refrigerated_transport", False)
        viable.append({
            **c,
            "margin_hours": margin,
            "needs_driver": needs_driver,
            "why_viable": (
                f"{cold} cold storage, takes up to {c.get('max_pallets')} pallets, "
                f"collects within {lead}h" if lead is not None else
                f"{cold} cold storage, takes up to {c.get('max_pallets')} pallets, "
                "collection time not stated"
            ),
        })

    # Ranking, in order: a comfortable margin (at least 2h and a quarter of the clock) beats a thin
    # or unknown one; then sturdier cold storage and own refrigerated transport; then meaning.
    # Margin is a tier, not a sort key, so 2h versus 3h of slack is not treated as a real difference.
    comfortable = max(2.0, 0.25 * hours_remaining)

    def rank(v: dict) -> tuple:
        m = v["margin_hours"]
        tier = 0 if (m is not None and m >= comfortable) else 1 if m is not None else 2
        sturdy = 0 if v.get("cold_storage") in REAL_COLD or not needs_cold else 1
        own_transport = 0 if v.get("refrigerated_transport") else 1
        return (tier, sturdy, own_transport, v.get("distance", 0))

    viable.sort(key=rank)
    return {"viable": viable, "eliminated": eliminated}


def lookup_neighborhood(latitude: float, longitude: float) -> dict:
    """Who the recipient's neighborhood is, from the nearest census tract (ACS), for the brief.

    The nearest tract is found by distance to the tract's internal point, because recipient
    locations are ZIP-level, not geocoded. Read it as the area the pantry sits in, not an exact tract.
    This describes need after the match; it is never used to rank recipients.

    Args:
        latitude: Recipient latitude.
        longitude: Recipient longitude.

    Returns:
        {"geo_id", "poverty_rate", "no_vehicle_rate", "assistance_rate", "median_income",
        "distance_km"}, or {"note": ...} if no tract is found.
    """
    from google.cloud import bigquery

    sql = f"""
    SELECT geo_id, poverty_rate, no_vehicle_rate, assistance_rate, median_income,
           ST_DISTANCE(ST_GEOGPOINT(tract_lon, tract_lat), ST_GEOGPOINT(@lon, @lat)) / 1000 AS distance_km
    FROM `{DATASET}.tract_demographics`
    ORDER BY distance_km
    LIMIT 1
    """
    job = _client().query(
        sql,
        job_config=bigquery.QueryJobConfig(query_parameters=[
            bigquery.ScalarQueryParameter("lat", "FLOAT64", latitude),
            bigquery.ScalarQueryParameter("lon", "FLOAT64", longitude),
        ]),
    )
    rows = list(job.result())
    if not rows:
        return {"note": "no census tract found near this location"}
    return dict(rows[0])


def _neighborhood_line(n: Optional[dict]) -> str:
    if not n or "poverty_rate" not in n:
        return "Neighborhood data was not looked up for this match."
    def pct(x):
        return "unknown" if x is None else f"{x:.0%}"
    return (f"Nearest census tract: {pct(n.get('poverty_rate'))} of residents below the poverty line, "
            f"{pct(n.get('no_vehicle_rate'))} of households without a vehicle, "
            f"{pct(n.get('assistance_rate'))} on food or cash assistance "
            "(ACS; recipient location is ZIP-level, so this is the area, not the exact block).")


def _outreach(name: str, load_description: str, donor_description: str,
              hours_remaining: float, margin: Optional[float], needs_driver: bool) -> str:
    """A plain first draft the agent may polish. Short, specific, and honest about the clock."""
    clock = (f"The food needs to leave by about {hours_remaining:g} hours from now"
             + (f", which leaves you roughly {margin:g} hours of slack to collect." if margin is not None
                else "."))
    driver = (" We can arrange a driver, since it has to stay cold on the way."
              if needs_driver else " You are set up to collect it yourselves.")
    return (f"Hello {name} team,\n\n"
            f"{donor_description} has {load_description}. It is still good but has to move soon. "
            f"From what we have on file you have the storage for it. {clock}{driver}\n\n"
            "Can you take it? If you can, tell us the time you can collect and a phone number for "
            "pickup. If not, a quick no helps us move to the next place.\n\nThank you,\n[Coordinator name]")


def _excerpt(text: str, limit: int = 240) -> str:
    """First part of a profile, cut at a sentence or word boundary so it never ends mid-word."""
    if len(text) <= limit:
        return text
    cut = text[:limit]
    end = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    if end > limit // 2:
        return cut[: end + 1]
    return cut[: cut.rfind(" ")].rstrip(",;:") + "..."


def build_match_brief(
    posting_text: str,
    hours_remaining: float,
    viable: list[dict],
    eliminated: Optional[list[dict]] = None,
    load_description: str = "surplus food",
    donor_description: str = "A local donor",
    pallets: float = 1,
    neighborhood: Optional[dict] = None,
) -> dict:
    """Assemble the Match Brief: six labelled parts a coordinator can act on without a follow-up.

    Parts: organization_and_why, what_they_can_take, the_clock, whose_neighborhood,
    outreach_message, next_two_options. `ranked` lists up to three options in order.

    Args:
        posting_text: The original offer.
        hours_remaining: Hours the food has left.
        viable: The `viable` list from apply_constraints.
        eliminated: The `eliminated` list, used to show why close semantic matches were rejected.
        load_description: The load in a few words, e.g. "ten crates of spinach".
        donor_description: Who is giving it, e.g. "A grocer on the north side".
        pallets: Load size in pallets, as passed to apply_constraints.
        neighborhood: The result of lookup_neighborhood for the top match's location.

    Returns:
        The brief as a dict. If nothing is viable `top` parts are None and `refusal` says so
        plainly: an honest "nobody can take this" beats a confident wrong answer.
    """
    eliminated = eliminated or []
    rejected = [{"name": e["name"], "because": e["eliminated_because"]} for e in eliminated[:3]]
    if not viable:
        return {
            "organization_and_why": None, "what_they_can_take": None,
            "the_clock": {"hours_remaining": hours_remaining, "margin_hours": None},
            "whose_neighborhood": None, "outreach_message": None, "next_two_options": [],
            "ranked": [], "rejected_but_close": rejected,
            "refusal": "No candidate can take this load in time. The closest rejections are listed "
                       "with the reason each was eliminated.",
        }

    def address(v: dict) -> str:
        return (f'{v.get("street", "")}, {v.get("city", "")}, {v.get("state", "")} '
                f'{v.get("zip_code", "")}').strip(", ")

    def card(rank: int, v: dict) -> dict:
        return {"rank": rank, "name": v["name"], "address": address(v),
                "why": v["why_viable"], "margin_hours": v["margin_hours"],
                "needs_driver": v["needs_driver"]}

    top = viable[0]
    ranked = [card(i + 1, v) for i, v in enumerate(viable[:3])]
    return {
        "organization_and_why": {
            "name": top["name"], "address": address(top),
            "why": top["why_viable"],
            "profile_excerpt": _excerpt(top.get("profile_text") or ""),
        },
        "what_they_can_take": {
            "load_pallets": pallets, "max_pallets": top.get("max_pallets"),
            "cold_storage": top.get("cold_storage"),
            "frozen_storage": top.get("frozen_storage"),
            "loading_dock": top.get("loading_dock"),
            "refrigerated_transport": top.get("refrigerated_transport"),
            "service_days": top.get("service_days"),
        },
        "the_clock": {
            "hours_remaining": hours_remaining,
            "collection_lead_hours": top.get("pickup_window_hours"),
            "margin_hours": top["margin_hours"],
            "needs_driver": top["needs_driver"],
        },
        "whose_neighborhood": {
            "households_per_week": top.get("weekly_households"),
            "populations_served": top.get("populations_served"),
            "tract": _neighborhood_line(neighborhood),
        },
        "outreach_message": _outreach(top["name"], load_description, donor_description,
                                      hours_remaining, top["margin_hours"], top["needs_driver"]),
        "next_two_options": ranked[1:3],
        "ranked": ranked,
        "rejected_but_close": rejected,
        "refusal": None,
    }
