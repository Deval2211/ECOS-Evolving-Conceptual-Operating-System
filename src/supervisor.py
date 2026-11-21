from typing import Dict, List, Optional
import uuid

from engine import CRSEngine
from models import ActorRole, EpistemicState, ProvenanceNode


class CognitiveSupervisor:
    """
    Phase 3 ECOS Cognitive Supervisor (Section 70).
    Evaluates source reliability, triages contradictions, flags critical UNKNOWN
    safety gaps, and audits fragile inferences — without deleting or overwriting claims.
    """

    RELIABILITY_SCORES: Dict[str, float] = {
        "authoritative": 0.95,
        "calibrated": 0.90,
        "peer-reviewed": 0.90,
        "high": 0.80,
        "moderate": 0.60,
        "unverified": 0.30,
        "unassessed": 0.30,
        "low": 0.20,
    }

    def __init__(self, crs: CRSEngine) -> None:
        self.crs = crs

    def _source_score(self, source_id: Optional[str]) -> float:
        if not source_id or source_id not in self.crs.sources:
            return 0.25
        rel = self.crs.sources[source_id].reliability.strip().lower()
        return self.RELIABILITY_SCORES.get(rel, 0.30)

    def _source_label(self, source_id: Optional[str]) -> str:
        if not source_id or source_id not in self.crs.sources:
            return "unknown_source (unassessed)"
        src = self.crs.sources[source_id]
        return f"{src.name} ({src.reliability})"

    def review(self) -> Dict[str, object]:
        """Run a full epistemic governance pass over the CRS."""
        contradiction_reviews = self.evaluate_contradictions()
        unknown_alerts = self.audit_unknowns()
        fragile_inferences = self.audit_inferences()

        return {
            "contradictions_reviewed": len(contradiction_reviews),
            "unknown_alerts": len(unknown_alerts),
            "fragile_inferences": len(fragile_inferences),
            "contradiction_reports": contradiction_reviews,
            "unknown_reports": unknown_alerts,
            "fragile_inference_reports": fragile_inferences,
        }

    # --- 1. Contradiction Triage (Non-Destructive) ---
    def evaluate_contradictions(self) -> List[Dict[str, object]]:
        reports: List[Dict[str, object]] = []

        for pair in self.crs.get_contradictions():
            claim_a = pair["claim_a"]
            claim_b = pair["claim_b"]
            link = pair["link"]

            score_a = self._source_score(claim_a.source_id)
            score_b = self._source_score(claim_b.source_id)
            diff = round(abs(score_a - score_b), 2)

            if diff >= 0.30:
                preferred = claim_a if score_a > score_b else claim_b
                weaker = claim_b if score_a > score_b else claim_a
                verdict = "PREFER_HIGHER_RELIABILITY"
                action = (
                    f"Favor {preferred.id} ({preferred.object_value}) over {weaker.id} "
                    f"({weaker.object_value}); retain both claims for auditability."
                )
            else:
                verdict = "UNRESOLVED_TIE"
                hints = list(claim_a.uncertainty.values()) + list(claim_b.uncertainty.values())
                hint_text = ", ".join(dict.fromkeys(hints)) if hints else "collect calibrated/independent evidence"
                action = f"Verification required: {hint_text}."

            # Record a non-destructive supervisor evaluation node in CRS provenance
            eval_id = f"sup_eval_{link.id}"
            if eval_id not in self.crs.provenance:
                self.crs.add_provenance(
                    ProvenanceNode(
                        id=eval_id,
                        kind="evaluation",
                        summary=f"Supervisor triage ({verdict}): {action}",
                        derived_from=tuple(
                            s for s in (claim_a.source_id, claim_b.source_id) if s and s in self.crs.provenance
                        ),
                    ),
                    actor=ActorRole.COGNITIVE_SUPERVISOR,
                )

            reports.append(
                {
                    "link_id": link.id,
                    "subject": claim_a.subject_id,
                    "relation": claim_a.relation,
                    "claim_a": {
                        "id": claim_a.id,
                        "value": claim_a.object_value,
                        "source": self._source_label(claim_a.source_id),
                        "score": score_a,
                    },
                    "claim_b": {
                        "id": claim_b.id,
                        "value": claim_b.object_value,
                        "source": self._source_label(claim_b.source_id),
                        "score": score_b,
                    },
                    "verdict": verdict,
                    "recommended_action": action,
                }
            )

        return reports

    # --- 2. Critical UNKNOWN Safety & Completeness Audit ---
    def audit_unknowns(self) -> List[Dict[str, object]]:
        alerts: List[Dict[str, object]] = []

        for claim in self.crs.query_claims(epistemic_state=EpistemicState.UNKNOWN):
            is_safety = "safety" in claim.uncertainty
            priority = "HIGH_SAFETY" if is_safety else "NORMAL"
            guidance = (
                "DO NOT ASSUME FALSE — verify before taking action."
                if is_safety
                else "Information missing — gather evidence before concluding."
            )
            alerts.append(
                {
                    "claim_id": claim.id,
                    "subject": claim.subject_id,
                    "relation": claim.relation,
                    "priority": priority,
                    "uncertainty": claim.uncertainty,
                    "guidance": guidance,
                }
            )

        return alerts

    # --- 3. Fragile Inference Audit ---
    def audit_inferences(self) -> List[Dict[str, object]]:
        fragile: List[Dict[str, object]] = []

        for claim in self.crs.query_claims(epistemic_state=EpistemicState.INFERRED):
            chain = self.crs.trace_provenance(claim.provenance_id or "")
            weak_sources = []

            for node in chain:
                if node.kind == "source" and node.id in self.crs.sources:
                    if self._source_score(node.id) < 0.50:
                        weak_sources.append(self._source_label(node.id))

            if claim.source_id and self._source_score(claim.source_id) < 0.50:
                lbl = self._source_label(claim.source_id)
                if lbl not in weak_sources:
                    weak_sources.append(lbl)

            if weak_sources:
                fragile.append(
                    {
                        "claim_id": claim.id,
                        "subject": claim.subject_id,
                        "relation": claim.relation,
                        "value": claim.object_value,
                        "weak_sources": weak_sources,
                        "warning": "Derived conclusion depends on unverified/low-reliability source.",
                    }
                )

        return fragile


