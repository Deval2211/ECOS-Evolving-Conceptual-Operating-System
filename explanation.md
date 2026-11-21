# ECOS Project — Presentation Explanation

## What Is ECOS?

ECOS stands for **Evolutionary Conceptual Operating System**. ECOS is the name of our **modular Small Language Model (SLM) project**. The core idea is:

> ECOS separates language understanding from reasoning. It operates on semantics (concepts, claims, relationships) internally, not raw natural language.

ECOS has a modular architecture:

| Module | Role | Status |
|--------|------|--------|
| **CRS — Concept Representation System** | The core: stores concepts, claims, evidence, provenance, temporal data | ✅ Built & tested |
| **Language Adapter** | Converts natural language (EN/HI/GU) → CRS semantics | ⚠️ Rule-based version built |
| **Reasoning Engine** | Symbolic reasoning over CRS concepts | ⚠️ Prototype built |
| **Cognitive Supervisor** | Contradiction triage, source reliability, UNKNOWN alerts | ⚠️ Prototype built |
| **Concept Evolution Engine** | Non-destructive concept refinement and splitting | ⚠️ Prototype built |
| **Neural Reasoning Core + Decoder** | Full neural SLM completion (planned) | 🔲 Planned (next phase) |

**CRS is the core of ECOS.** We built CRS completely. The full SLM (neural language encoders/decoders + neural reasoning) is the planned completion we will work on next.

---

## What Is Built: CRS Core (Working Prototype)

The `src/` directory contains a working **CRS prototype** — the core of ECOS — implemented in Python 3.11 standard library + SQLite + JSON.

### Source Code (`src/`)

| File | Purpose |
|------|---------|
| `models.py` | Record dataclasses (Concept, Claim, Entity, Source, Provenance, TemporalWindow, EpistemicState, Polarity, etc.) |
| `engine.py` | SQLite storage, validation, actor-based auth, queries (concepts, claims, temporal, vector search, provenance trace) |
| `language_adapter.py` | Rule-based text parser (EN/HI/GU) that converts sentences into structured CRS claims |
| `reasoning.py` | Symbolic reasoning: default/exception inheritance, deductive rules, auto-contradiction detection |
| `supervisor.py` | Cognitive supervision: source reliability scoring, contradiction triage, UNKNOWN safety alerts |
| `evolution.py` | Concept evolution: non-destructive REFINE, polysemy SPLIT with lineage edges |
| `seed.py` | Demo data seeding (cat/water/milk, John/Mary, car temporal colors, Pluto planet reclassification) |
| `extra_data.py` | Extended demo data (medical, scientific, multilingual concepts) |
| `server.py` | HTTP web server with frontend UI for live CRS demonstration |
| `test_crs.py` | 13 unit tests — all passing (concepts, entities, events, temporal queries, contradiction preservation, UNKNOWN invariant, provenance traversal, concept evolution, AEE write-block, vector search, reasoning, supervisor, evolution) |
| `static/` | Frontend HTML/CSS/JS for the web UI |
| `ecos_crs.db` | SQLite database file |

### Key CRS Features (Demonstrated & Tested)

- **Concepts with stable IDs** and multilingual labels (English, Hindi, Gujarati)
- **Claims with temporal validity** — valid time vs transaction time (time-travel queries)
- **Evidence and provenance** — every claim traces back to its source
- **Contradiction preservation** — conflicting claims stay on record instead of being deleted
- **UNKNOWN ≠ False** — an unknown state is not treated as a denial
- **Bounded graph traversal** — directional, depth-limited path finding
- **Supplied-vector similarity** — cosine search on stored embeddings
- **Atomic transactions** — batch ingestion rolls back entirely on any invalid record
- **Deterministic export and restart** — SQLite store can be exported and reloaded identically


## The PDF/PPT (Needs Updating)

The file **"Modular Small Language Model (SLM)- A Scalable Multilingual Reasoning System.pdf"** is the original 10-slide proposal. It was written for a neural SLM vision, but **ECOS is the actual project name** and **CRS is the core we built**. The PDF needs to be updated to reflect this:

| Slide | Current PDF Content | What It Should Say for ECOS |
|-------|---------------------|------------------------------|
| 1 | Modular SLM cover | **ECOS — Evolutionary Conceptual Operating System** (SLM project name) |
| 2 | LLM problems | Monolithic LLMs bind reasoning to language; ECOS separates them via CRS |
| 3 | SLM objectives | Build CRS core first; add neural language adapters later to complete the SLM |
| 4 | Neural architecture | **CRS at center**: Language Adapter → CRS → Query → Reasoning → Decoder |
| 5 | 9-step neural workflow | **CRS workflow**: JSON input → validate → store → query → export/restart |
| 6 | PyTorch/GPU stack | **Current**: Python stdlib + SQLite. **Planned**: PyTorch + GPU for neural SLM |
| 7 | GPU justification | CRS runs on CPU. GPU needed only for future neural SLM phase |
| 8 | SLM outcomes | **Working CRS prototype**: 13 tests passing, temporal reasoning, contradiction preservation |
| 9 | Future scope | **Roadmap**: CRS (done) → Reasoning → Supervisor → Learning → Evolution → Neural SLM |
| 10 | Conclusion | CRS proves the concept; full SLM completion is the next phase |

**Bottom line for the PDF:** The SLM is the project. CRS is the core we built. We are showing the working CRS prototype now and planning to complete the full SLM (neural encoders/decoders + neural reasoning) in the next phase.


## How to Explain This in Your Presentation (College External Review)

### Opening (30 seconds)
"ECOS is our modular Small Language Model project. The full SLM has a neural reasoning core with plug-in language encoders and decoders. We built the CRS — the Concept Representation System — which is the core of ECOS. CRS stores concepts, claims, evidence, and provenance without using natural language internally. We're showing the working CRS prototype now, and we plan to complete the full neural SLM in the next phase."

### What We Built — CRS Core (1 minute)
"We implemented CRS in Python with SQLite. It handles concepts with stable IDs and multilingual labels (English, Hindi, Gujarati). It stores claims with timestamps — so you can ask what was true on a specific date. It preserves contradictions — if two sources disagree, both claims stay on record with their sources. It distinguishes 'unknown' from 'false' — an unknown allergy is not the same as no allergy. All 13 unit tests pass."

### What We Plan — Full SLM Completion (1 minute)
"The CRS is the foundation. To complete the SLM, we will add: neural language encoders and decoders (plug-in per language), a neural reasoning core on top of CRS, and GPU-based training. Adding a new language then only requires training a small adapter module, not retraining the whole model. This reduces compute cost by ~70% compared to full retraining."

### The Gap / Honest Status (30 seconds)
"The current CRS prototype runs on a local CPU with Python standard library + SQLite — no GPU needed. The full neural SLM requires GPU training (~150 GPU-hours estimated) and multilingual datasets. That's our planned next phase."

### Closing
"CRS proves the architecture works. The full modular SLM is the next step. With continued development, ECOS can be a practical language-independent multilingual AI system."

## Team

- **Deval Shah** — 23AIML065
- **Parth Panara** — 23AIML040
- **Guide:** Niyati Patel
- **Department:** AIML, CHARUSAT
- **Project:** ECOS — Evolutionary Conceptual Operating System (Modular SLM)
- **Core Built:** CRS — Concept Representation System
- **Status:** Semester-end external review, November 2026
