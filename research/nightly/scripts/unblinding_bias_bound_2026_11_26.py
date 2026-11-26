"""If amyloid were not a cause, could unblinding alone explain the antibody results?
(night of 2026-11-26, repurposing lens, "assume the amyloid hypothesis is wrong" constraint).

The strongest evidence that removing amyloid helps is two antibody trials. A skeptic's main
alternative is that the benefit is an artefact: the drugs cause visible events (brain swelling
on scans, infusion reactions), so some participants, families and raters could guess who was
on drug, and the main outcome is a rating partly based on interview. This script asks how big
that bias would have to be, and how big it plausibly is.

Published inputs:
    lecanemab   benefit 0.45 points (95% interval 0.23 to 0.67); brain swelling on scans 12.6%
                and infusion reactions 26.4% on drug (doi 10.1056/NEJMoa2212948)
    donanemab   benefit 0.70 points (0.45 to 0.95); swelling 24.0% against 2.1% on placebo;
                infusion reactions 8.7% against 0.5% (doi 10.1001/jama.2023.13239)
    observer bias: where the same trials had both blinded and unblinded assessors of a
                subjective scale, unblinded assessors made the treatment look better by 0.23
                standard deviations (0.06 to 0.40) (doi 10.1503/cmaj.120744)
ASSUMED: the lecanemab placebo rates of swelling (1.7%) and infusion reactions (7.4%), quoted
from memory of the paper; that the two kinds of event occur independently; and that an
"unblinded" participant is rated with the full observer bias. The spread of individual change
is derived from each trial's confidence interval.

PART 1  the bias each unblinded participant would need for the whole benefit to be artefact
PART 2  the share of the benefit that the measured size of observer bias could explain
PART 3  what each reading predicts for an analysis that drops people after such an event

Group-level arithmetic on published numbers; it bounds an argument, it does not settle it.
Not medical advice.
"""

from __future__ import annotations

import numpy as np

OBSERVER_BIAS = (0.06, 0.23, 0.40)  # SD units: low, central, high

TRIALS = {
    "lecanemab": {
        "benefit": 0.45,
        "ci": (0.23, 0.67),
        "n": (859, 875),
        "placebo_decline": 1.66,
        "events_drug": (0.126, 0.264),
        "events_placebo": (0.017, 0.074),
    },
    "donanemab": {
        "benefit": 0.70,
        "ci": (0.45, 0.95),
        "n": (860, 876),
        "placebo_decline": 2.42,
        "events_drug": (0.240, 0.087),
        "events_placebo": (0.021, 0.005),
    },
}


def spread(ci, n) -> float:
    se = (ci[1] - ci[0]) / (2 * 1.96)
    return float(se / np.sqrt(1 / n[0] + 1 / n[1]))


def either(rates) -> float:
    return 1 - (1 - rates[0]) * (1 - rates[1])


def main() -> None:
    for name, t in TRIALS.items():
        sd = spread(t["ci"], t["n"])
        net = {
            "brain swelling only": t["events_drug"][0] - t["events_placebo"][0],
            "infusion reactions only": t["events_drug"][1] - t["events_placebo"][1],
            "either event": either(t["events_drug"]) - either(t["events_placebo"]),
        }
        print(f"=== {name}: benefit {t['benefit']} points; spread of change SD {sd:.2f} ===")
        print("PART 1. Bias needed per unblinded person if the true effect were zero")
        heads = f"{'extra share':>12}{'points':>9}{'in SDs':>8}{'vs decline':>12}"
        print(f"  {'who could guess':<26}{heads}")
        for label, share in net.items():
            need = t["benefit"] / share
            print(
                f"  {label:<26}{share:>12.0%}{need:>9.1f}{need / sd:>8.1f}"
                f"{need / t['placebo_decline']:>11.0%}"
            )
        print("  ('vs decline' = needed bias as a share of the whole decline on placebo)")
        print("PART 2. Share of the benefit explained by measured observer bias")
        print(f"  {'who could guess':<26}" + "".join(f"{f'{b} SD':>10}" for b in OBSERVER_BIAS))
        for label, share in net.items():
            cells = "".join(f"{b * sd * share / t['benefit']:>10.0%}" for b in OBSERVER_BIAS)
            print(f"  {label:<26}{cells}")
        central = OBSERVER_BIAS[1] * sd * net["either event"]
        left = t["benefit"] - central
        print(f"  Central case, either event: {central:.2f} points of bias, leaving {left:.2f}")
        print(
            f"  ({left / t['placebo_decline']:.0%} slowing against the reported "
            f"{t['benefit'] / t['placebo_decline']:.0%}).\n"
        )

    print("PART 3. What an analysis that drops people after an event should show")
    print("  pure artefact   benefit falls to about zero among those with no event")
    print("  real effect     benefit is about unchanged")
    print("  mixed           benefit shrinks by the share in Part 2")
    print("\nReading. For the whole benefit to be artefact, each person who could guess would")
    print("have to be rated one to several points better than the truth - for brain swelling")
    print("alone, more than the entire decline seen on placebo. That is not credible. But the")
    print("size of observer bias measured in other trials, applied to everyone with a visible")
    print("event, would account for roughly a quarter to a third of the headline benefit. So")
    print("unblinding cannot rescue the claim that amyloid removal does nothing, yet it could")
    print("mean the true effect is somewhat smaller than reported. The published analyses that")
    print("censor people after an event are the direct check. Assumed inputs are listed above.")


if __name__ == "__main__":
    main()
