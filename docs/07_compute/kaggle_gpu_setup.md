# Kaggle GPU Setup for ECOS Experiments

**Project:** ECOS — Evolutionary Conceptual Operating System  
**Document version:** 0.1.0  
**Status:** Verified official-source guidance; no Kaggle account, GPU, or AtomSpace build was tested  
**Purpose:** Explain current access, accelerators, limits, verification, and appropriate ECOS use without assuming account eligibility.  
**Date last verified:** 2026-11-20

## Current-state warning

Kaggle’s general notebook documentation still contains P100 and older TPU text, but newer official announcements supersede it: **P100 was retired on September 15, 2026**, and Kaggle staff stated that **T4x2 was the only generally offered GPU at that time**. T4x2 provides two separate 16 GB T4 GPUs. L4 access was described as limited to a small set of competitions.[16]

TPU v5e-8 is the newer TPU option; the older v3-8 is being phased out. Identity verification is required for TPU access. Treat the notebook’s live **Settings → Accelerator** menu and account quota page as the final account-specific answer.[13][17]

## 1. Account access and eligibility

1. Create a Kaggle account and provide accurate registration information. Kaggle’s terms allow only one active account per person and restrict use to internal, personal, non-commercial purposes; users below legal contracting age need the described parental-consent process.[27]
2. Complete **Phone Verification** in account settings. Kaggle staff documentation states that phone verification is required to use GPU access.[12]
3. Complete **identity verification** if using TPU. Kaggle’s 2026 announcement says this applies to all TPU users and uses a one-time Persona flow through account settings. The sources reviewed do not establish the same universal identity-verification requirement for ordinary T4x2 GPU use.[13]
4. Check the live Accelerator menu. Account eligibility, competition restrictions, queues, and capacity can affect which options are actually usable; verification does not guarantee immediate hardware.[8]

No account was created, phone-verified, identity-verified, or GPU-tested for this document.

## 2. Current accelerator options

| Accelerator | Status on 2026-11-20 | Notes |
|---|---|---|
| **T4x2** | Current general GPU option, subject to account and capacity | Two NVIDIA T4 GPUs with 16 GB each; selecting it restarts the session[16] |
| **Single T4** | Not confirmed as a current standalone general option | The recent staff statement identifies T4x2 as the available option; do not assume a single-T4 choice[16] |
| **P100** | **Retired 2026-09-15** | Older general docs still show P100 instructions/specs, but the newer announcement says P100 notebooks switch to T4x2[8][16] |
| **Other general GPUs** | None confirmed in the reviewed current official sources | Staff said no additional GPU offerings were planned at that time; recheck announcements[16] |
| **L4 / L4x4** | Competition-limited, not a general notebook entitlement | Staff comments restrict L4 to a small set of competitions[16] |
| **TPU v5e-8** | Current TPU option, separate from GPU | Requires identity verification; framework support differs from CUDA[13][17] |
| **TPU v3-8** | Being phased out | Older docs may still mention it; the newer TPU announcement describes migration to v5e-8[17] |

## 3. Quotas, sessions, queues, and idle behavior

| Item | Current official guidance | Planning rule |
|---|---|---|
| Weekly GPU quota | Kaggle’s GPU tips page states **30 hours, or sometimes higher depending on demand and resources**, resetting weekly[9] | Treat 30 hours as the published nominal figure, not a guaranteed fixed entitlement; inspect the account’s live quota |
| Reset schedule | Weekly reset is documented, but no current official reset day/time was found in the inspected pages[9] | Do not repeat a weekday/time from older community posts |
| CPU/GPU session | Notebook technical specifications state up to **12 hours** execution; TPU sessions state **9 hours**[8] | Checkpoint and save outputs before the cap |
| Queue | Free GPU availability can be limited and busy periods may queue; accelerator selection restarts the session[8] | Do not schedule immediate deadlines around queue access |
| Idle editor/session | The notebook page describes **20 minutes** of editor inactivity; the GPU tips page describes a **60-minute** interactive idle timeout[8][9] | The pages describe behavior differently and may cover different idle conditions; plan conservatively and stop sessions manually |
| Demand changes | Published quota can be higher depending on demand/resources and hardware can queue[8][9] | Recheck live limits rather than assuming a permanent allowance |
| Colab Pro promotion | The notebook page describes an experimental, limited-time link granting 15 extra GPU hours for Pro and 30 for Pro+[8] | Optional promotion, not required for ECOS; terms and availability can change |
| Competition limits | Special competitions can impose their own runtime, internet, accelerator, and quota rules | Read the specific competition rules; never bypass them |

## 4. Beginner setup walkthrough

1. **Create a Kaggle account.**
2. Open account settings and complete required **Phone Verification**; complete **identity verification** for TPU or if the account UI requires it for a particular resource.[12][13]
3. Open **Kaggle Notebooks** from the Notebooks section.
4. Select **Create → New Notebook** and choose **Python** under File → Language if needed.[8]
5. Open the notebook’s **Settings** pane.
6. Find **Accelerator**.
7. Choose **T4x2** if it is available for the account. Do not select P100 based on outdated instructions.[16]
8. Allow the session to restart and wait if a queue is reported. Unsaved in-memory state can be lost during restarts.[8]
9. Run the verification cells below and confirm the actual device names and count.
10. Save outputs under `/kaggle/working`, use **Save Version**, and download important artifacts. `/kaggle/working` has 20 GB auto-saved space; additional scratch outside it is not saved outside the current session.[8]

