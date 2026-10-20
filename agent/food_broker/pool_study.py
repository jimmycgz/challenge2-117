"""Reproduce the pool-size study: how many recipients survive the filters at each semantic pool size.

For the 6-hour spinach offer (half a pallet, must stay cold) it runs the search at several pool sizes, applies the same
filters as the agent, and prints how many recipients are viable and where in the search the first ones sit.

Needs the lab tables and the identity settings (see README.md). Run from the agent/ folder:
    python -m food_broker.pool_study
"""

from .tools import apply_constraints, vector_candidates

POSTING = "10 crates of spinach, harvested yesterday, needs cold storage"
HOURS, NEEDS_COLD, PALLETS = 6, True, 0.5
POOLS = (15, 40, 80)


def main():
    print(f"Posting: {POSTING!r}; clock {HOURS} h, {PALLETS:g} pallet, cold: {NEEDS_COLD}\n")
    print("| Pool (top_k) | Viable after filters | Meaning ranks of the first three viable |")
    print("|---|---|---|")
    for k in POOLS:
        out = apply_constraints(vector_candidates(POSTING, top_k=k), HOURS, NEEDS_COLD, PALLETS)
        ranks = sorted(v["semantic_rank"] for v in out["viable"])[:3]
        print(f"| {k} | {len(out['viable'])} | {', '.join(f'#{r}' for r in ranks) or 'none'} |")


if __name__ == "__main__":
    main()
