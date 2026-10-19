# open-ad-sim

An open, testable simulation of the Alzheimer's disease process at the mild-cognitive-impairment stage, built to ask one question honestly: **for a given type of patient, what is actually possible?** How much of today's impairment sits in neurons that are gone and how much in neurons that are alive but impaired, what each class of treatment (available, in trials, not yet invented) could do, and how fast the best possible outcome shrinks with time.

> **This is a research and hypothesis tool, not medical advice.** It cannot simulate any individual's brain or predict any individual's course. Every output is a modeled hypothesis for a *type* of patient, calibrated to published group-level data, with its failures documented. Decisions belong to patients, families and their clinicians.

> **Status in this repository: triage B (vet before relying on it); our status: reproducing.** Contributed as an archive (sha256 `abf02847bcc1…`) and vetted in [`research/reproductions/open-ad-sim`](../../research/reproductions/open-ad-sim/README.md). Its committed outputs reproduce bit-for-bit from its code, its code matches its documented equations, and its fit is stable across random seeds. But it is not peer reviewed, it has only two out-of-sample checks (both against external controls), it models no treatment harms, and several fitted parameters sit at their bounds. Read the vetting record before using any number.

## Rule #1 — no real patient information, ever

- Nothing about any real person goes into this repository: no names, initials, ages, dates, places, clinicians, scan values, test results or documents — and no exact values from a real person even without a name attached.
- The repository models **patient types** through generic profiles defined by ranges (`profiles/profiles.yaml`). Anyone running the model for a family member does so **locally**; their inputs live in `patients/` (git-ignored) and are never committed. See `kit/HOW_TO_RUN_FOR_A_FAMILY_MEMBER.md`.
- Enforced, not just stated, by the repository-wide privacy gate (`tools/check_data_policy.py`; rules in `policy/PRIVACY.md` at the repository root). Turn on its git hooks once per clone with `git config core.hooksPath .githooks`; CI runs it on every push and pull request over every file version, file name, commit message and author identity in the history. It blocks private directories, scan, document and data file types, identifier-like patterns, and every term in a **private denylist kept outside the repository** (`~/.config/alzheimer-research/denylist.txt`, or the older `~/.config/open-ad-sim/denylist.txt`, locally; the `PRIVACY_DENYLIST` secret in CI), so the protected names themselves never appear here.
- Pull requests that add real-patient information will be closed and the history rewritten.

## What the model is

A 10-region disease-process model (entorhinal cortex, hippocampus, parahippocampal/amygdala, inferior temporal, lateral temporal, posterior cingulate/precuneus, inferior parietal, prefrontal, occipital association, primary cortex), wired along the routes tau spreads in humans. Per person and region it tracks amyloid, tau, the fraction of neurons still alive, and the function of the surviving neurons, with TDP-43 co-pathology in a fraction of people, age-dependent vulnerability, and person-to-person variation in tau propagation and resilience. Cognition (CDR-SB) is computed from network function with a reserve threshold, plus reversible non-Alzheimer contributors. Plain-language description: `docs/MODEL.md`; equations: the docstring of `model/brain_sim.py`.

Interventions: anti-amyloid antibodies with drug-specific clearance kinetics and stopping rules; partial or complete blocking of new tau; neuroprotection; restoration of surviving-neuron function (at the natural pace or faster); full restoration including rewiring (theoretical ceiling); removal of non-Alzheimer contributors.

## How it was calibrated and tested

- **28 calibration targets** from published human data: 22 with a cited source, 4 derived or extrapolated from published figures (marked *[extrapolated]* in `docs/CALIBRATION.md`) and 2 stated without a specific citation (`N_PCC_mci`, `S_PFC_mci`). They cover stereological neuron counts, synapse/FDG/SV2A data by region, tau-PET positivity, trial decline and drug effects by tau stage, one-year stability with measurement noise, amyloid chronicity, 5-year progression of amyloid-positive MCI with and without tau, and the absence of tau-PET slowing and FDG recovery after amyloid removal. Sources and per-member fit: `docs/CALIBRATION.md`. About 19 global parameters are fitted per member, against those 28 targets.
- **Ensemble of six versions** (`ensemble/`) that fit the data comparably but differ in mechanisms the data cannot pin down: synaptic recovery speed, how much cognition depends on memory circuits, TDP-43 prevalence, and a linear vs convex damage-to-symptom mapping. Results are reported as ranges across versions. Two members (`v6_r01`, `late40_r01`) ended up with nearly identical parameters, so the ensemble spans five distinct fits rather than six.
- **Out-of-sample checks** against long-term results never used in fitting: `docs/VALIDATION.md`. The model reproduces the 3-year donanemab extension and gives about half to two-thirds of the 4-year lecanemab external-control estimate. An earlier version **failed** a 5-year progression check (92–98% vs 70%); the fix and the remaining misfits are documented rather than hidden.

## Quick start

