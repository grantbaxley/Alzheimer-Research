"""Step, fading step, or slope? Reading what kind of benefit a treatment report shows
(night of 2026-11-20, reversal-biology lens, "combine two catalogue ideas" constraint:
benefit-timing-shape-test x reversible-ceiling-staging).

A treatment can help in three different ways, and they leave different shapes over time:
    FADING STEP      a quick gain that disappears: what placebo and practice effects look like
    LASTING STEP     a quick gain that stays while decline continues in parallel: restored
                     function (a real reversal, or a symptomatic lift while the drug is on board)
    SLOPE            no quick gain, but slower decline from then on: disease slowed, nothing
                     restored

PART 1 asks how much of the lecanemab benefit could be a lasting step - function restored by
removing amyloid - using only the two randomised numbers in the public record: a difference of
0.17 CDR-SB points at 6 months (95% interval 0.05 to 0.29) and 0.45 at 18 months (0.23 to 0.67)
(van Dyck et al., NEJM 2023, doi 10.1056/NEJMoa2212948; the 6-month figure from a published
summary of the paper). With difference(t) = STEP + RATE * t, two visits give both numbers.

PART 2 is a benchmark for uncontrolled reports of the form "k of n patients improved": how
often that happens by chance alone if a given share of untreated patients improve at the same
visit.

PART 3 shows what the three shapes look like at 12, 28 and 52 weeks for a gain of the same
initial size, to compare against a report's time course.

Aggregate published numbers and arithmetic; the two visit estimates are treated as independent,
which overstates the uncertainty somewhat. Not medical advice.
"""

from __future__ import annotations

import numpy as np
from scipy import stats

D6, CI6 = 0.17, (0.05, 0.29)
D18, CI18 = 0.45, (0.23, 0.67)
BASELINE_DEFICIT = 3.2  # mean CDR-SB at entry in the trial


def se(ci) -> float:
    return (ci[1] - ci[0]) / (2 * 1.96)


def main() -> None:
    rng = np.random.default_rng(0)
    d6 = rng.normal(D6, se(CI6), 200_000)
    d18 = rng.normal(D18, se(CI18), 200_000)
    rate = (d18 - d6) / 12  # points per month
    step = d6 - 6 * rate
    lo, hi = np.percentile(step, [2.5, 97.5])
    print("PART 1. Lecanemab benefit split into a lasting step and a slope")
    print(f"  step (function restored): {np.median(step):+.2f} CDR-SB points")
    print(f"      95% range {lo:+.2f} to {hi:+.2f}")
    r_lo, r_hi = np.percentile(rate * 12, [2.5, 97.5])
    print(f"  slope (decline avoided): {np.median(rate) * 12:.2f} points per year")
    print(f"      95% range {r_lo:.2f} to {r_hi:.2f}")
    print(
        f"  For scale, the average deficit at entry was {BASELINE_DEFICIT} points, so the largest"
    )
    print(f"  step the data allow is about {hi / BASELINE_DEFICIT:.0%} of the existing deficit.")
    print("  The benefit is, as far as two visits can show, all slope: slowing, not restoring.\n")

    print("PART 2. 'k of n improved' with no control group: chance of seeing it anyway")
    print("  share of untreated patients who improve at that visit:   20%    30%    40%    50%")
    for k, n in ((5, 6), (4, 5), (6, 6)):
        cells = "".join(f"{stats.binom.sf(k - 1, n, p):>7.1%}" for p in (0.2, 0.3, 0.4, 0.5))
        print(f"  at least {k} of {n} improve:{'':<31}{cells}")
    print("  The count alone is weak evidence unless few untreated patients improve; the SIZE")
    print("  of each person's change against the test's retest noise carries the information.\n")

    print("PART 3. Three shapes for a gain of 1.0 at 12 weeks (arbitrary units, + is better)")
    print("  untreated decline assumed 1.0 per year; fading step halves every 16 weeks")
    print(f"  {'shape':<14}{'12 wk':>8}{'28 wk':>8}{'52 wk':>8}   after stopping")
    weeks = np.array([12, 28, 52])
    decline = -weeks / 52
    rows = (
        ("fading step", 0.5 ** ((weeks - 12) / 16), "nothing to lose"),
        ("lasting step", np.ones(3), "kept if restored; lost if symptomatic"),
        ("slope", 0.5 * weeks / 52, "kept"),  # half of the decline avoided
    )
    for name, gain, note in rows:
        cells = "".join(f"{v:>+8.2f}" for v in decline + gain)
        print(f"  {name:<14}{cells}   {note}")
    print("  (values are change from the person's own baseline)")
    print("  A gain at 12 weeks that is gone by 52 is the fading-step shape. A lasting step and a")
    print("  true reversal look the same until treatment stops, so a reversal claim needs a")
    print("  randomised stop: restored function stays, a symptomatic lift goes.")


if __name__ == "__main__":
    main()
