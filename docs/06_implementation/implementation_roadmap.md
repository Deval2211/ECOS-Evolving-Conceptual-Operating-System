# ECOS Phase 1 Implementation Roadmap

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed implementation plan; no code approved or written by this documentation task  
**Purpose:** Define a small vertical CRS prototype, its first ten tasks, resources, and completion criteria.  
**Last reviewed:** 2026-11-20

## Prototype scope

Build a local, single-writer CRS that accepts a versioned controlled JSON envelope; stores concepts, claims, contexts, provenance, evidence, and supplied vector records in SQLite; and supports deterministic lookup, filtering, bounded traversal, evidence retrieval, vector similarity, export, and restart. It must preserve conflicting claims and distinguish valid time from transaction time.

No unrestricted NLP, reasoning, verification, learning, concept evolution, reflection, neural adapter, or AEE behavior is included.

## Proposed repository structure

```text
src/ecos/
├── __init__.py
├── models.py          # Record dataclasses and explicit object union
├── validation.py      # Trust-boundary checks
├── storage.py         # SQLite schema, transactions, export
├── graph.py           # Adjacency and bounded traversal
├── vectors.py         # Supplied-vector storage and metrics
├── adapters.py        # Controlled JSON adapter/extractor
├── queries.py         # Query contracts and result envelopes
└── cli.py             # Small ingest/query/demo entry point

tests/
├── fixtures/
│   ├── basic_claims.json
│   ├── conflicts.json
│   ├── temporal.json
│   └── invalid_records.json
├── test_validation.py
├── test_storage.py
├── test_graph.py
├── test_vectors.py
└── test_demo.py
```

This is a proposed layout, not existing source. Keep storage and query code separate so a later RDFLib or AtomSpace spike does not rewrite ontology tests.

## First ten implementation tasks

| # | Task | Required check |
|---|---|---|
| 1 | Freeze the initial exchange fixture and record the schema decision | Review valid and invalid examples against ontology fields |
| 2 | Implement record dataclasses, JSON parsing, discriminated objects, and validation | Valid round trip; missing refs, bare confidence, bad timestamps, and ambiguous objects rejected |
| 3 | Implement SQLite registry/schema and atomic initialization | Foreign references enforced where practical; reopen test; schema version present |
| 4 | Implement transactional ingestion for concepts, contexts, provenance, evidence, and claims | Duplicate-ID behavior defined; invalid batch rolls back completely |
| 5 | Implement concept lookup and exact claim filters | Stable results and empty-result-is-not-false test |
| 6 | Implement evidence and provenance retrieval | Full source/extraction chain and typed support/contradiction links returned |
| 7 | Implement graph adjacency and bounded deterministic traversal | Incoming/outgoing direction, cycles, polarity, claim IDs, depth/result bounds |
| 8 | Implement supplied-vector records and cosine retrieval | Dimension mismatch and zero vectors rejected; deterministic ties; no verdict in output |
| 9 | Implement controlled adapter, CLI ingestion, and deterministic export | Provenance identifies adapter version; export/import round trip |
| 10 | Run the demonstration and working-draft stress cases; publish actual results | Restart passes; logs linked; stress findings updated case by case with no inferred passes |

## Delivery sequence

- **Vertical slice A (tasks 1–4):** one valid claim and evidence item survives ingestion and restart.
- **Vertical slice B (tasks 5–8):** conflicting claims, provenance, graph paths, and supplied-vector matches are queryable.
- **Vertical slice C (tasks 9–10):** one command reproduces the demo and publishes evidence.

Stop after each slice if the ontology needs correction. Do not build all modules as empty interfaces before the first round trip works.

## Expected demonstration outputs

1. Ingest receipt with schema version, record counts, and transaction status.
2. Two incompatible claims returned separately with provenance.
3. Evidence response containing typed relations and source locators.
4. Temporal response showing different valid and transaction times.
5. Bounded path containing ordered claim IDs.
6. Vector match containing score, metric, producer/version, and symbolic target—without a truth verdict.
7. Post-restart counts and deterministic JSON export.

## Resource requirements

- One developer/researcher for the initial slice; ontology reviewer for semantic decisions.
- Ordinary local CPU development machine with Python 3.11+ and SQLite support.
- Small public synthetic fixtures; no sensitive source data.
- No GPU, cloud account, Kaggle account, graph server, or model download.
- Additional persistent Linux environment only for a later AtomSpace build spike.

## Prototype success criteria

The prototype is successful only when all are demonstrated on a recorded revision:

- Valid controlled input round-trips without semantic loss.
- Invalid input fails atomically without damaging committed records.
- Conflicting claims and their evidence remain separately queryable.
- Unknown, explicit denial, valid time, and transaction time remain distinct.
- Exact, evidence, bounded graph, and supplied-vector queries meet their contracts.
- Restart and deterministic export preserve all records and provenance.
- The demo runs from a clean checkout using documented standard-library commands.
- The stress report records actual results for every in-scope case, including failures.
- The README states the same limitations as the implementation—no hidden reasoning or learning.

## Next decision after success

Measure where the prototype is insufficient. Choose exactly one follow-up: an RDF export spike, an AtomSpace mapping spike, or a narrow Phase 2 logical-reasoning rule. Do not start all three.

## References

- [Prototype requirements](prototype_requirements.md)
- [Testing strategy](testing_strategy.md)
- [Development setup](development_setup.md)
