import json
import os
import unittest
from io import BytesIO
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.error import HTTPError

from engine import CRSAuthError, CRSInvariantError
from evolution import ConceptEvolutionEngine
from extra_data import load_extended_data
from language_adapter import LanguageAdapter
from server import _load_dotenv
from models import ActorRole, Claim, Entity, EpistemicState, Polarity
from reasoning import ReasoningEngine
from seed import build_demo_crs
from supervisor import CognitiveSupervisor


class TestECOSCRS(unittest.TestCase):
    def setUp(self) -> None:
        self.crs = build_demo_crs(db_path=None)

    def test_01_language_independent_concepts(self) -> None:
        gujarati = self.crs.find_concepts("કાર")
        hindi = self.crs.find_concepts("कार")
        self.assertEqual([c.id for c in gujarati], ["concept_car"])
        self.assertEqual([c.id for c in hindi], ["concept_car"])

    def test_02_entities_distinct_from_concepts(self) -> None:
        self.assertIn("ent_car_001", self.crs.entities)
        self.assertEqual(
            self.crs.entities["ent_car_001"].concept_id, "concept_car"
        )

    def test_03_event_representation(self) -> None:
        evt = self.crs.events["evt_give_001"]
        self.assertEqual(evt.participants["giver"], "ent_john")
        self.assertEqual(evt.participants["receiver"], "ent_mary")

    def test_04_temporal_change_non_destructive(self) -> None:
        mar = [
            c.object_value
            for c in self.crs.query_claims(
                "ent_car_001", "color", valid_on=date(2026, 3, 15)
            )
        ]
        aug = [
            c.object_value
            for c in self.crs.query_claims(
                "ent_car_001", "color", valid_on=date(2026, 8, 15)
            )
        ]
        self.assertEqual(mar, ["red"])
        self.assertEqual(aug, ["blue"])

    def test_05_contradiction_preservation(self) -> None:
        pairs = self.crs.get_contradictions()
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0]["claim_a"].object_value, "red")
        self.assertEqual(pairs[0]["claim_b"].object_value, "blue")

    def test_06_unknown_not_false_invariant(self) -> None:
        unk = self.crs.claims["clm_second_car"]
        self.assertEqual(unk.epistemic_state, EpistemicState.UNKNOWN)
        self.assertEqual(unk.polarity, Polarity.UNKNOWN)
        with self.assertRaises(CRSInvariantError):
            self.crs.add_claim(
                Claim(
                    "clm_bad",
                    "ent_john",
                    "owns_boat",
                    True,
                    EpistemicState.UNKNOWN,
                    Polarity.NEGATIVE,
                )
            )

    def test_07_provenance_traversal(self) -> None:
        chain = [n.id for n in self.crs.trace_provenance("inf_01")]
        self.assertEqual(chain, ["inf_01", "clm_prem_01", "obs_01", "doc_bio"])

    def test_08_non_destructive_concept_evolution(self) -> None:
        self.assertIn("concept_bird_v1", self.crs.concepts)
        self.assertIn("concept_bird_v2", self.crs.concepts)
        self.assertIn(
            "penguin:cannot-fly", self.crs.concepts["concept_bird_v2"].exceptions
        )

    def test_09_aee_write_blocked(self) -> None:
        with self.assertRaises(CRSAuthError):
            self.crs.add_claim(
                Claim(
                    "clm_aee",
                    "ent_john",
                    "hacked",
                    True,
                    EpistemicState.REPORTED,
                ),
                actor=ActorRole.AEE,
            )

    def test_10_vector_search_isolated(self) -> None:
        hits = self.crs.vector_search((0.90, 0.15, 0.25), model="demo-embed-v1")
        self.assertEqual(hits[0]["object_id"], "concept_car")

    def test_11_reasoning_defaults_exceptions_and_conflicts(self) -> None:
        load_extended_data(self.crs)
        self.crs.add_entity(Entity("ent_sparrow", "concept_bird_v2", ("Sparrow",)))
        self.crs.add_entity(Entity("ent_penguin", "concept_bird_v2", ("Penguin",)))
        self.crs.add_claim(
            Claim("clm_loc_a", "ent_john", "city", "Ahmedabad", EpistemicState.REPORTED, source_id="src_a")
        )
        self.crs.add_claim(
            Claim("clm_loc_b", "ent_john", "city", "Mumbai", EpistemicState.REPORTED, source_id="src_b")
        )

        report = ReasoningEngine(self.crs).run_all()
        self.assertGreater(report["inferences_added"], 0)
        self.assertEqual(self.crs.claims["inf_def_ent_sparrow_usually-can-fly"].object_value, "usually-can-fly")
        self.assertEqual(self.crs.claims["inf_exc_ent_penguin_cannot-fly"].object_value, "cannot-fly")
        self.assertEqual(len(report["conflict_links"]), 1)

    def test_12_cognitive_supervisor_flags_safety_unknowns(self) -> None:
        load_extended_data(self.crs)
        ReasoningEngine(self.crs).run_all()
        sup = CognitiveSupervisor(self.crs).review()

        self.assertGreaterEqual(sup["contradictions_reviewed"], 2)
        safety_alerts = [
            u for u in sup["unknown_reports"] if u["claim_id"] == "clm_aarav_allergy"
        ]
        self.assertEqual(len(safety_alerts), 1)
        self.assertEqual(safety_alerts[0]["priority"], "HIGH_SAFETY")

    def test_dotenv_loads_values_without_overriding_shell_environment(self) -> None:
        with TemporaryDirectory() as directory:
            env_file = Path(directory) / ".env"
            env_file.write_text(
                "GROQ_API_KEY='test-placeholder'\n"
                "GROQ_MODEL=qwen/qwen3.8-27b # model\n",
                encoding="utf-8",
            )
            with patch.dict("os.environ", {"GROQ_MODEL": "shell-model"}):
                os.environ.pop("GROQ_API_KEY", None)
                _load_dotenv(env_file)
                self.assertEqual(os.environ["GROQ_API_KEY"], "test-placeholder")
                self.assertEqual(os.environ["GROQ_MODEL"], "shell-model")

    def test_chat_extracts_and_deduplicates_concepts_and_entities(self) -> None:
        extracted = {
            "reply": "Ada Lovelace was a mathematician.",
            "concepts": [{"canonical": "MATHEMATICIAN", "labels": ["mathematician"]}],
            "entities": [{"name": "Ada Lovelace", "concept": "MATHEMATICIAN"}],
        }
        api_response = {
            "choices": [{"message": {"content": json.dumps(extracted)}}]
        }
        first_message = "Tell me about Ada Lovelace, a mathematician."

        with patch.dict("os.environ", {"GROQ_API_KEY": "test-key"}):
            with patch(
                "language_adapter.urllib.request.urlopen",
                side_effect=[
                    BytesIO(json.dumps(api_response).encode("utf-8")),
                    BytesIO(json.dumps(api_response).encode("utf-8")),
                ],
            ) as urlopen:
                adapter = LanguageAdapter(self.crs)
                first = adapter.chat(first_message)
                second = adapter.chat(
                    "Can you tell me more?",
                    [
                        {"role": "user", "content": first_message},
                        {"role": "assistant", "content": first["reply"]},
                    ],
                )

        concept_id = first["added"]["concepts"][0]["id"]
        entity_id = first["added"]["entities"][0]["id"]
        self.assertEqual(self.crs.entities[entity_id].concept_id, concept_id)
        self.assertEqual(second["added"], {"concepts": [], "entities": []})
        sent_body = json.loads(urlopen.call_args_list[1].args[0].data)
        self.assertEqual(sent_body["messages"][-3]["content"], first_message)

    def test_chat_redacts_api_key_from_provider_errors(self) -> None:
        api_key = "test-secret-key"
        error_body = json.dumps(
            {"error": {"message": f"Invalid credential {api_key}"}}
        ).encode("utf-8")
        provider_error = HTTPError(
            "https://api.groq.com/openai/v1/chat/completions",
            400,
            "Bad Request",
            {},
            BytesIO(error_body),
        )

        with patch.dict("os.environ", {"GROQ_API_KEY": api_key}):
            with patch(
                "language_adapter.urllib.request.urlopen",
                side_effect=provider_error,
            ):
                with self.assertRaises(RuntimeError) as raised:
                    LanguageAdapter(self.crs).chat("Hello")

        self.assertIn("Invalid credential [redacted]", str(raised.exception))
        self.assertNotIn(api_key, str(raised.exception))

    def test_13_concept_evolution_learns_and_splits_polysemy(self) -> None:
        load_extended_data(self.crs)
        evo = ConceptEvolutionEngine(self.crs).run_evolution()

        self.assertGreater(evo["learned_claims_added"], 0)
        self.assertIn("concept_polysemy_java", self.crs.concepts)
        split_edges = [e for e in self.crs.lineage if e.operation == "SPLIT"]
        self.assertGreaterEqual(len(split_edges), 3)


if __name__ == "__main__":
    unittest.main()
