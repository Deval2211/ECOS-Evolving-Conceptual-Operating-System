# ECOS Ontology Stress-Test Specification — Working Draft

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0-draft  
**Status:** Proposed test design; no cases executed  
**Purpose:** Define repeatable representational and behavioral checks for the ontology working draft and CRS prototype.  
**Last reviewed:** 2026-11-20

## Test protocol

For each case, record fixture version, input records, operation, expected output, actual output, environment, implementation revision, and reviewer. A case passes only when actual output meets the oracle. A design-review expectation is not a result.

The Phase 1 suite runs against a fresh local store and again after restart. Each mutation case also checks that invalid input rolls back without changing committed data.

## Case matrix

| ID | Fixture and operation | Acceptance oracle | Capability tested |
|---|---|---|---|
| ST-01 | Add `cat drinks water` as structured claim | Exact subject/predicate/object round trip | Basic representation |
| ST-02 | Add English, Hindi, and Gujarati labels to one concept | One ID; all labels retained; no language-based merge | Labels versus identity |
| ST-03 | Represent a purchase with buyer, seller, item, price, and time roles | All roles and values remain addressable | N-ary event structure |
| ST-04 | Store no claim about A; separately store explicit denial of B | Query distinguishes unknown from denied | Open-world semantics |
| ST-05 | Store two different objects for a functional relation in one context | Both claims remain; no automatic winner | Conflict preservation |
| ST-06 | Store affirmation and denial of the same relation | Both remain with separate IDs and provenance | Polarity conflict |
| ST-07 | Store incompatible claims under different contexts | Contexts remain explicit; no false global contradiction report | Context sensitivity |
| ST-08 | Import a claim through two transformations | Both provenance events and original source are recoverable | Provenance chain |
| ST-09 | Attach one supporting and one contradicting evidence item | Typed evidence links remain distinct | Evidence pluralism |
| ST-10 | Submit bare confidence `0.98` | Validation rejects it; store unchanged | Qualified uncertainty |
| ST-11 | Record an event valid yesterday but ingested today | Valid and transaction dates remain distinct | Bi-temporal model |
| ST-12 | Record a date known only to month precision | No fabricated day or timezone | Temporal precision |
| ST-13 | Rename a concept label | ID and claim references remain unchanged | Stable identity |
| ST-14 | Review a hypothetical two-way concept split | Lineage requirements documented; no Phase 1 behavior claimed | Future evolution readiness |
| ST-15 | Query vectors for a claim with low evidential support | Similarity output has no truth/verdict promotion | Vector/epistemic separation |
| ST-16 | Traverse a cyclic graph with depth bound | Deterministic finite result; no infinite loop | Safe traversal |
| ST-17 | Submit a dangling object reference | Batch rejected and prior store unchanged | Referential integrity |
| ST-18 | Assess an existing claim | Assessment points to claim without altering it | Higher-order metadata |
| ST-19 | Add a quantity with datatype and unit | Value and unit survive exactly; incompatible unit query is rejected | Quantified knowledge |
| ST-20 | Interpret one claim under two explicit frameworks | Outputs name different assumptions and frameworks | Framework representation |

## Execution levels

- **L0 — Document review:** a human checks whether the model can express the fixture. This is conceptual evaluation and must be labeled as such.
- **L1 — Serialization test:** code validates and round-trips the fixture.
- **L2 — Behavioral test:** storage, query, rollback, and restart behavior meet the oracle.
- **L3 — Comparative experiment:** ECOS is compared with a defined baseline on effort, fidelity, and query results.

Only L1–L3 involve execution. L3 additionally requires a declared baseline and analysis; it is not required for the first prototype.

## Required outputs

1. Machine-readable fixtures.
2. Expected JSON or query results.
3. Test logs and implementation revision.
4. A result table with `not_run`, `pass`, `fail`, or `blocked` for every case.
5. A findings report separating representation defects, implementation defects, and unresolved semantics.

## Non-goals

These tests do not establish universal conceptual coverage, language independence, commonsense reasoning, confidence calibration, scalability, or safety. ST-14 is a design-readiness review only because concept evolution is deferred to Phase 5.

## References

- [Findings status](stress_test_findings.md)
- [Architectural invariants](../02_architecture/architectural_invariants.md)
- [Testing strategy](../06_implementation/testing_strategy.md)
