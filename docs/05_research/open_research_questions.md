# ECOS Open Research Questions

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Open question register; none resolved by this documentation  
**Purpose:** Keep unresolved semantics and validation needs visible before implementation locks them in.  
**Last reviewed:** 2026-11-20

| ID | Question | Needed evidence / decision | Blocks |
|---|---|---|---|
| RQ-01 | Where are the six named historical constitution/ontology/stress-test/CRS documents? | Recover originals and perform version comparison | Claiming continuity with Ontology v0.2 or historical findings |
| RQ-02 | How are concepts identified across sources and languages without label-driven false merges? | Identity-resolution rules, negative fixtures, manual review protocol | Reliable multi-source ingestion |
| RQ-03 | What is the minimal formal type system for concepts, relations, literals, events, and claims? | Type semantics and validation cases | Reasoning and safe schema evolution |
| RQ-04 | When are claims contradictory within or across contexts? | Context compatibility rules and contradiction fixtures | Phase 3 supervisor |
| RQ-05 | How should unknown, explicit denial, rejection, and lack of evidence interact? | Epistemic semantics and query examples | Reasoning and assessment |
| RQ-06 | What confidence representation is meaningful and calibrated? | Defined estimators, datasets, calibration analysis | Confidence claims in Phase 3 |
| RQ-07 | How should valid-time uncertainty, granularity, and open intervals be represented and queried? | Temporal fixtures and semantics; export mapping | Temporal reasoning |
| RQ-08 | How are transaction-time corrections replayed without changing prior query results unexpectedly? | Replay rules and historical-query specification | Learning and audit |
| RQ-09 | What constitutes independent evidence and support strength? | Evidence-quality model and evaluation | Evidence aggregation |
| RQ-10 | How are concept splits and merges mapped for historical claims? | Lineage algebra and migration fixtures | Phase 5 evolution |
| RQ-11 | What is a framework formally, and how can frameworks be compared? | Framework schema, semantics, and comparison criteria | Phase 6 reflection |
| RQ-12 | Can the canonical model map losslessly to RDF/PROV-O/OWL-Time? | RDFLib round-trip spike and query comparison | Standards interoperability decision |
| RQ-13 | Do AtomSpace pattern matching and rewriting justify their integration cost? | Pinned AtomSpace spike against the same fixtures | AtomSpace adoption |
| RQ-14 | Does MeTTa improve derivation clarity over a small explicit rule engine? | Phase 2 Hyperon comparison | Hyperon adoption |
| RQ-15 | What measurable advantage does CRS provide over a simpler document/triple baseline? | Comparative fixtures, query effort, fidelity, and runtime results | Architectural value claim |
| RQ-16 | Can language adapters preserve claim meaning across languages? | Multilingual semantic-equivalence dataset and error analysis | Language-independence claim |
| RQ-17 | Which vector representations preserve useful conceptual similarity? | Producer-specific retrieval evaluation and bias analysis | Neural/vector retrieval claims |
| RQ-18 | What maturity evidence would make AEE investigation safe and useful? | Verified earlier phases, threat model, simulation/rollback protocol | Phase 8 gate |
| RQ-19 | Which license should govern ECOS, and how does AtomSpace’s license exception affect reuse? | Owner licensing decision and legal review | Public release and AtomSpace integration |
| RQ-20 | What are the actual performance, scale, and resource requirements? | Benchmarks on declared fixtures and hardware | Capacity planning and timeline estimates |

## Prioritization

Resolve RQ-02 through RQ-08 enough for a narrow prototype, while explicitly limiting its domain. RQ-01 does not block a new draft, but it blocks historical compatibility claims. RQ-12 through RQ-14 require spikes, not more prose. RQ-15 is the central value test and should remain visible throughout development.

## Change rule

Closing a question requires a linked decision, experiment, or recovered source. Add the outcome and remaining limitations to the [decision log](../08_project_management/decision_log.md); do not delete the original question or its history.
