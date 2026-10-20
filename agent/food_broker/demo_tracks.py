"""One corpus, three tracks: run one posting from each track through the same vector search.

The challenge's claim is that matching on meaning handles every track with a single corpus, where a rule-based
system needs a rulebook per track. This prints, for a retail, a farm and an essentials posting, who the filters kept
and which close semantic matches they removed, each with its rank by meaning and the profile text that made it look
right. A recipient that ranks high by meaning and is removed for having no cold storage is the case where the search
alone would have been wrong.

Needs the lab tables and the identity settings (see README.md). Run from the agent/ folder:
    python -m food_broker.demo_tracks
"""

from .tools import _pallets, apply_constraints, vector_candidates

# (track, posting, needs_cold, pallets, hours_remaining). Postings are the notebook's own.
POSTINGS = [
    ("retail", "10 crates of spinach, harvested yesterday, needs cold storage", True, 0.5, 6),
    ("farm", "5 tons of potatoes still in the field, we can load pallets if someone collects",
     False, 5, 72),
    ("essentials", "48 cases of sealed infant formula, 8 months to expiry", False, 2, 168),
]


def main():
    for track, text, needs_cold, pallets, hours in POSTINGS:
        cands = vector_candidates(text, top_k=80)
        out = apply_constraints(cands, hours, needs_cold, pallets)
        print(f"\n[{track}] {text}")
        print(f"  semantic candidates: {len(cands)}   viable after constraints: {len(out['viable'])}")
        for pick, v in enumerate(out["viable"][:3], 1):
            print(f"  + agent's pick {pick}: {v['name']} (meaning rank #{v['semantic_rank']}, "
                  f"{v['cold_storage']}, room for {_pallets(v['max_pallets'])}, margin {v['margin_hours']}h)")
        if out["viable"]:
            nearest = min(out["viable"], key=lambda v: v["semantic_rank"])
            print(f"  = nearest by meaning that passed the filters: {nearest['name']} "
                  f"(meaning rank #{nearest['semantic_rank']}, {nearest['cold_storage']}, "
                  f"room for {_pallets(nearest['max_pallets'])}, margin {nearest['margin_hours']}h)")
        cold = [e for e in out["eliminated"] if "no cold storage" in e["eliminated_because"]]
        shown = sorted(cold[:1] + [e for e in out["eliminated"] if e not in cold[:1]][:2],
                       key=lambda e: e["semantic_rank"])
        for e in shown:
            print(f"  - removed: {e['name']} (meaning rank #{e['semantic_rank']}): {e['eliminated_because']}")
            if "no cold storage" in e["eliminated_because"]:
                print(f"      its profile reads: \"{e['profile_text'][:150]}...\"")


if __name__ == "__main__":
    main()
