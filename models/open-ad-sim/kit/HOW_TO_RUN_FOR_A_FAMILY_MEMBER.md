# Running the model for a family member, privately

The model describes a *type* of patient. You can narrow the type to what a clinic has measured for someone you love, but **their information stays on your computer** (Rule #1, `policy/PRIVACY.md` at the repository root). Ask for their consent, or their legal representative's, before you use their information at all.

## 1. One-time setup

```bash
git clone https://github.com/grantbaxley/alzheimer-research && cd alzheimer-research
pip install -e .                             # numpy, scipy, pyyaml
git config core.hooksPath .githooks          # the privacy gate runs before every commit and push
mkdir -p ~/.config/alzheimer-research
nano ~/.config/alzheimer-research/denylist.txt   # one term per line: the person's names, initials, nicknames,
                                                 # relatives, doctors, clinics, town, street, dates of birth and
                                                 # visits in every format, record numbers, and exact test values
                                                 # (e.g. a Centiloid to one decimal)
cd models/open-ad-sim
```

The denylist lives outside the repository, so the protected words never appear in it. If you ever try to commit a file, a file name or a commit message containing one of them, the commit is refused. (An older `~/.config/open-ad-sim/denylist.txt` is still read.)

## 2. Describe the person as ranges, in `patients/` (git-ignored)

Copy the closest profile from `profiles/profiles.yaml` into `patients/my_relative.yaml` and set each range around what was measured, wide enough to cover measurement error:

```yaml
age: [lo, hi]            # a few years either side
centiloid: [lo, hi]      # amyloid PET Centiloid ± ~7 (test-retest and tracer differences)
cdr_sb: [lo, hi]         # CDR sum of boxes ± 1 (single-visit noise is about ±1 point)
tau: unknown             # negative | positive | high, if tau PET or a validated blood test has staged it
atrophy: unknown         # present | absent, from the MRI read (medial temporal atrophy)
```

Leave genotype out: APOE has no effect in this model, and there is no side-effect (ARIA) module yet.

## 3. Run it

```bash
python3 model/run_ensemble.py --patient patients/my_relative.yaml    # all six fitted versions; ~10 min on 2 cores
```

That writes `results/RESULTS_local.md`. `results/` and `patients/` are git-ignored, and the privacy gate rejects both folders even if `.gitignore` is bypassed. Nothing you run here leaves your computer.

Use `run_ensemble.py` rather than looping over `scenarios.py` yourself: each fitted version needs its own structural variant (`ADSIM_VARIANT`), which `run_ensemble.py` sets for you. `scenarios.py` and `validate.py` refuse to run a version under the wrong variant.

## 4. Read the results honestly

- Every number is a **modeled hypothesis for virtual patients who fit those ranges**, not a forecast for your relative. People vary far more than any model.
- Report **ranges across ensemble members and attribution methods**, never a single number.
- **No side effects are modeled.** Antibody scenarios show modeled benefit only. Brain swelling or bleeding on amyloid antibodies (ARIA) is not simulated, and its risk rises steeply with the number of APOE ε4 copies. Weigh it with the treating neurologist.
- The least certain parts: how brain damage maps onto symptoms, how fast surviving neurons could recover, and anything labeled *hypothetical* (no such therapy exists).
- Read the model's vetting record (`research/reproductions/open-ad-sim/README.md` at the repository root) for what has and has not been checked.
- Bring questions to the treating neurologist; the model is for thinking, not for deciding.

## 5. Sharing

You are welcome to share what you learn about the **model** (bugs, better calibration data, new validation checks) through issues and pull requests. Never paste a real person's measurements, scans, reports, or identifying details into an issue, a pull request, a discussion or a commit message, or describe them there in a way that points to a real person.
