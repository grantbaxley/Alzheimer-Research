"""Is astrocyte reactivity a GATE between amyloid and tau, or just a downstream MARKER?
(night of 2026-11-17, modeling lens, "start from a single cell type" constraint: the astrocyte).

A widely cited human finding is that amyloid associates with tau only in cognitively unimpaired
people whose blood GFAP (an astrocyte-reactivity marker) is elevated (Bellaver et al., Nat Med
2023, doi 10.1038/s41591-023-02380-x). The tempting reading is causal: reactive astrocytes GATE
the amyloid-to-tau step, so calming them would uncouple amyloid from tau. This toy asks whether
that stratified pattern can tell a gate from a marker at all.

Two synthetic worlds with the same average amyloid-to-tau effect (tau responds to amyloid only
above a threshold, as in the real disease):
    GATE    astrocyte reactivity truly multiplies the amyloid-to-tau effect; GFAP measures it.
    MARKER  no gating at all; GFAP simply RISES IN RESPONSE to amyloid and tau.

Analyses a study could run, each scored by how often it "finds a gate" (p < 0.05 in the
gating direction) across simulated cohorts:
    T1  stratified: amyloid-tau correlation significant in GFAP-high, not in GFAP-low
    T1b stratified: correlation significantly STRONGER in GFAP-high (added after T1 proved
        uninformative at this sample size - with ~530 people even a weak link is significant)
    T2  cross-sectional interaction: tau ~ amyloid + GFAP + amyloid x GFAP
    T3  the same, but allowing amyloid's own effect to be non-linear (threshold term)
    T4  longitudinal: does baseline GFAP x amyloid predict LATER tau change, given baseline tau?
A useful test finds the gate in the GATE world and stays quiet in the MARKER world.

Synthetic data only; assumed effect sizes; says nothing about real astrocytes or any person.
"""

from __future__ import annotations

import numpy as np
from scipy import stats

N, REPS, THR = 800, 400, 1.0


def ols_t(x_cols, y):
    """t statistic and two-sided p for the LAST column of the design (intercept added)."""
    x = np.column_stack([np.ones(len(y)), *x_cols])
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    resid = y - x @ beta
    dof = len(y) - x.shape[1]
    cov = resid @ resid / dof * np.linalg.inv(x.T @ x)
    t = beta[-1] / np.sqrt(cov[-1, -1])
    return t, 2 * stats.t.sf(abs(t), dof)


def cohort(rng, world):
    pos = rng.random(N) < 0.35
    a = np.where(pos, rng.normal(2.0, 0.8, N), rng.normal(0.0, 0.3, N))  # amyloid burden
    drive = np.clip(a - THR, 0, None)  # tau responds only above an amyloid threshold
    if world == "GATE":
        g = 0.4 * (a - a.mean()) / a.std() + rng.normal(0, 1, N)  # astrocyte reactivity
        gate = 2 / (1 + np.exp(-2 * g))  # multiplies the effect; averages about 1
        tau0 = 0.6 * drive * gate + rng.normal(0, 0.5, N)
        gfap = g + rng.normal(0, 0.5, N)
    else:
        gate = np.ones(N)
        tau0 = 0.6 * drive + rng.normal(0, 0.5, N)
        gfap = 0.5 * a + 0.6 * tau0 + rng.normal(0, 1, N)  # GFAP responds to amyloid and tau
    dtau = 0.3 * drive * gate + 0.1 * tau0 + rng.normal(0, 0.3, N)  # later tau change
    return a, tau0, gfap, dtau, drive


def tests(rng, world):
    a, tau0, gfap, dtau, drive = cohort(rng, world)
    z = (gfap - gfap.mean()) / gfap.std()
    hi = gfap > np.quantile(gfap, 2 / 3)
    r_hi, p_hi = stats.pearsonr(a[hi], tau0[hi])
    r_lo, p_lo = stats.pearsonr(a[~hi], tau0[~hi])
    t1 = (p_hi < 0.05 and r_hi > 0) and not (p_lo < 0.05 and r_lo > 0)
    zdiff = (np.arctanh(r_hi) - np.arctanh(r_lo)) / np.sqrt(
        1 / (hi.sum() - 3) + 1 / ((~hi).sum() - 3)
    )
    t1b = zdiff > stats.norm.ppf(0.975)  # correlation significantly stronger in GFAP-high
    t, p = ols_t([a, z, a * z], tau0)
    t2 = p < 0.05 and t > 0
    t, p = ols_t([a, drive, z, a * z], tau0)
    t3 = p < 0.05 and t > 0
    t, p = ols_t([a, drive, tau0, z, a * z], dtau)
    t4 = p < 0.05 and t > 0
    return t1, t1b, t2, t3, t4, r_hi, r_lo


def main() -> None:
    rng = np.random.default_rng(0)
    print(f"{REPS} simulated cohorts of {N} people per world. Share of cohorts in which each")
    print("analysis 'finds a gate':\n")
    print("  analysis                                        GATE world   MARKER world")
    out = {}
    for world in ("GATE", "MARKER"):
        res = np.array([tests(rng, world) for _ in range(REPS)])
        out[world] = res
    names = (
        "T1 stratified (GFAP-high yes, GFAP-low no)",
        "T1b correlation stronger in GFAP-high",
        "T2 cross-sectional interaction",
        "T3 interaction, amyloid allowed non-linear",
        "T4 longitudinal interaction (later tau change)",
    )
    for i, name in enumerate(names):
        print(f"  {name:<46} {out['GATE'][:, i].mean():>8.2f} {out['MARKER'][:, i].mean():>13.2f}")
    print("\n  mean amyloid-tau correlation, GFAP-high vs GFAP-low:")
    for world in ("GATE", "MARKER"):
        print(f"    {world:<7} {out[world][:, 5].mean():.2f} vs {out[world][:, 6].mean():.2f}")
    print("\nReading: compare the two columns. An analysis that fires in BOTH worlds cannot tell a")
    print("gate from a marker; one that fires only in the GATE world can. Synthetic data with")
    print("assumed effect sizes - this shows what each analysis can and cannot distinguish, not")
    print("which world is the real one.")


if __name__ == "__main__":
    main()
