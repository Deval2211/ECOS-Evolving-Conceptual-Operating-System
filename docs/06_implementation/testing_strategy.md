# ECOS Testing Strategy

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed test strategy; no tests implemented or run  
**Purpose:** Verify semantic fidelity and data integrity before pursuing reasoning or scale.  
**Last reviewed:** 2026-11-20

## Test levels

1. **Validation unit tests:** record shape, IDs, references, discriminated objects, timestamps, confidence, and vectors.
2. **Storage tests:** atomic batches, duplicate handling, restart, immutable public behavior, schema version, export/reload.
3. **Query tests:** exact filters, empty results, evidence chains, deterministic ordering, and result metadata.
4. **Graph tests:** incoming/outgoing adjacency, multiple claims per tuple, polarity, cycles, depth and result bounds.
5. **Vector tests:** metric validation, dimensions, zero norm, filtering, deterministic ties, provenance.
6. **End-to-end tests:** controlled adapter through ingestion, query, export, and restart.
7. **Ontology stress suite:** L1/L2 cases from the [stress specification](../03_ontology/stress_test_specification.md).

## Core case matrix

| Test | Expected result |
|---|---|
| Valid minimal claim round trip | Fields and provenance are identical after export/reload |
| Ambiguous object string | Rejected before storage |
| Dangling reference | Entire batch rolls back |
| Conflicting duplicate ID | Rejected; existing record unchanged |
| Identical idempotent import | Behavior matches the documented rule; no duplicate records |
| Two contradictory claims | Both remain independently queryable with evidence |
| Unknown versus explicit denial | Different query results and serialized meaning |
| Month-only valid date | No fabricated day/timezone |
| Valid time versus recorded time | Independent fields and filters |
| Bare `confidence: 0.98` | Rejected; transaction unchanged |
| Graph cycle | Finite deterministic bounded result |
| Repeated claim tuple | Claims remain distinct by ID and provenance |
| Zero-vector cosine query | Validation error, not `NaN` |
| Vector tie | Score then vector-record ID ordering |
| Failed adapter extraction | No canonical records committed; error includes adapter metadata |
| Restart after commit | All records, references, and indexes behave identically |

## Fixtures

Use small synthetic public data. Keep valid, conflict, temporal, context, provenance, cycle, vector, and malformed fixtures in version control with their expected outputs. Do not use model-generated expected outputs without review. Each expected value needs a semantic rationale.

## Determinism and isolation

Each test receives a fresh temporary database and never writes to a developer’s real store. Tests control timestamps through fixture values rather than reading the wall clock. Record order, path order, and tie-breaking are asserted. Tests report implementation revision and Python/platform details for end-to-end runs.

## Negative and security cases

Malformed JSON, oversized depth/limit, invalid UTF-8 handling at the file boundary, non-finite numeric values, unsupported datatype, unexpected record type, and unknown schema version must fail explicitly. The prototype is local, but validation at the external-file trust boundary is mandatory.

## Evidence policy

A test is `pass` only after actual execution produces the expected result. Store commands, logs, fixture versions, and revision. Update [stress-test findings](../03_ontology/stress_test_findings.md) case by case. Conceptual review is labeled L0 and cannot substitute for executable L1/L2 evidence.

## Deferred test families

- Reasoning soundness and derivation validation (Phase 2).
- Contradiction detection and confidence calibration (Phase 3).
- Learning replay and update safety (Phase 4).
- Lineage/migration correctness (Phase 5).
- Framework comparison (Phase 6).
- Neural semantic equivalence and model regression (Phase 7).
- Architectural simulation/transition/rollback safety (Phase 8).
- Performance, concurrency, and large-scale benchmarks only after a workload target exists.

## References

- [Architectural invariants](../02_architecture/architectural_invariants.md)
- [Prototype requirements](prototype_requirements.md)
- [Evidence taxonomy](../project_status.md)
