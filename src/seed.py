from datetime import date
from typing import Optional

from engine import CRSEngine
from models import (
    ActorRole,
    Claim,
    Concept,
    Entity,
    EpistemicLink,
    EpistemicState,
    Event,
    Polarity,
    ProvenanceNode,
    Source,
    TemporalWindow,
    VectorAttachment,
)


def build_demo_crs(db_path: Optional[str] = "ecos_crs.db") -> CRSEngine:
    """Seeds all 10 Acceptance Test Cases from ECOS CRS v0.1 Section 89."""
    crs = CRSEngine(db_path=db_path)

    # Sources
    crs.add_source(Source("src_a", "person", "Witness A", "unverified"))
    crs.add_source(Source("src_b", "person", "Witness B", "unverified"))
    crs.add_source(
        Source("doc_bio", "document", "Zoology Reference 2024", "peer-reviewed")
    )

    # Test 1 & 2: Language-independent Concepts & Entities
    crs.add_concept(
        Concept(
            "concept_person",
            "PERSON",
            labels={"en": ("person",), "hi": ("व्यक्ति",)},
        )
    )
    crs.add_concept(
        Concept(
            "concept_apple",
            "APPLE",
            labels={"en": ("apple",), "hi": ("सेब",), "gu": ("સફરજન",)},
        )
    )
    crs.add_concept(
        Concept(
            "concept_dog",
            "DOG",
            labels={"en": ("dog",), "hi": ("कुत्ता",)},
        )
    )
    crs.add_concept(
        Concept(
            "concept_car",
            "CAR",
            labels={
                "en": ("car", "automobile"),
                "hi": ("कार",),
                "gu": ("કાર",),
                "fr": ("automobile",),
            },
        )
    )
    crs.add_concept(
        Concept(
            "concept_bird_v1",
            "BIRD",
            version=1,
            labels={"en": ("bird",), "hi": ("पक्षी",)},
            defaults=("can-fly",),
        )
    )

    crs.add_entity(Entity("ent_john", "concept_person", ("John",)))
    crs.add_entity(Entity("ent_mary", "concept_person", ("Mary",)))
    crs.add_entity(Entity("ent_car_001", "concept_car", ("Car_001",)))
    crs.add_entity(Entity("ent_apple_01", "concept_apple", ("Apple_01",)))
    crs.add_entity(Entity("ent_dog_001", "concept_dog", ("Dog_001",)))

    # Test 3: Relation (John owns Car_001)
    crs.add_claim(
        Claim(
            id="clm_owns_001",
            subject_id="ent_john",
            relation="owns",
            object_value="ent_car_001",
            epistemic_state=EpistemicState.SUPPORTED,
            source_id="src_a",
        )
    )

    # Test 5: Event (John gave Mary an apple)
    crs.add_event(
        Event(
            id="evt_give_001",
            event_type="GIVING",
            participants={
                "giver": "ent_john",
                "receiver": "ent_mary",
                "object": "ent_apple_01",
            },
            temporal=TemporalWindow(
                valid_from=date(2026, 5, 1), valid_to=date(2026, 5, 1)
            ),
            source_id="src_a",
        )
    )

    # Test 4 & 6: Property + Temporal Change (Red Jan-Jun -> Blue Jul-Present)
    crs.add_claim(
        Claim(
            id="clm_color_h1",
            subject_id="ent_car_001",
            relation="color",
            object_value="red",
            epistemic_state=EpistemicState.OBSERVED,
            source_id="src_a",
            temporal=TemporalWindow(
                valid_from=date(2026, 1, 1), valid_to=date(2026, 6, 30)
            ),
        )
    )
    crs.add_claim(
        Claim(
            id="clm_color_h2",
            subject_id="ent_car_001",
            relation="color",
            object_value="blue",
            epistemic_state=EpistemicState.OBSERVED,
            source_id="src_b",
            temporal=TemporalWindow(valid_from=date(2026, 7, 1), valid_to=None),
        )
    )

    # Test 7: Contradiction Preservation (Both claims retained)
    crs.add_claim(
        Claim(
            id="clm_conflict_red",
            subject_id="ent_car_001",
            relation="incident_color",
            object_value="red",
            epistemic_state=EpistemicState.CONTESTED,
            source_id="src_a",
            temporal=TemporalWindow(
                valid_from=date(2026, 9, 10), valid_to=date(2026, 9, 10)
            ),
            uncertainty={"conflict": "high"},
        )
    )
    crs.add_claim(
        Claim(
            id="clm_conflict_blue",
            subject_id="ent_car_001",
            relation="incident_color",
            object_value="blue",
            epistemic_state=EpistemicState.CONTESTED,
            source_id="src_b",
            temporal=TemporalWindow(
                valid_from=date(2026, 9, 10), valid_to=date(2026, 9, 10)
            ),
            uncertainty={"conflict": "high"},
        )
    )
    crs.link_claims(
        EpistemicLink(
            id="lnk_contra_01",
            relation="contradicts",
            from_id="clm_conflict_red",
            to_id="clm_conflict_blue",
            note="Simultaneous conflicting witness reports",
        )
    )

    # Test 8: Explicit UNKNOWN (Unknown != False)
    crs.add_claim(
        Claim(
            id="clm_second_car",
            subject_id="ent_john",
            relation="owns_second_car",
            object_value=True,
            epistemic_state=EpistemicState.UNKNOWN,
            polarity=Polarity.UNKNOWN,
            uncertainty={"completeness": "insufficient_evidence"},
        ),
        actor=ActorRole.COGNITIVE_SUPERVISOR,
    )

    # Test 9: Provenance Chain (Document -> Observation -> Claim -> Inference)
    crs.add_provenance(
        ProvenanceNode(
            "obs_01",
            "observation",
            "Read: All mammals are warm-blooded",
            ("doc_bio",),
        )
    )
    crs.add_provenance(
        ProvenanceNode(
            "clm_prem_01",
            "claim",
            "Premise: Dog_001 is a mammal",
            ("obs_01",),
        )
    )
    crs.add_provenance(
        ProvenanceNode(
            "inf_01",
            "inference",
            "Derived: Dog_001 is warm-blooded",
            ("clm_prem_01",),
        ),
        actor=ActorRole.REASONING_ENGINE,
    )
    crs.add_claim(
        Claim(
            id="clm_dog_wb",
            subject_id="ent_dog_001",
            relation="thermoregulation",
            object_value="warm-blooded",
            epistemic_state=EpistemicState.INFERRED,
            source_id="doc_bio",
            provenance_id="inf_01",
        ),
        actor=ActorRole.REASONING_ENGINE,
    )

    # Test 10: Non-Destructive Concept Evolution (Bird v1 -> Bird v2)
    crs.refine_concept(
        old_id="concept_bird_v1",
        new_id="concept_bird_v2",
        defaults=("usually-can-fly",),
        exceptions=("penguin:cannot-fly", "ostrich:cannot-fly"),
        reason="Flightless bird exceptions discovered",
    )

    # Vector Attachments (Secondary to symbolic identity)
    crs.attach_vector(
        VectorAttachment("vec_1", "concept_car", "demo-embed-v1", (0.94, 0.12, 0.28))
    )
    crs.attach_vector(
        VectorAttachment("vec_2", "concept_bird_v2", "demo-embed-v1", (0.11, 0.92, 0.30))
    )
    return crs
