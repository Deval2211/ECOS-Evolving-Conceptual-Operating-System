# ECOS Component Responsibilities

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed component contracts; none implemented  
**Purpose:** Assign each component a narrow responsibility, inputs, outputs, and dependencies.  
**Last reviewed:** 2026-11-20

## Phase 1 contracts

| Component | Consumes | Produces | Depends on / boundary |
|---|---|---|---|
| Language Adapter | Controlled JSON or another explicitly versioned external format | Adapter envelope with source, language, method, and payload | No neural parser in the prototype |
| Concept Extractor | Valid adapter envelope | Candidate concepts, claims, evidence references, extraction provenance | Deterministic mapping for controlled input; ambiguity remains explicit |
| CRS | Candidate records and provenance | Validated canonical records and stable IDs | Owns semantics and transaction boundaries |
| Concept Memory | Canonical records | Durable concepts, claims, evidence, contexts, assessments, lineage events | SQLite is recommended for the prototype, not mandated long term |
| Concept Graph | Claims and concept references | Adjacency and bounded paths | Derived view; no independent truth |
| Vector Memory | Vector records linked to symbolic IDs | Similarity results with model and metric metadata | Supplied numeric vectors in Phase 1; not epistemic authority |
| Query Engine | Query specification and CRS projections | Concepts, claims, evidence, paths, and similarity results | No inference beyond explicitly requested traversal |

## Phase 2 reasoning services

| Service | Planned responsibility | Required constraint |
|---|---|---|
| Logical | Apply explicit deduction over formalized claims | Return rule and premise trace |
| Mathematical | Evaluate exact or formally defined expressions | Preserve units, domains, and numeric semantics |
| Temporal | Compare instants, intervals, and ordering relations | Keep valid and transaction time distinct |
| Spatial | Represent and evaluate formally defined spatial relations | Declare reference frame and precision |
| Causal | Represent causal hypotheses and evaluate defined interventions or rules | Do not infer causation from correlation alone |
| Analogical | Map structures under declared constraints | Return mapping and unmatched structure |
| Commonsense | Evaluate curated rules or external evidence | State coverage limits; avoid universal competence claims |

These are separate research services over CRS, not seven placeholders to build at once. Start with one narrow reasoning domain after Phase 1.

## Phase 3 — Cognitive Supervisor

Consumes claims, derivations, evidence, and alternative outcomes. Produces assessments, contradiction reports, missing-knowledge reports, alternative derivations, and verification reports. It must preserve the original records and identify the method and version used for every assessment.

## Phase 4 — Learning Engine

Consumes new evidence and reviewed candidate updates. Produces new claims, relationship revisions, integration events, and provenance links. It must support replay and historical inspection rather than mutating away the past.

## Phase 5 — Concept Evolution Engine

Consumes reviewed evolution proposals. Produces concept versions and lineage events for creation, merge, split, refinement, and deprecation. It depends on stable identity, mature learning behavior, and migration tests.

## Phase 6 — Reflection Engine

Consumes a problem, candidate contexts, and explicit frameworks. Produces framework-specific interpretations and comparisons. Framework selection criteria and unresolved ambiguity are part of the output.

## Phase 7 — Neural Language Adapters

Consume natural language or conceptual output plans. Produce candidate CRS records or natural-language realizations with model/version provenance. They are replaceable and must pass semantic-equivalence regression tests.

## Phase 8 — Architecture Evolution Engine

Consumes verified failure analyses and architecture evaluations. Produces proposals, simulation evidence, verification results, and controlled transition plans. It cannot approve or apply its own proposals; human-controlled transitions and rollback are mandatory.

## References

- [Complete architecture](complete_architecture.md)
- [CRS retrieval architecture](../04_crs/retrieval_architecture.md)
- [Open research questions](../05_research/open_research_questions.md)
