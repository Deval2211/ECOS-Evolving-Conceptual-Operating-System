# ECOS Risk Register

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Active proposed risk register; no risk owners assigned yet  
**Purpose:** Identify the failures most likely to undermine semantic fidelity, implementation readiness, or research credibility.  
**Last reviewed:** 2026-11-20

| ID | Risk | Early signal | Mitigation | Residual concern |
|---|---|---|---|---|
| R-01 | Prose is mistaken for a working cognitive system | Documents say “ECOS does” without revision/test evidence | Enforce status taxonomy and changelog evidence | Readers may still over-trust architecture diagrams |
| R-02 | Missing historical sources cause false continuity | Ontology v0.2 cited as if inspected | Keep working-draft names and source-gap record | Originals may contradict new semantics |
| R-03 | Scope expands into neural/platform work before CRS proof | Model downloads, services, or empty phase modules appear | Ten-task vertical slice and explicit exclusions | Research pressure to demonstrate fluency early |
| R-04 | Identity resolution merges distinct concepts | Label-based IDs or silent deduplication | Opaque IDs, negative fixtures, reviewable resolution | Cross-source identity remains unsolved |
| R-05 | Contradictions or provenance are lost | Overwrite-on-ingest or bare edge export | Append-only claims, evidence links, round-trip tests | Migration tools could bypass public API |
| R-06 | Confidence appears calibrated without evidence | Bare scores or vector-as-truth behavior | Qualification validation and calibration research later | Users may still interpret numeric scores intuitively |
| R-07 | Temporal semantics collapse | Ingestion time copied into valid time | Bi-temporal fixtures and precision tests | Complete interval/vagueness semantics remain open |
| R-08 | Dependency complexity exceeds research value | Large stack before first round trip | Standard-library baseline and measured reuse gates | SQLite limitations may eventually require migration |
| R-09 | AtomSpace integration is underestimated | Assuming pip installation or native provenance support | Pinned local spike, seven-layer mapping, build/license review | API/deprecation and storage compatibility |
| R-10 | Licensing/attribution is unresolved | Public release with `TBD` or unreviewed dependencies | Owner license decision and dependency-specific legal review | AtomSpace’s exact use model matters[14] |
| R-11 | Kaggle information becomes stale | P100 instructions or fixed quota assumptions reused | Date-stamp sources and recheck live UI/announcements[16] | Account-specific access still differs |
| R-12 | Ephemeral experiments lose outputs | Artifacts outside saved working output | Save/download outputs and record environment | Native build artifacts may not be portable |
| R-13 | Test expectations are generated rather than justified | Model-written oracle accepted without review | Human-reviewed synthetic fixtures and semantic rationale | Shared misconceptions between designer/reviewer |
| R-14 | Query retrieval is mistaken for reasoning | Paths or nearest neighbors presented as proof | Result-kind labels and derivation records in Phase 2 | UI/rendering may hide distinction |
| R-15 | Sensitive data enters a public/hosted experiment | Private sources uploaded to notebooks | Public synthetic fixtures, privacy/license review | Redaction can break provenance locators |
| R-16 | AEE begins before safety/maturity evidence | Self-modifying proposals in early code | Constitutional prohibition and explicit Phase 8 gate | Future transition safety remains a hard research problem |

## Review cadence

Review R-01 through R-08 at every Phase 1 milestone. Revalidate external maintenance and Kaggle facts immediately before dependency or compute decisions. Add actual risk outcomes to the changelog rather than silently closing entries.

## References

- [Decision log](decision_log.md)
- [Open research questions](../05_research/open_research_questions.md)
- [Compute strategy](../07_compute/compute_strategy.md)

## Sources

[14] https://raw.githubusercontent.com/opencog/atomspace/master/LICENSE
[16] https://www.kaggle.com/product-announcements/735239
