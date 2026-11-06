"""Can an at-home readout detect within-person cognitive IMPROVEMENT over 6-12 months? (night of
2026-11-06, red-team lens, "only things measurable at home" constraint). A detectability toy for
the catalogue idea improvement-endpoint-validation, built around tonight's central red-team threat:
the practice (retest) effect both MIMICS improvement and, by its attenuation, is itself an AD
signal - so the ruler should measure normalization of the practice-learning curve, not raw change.

Two questions, both dimensionless and in units of the between-person SD:

(1) RELIABILITY x SAMPLING. A single home test has session reliability ICC; averaging k independent
    "burst" measures (the M2C2 design) cuts measurement-noise SD by sqrt(k), raising effective
    reliability. With measurement noise sigma = sqrt((1-ICC)/ICC), the smallest within-person change
    detectable between two visits (reliable-change index, p<0.05) is
        MDC = 1.96 * sqrt(2) * sigma / sqrt(k)   (in SD units).
    A plausible treatment gain is ~0.2 SD, and naive retest can fake ~0.2 SD, so the ruler must
    resolve well below 0.2 SD. We show which (ICC, k) clear that bar.

(2) PRACTICE-EFFECT BIAS. Scores follow baseline + a saturating practice curve + a (possibly zero)
    true gain after an onset + noise. The naive endpoint-minus-baseline estimate is biased UP by the
    practice gain (a false "improvement" under a true null). Fitting the practice curve to the
    pre-onset samples and subtracting it removes the bias - but only if you have enough early
    repeated measures to estimate the curve (another reason dense AT-HOME sampling matters), and
    only if the curve's shape is modelled correctly.

Not calibrated to any person, measure, or drug; a structural illustration of what at-home sampling
can and cannot buy.
"""

from __future__ import annotations

import numpy as np

PRACTICE_AMP = 0.30  # size of the saturating retest gain, SD units
TAU_P = 0.30  # practice saturates over ~this fraction of the observation window
ONSET = 0.5  # treatment turns on halfway through


def sigma_of(icc: float) -> float:
    return float(np.sqrt((1 - icc) / icc))


def min_detectable_change(icc: float, k: int) -> float:
    return 1.96 * np.sqrt(2) * sigma_of(icc) / np.sqrt(k)


def simulate(
    true_gain: float, icc: float, k: int, n_time: int, rng
) -> tuple[np.ndarray, np.ndarray]:
    t = np.linspace(0.0, 1.0, n_time)
    practice = PRACTICE_AMP * (1 - np.exp(-t / TAU_P))
    gain = true_gain * (t >= ONSET)
    truth = practice + gain
    noise = rng.normal(0.0, sigma_of(icc) / np.sqrt(k), size=n_time)
    return t, truth + noise


def fit_practice_then_residual(t, y, true_gain_known_onset=ONSET):
    """Estimate the gain as the post-onset residual after fitting practice to pre-onset points."""
    pre = t < true_gain_known_onset
    # fit amp*(1-exp(-t/tau)) to pre-onset points over a small tau grid (shape assumed known)
    best = None
    for tau in np.linspace(0.1, 0.8, 36):
        basis = 1 - np.exp(-t[pre] / tau)
        amp = float(np.dot(basis, y[pre]) / np.dot(basis, basis))
        resid = y[pre] - amp * basis
        sse = float(np.dot(resid, resid))
        if best is None or sse < best[0]:
            best = (sse, amp, tau)
    _, amp, tau = best
    projected = amp * (1 - np.exp(-t / tau))
    post = t >= true_gain_known_onset
    return float(np.mean(y[post] - projected[post]))


def main() -> None:
    rng = np.random.default_rng(0)

    print("(1) Smallest within-person change detectable (SD units); treatment ~0.2 SD is the bar.")
    print("    ICC is per-session reliability; k = number of averaged at-home burst measures.")
    print("      ICC    k=1     k=4     k=16    k=64")
    for icc in (0.6, 0.75, 0.9):
        row = "  ".join(f"{min_detectable_change(icc, k):6.2f}" for k in (1, 4, 16, 64))
        flag = "" if min_detectable_change(icc, 64) < 0.2 else "  (never < 0.2 here)"
        print(f"      {icc:.2f}  {row}{flag}")
    print("    -> only high session reliability (~0.9, e.g. M2C2 burst aggregates) AND dense")
    print(
        "       sampling (large k) push the detectable gain below the 0.2 SD practice-mimic floor."
    )
    print("")

    print("(2) Practice-effect bias: naive endpoint-minus-baseline vs practice-curve-deviation.")
    print("    1000 simulated people, ICC=0.9, k=16, 24 at-home timepoints.")
    for label, true_gain in (("TRUE NULL (gain=0.0)", 0.0), ("TRUE GAIN (gain=0.3)", 0.3)):
        naive, model = [], []
        for _ in range(1000):
            t, y = simulate(true_gain, icc=0.9, k=16, n_time=24, rng=rng)
            naive.append(float(np.mean(y[-3:]) - np.mean(y[:3])))
            model.append(fit_practice_then_residual(t, y))
        print(
            f"    {label}: naive Delta = {np.mean(naive):+.2f} (SD {np.std(naive):.2f}) | "
            f"practice-curve-deviation = {np.mean(model):+.2f} (SD {np.std(model):.2f})"
        )
    print(
        "    -> naive change reads a false ~+0.3 'improvement' under the TRUE NULL (it is just the"
    )
    print("       practice gain); modelling the practice curve and taking the post-onset residual")
    print(
        "       recovers ~0 under null and ~+0.3 under a real gain - but needs the dense pre-onset"
    )
    print("       samples to fit the curve, and assumes its shape is right.\n")

    print(
        "Reading: an at-home improvement ruler is feasible ONLY as (a) a high-reliability measure"
    )
    print("averaged over many burst sessions, scored as (b) deviation from each person's expected")
    print(
        "practice-learning curve - not raw endpoint-minus-baseline, which a retest effect fakes at"
    )
    print("~0.2 SD. Dense at-home sampling is the lever on both counts (reliability via averaging;")
    print(
        "curve estimability). Caveat: mis-specifying the practice curve reintroduces the bias, and"
    )
    print("this says nothing about whether any real measure's practice curve is this clean.")


if __name__ == "__main__":
    main()
