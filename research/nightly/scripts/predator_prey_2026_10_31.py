"""Microglia-amyloid predator-prey model with peripheral-immune reinforcement, plus a
sensitivity sweep (night of 2026-10-31, modeling lens, peripheral-immune constraint;
builds idea microglia-plaque-predator-prey and connects to vaccine-trained-immunity).

Idea microglia-plaque-predator-prey proposed a population model where microglia clear amyloid
like predators eating prey, but the predator DEGRADES as it feeds (chronic activation -> exhausted
/ dysfunctional state). Tonight's peripheral-immune constraint adds a third element: recruited
peripheral myeloid cells can REINFORCE clearance (the mechanism trained-immunity / GM-CSF ideas
invoke). We write the minimal such model and ask the modeling-lens questions: what regimes exist,
and how sensitive is the outcome to the parameters the data do not pin down?

Model (one well-mixed region; dimensionless):
    dP/dt = g P (1 - P)            amyloid grows logistically (prey)
            - a M P / (1 + h P)    cleared by active microglia, saturating (Holling type II)
    dM/dt = b a M P / (1 + h P)    microglia expand on clearance (predator growth)
            - d M                   baseline turnover
            - q M * M              self-limitation / EXHAUSTION (chronic activation is costly)
            + r                     peripheral-immune reinforcement (recruited myeloid influx)

The clinically unidentified knobs are a (clearance efficiency), q (exhaustion strength) and r
(peripheral reinforcement). We report the final amyloid burden over a grid of these, label the
regime (cleared / high plaque), and summarise sensitivity. This is a toy ecological ODE, not a
calibrated disease model: it shows what the equation structure implies, not what a brain does.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

G, B, D, H = 1.0, 0.8, 0.2, 2.0
T_MAX = 400.0


def final_burden(a: float, q: float, r: float) -> float:
    def rhs(_t, y):
        p, m = max(y[0], 0.0), max(y[1], 0.0)
        clear = a * m * p / (1 + H * p)
        dp = G * p * (1 - p) - clear
        dm = B * clear - D * m - q * m * m + r
        return [dp, dm]

    sol = solve_ivp(rhs, (0, T_MAX), [0.05, 0.05], method="LSODA", rtol=1e-8, atol=1e-10)
    return float(np.clip(sol.y[0, -1], 0.0, 1.0))


def main() -> None:
    a_vals = [0.6, 1.0, 1.5, 2.0]
    q_vals = [0.0, 0.1, 0.3]
    r_vals = [0.0, 0.05, 0.15]

    print("Final amyloid burden P (0 = cleared, ~1 = saturated) over the unidentified knobs.")
    print("a = clearance efficiency, q = microglial exhaustion, r = peripheral reinforcement.\n")
    for r in r_vals:
        print(f"peripheral reinforcement r = {r}")
        print("  q/a :" + "".join(f"{a:>8}" for a in a_vals))
        for q in q_vals:
            row = "".join(f"{final_burden(a, q, r):>8.2f}" for a in a_vals)
            print(f"  {q:>6}" + row)
        print()

    # crude sensitivity: how much does final burden move per unit change in each knob,
    # averaged over the grid (one-at-a-time around a middle point)?
    base = (1.0, 0.1, 0.05)
    b0 = final_burden(*base)
    da = final_burden(1.5, 0.1, 0.05) - final_burden(0.6, 0.1, 0.05)
    dq = final_burden(1.0, 0.3, 0.05) - final_burden(1.0, 0.0, 0.05)
    dr = final_burden(1.0, 0.1, 0.15) - final_burden(1.0, 0.1, 0.0)
    print(f"Around base {base} (burden {b0:.2f}), burden change across each knob's range:")
    print(f"  clearance a (0.6->1.5):      {da:+.2f}")
    print(f"  exhaustion q (0.0->0.3):     {dq:+.2f}")
    print(f"  peripheral r (0.0->0.15):    {dr:+.2f}")
    print(
        "\nReading: the outcome is a threshold, not a dial - raising clearance a or peripheral\n"
        "reinforcement r can flip the system from saturated to cleared, while microglial\n"
        "exhaustion q pushes the other way, so peripheral reinforcement and exhaustion act as\n"
        "opposing forces on the same boundary. The exact flip point depends on parameters the\n"
        "data do not identify, so the model gives a QUALITATIVE prediction (a reinforcement\n"
        "threshold exists) and a falsification (no threshold, or clearance that cannot be rescued\n"
        "by added peripheral influx, would break it), not a number to trust. Toy ODE, not a brain."
    )


if __name__ == "__main__":
    main()
