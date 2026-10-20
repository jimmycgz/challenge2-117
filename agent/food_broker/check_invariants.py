"""Check the hard constraints hold on every recommended recipient, for all ten postings in the lab table.

The product goal is that the agent never recommends a recipient that cannot store the food, hold the load or collect
in time. This runs the search and the filters for each posting and checks that every recipient left standing meets
every constraint, and that every candidate was either kept or removed with a reason (none silently lost).

Needs the lab tables and the identity settings (see README.md). Run from the agent/ folder:
    python -m food_broker.check_invariants
Exit code 0 only if every check passes.
"""

import sys

from .equity_audit import CLOCK_OVERRIDE, PALLETS, _postings
from .tools import DOMESTIC_FRIDGE_PALLETS, REAL_COLD, apply_constraints, vector_candidates


def violations_for(viable: list[dict], needs_cold: bool, pallets: float, hours: float) -> list[str]:
    bad = []
    for v in viable:
        name = v["name"]
        if needs_cold and v.get("cold_storage") == "none":
            bad.append(f"{name}: recommended with no cold storage")
        if needs_cold and v.get("cold_storage") == "domestic" and pallets > DOMESTIC_FRIDGE_PALLETS:
            bad.append(f"{name}: household fridge for {pallets:g} pallets")
        if (v.get("max_pallets") or 0) < pallets:
            bad.append(f"{name}: room for {v.get('max_pallets')} pallets, load is {pallets:g}")
        lead = v.get("pickup_window_hours")
        if lead is not None and lead > hours:
            bad.append(f"{name}: needs {lead:g}h to collect, food has {hours:g}h")
    return bad


def main() -> int:
    failures = 0
    print("| # | Track | Candidates | Viable | Removed | Cold-storage removals | Violations |")
    print("|---|---|---|---|---|---|---|")
    for p in _postings():
        pid = p["posting_id"]
        needs_cold = p["storage_state"] == "refrigerated"
        pallets = PALLETS.get(pid, 1)
        hours = CLOCK_OVERRIDE.get(pid, p["hours_remaining"])
        cands = vector_candidates(p["posting_text"], top_k=80)
        out = apply_constraints(cands, hours, needs_cold, pallets)
        bad = violations_for(out["viable"], needs_cold, pallets, hours)
        lost = len(cands) - len(out["viable"]) - len(out["eliminated"])
        if lost:
            bad.append(f"{lost} candidates were neither kept nor removed")
        if any(not e.get("eliminated_because") for e in out["eliminated"]):
            bad.append("a removed candidate has no reason")
        cold_removed = sum("no cold storage" in e["eliminated_because"] for e in out["eliminated"])
        failures += len(bad)
        print(f"| {pid} | {p['track']} | {len(cands)} | {len(out['viable'])} | {len(out['eliminated'])} | "
              f"{cold_removed} | {len(bad)} |")
        for line in bad:
            print(f"  VIOLATION posting {pid}: {line}")
    print(f"\n{'PASS' if not failures else 'FAIL'}: {failures} violations across the ten postings "
          f"(recipients counted as cold: {sorted(REAL_COLD)} plus domestic for one pallet or less).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
