# ECOS Compute Strategy

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Proposed compute plan; no hosted resources provisioned or verified  
**Purpose:** Keep Phase 1 reproducible locally and reserve hosted accelerators for bounded experiments that need them.  
**Last reviewed:** 2026-11-20

## Environment allocation

| Stage | Environment | Reason |
|---|---|---|
| Ontology and fixtures | Local editor + Git | Reviewable text and deterministic fixtures |
| Phase 1 CRS | Local Python + SQLite | No neural dependency or accelerator requirement |
| RDF interoperability | Local isolated virtual environment | Small, reproducible dependency spike |
| AtomSpace spike | Persistent Linux/Docker | Native build chain and durable artifacts; not an ephemeral GPU task[1][15] |
| Phase 7 neural experiments | Local GPU if available, otherwise bounded Kaggle notebook | Accelerator may help after model/data requirements are known |
| Long-running services | Not Kaggle | Session limits and acceptable-use restrictions make notebooks unsuitable as persistent service infrastructure[8][26] |

## Workflow

1. Implement and test the complete Phase 1 demo locally.
2. Record actual CPU, memory, storage, and runtime measurements for representative fixtures.
3. For a neural experiment, define model, dataset, output, metric, maximum steps, and expected memory before enabling a GPU.
4. Run a tiny smoke test and save configuration, package versions, model/revision, data hashes, and random seeds where relevant.
5. Save outputs to durable notebook output or download them; stop the accelerator session explicitly.
6. Compare against the CPU/smaller baseline and report failures as well as successful runs.

## Kaggle role

Kaggle is appropriate for bounded, reproducible notebook experiments such as embedding generation, small neural inference, and feasible adapter experiments. It is not needed for symbolic graph storage and should not be treated as free persistent infrastructure. Current GPU access, quotas, queueing, and T4x2 availability are account- and demand-dependent; check the live UI before scheduling work.[8][9][16]

## Reproducibility package

Every hosted experiment should produce:

- Notebook and dependency manifest.
- Model and data identifiers, revisions, and licenses.
- Hardware actually reported by `torch` and `nvidia-smi`.
- Start/end time, outcome, metric, and failure logs.
- Output artifacts and a small verification script that can rerun the result locally where practical.

## Data and usage policy

Use public synthetic Phase 1 fixtures. Review source-data privacy and licenses before uploading anything. Follow Kaggle’s terms and acceptable-use policy, including restrictions on resource abuse and activity unrelated to ML data science. Do not create duplicate accounts or attempt to circumvent quotas, queues, identity checks, or competition restrictions.[26][27][28]

## Decision rule

Choose the least powerful environment that can reproduce the experiment. A local CPU is the default. Kaggle T4x2 is an experiment option, not an architectural dependency. AEE resource planning remains unjustified until a real Phase 8 proposal exists.

## References

- [Compute requirements](compute_requirements.md)
- [Kaggle GPU setup](kaggle_gpu_setup.md)
- [AtomSpace evaluation](../05_research/atomspace_evaluation.md)

## Sources

[1] https://github.com/opencog/atomspace
[8] https://www.kaggle.com/docs/notebooks
[9] https://www.kaggle.com/docs/efficient-gpu-usage
[15] https://raw.githubusercontent.com/opencog/atomspace/master/CMakeLists.txt
[16] https://www.kaggle.com/product-announcements/735239
[26] https://www.kaggle.com/aup
[27] https://www.kaggle.com/terms
[28] https://www.kaggle.com/community-guidelines
