"""Executable test suite for the food_broker agent and tools.

Reads the structured test catalog in `agent/food_broker/test_questions.json` and validates:
  1. Catalog completeness: all 10 original surplus postings, all 9 planted teaching recipients,
     all demo/refusal guardrails, the 8-turn coordinator follow-up sequence, and MCP boundary cases.
  2. Offline deterministic unit checks: physical constraint filtering, domestic fridge 1-pallet limit,
     planted near-miss decoy rejection, contradictory profile handling, genuine ties, vocabulary
     mismatch, FoodKeeper 1-hour opened-container caution override, and 6-part Match Brief structure.
  3. Live BigQuery integration checks (parallelized via ThreadPoolExecutor): executes `find_matches`,
     `lookup_shelf_life`, `explain_candidate`, and the MCP walk-in query against the live `a4i_food`
     BigQuery dataset for every case in `test_questions.json`.
  4. Optional end-to-end ADK Agent LLM evaluation (`A4I_RUN_LIVE_AGENT=1` or `--live-agent`): runs
     coordinator prompts through `food_broker.agent.root_agent` and checks real-world response quality.

Run from repository root:
    PYTHONPATH=agent python3 -m unittest food_broker.test_suite -v
    PYTHONPATH=agent python3 -m food_broker.test_suite
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import sys
import unittest

# Configure lab defaults if not already set in the environment so a coding agent can run out of the box.
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-04-6c7101c1dba1")
os.environ.setdefault("A4I_EXPECTED_PROJECT", "qwiklabs-gcp-04-6c7101c1dba1")
os.environ.setdefault("A4I_EXPECTED_PRINCIPAL_SUFFIX", "@qwiklabs.net")
os.environ.setdefault("A4I_EXPECTED_PROJECT_NUMBER", "817377390808")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "true")
if "--live-agent" in sys.argv:
    os.environ["A4I_RUN_LIVE_AGENT"] = "1"
    sys.argv.remove("--live-agent")

from food_broker.identity_guard import WrongIdentity, assert_lab_identity
from food_broker.tools import (
    DATASET,
    DOMESTIC_FRIDGE_PALLETS,
    _client,
    _shelf_caution,
    apply_constraints,
    build_match_brief,
    explain_candidate,
    find_matches,
    lookup_shelf_life,
)

CATALOG_PATH = Path(__file__).resolve().parent / "test_questions.json"
SIX_BRIEF_PARTS = (
    "organization_and_why",
    "what_they_can_take",
    "the_clock",
    "whose_neighborhood",
    "outreach_message",
    "next_two_options",
)


def load_catalog() -> dict:
    with CATALOG_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _has_live_bq_credentials() -> bool:
    if os.environ.get("A4I_SKIP_LIVE_BQ") == "1":
        return False
    try:
        assert_lab_identity()
        return True
    except (WrongIdentity, Exception):  # noqa: BLE001
        return False


LIVE_BQ_AVAILABLE = _has_live_bq_credentials()


class TestCatalogIntegrity(unittest.TestCase):
    """Verifies that test_questions.json contains all original repo cases and functional guardrails."""

    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog()

    def test_all_10_original_surplus_postings_present(self):
        postings = self.catalog["original_surplus_postings"]
        self.assertEqual(len(postings), 10)
        ids = [p["posting_id"] for p in postings]
        self.assertEqual(ids, list(range(1, 11)))
        tracks = {p["track"] for p in postings}
        self.assertEqual(tracks, {"retail", "farm", "essentials"})

    def test_all_9_planted_recipients_present(self):
        planted = self.catalog["planted_teaching_cases"]
        all_recipients = [r for group in planted for r in group["recipients"]]
        expected = {
            "Greenline Community Pantry",
            "Harborview Neighbors Trust",
            "Anso Child Development",
            "Cedar Street Produce Alliance",
            "Maple Street Produce Alliance",
            "Ridgeway Avenue Food Ministry",
            "Southline Neighbors Pantry",
            "Third Ward Community Table",
            "Brookfield Family Resource Center",
            "Lakeshore Mutual Aid Collective",
        }
        self.assertTrue(expected.issubset(set(all_recipients)))

    def test_guardrails_followups_and_mcp_cases_present(self):
        self.assertGreaterEqual(len(self.catalog["demo_and_refusal_guardrails"]), 5)
        self.assertEqual(len(self.catalog["multi_turn_follow_ups"]), 8)
        self.assertEqual(len(self.catalog["mcp_and_scope_boundaries"]), 3)


class TestOfflinePlantedAndGuardrailCases(unittest.TestCase):
    """Fast, zero-cloud unit tests verifying physical constraint enforcement on planted & edge cases."""

    def _row(self, name, cold, pallets, lead, distance, **kw):
        return {
            "name": name,
            "cold_storage": cold,
            "frozen_storage": kw.get("frozen", False),
            "loading_dock": kw.get("dock", False),
            "refrigerated_transport": kw.get("transport", False),
            "max_pallets": pallets,
            "pickup_window_hours": lead,
            "weekly_households": kw.get("households", 200),
            "populations_served": kw.get("populations", "families, seniors"),
            "service_days": "Mon-Fri",
            "profile_text": kw.get("profile_text", f"{name} serves local families."),
            "street": "100 Main St",
            "city": "Chicago",
            "state": "IL",
            "zip_code": "60601",
            "latitude": 41.88,
            "longitude": -87.63,
            "distance": distance,
            "semantic_rank": kw.get("semantic_rank", 1),
        }

    def test_planted_near_miss_decoy_eliminated_and_shown_in_rejected(self):
        """PLANTED-01: Greenline Community Pantry ranks #1 by meaning for greens but has cold_storage='none'."""
        candidates = [
            self._row("Greenline Community Pantry", "none", 1, 12, 0.10, semantic_rank=1),
            self._row("Southline Neighbors Pantry", "walk-in", 3, 6, 0.20, semantic_rank=2),
            self._row("Third Ward Community Table", "domestic", 1, 4, 0.22, semantic_rank=3),
            self._row("Maple Street Produce Alliance", "walk-in", 10, 3, 0.28, transport=True, semantic_rank=4),
        ]
        res = apply_constraints(candidates, hours_remaining=6, needs_cold=True, pallets=0.5)
        viable_names = [v["name"] for v in res["viable"]]
        self.assertNotIn("Greenline Community Pantry", viable_names)
        brief = build_match_brief("10 crates of spinach", 6, res["viable"], res["eliminated"], pallets=0.5)
        rejected = {r["name"]: r for r in brief["rejected_but_close"]}
        self.assertIn("Greenline Community Pantry", rejected)
        self.assertIn("no cold storage", rejected["Greenline Community Pantry"]["because"])

    def test_planted_contradictory_profile_uses_structured_columns(self):
        """PLANTED-02: Harborview Neighbors Trust prose contradicts itself; structured columns decide."""
        harborview = self._row(
            "Harborview Neighbors Trust",
            "walk-in",
            6,
            12,
            0.15,
            frozen=True,
            profile_text=(
                "We operate a walk-in freezer and commercial cooler. "
                "We only have a single cupboard shelf and no freezer or cooler on site."
            ),
        )
        res = apply_constraints([harborview], hours_remaining=24, needs_cold=True, pallets=4)
        self.assertEqual(len(res["viable"]), 1)
        self.assertEqual(res["viable"][0]["margin_hours"], 12)

    def test_planted_genuine_ties_both_viable_and_ordered(self):
        """PLANTED-03: Cedar Street and Maple Street Produce Alliances have identical capabilities."""
        ties = [
            self._row("Cedar Street Produce Alliance", "walk-in", 10, 12, 0.21, dock=True, transport=True),
            self._row("Maple Street Produce Alliance", "walk-in", 10, 12, 0.21, dock=True, transport=True),
        ]
        res = apply_constraints(ties, hours_remaining=24, needs_cold=True, pallets=5)
        self.assertEqual([v["name"] for v in res["viable"]], [
            "Cedar Street Produce Alliance",
            "Maple Street Produce Alliance",
        ])

    def test_planted_vocabulary_mismatch_and_domestic_fridge_cutoff(self):
        """PLANTED-04 & GUARD-02: Domestic fridge accepts 0.5 pallets of cold food but rejects >1 pallet."""
        vocab_candidates = [
            self._row("Ridgeway Avenue Food Ministry", "walk-in", 3, 6, 0.18),
            self._row("Southline Neighbors Pantry", "walk-in", 3, 6, 0.19),
            self._row("Third Ward Community Table", "domestic", 3, 4, 0.12),
            self._row("Brookfield Family Resource Center", "walk-in", 3, 6, 0.22),
            self._row("Lakeshore Mutual Aid Collective", "commercial", 3, 6, 0.24),
        ]
        small_load = apply_constraints(vocab_candidates, hours_remaining=8, needs_cold=True, pallets=0.5)
        self.assertIn("Third Ward Community Table", [v["name"] for v in small_load["viable"]])

        multi_pallet_load = apply_constraints(
            vocab_candidates, hours_remaining=8, needs_cold=True, pallets=DOMESTIC_FRIDGE_PALLETS + 1
        )
        self.assertNotIn("Third Ward Community Table", [v["name"] for v in multi_pallet_load["viable"]])
        eliminated_reasons = {
            e["name"]: e["eliminated_because"] for e in multi_pallet_load["eliminated"]
        }
        self.assertIn("only a household fridge", eliminated_reasons["Third Ward Community Table"])

    def test_impossible_clock_and_over_capacity_produce_refusal(self):
        """GUARD-01 & GUARD-03: 1-hour deadline or 60-pallet load produces explicit refusal with closest rejections."""
        candidates = [
            self._row("Greenline Community Pantry", "none", 2, 12, 0.10, semantic_rank=1),
            self._row("Maple Street Produce Alliance", "walk-in", 10, 12, 0.20, semantic_rank=2),
            self._row("Greater Chicago Food Depository", "walk-in", 20, 36, 0.25, semantic_rank=3),
        ]
        one_hour = apply_constraints(candidates, hours_remaining=1, needs_cold=True, pallets=1)
        brief_1h = build_match_brief("40 trays of cream-filled pastries", 1, one_hour["viable"], one_hour["eliminated"])
        self.assertIsNone(brief_1h["organization_and_why"])
        self.assertIsNotNone(brief_1h["refusal"])
        self.assertEqual(len(brief_1h["rejected_but_close"]), 3)

        sixty_pallets = apply_constraints(candidates, hours_remaining=48, needs_cold=True, pallets=60)
        brief_60p = build_match_brief("60 pallets of frozen turkeys", 48, sixty_pallets["viable"], sixty_pallets["eliminated"], pallets=60)
        self.assertIsNone(brief_60p["organization_and_why"])
        self.assertIsNotNone(brief_60p["refusal"])

    def test_sealed_formula_opened_container_caution_trigger(self):
        """ORIG-08: Shelf life <= 2h triggers _shelf_caution so the agent uses the donor's sealed expiry."""
        caution = _shelf_caution(1.0)
        self.assertIsNotNone(caution)
        self.assertIn("opened container", caution)
        self.assertIsNone(_shelf_caution(168.0))


