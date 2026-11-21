from datetime import date

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
    Source,
    TemporalWindow,
    VectorAttachment,
)


def load_extended_data(crs: CRSEngine) -> None:
    """Adds real-world multilingual, scientific, medical, and tech knowledge."""

    # Sources
    crs.add_source(Source("src_iau", "organization", "IAU Resolution 2006", "authoritative"))
    crs.add_source(Source("src_dr_patel", "person", "Dr. Patel (MD)", "high"))
    crs.add_source(Source("src_dr_mehta", "person", "Dr. Mehta (MD)", "high"))
    crs.add_source(Source("src_sensor_med", "sensor", "Ward-4 Digital Thermometer", "calibrated"))

    # Multilingual Concepts
    crs.add_concept(
        Concept(
            "concept_water",
            "WATER",
            labels={"en": ("water", "H2O"), "hi": ("पानी", "जल"), "gu": ("પાણી",), "fr": ("eau",)},
        )
    )
    crs.add_concept(
        Concept(
            "concept_city",
            "CITY",
            labels={"en": ("city", "metropolis"), "hi": ("शहर", "नगर"), "gu": ("શહેર",)},
        )
    )
    crs.add_concept(
        Concept(
            "concept_hospital",
            "HOSPITAL",
            labels={"en": ("hospital", "clinic"), "hi": ("अस्पताल",), "gu": ("હોસ્પિટલ",)},
        )
    )
    crs.add_concept(
        Concept(
            "concept_phone",
            "SMARTPHONE",
            labels={"en": ("smartphone", "mobile", "phone"), "hi": ("फ़ोन", "मोबाइल"), "gu": ("મોબાઇલ",)},
        )
    )
    crs.add_concept(
        Concept(
            "concept_ai",
            "ARTIFICIAL_INTELLIGENCE",
            labels={
                "en": ("AI", "artificial intelligence", "cognitive system"),
                "hi": ("कृत्रिम बुद्धिमत्ता",),
                "gu": ("કૃત્રિમ બુદ્ધિમત્તા",),
            },
        )
    )

    # Polysemy Showcase ("Java" -> 3 distinct Concepts)
    crs.add_concept(
        Concept("concept_java_lang", "JAVA_PROGRAMMING_LANGUAGE", labels={"en": ("java", "jvm language")})
    )
    crs.add_concept(
        Concept("concept_java_coffee", "JAVA_COFFEE", labels={"en": ("java", "java coffee", "espresso")})
    )
    crs.add_concept(
        Concept("concept_java_island", "JAVA_ISLAND", labels={"en": ("java", "java island", "indonesia")})
    )

    # Scientific Concept Evolution: PLANET v1 -> PLANET v2
    crs.add_concept(
        Concept(
            "concept_planet_v1",
            "PLANET",
            version=1,
            labels={"en": ("planet",), "hi": ("ग्रह",), "gu": ("ગ્રહ",)},
            defaults=("orbits-sun", "spherical"),
        )
    )
    crs.refine_concept(
        old_id="concept_planet_v1",
        new_id="concept_planet_v2",
        defaults=("orbits-sun", "spherical", "clears-orbital-neighborhood"),
        exceptions=("pluto:reclassified-as-dwarf-planet",),
        reason="IAU 2006 planetary definition refinement",
    )

    # Entities
    crs.add_entity(Entity("ent_pluto", "concept_planet_v2", ("Pluto",)))
    crs.add_entity(Entity("ent_aarav", "concept_person", ("Aarav",)))
    crs.add_entity(Entity("ent_ahmedabad", "concept_city", ("Ahmedabad", "અમદાવાદ")))
    crs.add_entity(Entity("ent_civil_hosp", "concept_hospital", ("Civil Hospital",)))
    crs.add_entity(Entity("ent_ecos", "concept_ai", ("ECOS v0.1",)))

    # Temporal Showcase: Pluto 1930-2006 vs 2006-Present
    crs.add_claim(
        Claim(
            "clm_pluto_1930",
            "ent_pluto",
            "classification",
            "planet",
            EpistemicState.ACCEPTED,
            source_id="src_iau",
            temporal=TemporalWindow(valid_from=date(1930, 2, 18), valid_to=date(2006, 8, 23)),
        )
    )
    crs.add_claim(
        Claim(
            "clm_pluto_2006",
            "ent_pluto",
            "classification",
            "dwarf_planet",
            EpistemicState.ACCEPTED,
            source_id="src_iau",
            temporal=TemporalWindow(valid_from=date(2006, 8, 24), valid_to=None),
        )
    )

    # Medical Domain: Event + Sensor Observation + Contradiction + Unknown
    crs.add_event(
        Event(
            "evt_hospital_admit",
            "ADMISSION",
            {"patient": "ent_aarav", "facility": "ent_civil_hosp", "city": "ent_ahmedabad"},
            TemporalWindow(valid_from=date(2026, 11, 18), valid_to=date(2026, 11, 21)),
            "src_dr_patel",
        )
    )
    crs.add_claim(
        Claim(
            "clm_aarav_temp",
            "ent_aarav",
            "body_temperature",
            "39.2 C",
            EpistemicState.OBSERVED,
            source_id="src_sensor_med",
            temporal=TemporalWindow(valid_from=date(2026, 11, 18), valid_to=date(2026, 11, 19)),
        )
    )
    crs.add_claim(
        Claim(
            "clm_diag_viral",
            "ent_aarav",
            "diagnosis",
            "Viral Fever",
            EpistemicState.HYPOTHESIZED,
            source_id="src_dr_patel",
            uncertainty={"clinical": "pending_blood_panel"},
        )
    )
    crs.add_claim(
        Claim(
            "clm_diag_dengue",
            "ent_aarav",
            "diagnosis",
            "Dengue Fever",
            EpistemicState.HYPOTHESIZED,
            source_id="src_dr_mehta",
            uncertainty={"clinical": "pending_ns1_test"},
        )
    )
    crs.link_claims(
        EpistemicLink(
            "lnk_contra_med",
            "contradicts",
            "clm_diag_viral",
            "clm_diag_dengue",
            "Competing differential diagnoses preserved until lab confirmation",
        )
    )
    crs.add_claim(
        Claim(
            "clm_aarav_allergy",
            "ent_aarav",
            "allergic_to_penicillin",
            True,
            epistemic_state=EpistemicState.UNKNOWN,
            polarity=Polarity.UNKNOWN,
            uncertainty={"safety": "never_assume_false"},
        ),
        actor=ActorRole.COGNITIVE_SUPERVISOR,
    )

    # ECOS Self-Representation Claim
    crs.add_claim(
        Claim(
            "clm_ecos_loc",
            "ent_ecos",
            "developed_in",
            "ent_ahmedabad",
            EpistemicState.OBSERVED,
            source_id="src_a",
        )
    )

    # Extra Vectors
    crs.attach_vector(VectorAttachment("vec_3", "concept_water", "demo-embed-v1", (0.20, 0.30, 0.91)))
    crs.attach_vector(VectorAttachment("vec_4", "concept_ai", "demo-embed-v1", (0.88, 0.15, 0.44)))
    crs.attach_vector(VectorAttachment("vec_5", "concept_planet_v2", "demo-embed-v1", (0.14, 0.85, 0.48)))
