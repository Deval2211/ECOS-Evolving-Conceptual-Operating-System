# ECOS Phase Roadmap

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed gated roadmap; no phase is implemented or time-validated  
**Purpose:** Define dependencies and evidence gates instead of treating the eight phases as a feature checklist.  
**Last reviewed:** 2026-11-20

| Phase | Components and responsibilities | Minimum exit evidence |
|---|---|---|
| **1 — Foundation** | Language Adapter, Concept Extractor, CRS, Concept Graph, Concept Memory, Vector Memory, Query Engine | Versioned schema; durable claim/evidence round trip; exact and bounded graph queries; supplied-vector retrieval; restart and negative-case tests |
| **2 — Reasoning** | Logical, mathematical, temporal, spatial, causal, analogical, commonsense reasoning | Explicit semantics per reasoner; proof/derivation traces; soundness and failure fixtures; no hidden natural-language inference |
| **3 — Cognitive Supervisor** | Confidence evaluation, contradiction and missing-knowledge detection, alternatives, evidence evaluation, verification | Measured detection behavior; abstention cases; confidence evaluation; reproducible verification reports |
| **4 — Learning Engine** | Evidence acquisition, concept and relationship updates, integration, provenance | Replayable updates; historical queries; conflict retention; rollback and provenance-chain tests |
| **5 — Concept Evolution Engine** | Create, merge, split, refine, deprecate, lineage | Migration fixtures; unambiguous historical identity; lineage queries; reversible or compensating transitions |
| **6 — Reflection Engine** | Context/framework selection, interpretive reasoning, framework comparison | Explicit framework definitions; comparable outputs; assumptions visible; no hidden framework privileging |
| **7 — Neural Language Adapters** | Neural translation into and out of CRS | Cross-lingual semantic-equivalence fixtures; adapter provenance; regression tests showing core independence |
| **8 — Architecture Evolution Engine** | Failure analysis, evaluation, proposals, simulation, verification, controlled transitions | Sandboxed proposal evaluation; independent verification; human approval; rollback; audit log; demonstrated need |

## Dependency gates

```mermaid
flowchart LR
    P1[Foundation evidence] --> P2[Reasoning evidence]
    P2 --> P3[Supervisor evidence]
    P3 --> P4[Learning evidence]
    P4 --> P5[Concept evolution evidence]
    P5 --> P6[Reflection evidence]
    P1 --> P7
    P6 --> P8[AEE research gate]
    P7 --> P8
```

Neural adapter research can be prepared independently after the CRS contract is stable, but it must not redefine that contract implicitly. AEE requires the combined maturity of representation, reasoning, verification, learning, reflection, and adapter boundaries.

## Phase 1 slices

1. **Schema slice:** validate and round-trip one concept, claim, and evidence item.
2. **Persistence slice:** restart without losing claims, provenance, or transaction history.
3. **Graph slice:** retrieve neighbors and bounded paths from claims, including incompatible assertions.
4. **Vector slice:** store and query a small set of supplied numeric vectors with model/metric metadata.
5. **Demonstration slice:** run one documented fixture end to end and emit inspectable JSON.

## Estimation policy

Legacy duration and hardware estimates are planning hypotheses, not commitments. Produce estimates only after the first vertical slice establishes actual implementation and evaluation cost. Do not infer a total project timeline by adding optimistic phase durations.

## AEE gate

AEE remains excluded until a written review shows that earlier phases have reproducible evidence, known failure modes, stable interfaces, and a safe need for architectural proposals. Merely completing documentation or accumulating experience data does not open this gate.

## References

- [Implementation roadmap](../06_implementation/implementation_roadmap.md)
- [Milestones](../08_project_management/milestones.md)
- [Prototype requirements](../06_implementation/prototype_requirements.md)
