# ECOS Architectural Constitution

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed constitution; assignment-derived rules plus recommendations awaiting project-owner ratification  
**Purpose:** Define the constraints that later designs and implementations must not silently violate.  
**Last reviewed:** 2026-11-20

## Article 1 — Purpose and evidence

1. ECOS investigates structured conceptual representation; it does not presume general intelligence or universal semantics.
2. Every capability claim must carry a status from the [evidence taxonomy](../project_status.md).
3. A conceptual walkthrough is not an executed test, and external project results are not ECOS results.

## Article 2 — Representation

4. Natural-language labels are annotations attached to stable conceptual identifiers, not the identifiers themselves.
5. Knowledge assertions are represented as identified **claims**, not only as context-free edges.
6. Every claim has a subject, predicate, object, polarity, context, and provenance. Unknown values remain explicitly unknown.
7. Absence of a claim is not negation. Explicit denial, absence of evidence, and rejection by an assessor are different states.
8. Valid time and transaction time are separate. Partial or uncertain temporal knowledge must not be coerced into a false exact timestamp.

## Article 3 — Evidence and history

9. Externally sourced claims require provenance sufficient to locate their origin and extraction path.
10. Evidence supports or contradicts a claim through a typed, provenance-bearing relation; evidence is not synonymous with proof.
11. Incompatible claims coexist with their own contexts and evidence. No component may silently delete one to manufacture consistency.
12. Claims and evidence records are append-only in the initial design. Assessments and supersession are new records, not destructive rewrites.
13. Concept lineage must be explicit before merge, split, refinement, or deprecation behavior is introduced.

## Article 4 — Reasoning and assessment

14. Reasoning operates over conceptual records and returns its inputs, rules, assumptions, and derivation path.
15. Vector similarity is a retrieval hint, never a truth value or proof.
16. Confidence is optional and must include method, assessor, basis, and assessment time. A bare number is uncalibrated metadata.
17. A component may abstain and report missing knowledge; it must not invent certainty to complete an answer.

## Article 5 — Modularity and compute

18. The CRS owns the canonical record. Language adapters, storage engines, vector indexes, and neural models are replaceable boundaries.
19. Phase 1 requires no neural network or GPU. GPU-backed adapters are deferred to Phase 7.
20. Prefer the smallest dependency that satisfies a measured requirement. Reuse must preserve ECOS’s ontology and epistemic semantics rather than renaming an external system.

## Article 6 — Staged autonomy

21. **Capability must precede autonomy.** Representation precedes reasoning; reasoning precedes verification; verification precedes learning and concept evolution; these precede reflection and architectural evolution.
22. The Architecture Evolution Engine is excluded from Phase 1 and investigated only in Phase 8 after explicit maturity gates.
23. Any future architectural transition requires failure analysis, simulation, verification, human-controlled approval, and rollback. Unreviewed self-modification is prohibited.

## Article 7 — Engineering discipline

24. Trust-boundary input validation, provenance preservation, data-loss protection, and reproducible tests are not optional simplifications.
25. Each phase requires fixtures, negative cases, and documented exit criteria. A phase number is not evidence of maturity.
26. No dependency, storage migration, or architectural evolution may destroy the ability to read historical claims and provenance.

## Interpretation

“Must” applies when this constitution is adopted for implementation. Until ratification, these rules are the proposed baseline derived from the current assignment and architecture review. Changes require an entry in the [decision log](../08_project_management/decision_log.md), a compatibility analysis, and updates to dependent documents.

## References

- [Architectural invariants](architectural_invariants.md)
- [Phase roadmap](phase_roadmap.md)
- [Ontology working draft](../03_ontology/ontology_working_draft.md)
