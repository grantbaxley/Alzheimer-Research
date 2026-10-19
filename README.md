# alzheimer-research

An open, verification-first project for modeling Alzheimer's disease: helping to
**prevent, slow and understand** it by building on the best freely available work
and checking it before trusting it.

> **Not medical advice.** Nothing here is a validated clinical tool. No intervention
> has been shown to reverse Alzheimer's disease; see [evidence/](evidence/README.md).

> **Rule #1: nothing that could identify a real person ever enters this repository**:
> no names, initials, dates, places, clinicians, exact test values, documents or photos,
> in files, file names, commit messages, pull requests or issues. It is enforced on every
> commit and push and across the whole history ([policy/PRIVACY.md](policy/PRIVACY.md)).

## Why this project exists

A [landscape review (Oct 2026)](docs/landscape-2026-10/report.md) of open brain and
Alzheimer's modeling found:

- **Mature open infrastructure:** imaging pipelines (Clinica, ClinicaDL, FastSurfer,
  SynthSeg), progression models (pySuStaIn), simulators (NEURON, The Virtual Brain,
  NEST, Brian2) and atlases (siibra).
- **Weak disease-model evidence:** many mechanistic models, "digital twins", foundation
  models and AI agents are unreplicated, abstract- or press-only, or carry licenses that
  block reuse.
- **Leakage-inflated ML:** more than half of surveyed AD deep-learning papers may have
  leaked test data.
- **Gated data:** nearly every major cohort sits behind a data use agreement, so a public
  repo can share code but not participant data.

So this project aims to be the missing **verification layer**: reproducible
re-implementations, explicit null models, synthetic ground-truth benchmarks,
leakage-proof evaluation and provenance tracking. It does not set out to be one more
model claiming a cure.

## What's here

