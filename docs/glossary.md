# ECOS Glossary

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed terminology baseline  
**Purpose:** Keep technical language consistent across architecture, ontology, research, and implementation.  
**Last reviewed:** 2026-11-20

| Term | ECOS meaning |
|---|---|
| ECOS | **Evolutionary Conceptual Operating System**, a proposed architecture—not a conventional operating system kernel. |
| CRS | **Concept Representation System**: the substrate for concepts, claims, relationships, evidence, memory, and queries. |
| Concept | A stable, language-independent-by-design identity for a category, entity, event type, relation, context, or framework. “Independent” is a design goal, not a demonstrated universal semantics. |
| Concept Graph | A graph view derived from concepts and claim relationships; it is not the whole CRS. |
| Claim | An immutable, identified assertion with a subject, predicate, object, polarity, context, and provenance. A claim can be disputed without being deleted. |
| Epistemic layer | Information about assertion, evidence, confidence, and assessment—distinct from the factual content asserted. |
| Evidence | A source-backed item linked to claims by typed relations such as `supports` or `contradicts`. Evidence is not automatically proof. |
| Provenance | The origin and processing history of a claim, concept, vector, or assessment, including source locators and acquisition times. |
| Contradiction preservation | Retaining incompatible claims and their contexts rather than silently overwriting one with another. Detection is a later capability. |
| Confidence | An optional bounded assessment associated with a method, assessor, basis, and time. It is not automatically calibrated probability. |
| Context | Explicit assumptions and scope that affect a claim’s interpretation. |
| Framework | A named collection of definitions, rules, or interpretive assumptions used during reasoning or reflection. |
| Valid time | When a claim is asserted to hold in the modeled world; distinct from when ECOS records it. |
| Transaction time | When ECOS records, revises an assessment of, or stops using an item. |
| Concept lineage | Links among concept versions and operations such as split, merge, refinement, and deprecation; reserved for Phase 5 behavior. |
| Concept Memory | Durable symbolic storage for concepts, claims, evidence, contexts, and associated metadata. |
| Vector Memory | Numeric vectors linked to symbolic IDs with explicit model and distance provenance; subordinate to the symbolic record. |
| Query Engine | Exact lookup, filtering, bounded traversal, evidence retrieval, and optional vector similarity over stored records; not automated reasoning. |
| Language Adapter | Translation between an external representation and CRS input/output. Phase 1 uses structured or controlled input, not unrestricted neural translation. |
| Cognitive Supervisor | Phase 3 component intended to evaluate reasoning, evidence, missing knowledge, and contradictions. |
| AEE | **Architecture Evolution Engine**, a Phase 8 research topic for controlled architectural improvement. It is excluded from the initial implementation. |
| Open-world assumption | Absence of a stored claim does not imply that the claim is false. |
| Reification | Representing a statement as an identified object so provenance and assessments can refer to it. |
| Hypergraph | A generalization in which a relation can connect an ordered collection of atoms rather than only two vertices. |
| Bi-temporal model | Separate tracking of valid time and transaction time. |

## Naming rule

Use “conceptual” for the representation, “semantic core” only when referring to legacy documents, and “language-independent-by-design” rather than claiming that universal or culture-independent meaning has been achieved.
