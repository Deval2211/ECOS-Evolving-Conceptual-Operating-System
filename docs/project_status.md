# ECOS Project Status and Evidence Taxonomy

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Verified project-status statement  
**Purpose:** Distinguish decisions, designs, hypotheses, implementation, demonstration, validation, and open research.  
**Last reviewed:** 2026-11-20

## Current status

ECOS is a **proposed cognitive architecture with legacy conceptual documentation and a new documentation baseline**. The audited repository contains no ECOS implementation or executable experiment. Therefore:

- **Implemented ECOS features:** none verified.
- **Experimentally demonstrated ECOS capabilities:** none verified.
- **Validated ECOS capabilities:** none verified.
- **Current deliverable:** documentation and research only.
- **External software:** AtomSpace, RDFLib, Graphiti, and other reviewed projects have their own implementations; those are not ECOS implementations.

## Required labels

| Label | Meaning | Minimum evidence |
|---|---|---|
| Architectural decision | A selected constraint or direction | Decision-log entry and scope; does not imply code |
| Proposed design | A concrete but unbuilt specification | Document version, dependencies, unresolved questions |
| Research hypothesis | A falsifiable expectation | Proposed experiment and failure criterion |
| Implemented feature | Code exists and can be executed | Revision, path, invocation, and repeatable setup |
| Experimentally demonstrated capability | A specific run produced observed evidence | Inputs, outputs, environment, logs, and limitations |
| Validated capability | Independent checks support a defined claim | Acceptance criteria, test evidence, and review; scope of validity stated |
| Open research question | No justified decision or result yet | Why it matters and what evidence would resolve it |

“Conceptual evaluation” means a human or model reasoned through an example without executing ECOS. It must never be shortened to “test passed.”

## Phase capability status

| Phase | Design status | Implementation status |
|---|---|---|
| 1 — Foundation | Proposed working draft | Not implemented |
| 2 — Reasoning | Research scope only | Not implemented |
| 3 — Cognitive Supervisor | Research scope only | Not implemented |
| 4 — Learning Engine | Research scope only | Not implemented |
| 5 — Concept Evolution Engine | Research scope only | Not implemented |
| 6 — Reflection Engine | Research scope only | Not implemented |
| 7 — Neural Language Adapters | Future research scope | Not implemented |
| 8 — Architecture Evolution Engine | Explicitly deferred investigation | Prohibited from initial implementation |

## Documentation change rule

A status upgrade requires evidence, not prose. When implementation begins, add the revision and test report to the changelog, link the exact demonstration, and retain failed or negative results. Do not retroactively rewrite a proposal to make an experiment look successful.

## Related references

- [Source audit](source_audit.md)
- [Phase roadmap](02_architecture/phase_roadmap.md)
- [Testing strategy](06_implementation/testing_strategy.md)
- [Decision log](08_project_management/decision_log.md)
