# ECOS Ontology and Core Data Model — Working Draft

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0-draft  
**Status:** Proposed design; not the missing Ontology v0.1/v0.2 and not implemented  
**Purpose:** Provide a minimal, explicit conceptual model for Phase 1 review and prototyping.  
**Last reviewed:** 2026-11-20

## Modeling principles

- A **concept** identifies something; a **claim** says something about it.
- Claims are first-class records so provenance, context, polarity, time, and assessments do not have to be squeezed onto an edge.
- Labels are language-tagged annotations; stable IDs carry identity.
- Unknown is not false. Explicit denial uses claim polarity.
- Contradictory assertions are retained. Detection and resolution belong to later phases.
- Valid time describes the modeled world; transaction time describes ECOS’s record.
- Vector representations are derived retrieval data, not semantic or epistemic authority.

## Core record types

### 1. Concept

| Field | Requirement | Meaning |
|---|---|---|
| `id` | Required, stable | Opaque unique identifier such as `concept:<uuid>` |
| `kind` | Required | `category`, `entity`, `event_type`, `relation`, `context`, or `framework` |
| `labels` | Required, may be empty | List of `{text, language}`; labels are non-unique annotations |
| `definition` | Optional | Human-readable definition, not a formal proof of meaning |
| `schema_version` | Required | Exchange-model version |
| `created_at` | Required | Transaction timestamp |
| `status` | Required | Initially `active`; other lifecycle behavior is deferred |

A relation is itself a concept, allowing its definition, domain/range guidance, labels, and provenance to be inspected. Domain/range checks are validation aids, not inference.

### 2. Claim

| Field | Requirement | Meaning |
|---|---|---|
| `id` | Required | Immutable claim identifier |
| `subject_ref` | Required | Concept or claim being described |
| `predicate_ref` | Required | Relation concept |
| `object` | Required | `{concept_ref}` or `{literal_value, datatype, unit_ref?}` |
| `polarity` | Required | `affirm` or `deny` |
| `context_ref` | Required | Context, including a default explicitly named context |
| `valid_time` | Optional | Interval/instant plus precision and calendar where known; absent means not asserted |
| `recorded_at` | Required | Transaction timestamp |
| `provenance_ref` | Required | Extraction or assertion event |

The object union must be discriminated explicitly in serialized JSON; a string must not ambiguously mean either an ID or literal. Phase 1 stores claims without automatically deciding whether they are true.

### 3. Context and Framework

A **Context** has `id`, optional description, optional `framework_ref`, optional assumption claim references, and optional spatial/temporal scope. A **Framework** has `id`, version, definition, and optional references to formal rule sets. A context groups interpretive assumptions; it does not make incompatible claims magically consistent.

### 4. ProvenanceEvent

Records `id`, `activity_type` (`assert`, `extract`, `transform`, `import`, `assess`), `source_refs`, `agent`, `agent_version`, `started_at`, `ended_at`, and optional input-record references. Source references should include a resolvable locator where available and a content hash for reproducibility.

### 5. EvidenceItem and EvidenceRelation

An **EvidenceItem** contains `id`, `source_ref`, optional locator (for example page or span), optional media type, optional content hash, `acquired_at`, and optional observed time. An **EvidenceRelation** links evidence to a claim using `supports`, `contradicts`, or `mentions`, plus method and creation metadata.

`mentions` does not support truth. `supports` is not proof. Multiple evidence relations may disagree and must remain inspectable.

### 6. Assessment

An assessment targets a claim or derivation and contains `id`, `target_ref`, optional `verdict`, optional `confidence`, `method`, `assessor`, `basis`, and `assessed_at`. If `confidence` is present, all qualification fields are mandatory. Confidence is an assessment, not an inherent property of the claim.

### 7. VectorRecord

Contains `id`, `target_ref`, numeric `values`, `dimensions`, `metric`, producer name/version, source provenance, and `created_at`. Dimension count must match the vector length. Similarity results must link back to this record and its symbolic target.

### 8. ConceptLineageEvent — reserved

Reserved for Phase 5 operations: `create`, `merge`, `split`, `refine`, and `deprecate`, with inputs, outputs, rationale, actor, time, and migration mapping. Phase 1 may version the schema to accommodate this record but must not implement evolution behavior.

## Minimal JSON shape

```json
{
  "id": "claim:example-1",
  "subject_ref": "concept:cat",
  "predicate_ref": "relation:drinks",
  "object": {"concept_ref": "concept:water"},
  "polarity": "affirm",
  "context_ref": "context:default",
  "valid_time": null,
  "recorded_at": "2026-11-20T00:00:00Z",
  "provenance_ref": "provenance:fixture-1"
}
```

This is an illustrative exchange shape, not evidence of a running parser or a real-world fact.

## Phase 1 validation rules

1. IDs and references are non-empty and resolve to the expected record type.
2. A claim object is exactly one of concept reference or typed literal.
3. Timestamps use explicit timezone-aware ISO 8601 strings; partial dates use a precision field rather than fabricated times.
4. Numeric values declare datatype and, where applicable, a unit concept.
5. Vector dimensions and values agree; similarity uses a declared metric.
6. Every mutation is transactional; a failed batch does not partially ingest.
7. Claims and evidence are not destructively updated or deleted by the prototype.

## Deliberately unresolved

- Identity resolution across datasets and languages.
- Formal semantics and allowed rule sets for each relation.
- Calibration and aggregation of confidence.
- Temporal vagueness beyond interval bounds and precision.
- Merge/split semantics and historical query rewriting.
- Formal context inheritance and framework composition.
- Mapping to RDF reification, RDF-star, named graphs, or AtomSpace without losing semantics.

See [open research questions](../05_research/open_research_questions.md), [logical data model](../04_crs/logical_data_model.md), and the W3C-informed [provenance model](../04_crs/provenance_model.md).