@unittest.skipUnless(LIVE_BQ_AVAILABLE, "Live BigQuery lab credentials not available")
class TestLiveBigQuerySuite(unittest.TestCase):
    """Runs all test cases in test_questions.json against the live BigQuery dataset in parallel."""

    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog()
        cls.posting_results = {}
        cls.guardrail_results = {}

        def run_posting(case):
            brief = find_matches(
                search_text=case["raw_posting_text"],
                hours_remaining=case["effective_hours_remaining"],
                needs_cold=case["needs_cold"],
                pallets=case["estimated_pallets"],
                load_description=case["raw_posting_text"],
            )
            shelf = lookup_shelf_life(case["foodkeeper_product"], case["storage_state"])
            return case["id"], {"brief": brief, "shelf": shelf, "case": case}

        def run_guardrail(case):
            brief = find_matches(
                search_text=case["search_text"],
                hours_remaining=case["hours_remaining"],
                needs_cold=case["needs_cold"],
                pallets=case["pallets"],
            )
            return case["id"], {"brief": brief, "case": case}

        with ThreadPoolExecutor(max_workers=8) as pool:
            for cid, data in pool.map(run_posting, cls.catalog["original_surplus_postings"]):
                cls.posting_results[cid] = data
            guardrails_with_bq = [
                g for g in cls.catalog["demo_and_refusal_guardrails"] if "expected_live_bq" in g
            ]
            for cid, data in pool.map(run_guardrail, guardrails_with_bq):
                cls.guardrail_results[cid] = data

    def test_all_10_original_surplus_postings_match_ground_truth(self):
        """Verifies ORIG-01 through ORIG-10 against live BigQuery vector search, constraints, and FoodKeeper."""
        for cid, entry in self.posting_results.items():
            with self.subTest(case_id=cid):
                case = entry["case"]
                brief = entry["brief"]
                shelf = entry["shelf"]
                expected = case["expected_live_bq"]

                self.assertNotIn("error", brief, f"{cid} returned error: {brief}")
                self.assertEqual(
                    brief["search"]["viable_after_filters"],
                    expected["viable_after_filters"],
                    f"{cid} viable count mismatch",
                )
                self.assertEqual(bool(brief.get("refusal")), expected["refusal"])
                self.assertEqual(
                    brief["organization_and_why"]["name"],
                    expected["top_match"],
                    f"{cid} top match mismatch",
                )
                self.assertEqual(
                    [r["name"] for r in brief["ranked"]],
                    expected["ranked_top_3"],
                    f"{cid} top-3 ranking mismatch",
                )
                for part in SIX_BRIEF_PARTS:
                    self.assertTrue(brief.get(part), f"{cid} missing Match Brief section: {part}")

                self.assertEqual(
                    shelf["hours"],
                    case["expected_shelf_life_hours"],
                    f"{cid} shelf life hours mismatch for {case['foodkeeper_product']}",
                )
                if cid == "ORIG-08":
                    self.assertIn("caution", shelf, "ORIG-08 Formula (pantry 1.0h) must include caution")

    def test_live_guardrail_cases_refusal_and_filtering(self):
        """Verifies GUARD-01 (1h pastries refusal), GUARD-02 (3p dairy domestic cutoff), GUARD-03 (60p refusal), GUARD-05 (halal)."""
        for cid, entry in self.guardrail_results.items():
            with self.subTest(case_id=cid):
                case = entry["case"]
                brief = entry["brief"]
                expected = case["expected_live_bq"]

                self.assertNotIn("error", brief)
                self.assertEqual(brief["search"]["viable_after_filters"], expected["viable_after_filters"])
                self.assertEqual(bool(brief.get("refusal")), expected["refusal"])
                if expected["refusal"]:
                    self.assertIsNone(brief["organization_and_why"])
                    self.assertGreaterEqual(
                        len(brief["rejected_but_close"]), expected["min_rejected_shown"]
                    )
                else:
                    self.assertEqual(brief["organization_and_why"]["name"], expected["top_match"])
                    if cid == "GUARD-02":
                        self.assertNotEqual(
                            brief["what_they_can_take"]["cold_storage"],
                            "domestic",
                            "3-pallet cold load must not match a household fridge",
                        )

    def test_multi_turn_follow_up_progression_and_explanations(self):
        """Verifies FOLLOWUP-01 through FOLLOWUP-05 on live BigQuery ('They said no' + 'Why not X')."""
        posting = "10 crates of spinach, harvested yesterday, needs cold storage"
        # Turn 1: initial match
        t1 = self.posting_results["ORIG-01"]["brief"]
        self.assertEqual(t1["organization_and_why"]["name"], "Shakespear Rose Community Table Incorporated")

        # Turn 2: "They said no. Who's next?"
        t2 = find_matches(
            search_text=posting,
            hours_remaining=6.0,
            needs_cold=True,
            pallets=0.5,
            exclude_names=["Shakespear Rose Community Table Incorporated"],
        )
        self.assertEqual(t2["organization_and_why"]["name"], "Love Of Angels")
        self.assertEqual(t2["next_two_options"][0]["name"], "Habibi Care")

        # Turn 3: "They said no too. Who's after that?"
        t3 = find_matches(
            search_text=posting,
            hours_remaining=6.0,
            needs_cold=True,
            pallets=0.5,
            exclude_names=["Shakespear Rose Community Table Incorporated", "Love Of Angels"],
        )
        self.assertEqual(t3["organization_and_why"]["name"], "Habibi Care")

        # Turn 4: "Why them and not Greenline Community Pantry?"
        t4 = explain_candidate("greenline", posting, 6.0, True, 0.5)
        self.assertEqual(len(t4["matches"]), 1)
        self.assertEqual(t4["matches"][0]["name"], "Greenline Community Pantry")
        self.assertEqual(t4["matches"][0]["semantic_rank"], 3)
        self.assertEqual(t4["matches"][0]["outcome"], "removed")
        self.assertIn("no cold storage", t4["matches"][0]["detail"])

        # Turn 5: "Why them and not the big food bank downtown?"
        t5_bank = explain_candidate("food bank", posting, 6.0, True, 0.5)
        self.assertEqual(t5_bank["matches"][0]["name"], "Americas Food Bank")
        self.assertEqual(t5_bank["matches"][0]["outcome"], "removed")

        t5_depo = explain_candidate("food depository", posting, 6.0, True, 0.5)
        self.assertEqual(t5_depo["matches"][0]["name"], "Greater Chicago Food Depository")
        self.assertEqual(t5_depo["matches"][0]["semantic_rank"], 29)
        self.assertEqual(t5_depo["matches"][0]["outcome"], "removed")
        self.assertIn("needs 36h to collect, food has 6h", t5_depo["matches"][0]["detail"])

    def test_mcp_walk_in_cold_storage_corpus_query(self):
        """Verifies MCP-01 ground truth: 13 of 192 recipients (6.8%) have walk-in cold storage."""
        sql = f"""
        SELECT
          COUNTIF(cold_storage = 'walk-in') AS walk_in_recipients,
          COUNT(*) AS total_recipients,
          ROUND(100.0 * COUNTIF(cold_storage = 'walk-in') / COUNT(*), 1) AS walk_in_pct
        FROM `{DATASET}.recipients`
        """
        row = dict(next(iter(_client().query(sql).result())))
        expected = self.catalog["mcp_and_scope_boundaries"][0]["expected_result"]
        self.assertEqual(row["walk_in_recipients"], expected["walk_in_recipients"])
        self.assertEqual(row["total_recipients"], expected["total_recipients"])
        self.assertAlmostEqual(float(row["walk_in_pct"]), expected["walk_in_pct"], places=1)


