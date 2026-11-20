# OpenCog AtomSpace Evaluation for ECOS

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Verified source research; integration is proposed and untested  
**Purpose:** Determine what AtomSpace already provides, what ECOS must build, and whether adoption is justified.  
**Research date:** 2026-11-20  
**Inspected revision:** `c8d633bf272b838c2132c21b7c8ddf169a18dd22` (`master` at inspection), version header `5.2.0`[25][31]

## Executive decision

**Do not make AtomSpace a Phase 1 dependency.** First prove the ECOS claim/evidence model with the small SQLite prototype. AtomSpace is a candidate for a later, bounded spike when native typed-hypergraph pattern matching or graph rewriting is a measured requirement.

AtomSpace already provides an in-RAM typed hypergraph/metagraph store, immutable globally unique Atoms, per-atom Values, a graph pattern engine, and graph rewriting. It does not supply ECOS’s claim semantics, evidence model, contradiction policy, bi-temporal model, concept lineage, or framework semantics as finished features.[1][10]

## Verified capability review

| Area | Current AtomSpace functionality | ECOS implication |
|---|---|---|
| Architecture | In-RAM knowledge-representation database with query and graph-rewriting system; described as a generalized hypergraph/metagraph database[1] | Candidate substrate, not a complete cognitive architecture |
| Atoms and Links | Immutable, globally unique typed Nodes and Links; Nodes can be named, Links contain ordered outgoing Atom sets and Atoms track incoming Links[10] | Stable structure is useful, but ECOS needs separate claim instances even when content repeats |
| Typed hypergraphs | Types and constructors are native; third-party type hierarchies can be declared through the type-extension mechanism[1][24] | ECOS types could be added, but type names alone do not define epistemic semantics |
| Values | Each Atom can hold key-addressed Values; Values are not content-indexed like Atoms and are suitable for transient/streaming data[10] | Searchable claims/evidence should be Atoms, not hidden only in Values |
| Storage | Core is in RAM; `StorageNode` infrastructure is separate, with RocksDB, network, proxy, file, and other modules in related repositories[1][11] | Persistence adds repository and operational choices; verify durability and query behavior in a spike |
| Query | Pattern engine performs hypergraph matching/unification; queries are themselves Atoms and support variables, callbacks, inverted search, and virtual relations[1][30] | Strong reuse candidate for structural queries |
| Traversal | Incoming/outgoing connectivity supports graph exploration and pattern search; exhaustive unordered matching can become combinatorial[30] | ECOS still needs bounded, provenance-aware traversal and query limits |
| Rewriting | Match results can instantiate new graphs; `PatternLink::satisfy()` supports forward-chaining-style rewriting[30] | Potential Phase 2 mechanism; every rewrite needs ECOS provenance and derivation records |
| Truth values | Current documentation is transitional: root README says TruthValues are “on the way out,” while `opencog/atoms/README.md` says they are gone and identifies `FloatValue` as successor[1][29] | Do not build ECOS uncertainty on legacy TruthValue APIs; generic numbers are not an epistemic theory |
| Attention values | No current `AttentionValue` implementation was found in the inspected revision’s source scan; current root documentation does not offer it as core functionality[25] | No reusable attention-allocation capability should be assumed; ECOS attention/supervision remains custom research |
| APIs and bindings | Native C++; Scheme/Guile is described as the most complete interface; Python Cython bindings exist but are described as less used and having technical issues. OCaml and Haskell bindings are listed as removed[1] | Python integration cost and API compatibility must be tested, not inferred from a package file |
| Build requirements | CMake 3.12+, CogUtil 2.2.1+, and Guile 3.x are required; CxxTest is needed for tests, with Cython/Python development files optional for bindings[1][15] | Not a one-step pure-Python dependency |
| Dependencies and platform | Current README targets GNU/Linux and prescribes building/installing CogUtil before AtomSpace; storage adds further modules[1][11] | Use a pinned persistent Linux environment for evaluation |
| Documentation quality | Extensive READMEs, examples, design notes, and tutorials exist, but documentation includes historical sections and deprecation inconsistencies. The project itself notes a challenging learning curve[1] | Pin revisions and verify behavior with tests rather than copying old examples |
| License | AGPLv3 with an additional linking exception for independent modules; exact notices and conditions are in the repository license[14] | Preserve notices and obtain legal review for the intended linking, modification, distribution, and network-use model |
| Maintenance and compatibility | The inspected master commit is dated 2026-02-10. The README records ongoing removals/deprecations and labels several sibling projects zombie or dead[1][25] | Core is maintained, but ecosystem compatibility cannot be assumed from repository age or stars |