**Quick Save** snapshots the notebook without a clean top-to-bottom run. **Save & Run All** starts a clean session and executes the notebook; successful completion is bounded by the 12-hour CPU/GPU or 9-hour TPU limit.[8]

Official visual references are available on the [Kaggle Notebooks documentation](https://www.kaggle.com/docs/notebooks), including editor images; this guide intentionally uses links rather than copied screenshots whose UI may become stale.[8]

## 5. GPU verification notebook

Run this Python cell after the accelerator session starts:

```python
import torch

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("CUDA device count:", torch.cuda.device_count())

if torch.cuda.is_available():
    for index in range(torch.cuda.device_count()):
        print(f"GPU {index}:", torch.cuda.get_device_name(index))
        memory_mib = torch.cuda.get_device_properties(index).total_memory // (1024 ** 2)
        print(f"Memory {index}: {memory_mib} MiB")
else:
    raise RuntimeError(
        "No CUDA GPU is visible. Check Settings > Accelerator and restart the notebook."
    )
```

Then run:

```bash
!nvidia-smi
```

**Successful result:** `CUDA available` is `True`, the count is at least one, and `nvidia-smi` lists driver/CUDA information and GPU hardware. For a current T4x2 session, expect two `Tesla T4` devices with approximately 16 GB each. Exact driver, CUDA, PyTorch, and MiB text can vary; verify rather than pasting expected output into results.[16]

Two visible GPUs do not mean ordinary single-GPU code uses both. Multi-GPU execution requires explicit code, and their memory is not automatically pooled.

## 6. Appropriate ECOS workloads

**Use CPU/local execution for:** CRS schema validation, SQLite Concept Memory, provenance, exact queries, graph traversal, deterministic export, and small supplied-vector searches. These do not need CUDA.

**Consider Kaggle T4x2 later for:** embedding generation, neural language-adapter inference, model experimentation, and small fine-tuning experiments after a model/memory assessment. Start with a smoke test, fixed dataset subset, and saved checkpoints. GPU suitability depends on the actual model and batch shape, not the ECOS name.

**Do not use Kaggle for:** Phase 1 GPU acceleration, a persistent graph service, an always-on inference endpoint, or any attempt to bypass quotas and access controls. Kaggle’s AUP prohibits resource abuse including server farming and activity unrelated to ML data science.[26]

## 7. AtomSpace on Kaggle

AtomSpace core is a CPU/native C++ workload, not a CUDA workload. Its build requires CogUtil, Guile, CMake, and related native dependencies; standard instructions include building CogUtil first and installing artifacts. Persistence requires additional storage modules.[1][11][15]

**Practical recommendation:** do not make Kaggle the first AtomSpace build environment. Use a persistent local Ubuntu/Docker or VM environment with pinned revisions and enough time to diagnose native dependencies. No Kaggle build was attempted for this document, so feasibility on the current notebook image is unverified.

If a later experiment supplies a compatible prebuilt environment, test it with tiny fixtures, save build/output artifacts under `/kaggle/working`, and expect to rebuild or reinstall when the environment changes. Do not run a persistent AtomSpace service from a notebook.

## 8. Save and quota checklist

- [ ] Confirm live accelerator and remaining quota before each run.
- [ ] Run a small GPU smoke test before a long experiment.
- [ ] Save code, configuration, model/data revisions, and dependency versions.
- [ ] Write artifacts to `/kaggle/working` and download important outputs.
- [ ] Use Save & Run All for a clean reproducibility check within the execution cap.
- [ ] Stop interactive sessions explicitly instead of relying on idle timeout.
- [ ] Follow Kaggle’s terms, AUP, and competition-specific restrictions.[26][27]

## Limitations of this guide

Availability and quotas change. This page records official sources retrieved on 2026-11-20; it does not guarantee that a particular account sees T4x2, receives exactly 30 hours, avoids a queue, or can run a chosen model. The 20/60-minute idle descriptions are reported as a documentation discrepancy rather than resolved by guesswork. Recheck the official pages and live account UI before each significant experiment.

## Sources

[1] https://github.com/opencog/atomspace
[8] https://www.kaggle.com/docs/notebooks
[9] https://www.kaggle.com/docs/efficient-gpu-usage
[11] https://github.com/opencog/atomspace-storage
[12] https://www.kaggle.com/product-feedback/202584
[13] https://www.kaggle.com/product-announcements/670573
[15] https://raw.githubusercontent.com/opencog/atomspace/master/CMakeLists.txt
[16] https://www.kaggle.com/product-announcements/735239
[17] https://www.kaggle.com/product-announcements/607202
[26] https://www.kaggle.com/aup
[27] https://www.kaggle.com/terms
