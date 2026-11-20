# ECOS CRS Prototype Requirements

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed acceptance requirements; not implemented or tested  
**Purpose:** Specify the minimum complete behavior for the first CRS prototype.  
**Last reviewed:** 2026-11-20

## Functional requirements

| ID | Requirement | Acceptance example |
|---|---|---|
| FR-01 | Accept a versioned controlled JSON envelope with adapter provenance | Missing format version or adapter version is rejected |
| FR-02 | Create and retrieve concepts with stable IDs and language-tagged labels | Label rename does not change ID or claims |
| FR-03 | Append claims with discriminated objects, polarity, context, valid time, recording time, and provenance | Every field survives export exactly |
| FR-04 | Append sources, acquisition/extraction events, evidence items, and typed evidence relations | A claim returns both supporting and contradicting evidence |
| FR-05 | Store an explicit default context and optional framework references | Two context-specific readings remain distinguishable |
| FR-06 | Query concepts and claims using exact filters | Empty result is labeled no-match, not false |
| FR-07 | Traverse concept relationships with direction, depth, and result bounds | Cyclic fixture terminates with deterministic paths |
| FR-08 | Store supplied numeric vectors with target, dimensions, metric, and producer provenance | Invalid dimensions and zero norm are rejected for cosine |
| FR-09 | Return deterministic vector similarity without changing epistemic state | Low-evidence claim can be nearest without becoming verified |
| FR-10 | Export and reload a complete store deterministically | Record IDs and provenance match after restart/reload |

## Data-integrity requirements

- A batch is atomic; any invalid record aborts the entire batch.
- IDs are unique and references resolve to the expected record type.
- Claims and evidence are immutable through the public repository API.
- No timestamp is invented for valid time.
- Literal values retain lexical value and datatype; units are explicit concepts where applicable.
- Confidence is rejected unless method, assessor, basis, and assessment time are present.
- Duplicate IDs are rejected unless a documented idempotent-import comparison proves the records identical; conflicting duplicates are always rejected.

## Query-result requirements

Every result envelope includes schema version, result kind, query parameters, and records. Paths include claim IDs. Evidence responses include provenance. Vector responses include score, metric, dimensions, and producer/version. No result promotes a vector score to a verdict or confidence value.

## Non-functional requirements

- Deterministic behavior for a fixed store, fixture, and query.
- Python 3.11+ standard library only for the initial implementation and tests.
- Local single-writer operation; no network service.
- Small public synthetic fixtures and inspectable JSON output.
- Clean-checkout setup and demo instructions.
- No performance or scalability claim until a benchmark exists.

## Explicit exclusions

Unrestricted NLP, multimodal ingestion, embeddings generation, automated reasoning, contradiction detection/resolution, confidence calibration, learning, concept evolution, reflection, neural adapters, distributed/concurrent writes, multi-user access control, UI, and AEE are excluded.

## Demonstration fixture

Use synthetic concepts `cat`, `water`, and `milk`, relation `drinks`, and two sources asserting incompatible claims. Add one explicit denial, one claim with distinct valid/recorded times, a cycle for traversal, and two small supplied vectors. The expected outputs are listed in the [implementation roadmap](implementation_roadmap.md#expected-demonstration-outputs); they are not current results.

## Acceptance gate

A reviewer must be able to run the demo from a clean checkout, inspect the output and test log, and verify every requirement without reading source code to discover hidden behavior. Failures remain in the report and block the corresponding success criterion.
