"""Who will not progress? What a second scan and a reserve marker each add
(night of 2026-11-21, resilience lens, "start from sleep" constraint; revisit of
nonprogressor-rate-plus-synapse).

Our idea was a two-part test for amyloid-positive people who will stay well: "where you are"
(a marker of synaptic integrity or reserve) plus "where you are going" (the person's own rate of
tau build-up from repeat scans). This script asks how much each part can add once realistic
measurement noise is included, and how good a cheap reserve marker - for example slow-wave power
from an at-home sleep recording - would have to be to match a second scan.

Synthetic people (no real data):
    tau burden above the scan's floor grows exponentially at a personal rate;
    each person has a hidden RESERVE that sets how much tau they tolerate before symptoms;
    a person "progresses" if their tau passes their own tolerance within five years.
What can be measured:
    LEVEL     one tau scan, with test-retest error
    RATE      the change between two scans two years apart (or four years apart)
    RESERVE   a marker that correlates with the hidden reserve at a chosen validity
Each combination is scored by AUC (0.5 = coin toss, 1.0 = perfect) for predicting who stays
well, using a model fitted on half the people and tested on the other half.

ASSUMED parameters (see the night's log for the published values they sit near): personal
growth rates with mean RATE_MEAN and between-person SD RATE_SD per year; scan test-retest error
SCAN_SD in SUVR units, shown at three values because it differs by tracer and region; about a
quarter of people progressing in five years. Synthetic illustration only; says nothing about any
person.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import rankdata

N = 40_000
RATE_MEAN, RATE_SD = 0.06, 0.08  # per year
SCAN_SDS = (0.02, 0.04, 0.06)  # SUVR, test-retest
HORIZON = 5.0
RESERVE_SPREAD = 0.45  # log-scale spread of tolerated tau
TOLERANCE = 0.36  # median tolerated tau burden (sets the share who progress)


def auc(score, outcome) -> float:
    r = rankdata(score)
    pos = outcome.astype(bool)
    n1, n0 = pos.sum(), (~pos).sum()
    return float((r[pos].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def fit_logistic(x, y, iters: int = 25):
    x = np.column_stack([np.ones(len(y)), x])
    beta = np.zeros(x.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(x @ beta, -30, 30)))
        w = p * (1 - p) + 1e-9
        beta += np.linalg.solve(x.T @ (x * w[:, None]) + 1e-6 * np.eye(x.shape[1]), x.T @ (y - p))
    return beta


def score(features, y) -> float:
    x = np.column_stack(features)
    x = (x - x.mean(0)) / x.std(0)
    half = len(y) // 2
    beta = fit_logistic(x[:half], y[:half])
    return auc(np.column_stack([np.ones(len(y) - half), x[half:]]) @ beta, y[half:])


def main() -> None:
    rng = np.random.default_rng(0)
    tau0 = 0.15 * np.exp(rng.normal(0, 0.5, N))
    rate = rng.normal(RATE_MEAN, RATE_SD, N)
    reserve = rng.normal(0, 1, N)

    def tau_at(t):
        return tau0 * np.exp(rate * t)

    stays_well = (tau_at(HORIZON) < TOLERANCE * np.exp(RESERVE_SPREAD * reserve)).astype(float)
    true_2y = (tau_at(2.0) - tau0) / 2
    true_4y = (tau_at(4.0) - tau0) / 4
    print(f"{N:,} synthetic amyloid-positive people; {1 - stays_well.mean():.0%} progress in")
    print(
        f"five years. True yearly change in scan signal: mean {true_2y.mean():.3f}, between-person"
    )
    print(f"SD {true_2y.std():.3f} SUVR.\n")

    print("A. Is a personal rate measurable? Share of the measured rate's variation that is real,")
    print("   and AUC for predicting who stays well.\n")
    print(f"   {'scan error (SUVR)':<20}{'rate reliability':>18}{'':>4}{'AUC':>6}")
    heads = f"{'2 years':>9}{'4 years':>9}{'':>4}{'level':>7}{'+2y rate':>10}{'+4y rate':>10}"
    print(f"   {'':<20}{heads}")
    for sd in SCAN_SDS:
        level = 1 + tau0 + rng.normal(0, sd, N)
        r2 = (1 + tau_at(2.0) + rng.normal(0, sd, N) - level) / 2
        r4 = (1 + tau_at(4.0) + rng.normal(0, sd, N) - level) / 4
        rel2 = np.corrcoef(r2, true_2y)[0, 1] ** 2
        rel4 = np.corrcoef(r4, true_4y)[0, 1] ** 2
        cells = "".join(
            f"{score(f, stays_well):>9.3f}" for f in ([level], [level, r2], [level, r4])
        )
        print(f"   {sd:<20}{rel2:>9.2f}{rel4:>9.2f}{'':>4}{cells}")
    ceiling = score([1 + tau0, true_2y], stays_well)
    print(f"   level and rate both measured without error: AUC {ceiling:.3f}\n")

    sd = SCAN_SDS[1]
    level = 1 + tau0 + rng.normal(0, sd, N)
    r2 = (1 + tau_at(2.0) + rng.normal(0, sd, N) - level) / 2
    print(f"B. What a reserve marker adds (scan error {sd} SUVR). Validity = its correlation with")
    print("   the hidden reserve.\n")
    print(f"   {'marker validity':<18}{'level + marker':>16}{'level + marker + 2y rate':>28}")
    for validity in (0.0, 0.3, 0.5, 0.7, 1.0):
        marker = validity * reserve + np.sqrt(1 - validity**2) * rng.normal(0, 1, N)
        a, b = score([level, marker], stays_well), score([level, marker, r2], stays_well)
        print(f"   {validity:<18}{a:>16.3f}{b:>28.3f}")
    everything = score([1 + tau0, reserve, true_2y], stays_well)
    print(f"   everything known without error: AUC {everything:.3f}")


if __name__ == "__main__":
    main()
