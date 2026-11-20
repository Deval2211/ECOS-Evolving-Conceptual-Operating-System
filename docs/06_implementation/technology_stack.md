# ECOS Initial Technology Stack

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed stack; external candidates researched, no ECOS integration tested  
**Purpose:** Select the minimum reproducible Phase 1 stack and defer dependencies that have no current workload.  
**Last reviewed:** 2026-11-20

## Recommended baseline

**Python 3.11+ standard library + SQLite + JSON + `unittest`.** Use dataclasses for records, `sqlite3` for persistence, `json` for exchange, `math` for vector metrics, `pathlib` for files, and `unittest` for checks. No runtime package installation is required for the proposed prototype.

## Evaluation matrix

| Technology | Why and component | Advantages | Limitations | Integration complexity | Necessary in Phase 1? |
|---|---|---|---|---|---|
| **Python** | Models, adapters, validation, storage, graph, vectors, CLI, tests | Readable fixtures and fast iteration; standard library covers the slice | Not a systems-language performance choice; scaling needs evidence | Low | **Yes** |
| **C++** | Possible later performance work or native AtomSpace integration | Native control and direct AtomSpace API | Slower initial iteration and more build/tooling complexity | High for the prototype | **No** |
| **SQLite** | Canonical Concept Memory | Local atomic persistence and easy inspection; standard Python driver | No native hypergraph or distributed query; JSON payloads need validation | Low | **Yes** |
| **JSON** | Versioned exchange and deterministic export | Debuggable, portable, preserves record unions explicitly | Schema must be enforced in application code | Low | **Yes** |
| **AtomSpace** | Candidate typed-hypergraph query/rewrite substrate | Native Atoms, pattern matching, rewriting, Values[1] | Native dependencies, storage modules, API/deprecation issues, AGPLv3+exception review, custom ECOS layers[14][15] | High | **No; spike later** |
| **RDFLib** | RDF/SPARQL import-export evaluation | Python-native RDF ecosystem and standards interop[5] | Claim/context/time/evidence conventions still custom | Medium | **No; optional export spike** |
| **Graph databases** | Future large/concurrent traversal or backend requirement | Managed indexes and graph query capabilities | Operations and another canonical-store risk; no measured need | Medium–high | **No** |
| **Vector databases** | Future large neural embedding indexes | Approximate search and scale when justified | Unnecessary service/dependency; scores remain non-epistemic | Medium | **No** |
| **PyTorch** | Phase 7 neural inference/training and embeddings | GPU tensor/model ecosystem | No Phase 1 neural workload; heavy dependency | Medium | **No** |
| **Hugging Face** | Phase 7 model/dataset access and adapter experiments | Broad model/tooling ecosystem | Model/version/provenance and reproducibility must be managed | Medium | **No** |
| **Jupyter** | Interactive evaluation and experiment narratives | Useful inspection and reproducible notebooks | Not required for the deterministic CLI/core | Low | **Optional, not core** |
| **Kaggle** | Hosted notebook GPU for bounded later experiments | Preconfigured accelerator environment[8] | Account gates, queues, quotas, session/storage limits; no Phase 1 GPU need[9][16] | Low–medium | **No** |
| **NetworkX / FAISS / Neo4j** | Legacy stack suggestions for graph/vector work | Useful if measured graph analysis or index scale emerges | Dependencies without a current requirement | Low–medium | **No** |
| **Mamba** | Legacy long-term memory hypothesis | Possible future sequence-state research | Unspecified need and conflicts with non-neural first milestone | High | **No** |

## Dependency policy

A new dependency needs a named requirement, a failing or inadequate baseline, a small evaluation, and a removal/exit path. Prefer an export boundary over making an external store canonical. Pin versions for experiment code and record adapter/model provenance for any later neural work.

## Future conditional additions

- **RDFLib:** when RDF/SPARQL interchange is required and a lossless mapping is demonstrated.
- **AtomSpace:** when native hypergraph matching/rewriting demonstrates enough value to cover its costs.
- **Hyperon:** when Phase 2 has a concrete MeTTa comparison to run.[34]
- **PyTorch/Hugging Face/Kaggle:** when Phase 7 has bounded neural experiments and model/data governance.[8]
- **Graph/vector services:** only after measured volume, concurrency, or latency requirements.

## Verification gap

No stack component has been integrated into ECOS because no ECOS code exists. The baseline is a design recommendation; its first verification is the clean-checkout prototype demonstration defined in the [implementation roadmap](implementation_roadmap.md).

## Sources

[1] https://github.com/opencog/atomspace
[5] https://github.com/RDFLib/rdflib
[8] https://www.kaggle.com/docs/notebooks
[9] https://www.kaggle.com/docs/efficient-gpu-usage
[14] https://raw.githubusercontent.com/opencog/atomspace/master/LICENSE
[15] https://raw.githubusercontent.com/opencog/atomspace/master/CMakeLists.txt
[16] https://www.kaggle.com/product-announcements/735239
[34] https://raw.githubusercontent.com/trueagi-io/hyperon-experimental/main/README.md
