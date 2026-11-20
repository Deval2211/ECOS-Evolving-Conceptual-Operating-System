# ECOS Existing Research and Standards

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Focused research map, not a systematic literature review  
**Purpose:** Ground ECOS design choices in existing representations while avoiding claims that the combination is already validated.  
**Research date:** 2026-11-20

## 1. RDF and named graphs

RDF 1.1 defines graphs as sets of subject–predicate–object triples and datasets as a default graph plus zero or more named graphs. This gives ECOS a standards-based exchange model and a possible context boundary, but not a ready-made claim-assessment or valid-time semantics.[22]

**Use:** map stable concept IDs and claim records to IRIs; evaluate named graphs for context/export.  
**Do not assume:** a triple named by a graph is automatically true in that graph, or that reification supplies provenance by itself.

## 2. Provenance

PROV-O expresses the PROV Data Model in OWL2 for representing and exchanging provenance across systems. It can be specialized for application needs.[19]

**Use:** align ECOS provenance events, sources, agents, and inputs with PROV concepts at an export boundary.  
**Research gap:** a complete mapping for claim polarity, evidence judgment, extraction uncertainty, and framework context must be tested for losslessness.

## 3. Temporal representation

OWL-Time provides vocabulary for instants, intervals, durations, ordering relations, and temporal reference systems. The inspected latest published page is a Candidate Recommendation Draft, so its status must not be overstated.[21]

**Use:** inform valid-time representation and RDF export.  
**Research gap:** transaction time, ingestion history, vague dates, and temporal confidence still require ECOS-specific conventions.

## 4. Validation

SHACL validates RDF data graphs against shapes and conditions. It can express structural constraints but does not prove the truth or evidential quality of claims.[20]

**Use:** evaluate SHACL for RDF export validation after the canonical JSON constraints are stable.  
**Research gap:** cross-record rules such as confidence qualification and vector compatibility may need application validation as well.

## 5. Temporal agent memory

The Zep paper introduces Graphiti as a temporally aware knowledge-graph engine that integrates changing data while maintaining historical relationships. Its reported benchmark results belong to Zep’s evaluated systems and datasets, not to ECOS.[23]

**Use:** study bi-temporal validity and raw-episode provenance as design patterns.  
**Do not transfer:** claimed accuracy or latency improvements to a future ECOS adapter or store.

## 6. Typed hypergraphs and rewriting

AtomSpace represents immutable, globally unique typed Nodes and Links and provides graph queries and rewriting. Its current direction favors generic Values over legacy TruthValues.[1][29]

**Use:** evaluate native higher-order structure and explicit query/rewrite graphs for later reasoning.  
**Research gap:** ECOS must demonstrate that its epistemic and temporal layers survive this representation without unacceptable complexity.

## 7. Symbolic languages and inference

Hyperon’s MeTTa implementation targets clear semantics and multiple forms of inference while explicitly remaining pre-alpha.[34]

**Use:** future comparison of rule representation, derivation traces, and Python integration.  
**Research gap:** language expressiveness alone does not establish reasoning soundness or ECOS compatibility.

## Research hypotheses ECOS must test

| Hypothesis | Experiment | Failure condition |
|---|---|---|
| Explicit claims improve auditability over bare edges | Implement the same fixtures in ECOS JSON and a simple triple baseline | Provenance cannot be recovered or query effort is worse without measured benefit |
| Bi-temporal records improve historical fidelity | Query current and past states after contradictory updates | Historical answers are ambiguous or prior evidence is lost |
| Context/framework records improve interpretability | Compare the same claim under two frameworks | Framework assumptions cannot be reconstructed from output |
| Vector projections aid retrieval without controlling truth | Combine exact, path, and vector queries | Similarity changes verdicts or cannot be traced to producer metadata |
| Hypergraph rewriting simplifies later derivations | Compare a narrow rule in SQLite-backed code and AtomSpace | No maintainability or query benefit justifies integration cost |

## Scope limitation

This is a targeted review of directly relevant standards and repositories requested for the first architecture decision. It is not an exhaustive review of conceptual graphs, description logics, belief revision, truth-maintenance systems, probabilistic logic, causal inference, or neuro-symbolic AI. Those areas become separate literature-review tasks before corresponding Phase 2–6 claims are designed.

## References

- [Related projects](related_projects.md)
- [AtomSpace evaluation](atomspace_evaluation.md)
- [Open research questions](open_research_questions.md)

## Sources

[1] https://github.com/opencog/atomspace
[19] https://www.w3.org/TR/prov-o
[20] https://www.w3.org/TR/shacl
[21] https://www.w3.org/TR/owl-time
[22] https://www.w3.org/TR/rdf11-concepts
[23] https://arxiv.org/abs/2501.13956
[29] https://raw.githubusercontent.com/opencog/atomspace/master/opencog/atoms/README.md
[34] https://raw.githubusercontent.com/trueagi-io/hyperon-experimental/main/README.md
