# ECOS Ontology and CRS Source Availability

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Verified source-gap record  
**Purpose:** Explain why this package contains new working drafts rather than purported copies of Ontology v0.1/v0.2 and CRS v0.1.  
**Last reviewed:** 2026-11-20

## Audit result

The repository and all local Git-history filenames were checked on 2026-11-20. None of the six named historical documents were present. No ontology stress-test execution artifact was found either.

| Requested historical source | Availability | Treatment in this package |
|---|---|---|
| ECOS Architectural Constitution v0.1 | Not found | New [proposed constitution](../02_architecture/architectural_constitution.md), not a recovered original |
| ECOS Ontology & Core Data Model v0.1 | Not found | No v0.1 reconstruction; see [ontology working draft](ontology_working_draft.md) |
| ECOS Ontology Stress Test v0.1 | Not found | New [unexecuted stress-test specification](stress_test_specification.md) |
| ECOS Ontology Stress Test Execution & Findings v0.1 | Not found | [Findings status record](stress_test_findings.md); no conceptual or runtime results invented |
| ECOS Ontology & Core Data Model v0.2 | Not found | No claim of compatibility with unseen v0.2 content |
| ECOS CRS Architecture Specification v0.1 | Not found | New [CRS working draft](../04_crs/crs_architecture_working_draft.md) |

## Why the usual filenames are intentionally avoided

Creating `ontology_v0.2.md` as if it were the missing reference would fabricate provenance and could overwrite a later recovered original. The new drafts therefore use explicit `working_draft` filenames and independent document versions.

## Required action when originals arrive

1. Add the originals unchanged under a clearly named historical-source directory.
2. Record their hashes and Git revisions.
3. Compare terminology, cardinality, identity, provenance, contradiction, temporal, and confidence semantics.
4. Mark each conflict as accepted, rejected, or unresolved in the decision log.
5. Only then designate a new Ontology v0.2 or CRS v0.1 baseline and execute the stress suite.

## Current compatibility statement

All new documents are internally aligned with the proposed ontology working draft. **Compatibility with the missing external Ontology v0.2 is unverified.** This is a blocking documentation gap for claiming historical continuity, but not for reviewing or implementing a small explicit prototype after approval.

See the full [repository source audit](../source_audit.md).
