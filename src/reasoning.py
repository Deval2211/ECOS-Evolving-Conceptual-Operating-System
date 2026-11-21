from datetime import date
from typing import Dict, List
import uuid

from engine import CRSEngine
from models import (
    ActorRole,
    Claim,
    Entity,
    EpistemicLink,
    EpistemicState,
    Polarity,
    ProvenanceNode,
    TemporalWindow,
)


def windows_overlap(a: TemporalWindow, b: TemporalWindow) -> bool:
    """Return True if two temporal windows overlap in time."""
    start_a = a.valid_from or date.min
    end_a = a.valid_to or date.max
    start_b = b.valid_from or date.min
    end_b = b.valid_to or date.max
    return start_a <= end_b and start_b <= end_a


class ReasoningEngine:
    """
    Phase 2 ECOS Reasoning Engine (Sections 23, 27, 35, 69).
    Operates strictly outside CRSEngine and writes back only as ActorRole.REASONING_ENGINE.
    """

    UNTRUSTED_STATES = {
        EpistemicState.UNKNOWN,
        EpistemicState.REJECTED,
        EpistemicState.CONTESTED,
    }

    def __init__(self, crs: CRSEngine) -> None:
        self.crs = crs

    def run_all(self) -> Dict[str, object]:
        """Run all reasoning passes and return a summary of derived knowledge."""
        default_inferences = self.apply_concept_defaults()
        rule_inferences = self.apply_deductive_rules()
        detected_conflicts = self.detect_contradictions()

        all_inferences = default_inferences + rule_inferences
        return {
            "inferences_added": len(all_inferences),
            "contradictions_detected": len(detected_conflicts),
            "default_inferences": default_inferences,
            "rule_inferences": rule_inferences,
            "conflict_links": detected_conflicts,
        }

    # --- Pass 1: Default & Exception Inheritance (Section 35 & 83) ---
    def apply_concept_defaults(self) -> List[str]:
        created: List[str] = []

        for ent in list(self.crs.entities.values()):
            concept = self.crs.concepts.get(ent.concept_id)
            if not concept or (not concept.defaults and not concept.exceptions):
                continue

            ent_tokens = {ent.id.lower(), *(lbl.lower() for lbl in ent.labels)}
            matched_exceptions = [
                ex
                for ex in concept.exceptions
                if ex.split(":", 1)[0].strip().lower() in ent_tokens
            ]

            # If an explicit exception matches this entity, apply the exception instead of defaults
            if matched_exceptions:
                for exc in matched_exceptions:
                    trait = exc.split(":", 1)[1].strip() if ":" in exc else exc
                    claim_id = f"inf_exc_{ent.id}_{trait}"
                    if claim_id in self.crs.claims:
                        continue

                    prov_id = f"prov_{uuid.uuid4().hex[:6]}"
                    self.crs.add_provenance(
                        ProvenanceNode(
                            id=prov_id,
                            kind="inference",
                            summary=f"Exception override '{exc}' from {concept.id} applied to {ent.id}",
                            derived_from=(),
                        ),
                        actor=ActorRole.REASONING_ENGINE,
                    )
                    self.crs.add_claim(
                        Claim(
                            id=claim_id,
                            subject_id=ent.id,
                            relation="inferred_trait",
                            object_value=trait,
                            epistemic_state=EpistemicState.INFERRED,
                            polarity=Polarity.POSITIVE,
                            provenance_id=prov_id,
                            uncertainty={"derivation": "exception_override"},
                        ),
                        actor=ActorRole.REASONING_ENGINE,
                    )
                    created.append(claim_id)
                continue

            # Otherwise inherit concept defaults
            for default_trait in concept.defaults:
                claim_id = f"inf_def_{ent.id}_{default_trait}"
                if claim_id in self.crs.claims:
                    continue

                prov_id = f"prov_{uuid.uuid4().hex[:6]}"
                self.crs.add_provenance(
                    ProvenanceNode(
                        id=prov_id,
                        kind="inference",
                        summary=f"Default trait '{default_trait}' inherited from {concept.id}",
                        derived_from=(),
                    ),
                    actor=ActorRole.REASONING_ENGINE,
                )
                self.crs.add_claim(
                    Claim(
                        id=claim_id,
                        subject_id=ent.id,
                        relation="inferred_trait",
                        object_value=default_trait,
                        epistemic_state=EpistemicState.INFERRED,
                        polarity=Polarity.POSITIVE,
                        provenance_id=prov_id,
                        uncertainty={"derivation": "default_inheritance"},
                    ),
                    actor=ActorRole.REASONING_ENGINE,
                )
                created.append(claim_id)

        return created

    # --- Pass 2: Deductive Rules with Full Provenance (Section 23 & 69) ---
    def apply_deductive_rules(self) -> List[str]:
        created: List[str] = []

        # Rule A: Ownership implies responsibility (only from trusted positive claims)
        for claim in list(self.crs.claims.values()):
            if claim.relation != "owns":
                continue
            if claim.epistemic_state in self.UNTRUSTED_STATES:
                continue
            if claim.polarity != Polarity.POSITIVE:
                continue

            derived_id = f"inf_resp_{claim.subject_id}_{claim.object_value}"
            if derived_id in self.crs.claims:
                continue

            premise_prov_id = f"prov_prem_{claim.id}"
            if premise_prov_id not in self.crs.provenance:
                parents = tuple(
                    p for p in (claim.provenance_id, claim.source_id) if p and p in self.crs.provenance
                )
                self.crs.add_provenance(
                    ProvenanceNode(
                        id=premise_prov_id,
                        kind="claim",
                        summary=f"Premise {claim.id}: {claim.subject_id} owns {claim.object_value}",
                        derived_from=parents,
                    ),
                    actor=ActorRole.REASONING_ENGINE,
                )

            inf_prov_id = f"prov_inf_{uuid.uuid4().hex[:6]}"
            self.crs.add_provenance(
                ProvenanceNode(
                    id=inf_prov_id,
                    kind="inference",
                    summary=f"Rule (owns -> responsible_for): {claim.subject_id} is responsible for {claim.object_value}",
                    derived_from=(premise_prov_id,),
                ),
                actor=ActorRole.REASONING_ENGINE,
            )
            self.crs.add_claim(
                Claim(
                    id=derived_id,
                    subject_id=claim.subject_id,
                    relation="responsible_for",
                    object_value=claim.object_value,
                    epistemic_state=EpistemicState.INFERRED,
                    polarity=Polarity.POSITIVE,
                    source_id=claim.source_id,
                    temporal=claim.temporal,
                    provenance_id=inf_prov_id,
                    uncertainty={"derivation": "ownership_rule"},
                ),
                actor=ActorRole.REASONING_ENGINE,
            )
            created.append(derived_id)

        # Rule B: Hospital admission event implies patient was located at that facility during that window
        for evt in list(self.crs.events.values()):
            if evt.event_type != "ADMISSION":
                continue
            patient = evt.participants.get("patient")
            facility = evt.participants.get("facility")
            if not patient or not facility:
                continue

            derived_id = f"inf_admit_{patient}_{facility}"
            if derived_id in self.crs.claims:
                continue

            evt_prov_id = f"prov_evt_{evt.id}"
            if evt_prov_id not in self.crs.provenance:
                parents = (evt.source_id,) if evt.source_id in self.crs.provenance else ()
                self.crs.add_provenance(
                    ProvenanceNode(
                        id=evt_prov_id,
                        kind="observation",
                        summary=f"Event {evt.id}: {patient} admitted to {facility}",
                        derived_from=parents,
                    ),
                    actor=ActorRole.REASONING_ENGINE,
                )

            inf_prov_id = f"prov_inf_{uuid.uuid4().hex[:6]}"
            self.crs.add_provenance(
                ProvenanceNode(
                    id=inf_prov_id,
                    kind="inference",
                    summary=f"Rule (ADMISSION -> located_at): {patient} located at {facility}",
                    derived_from=(evt_prov_id,),
                ),
                actor=ActorRole.REASONING_ENGINE,
            )
            self.crs.add_claim(
                Claim(
                    id=derived_id,
                    subject_id=patient,
                    relation="located_at",
                    object_value=facility,
                    epistemic_state=EpistemicState.INFERRED,
                    polarity=Polarity.POSITIVE,
                    source_id=evt.source_id,
                    temporal=evt.temporal,
                    provenance_id=inf_prov_id,
                    uncertainty={"derivation": "event_rule"},
                ),
                actor=ActorRole.REASONING_ENGINE,
            )
            created.append(derived_id)

        return created

    # --- Pass 3: Automatic Contradiction Scanner (Section 27 & 81) ---
    def detect_contradictions(self) -> List[str]:
        existing_pairs = {
            frozenset((link.from_id, link.to_id))
            for link in self.crs.epistemic_links
            if link.relation == "contradicts"
        }
        claims = list(self.crs.claims.values())
        detected: List[str] = []

        for i in range(len(claims)):
            for j in range(i + 1, len(claims)):
                a, b = claims[i], claims[j]

                if a.subject_id != b.subject_id or a.relation != b.relation:
                    continue
                if a.object_value == b.object_value and a.polarity == b.polarity:
                    continue
                if EpistemicState.UNKNOWN in (a.epistemic_state, b.epistemic_state):
                    continue
                if EpistemicState.REJECTED in (a.epistemic_state, b.epistemic_state):
                    continue
                # Non-overlapping time intervals are temporal changes, NOT contradictions
                if not windows_overlap(a.temporal, b.temporal):
                    continue

                pair_key = frozenset((a.id, b.id))
                if pair_key in existing_pairs:
                    continue

                link_id = f"lnk_auto_{uuid.uuid4().hex[:6]}"
                self.crs.link_claims(
                    EpistemicLink(
                        id=link_id,
                        relation="contradicts",
                        from_id=a.id,
                        to_id=b.id,
                        note=(
                            f"Auto-detected overlapping conflict on {a.subject_id}.{a.relation}: "
                            f"{a.object_value} vs {b.object_value}"
                        ),
                    ),
                    actor=ActorRole.REASONING_ENGINE,
                )
                existing_pairs.add(pair_key)
                detected.append(link_id)

        return detected


