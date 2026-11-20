# ECOS Project Scope

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed scope boundary  
**Purpose:** Prevent a research prototype from expanding into an unfinished cognitive platform.  
**Last reviewed:** 2026-11-20

## Phase 1 prototype: in scope

- A versioned, validated JSON exchange format for concepts, claims, evidence, contexts, and vector records.
- A structured Language Adapter boundary and deterministic Concept Extractor for the controlled fixture format.
- Local durable Concept Memory and a Concept Graph view derived from claims.
- Exact lookup, filtering, bounded traversal, evidence retrieval, and simple cosine search over supplied vectors.
- Provenance, valid-time versus transaction-time distinction, explicit negation, and contradiction preservation.
- A command-line demonstration and small automated test suite.
- Serialization and restart recovery.

## Explicitly out of scope for the prototype

- Neural networks, model training, fine-tuning, teacher distillation, or foundation-model pretraining.
- Unrestricted natural-language, voice, image, PDF, OCR, or ASR understanding.
- Automated logical, causal, mathematical, spatial, analogical, or commonsense inference.
- Automatic contradiction detection or resolution, calibrated confidence, and verification.
- Autonomous learning, concept merging/splitting, reflection, and framework selection.
- Mamba memory, mobile deployment, distributed storage, multi-user services, and a web UI.
- Architecture Evolution Engine behavior or self-modifying code.
- Claims of language independence, general reasoning, or validated cognitive capability.

## Architectural scope versus prototype scope

The complete eight-phase architecture describes a research direction, not permission to build all phases. Phase 1 includes interfaces that later components can consume, but placeholders must not expose fake behavior. Reserved lineage and assessment fields can be stored without implementing evolution or verification engines.

## Dependency boundary

The recommended prototype uses Python and its standard library, including `sqlite3`, `dataclasses`, `json`, `math`, and `unittest`. AtomSpace and RDFLib are evaluation options, not mandatory runtime dependencies. No graph server, vector database, PyTorch, Hugging Face, or Kaggle account is required for the initial CRS.

## Resource boundary

Target a small local fixture set and a single-writer process. Scalability, concurrency, distributed transactions, and large vector indexes require later benchmarks and explicit decisions; the prototype must not pretend to solve them.

## Approval gate

Implementation should start only after review of the ontology working draft, prototype acceptance criteria, and first ten tasks. The immediate deliverable is one working vertical slice, not a phased big-bang build.
