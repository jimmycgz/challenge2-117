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
      base.latitude, base.longitude, base.profile_source, distance
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
    rows = [dict(row) for row in job.result()]
    for position, row in enumerate(rows, 1):
        row["semantic_rank"] = position
    return rows


def _shelf_caution(hours) -> Optional[str]:
    """Warn when a shelf life is short enough to be an opened- or prepared-container figure, not a sealed product's."""
    if hours is not None and hours <= 2:
        return ("Under 2 hours is probably FoodKeeper's figure for an opened or prepared container. If the posting "
                "says the product is sealed or gives its own expiry, use the donor's figure instead.")
    return None


def shape_shelf_result(product: str, storage_state: str, rows: list[dict]) -> dict:
    """Turn the lookup's rows into the tool result. Pure, so it is tested without BigQuery.

    `rows` are product matches, best first, each {product_name, product_subtitle, hours, note, is_exact}.
    """
    exact = [r for r in rows if r.get("is_exact")]
    if exact:
        r = exact[0]
        result = {"product": r["product_name"], "storage_state": storage_state, "hours": r["hours"],
                  "note": r["note"]}
        caution = _shelf_caution(r["hours"])
        if caution:
            result["caution"] = caution
        return result
    if rows:
        return {
            "product": product, "storage_state": storage_state, "hours": None,
            "note": "No FoodKeeper entry is named exactly that. The closest entries are in `closest`: pick the one "
                    "that fits the product as sold (not canned or processed unless the posting says so), use its "
                    "hours, and say which entry you used.",
            "closest": [{"product_name": r["product_name"], "product_subtitle": r.get("product_subtitle"),
                         "hours": r["hours"]} for r in rows[:4]],
        }
    return {"product": product, "storage_state": storage_state, "hours": None,
            "note": "Nothing in FoodKeeper matches that name or keywords."}


def lookup_shelf_life(product_name: str, storage_state: str = "refrigerated") -> dict:
    """USDA FoodKeeper shelf life for a product, in hours (consumer guidance, not cold-chain science).

    Matches the exact product name first. If there is none (FoodKeeper lists spinach under "Bagged greens" and
    "Lettuce", for example) it returns the closest entries by name, subtitle or keyword for the caller to choose from.

    Args:
        product_name: A product, e.g. "Lettuce", "Milk", "Bread", "Spinach".
        storage_state: "refrigerated" or "pantry".

    Returns:
        {"product", "storage_state", "hours", "note"}; hours is None when FoodKeeper has no figure. A "caution" key is
        added when the figure is under 2 hours (likely an opened or prepared container figure). With no exact entry, `closest`
        lists up to four candidate entries {product_name, product_subtitle, hours}.
    """
    from google.cloud import bigquery

    column = "refrigerated_hours" if storage_state == "refrigerated" else "pantry_hours"
    note_column = "refrigerated_note" if storage_state == "refrigerated" else "pantry_note"
    sql = f"""
    SELECT product_name, product_subtitle, {column} AS hours, {note_column} AS note,
           LOWER(product_name) = LOWER(@product) AS is_exact
    FROM `{DATASET}.shelf_life`
    WHERE LOWER(product_name) = LOWER(@product)
       OR LOWER(product_name) LIKE CONCAT('%', LOWER(@product), '%')
       OR LOWER(IFNULL(product_subtitle, '')) LIKE CONCAT('%', LOWER(@product), '%')
       OR LOWER(IFNULL(keywords, '')) LIKE CONCAT('%', LOWER(@product), '%')
    ORDER BY is_exact DESC, hours IS NULL, LENGTH(product_name)
    LIMIT 6
    """
    job = _client().query(
        sql,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("product", "STRING", product_name)]
        ),
    )
    return shape_shelf_result(product_name, storage_state, [dict(r) for r in job.result()])


def _pallets(n) -> str:
    return f"{n} pallet" if n == 1 else f"{n} pallets"


