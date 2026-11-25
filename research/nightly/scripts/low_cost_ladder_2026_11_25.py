"""What do the cheap options buy? Months of decline deferred, per person and per dollar
(night of 2026-11-25, inversion lens, "under 100 dollars per person per year" constraint).

Working backwards from "cognition improves and stays improved", this script puts the low-cost
options that have randomised or natural-experiment evidence on one scale: MONTHS of decline or
of dementia onset deferred. Three kinds of published effect are converted:

  step      a one-time gain that lasts while the intervention continues: gain / yearly decline
  hazard    a lower rate of new dementia or mild impairment: because dementia incidence roughly
            doubles every five years of age, a hazard ratio HR delays onset by about
            5 * log2(1/HR) years
  slope     slower decline while a programme runs: fraction slowed * months of treatment

Each is then multiplied by an ASSUMED chance that the effect is real, set from how well it has
been confirmed (the reasoning is in the night's log and follows the base-rate model of
2026-11-22), and divided by a five-year cost.

Published inputs (sources in the log): blood-pressure lowering RR 0.85; shingles vaccination
about 20% fewer diagnoses among the vaccinated; a daily multivitamin +0.07 SD; speed training
HR 0.87 by intention to treat; a generic symptomatic drug +1.05 points on a 30-point screen in
diagnosed Alzheimer's against a decline of 1.84 points a year; a plaque-removing antibody 27%
slower decline. Costs are approximate US prices for the product alone; the antibody's yearly
list price is as widely reported and was not re-checked on this night.

IMPORTANT: the rows are measured in DIFFERENT people (healthy older adults, people with high
blood pressure, people with diagnosed Alzheimer's) and are not interchangeable. The table ranks
value for money within its own assumptions; it is not advice to anyone. Not medical advice.
"""

from __future__ import annotations

import math

HEALTHY_DECLINE = 0.05  # SD per year in healthy older adults (published range 0.035-0.067)
HORIZON_YEARS = 5


def delay_from_hazard(hr: float) -> float:
    """Months of onset delay implied by a hazard ratio, incidence doubling every five years."""
    return 12 * 5 * math.log2(1 / hr)


ROWS = (
    # name, who, kind, months if real, low, high, chance real, five-year cost in dollars
    (
        "blood-pressure lowering (generic)",
        "adults with high blood pressure",
        "hazard",
        delay_from_hazard(0.85),
        delay_from_hazard(0.95),
        delay_from_hazard(0.76),
        0.80,
        50,
    ),
    (
        "symptomatic drug (generic)",
        "diagnosed Alzheimer's",
        "step",
        12 * 1.05 / 1.84,
        12 * 0.73 / 1.84,
        12 * 1.37 / 1.84,
        0.95,
        100,
    ),
    (
        "shingles vaccination (two doses)",
        "older adults",
        "hazard",
        delay_from_hazard(0.80),
        delay_from_hazard(0.935),
        delay_from_hazard(0.666),
        0.30,
        485,
    ),
    (
        "daily multivitamin",
        "healthy older adults",
        "step",
        12 * 0.07 / HEALTHY_DECLINE,
        12 * 0.03 / HEALTHY_DECLINE,
        12 * 0.11 / HEALTHY_DECLINE,
        0.35,
        160,
    ),
    (
        "speed-of-processing training",
        "healthy older adults",
        "hazard",
        delay_from_hazard(0.87),
        0.0,
        delay_from_hazard(0.72),
        0.15,
        96,
    ),
    (
        "plaque-removing antibody (for scale)",
        "early Alzheimer's, amyloid-positive",
        "slope",
        0.27 * 12 * HORIZON_YEARS,
        0.14 * 12 * HORIZON_YEARS,
        0.40 * 12 * HORIZON_YEARS,
        0.95,
        26_500 * HORIZON_YEARS,
    ),
)


def main() -> None:
    print("Months of decline or dementia onset deferred if the effect is real; the chance it")
    print("is real (assumed); and expected months per 100 dollars, with cost counted over")
    print(f"{HORIZON_YEARS} years.\n")
    head = f"  {'option':<38}{'months':>7}{'(range)':>12}{'chance':>8}{'expected':>10}"
    print(head + f"{'5-yr cost':>11}{'per $100':>10}")
    for name, who, _kind, months, low, high, chance, cost in ROWS:
        expected = months * chance
        per100 = expected / cost * 100
        rng = f"({low:.0f}-{high:.0f})"
        print(
            f"  {name:<38}{months:>7.0f}{rng:>12}{chance:>8.0%}{expected:>10.1f}"
            f"{cost:>11,}{per100:>10.2f}"
        )
        print(f"      measured in: {who}")
    print("\nReading. The cheap options with the firmest evidence defer about as many months per")
    print("person as the expensive one, for a few thousandths of the cost - but in different")
    print("people and by different routes. Only one row is a gain in function (the symptomatic")
    print("drug), and that gain is lost on stopping; the rest delay onset. None is a reversal.")
    print("The ranking is driven as much by the assumed chance that each effect is real as by")
    print("its size: the two rows resting on a single trial or on natural experiments would")
    print("move most if their pending trials read out. Different populations; product cost")
    print("only; assumed chances. A way to compare claims, not a recommendation.")


if __name__ == "__main__":
    main()
