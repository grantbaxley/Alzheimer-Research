# Notes for AI coding agents

- Never commit or process participant-level data from DUA cohorts (ADNI, OASIS, NACC,
  UK Biobank, AD Knowledge Portal, etc.), and never read such data into the conversation.
  Use `alzres.synthetic` instead. See policy/DATA_ACCESS.md.
- Treat every external resource as unverified until `registry/` says otherwise; follow
  policy/VETTING.md. Read upstream LICENSE files directly before changing a license field.
- Don't copy upstream code into the repo; add it as a pinned dependency. Keep GPL/AGPL code
  out of `src/alzres`.
- Before pushing, run: `pytest`, `ruff check .`, `ruff format --check .`,
  `python tools/check_data_policy.py`, `python tools/build_docs.py --check`.
- After editing `registry/*.yaml` or `evidence/claims.yaml`, run `python tools/build_docs.py`.
- Don't overstate results: synthetic-data tests show the tooling works, not anything about
  Alzheimer's disease.
