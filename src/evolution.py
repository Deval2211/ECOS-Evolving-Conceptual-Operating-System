import uuid
from typing import Dict, List, Tuple

from engine import CRSEngine
from models import (
    ActorRole,
    Claim,
    Concept,
    EpistemicState,
    LineageEdge,
    Polarity,
    ProvenanceNode,
)


class ConceptEvolutionEngine:
    """
    Phases 4 & 5 ECOS Learning & Concept Evolution Engine (Sections 39-45, 71-72).
    Learns recurring patterns from CRS claims/events and performs non-destructive
    concept refinements or splits while preserving prior versions and lineage edges.
    """

    def __init__(self, crs: CRSEngine) -> None:
        self.crs = crs

    def run_evolution(self) -> Dict[str, object]:
        """Execute pattern learning + non-destructive concept evolution passes."""
        learned_claims = self.learn_recurring_patterns()
        refined_concepts = self.refine_overloaded_defaults()
        split_concepts = self.split_ambiguous_labels()

        return {
            "learned_claims_added": len(learned_claims),
            "concepts_refined": len(refined_concepts),
            "concepts_split": len(split_concepts),
            "learned_claim_ids": learned_claims,
            "refined_concept_ids": refined_concepts,
            "split_concept_ids": split_concepts,
        }

    # --- Phase 4: Pattern Learning from Existing Claims ---
    def learn_recurring_patterns(self) -> List[str]:
        """
        Detects entities with multiple distinct claims and records a learned summary claim
        as ActorRole.LEARNING_ENGINE without mutating or deleting underlying claims.
        """
        by_subject: Dict[str, List[Claim]] = {}
        for claim in self.crs.claims.values():
            if claim.epistemic_state == EpistemicState.UNKNOWN:
                continue
            by_subject.setdefault(claim.subject_id, []).append(claim)

        created: List[str] = []
        for subject_id, claims in by_subject.items():
            if len(claims) < 2:
                continue

            claim_id = f"learn_profile_{subject_id}"
            if claim_id in self.crs.claims:
                continue

            relations = sorted({f"{c.relation}={c.object_value}" for c in claims})
            prov_id = f"prov_learn_{uuid.uuid4().hex[:6]}"
            self.crs.add_provenance(
                ProvenanceNode(
                    id=prov_id,
                    kind="interpretation",
                    summary=f"Learned {len(claims)} co-occurring claims for {subject_id}: {', '.join(relations)}",
                    derived_from=(),
                ),
                actor=ActorRole.LEARNING_ENGINE,
            )
            self.crs.add_claim(
                Claim(
                    id=claim_id,
                    subject_id=subject_id,
                    relation="learned_claim_count",
                    object_value=len(claims),
                    epistemic_state=EpistemicState.INTERPRETED,
                    polarity=Polarity.POSITIVE,
                    provenance_id=prov_id,
                    uncertainty={"learning": "statistical_cooccurrence"},
                ),
                actor=ActorRole.LEARNING_ENGINE,
            )
            created.append(claim_id)

        return created

    # --- Phase 5A: Non-Destructive Concept Refinement ---
    def refine_overloaded_defaults(self) -> List[str]:
        """
        When a concept has explicit exceptions but its default still uses a legacy/unqualified
        label (e.g. 'can-fly' instead of 'usually-can-fly'), creates a new versioned concept
        and records a REFINE LineageEdge while keeping the older version intact.
        """
        refined_ids: List[str] = []

        for concept in list(self.crs.concepts.values()):
            if not concept.exceptions or not concept.defaults:
                continue
            if not any(d.startswith("can-") for d in concept.defaults):
                continue

            new_id = f"{concept.id}_evo_v{concept.version + 1}"
            if new_id in self.crs.concepts:
                continue

            new_defaults: Tuple[str, ...] = tuple(
                f"usually-{d}" if d.startswith("can-") else d for d in concept.defaults
            )
            updated = Concept(
                id=new_id,
                canonical=concept.canonical,
                version=concept.version + 1,
                labels=concept.labels,
                defaults=new_defaults,
                exceptions=concept.exceptions,
            )
            self.crs.add_concept(updated, actor=ActorRole.CONCEPT_EVOLUTION)
            edge = LineageEdge(
                from_concept_id=concept.id,
                to_concept_id=new_id,
                operation="REFINE",
                reason=f"Refined default capability {concept.defaults} -> {new_defaults} given exceptions {concept.exceptions}",
            )
            self.crs.lineage.append(edge)
            self.crs._persist("lineage", f"{concept.id}->{new_id}", edge)
            self.crs._audit(
                ActorRole.CONCEPT_EVOLUTION,
                "REFINE_CONCEPT",
                new_id,
                "OK",
                f"{concept.id} -> {new_id}",
            )
            refined_ids.append(new_id)

        return refined_ids

    # --- Phase 5B: Non-Destructive Polysemy / Label Split ---
    def split_ambiguous_labels(self) -> List[str]:
        """
        Detects when the same surface label is shared across multiple distinct concepts
        (polysemy, Section 84) and creates an explicit disambiguation hub concept
        linked via SPLIT lineage edges — without deleting any existing concepts.
        """
        label_to_concepts: Dict[str, List[Concept]] = {}
        for concept in self.crs.concepts.values():
            for group in concept.labels.values():
                for lbl in group:
                    key = lbl.strip().lower()
                    if key:
                        label_to_concepts.setdefault(key, []).append(concept)

        split_created: List[str] = []
        for label, matched in label_to_concepts.items():
            # Deduplicate concepts sharing the same label
            unique_concepts = list({c.id: c for c in matched}.values())
            if len(unique_concepts) < 2:
                continue

            hub_id = f"concept_polysemy_{label}"
            if hub_id in self.crs.concepts:
                continue

            hub = Concept(
                id=hub_id,
                canonical=f"POLYSEMY_{label.upper()}",
                version=1,
                labels={"en": (f"{label} (ambiguous)",)},
                defaults=(f"senses:{len(unique_concepts)}",),
            )
            self.crs.add_concept(hub, actor=ActorRole.CONCEPT_EVOLUTION)

            for sense in unique_concepts:
                edge = LineageEdge(
                    from_concept_id=hub_id,
                    to_concept_id=sense.id,
                    operation="SPLIT",
                    reason=f"Label '{label}' disambiguated across {len(unique_concepts)} concepts",
                )
                self.crs.lineage.append(edge)
                self.crs._persist("lineage", f"{hub_id}->{sense.id}", edge)

            self.crs._audit(
                ActorRole.CONCEPT_EVOLUTION,
                "SPLIT_CONCEPT",
                hub_id,
                "OK",
                f"Linked {len(unique_concepts)} senses for label '{label}'",
            )
            split_created.append(hub_id)

        return split_created


if __name__ == "__main__":
    from extra_data import load_extended_data
    from seed import build_demo_crs

    crs = build_demo_crs(db_path=None)
    load_extended_data(crs)

    evo = ConceptEvolutionEngine(crs)
    report = evo.run_evolution()

    print("=== ECOS Phases 4 & 5: Learning & Concept Evolution Report ===")
    print(f"Learned profile claims added : {report['learned_claims_added']}")
    print(f"Concepts refined (non-dest.) : {report['concepts_refined']} -> {report['refined_concept_ids']}")
    print(f"Polysemy hubs created (SPLIT): {report['concepts_split']} -> {report['split_concept_ids']}")

    print("\n--- Lineage Edges ---")
    for edge in crs.lineage:
        print(f"  {edge.from_concept_id} --[{edge.operation}]--> {edge.to_concept_id} | {edge.reason}")
