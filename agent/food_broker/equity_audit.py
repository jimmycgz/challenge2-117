"""Equity audit: where did the matcher send the food, compared with where the need is?

Runs the matcher (search, filters, ranking, without the language model) over the ten postings in
`surplus_postings` and looks up the census tract nearest each top match. It then compares the matches with:

  1. the metro: every tract in the loaded area, each tract weighted by its population
  2. every recipient in the corpus, each at the tract nearest its ZIP-level point (one row per recipient)
  3. the same recipients split into those with a loading dock or room for 5+ pallets, and the rest
  4. the top matches counted three ways: once per posting, once per distinct recipient, and weighted by the
     estimated size of each load

The matches are counted three ways because one recipient can win several postings, and the large loads are few
but carry most of the volume. Race and ethnicity are not in the data and are not used.

Needs the lab tables and the settings in README.md. Run from the agent/ folder:
    python -m food_broker.equity_audit
"""

import statistics

from .tools import DATASET, _client, apply_constraints, lookup_neighborhood, vector_candidates

# The postings table has no load size. Pallets per posting are estimates, written down here so anyone can
# change them and see the audit move. Keyed by posting_id (the notebook's order).
PALLETS = {1: 0.5, 2: 1, 3: 2, 4: 0.5, 5: 5, 6: 10, 7: 15, 8: 2, 9: 1, 10: 0.5}
# The table's clock for posting 8 (sealed infant formula, 8 months to expiry) was a shelf-life figure of 1 hour:
# the loader took FoodKeeper's opened-container figure. The audit uses the donor's own 168 hours instead and
# prints both, so the override is visible in the output.
CLOCK_OVERRIDE = {8: 168}
DEFAULT_HOURS = 24  # used only if the table has no clock for a posting; printed if it ever applies
DOCK_PALLETS = 5    # a recipient with a loading dock or at least this many pallets of room counts as large
RATES = ("poverty_rate", "no_vehicle_rate", "assistance_rate")


def _postings() -> list[dict]:
    sql = f"""SELECT posting_id, track, posting_text, storage_state, hours_remaining
              FROM `{DATASET}.surplus_postings` ORDER BY posting_id"""
    return [dict(r) for r in _client().query(sql).result()]


def _metro() -> tuple[dict, int]:
    parts = ",\n".join(
        f"SAFE_DIVIDE(SUM({r} * total_pop), SUM(IF({r} IS NULL, NULL, total_pop))) AS {r}" for r in RATES)
    sql = f"SELECT {parts}, COUNT(*) AS tracts FROM `{DATASET}.tract_demographics`"
    row = dict(next(iter(_client().query(sql).result())))
    return row, row.pop("tracts")


def _corpus() -> list[dict]:
    """One row per recipient: its size fields and the tract whose internal point is nearest its ZIP point."""
    sql = f"""
    SELECT r.recipient_id, r.loading_dock, r.max_pallets,
           ARRAY_AGG(t ORDER BY ST_DISTANCE(
             ST_GEOGPOINT(t.tract_lon, t.tract_lat), ST_GEOGPOINT(r.longitude, r.latitude)) LIMIT 1)[OFFSET(0)] AS t
    FROM `{DATASET}.recipients` r
    CROSS JOIN (SELECT * FROM `{DATASET}.tract_demographics`
                WHERE tract_lat IS NOT NULL AND tract_lon IS NOT NULL) t
    WHERE r.latitude IS NOT NULL AND r.longitude IS NOT NULL
    GROUP BY r.recipient_id, r.loading_dock, r.max_pallets"""
    out = []
    for row in _client().query(sql).result():
        d = dict(row["t"])
        d.update(recipient_id=row["recipient_id"], large=bool(row["loading_dock"])
                 or (row["max_pallets"] or 0) >= DOCK_PALLETS)
        out.append(d)
    return out


def _vals(rows: list[dict], key: str) -> list[float]:
    return [r[key] for r in rows if r.get(key) is not None]


def _mean(rows: list[dict], key: str, weights: list[float] | None = None):
    pairs = [(r[key], (weights[i] if weights else 1)) for i, r in enumerate(rows) if r.get(key) is not None]
    if not pairs:
        return None
    return sum(v * w for v, w in pairs) / sum(w for _, w in pairs)


def _median(rows: list[dict], key: str):
    v = _vals(rows, key)
    return statistics.median(v) if v else None


