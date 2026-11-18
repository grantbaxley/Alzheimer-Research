"""Does a nightly dip add up? Putting numbers on orexin-antagonist-early-window
(night of 2026-11-18, cross-domain lens, revisit).

A single evening dose of the sleep drug suvorexant lowered spinal-fluid amyloid-beta by roughly
10-20% for some hours (Lucey et al., Ann Neurol 2023, doi 10.1002/ana.26641). Our idea proposed a
prevention trial with amyloid-PET endpoints to see whether that nightly dip accumulates into
slower plaque build-up. Before asking anyone to run it, this script asks three questions:

  1. How much does a part-of-the-day dip lower the 24-hour average? (arithmetic)
  2. How much slower would plaque then accumulate, if deposition depends on concentration to the
     power 1 (simple deposition), 2 (secondary nucleation, the dominant in-vitro mechanism for
     amyloid-beta 42; Cohen et al., PNAS 2013, doi 10.1073/pnas.1218402110) or 3?
  3. How many people would a PET trial need to SEE that slowing - and is the slowing even as
     large as the one that already failed to help cognition? In the A4 prevention trial the
     antibody arm accumulated about 11.6 Centiloids against 19.3 on placebo over 240 weeks, a
     40% slowing, with no cognitive benefit (Sperling et al., NEJM 2023,
     doi 10.1056/NEJMoa2305032).

Three worlds for what the spinal-fluid dip means:
    PRODUCTION  the dip is real lower release into brain tissue during the dosed hours
    REBOUND     release is lower at night but made up during the day (24-hour total conserved)
    MARKER      the dip is a sampling/clearance-route shift; tissue concentration is unchanged
Only the first can slow plaque at all.

The trial arithmetic is checked by simulation. The spread of accumulation and the scan noise are
ASSUMED round numbers, not estimates, and the A4 Centiloid figures are quoted as recalled from the
paper - neither was re-checked against the source on this night. Synthetic; not a drug claim and
not medical advice.
"""

from __future__ import annotations

import numpy as np
from scipy import stats

RATE = 4.3  # placebo accumulation, Centiloids/year (A4 placebo: 19.3 over about 4.6 years)
SLOPE_SD = 3.0  # between-person SD of true annual change, Centiloids/year (assumed)
MEAS_SD = 4.0  # measurement SD of one scan, Centiloids (assumed; test-retest scale)
A4_SLOWING = 1 - 11.6 / 19.3


def daily_reduction(dip: float, hours: float) -> float:
    return dip * hours / 24


def plaque_slowing(mean_reduction: float, order: float) -> float:
    return 1 - (1 - mean_reduction) ** order


def change_sd(years: float) -> float:
    """SD of an individual's measured change over the trial (true slope spread + two scans)."""
    return float(np.sqrt((SLOPE_SD * years) ** 2 + 2 * MEAS_SD**2))


def n_per_arm(slowing: float, years: float, power: float = 0.8, alpha: float = 0.05) -> float:
    delta = RATE * years * slowing
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return 2 * (z * change_sd(years) / delta) ** 2


def simulated_power(slowing: float, years: float, n: int, rng, reps: int = 2000) -> float:
    hits = 0
    for _ in range(reps):
        arms = []
        for rate in (RATE, RATE * (1 - slowing)):
            true = rng.normal(rate, SLOPE_SD, n) * years
            arms.append(true + rng.normal(0, MEAS_SD, n) - rng.normal(0, MEAS_SD, n))
        res = stats.ttest_ind(arms[0], arms[1])
        hits += res.pvalue < 0.05 and arms[1].mean() < arms[0].mean()
    return hits / reps


def main() -> None:
    rng = np.random.default_rng(0)
    print("(1) 24-hour average reduction from a night-time dip (PRODUCTION world):")
    print("    dip   hours   daily mean reduction")
    cases = ((0.10, 8), (0.20, 8), (0.20, 12), (0.20, 24))
    for dip, hours in cases:
        print(f"    {dip:.0%}   {hours:>3}     {daily_reduction(dip, hours):.1%}")
    print("    (the last row is an upper bound: the full dip held around the clock)\n")

    print("(2) Slowing of plaque accumulation, by how steeply deposition depends on concentration:")
    print("    daily reduction    order 1    order 2    order 3")
    for dip, hours in cases:
        r = daily_reduction(dip, hours)
        cells = "".join(f"{plaque_slowing(r, k):>11.1%}" for k in (1, 2, 3))
        print(f"    {r:>8.1%}       {cells}")
    print(f"    For scale: the antibody in the A4 trial slowed accumulation by {A4_SLOWING:.0%}")
    print("    and cognition did not benefit.")
    print("    REBOUND and MARKER worlds: 0% in every cell.\n")

    print("(3) People per arm for 80% power to see the slowing on amyloid PET")
    print(
        f"    (placebo {RATE} CL/yr; spread of true change {SLOPE_SD} CL/yr; scan noise "
        f"{MEAS_SD} CL)"
    )
    print("    slowing    2-year trial    4.5-year trial")
    for s in (0.033, 0.067, 0.13, 0.19, 0.27, A4_SLOWING):
        print(f"    {s:>6.1%} {n_per_arm(s, 2):>14,.0f} {n_per_arm(s, 4.5):>17,.0f}")
    print()

    print("    Simulation check of the formula (target power 0.80):")
    for s, years in ((0.13, 4.5), (A4_SLOWING, 4.5), (0.27, 2)):
        n = int(round(n_per_arm(s, years)))
        print(
            f"      slowing {s:.0%}, {years} years, n={n:,} per arm -> simulated power "
            f"{simulated_power(s, years, n, rng):.2f}"
        )
    print()

    print("(4) What the slowing would buy: years of delay in amyloid build-up after 10 years")
    for s in (0.067, 0.13, 0.27):
        print(f"    slowing {s:.1%}: about {10 * s:.1f} years' worth of accumulation avoided")
    print()

    print("Reading. A dip confined to the night shrinks to a few percent of the 24-hour average.")
    print("With simple deposition the slowing is 3-10%; only steep (order 2-3) dependence on")
    print("concentration lifts it to 7-27%, and only the round-the-clock upper bound reaches the")
    print("40% that already failed to move cognition in A4. Seeing a 3-7% slowing on PET needs")
    print("thousands of people per arm for years; 13% still needs several hundred. So a PET trial")
    print("is a poor test of this idea: a null would be uninformative and a positive would predict")
    print("little clinical benefit. If the dip is rebound-compensated or only a marker shift, the")
    print("expected effect is zero. Assumed spreads: halving or doubling them moves the sample")
    print("sizes about four-fold either way, which does not rescue the small-effect rows.")


if __name__ == "__main__":
    main()