@unittest.skipUnless(
    os.environ.get("A4I_RUN_LIVE_AGENT") == "1",
    "Set A4I_RUN_LIVE_AGENT=1 (or pass --live-agent) to run end-to-end Gemini ADK agent evaluations",
)
class TestLiveAgentEndToEnd(unittest.TestCase):
    """End-to-end ADK InMemoryRunner tests validating the LLM agent's real-world coordinator answers."""

    @staticmethod
    def _ask_agent(prompts: list[str]) -> list[str]:
        from google.adk.runners import InMemoryRunner
        from google.genai import types
        from food_broker.agent import root_agent

        async def _run():
            runner = InMemoryRunner(agent=root_agent, app_name="food_broker_test")
            session = await runner.session_service.create_session(
                app_name="food_broker_test", user_id="coordinator"
            )
            replies = []
            for prompt in prompts:
                msg = types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
                chunks = []
                async for event in runner.run_async(
                    user_id="coordinator", session_id=session.id, new_message=msg
                ):
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                chunks.append(part.text)
                replies.append("".join(chunks))
            return replies

        return asyncio.run(_run())

    def test_missing_deadline_asks_clarifying_question(self):
        """GUARD-04: Agent must ask for the missing pickup deadline instead of guessing."""
        reply = self._ask_agent([
            "A grocer in Lincoln Park has 10 crates of fresh strawberries that need to stay cold. Who can take them?"
        ])[0].lower()
        self.assertTrue(
            any(w in reply for w in ("deadline", "hours", "when", "how long", "pickup", "collect")),
            f"Expected clarifying question about deadline, got: {reply}",
        )

    def test_impossible_clock_refuses_safely(self):
        """GUARD-01: Agent refuses 1-hour bakery posting and shows closest rejected candidates."""
        reply = self._ask_agent([
            "A bakery has 40 trays of cream-filled pastries that must stay refrigerated and leave their dock within 1 hour."
        ])[0].lower()
        self.assertTrue(
            any(w in reply for w in ("no recipient", "no candidate", "nobody", "cannot", "can't", "no viable", "none", "unable")),
            f"Expected explicit refusal for 1h clock, got: {reply}",
        )


if __name__ == "__main__":
    if "--live-agent" in sys.argv:
        os.environ["A4I_RUN_LIVE_AGENT"] = "1"
        sys.argv.remove("--live-agent")
    unittest.main(verbosity=2)