if __name__ == "__main__":
    from extra_data import load_extended_data
    from reasoning import ReasoningEngine
    from seed import build_demo_crs

    crs = build_demo_crs(db_path=None)
    load_extended_data(crs)

    # Run Phase 2 first so Phase 3 can also audit derived inferences
    ReasoningEngine(crs).run_all()

    supervisor = CognitiveSupervisor(crs)
    report = supervisor.review()

    print("=== ECOS Phase 3: Cognitive Supervisor Report ===")
    print(f"Contradictions reviewed : {report['contradictions_reviewed']}")
    print(f"Unknown alerts          : {report['unknown_alerts']}")
    print(f"Fragile inferences      : {report['fragile_inferences']}")

    print("\n--- Contradiction Triage ---")
    for r in report["contradiction_reports"]:
        print(f"  [{r['verdict']}] {r['subject']}.{r['relation']}:")
        print(f"      A: {r['claim_a']['value']} via {r['claim_a']['source']} (score={r['claim_a']['score']})")
        print(f"      B: {r['claim_b']['value']} via {r['claim_b']['source']} (score={r['claim_b']['score']})")
        print(f"      Action: {r['recommended_action']}")

    print("\n--- Critical UNKNOWN Alerts ---")
    for u in report["unknown_reports"]:
        print(f"  [{u['priority']}] {u['subject']}.{u['relation']} -> {u['guidance']}")

    print("\n--- Fragile Inferences ---")
    for f in report["fragile_inference_reports"]:
        print(f"  [FRAGILE] {f['subject']}.{f['relation']} = {f['value']} (depends on {f['weak_sources']})")
