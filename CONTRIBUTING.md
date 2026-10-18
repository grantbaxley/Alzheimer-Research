# Contributing

Thanks for helping. This project is deliberately skeptical, including of its own work.

## Before you start

- Read [policy/DATA_ACCESS.md](policy/DATA_ACCESS.md). **Never commit participant data**
  or send gated cohort data to AI tools.
- Read [policy/VETTING.md](policy/VETTING.md) for the triage grades and reproduction protocol.

## Setup

```bash
pip install -e ".[dev]"
pip install pre-commit && pre-commit install   # runs the data-policy scanner on commit
```

## Every pull request

- `pytest`, `ruff check .` and `ruff format --check .` pass.
- `python tools/check_data_policy.py` passes.
- If you changed `registry/` or `evidence/`, run `python tools/build_docs.py` and commit
  the regenerated files.
- New code has tests. Models come with synthetic ground-truth tests and baseline or
  null comparisons.

## Adding or changing a registry record

- Read the upstream **LICENSE file** yourself and set `license.source: license-file`.
  API metadata and READMEs are often wrong.
- Give a one-line `reason` for the grade and list `red_flags` and `sources`.
- Don't raise `our_status` without a `verification` pointer to the test, report or PR.
- Downgrades are as welcome as additions. If you find a problem with something graded
  A, open an issue.

## Bringing in a model or result

Follow the stages in [research/README.md](research/README.md): intake, then dependency
mapping, then re-modeling, then promotion. Install and pin upstream code instead of
copying it, and keep copyleft upstreams out of the Apache-2.0 core.

## Claims

Every claim about efficacy, accuracy or mechanism needs a source and an evidence grade.
State effect sizes with uncertainty. Don't present subgroup results, biomarker changes
or observational associations as clinical benefit.
