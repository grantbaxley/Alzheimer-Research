## What and why

## Checklist

- [ ] **Rule #1:** nothing here (files, file names, commit messages, this description) could identify a real person: no names, initials, dates, places, clinicians, exact test values, documents or photos (policy/PRIVACY.md)
- [ ] No participant-level or gated-cohort data, and none was sent to AI tools (policy/DATA_ACCESS.md)
- [ ] New external resources have registry records with licenses read from the LICENSE file
- [ ] `our_status` changes have a `verification` pointer
- [ ] Models are tested on synthetic ground truth and compared against baselines/nulls
- [ ] Claims carry sources and an evidence grade; no subgroup or biomarker-only results presented as benefit
- [ ] `python tools/build_docs.py` re-run if registry/ or evidence/ changed
