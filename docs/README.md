# ECOS Documentation Guide

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed documentation baseline; ECOS software is not implemented  
**Purpose:** Provide a navigable, evidence-conscious entry point for research and a small Phase 1 CRS prototype.  
**Last reviewed:** 2026-11-20

## Read this first

1. [Source audit](source_audit.md) — what actually exists and which named sources are missing.
2. [Project status and evidence taxonomy](project_status.md) — prevents designs from being mistaken for results.
3. [Project overview](01_overview/project_overview.md) and [scope](01_overview/project_scope.md).
4. [Architectural constitution](02_architecture/architectural_constitution.md) and [complete architecture](02_architecture/complete_architecture.md).
5. [Proposed ontology working draft](03_ontology/ontology_working_draft.md) and [CRS logical model](04_crs/logical_data_model.md).
6. [Implementation roadmap](06_implementation/implementation_roadmap.md) and [prototype requirements](06_implementation/prototype_requirements.md).

## Documentation map

| Area | Contents |
|---|---|
| [01 Overview](01_overview/project_overview.md) | Problem, objectives, scope, and research framing |
| [02 Architecture](02_architecture/complete_architecture.md) | Phases, components, decisions, and invariants |
| [03 Ontology](03_ontology/ontology_working_draft.md) | Proposed conceptual model and unexecuted stress-test assets |
| [04 CRS](04_crs/crs_architecture_working_draft.md) | Concept Representation System design and boundaries |
| [05 Research](05_research/related_projects.md) | AtomSpace, alternatives, related research, and reuse decisions |
| [06 Implementation](06_implementation/implementation_roadmap.md) | Stack, setup, tests, and first ten tasks |
| [07 Compute](07_compute/compute_requirements.md) | CPU-first foundation and current Kaggle GPU guidance |
| [08 Project management](08_project_management/decision_log.md) | Decisions, milestones, risks, and documentation history |

## Authority rules

- The assignment supplied on 2026-11-20 sets the current documentation direction: symbolic foundation first, neural language adapters in Phase 7, and Architecture Evolution Engine only in Phase 8.
- The root `ARCHITECTURE.md`, `PHASE.md`, `TIMELINE.md`, and original `README.md` are legacy sources, not evidence of implementation.
- The six named constitution/ontology/stress-test/CRS documents were not found. The [source audit](source_audit.md) records that gap; no historical findings have been reconstructed as fact.
- External project capabilities belong to their respective projects. Reuse does not make them ECOS capabilities.
- A proposed document becomes normative only through an explicit entry in the [decision log](08_project_management/decision_log.md).

## Working in Obsidian

This directory uses ordinary Markdown, relative links, and Mermaid blocks, so the repository can be opened directly as an Obsidian vault. No Obsidian-specific configuration is required. Standard relative links are preferred over vault-only wikilinks so the same documentation also works on GitHub.

## Immediate next action

Review the [CRS prototype scope](06_implementation/prototype_requirements.md), resolve the open ontology decisions, and approve only the small vertical slice described in the [implementation roadmap](06_implementation/implementation_roadmap.md). Do not start with neural training, a distributed graph platform, or architectural self-modification.
