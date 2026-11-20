# ECOS CRS Storage Architecture

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0-draft  
**Status:** Proposed storage design; no database created or benchmarked  
**Purpose:** Choose a minimal durable Phase 1 store while preserving future migration options.  
**Last reviewed:** 2026-11-20

## Recommendation

Use one local SQLite database through Python’s standard-library `sqlite3`. It is sufficient for small transactional fixtures and avoids introducing a graph server before query requirements justify one. JSON columns hold variable temporal, label, provenance, and vector payloads after application validation; frequently filtered references remain typed columns.

## Logical tables

| Table | Important fields / indexes |
|---|---|
| `records` | `id` primary key, `record_type`, `schema_version`; central reference target |
| `concepts` | `id`, `kind`, `labels_json`, `definition`, `created_at`, `status`; index `(kind)` |
| `contexts` | `id`, `framework_ref`, `payload_json` |
| `frameworks` | `id`, `version`, `definition`, `payload_json` |
| `provenance_events` | `id`, `activity_type`, `agent`, `agent_version`, `payload_json` |
| `claims` | `id`, `subject_ref`, `predicate_ref`, `object_type`, `object_ref`, `literal_json`, `polarity`, `context_ref`, `valid_time_json`, `recorded_at`, `provenance_ref`; indexes on subject, predicate, object, context |
| `evidence_items` | `id`, `source_ref`, `provenance_ref`, `locator_json`, `content_hash`, `payload_json` |
| `evidence_relations` | `id`, `evidence_ref`, `claim_ref`, `relation_type`, `method_json`; indexes on claim and evidence |
| `assessments` | `id`, `target_ref`, `method`, `assessor`, `basis`, `assessed_at`, `verdict`, `confidence`, `payload_json` |
| `vector_records` | `id`, `target_ref`, `values_json`, `dimensions`, `metric`, `producer`, `producer_version`, `provenance_ref`; index on target |
| `schema_metadata` | Store schema version, creation revision, migration history |

This is a logical schema, not a request to create all indexes blindly. The prototype can create the listed reference indexes because they directly support required queries; further optimization waits for measurement.

## Integrity and transactions

- Enable foreign-key enforcement for every connection.
- Register every ID in `records`; references use that registry where practical.
- Validate relation-kind, discriminated unions, timestamps, and vector dimensions in application code before commit.
- Execute one ingestion batch in one transaction. Any error rolls back the entire batch.
- Treat claim/evidence immutability as a repository contract covered by tests; database triggers can be added if direct SQL writes must be supported.
- Keep raw source content outside the database when large, but retain its locator and content hash.

## JSON and canonical export

SQLite JSON storage is an implementation convenience, not the canonical exchange format. Export uses deterministic key ordering and record ordering, preserves literal lexical values, and includes schema version. JSON floats must not be used for exact decimal quantities where exactness matters; retain the lexical value and datatype.

## Projections

Graph adjacency is computed from claims. The initial Vector Memory scans a small table and computes the declared metric in Python. Both projections can be rebuilt from canonical records. A vector index or graph server is introduced only after a measured workload exceeds this simple design.

## Backup and migration

A prototype demonstration must close and reopen the database successfully. Before schema changes, export the complete store and test loading it into the new schema. Never drop unknown columns or records during migration; report them explicitly.

## Alternatives and upgrade triggers

- **RDFLib/RDF store:** evaluate when standards-based interchange or SPARQL is a demonstrated requirement.
- **AtomSpace:** evaluate when typed hypergraph pattern matching and rewriting justify its build and integration cost.
- **Dedicated graph database:** evaluate after measured traversal, concurrency, or scale limits.
- **Vector database:** evaluate after measured vector volume/latency requirements; not for a handful of fixtures.

## References

- [Logical data model](logical_data_model.md)
- [Build versus reuse](../05_research/build_vs_reuse.md)
- [Development setup](../06_implementation/development_setup.md)
