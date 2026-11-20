# ECOS Build versus Reuse Decision

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed technology decision; no integration executed  
**Purpose:** Choose the smallest stack that can test ECOS semantics while preserving later reuse options.  
**Last reviewed:** 2026-11-20

## Decision summary

| Capability | Build or reuse | Phase 1 decision | Reason |
|---|---|---|---|
| Language/runtime | Reuse Python | **Adopt** | Fast iteration, inspectable dataclasses, broad future adapter ecosystem |
| Durable store | Reuse SQLite through standard library | **Adopt** | Atomic local persistence without operating a server |
| Exchange format | Reuse JSON with ECOS-owned schema | **Adopt** | Explicit, debuggable, language-neutral transport |
| Claim/evidence semantics | Build | **ECOS-owned** | This is the research contribution; no candidate supplies it unchanged |
| Graph projection/traversal | Build small bounded implementation | **ECOS-owned** | Required behavior is narrow and deterministic |
| Vector memory | Build small supplied-vector scan | **ECOS-owned** | Avoids a database and neural embedding dependency |
| RDF interoperability | Reuse RDFLib later | **Optional spike** | Useful for standards export; not needed to validate the core[5] |
| Typed hypergraph/rewriting | Reuse AtomSpace only after a spike | **Defer** | Strong capabilities, but native build, semantic mapping, persistence, and license costs[1][14] |
| Symbolic language | Reuse Hyperon only after Phase 1 | **Defer** | Potential Phase 2 value; pre-alpha and unnecessary now[34] |
| Temporal/provenance patterns | Learn from Graphiti/OntoRAG | **Reference, not integrate** | Useful designs without importing LLM pipelines[7][33] |
| GraphRAG/OpenSPG | No adoption | **Reject for Phase 1** | Does not fit the minimal non-neural objective[3][32] |
| Neural frameworks | PyTorch/Hugging Face | **Defer to Phase 7** | No neural workload in the CRS prototype |
| Notebook compute | Jupyter/Kaggle | **Optional later** | Development convenience, not a runtime dependency |

## Why not adopt RDFLib as the canonical store immediately?

RDF gives a useful triple/dataset standard, but ECOS’s primary unit is an identified claim with polarity, context, provenance, temporal metadata, and assessments. Designing that model directly is easier to reason about than encoding it prematurely and then querying through reification conventions.[22]

An RDF export spike is justified only after the canonical JSON can round-trip without loss. The spike must prove claim identity, source chains, temporal precision, conflicting claims, and SPARQL query value. RDFLib remains the preferred candidate for that boundary because it is Python-native and actively maintained.[5]

## Why not adopt AtomSpace immediately?

AtomSpace offers real hypergraph and rewriting functionality, but ECOS would still build all seven requested semantic extensions. It also adds native dependencies, a separate storage decision, API risk, and AGPLv3-with-linking-exception review.[1][14]

The correct sequence is **baseline → mapping → pinned spike → comparison → decision**, not dependency first. Adoption is justified only when native pattern matching or rewriting solves a demonstrated baseline limitation.

## Reuse acceptance test

Every external candidate must pass the same fixture suite:

1. Lossless claim/evidence round trip.
2. Duplicate content with distinct provenance.
3. Contradictory claims preserved.
4. Valid-time and transaction-time queries.
5. Context/framework distinction.
6. Concept version and lineage representation.
7. Deterministic export and restart.
8. Reproducible build, license review, and acceptable integration effort.

A candidate that fails semantics cannot compensate with popularity or benchmark claims from a different workload.

## Cost of the minimal choice

SQLite does not provide native hypergraph matching, SPARQL, distributed graphs, or a vector index. The prototype must implement its small bounded traversal and vector scan. Those limitations are deliberate and documented; they become upgrade triggers only when measured requirements exceed them.

## Immediate decision requested

Approve Python + standard-library SQLite + JSON for the first vertical slice. Do not approve external runtime dependencies until the baseline acceptance tests exist. See [implementation roadmap](../06_implementation/implementation_roadmap.md) and [technology stack](../06_implementation/technology_stack.md).

## Sources

[1] https://github.com/opencog/atomspace
[3] https://github.com/OpenSPG/openspg
[5] https://github.com/RDFLib/rdflib
[7] https://github.com/ontorag/ontorag
[14] https://raw.githubusercontent.com/opencog/atomspace/master/LICENSE
[22] https://www.w3.org/TR/rdf11-concepts
[32] https://raw.githubusercontent.com/microsoft/graphrag/main/README.md
[33] https://raw.githubusercontent.com/getzep/graphiti/main/README.md
[34] https://raw.githubusercontent.com/trueagi-io/hyperon-experimental/main/README.md