if __name__ == "__main__":
    from extra_data import load_extended_data
    from seed import build_demo_crs

    crs = build_demo_crs(db_path=None)
    load_extended_data(crs)

    # Add two birds to demonstrate Default vs. Exception inheritance live
    crs.add_entity(Entity("ent_sparrow", "concept_bird_v2", ("Sparrow",)))
    crs.add_entity(Entity("ent_penguin", "concept_bird_v2", ("Penguin",)))

    # Add an unlinked overlapping conflict to demonstrate auto-contradiction detection
    crs.add_claim(
        Claim("clm_john_loc_1", "ent_john", "city", "Ahmedabad", EpistemicState.REPORTED, source_id="src_a")
    )
    crs.add_claim(
        Claim("clm_john_loc_2", "ent_john", "city", "Mumbai", EpistemicState.REPORTED, source_id="src_b")
    )

    reasoner = ReasoningEngine(crs)
    report = reasoner.run_all()

    print("=== ECOS Phase 2: Reasoning Engine Report ===")
    print(f"New inferred claims added      : {report['inferences_added']}")
    print(f"New contradictions detected    : {report['contradictions_detected']}")
    print("\n--- Derived Claims ---")
    for cid in report["default_inferences"] + report["rule_inferences"]:
        c = crs.claims[cid]
        trace = " <- ".join(f"{n.kind}({n.id})" for n in crs.trace_provenance(c.provenance_id or ""))
        print(f"  [{c.epistemic_state.value}] {c.subject_id}.{c.relation} = {c.object_value}")
        print(f"      Provenance: {trace}")

    print("\n--- Auto-Detected Contradictions ---")
    for lid in report["conflict_links"]:
        link = next(l for l in crs.epistemic_links if l.id == lid)
        print(f"  {link.from_id} <--> {link.to_id} | {link.note}")
