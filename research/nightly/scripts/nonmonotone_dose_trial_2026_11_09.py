"""Why a remyelination trial can miss a real effect: the inverted-U dose-response (night of
2026-11-09, trial-design lens, "start from the oligodendrocyte" constraint). Remyelination has a
mechanistically expected NON-MONOTONE dose-response - there is an optimal OPC-differentiation window
and over-drive is harmful - and the clearest human case is opicinumab (anti-LINGO-1): the SYNERGY MS
trial (Cadavid, Lancet Neurol 2019, PMID 31285147) saw its best signal at an INTERMEDIATE dose
(~10-30 mg/kg) with benefit falling off at the top dose, so the pre-specified LINEAR dose-trend test
was null (trend p ~ 0.89) and the trial missed; the follow-up (AFFINITY) then bet on a SINGLE fixed
dose - the wrong move if the true curve is a bell.

This toy simulates that structure and asks which trial design/analysis detects a real inverted-U
effect. Doses mirror SYNERGY {0, 3, 10, 30, 100}; the mean effect is a bell in log-dose peaking at
an interior dose. We compare, on the SAME simulated data:
  - two-arm, TOP dose vs placebo (the usual "go" arm - sits on the downslope)
  - monotone linear dose-trend (averages the up- and down-slopes toward zero)
  - omnibus one-way ANOVA across arms
  - orthogonal QUADRATIC contrast (captures curvature)
  - best active dose vs placebo with multiplicity correction (Bonferroni over the active arms)

Then an honest counter-case: when the drug is TRULY MONOTONE (peak at the top dose), the two-arm and
linear-trend tests match or beat the curvature-aware ones, i.e. the extra arms just cost power - the
non-monotone machinery is not magic, only matched to genuine non-monotonicity.

Synthetic illustration in units of the between-person SD; not calibrated to any drug or patient.
"""

from __future__ import annotations

import numpy as np
from scipy import stats

DOSES = np.array([0.0, 3.0, 10.0, 30.0, 100.0])
N_PER_ARM = 90
NOISE_SD = 1.0
EMAX = 0.3  # peak effect vs placebo, SD units
SW = 0.9  # bell width in log-dose
N_SIM = 2000


def mean_effect(d: np.ndarray, d_opt: float) -> np.ndarray:
    g = np.exp(-((np.log(d + 1) - np.log(d_opt + 1)) ** 2) / (2 * SW**2))
    g0 = np.exp(-((np.log(1) - np.log(d_opt + 1)) ** 2) / (2 * SW**2))
    return EMAX * (g - g0)


def one_trial(rng, d_opt: float):
    return {d: rng.normal(mean_effect(np.array([d]), d_opt)[0], NOISE_SD, N_PER_ARM) for d in DOSES}


def quadratic_contrast_p(arms) -> float:
    # orthogonal polynomial (quadratic) contrast across equally-indexed dose arms
    k = len(DOSES)
    idx = np.arange(k, dtype=float)
    quad = (idx - idx.mean()) ** 2
    quad = quad - quad.mean()  # orthogonal to the mean
    means = np.array([arms[d].mean() for d in DOSES])
    c = float(np.dot(quad, means))
    var = NOISE_SD**2 / N_PER_ARM * float(np.dot(quad, quad))
    z = c / np.sqrt(var)
    return 2 * (1 - stats.norm.cdf(abs(z)))


def power_table(d_opt: float, label: str) -> None:
    rng = np.random.default_rng(0)
    hits = dict(top=0, trend=0, anova=0, quad=0, bestbonf=0)
    for _ in range(N_SIM):
        arms = one_trial(rng, d_opt)
        pbo = arms[0.0]
        # top dose vs placebo
        p = stats.ttest_ind(arms[100.0], pbo).pvalue
        hits["top"] += p < 0.05 and arms[100.0].mean() > pbo.mean()
        # monotone linear trend on log-dose
        x = np.concatenate([[np.log(d + 1)] * N_PER_ARM for d in DOSES])
        y = np.concatenate([arms[d] for d in DOSES])
        lr = stats.linregress(x, y)
        hits["trend"] += lr.pvalue < 0.05 and lr.slope > 0
        # omnibus ANOVA
        hits["anova"] += stats.f_oneway(*[arms[d] for d in DOSES]).pvalue < 0.05
        # quadratic contrast
        hits["quad"] += quadratic_contrast_p(arms) < 0.05
        # best active dose vs placebo, Bonferroni over 4 active arms
        best = min(stats.ttest_ind(arms[d], pbo).pvalue for d in DOSES[1:])
        hits["bestbonf"] += best < 0.05 / 4
    print(f"  {label} (d_opt={d_opt:g}): power over {N_SIM} sims, n={N_PER_ARM}/arm")
    print(
        f"    two-arm top-vs-pbo {hits['top'] / N_SIM:.2f} | linear-trend "
        f"{hits['trend'] / N_SIM:.2f} | ANOVA {hits['anova'] / N_SIM:.2f} | "
        f"quadratic {hits['quad'] / N_SIM:.2f} | best-dose(Bonf) {hits['bestbonf'] / N_SIM:.2f}"
    )


def main() -> None:
    print("True effect by dose (SD units):")
    for d_opt, lab in ((10.0, "inverted-U, interior peak"), (100.0, "monotone, peak at top")):
        eff = {float(d): round(float(mean_effect(np.array([d]), d_opt)[0]), 2) for d in DOSES}
        print(f"  {lab}: {eff}")
    print()
    print("(1) Inverted-U drug (the opicinumab case):")
    power_table(10.0, "inverted-U")
    print("(2) Honest counter-case - a truly MONOTONE drug:")
    power_table(100.0, "monotone")
    print()
    print(
        "Reading: for an inverted-U remyelination drug, the two-arm TOP-dose test and the monotone"
    )
    print(
        "linear-trend test are near-powerless (the top dose is on the downslope; the trend averages"
    )
    print(
        "up- and down-slopes to ~zero - exactly SYNERGY's p~0.89), while the omnibus, the quadratic"
    )
    print("curvature contrast, and a best-dose-vs-placebo design with multiplicity recover it.")
    print(
        "The counter-case keeps it honest: when the drug is truly monotone, the simple tests match"
    )
    print(
        "or beat the curvature-aware ones, so multi-dose + non-monotonicity machinery is not free -"
    )
    print("it only pays when the biology is genuinely non-monotone, which for remyelination (an")
    print("optimal differentiation window) it is expected to be. Trial-design lesson: never make a")
    print(
        "two-arm or monotone-trend the primary for a remyelination agent, and never collapse to one"
    )
    print(
        "'top' dose after a bell-shaped phase 2 (AFFINITY's mistake). Synthetic; not a drug claim."
    )


if __name__ == "__main__":
    main()
