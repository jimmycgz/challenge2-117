"""Offline check of the constraint filter against the planted teaching cases. No cloud needed.

Run:  python -m food_broker.selfcheck   (from the agent/ directory)

Each check is built so it fails if the filter is removed or weakened.
"""

from food_broker.tools import apply_constraints, build_match_brief


def row(name, cold, pallets, lead, distance, **kw):
    return {"name": name, "cold_storage": cold, "max_pallets": pallets,
            "pickup_window_hours": lead, "distance": distance,
            "refrigerated_transport": kw.get("transport", False),
            "street": "", "city": "Chicago", "state": "IL", "zip_code": "",
            "latitude": 41.9, "longitude": -87.7}


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

    ok_pre = build_match_brief("x", 6, out["viable"], out["eliminated"], pallets=0.5)

    # Nothing viable must produce an explicit refusal, not a guess.
    none = apply_constraints(CANDIDATES, hours_remaining=1, needs_cold=True, pallets=0.5)
    brief = build_match_brief("10 crates of spinach", 1, none["viable"], none["eliminated"])
    assert brief["organization_and_why"] is None and brief["refusal"], brief
    assert brief["rejected_but_close"], "refusal must show the closest rejections"

    decoy = [r for r in ok_pre["rejected_but_close"] if r["name"] == "Greenline Community Pantry"]
    assert decoy and decoy[0]["semantic_rank"] == 1 and "no cold storage" in decoy[0]["because"], \
        "the no-cold-storage decoy must appear in rejected_but_close with its semantic rank"

    # The rule must do real work: put the no-cold-storage decoy at semantic rank 5, behind four recipients that fail
    # only on the clock. Without the rule the three nearest rejections would all be clock failures.
    far = [row(f"Slow{i}", "walk-in", 10, 24, 0.1 + i / 100) for i in range(4)] + [
        row("Looks Perfect But Warm", "none", 10, 2, 0.5)]
    far_out = apply_constraints(far, hours_remaining=6, needs_cold=True, pallets=0.5)
    far_brief = build_match_brief("x", 6, far_out["viable"], far_out["eliminated"], pallets=0.5)
    shown = {r["name"]: r for r in far_brief["rejected_but_close"]}
    assert "Looks Perfect But Warm" in shown, "a no-cold-storage rejection must always be shown when there is one"
    assert shown["Looks Perfect But Warm"]["semantic_rank"] == 5, shown
    assert len(far_brief["rejected_but_close"]) == 3

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

    # find_matches: the one-call path the agent uses. Search and neighborhood are faked here so the
    # wiring, the brief shape and the error shape are checked without a cloud project.
    import food_broker.tools as T

    real_search, real_nb = T.vector_candidates, T.lookup_neighborhood
    try:
        T.vector_candidates = lambda text, top_k=80: CANDIDATES
        T.lookup_neighborhood = lambda lat, lon: {"poverty_rate": 0.31, "no_vehicle_rate": 0.22,
                                                  "assistance_rate": 0.18}
        fm = T.find_matches("cold produce, small load", 6, True, 0.5,
                            load_description="ten crates of spinach",
                            donor_description="A grocer on the north side")
        assert "error" not in fm, fm
        assert [k for k in SIX if not fm.get(k)] == [], "find_matches brief is missing parts"
        assert [r["rank"] for r in fm["ranked"]] == [1, 2, 3]
        assert all("meaning_rank" in r for r in fm["ranked"] + fm["next_two_options"]), "cards need a meaning_rank field"
        assert fm["search"] == {"candidates_searched": 5, "viable_after_filters": 3}, fm["search"]
        assert "31%" in fm["whose_neighborhood"]["tract"]

        # "They said no": the declined recipient is skipped and the next one is briefed, and the remaining
        # recipients keep their original rank by meaning. Explaining "why not X" reports rank and reason.
        T.vector_candidates = lambda text, top_k=80: [dict(c, semantic_rank=i) for i, c in enumerate(CANDIDATES, 1)]
        first = T.find_matches("cold produce, small load", 6, True, 0.5)
        top = first["organization_and_why"]["name"]
        again = T.find_matches("cold produce, small load", 6, True, 0.5, exclude_names=[top])
        assert "error" not in again, again
        assert again["organization_and_why"]["name"] != top, "declined recipient was briefed again"
        assert top not in [r["name"] for r in again["ranked"]], "declined recipient still ranked"
        assert again["ranked"][0]["name"] == first["next_two_options"][0]["name"], "next recipient is not rank 2"
        cedar = [r for r in again["rejected_but_close"] if r["name"] == "Cedar Street Produce Alliance"]
        assert not cedar or cedar[0]["semantic_rank"] == 4, "excluding a recipient changed other ranks by meaning"
        everyone = T.find_matches("x", 6, True, 0.5, exclude_names=[c["name"] for c in CANDIDATES])
        assert everyone["refusal"], "with everyone declined the brief must refuse, not invent a match"

        why = T.explain_candidate("greenline", "cold produce, small load", 6, True, 0.5)["matches"]
        assert why and why[0]["outcome"] == "removed" and why[0]["semantic_rank"] == 1, why
        assert "no cold storage" in why[0]["detail"], why
        ok_one = T.explain_candidate("maple street", "x", 6, True, 0.5)["matches"]
        assert ok_one and ok_one[0]["outcome"] == "viable", ok_one
        gone = T.explain_candidate("no such organization", "x", 6, True, 0.5)
        assert gone["matches"] == [] and "note" in gone, gone

        def boom(text, top_k=80):
            raise RuntimeError("bigquery unavailable")
        T.vector_candidates = boom
        err = T.find_matches("x", 6, True)
        assert err == {"error": {"code": "search_failed",
                                 "message": "RuntimeError: bigquery unavailable"}}, err

        def refused_search(text, top_k=80):
            raise WrongIdentity("wrong account")
        T.vector_candidates = refused_search
        err = T.find_matches("x", 6, True)
        assert err["error"]["code"] == "identity_refused", err
    finally:
        T.vector_candidates, T.lookup_neighborhood = real_search, real_nb

    from food_broker.tools import _shelf_caution
    assert _shelf_caution(1.0) and _shelf_caution(2.0), "a 1 or 2 hour shelf life must carry a caution"
    assert _shelf_caution(168.0) is None and _shelf_caution(None) is None

    # Shelf life: an exact entry wins; with none, the closest entries are returned for the caller to choose from.
    from food_broker.tools import shape_shelf_result
    exact = shape_shelf_result("Lettuce", "refrigerated", [
        {"product_name": "Lettuce", "product_subtitle": "leaf", "hours": 168.0, "note": "ok", "is_exact": True},
        {"product_name": "Bagged greens", "product_subtitle": "leaf, spinach", "hours": 120.0, "note": "ok",
         "is_exact": False}])
    assert exact["hours"] == 168.0 and "closest" not in exact, exact
    near = shape_shelf_result("Spinach", "refrigerated", [
        {"product_name": "Bagged greens", "product_subtitle": "leaf, spinach, lettuce", "hours": 120.0, "note": "ok",
         "is_exact": False},
        {"product_name": "Lettuce", "product_subtitle": "leaf, spinach", "hours": 168.0, "note": "ok",
         "is_exact": False}])
    assert near["hours"] is None and [c["product_name"] for c in near["closest"]] == ["Bagged greens", "Lettuce"], near
    assert shape_shelf_result("Zzz", "pantry", [])["hours"] is None
    short = shape_shelf_result("Formula", "pantry", [
        {"product_name": "Formula", "product_subtitle": "", "hours": 1.0, "note": "ok", "is_exact": True}])
    assert "caution" in short, "a 1-hour exact figure must still carry the caution"

    # profile_source reaches the brief, the rejections and the explanation, so a planted teaching case can be labelled.
    planted = dict(row("Invented Teaching Case", "walk-in", 10, 2, 0.05), profile_source="planted")
    real = dict(row("Real Organization", "walk-in", 10, 3, 0.10), profile_source="generated")
    pout = apply_constraints([planted, real], hours_remaining=6, needs_cold=True, pallets=0.5)
    pb = build_match_brief("x", 6, pout["viable"], pout["eliminated"], pallets=0.5)
    assert pb["organization_and_why"]["profile_source"] == "planted", pb["organization_and_why"]
    assert [r["profile_source"] for r in pb["ranked"]] == ["planted", "generated"], pb["ranked"]
    import food_broker.tools as T2
    keep = T2.vector_candidates
    try:
        T2.vector_candidates = lambda text, top_k=80: [dict(planted, semantic_rank=1)]
        ex = T2.explain_candidate("invented", "x", 6, True, 0.5)["matches"]
        assert ex and ex[0]["profile_source"] == "planted", ex
    finally:
        T2.vector_candidates = keep

    # A person whose credentials come from the metadata server (Cloud Shell, Workbench) is reported with their own email as
    # the "service account email". They must be judged as a user, by the account suffix, not by the service-account rules.
    from food_broker.identity_guard import _principal_of

    class MetadataCreds:  # what google-auth returns in Cloud Shell
        service_account_email = "student-00-abc@labs.example"

    class ServiceAccountCreds:
        service_account_email = "svc@some-project.iam.gserviceaccount.com"

    assert _principal_of(MetadataCreds()) == ("student-00-abc@labs.example", False, False), _principal_of(MetadataCreds())
    assert _principal_of(ServiceAccountCreds())[1] is True, "a real service account must still be judged as one"

    # The decision, not only the classifier: a metadata-reported user whose address is not the lab's is still refused,
    # including a lookalike that ends in the suffix without the at-sign.
    class OutsiderCreds:  # a Cloud Shell user on some other organisation
        service_account_email = "someone@other.example"

    class LookalikeCreds:
        service_account_email = "evil@notlabs.example"

    def decide(creds):  # the guard's two steps: classify the credential, then decide
        who, is_sa, impersonated = _principal_of(creds)
        return refused(who, P, is_sa, P, S, impersonated=impersonated)

    for creds in (OutsiderCreds(), LookalikeCreds()):
        assert decide(creds), f"metadata user outside the lab accepted: {creds.service_account_email}"
    assert not decide(MetadataCreds()), "metadata user inside the lab refused"

    # Frozen food: a walk-in cooler with no freezer is removed when the food must stay frozen, and kept when it need not.
    two = [
        {"name": "Cooler only", "cold_storage": "walk-in", "frozen_storage": False, "max_pallets": 4, "pickup_window_hours": 2},
        {"name": "Has freezer", "cold_storage": "walk-in", "frozen_storage": True, "max_pallets": 4, "pickup_window_hours": 2},
    ]
    frozen = apply_constraints(two, hours_remaining=24, needs_cold=True, pallets=1, needs_frozen=True)
    assert [v["name"] for v in frozen["viable"]] == ["Has freezer"], frozen["viable"]
    assert "no freezer" in frozen["eliminated"][0]["eliminated_because"], frozen["eliminated"]
    chilled = apply_constraints(two, hours_remaining=24, needs_cold=True, pallets=1)
    assert len(chilled["viable"]) == 2, "freezer required for food that only needs to be chilled"

    print("selfcheck passed:", len(CANDIDATES), "candidates,", len(viable), "viable for spinach")


if __name__ == "__main__":
    main()