```bash
# from the repository root
pip install -e .                                               # numpy, scipy, pyyaml
git config core.hooksPath .githooks                            # turn on the privacy gate before your first commit
cd models/open-ad-sim
python3 model/run_ensemble.py --profile mci_moderate_amyloid_70s   # runs all six fitted versions (~10 min on 2 cores)
```

That writes `docs/RESULTS_<profile>.md`. To refit or extend the ensemble:

```bash
mkdir -p results
python3 model/calibrate.py 0.1 4000 150 700 ensemble/calib_v6_r01.json my_member              # fit one member (~15–20 min)
ADSIM_VARIANT=flatcog python3 model/calibrate.py 0.5 4000 100 450 ensemble/calib_v6_r05.json my_variant
ADSIM_VARIANT=base python3 model/validate.py results/calib_my_member.json                  # out-of-sample checks
python3 model/make_docs.py ensemble/calib_*.json                                            # regenerate the docs tables
```

Each member was fitted under a structural variant (`"variant"` in its calibration file). `validate.py` and `scenarios.py` refuse to run a member under a different `ADSIM_VARIANT`, because doing so silently simulates a different model; `run_ensemble.py` sets the variant for every member.

For a family member, privately: `kit/HOW_TO_RUN_FOR_A_FAMILY_MEMBER.md`.

## What it shows for the generic MCI profile

See `docs/RESULTS_mci_moderate_amyloid_70s.md` and the research note `docs/hypotheses/survivor-share-and-window.md`. In short: available antibodies slow the decline and do not reverse it; roughly half of the Alzheimer-related impairment at this stage sits in neurons that are alive but impaired (recoverable in principle, by no therapy that exists); and that share shrinks every year. Treatment rows show modeled benefit only: no side effects are modeled.

## Repository map

- `model/` — simulation, calibration, validation, scenarios, ensemble pooling and runner, docs generator
- `ensemble/` — the six fitted versions (parameters, fit metrics, validation)
- `profiles/` — generic patient types (ranges only; no genotype)
- `docs/` — model description, calibration and validation tables with sources, results by profile, research notes
- `kit/` — running the model privately for a family member; a template for an AI research partner on one patient's case
- Rule #1 enforcement is repository-wide: `tools/check_data_policy.py`, `.githooks/` and CI at the repository root
- Tests: `tests/test_open_ad_sim.py` at the repository root (documented equations versus code, invariants, reproduction of the committed outputs)

## Contributing

Most useful: better calibration data (with sources), new out-of-sample checks, structural variants that fix a documented misfit (high-tau decline, tau-negative progression, posterior cingulate hypometabolism in tau-negative people), and independent reviews. Every contribution must pass the privacy gate.

## Limitations (read before using any number)

- Group-level calibration; individuals vary far more than any model.
- Several mechanisms are not identifiable from current human data; different ensemble members explain the same data differently.
- The mapping from brain damage to symptoms is the least constrained part and drives the "what could come back" estimates.
- Known misfits: decline in people with widespread tau is under-predicted; tau-negative and tau-positive progression are separated less than in human cohorts; amyloid-positive, tau-positive MCI still reaches dementia somewhat faster than cohorts show; amyloid is credited with more harm to surviving neurons than imaging supports.
- Hypothetical therapies are upper bounds, not forecasts; none exists.
- No neuron replacement is modeled: lost neurons, and what they encoded, are treated as permanent.
- **No treatment harms are modeled.** There is no side-effect (ARIA) module, and ARIA risk rises steeply with the number of APOE ε4 copies. APOE genotype does not change any result here, so treatment comparisons show modeled benefit only.
- **Hand-set structure.** The 10-region connection weights, regional vulnerability, amyloid sensitivity and the weights of each region in cognition are set by hand, not taken from a measured connectome or fitted.
- **Fit limits found in vetting** (`research/reproductions/open-ad-sim`): every member misses at least two targets by more than twice their tolerance, even with four times the virtual population. The miss shared by all six is placebo decline in high-tau patients, under-predicted by more than half (the target was derived as 3.56; the published post hoc value is 3.34, and the shortfall against it is still more than half). Some parameters press against their fitting bounds (person-to-person heterogeneity in two members), and both tau-PET thresholds are only weakly constrained. In a parameter-recovery test, about half the parameters did not return to their true values even though the fit did. The data do not identify how strongly tau harms surviving neurons, the neuron-death rate or disconnection. The headline split between lost and impaired neurons still moved only about 4.5 points.
- **Calibration sources** (checked against primary sources; details in the vetting record, §5). Most numbers are real and correctly quoted, but:
  - `N_EC_mild` mixes a single case's layer-II count with whole-region counts;
  - `S_PCC_mci` and `S_PCC_ApTn_CU` cite papers that do not contain those findings;
  - `N_PCC_mci` and `S_EC_mci` have no source;
  - `S_PFC_mci` appears to rest on a paper by an author on the integrity watchlist;
  - two derived targets now have directly published values (`dCDR_pbo_TB_hi` 3.34; A+T− MCI 5-year risk 30%);
  - there is contrary evidence for the assumption that rates double every 15 years of age.

## License

Code: MIT. Documentation and research notes: CC BY 4.0.
