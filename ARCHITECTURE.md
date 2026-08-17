# ECOS v1.0 Architecture

## Main Pipeline

```mermaid
flowchart TD
    UI[User Input<br/>Text / Voice / Image / PDF] --> MP[Multimodal Preprocessing<br/>OCR • ASR • Vision • Tokenization]
    MP --> LA[Language Adapter<br/>Detect Language • Normalize • Encode]
    LA --> SE[Semantic Extractor<br/>Entity • Relation • Intent • Event • Temporal]
    SE --> SC[LANGUAGE-INDEPENDENT SEMANTIC CORE]
    SC --> CS[Concept Space<br/>Concept Embeddings • Semantic Graph • Ontology<br/>Entity Graph • Relationship Graph • Memory Index]
    CS --> MC[Meta-Cognition Controller<br/>Need Memory? • Need Reasoning? • Need Search?<br/>Need Tool? • Confidence Check]
    MC --> MM[Mamba Memory Core<br/>Conversation State • User Preferences<br/>Context • Long-term Memory]
    MC --> RE[Reasoning Engine<br/>Logic • Planning • Problem Solving • Decision Making]
    MM --> KR[Knowledge Retrieval<br/>Vector Database • Knowledge Graph<br/>Documents • User Knowledge]
    RE --> KR
    KR --> RP[Response Planning<br/>Final Semantic Representation]
    RP --> LG[Language Generator<br/>Semantic → Natural Language<br/>Target Language Generation]
    LG --> UO[User Output<br/>Text / Speech / Image]
```

## Background Continuous Learning Loop

```mermaid
flowchart TD
    A[User Feedback] --> B[Experience Buffer]
    B --> C[Concept Validator]
    C --> D[Knowledge Graph Update]
    D --> E[Memory Update]
    E --> F[Optional Offline Distillation]
    F --> G[Improved Semantic Core]
```

## Module Architecture

| Module             | Architecture                         |
| ------------------ | ------------------------------------ |
| Language Adapter   | Small Transformer                    |
| Semantic Extractor | Distilled Transformer                |
| Semantic Core      | Vectors + Knowledge Graph + Ontology |
| Meta-Cognition     | Small Policy Network                 |
| Memory             | Mamba                                |
| Reasoning          | Neural + Symbolic                    |
| Knowledge          | Vector DB + Graph DB                 |
| Language Generator | Small Transformer Decoder            |

## Data Flow

```mermaid
flowchart TD
    A[Input] --> B[Language Adapter]
    B --> C[Semantic Extractor]
    C --> D[Semantic Core]
    D --> E[Meta-Cognition]
    E --> F[Memory / Reasoning / Knowledge]
    F --> G[Response Planning]
    G --> H[Language Generator]
    H --> I[Output]
```

## Key Design Idea

The most important design decision is that everything inside ECOS operates on semantics, not language.

- The Language Adapter converts language → semantics.
- The Semantic Core stores concepts and relationships.
- The Reasoning Engine manipulates concepts.
- The Memory stores conceptual state.
- The Language Generator converts semantics → any language.

This means adding a new language only requires a new Language Adapter and Language Generator. The Semantic Core, Memory, Meta-Cognition, and Reasoning Engine remain unchanged, making ECOS naturally scalable and suitable for multilingual operation on resource-constrained devices.