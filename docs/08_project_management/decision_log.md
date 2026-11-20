# ECOS Decision Log

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Active decision register; proposed items require owner ratification  
**Purpose:** Record architectural direction, research decisions, unresolved choices, and their consequences.  
**Last reviewed:** 2026-11-20

## Status meanings

- **Assignment decision:** explicitly directed by the supplied project assignment.
- **Verified research finding:** current external/local fact checked against source.
- **Proposed:** recommended by this documentation review; not yet owner-ratified.
- **Open:** cannot be decided responsibly with available evidence.

| ID | Status | Decision / finding | Consequence |
|---|---|---|---|
| D-001 | Assignment decision | Use **Evolutionary Conceptual Operating System** in new documentation | Legacy “Evolving” name remains only in historical files |
| D-002 | Assignment decision | Build a non-neural conceptual foundation before neural language adapters | No PyTorch, Hugging Face, model training, or GPU in Phase 1 |
| D-003 | Assignment decision | **Capability must precede autonomy**; AEE is Phase 8 only | No AEE or self-modifying initial implementation |
| D-004 | Assignment decision | Preserve source files and project history; do not invent implementation results | Legacy root documents remain in Git; status labels are mandatory |
| D-005 | Verified local finding | Six named constitution/ontology/stress-test/CRS sources are absent from the repository/history | New files use `working_draft`; historical compatibility is unverified |
| D-006 | Proposed | Use Python standard library, JSON, and SQLite for the first vertical slice | Minimal local setup; no server or runtime package dependency |
| D-007 | Proposed | Defer AtomSpace until canonical semantics and a pinned mapping spike exist | Avoid native integration cost before a measured need[1] |
| D-008 | Proposed | Use RDFLib only for an optional interoperability spike | RDF does not become the canonical model by default[5] |
| D-009 | Proposed | Treat Graphiti and OntoRAG as design references; Hyperon as a later reasoning candidate | No integration of all reviewed repositories[4][7][33] |
| D-010 | Proposed | Keep Mamba, multimodal input, mobile optimization, and early distillation outside the baseline | Legacy ideas require a later demonstrated need |
| D-011 | Verified research finding | P100 retired from Kaggle on 2026-09-15; T4x2 is the current general GPU option cited by staff | Kaggle guide overrides older P100 text[16] |
| D-012 | Proposed | Use Kaggle only for bounded later neural experiments | Phase 1 remains local and CPU-first[8] |
| D-013 | Proposed | Preserve claims/evidence append-only in the prototype; corrections become new records | History and provenance are inspectable; updates are deferred |
| D-014 | Open | ECOS project license | No `LICENSE` created; owner must choose before release |
| D-015 | Open | Compatibility with missing Ontology v0.2 | Recover originals before claiming continuity |
| D-016 | Open | Long-term canonical store after baseline | Decide only from measured SQLite/RDFLib/AtomSpace comparisons |

## Change protocol

New decisions include date, status, rationale, affected documents, compatibility impact, and verification. Proposed decisions become assignment/owner decisions only after explicit approval. A reversal keeps the old entry and adds a superseding entry rather than erasing history.

## References

- [Risks](risks.md)
- [Changelog](changelog.md)
- [Build versus reuse](../05_research/build_vs_reuse.md)

## Sources

[1] https://github.com/opencog/atomspace
[4] https://github.com/trueagi-io/hyperon-experimental
[5] https://github.com/RDFLib/rdflib
[7] https://github.com/ontorag/ontorag
[8] https://www.kaggle.com/docs/notebooks
[16] https://www.kaggle.com/product-announcements/735239
[33] https://raw.githubusercontent.com/getzep/graphiti/main/README.md
