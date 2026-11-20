# ECOS Architectural Invariants

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed invariants; tests not implemented  
**Purpose:** Define observable properties that every implementation and migration must preserve.  
**Last reviewed:** 2026-11-20

An invariant is a property that must remain true before and after an operation. These are acceptance requirements, not claims about current software.

| ID | Invariant | Initial verification |
|---|---|---|
| INV-01 | A concept’s stable ID is not derived solely from a mutable natural-language label | Rename label; identity and references remain unchanged |
| INV-02 | Every claim has a unique ID, subject, predicate, object, polarity, context, and provenance | Schema validation and round trip |
| INV-03 | Missing information is never serialized as explicit falsehood | Unknown/negation fixtures remain distinguishable |
| INV-04 | Valid time and transaction time cannot overwrite one another | Temporal round trip and point-in-time query |
| INV-05 | Ingesting a contradictory claim does not delete or mutate the earlier claim | Two-claim fixture; both remain queryable |
| INV-06 | Evidence and claim IDs remain recoverable after restart and migration | Persistence and compatibility tests |
| INV-07 | A confidence value is rejected unless method, assessor, basis, and assessment time are present | Negative validation tests |
| INV-08 | Vector results include the source vector record, model/embedding provenance, metric, and symbolic ID | Similarity result contract test |
| INV-09 | Graph traversal is bounded and deterministic for a fixed store and query | Repeated traversal and cycle fixtures |
| INV-10 | Query results distinguish stored assertions from inferred derivations | Result-type and provenance test once reasoning exists |
| INV-11 | Every derived assertion retains premises, rule/method, and context | Derivation inspection in Phase 2 |
| INV-12 | Updates and evolution operations append auditable events rather than silently destroying history | Replay and lineage tests in Phases 4–5 |
| INV-13 | Adapter or model changes do not require changing canonical concept IDs | Two-adapter equivalence fixture |
| INV-14 | No Phase 1 execution path loads a neural model or invokes AEE | Dependency and execution inspection |
| INV-15 | Failed ingestion leaves the previous committed store intact | Transaction rollback test |
| INV-16 | Deprecation does not make historical claims or evidence inaccessible | Historical query after Phase 5 deprecation |

## Compatibility rule

If a design cannot preserve an invariant, the change requires an explicit constitution amendment, migration analysis, and updated tests. A faster query or simpler implementation is not sufficient justification for silent semantic loss.

## Relationship to stress tests

The [ontology stress-test specification](../03_ontology/stress_test_specification.md) provides representational cases; this document defines system-wide properties. A stress case can show expressiveness without proving reasoning, calibration, scalability, or safety.

## References

- [Architectural constitution](architectural_constitution.md)
- [Testing strategy](../06_implementation/testing_strategy.md)
- [Logical data model](../04_crs/logical_data_model.md)
