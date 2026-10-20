"""Offline check of the constraint filter against the planted teaching cases. No cloud needed.

Run:  python -m food_broker.selfcheck   (from the agent/ directory)

Each check is built so it fails if the filter is removed or weakened.
"""

from food_broker.tools import apply_constraints, build_match_brief


def row(name, cold, pallets, lead, distance, **kw):
    return {"name": name, "cold_storage": cold, "max_pallets": pallets,
            "pickup_window_hours": lead, "distance": distance,
            "refrigerated_transport": kw.get("transport", False),
            "street": "", "city": "Chicago", "state": "IL", "zip_code": ""}


CANDIDATES = [
    # Semantically perfect, physically useless: the near-miss decoy.
    row("Greenline Community Pantry", "none", 1, 12, 0.10),
    row("Southline Neighbors Pantry", "walk-in", 3, 6, 0.20),
    row("Third Ward Community Table", "domestic", 1, 4, 0.22),
    row("Cedar Street Produce Alliance", "walk-in", 10, 24, 0.25),
    row("Maple Street Produce Alliance", "walk-in", 10, 3, 0.31, transport=True),
]


def main():
    # Ten crates of spinach: under one pallet, cold, 6 hours left.
    out = apply_constraints(CANDIDATES, hours_remaining=6, needs_cold=True, pallets=0.5)
    viable = [v["name"] for v in out["viable"]]
    rejected = {e["name"]: e["eliminated_because"] for e in out["eliminated"]}

    assert "Greenline Community Pantry" not in viable, "decoy with no cold storage got through"
    assert "no cold storage" in rejected["Greenline Community Pantry"]
    assert "Cedar Street Produce Alliance" not in viable, "24h collection lead beat a 6h clock"
    assert viable[0] == "Maple Street Produce Alliance", viable  # largest margin, own transport
    assert "Third Ward Community Table" in viable  # household fridge is fine for half a pallet

    # A five-pallet load: the household fridge must now drop out.
    big = apply_constraints(CANDIDATES, hours_remaining=48, needs_cold=True, pallets=5)
    assert "Third Ward Community Table" not in [v["name"] for v in big["viable"]]

    # Nothing viable must produce an explicit refusal, not a guess.
    none = apply_constraints(CANDIDATES, hours_remaining=1, needs_cold=True, pallets=0.5)
    brief = build_match_brief("10 crates of spinach", 1, none["viable"], none["eliminated"])
    assert brief["organization_and_why"] is None and brief["refusal"], brief
    assert brief["rejected_but_close"], "refusal must show the closest rejections"

    # The Match Brief on the challenge sheet: six labelled parts, and three ranked options.
    SIX = ["organization_and_why", "what_they_can_take", "the_clock", "whose_neighborhood",
           "outreach_message", "next_two_options"]
    ok = build_match_brief(
        "10 crates of spinach", 6, out["viable"], out["eliminated"],
        load_description="ten crates of spinach", donor_description="A grocer on the north side",
        pallets=0.5,
        neighborhood={"poverty_rate": 0.31, "no_vehicle_rate": 0.22, "assistance_rate": 0.18})
    missing = [k for k in SIX if not ok.get(k)]
    assert not missing, f"Match Brief is missing parts: {missing}"
    assert [r["rank"] for r in ok["ranked"]] == [1, 2, 3], ok["ranked"]
    assert len(ok["next_two_options"]) == 2, "need exactly the next two options"
    assert ok["organization_and_why"]["name"] == ok["ranked"][0]["name"] == "Maple Street Produce Alliance"
    assert ok["organization_and_why"]["name"] in ok["outreach_message"]
    assert "31%" in ok["whose_neighborhood"]["tract"], "neighborhood figures not carried into the brief"
    assert ok["the_clock"]["margin_hours"] is not None
    assert ok["refusal"] is None
    # A missing neighborhood must be said, not silently dropped.
    nb = build_match_brief("x", 6, out["viable"], out["eliminated"], pallets=0.5)
    assert "not looked up" in nb["whose_neighborhood"]["tract"]

    # Identity guard: the decision function must refuse the wrong principal, the wrong project, and
    # missing configuration, and accept only the lab's. Names below are made up.
    from food_broker.identity_guard import WrongIdentity, check_identity

    def refused(*args, **kwargs):
        try:
            check_identity(*args, **kwargs)
        except WrongIdentity:
            return True
        return False

    P, S = "lab-project-1", "@labs.example"
    assert refused("someone@other-org.example", P, False, P, S), "wrong principal accepted"
    assert refused("student@labs.example", "other-project", False, P, S), "wrong project accepted"
    assert refused("sa@other.iam.gserviceaccount.com", "other-project", True, P, S), "foreign SA accepted"
    # Impersonated credentials are refused even when the email looks like the lab's.
    assert refused(f"svc@{P}.iam.gserviceaccount.com", P, True, P, S, impersonated=True), \
        "impersonated credentials accepted"
    # The compute account passes only with the project number given, and only that number.
    NUM = "123456789"
    compute = f"{NUM}-compute@developer.gserviceaccount.com"
    assert refused(compute, P, True, P, S), "compute SA accepted with no project number configured"
    assert refused(f"999-compute@developer.gserviceaccount.com", P, True, P, S, project_number=NUM), \
        "another project's compute SA accepted"
    assert "service account" in check_identity(compute, P, True, P, S, project_number=NUM)
    # An allowlisted address passes; one that merely resembles it does not.
    assert "service account" in check_identity("ok@x.iam.gserviceaccount.com", P, True, P, S,
                                               sa_allowlist=("ok@x.iam.gserviceaccount.com",))
    assert refused("ok@y.iam.gserviceaccount.com", P, True, P, S,
                   sa_allowlist=("ok@x.iam.gserviceaccount.com",)), "non-listed SA accepted"
    assert refused("student@labs.example", P, False, "", S), "unset expected project accepted"
    assert refused("student@labs.example", P, False, P, ""), "unset suffix accepted"
    # SBX's hole: GOOGLE_CLOUD_PROJECT forces the resolved project to the lab's, so a foreign
    # service account must still be refused on its EMAIL, not on the project it resolved to.
    assert refused("impersonated-sa@employer-proj.iam.gserviceaccount.com", P, True, P, S), \
        "foreign service account accepted because the project env var was set to the lab"
    assert "student@labs.example" in check_identity("student@labs.example", P, False, P, S)
    assert "service account" in check_identity(f"svc@{P}.iam.gserviceaccount.com", P, True, P, S)

    print("selfcheck passed:", len(CANDIDATES), "candidates,", len(viable), "viable for spinach")


if __name__ == "__main__":
    main()
