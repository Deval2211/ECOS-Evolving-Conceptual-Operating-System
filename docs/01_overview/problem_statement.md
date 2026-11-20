# ECOS Problem Statement

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Research framing; hypotheses are unvalidated  
**Purpose:** Define the problems ECOS should test without presuming that its architecture solves them.  
**Last reviewed:** 2026-11-20

## Problem

Language-centric systems can produce fluent output while leaving the underlying claims, assumptions, evidence, temporal scope, and revision history difficult to inspect or control. ECOS asks whether a separate conceptual substrate can make those elements explicit enough to support reproducible symbolic reasoning and evidence-aware knowledge evolution.

The engineering problem is not “put text in a graph.” It is to define identities, claims, contexts, provenance, temporal semantics, and query behavior precisely enough that different components—and eventually different languages—can operate on the same records without hidden reinterpretation.

## Specific failure modes to investigate

| Failure mode | Required ECOS response | Initial testability |
|---|---|---|
| A new assertion silently overwrites an incompatible one | Store claims separately with polarity, context, and provenance | Directly testable in Phase 1 storage |
| “Not observed” is treated as false | Distinguish unknown, explicit negation, and rejected assessment | Directly testable in schema and queries |
| A fact’s valid time is confused with ingestion time | Use separate valid-time and transaction-time fields | Directly testable with temporal fixtures |
| Confidence appears precise without a basis | Require method and assessor metadata whenever confidence is present | Validation-rule test |
| A vector score is treated as truth | Keep vectors subordinate to symbolic claims and evidence | API and result-shape test |
| A label change destroys identity or history | Use stable IDs and explicit lineage, with evolution behavior deferred | Identity test now; lineage behavior in Phase 5 |
| Natural-language extraction uncertainty is hidden | Preserve adapter method, version, input, and extraction confidence separately | Provenance inspection test |
| Architecture changes before basic competence exists | Exclude AEE until Phases 1–7 meet explicit gates | Roadmap and scope review |

## Research uncertainty

A language-independent-by-design identifier does not guarantee language-independent meaning. Concept boundaries, relation choices, and extraction procedures may encode cultural or linguistic assumptions. Likewise, explicit provenance does not establish truth, and symbolic reasoning does not automatically provide commonsense competence.

## What would count as progress

Progress is a small, reproducible CRS that can demonstrate lossless claim/evidence round trips, temporal distinction, contradiction preservation, deterministic queries, and clear provenance. It is not a fluent chatbot, a large ontology, or a high benchmark score.

## Out-of-scope claims

ECOS documentation must not claim general intelligence, universal semantics, calibrated uncertainty, commonsense reasoning, autonomous improvement, multilingual superiority, or resource efficiency until those claims have explicit experimental support.

## References

- [Research objectives](research_objectives.md)
- [Ontology working draft](../03_ontology/ontology_working_draft.md)
- [Testing strategy](../06_implementation/testing_strategy.md)