No AtomSpace build, unit test, integration test, or performance benchmark was run for this documentation. The official wiki was unreachable during inspection, so claims above are based on the cloned source, READMEs, build files, license, and GitHub repository pages.

## ECOS extensions that remain custom

| Required ECOS layer | Proposed mapping on AtomSpace | Significant custom work |
|---|---|---|
| Epistemic Claim Layer | Unique claim Nodes/Links with stable ECOS IDs, explicit polarity, context, and object union | Identity model, validation, claim semantics, export, queries |
| Evidence and Provenance Layer | Evidence/activity/source Atoms and typed Links; Values only for auxiliary unindexed metadata | Source chains, content hashes, extraction events, evidence semantics |
| Contradiction Preservation | Separate claim IDs for affirmation, denial, and competing values; no overwrite | Conflict model and later detection/assessment; no native paraconsistent reasoning assumed |
| Temporal Knowledge | Valid-time and transaction-time records on claims, with explicit interval/precision nodes | Bi-temporal semantics, partial dates, temporal query rules |
| Concept Versioning | New concept/version identities rather than mutating an Atom’s meaning | Migration rules and historical identity behavior |
| Concept Lineage | Explicit split/merge/refine/deprecate event Atoms connecting inputs and outputs | Lineage semantics, replay, historical query rewriting |
| Context and Framework | Explicit context/framework Atoms and scoped claim Links | Framework composition and semantics; overlay AtomSpaces/Frames can be evaluated but are not automatically equivalent |

**Design rule:** if a value must be found through graph query or participate in provenance, represent it as queryable structure rather than burying it in an unindexed Value.

## Integration strategy

1. **Freeze semantics first.** Define lossless mapping between ECOS JSON and proposed Atom representations, including repeated and contradictory claims.
2. **Run a local pinned spike.** Use a persistent Linux machine or container; build CogUtil, AtomSpace, and the selected storage module at recorded revisions. Do not start on Kaggle.
3. **Prove round trips before rewriting.** Import fixtures, restart, query claims/evidence, export, and compare against the canonical JSON.
4. **Test the seven extensions.** Include temporal precision, duplicate content with different provenance, context-specific conflicts, lineage, and framework-specific queries.
5. **Evaluate API and operations.** Exercise the chosen C++ or Python path, storage backend, resource usage, failure behavior, and migration/export.
6. **Review license and attribution.** Record notices and the exact use model before any distribution or network deployment.
7. **Adopt only on evidence.** Acceptance requires semantic round trips, required queries, maintainable build instructions, and a clear advantage over SQLite for the same fixtures.

## Kaggle practicality

AtomSpace’s core graph operations do not need a GPU. Its documented build requires native dependencies and CogUtil, and the standard instructions include system installation; adapting that chain to an ephemeral notebook is additional work, not a verified one-command process.[1][15]

No Kaggle build was attempted. For reproducible evaluation, use local Ubuntu/Docker or a persistent Linux VM. If a compatible build is later produced, Kaggle can be evaluated for disposable experiments with artifacts saved under `/kaggle/working`, but it is not the recommended build host or a persistent AtomSpace service.[8]

## Bottom line

Reuse **Atoms, typed structure, pattern matching, and rewriting** only if they outperform or simplify the baseline for real ECOS fixtures. Build the **epistemic, provenance, contradiction, temporal, lineage, and framework layers as ECOS-owned semantics** regardless of substrate. Do not rename AtomSpace “ECOS,” and do not inherit deprecated TruthValue or historical attention assumptions.

## Sources

[1] https://github.com/opencog/atomspace
[8] https://www.kaggle.com/docs/notebooks
[10] https://github.com/opencog/atomspace/blob/master/opencog/README.md
[11] https://github.com/opencog/atomspace-storage
[14] https://raw.githubusercontent.com/opencog/atomspace/master/LICENSE
[15] https://raw.githubusercontent.com/opencog/atomspace/master/CMakeLists.txt
[24] https://raw.githubusercontent.com/opencog/atomspace/master/opencog/atoms/atom_types/README.md
[25] https://github.com/opencog/atomspace/commit/c8d633bf272b838c2132c21b7c8ddf169a18dd22
[29] https://raw.githubusercontent.com/opencog/atomspace/master/opencog/atoms/README.md
[30] https://raw.githubusercontent.com/opencog/atomspace/master/opencog/query/README.md
[31] https://raw.githubusercontent.com/opencog/atomspace/master/opencog/atomspace/version.h
