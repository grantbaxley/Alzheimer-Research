"""Prevention-at-population-scale arithmetic for the night of 2026-10-25.

Tonight's lens does not map onto the tau-spreading tools, so this is demographic arithmetic
(numpy only), not a disease model. It illustrates the classic prevention claim (Brookmeyer):
because dementia incidence rises steeply with age while mortality removes people before they
can develop it, shifting age-of-onset LATER by a few years cuts prevalence by much more than
the shift itself.

Toy model of a synthetic cohort:
  - age-specific dementia incidence rises exponentially, doubling about every 5 years
    (a standard epidemiological regularity), applied as a yearly hazard;
  - a competing all-cause mortality hazard also rises with age;
  - an intervention shifts the onset hazard curve `delay` years later (you reach a given
    age's risk only when `delay` years older), modeling "delayed onset".
We follow the cohort from age 65 to 100 and report lifetime probability of developing dementia
and point prevalence among survivors, with and without the delay.

Numbers are illustrative of the mechanism (steep age-incidence + competing mortality), not an
estimate for any real population. Synthetic arithmetic only.
"""

from __future__ import annotations

import numpy as np

AGES = np.arange(65, 101)
INCIDENCE_AT_65 = 0.002  # yearly hazard of onset at age 65 (illustrative)
DOUBLING_YEARS = 5.0  # incidence doubles about every 5 years
MORT_AT_65 = 0.012  # yearly all-cause mortality hazard at 65 (illustrative)
MORT_DOUBLING = 8.0  # mortality doubles about every 8 years


def onset_hazard(age: np.ndarray, delay: float) -> np.ndarray:
    eff_age = age - delay  # delayed onset: risk of age a is reached `delay` years later
    return INCIDENCE_AT_65 * 2.0 ** ((eff_age - 65) / DOUBLING_YEARS)


def mortality_hazard(age: np.ndarray) -> np.ndarray:
    return MORT_AT_65 * 2.0 ** ((age - 65) / MORT_DOUBLING)


def simulate(delay: float) -> dict:
    alive_well = 1.0  # alive, no dementia
    alive_dem = 0.0  # alive, with dementia
    ever = 0.0  # cumulative lifetime incidence
    prevalence_track = []
    inc = np.clip(onset_hazard(AGES, delay), 0, 1)
    mort = np.clip(mortality_hazard(AGES), 0, 1)
    for i, _age in enumerate(AGES):
        new_cases = alive_well * inc[i]
        ever += new_cases
        alive_well -= new_cases
        alive_dem += new_cases
        # mortality removes from both pools
        alive_well *= 1 - mort[i]
        alive_dem *= 1 - mort[i]
        survivors = alive_well + alive_dem
        prevalence_track.append(alive_dem / survivors if survivors > 0 else 0.0)
    return {
        "lifetime_incidence": ever,
        "peak_prevalence": max(prevalence_track),
    }


def main() -> None:
    base = simulate(delay=0.0)
    print(f"{'delay (yr)':>11} {'lifetime incidence':>19} {'peak prevalence':>16}")
    print(f"{0.0:>11.1f} {base['lifetime_incidence']:>19.3f} {base['peak_prevalence']:>16.3f}")
    for d in (1.0, 2.0, 5.0):
        r = simulate(delay=d)
        li_drop = (
            100
            * (base["lifetime_incidence"] - r["lifetime_incidence"])
            / base["lifetime_incidence"]
        )
        pv_drop = 100 * (base["peak_prevalence"] - r["peak_prevalence"]) / base["peak_prevalence"]
        print(
            f"{d:>11.1f} {r['lifetime_incidence']:>19.3f} {r['peak_prevalence']:>16.3f}"
            f"   (lifetime -{li_drop:.0f}%, peak prevalence -{pv_drop:.0f}%)"
        )
    print(
        "\nReading: a 5-year delay cuts lifetime incidence and peak prevalence by far more than\n"
        "5/35 of the span, because onset risk is back-loaded into late ages many people do not\n"
        "survive to reach - why 'delay onset 5 years' is such a powerful population lever."
    )
    print("Illustrative demographic arithmetic; not a disease model, not an estimate.")


if __name__ == "__main__":
    main()
