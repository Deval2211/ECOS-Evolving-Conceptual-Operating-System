# ECOS Related Projects and Repository Review

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Verified official-source review; recommendations are proposed  
**Purpose:** Compare candidate technologies by architectural purpose instead of assembling an unnecessary integration stack.  
**Research date:** 2026-11-20

## Comparison

| Project | Verified role and current indicators | Strength for ECOS | Limitation for Phase 1 | Recommended role |
|---|---|---|---|---|
| **Graphiti** | Python temporal context-graph framework; supports validity windows, episode provenance, incremental updates, hybrid retrieval, and custom types. Requires a graph backend and LLM/embedder for its normal ingestion path. Apache-2.0; repository showed current activity on the review date.[2][33] | Strong reference for valid-time history and source episodes | Neural extraction and external services conflict with a minimal non-neural substrate | **Reference design; do not adopt initially** |
| **OpenSPG** | Java/Scala knowledge-graph engine with domain-constrained modeling, construction, reasoning, and KAG orientation. Apache-2.0; inspected master’s latest commit was 2025-06-29.[3] | Schema and symbolic reasoning ideas | Different runtime stack and substantial platform scope; no demonstrated ECOS temporal/epistemic fit | **Reference only; no Phase 1 integration** |
| **Hyperon Experimental** | MeTTa implementation with Rust core, C API, and Python bindings; offers package and Docker paths. The project explicitly calls itself active pre-alpha. MIT; inspected main’s latest commit was 2026-02-11.[4][34] | Future symbolic language and inference research | Pre-alpha semantics/API risk; not needed to prove Phase 1 storage and retrieval | **Evaluate after Phase 1 for reasoning** |
| **RDFLib** | Actively maintained Python RDF library with graph/store abstractions, parsers/serializers, and SPARQL support. BSD-3-Clause; repository showed current activity on the review date.[5] | Standards-based RDF interchange and SPARQL experiments | Triples do not by themselves provide ECOS claim identity, bi-temporal semantics, evidence assessment, or contradiction policy | **Optional export/interoperability spike, not required core** |
| **Microsoft GraphRAG** | LLM-based unstructured-text transformation and graph-memory demonstration. The README explicitly says largely maintenance mode, not an officially supported Microsoft offering, and warns indexing can be expensive. MIT.[6][32] | Reference for graph-based RAG and community summarization | Wrong Phase 1 objective: LLM pipeline rather than conceptual epistemic substrate | **Do not adopt for Phase 1** |
| **OntoRAG** | Publicly accessible experimental Python ontology/RAG system using RDFLib, SPARQL, deterministic schema merging, and mention/origin provenance alongside LLM-assisted extraction. Apache-2.0; inspected main’s latest commit was 2026-09-23.[7] | Useful provenance and human-governed ontology patterns | Small experimental project, changing APIs, and LLM-assisted scope beyond the CRS core | **Reference provenance patterns only** |

Maintenance observations are snapshots, not quality scores or guarantees. Star counts were intentionally not used as adoption criteria.

## What each project clarifies

- **Graphiti:** old facts can be invalidated without deletion while raw episodes remain traceable. That pattern informs ECOS history but does not supply ECOS semantics.[33]
- **OpenSPG:** schema-constrained construction and reasoning can share a platform, but adopting a large JVM ecosystem would be a disproportionate first step.[3]
- **Hyperon:** a future reasoning spike should test MeTTa semantics against ECOS derivation and provenance requirements rather than assuming it is “AtomSpace with a nicer API.”[34]
- **RDFLib:** RDF is an interoperability choice, not a complete epistemic model. ECOS must define how claims, polarity, contexts, and temporal records survive any RDF mapping.[5][22]
- **GraphRAG:** graph-shaped RAG output is not equivalent to explicit, verified conceptual reasoning. Its current maintenance guidance further reduces its fit as a new foundation.[32]
- **OntoRAG:** fine-grained mention provenance and explicit schema origin are worth studying, but the project’s own experimental status argues against a new mandatory dependency.[7]

## Selection outcome

Only two candidates merit near-term optional spikes after the baseline works:

1. **RDFLib** for standards-based export/import and SPARQL comparison.
2. **Hyperon Experimental** for a later Phase 2 reasoning investigation.

AtomSpace is assessed separately in [AtomSpace evaluation](atomspace_evaluation.md). Graphiti and OntoRAG are design references. OpenSPG and GraphRAG are not recommended for the initial implementation. No integration of all six is proposed.

## Verification gaps

- No alternative repository was built or benchmarked for ECOS.
- RDF round-trip mapping and SPARQL coverage remain unverified.
- Hyperon package/Docker reproducibility was documented from upstream instructions, not executed.
- OntoRAG’s external provenance vocabulary stability was not established.
- Maintenance status must be rechecked immediately before adopting any dependency.

## Sources

[2] https://github.com/getzep/graphiti
[3] https://github.com/OpenSPG/openspg
[4] https://github.com/trueagi-io/hyperon-experimental
[5] https://github.com/RDFLib/rdflib
[6] https://github.com/microsoft/graphrag
[7] https://github.com/ontorag/ontorag
[22] https://www.w3.org/TR/rdf11-concepts
[32] https://raw.githubusercontent.com/microsoft/graphrag/main/README.md
[33] https://raw.githubusercontent.com/getzep/graphiti/main/README.md
[34] https://raw.githubusercontent.com/trueagi-io/hyperon-experimental/main/README.md
