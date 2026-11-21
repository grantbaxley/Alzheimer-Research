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

ASSUMED parameters (see the night's log for the published values they sit near). The key
unknown is how much people truly differ in their rate of build-up, so two scenarios are run: a
LOW and a HIGH between-person spread, bracketing the range implied by published scan data
(observed spread of yearly change about 0.026 SUVR including noise; implied true spread roughly
0.005 to 0.02). Scan test-retest error is shown at three values because it differs by tracer.
About a quarter of people progress in five years in every scenario. Synthetic illustration only;
says nothing about any person.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import rankdata

N = 40_000
RATE_MEAN = 0.06  # per year
RATE_SPREADS = {"LOW": 0.025, "HIGH": 0.08}  # between-person SD of the yearly growth rate
SCAN_SDS = (0.02, 0.04, 0.06)  # SUVR, test-retest
HORIZON = 5.0
RESERVE_SPREAD = 0.45  # log-scale spread of tolerated tau
SHARE_PROGRESSING = 0.23


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


def scenario(name: str, rate_sd: float, rng) -> None:
    tau0 = 0.15 * np.exp(rng.normal(0, 0.5, N))
    rate = rng.normal(RATE_MEAN, rate_sd, N)
    reserve = rng.normal(0, 1, N)

    def tau_at(t):
        return tau0 * np.exp(rate * t)

    margin = tau_at(HORIZON) / np.exp(RESERVE_SPREAD * reserve)
    stays_well = (margin < np.quantile(margin, 1 - SHARE_PROGRESSING)).astype(float)
    true_2y = (tau_at(2.0) - tau0) / 2
    true_4y = (tau_at(4.0) - tau0) / 4
    print(f"=== {name} spread of personal rates ===")
    print(f"True yearly change in scan signal: mean {true_2y.mean():.3f}, between-person SD")
    print(f"{true_2y.std():.3f} SUVR; {1 - stays_well.mean():.0%} progress in five years.\n")

    print("A. Is a personal rate measurable, and does it help predict who stays well?")
    print("   ('repeat' = a second scan straight away, which sharpens the level but carries no")
    print("   rate information: the fair comparison for a scan two years later)")
    print(f"   {'scan error':<12}{'rate reliability':>18}{'':>3}{'AUC':>5}")
    heads = f"{'2 years':>9}{'4 years':>9}{'':>3}{'level':>7}{'repeat':>8}"
    heads += f"{'+2y rate':>10}{'+4y rate':>10}"
    print(f"   {'(SUVR)':<12}{heads}")
    for sd in SCAN_SDS:
        level = 1 + tau0 + rng.normal(0, sd, N)
        again = 1 + tau0 + rng.normal(0, sd, N)
        r2 = (1 + tau_at(2.0) + rng.normal(0, sd, N) - level) / 2
        r4 = (1 + tau_at(4.0) + rng.normal(0, sd, N) - level) / 4
        rel2 = np.corrcoef(r2, true_2y)[0, 1] ** 2
        rel4 = np.corrcoef(r4, true_4y)[0, 1] ** 2
        feats = ([level], [level, again], [level, r2], [level, r4])
        aucs = [score(f, stays_well) for f in feats]
        cells = f"{aucs[0]:>7.3f}{aucs[1]:>8.3f}{aucs[2]:>10.3f}{aucs[3]:>10.3f}"
        print(f"   {sd:<12}{rel2:>9.2f}{rel4:>9.2f}{'':>3}{cells}")
    ceiling = score([1 + tau0, true_2y], stays_well)
    print(f"   level and rate both measured without error: AUC {ceiling:.3f}\n")

    sd = SCAN_SDS[1]
    level = 1 + tau0 + rng.normal(0, sd, N)
    r2 = (1 + tau_at(2.0) + rng.normal(0, sd, N) - level) / 2
    print(f"B. What a reserve marker adds (scan error {sd}). Validity = its correlation with the")
    print("   hidden reserve.")
    print(f"   {'validity':<12}{'level + marker':>16}{'level + marker + 2y rate':>28}")
    for validity in (0.0, 0.3, 0.5, 0.7, 1.0):
        marker = validity * reserve + np.sqrt(1 - validity**2) * rng.normal(0, 1, N)
        a, b = score([level, marker], stays_well), score([level, marker, r2], stays_well)
        print(f"   {validity:<12}{a:>16.3f}{b:>28.3f}")
    everything = score([1 + tau0, reserve, true_2y], stays_well)
    print(f"   everything known without error: AUC {everything:.3f}\n")


def main() -> None:
    rng = np.random.default_rng(0)
    for name, rate_sd in RATE_SPREADS.items():
        scenario(name, rate_sd, rng)
    print("Reading. (1) Much of what a second scan adds is a better fix on the LEVEL: compare")
    print("'repeat' with '+2y rate'. (2) If people differ little in their rate (LOW), a personal")
    print("rate adds almost nothing beyond that, even measured perfectly. If they differ a lot")
    print("(HIGH), it adds about 0.05-0.07 AUC, and four years between scans beats two.")
    print("(3) A reserve marker adds about 0.03-0.04 at validity 0.5 and about 0.07 at 0.7, in")
    print("either scenario, on top of whatever the scans give. Assumed parameters; the ordering")
    print("and the LOW-versus-HIGH contrast are the result, not the third decimal.")


if __name__ == "__main__":
    main()
