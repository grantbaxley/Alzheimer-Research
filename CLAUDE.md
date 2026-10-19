# Notes for AI coding agents

- **Rule #1 (policy/PRIVACY.md): nothing that could identify a real person ever enters this
  repository**: not files, file names, commit messages, branch names, PR or issue text. If a
  user shares a real person's details in chat, do not write them into the repository; use
  ranges in a git-ignored `patients/` folder only if they ask you to run something locally.
  Never open files under `patients/`, `private/` or `local/`, never read or print a privacy
  denylist, and never weaken `tools/check_data_policy.py` or add allowlist entries for
  anything about a person.
- Use a no-reply commit identity; CI rejects commits whose author or committer e-mail is not
  a no-reply address.
- Never commit or process participant-level data from DUA cohorts (ADNI, OASIS, NACC,
  UK Biobank, AD Knowledge Portal, etc.), and never read such data into the conversation.
  Use `alzres.synthetic` instead. See policy/DATA_ACCESS.md.
- Treat every external resource as unverified until `registry/` says otherwise; follow
  policy/VETTING.md. Read upstream LICENSE files directly before changing a license field.
- Don't copy upstream code into the repo; add it as a pinned dependency. Keep GPL/AGPL code
  out of `src/alzres`.
- Before pushing, run: `pytest`, `ruff check .`, `ruff format --check .`,
  `python tools/check_data_policy.py`, `python tools/check_data_policy.py --history`,
  `python tools/build_docs.py --check`.
- After editing `registry/*.yaml` or `evidence/claims.yaml`, run `python tools/build_docs.py`.
- Don't overstate results: synthetic-data tests show the tooling works, not anything about
  Alzheimer's disease.