| Path | What it is |
|---|---|
| [`registry/`](registry/README.md) | 90 graded records (A build on / B vet first / C avoid) for external tools, models, datasets and claims, with license provenance and our verification status. |
| [`awesome/`](awesome/README.md) | The registry rendered as a curated, graded resource list. |
| [`evidence/`](evidence/README.md) | Evidence-graded prevention/slowing/"reversal" claims. |
| [`policy/`](policy/) | [Privacy (Rule #1)](policy/PRIVACY.md), [vetting](policy/VETTING.md), [data access](policy/DATA_ACCESS.md) and [integrity](policy/INTEGRITY.md) rules, enforced in CI. |
| [`src/alzres/`](src/alzres/) | Python package (Apache-2.0). |
| [`models/open-ad-sim/`](models/open-ad-sim/README.md) | A calibrated 10-region model of the Alzheimer's disease process at the MCI stage, run as a six-member ensemble (MIT). It asks how much of today's impairment sits in lost neurons versus impaired surviving neurons, and what each class of treatment could do for a patient *type*. Triage B: see its [vetting record](research/reproductions/open-ad-sim/README.md). |
| [`research/`](research/README.md) | Where our own work lands: intake, then [reproductions](research/reproductions/), then studies. |
| [`docs/landscape-2026-10/`](docs/landscape-2026-10/report.md) | The landscape report and the six source notes behind it. |

### The `alzres` package

- `alzres.synthetic`: cohorts with **known** event orders, subtypes and stages, so
  any progression model can be checked against the truth on shareable data.
- `alzres.spreading`: network diffusion and FKPP models re-implemented from the published
  equations, with **mandatory null tests** (degree-preserving rewiring and spatial-distance
  spread).
- `alzres.eval`: subject-level splits that raise on leakage, naive baselines (train mean,
  last value carried forward, mean-rank event order) and ordering metrics.
- `alzres.integrations.pysustain`: runs [pySuStaIn](https://github.com/ucl-pond/pySuStaIn)
  (installed, not copied; pinned commit) against synthetic ground truth.
- `alzres.registry`: loads and validates the registry.

In the shipped example, pySuStaIn recovers both of two opposite-ordered synthetic
subtypes exactly (Kendall τ = 1.0), while the subtype-blind baseline cannot
(τ = 0.8 and −0.8). The network diffusion model beats 200 rewired connectomes
(p = 0.005) and a spatial null on a synthetic connectome. These are smoke tests of the
tooling, not findings about Alzheimer's.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
git config core.hooksPath .githooks      # Rule #1 privacy gate on every commit and push
pytest                                   # unit + policy tests (fast)
python -m alzres.registry summary        # what's graded A/B/C and what we've verified
python examples/spreading_null_test.py

pip install -e ".[progression]"          # optional: pinned pySuStaIn
pytest -m integration                    # slower: pySuStaIn and all six open-ad-sim members
python examples/pysustain_synthetic_recovery.py

cd models/open-ad-sim && python model/run_ensemble.py --profile mci_moderate_amyloid_70s
```

## Principles

0. **Rule #1: no identifying information, ever.** Real people are described only as
   ranges, locally, in git-ignored folders ([policy](policy/PRIVACY.md)).
1. **Build on others' work, credit it, verify it.** Upstream tools are installed and
   pinned, never copied in. Re-implementations cite the paper and are cross-checked
   against the original.
2. **Nothing is trusted because it is listed.** Grades are desk research; `our_status`
   records what we actually ran. See the [reproduction protocol](policy/VETTING.md#reproduction-protocol-b-to-a-inside-this-project).
3. **Code, not data.** No participant-level data from any DUA cohort, and none sent to AI
   tools ([policy](policy/DATA_ACCESS.md)).
4. **Nulls and baselines or it didn't happen.** Every model result is reported against
   naive baselines and null models, on subject-level splits.
5. **Integrity screening.** Retracted and misconduct-affected work is excluded
   ([watchlist](registry/integrity_watchlist.yaml)).

## Roadmap

Gap areas from the landscape review, in priority order:

1. **Reference spreading library:** NDM, FKPP, amyloid-weighted FKPP and SIR behind
   one API with standard nulls, cross-checked against UCL `network_spreading_models` and
   UCSF Nexis. *(NDM, FKPP and nulls are started.)*
2. **Synthetic benchmark cohorts:** ground-truth recovery tests for pySuStaIn, kde_ebm
   and Leaspy. *(Generator and pySuStaIn check are started.)*
3. **Leakage-proof evaluation harness:** splits, baselines, calibration, and a linter
   built from the red-flag checklist. *(Splits and baselines are started.)*
4. **Benefit/risk and biomarker-to-clinical translation models** from published aggregate
   trial data (e.g. ARIA risk by APOE genotype).
5. **Integrity and provenance tooling:** retraction-filtered builds of AlzKB/PrimeKG,
   evidence tiers on every claim.
6. **Open SBML re-implementation** of the 19-variable multiscale AD ODE model, with
   identifiability analysis.
7. **Take open-ad-sim from B to A:** primary-source checks of every calibration target, a
   measured connectome in place of its hand-set network (tested with `alzres.spreading`
   nulls), external validation of progression, and a side-effect (ARIA) module before any
   treatment comparison is read as benefit versus harm. Open items are listed in its
   [vetting record](research/reproductions/open-ad-sim/README.md).

Open items carried over from the review (unverified figures, scout disagreements) are
listed in [the report](docs/landscape-2026-10/report.md#where-the-scouts-disagree-and-what-was-never-re-fetched).

## Contributing and licenses

See [CONTRIBUTING.md](CONTRIBUTING.md). Code is [Apache-2.0](LICENSE). Documentation,
the registry and the evidence tables are [CC BY 4.0](LICENSES/CC-BY-4.0.txt).
`models/open-ad-sim` keeps the license it was contributed under ([MIT](models/open-ad-sim/LICENSE)
for code, CC BY 4.0 for its docs). External resources keep their own licenses and terms,
recorded per record in `registry/`.
