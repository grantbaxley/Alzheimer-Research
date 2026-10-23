"""Feasibility arithmetic for the night of 2026-10-23 (repurposing lens).

Tonight's lens does not map onto the repo's tau-spreading tools, so this is NOT a disease
model. It is standard trial-design arithmetic (numpy/scipy only) supporting two ideas:
`vaccine-trained-immunity` and `repurposing-credibility-gate`.

Two small calculations:

1. Bias gap. Observational cohorts put the shingles-vaccine dementia hazard ratio near 0.49-0.74,
   while a regression-discontinuity natural experiment puts it near 0.80 (the ~20% relative
   reduction). The gap is the plausible scale of healthy-vaccinee bias. We just report the
   implied bias factor so the inflation is explicit.

2. Events needed. For an active-comparator design (two vaccinated groups, which removes
   healthy-user self-selection), how many dementia events must accrue to detect a given true
   hazard ratio at 80% power, two-sided alpha 0.05? Uses Schoenfeld's formula
   E = (z_alpha/2 + z_beta)^2 / (p*(1-p)*ln(HR)^2), with p=0.5 allocation. This says whether the
   de-biased effect is even detectable without an implausibly large cohort.

All numbers are design arithmetic, not findings about the disease or any drug.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import norm


def events_for_hr(hr: float, power: float = 0.80, alpha: float = 0.05, p: float = 0.5) -> int:
    z = norm.ppf(1 - alpha / 2) + norm.ppf(power)
    e = z**2 / (p * (1 - p) * np.log(hr) ** 2)
    return int(np.ceil(e))


def main() -> None:
    print("1. Healthy-vaccinee bias gap (shingles vaccine, dementia HR):")
    rd = 0.80  # regression-discontinuity (de-biased) estimate
    for cohort in (0.49, 0.67, 0.74):
        print(
            f"   cohort HR {cohort:.2f} vs RD HR {rd:.2f}  ->  "
            f"bias factor {rd / cohort:.2f}x (cohort overstates the effect)"
        )

    print("\n2. Dementia events needed (active-comparator, 80% power, two-sided 0.05):")
    for hr in (0.80, 0.85, 0.90):
        print(f"   true HR {hr:.2f}: {events_for_hr(hr):>5d} events")
    print(
        "\nReading: the de-biased effect (HR ~0.80) needs on the order of hundreds of events - "
        "feasible in a large active-comparator cohort - while HR 0.90 needs thousands, so a "
        "credible design is powered only for the larger de-biased effects, not the attenuated ones."
    )
    print("Design arithmetic only; not a disease model and not evidence about any drug.")


if __name__ == "__main__":
    main()
