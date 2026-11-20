# ECOS Development Setup — Planned

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed setup instructions; source files do not yet exist  
**Purpose:** Define a minimal, reproducible setup for the approved CRS prototype without implying it already runs.  
**Last reviewed:** 2026-11-20

## Prerequisites

- Python 3.11 or newer with `venv`, `sqlite3`, and `unittest` available.
- Git.
- A local CPU machine; no GPU, Kaggle account, database server, or API key.

Check the interpreter and SQLite module:

```bash
python3 --version
python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
```

These checks inspect the environment only; they do not indicate ECOS is installed.

## Planned clean-checkout workflow

After the prototype source is implemented:

```bash
git clone <project-url> ECOS
cd ECOS
python3 -m venv .venv
. .venv/bin/activate
PYTHONPATH=src python -m unittest discover -s tests -v
```

No third-party dependency installation is planned for the first slice. If packaging metadata is added later, document its build requirements rather than assuming editable installation is dependency-free.

## Planned demonstration

The target interface is one deterministic command such as:

```bash
PYTHONPATH=src python -m ecos.cli demo \
  --fixture tests/fixtures/basic_claims.json \
  --database /tmp/ecos-demo.sqlite \
  --output /tmp/ecos-demo-output.json
```

This command is a **contract for implementation**, not an executable instruction today. The completed implementation must update this section with its actual CLI and verified output.

## Development rules

1. Write validation and a failing fixture before each storage/query behavior.
2. Use temporary databases in tests; never commit generated SQLite files or outputs.
3. Keep source records immutable through the public API.
4. Record actual commands and results in the relevant findings/changelog entry.
5. Do not add dependencies without updating [technology stack](technology_stack.md) and [build versus reuse](../05_research/build_vs_reuse.md).
6. Do not add neural, reasoning, learning, reflection, or AEE placeholders to the prototype.

## Optional later environments

- **RDF spike:** isolated virtual environment with a recorded RDFLib version and round-trip fixtures.
- **AtomSpace spike:** persistent Linux/Docker environment with pinned CogUtil, AtomSpace, and storage-module revisions; separate from the clean baseline.[1]
- **Neural experiments:** separate dependency manifest and model/version provenance; Kaggle may be used only within its current access and usage rules.[8]

## Current repository state

As of 2026-11-20, the repository contains documentation and legacy proposal files only. The setup becomes actionable after the first implementation tasks are approved and completed. See [implementation roadmap](implementation_roadmap.md).

## Sources

[1] https://github.com/opencog/atomspace
[8] https://www.kaggle.com/docs/notebooks
