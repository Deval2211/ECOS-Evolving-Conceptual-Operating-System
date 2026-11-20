# ECOS — Evolutionary Conceptual Operating System

- **Document version:** 0.1.0
- **Status:** Proposed architecture; documentation and research only
- **Purpose:** Provide the project introduction and authoritative documentation navigation.
- **Last reviewed:** 2026-11-20

ECOS is a **proposed** language-independent-by-design, concept-driven cognitive AI architecture. Its goal is to represent, retrieve, reason about, verify, learn, and eventually evolve structured conceptual knowledge without using natural language as the canonical internal representation.

> **Current status:** documentation and research only. No ECOS implementation, executed cognitive capability, or validated experimental result is present in this repository.

## Start here

**[Open the documentation guide](docs/README.md)**

Key documents:

- [Source audit](docs/source_audit.md) — actual repository material, missing named sources, and conflicts.
- [Project status and evidence taxonomy](docs/project_status.md) — what is proposed, implemented, demonstrated, and validated.
- [Project overview](docs/01_overview/project_overview.md) and [scope](docs/01_overview/project_scope.md).
- [Complete architecture](docs/02_architecture/complete_architecture.md) and [phase roadmap](docs/02_architecture/phase_roadmap.md).
- [Ontology working draft](docs/03_ontology/ontology_working_draft.md).
- [CRS architecture working draft](docs/04_crs/crs_architecture_working_draft.md).
- [AtomSpace evaluation](docs/05_research/atomspace_evaluation.md) and [build versus reuse](docs/05_research/build_vs_reuse.md).
- [Phase 1 implementation roadmap](docs/06_implementation/implementation_roadmap.md).
- [Kaggle GPU setup](docs/07_compute/kaggle_gpu_setup.md).
- [Documentation report](docs/08_project_management/documentation_report.md).

## Architectural direction

The current eight-phase roadmap is:

1. **Foundation:** controlled language adapter, concept extractor, Concept Representation System (CRS), Concept Graph, Concept Memory, Vector Memory, and Query Engine—without neural networks.
2. **Reasoning:** explicit logical, mathematical, temporal, spatial, causal, analogical, and commonsense methods over conceptual records.
3. **Cognitive Supervisor:** confidence, contradictions, missing knowledge, alternatives, evidence, and verification.
4. **Learning Engine:** evidence acquisition and auditable knowledge integration.
5. **Concept Evolution Engine:** concept creation, merge, split, refinement, deprecation, and lineage.
6. **Reflection Engine:** explicit contexts, frameworks, and alternative interpretations.
7. **Neural Language Adapters:** replaceable neural translation into and out of CRS.
8. **Architecture Evolution Engine:** controlled future research into architectural improvement.

**Capability must precede autonomy.** The Architecture Evolution Engine is excluded from the initial implementation.

## Initial engineering target

The proposed first prototype is deliberately small: Python standard library, JSON, and SQLite; controlled structured input; durable concepts, claims, evidence, and provenance; deterministic symbolic and supplied-vector queries; restart and export tests. It does not include unrestricted NLP, neural models, automated reasoning, continual learning, or self-modification.

See [prototype requirements](docs/06_implementation/prototype_requirements.md) and the [first ten implementation tasks](docs/06_implementation/implementation_roadmap.md#first-ten-implementation-tasks). No implementation should begin without approval of this scope.

## Legacy material

The original repository documents remain available as historical proposals:

- [Legacy architecture](ARCHITECTURE.md)
- [Legacy development phases](PHASE.md)
- [Legacy timeline and hardware assumptions](TIMELINE.md)
- [Modular Small Language Model proposal](<Modular Small Language Model (SLM)- A Scalable Multilingual Reasoning System.pdf>)

These sources use the earlier “Evolving Conceptual Operating System” expansion and a different neural/Mamba roadmap. They are preserved as history, not treated as the new baseline or as evidence of running software. The six ontology/CRS documents named in the documentation assignment were **not found**; see the [source-availability record](docs/03_ontology/source_availability.md).

## Documentation conventions

Markdown and Mermaid are used throughout. The repository can be opened directly as an Obsidian vault; no Obsidian-specific setup is required. External research includes retrieval dates and citations, and changing infrastructure facts—especially Kaggle availability—must be rechecked before use.

## License

`TBD`. No license has been selected, and no `LICENSE` file has been inferred or created. The project owner must make this decision before public release or dependency integration. See [D-014](docs/08_project_management/decision_log.md).
