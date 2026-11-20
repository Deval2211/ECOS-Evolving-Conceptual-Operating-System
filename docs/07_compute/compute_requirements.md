# ECOS Compute Requirements

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed resource model; no ECOS benchmarks or account verification performed  
**Purpose:** Separate CPU-first conceptual infrastructure from later neural workloads that may benefit from accelerators.  
**Last reviewed:** 2026-11-20

## Principle

Phase 1 does not require a GPU. Concepts, claims, evidence, provenance, SQLite transactions, exact filters, bounded graph traversal, JSON export, and small supplied-vector cosine searches are CPU workloads. A GPU would add setup cost without improving the prototype’s acceptance criteria.

## Workload map

| ECOS workload | Compute class | GPU benefit | Recommended environment |
|---|---|---|---|
| Controlled JSON parsing and validation | CPU | None | Local Python |
| Concept Memory and provenance | CPU + local disk | None | Local SQLite |
| Concept Graph construction and bounded traversal | CPU | None for initial fixtures | Local Python/SQLite |
| Exact and evidence queries | CPU + disk | None | Local SQLite |
| Supplied-vector similarity over small records | CPU | Negligible at prototype scale | Local standard-library math |
| Deterministic export and stress tests | CPU + disk | None | Local development machine |
| RDF/AtomSpace evaluation spikes | CPU + native build tools | None for core graph operations | Persistent Linux/Docker, not GPU-first |
| Embedding generation | Neural inference | Potentially useful | Later local GPU or bounded Kaggle notebook |
| Neural language-adapter inference | Neural inference | Potentially useful | Phase 7 experiment environment |
| Adapter experimentation or fine-tuning | Neural training | Often useful, model/data dependent | Phase 7 only after memory/feasibility checks |
| Foundation-model pretraining | Large neural training | Outside current project scope | Not part of the approved roadmap |
| AEE simulation | Unknown future workload | Cannot estimate | Defer until Phase 8 requirements exist |

## Phase 1 resource envelope

Use an ordinary development machine with Python 3.11+, local disk, and enough memory for small fixtures. No defensible RAM, latency, or storage ceiling should be invented before a target dataset exists. The first benchmark must publish record counts, vector dimensions, query shapes, hardware, Python/SQLite versions, and revision.

## When acceleration becomes relevant

GPU evaluation begins only when a neural adapter or embedding workload has a defined model, input size, batch shape, memory requirement, and acceptance metric. First establish a CPU or small-model baseline. Then decide whether Kaggle’s available accelerator is appropriate; do not buy or allocate compute against a vague “AI” requirement.[8]

## Memory and persistence

Two T4 devices in Kaggle’s T4x2 option are separate 16 GB GPUs, not one automatically pooled 32 GB device. Model and data parallelism must be explicit. Kaggle sessions and scratch state are temporary; durable experiment outputs belong in saved notebook output or downloaded artifacts.[8][16]

## Resource risks

- Ontology and integration effort may dominate compute cost.
- Graph pattern complexity can become a CPU problem before large memory is needed.
- Vector dimensions and index size can create memory pressure even without training.
- Ephemeral notebook setup can consume more wall time than the experiment.
- Neural model licensing, dataset size, and output persistence can matter more than GPU availability.

## References

- [Compute strategy](compute_strategy.md)
- [Kaggle GPU setup](kaggle_gpu_setup.md)
- [Technology stack](../06_implementation/technology_stack.md)

## Sources

[8] https://www.kaggle.com/docs/notebooks
[16] https://www.kaggle.com/product-announcements/735239
