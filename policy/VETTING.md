# Vetting policy

This project builds on other people's work only after checking it. Being listed in
the registry is not an endorsement. Every external resource is graded, and every
claim we make ourselves is held to the same standard.

## Triage grades

Grades come from the [2026-10 landscape review](../docs/landscape-2026-10/report.md)
and are stored per resource in [`registry/`](../registry/).

| Grade | Meaning | What it lets you do |
|---|---|---|
| **A** | Open, reusable license; peer-reviewed; independently used or replicated; maintained | Depend on it. Still reproduce before trusting any number it produces. |
| **B** | Promising, but missing one or more of the above (unreplicated, unconfirmed license, abstract-only evidence, stale) | Experiment with it in a branch. Nothing B-grade feeds a published result until it is reproduced here. |
| **C** | Retracted, misconduct, unreplicated hype, abandoned, or a license/DUA that blocks use in a public repo | Do not depend on it, vendor it, or cite it as support. May be cited as a cautionary example. |

**A means "safe to depend on", not "pre-vetted".** The `our_status` field records
what *this* project has actually checked:

| `our_status` | Meaning |
|---|---|
| `not-started` | Only the landscape review's desk research. The default. |
| `smoke-tested` | Installed and run on synthetic data here; behaves as documented. |
| `reproducing` | Reproduction under way (link the issue or PR). |
| `reproduced` | Passed the full reproduction protocol below. |
| `failed` | Reproduction attempted and failed; record why. |
| `rejected` | Reviewed and excluded (e.g. license, integrity). |

Any status other than `not-started`, `reproducing` or `rejected` needs a
`verification` pointer to the test, report or PR that backs it. CI enforces this.

## Reproduction protocol (B to A inside this project)

Before a model's output is used in anything we publish:

1. **Pin** the exact upstream version (commit SHA or release) and environment (lockfile or container).
2. **Reproduce** one published figure or table exactly, or explain why it can't be (e.g. gated data).
3. **Recover ground truth** on `alzres.synthetic` data with known answers.
4. **Refit out of sample** on a cohort the original authors did not use, with subject-level splits (`alzres.eval`).
5. **Beat baselines and nulls**: naive baselines (`alzres.eval.baselines`) for prediction; rewired and spatial nulls (`alzres.spreading.null_test`) for connectome models.
6. **Report uncertainty and calibration**, not just a headline metric.
7. **Confirm the license** from the upstream LICENSE file (not API metadata) and any data terms from the primary source.

Write up the result in `research/reproductions/<id>.md` and update the registry record.

## Red-flag checklist

Treat a resource or paper as suspect until these are answered:

- [ ] Train/test split is by **subject**, not scan, slice or visit.
- [ ] External validation on an **independent** cohort, not a random hold-out of the same one.
- [ ] Pretraining data does not overlap the test set (foundation models and ADNI/OASIS are a common overlap).
- [ ] Compared against naive baselines; a fancy model that ties last-value-carried-forward is not progress.
- [ ] Labels are not derived from the predictors (ADNI diagnoses come from MMSE/CDR).
- [ ] Accuracy is plausible (MRI AD-vs-CN >95% or speech >90% is presumed leaky until shown otherwise).
- [ ] No reliance on subgroup results after a missed primary endpoint.
- [ ] Evidence is peer-reviewed, not only a press release, prize announcement or company deck.
- [ ] No dependence on work in the [integrity watchlist](../registry/integrity_watchlist.yaml).
- [ ] Code and weights are actually downloadable and runnable, under a license we can use.
- [ ] Results are stable across cohorts, seeds and reasonable preprocessing choices.

## Licensing rules for code we bring in

- The core package (`src/alzres`) is **Apache-2.0**. Only permissively licensed
  upstreams (MIT, BSD, Apache-2.0) may be imported from it.
- **Copyleft** upstreams (GPL: TVB, kde_ebm, NEST, pyebm; AGPL: nmed2024) are used
  only from separately licensed modules with their own `LICENSE` file, never imported
  by the Apache-2.0 core.
- **Non-commercial, no-derivatives or unlicensed** code and weights (BrainIAC, pyment,
  BrainLM, neuromaps, AlphaGenome, anything with no LICENSE file) are never vendored,
  required or redistributed.
- Upstream code is **installed and pinned, not copied** into this repository. Where we
  re-implement a published method (e.g. `alzres.spreading`), we cite the paper and
  cross-check against the original toolbox.

This is a project policy, not legal advice. Have an institution's open-source or
tech-transfer office review the licensing plan before any commercial use.