def apply_constraints(
    candidates: list[dict],
    hours_remaining: float,
    needs_cold: bool,
    pallets: float = 1,
    needs_frozen: bool = False,
) -> dict:
    """Split semantic candidates into viable matches (ranked) and eliminated ones, with reasons.

    Args:
        candidates: Rows from vector_candidates.
        hours_remaining: Hours the food has left, already capped by the donor's own deadline.
        needs_cold: True if the food must stay cold.
        pallets: Size of the load in pallets (a crate-sized load is a fraction of 1).
        needs_frozen: True if the food must stay frozen. A recipient without a freezer is removed.

    Returns:
        {"viable": [...], "eliminated": [...]}. Viable rows carry `margin_hours` (time left after
        the recipient's collection lead time), `needs_driver` and `why_viable`. Eliminated rows
        carry `eliminated_because`. Viable is ordered by margin first, then semantic distance.
    """
    viable, eliminated = [], []
    for position, c in enumerate(candidates, 1):
        semantic_rank = c.get("semantic_rank", position)
        cold = c.get("cold_storage", "none")
        reasons = []

        if needs_cold:
            if cold == "none":
                reasons.append("no cold storage")
            elif cold == "domestic" and pallets > DOMESTIC_FRIDGE_PALLETS:
                reasons.append(
                    f"only a household fridge, load is {pallets:g} pallets"
                )
        if needs_frozen and not c.get("frozen_storage"):
            reasons.append("no freezer")
        if (c.get("max_pallets") or 0) < pallets:
            reasons.append(f"capacity {_pallets(c.get('max_pallets'))}, load is {pallets:g}")
        lead = c.get("pickup_window_hours")
        margin = None if lead is None else hours_remaining - lead
        if margin is not None and margin < 0:
            reasons.append(f"needs {lead:g}h to collect, food has {hours_remaining:g}h")

        if reasons:
            eliminated.append({**c, "eliminated_because": "; ".join(reasons),
                               "semantic_rank": semantic_rank})
            continue

        needs_driver = needs_cold and not c.get("refrigerated_transport", False)
        viable.append({
            **c,
            "semantic_rank": semantic_rank,
            "margin_hours": margin,
            "needs_driver": needs_driver,
            "why_viable": (
                f"{cold} cold storage, takes up to {_pallets(c.get('max_pallets'))}, "
                f"collects within {lead}h" if lead is not None else
                f"{cold} cold storage, takes up to {_pallets(c.get('max_pallets'))}, "
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
    # The closest rejections by meaning, but always including one that failed on cold storage when there is
    # one: that is the case where the search looked right and the recipient could not store the food.
    cold_failed = [e for e in eliminated if "no cold storage" in e["eliminated_because"]]
    others = [e for e in eliminated if e not in cold_failed]
    picked = cold_failed[:1]
    picked += others[: 3 - len(picked)]
    shown = sorted(picked, key=lambda e: e.get("semantic_rank", 0))
    rejected = [{"name": e["name"], "because": e["eliminated_because"],
                 "semantic_rank": e.get("semantic_rank"), "profile_source": e.get("profile_source")} for e in shown]
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
        return {"rank": rank, "meaning_rank": v.get("semantic_rank"), "name": v["name"], "address": address(v),
                "profile_source": v.get("profile_source"),
                "why": v["why_viable"], "margin_hours": v["margin_hours"],
                "needs_driver": v["needs_driver"]}

    top = viable[0]
    ranked = [card(i + 1, v) for i, v in enumerate(viable[:3])]
    return {
        "organization_and_why": {
            "name": top["name"], "address": address(top), "profile_source": top.get("profile_source"),
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


def explain_candidate(
    name_fragment: str,
    search_text: str,
    hours_remaining: float,
    needs_cold: bool,
    pallets: float = 1.0,
    top_k: int = 80,
    needs_frozen: bool = False,
) -> dict:
    """Why a named organization was or was not chosen for a posting.

    Re-runs the same search and filters and reports where organizations whose name contains the fragment came out:
    their rank by meaning, and either why they were removed or where they ranked among the viable ones.

    Args:
        name_fragment: Part of the organization's name, e.g. "food depository" or "greenline".
        search_text, hours_remaining, needs_cold, pallets, top_k, needs_frozen: The same values used for find_matches.

    Returns:
        {"matches": [...]} with up to five organizations, each {"name", "semantic_rank", "outcome", "detail"},
        or {"matches": [], "note": ...} when none is in the semantic pool, or {"error": {...}} on failure.
    """
    from .identity_guard import WrongIdentity

    try:
        candidates = vector_candidates(search_text, top_k=top_k)
        result = apply_constraints(candidates, hours_remaining, needs_cold, pallets, needs_frozen)
        fragment = name_fragment.strip().lower()
        found = []
        for e in result["eliminated"]:
            if fragment in e["name"].lower():
                found.append({"name": e["name"], "semantic_rank": e["semantic_rank"], "outcome": "removed",
                              "profile_source": e.get("profile_source"), "detail": e["eliminated_because"]})
        for place, v in enumerate(result["viable"], 1):
            if fragment in v["name"].lower():
                found.append({"name": v["name"], "semantic_rank": v["semantic_rank"], "outcome": "viable",
                              "profile_source": v.get("profile_source"),
                              "detail": f"passed every filter and ranked {place} of {len(result['viable'])} "
                                        f"viable; {v['why_viable']}"})
        found.sort(key=lambda f: f["semantic_rank"])
        if not found:
            return {"matches": [], "note": f"No organization with '{name_fragment}' in its name is among the "
                                           f"{len(candidates)} closest by meaning. It may not be in the corpus, or "
                                           "it is a poor semantic fit for this offer."}
        return {"matches": found[:5]}
    except WrongIdentity as exc:
        return {"error": {"code": "identity_refused", "message": str(exc)}}
    except Exception as exc:  # noqa: BLE001
        return {"error": {"code": "search_failed", "message": f"{type(exc).__name__}: {exc}"}}


def find_matches(
    search_text: str,
    hours_remaining: float,
    needs_cold: bool,
    pallets: float = 1.0,
    load_description: str = "surplus food",
    donor_description: str = "A local donor",
    top_k: int = 80,
    exclude_names: Optional[list[str]] = None,
    needs_frozen: bool = False,
) -> dict:
    """Find recipients for a posting and return the finished Match Brief, in one step.

    Searches wide on meaning, applies the hard filters (storage, capacity, the clock), ranks, looks up
    the top match's neighborhood and assembles the brief. The candidate rows stay inside this function
    on purpose: passing 80 profiles through the language model made each of its calls take over a minute.

    Args:
        search_text: The posting rewritten as plain language describing a good recipient (storage, kind
            of food, scale). This is what gets embedded for the semantic search.
        hours_remaining: Hours the food has left, already capped by the donor's own deadline.
        needs_cold: True if the food must stay cold.
        pallets: Size of the load in pallets (a crate-sized load is a fraction of 1).
        load_description: The load in a few words, e.g. "ten crates of spinach".
        donor_description: Who is giving it, e.g. "A grocer on the north side".
        top_k: Size of the semantic pool before filtering. Keep it wide.
        exclude_names: Recipients that have already said no (or are closed). They are skipped, so the brief is
            for the next best recipient. Use the exact names from the earlier brief.
        needs_frozen: True if the food must stay frozen (also pass needs_cold=True). Recipients without a freezer
            are removed.

    Returns:
        The brief from build_match_brief, plus `search` with the pool size and how many survived the
        filters. On failure: {"error": {"code", "message"}} where code is "identity_refused" or
        "search_failed". An empty result is not an error: it is a brief with `refusal` set.
    """
    from .identity_guard import WrongIdentity

    try:
        candidates = vector_candidates(search_text, top_k=top_k)
        if exclude_names:
            skip = {n.strip().lower() for n in exclude_names}
            candidates = [c for c in candidates if c["name"].strip().lower() not in skip]
        result = apply_constraints(candidates, hours_remaining, needs_cold, pallets, needs_frozen)
        neighborhood = None
        if result["viable"]:
            top = result["viable"][0]
            try:
                neighborhood = lookup_neighborhood(top["latitude"], top["longitude"])
            except WrongIdentity:
                raise
            except Exception:  # noqa: BLE001  (the brief is still useful without the tract figures)
                neighborhood = None
        brief = build_match_brief(
            search_text, hours_remaining, result["viable"], result["eliminated"],
            load_description=load_description, donor_description=donor_description,
            pallets=pallets, neighborhood=neighborhood)
        brief["search"] = {"candidates_searched": len(candidates),
                           "viable_after_filters": len(result["viable"])}
        return brief
    except WrongIdentity as exc:
        return {"error": {"code": "identity_refused", "message": str(exc)}}
    except Exception as exc:  # noqa: BLE001
        return {"error": {"code": "search_failed", "message": f"{type(exc).__name__}: {exc}"}}
