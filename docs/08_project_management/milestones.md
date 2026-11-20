# ECOS Milestones

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Verified documentation progress; future engineering milestones proposed  
**Purpose:** Track evidence-based progress without converting completed prose into completed capability.  
**Last reviewed:** 2026-11-20

| Milestone | Deliverable and exit evidence | Status on 2026-11-20 |
|---|---|---|
| M0 — Source and research baseline | Local audit, named-source gap record, AtomSpace/alternative review, current Kaggle research | **Documentation complete; consistency review required before finalization** |
| M1 — Design approval | Owner approves scope, ontology working draft, minimal stack, and acceptance tests; license remains separately unresolved | **Pending** |
| M2 — Vertical slice A | One valid claim/evidence batch ingests atomically and survives restart | **Not started** |
| M3 — Vertical slice B | Exact, evidence, conflict, temporal, graph, and vector queries pass | **Not started** |
| M4 — CRS prototype | Clean-checkout demo, deterministic export, tests, limitations, and actual stress results published | **Not started** |
| M5 — One reuse decision | RDFLib, AtomSpace, or narrow Phase 2 rule selected from measured baseline need | **Not started; choose only one** |
| M6 — Reasoning foundation | Narrow explicit reasoning with premises, rules, derivations, and failure fixtures | **Future Phase 2** |
| M7+ — Later cognition | Supervisor, learning, concept evolution, reflection, neural adapters | **Future gated phases** |
| M8 — AEE investigation | Separate safety/maturity review after earlier evidence | **Deferred; not approved** |

## Milestone rules

- `Documentation complete` means files exist and pass link/metadata/citation checks; it does not mean architecture validation.
- `Prototype complete` requires the recorded clean-checkout demo and tests in the implementation roadmap.
- `Capability validated` requires the evidence level named in the [status taxonomy](../project_status.md).
- A missed gate leaves the milestone open; dates and descriptions are not edited to imply success.

## Immediate milestone

Finish the documentation consistency review, then obtain M1 approval. The first engineering target is M2, not a dataset build, neural adapter, or AtomSpace integration.

## References

- [Phase roadmap](../02_architecture/phase_roadmap.md)
- [Implementation roadmap](../06_implementation/implementation_roadmap.md)
- [Decision log](decision_log.md)