def _pct(x) -> str:
    return "n/a" if x is None else f"{x:.0%}"


def _row(label: str, n, rows: list[dict], how: str = "mean", weights: list[float] | None = None) -> str:
    fn = _median if how == "median" else _mean
    cells = [fn(rows, r, weights) if how == "mean" else fn(rows, r) for r in RATES]
    return f"| {label} | {n} | " + " | ".join(_pct(c) for c in cells) + " |"


def main():
    metro, n_tracts = _metro()
    corpus = _corpus()
    corpus_tract_ids = {r["geo_id"] for r in corpus}

    print("| # | Track | Table clock (h) | Clock used (h) | Pallets (est.) | Viable | Top match | Cold | Pallets of room "
          "| Collects in (h) | Tract poverty | No vehicle | Assistance |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    chosen, chosen_ids, pallets_used = [], [], []
    refused = []
    for p in _postings():
        pid = p["posting_id"]
        needs_cold = p["storage_state"] == "refrigerated"
        pallets = PALLETS.get(pid, 1)
        table_clock = p["hours_remaining"]
        hours = CLOCK_OVERRIDE.get(pid, table_clock if table_clock is not None else DEFAULT_HOURS)
        out = apply_constraints(vector_candidates(p["posting_text"], top_k=80), hours, needs_cold, pallets)
        viable = len(out["viable"])
        if not viable:
            refused.append(pid)
            print(f"| {pid} | {p['track']} | {table_clock} | {hours} | {pallets} | 0 | nobody viable | | | | | | |")
            continue
        top = out["viable"][0]
        tract = lookup_neighborhood(top["latitude"], top["longitude"])
        chosen.append(tract)
        chosen_ids.append(top["recipient_id"])
        pallets_used.append(pallets)
        print(f"| {pid} | {p['track']} | {table_clock} | {hours} | {pallets:g} | {viable} | {top['name'][:28]} | "
              f"{top['cold_storage']} | {top['max_pallets']} | {top['pickup_window_hours']} | "
              f"{_pct(tract.get('poverty_rate'))} | {_pct(tract.get('no_vehicle_rate'))} | "
              f"{_pct(tract.get('assistance_rate'))} |")

    # One tract row per distinct recipient, first win kept.
    seen, distinct = set(), []
    for rid, tr in zip(chosen_ids, chosen):
        if rid not in seen:
            seen.add(rid)
            distinct.append(tr)
    large = [r for r in corpus if r["large"]]
    small = [r for r in corpus if not r["large"]]

    print(f"\nMetro: {n_tracts} tracts in the loaded area. Corpus: {len(corpus)} recipients on "
          f"{len(corpus_tract_ids)} distinct tracts.\n")
    print("| Group | n | Poverty | No vehicle | Assistance |")
    print("|---|---|---|---|---|")
    print(f"| Metro, tracts weighted by population | {n_tracts} tracts | "
          + " | ".join(_pct(metro[r]) for r in RATES) + " |")
    print(_row("All recipients, mean", len(corpus), corpus))
    print(_row("All recipients, median", len(corpus), corpus, "median"))
    print(_row(f"Recipients with a dock or {DOCK_PALLETS}+ pallets, mean", len(large), large))
    print(_row(f"Recipients with a dock or {DOCK_PALLETS}+ pallets, median", len(large), large, "median"))
    print(_row("All other recipients, mean", len(small), small))
    print(_row("All other recipients, median", len(small), small, "median"))
    print(_row("Top matches, once per posting, mean", len(chosen), chosen))
    print(_row("Top matches, once per posting, median", len(chosen), chosen, "median"))
    print(_row("Top matches, once per distinct recipient, mean", len(distinct), distinct))
    print(_row("Top matches, once per distinct recipient, median", len(distinct), distinct, "median"))
    print(_row(f"Top matches, weighted by estimated pallets ({sum(pallets_used):g} total)", len(chosen), chosen,
               "mean", pallets_used))
    if refused:
        print(f"\nPostings with nobody viable: {refused}")
    print(f"\nClock overrides: {CLOCK_OVERRIDE}. Pallet sizes are estimates (PALLETS in equity_audit.py). "
          "The audit searches with the raw posting text; the deployed agent searches with a rewrite the language "
          "model writes, so this audits the matcher, not that exact query. Tracts are the nearest tract by internal "
          "point to a ZIP-level location, so they describe the surrounding area.")


if __name__ == "__main__":
    main()
