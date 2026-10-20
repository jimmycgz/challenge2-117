"""One corpus, three tracks: run one posting from each track through the same vector search.

The challenge's claim is that matching on meaning handles every track with a single corpus, where a
rule-based system needs a rulebook per track. This prints the top candidates for a retail, a farm
and a critical-essentials posting, and shows which ones the constraint filter then removes.

Needs the lab tables and the identity settings (see README.md). Run from the agent/ folder:
    python -m food_broker.demo_tracks
"""

from .tools import apply_constraints, vector_candidates

# (track, posting, needs_cold, pallets, hours_remaining). Postings are the notebook's own.
POSTINGS = [
    ("retail", "10 crates of spinach, harvested yesterday, needs cold storage", True, 0.5, 6),
    ("farm", "5 tons of potatoes still in the field, we can load pallets if someone collects",
     False, 5, 72),
    ("essentials", "48 cases of sealed infant formula, 8 months to expiry", False, 2, 168),
]


def main():
    for track, text, needs_cold, pallets, hours in POSTINGS:
        cands = vector_candidates(text, top_k=15)
        out = apply_constraints(cands, hours, needs_cold, pallets)
        print(f"\n[{track}] {text}")
        print(f"  semantic candidates: {len(cands)}   viable after constraints: {len(out['viable'])}")
        for v in out["viable"][:3]:
            print(f"  + {v['name']} ({v['cold_storage']}, {v['max_pallets']} pallets, "
                  f"margin {v['margin_hours']}h)")
        for e in out["eliminated"][:2]:
            print(f"  - {e['name']}: {e['eliminated_because']}")


if __name__ == "__main__":
    main()
