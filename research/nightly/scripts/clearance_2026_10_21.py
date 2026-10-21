"""Clearance-threshold illustration for the night of 2026-10-21 (red-team lens,
blood-vessel / blood-brain-barrier constraint).

The vascular hypothesis is that failing perivascular/BBB clearance, not extra
seeding, lets pathology take off. The repo's FKPP model

    dx/dt = -rho * L @ x + alpha * x * (1 - x)

has no clearance term, so it cannot express that idea. Here we add a linear
clearance term -gamma * x (a crude stand-in for clearance capacity):

    dx/dt = -rho * L @ x + alpha * x * (1 - x) - gamma * x

At low burden the local dynamics are ~(alpha - gamma) * x, so a small seed
decays when gamma > alpha and grows when gamma < alpha. The question this script
asks is narrow: holding the seed fixed, is there a clearance threshold below
which the SAME seed goes from clearing to spreading? A yes shows only that the
extended equation behaves as its algebra predicts; it is not evidence that any
real brain works this way, and it says nothing about Alzheimer's disease.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

from alzres.spreading.graph import graph_laplacian, synthetic_connectome

SEED = 20261021
RHO = 1.0
ALPHA = 1.0
T_MAX = 40.0


def final_burden(A, x0, gamma: float) -> float:
    L = graph_laplacian(A, normalized=False)

    def rhs(_t, x):
        return -RHO * (L @ x) + ALPHA * x * (1.0 - x) - gamma * x

    sol = solve_ivp(rhs, (0.0, T_MAX), x0, method="LSODA", rtol=1e-7, atol=1e-9)
    if not sol.success:
        raise RuntimeError(sol.message)
    return float(np.clip(sol.y[:, -1], 0.0, 1.0).mean())


def main() -> None:
    A, _ = synthetic_connectome(n_regions=60, seed=SEED)
    x0 = np.zeros(A.shape[0])
    x0[0] = 0.05  # one fixed seed region, identical across all runs

    gammas = np.round(np.arange(0.6, 1.26, 0.1), 2)
    print(f"{'gamma':>6} {'mean final burden':>18}")
    rows = []
    for g in gammas:
        b = final_burden(A, x0, g)
        rows.append((float(g), b))
        print(f"{g:>6} {b:>18.3f}")

    spread = [g for g, b in rows if b > 0.10]
    clear = [g for g, b in rows if b <= 0.10]
    if spread and clear:
        thr = (max(spread), min(g for g, b in rows if g > max(spread)))
        print(
            f"\nSame seed: clears for gamma >= {min(clear):.2f}, spreads for "
            f"gamma <= {max(spread):.2f}; threshold between {thr[0]:.2f} and {thr[1]:.2f}."
        )
        print("The trigger here is clearance, not seeding (the seed never changed).")
    else:
        print("\nNo threshold in this gamma range.")
    print("Synthetic illustration of the extended equation only; not about the disease.")


if __name__ == "__main__":
    main()
