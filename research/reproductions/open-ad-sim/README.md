# open-ad-sim: vetting record

| | |
|---|---|
| Model | [`models/open-ad-sim`](../../../models/open-ad-sim/README.md): 10-region Alzheimer's disease-process model at the MCI stage, v6, six-member ensemble |
| Registry | `open-ad-sim` in [`registry/project_models.yaml`](../../../registry/project_models.yaml): **triage B**, our status **reproducing** |
| Source | `open-ad-sim.zip` (sha256 `abf02847bcc1a6dd579f0ef28b82cd362323f8475e5ecfc72962d06f44559d95`, archive comment `33616530daa4…`), 33 files, built with AI assistance in a separate session |
| Imported | Vetted on an exact copy of the archive. The first public commit already carries the changes in [§7](#7-what-was-changed-and-why). The original profile file was never published, because it held an unused genotype label ([§1](#1-privacy-review-rule-1)). Anyone holding the archive can check the import against its checksum and §7. |
| Checked | 2026-10-19, Python 3.13.16, NumPy 2.3.5, SciPy 1.18.1, Linux x86_64 |
| Re-run | `python research/reproductions/open-ad-sim/vet.py all` (about 15 min on 2 cores), plus the commands in [§8](#8-how-to-re-run-every-check) |

## Verdict

**Worth building on, as a hypothesis generator, not as evidence.** The model is unusually
honest about itself: its calibration targets carry sources and tolerances, its misfits and
an earlier failed validation are documented, and every result is a range across an
ensemble. This vetting confirmed the parts that can be checked without new data:

- **Reproducibility.** Every committed number reproduces **bit-for-bit** from its own code:
  all 39 fit metrics and the loss of all six members, all validation outputs, and the
  generated calibration, validation and results documents.
- **Code matches the documentation.** An independent re-implementation of the documented
  equations agrees with the model's code to 12 significant digits.
- **No luck in the random draw.** The fit holds on fresh random seeds and on a population
  four times larger.

It also found real problems, some fixed here and some open:

- **A silent-wrong-results bug.** A member run without its structural-variant setting
  simulated a different model with no warning. The documented family-member workflow ran
  three of the six members that way. The model now refuses mismatches.
- **No harms are modeled.** The docs claimed APOE genotype fed a side-effect (ARIA) module
  that does not exist, so treatment scenarios show modeled benefit only.
- **The fit has limits.** Every member misses at least two calibration targets by more than
  twice their tolerance, and some parameters press against their fitting bounds. Two of the
  six members are near-duplicates.
- **Validation is thin.** There are two out-of-sample checks, both open-label extensions
  against external controls. The lecanemab one is under-predicted by a third to a half.
- **Several mechanisms are not identifiable.** Fitting the model's own synthetic targets
  from a perturbed start recovers the fit but leaves about half the parameters more than 10%
  off. The headline "lost versus impaired neurons" split still moved only about 4.5 points.
- **Some calibration targets need correcting.** Most source numbers check out. But one
  target mixes counting bases (entorhinal loss at mild dementia), two cite the wrong papers,
  two have no source, and one probably rests on a paper on the integrity watchlist (§5).
  The age-scaling assumption has contrary evidence.

Nothing in it is peer reviewed or independently replicated. Grade B stands until the
open items in [§9](#9-what-it-would-take-to-reach-grade-a) are done.

## 1. Privacy review (Rule #1)

All 33 files were read in full before anything was published.

- **No direct identifiers.** The scan found no names, contact details, record numbers,
  dates, places, documents or images. The upload's own privacy rule and denylist design
  were sound, and they were folded into the repository-wide gate (`tools/check_data_policy.py`).
- **Indirect detail removed.** The profiles carried genotype labels and some person-like
  wording. Neither is published here. Genotype had **no effect** on any result, because no
  code reads it. The profiles now carry ranges of age, amyloid, CDR-SB and tau status only. The
  duplicate profile that differed only by genotype was merged, and the genotype-named one
  was renamed. All ranges are unchanged, so no number moved.
- **Indirect detail reworded.** The family-member guide and AI-partner template now
  require consent, use ranges only, and keep everything local.

## 2. Reproduction

All checks ran the committed parameters with the settings the model used.

| Member | Variant | Fit metrics (39) and loss | Validation outputs (13) |
|---|---|---|---|
| `v6_r01` | base | identical (loss 50.598) | identical |
| `v6_r05` | base | identical (loss 46.601) | identical |
| `q1_r01` | base, q fixed at 1 | identical (loss 35.940) | identical |
| `flatcog_r05` | flatcog | identical (loss 37.767) | identical |
| `late40_r01` | late40 | identical (loss 49.452) | identical |
| `nolate_r05` | nolate | identical (loss 42.915) | identical |

The fit metrics used P = 4,000 and seed 11; validation used P = 8,000 and seed 33.

- `docs/CALIBRATION.md` and `docs/VALIDATION.md` regenerate byte-identically from the
  ensemble files (`model/make_docs.py`, members in their original order).
- `docs/RESULTS_*.md` (all six members, 150,000 virtual people each) reproduced
  **byte-identically** from the original code. Regeneration under the renamed profile with
  the modified code is in progress (§7).

Across platforms, BLAS and NumPy versions can move a borderline virtual person across a
threshold, so CI checks agreement to 0.02 rather than bit-identity
(`tests/test_open_ad_sim.py`).

## 3. Does the code do what the documentation says?

- **Equations.** `tests/test_open_ad_sim.py::test_code_matches_documented_equations`
  re-implements one simulation step from the documented equations, person by person and
  region by region with plain loops. It covers amyloid, the amyloid "permission" for tau,
  age scaling, tau growth and spread, neuron loss including TDP-43, surviving-neuron
  function and the cognition mapping. It matches the model's vectorised code to
  `rtol = 1e-12` for all three base-variant members.
- **Invariants over a simulated life course (age 48 to 90).** Tau and surviving-neuron
  function stay in [0, 1]. Neurons never come back. Amyloid stays below each person's
  ceiling. Freezing tau and neuron loss freezes them. Antibodies clear amyloid toward the
  5 Centiloid floor. The "ceiling" scenario holds function at 1. Losing neurons never
  improves cognition.
- **Lint.** No undefined names or logic errors. `calibrate.py` treats any exception during
  a fit as a very large loss (`except Exception: return 1e6`), which can hide a bug during
  refitting.
- **Minor quirks.** None of these affects the shipped results:
  - The antibody term pulls amyloid toward 5 Centiloid from either side, so it would nudge
    an amyloid-negative person up. Antibodies are only given to amyloid-positive virtual
    patients.
  - The symptom score is capped at 18 before the reversible non-Alzheimer part is added.
  - `validate.py`'s docstring still says "v2".

## 4. Is the fit robust?

**Random-seed robustness.** Each member was re-evaluated at its fitted parameters on five
fresh random populations and on one population four times larger.

| Member | Loss at the fitting seed | Fresh seeds, mean (range) | P = 16,000 |
|---|---|---|---|
| `flatcog_r05` | 37.8 | 38.3 (37.1–39.6) | 38.5 |
| `late40_r01` | 49.5 | 50.5 (49.3–52.1) | 50.2 |
| `nolate_r05` | 42.9 | 45.1 (44.3–47.4) | 45.5 |
| `q1_r01` | 35.9 | 38.9 (37.9–39.7) | 36.8 |
| `v6_r01` | 50.6 | 50.4 (49.2–51.1) | 51.2 |
| `v6_r05` | 46.6 | 48.1 (46.9–50.0) | 48.7 |

The optimiser gained at most about 3 loss units (under 8%) from its particular random
draw. The out-of-sample results are just as stable: the donanemab and lecanemab
comparisons vary with SD ≤ 0.015 CDR-SB across five fresh seeds.

**Misfits that do not go away.** These targets are missed by more than twice their
tolerance at P = 16,000. Tolerances express how far apart published sources are, so
|z| > 2 is outside that band.

| Target | What it is | Members with \|z\| ≥ 2 (z) |
|---|---|---|
| `dCDR_pbo_TB_hi` | Placebo decline, high-tau, TRAILBLAZER-ALZ 2 (a derived target) | all six (−2.7 to −3.2) |
| `prog5_ATpos_mci` | Amyloid+ tau+ MCI reaching dementia in 5 years (70%) | `v6_r01` +3.5, `late40_r01` +3.3 |
| `prog5_ATneg_mci` | Amyloid+ tau− MCI reaching dementia in 5 years (~35%, derived) | `v6_r05` +2.7, `nolate_r05` +2.7, `flatcog_r05` +2.1 |
| `S_PCC_ApTn_CU` | Little posterior-cingulate hypometabolism in amyloid+ tau− unimpaired people | `v6_r01`, `late40_r01` −2.5 |
| `chron_dem` | Years from amyloid positivity to dementia (13.6) | `v6_r05` +2.6, `nolate_r05` +2.2 |
| `tau_slow_neo_TB` | No slowing of neocortical tau-PET with donanemab | `v6_r05` +2.4, `nolate_r05` +2.2 |
| `nodecl_act_TB_lo` | Share without decline at 1 year on donanemab, low/medium tau | `flatcog_r05`, `v6_r05` −2.1 |
| `tau_pos_mci` | Tau-PET positivity in amyloid+ MCI (58%) | `q1_r01` +2.3 |

**Which parameters the data constrain.** Each free parameter was moved by ±10% and ±30%,
one at a time, with the same virtual population (common random numbers).

- **Mostly genuine local minima.** For most parameters a 10% move raises the loss by 0.5
  to 4 units.
- **Bounds that bind.** The fit would improve past the allowed range for:
  - person-to-person heterogeneity `het` in `v6_r05` and `nolate_r05`;
  - the neuron-loss exponent `pN` in `flatcog_r05`;
  - reserve spread `sdR` in `q1_r01`.

  The model wants more person-to-person variation than it is allowed, which fits its
  documented tendency to make progression too uniform.
- **Weakly constrained.** The high-tau PET threshold `thr_hi` (all six members), the
  positivity threshold `thr_pos` (four of six) and the reserve `R0` (three of six).
- **Near-duplicate members.** `v6_r01` and `late40_r01` have nearly identical parameters,
  so the ensemble spans five distinct fits rather than six.
- **Members disagree about the patients.** Among virtual patients who match the default
  profile, the tau-PET-negative share ranges from 12% (`q1_r01`) to 70% (`v6_r05`) depending
  on the member (P = 150,000 runs). For comparison, 42% of amyloid-positive MCI patients are
  tau-negative in the calibration source.
- **Degrees of freedom.** About 19 parameters are fitted per member against 28 targets, and
  the fitted values differ several-fold between members with similar loss: `kauto` 0.055
  to 0.46, `sD` 0.022 to 0.43, `delta` 0.033 to 0.20. The data do not pin down the
  mechanism. The model says so itself, which is why it reports ensemble ranges.

**Parameter recovery.** Two members were tested (`v6_r05`, `q1_r01`). The steps:

1. Replace the targets with the model's own output at the fitted parameters.
2. Start the optimiser from a random perturbation of up to about 37%.
3. Give it the same kind of budget the calibration used (400 Nelder-Mead evaluations).

The optimiser fits the synthetic targets almost perfectly: loss 0.6 and 1.6, down from
about 9. But **about half the parameters do not come back.** They stay more than 10% from
the truth:

- 8 of 18 in `q1_r01`: `sT` +28%, `sdR` −25%, `delta` +16%, both PET thresholds −15%, `sD`
  −14%, `kauto` +13%, `hetK` −11%;
- 10 of 19 in `v6_r05`: `het` −37%, `sT` +33%, `pN` −21%, `R0` −17%, `delta` +13% and
  others.

Several barely moved from where they started. So the 28 targets do not identify how
strongly tau harms surviving neurons (`sT`), the neuron-death rate (`delta`), disconnection
(`sD`), tau self-propagation (`kauto`) or person-to-person heterogeneity.

**Does that move the headline?** The headline result splits today's impairment into
"neurons already lost" and "neurons alive but impaired". It was recomputed for the default
profile (40,000 virtual people) at the recovered parameters, which fit the targets as well
as the true ones:

| Member | Share of impairment in lost neurons, fitted | Recovered |
|---|---|---|
| `q1_r01` | 31.5–32.8% | 32.0–33.0% |
| `v6_r05` | 37.7–39.1% | 41.9–43.6% |

The share moves by at most about 4.5 points, which stays inside the 31–48% range the model
reports across its ensemble. Members' disagreement about the patients themselves is a
separate matter: the tau-negative share is 9–12% in `q1_r01` against 69–70% in `v6_r05`,
and it does not depend on the recovered parameters. This rests on one random start per
member, for two members. It shows the headline is not *very* fragile; it does not show it
is pinned down.

## 5. Calibration and validation sources

The 28 targets break down as follows (the upload's README said "28 published human
targets"; corrected):

- **Cited from a published source:** 22.
- **Derived or extrapolated from published figures, and marked as such:** 4 (`S_EC_mci`,
  `dCDR_pbo_TB_hi`, `prog5_ATneg_mci`, `slow_TB_hi`).
- **Stated without a specific citation:** 2 (`N_PCC_mci`, `S_PFC_mci`).

Every target was checked against the source it cites. AI research assistants did the
checks and recorded the sources they opened and the quotes they used:
[`citations_clinical.md`](citations_clinical.md) covers 19 trial and cohort items and
[`citations_pathology.md`](citations_pathology.md) covers 14 pathology and imaging items.
The two findings that matter most were then re-checked independently against the primary
documents:

- **Gómez-Isla 1996**, Tables 3 and 4: there is exactly one CDR 1 case, whole entorhinal
  cortex 5.82 × 10⁶ neurons against a control mean of 6.91 × 10⁶, and layer II 0.28 against
  0.65 × 10⁶.
- **Lilly's FDA advisory-committee briefing document**, p. 20: high-tau placebo CDR-SB change
  3.34 against donanemab 2.64 (difference −0.69, 21% slowing).

**Most numbers are real and correctly quoted.** These include:

- the TRAILBLAZER-ALZ 2 and Clarity AD trial results, baseline distributions and no-decline
  shares;
- the progression risks (Vos 2015, 59%; Moscoso 2025, 70%; Betthauser 2022, 13.6 years;
  Ossenkoppele 2025, 58.1%);
- both external validation figures;
- the stereology (Gómez-Isla 1996 and Price 2001 at the MCI stage), the synapse counts
  (Scheff 2007 and 2011) and the SV2A PET papers.

The model's antibody kinetics also reproduce the published amyloid-PET aggregates closely:
for donanemab, the share below 24.1 Centiloids at weeks 24, 52 and 76 is 30%, 65% and 80%
in the model against 29.7%, 66.1% and 76.4% published.

**Problems found:**

| Target or assumption | Problem | Effect or fix |
|---|---|---|
| `N_EC_mild` = 0.45 (entorhinal neurons at mild dementia) | **Wrong basis.** The source has one CDR 1 case. Its whole-entorhinal count gives 0.84; 0.45 is that case's layer II only, while the MCI-stage target uses whole-region counts. | Pushes the model toward more entorhinal loss than whole-region data show, which bears on the "lost neurons" share. Re-derive on one basis with a wide tolerance, or drop it. |
| `dCDR_pbo_TB_hi` = 3.56 (placebo decline, high tau) | **Derived, but a published value exists**: 3.34 (post hoc, MMRM). | The target is about 7% high. The model's 1.27–1.63 is still less than half of 3.34, so the misfit stands. |
| `prog5_ATneg_mci` ≈ 0.35 | Derived by mixing CSF-based odds ratios with a tau-PET-based risk. | Moscoso 2025 reports the 5-year risk directly: 30.4% (15.9–47.8%). |
| `S_PCC_mci` = 0.85 | **Misattributed.** The cited papers report only Z/W-scores, at the dementia stage. The numbers match a 2019 conference abstract (n = 9, MCI and mild dementia pooled) and Minoshima 1997 (n = 8). PCC SV2A loss is not significant after partial-volume correction (Mecca 2020). | The value is plausible; re-cite and widen the tolerance. |
| `S_PCC_ApTn_CU` = 0.97 | **Misattributed.** Strom 2022 included only cognitively impaired patients. | The claim is supported by Hanseeuw 2017 (clinically normal adults); re-cite. |
| `S_PFC_mci` = 0.92 | **Uncited.** Its "−25% frontal synaptophysin" matches Masliah et al. 2001, and Masliah is on the [integrity watchlist](../../../registry/integrity_watchlist.yaml). | Under [INTEGRITY.md](../../../policy/INTEGRITY.md) it must not rest on that paper. Independent sources support a similar value: Mecca 2020 SV2A −5.7% after correction; Counts 2006 found no frontal synaptophysin loss in MCI. |
| `N_PCC_mci` = 0.98; `S_EC_mci` = 0.92 | **No source found.** There are no PCC neuron counts at MCI. The entorhinal survivor claim has mixed indirect evidence: layer II neurons shrink 24% in MCI (Kordower 2001). | Label both as assumptions and test their sensitivity. |
| `N_HC_mci` = 0.65 | One supporting figure is misdescribed: West 2004's −48% is the symptomatic AD group, not mixed AD or MCI. | The value lies between Price (0.54) and von Gunten (0.74); keep it, re-cite, and note it is CA1-only. |
| TDP-43 prevalence: 25%, and 40% "upper range" | 40% is the *average* any-stage prevalence at a mean age of death of 88. Among amyloid-positive brains it is about 50–55%. | The `late40` variant is a central estimate, not an upper bound. |
| Rates double every 15 years of age | **No support found, and contrary evidence exists.** In symptomatic people, younger age predicts faster tau accumulation (Jack 2020) and faster posterior atrophy (Fiford 2018). | A structural assumption that needs a sensitivity analysis or removal. |
| Donanemab stopping rule | The model omits the "11 to <25 Centiloids on two consecutive scans" arm. | Fewer modeled stops by week 76: about 60% against the trial's 69%. |
| CDR-SB measurement noise SD 0.85 | Derived from ICCs measured in narrow-spread samples. The published SEm in early AD is about 0.7. | About 20% high; affects the "no decline at 1 year" targets. |
| `dS_PCC_ab` ≈ 0 (no FDG recovery) | DIAN-TU's gantenerumab only partly lowered amyloid (64.6 to 46.6 Centiloids). | Weak evidence about full amyloid removal. |
| Tau-positivity definitions | `prog5_*` use a visual read; `tau_pos_mci` uses a temporal-ROI threshold. The model applies one threshold to both. | Expect some of the tau-group misfit to be definitional. |
| Lecanemab 4-year validation figure | A conference abstract and a press release, with no confidence intervals and heavy attrition. | The weakest number in the validation set. |

Not modeled at all: amyloid re-accumulation after stopping an antibody (about 2.4–2.8
Centiloids per year for donanemab and 2.6 for lecanemab, per the labels and extension
studies).

## 6. Out-of-sample validation

There are only two independent checks, and both compare open-label extensions with
external natural-history controls (evidence grade C).

| Check | Published | Model, six members | Read |
|---|---|---|---|
| Donanemab early start vs untreated, CDR-SB at 3 years | −1.2 (95% CI −1.7 to −0.7) | −0.96 to −1.04 | inside the CI |
| Lecanemab continuous vs untreated, CDR-SB at 4 years | 1.75 (vs ADNI) to 2.17 (vs BioFINDER) | 1.10 to 1.20 | under-predicted by a third to a half; robust to seeds |

A third check (5-year progression of amyloid+ tau+ MCI) failed in v5 and became a
calibration target in v6, so it is no longer independent. Even in-sample, two members sit
outside its confidence interval (0.89 against 70%, CI 59–81%).

## 7. What was changed and why

Model numerics are untouched. After the changes, every reproduction check above passes
again (`tests/test_open_ad_sim.py`, `pytest -m integration`). Confirmation that the
results document regenerates with identical numbers under the renamed profile is in
progress.

| Change | Why |
|---|---|
| `brain_sim.require_variant()`, called by `validate.py` and `scenarios.py` | Running a member without its `ADSIM_VARIANT` silently simulated a different model. For `flatcog_r05` the out-of-sample loss went from 4.3 to 8.5 with no warning. |
| Family-member guide runs `run_ensemble.py --patient` | The documented loop over `scenarios.py` ran three of six members under the wrong variant, and looked for members in a folder where none are stored. |
| APOE removed from profiles; output note and docs corrected | No code reads APOE and no ARIA module exists. The docs said otherwise, and the genotype label added sensitive detail for nothing. |
| Profiles renamed without genotype (default `mci_moderate_amyloid_70s`); genotype-only duplicate merged; person-like wording replaced | Rule #1: keep profiles generic. Ranges unchanged. |
| "No treatment harms are modeled" added to README, MODEL.md and the guide | Antibody scenarios show modeled benefit only; ARIA risk rises steeply with APOE ε4 copies. |
| "28 published human targets" corrected to the breakdown in §5 | Six targets are derived or uncited. |
| Upload's own privacy script, git hook and nested CI workflow removed | Superseded by the repository-wide gate. The nested workflow could never run, because GitHub only runs workflows at the repository root. |
| Status banner and vetting limits added to the model's README | So nobody uses a number without this context. |

Left as found, for the model's maintainers:

- **the calibration targets flagged in §5.** Correcting them means refitting all six
  members, which changes the model's results, so it is proposed as the next step rather
  than done silently;
- the exception-swallowing in `calibrate.py`;
- the quirks in §3;
- the hand-set 10-region network and regional constants;
- the binding bounds.

## 8. How to re-run every check

```bash
pip install -e ".[dev]"
python research/reproductions/open-ad-sim/vet.py all --out results.json     # §2, §4 (about 15 min on 2 cores)
python research/reproductions/open-ad-sim/vet.py all --tasks recovery \
    --members v6_r05,q1_r01 --out recovery.json                               # §4 parameter recovery (~10 min)
python research/reproductions/open-ad-sim/vet.py all --tasks recovery_impact \
    --members v6_r05,q1_r01 --out recovery_impact.json                        # §4 effect on the headline split
pytest tests/test_open_ad_sim.py && pytest -m integration                     # §3, plus all six members
cd models/open-ad-sim
python model/make_docs.py ensemble/calib_v6_r01.json ensemble/calib_v6_r05.json \
    ensemble/calib_q1_r01.json ensemble/calib_flatcog_r05.json ensemble/calib_late40_r01.json \
    ensemble/calib_nolate_r05.json && git diff --exit-code docs/                # tables regenerate unchanged
python model/run_ensemble.py --profile mci_moderate_amyloid_70s && git diff --exit-code docs/
```

The outputs from this vetting run are in [`results.json`](results.json),
[`recovery.json`](recovery.json) and [`recovery_impact.json`](recovery_impact.json). The
source checks are in [`citations_clinical.md`](citations_clinical.md) and
[`citations_pathology.md`](citations_pathology.md).

## 9. What it would take to reach grade A

Mapped to the [reproduction protocol](../../../policy/VETTING.md#reproduction-protocol-b-to-a-inside-this-project):

| Step | Status |
|---|---|
| 1. Pin version and environment | Done: archive checksum, the change list in §7, and the environment above |
| 2. Reproduce published figures | Done for the model's own outputs. The external figures it calibrates to are checked in §5. |
| 3. Recover ground truth | Done. The fit is recovered, about half the parameters are not, and the headline moves ≤ 4.5 points (§4). |
| 4. Refit out of sample | **Open.** First correct the targets in §5 and refit. Then fit to group-level targets from a cohort not used here, and test progression rates externally. |
| 5. Beat baselines and nulls | **Open.** Compare progression against a naive CDR-SB slope model, and the hand-set network against shuffled and distance-only networks (`alzres.spreading.null_test`). |
| 6. Uncertainty and calibration | Partly done: ensemble ranges. **Open:** a profile likelihood or posterior for the non-identified parameters. |
| 7. License | Done: MIT (code) and CC BY 4.0 (docs), from the LICENSE file |

Also needed before any treatment comparison is read as benefit against harm: a side-effect
(ARIA) model that uses APOE genotype.
