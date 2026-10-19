"""Illustrates the logic of idea `sex-amyloid-tau-window` (night 2026-10-19).

Human observation (JAMA Neurol 2025; J Prev Alzheimers Dis 2026): once amyloid is
present, tau accumulates and spreads faster in women, and the amyloid-to-tau
interval is shorter. The idea is that an anti-seeding therapy's useful window is
set by *time since the tau process started*, not by chronological age, and that
this window is compressed when the local tau-growth rate is higher.

This script does NOT use any human or sex-specific data. It asks a narrow
mechanistic question on a synthetic connectome: if the local tau-growth rate
(FKPP alpha) is higher, how much shorter is the window between tau first becoming
detectable in a seed region and tau becoming widespread? A synthetic result shows
only that the tooling behaves as expected; it says nothing about Alzheimer's
disease or about women.
"""

from __future__ import annotations

import numpy as np

from alzres.spreading import fkpp, synthetic_connectome

SEED = 20261019
DETECT = 0.10  # "detectable" tau fraction in the seed region
WIDESPREAD = 0.50  # tau is "widespread" when half the regions exceed DETECT


def first_time(series: np.ndarray, t: np.ndarray, threshold: float) -> float:
    hit = np.where(series >= threshold)[0]
    return float(t[hit[0]]) if hit.size else float("nan")


def window_for_alpha(A, x0, t, alpha: float) -> dict:
    x = fkpp(A, x0, t, rho=1.0, alpha=alpha)  # (len(t), n_regions)
    seed = x[:, 0]
    frac_regions = (x >= DETECT).mean(axis=1)
    t_detect = first_time(seed, t, DETECT)
    t_widespread = first_time(frac_regions, t, WIDESPREAD)
    return {
        "alpha": alpha,
        "t_detect_seed": round(t_detect, 3),
        "t_widespread": round(t_widespread, 3),
        "window": round(t_widespread - t_detect, 3),
    }


def main() -> None:
    A, _ = synthetic_connectome(n_regions=60, seed=SEED)
    n = A.shape[0]
    x0 = np.zeros(n)
    x0[0] = 0.02  # a single seed region, as in an entorhinal-onset picture
    t = np.linspace(0.0, 12.0, 600)

    rows = [window_for_alpha(A, x0, t, a) for a in (0.6, 1.0, 1.6)]
    print(f"{'alpha':>6} {'t_detect':>9} {'t_wide':>8} {'window':>7}")
    for r in rows:
        print(f"{r['alpha']:>6} {r['t_detect_seed']:>9} {r['t_widespread']:>8} {r['window']:>7}")

    base = next(r for r in rows if r["alpha"] == 1.0)["window"]
    fast = next(r for r in rows if r["alpha"] == 1.6)["window"]
    print(
        f"\nRaising local growth 1.0 -> 1.6 changes the detect->widespread window "
        f"from {base} to {fast} ({100 * (fast - base) / base:+.0f}%)."
    )
    print("Synthetic illustration only; not evidence about the disease or about women.")


if __name__ == "__main__":
    main()
