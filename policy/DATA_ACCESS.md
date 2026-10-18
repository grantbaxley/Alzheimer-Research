# Data access policy

**This repository ships code, not participant data.** Almost every major Alzheimer's
cohort is governed by a data use agreement (DUA) that forbids redistribution. Breaking
one can end a researcher's access and harm the cohort's participants and future
science. These rules are absolute.

## Rules

1. **No participant-level data, ever.** No rows, images, scans, per-subject derived
   features, model outputs indexed by subject, or screenshots of any of these, from
   any DUA-governed source (ADNI, OASIS, AIBL, NACC, A4/LEARN, UK Biobank, AD Knowledge
   Portal controlled tier, ADSP/NIAGADS, GNPC, EPAD, DPUK, HCP-Aging).
2. **Bring your own data.** Loaders read from a path the user supplies (e.g. an
   environment variable or config file outside the repo). Nothing downloads gated
   data automatically.
3. **No gated data in AI tools.** Do not paste, upload or send DUA-governed data to
   cloud LLMs, AI coding assistants or other third-party AI services. The ADNI DUA
   explicitly calls this a violation. Use synthetic data when working with AI tools.
4. **Aggregates need clearance.** Group-level tables derived from ADNI must be cleared
   with the ADNI Data and Publications Committee before posting; check each cohort's
   rules for the equivalent. Suppress small cells.
5. **Open data is linked, not re-hosted.** SEA-AD (Allen Institute terms) and OpenNeuro
   (CC0) are fetched at runtime from the source, pinned by version and checksum. Keep
   upstream terms; never relabel them under this project's license.
6. **No mirrors.** Kaggle, Hugging Face or GitHub re-uploads of cohort data are banned;
   they are usually DUA breaches and often leakage-prone 2D slices.
7. **CI runs only on synthetic and CC0 data.** `alzres.synthetic` exists so that every
   test and demo can be public.

## Enforcement

- `tools/check_data_policy.py` blocks imaging/raw-data file types (NIfTI, DICOM,
  MGZ, EDF, h5ad, pickles and others), cohort participant ID patterns and files over
  5 MB. It runs in CI and as a pre-commit hook (`pre-commit install`).
- `.gitignore` excludes `data/`, `private/` and common imaging formats.
- If gated data is committed by mistake: do not just delete it in a new commit. Tell
  the maintainers immediately; history must be rewritten and the cohort may need to be
  notified under its DUA.

## Access terms at a glance

Per-cohort access tier, license class and caveats live in
[`registry/data.yaml`](../registry/data.yaml) and the
[landscape report](../docs/landscape-2026-10/report.md#every-major-cohort-is-dua-gated-so-the-repo-must-ship-code-not-data).
Terms change (ADNI and SEA-AD pages carried "under review" banners in Oct 2026), so
re-read the primary source before relying on them.
