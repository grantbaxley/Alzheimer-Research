"""How much reversal is possible once symptoms have begun? (night of 2026-11-01, cross-domain
lens, symptomatic constraint). Borrows the hepatology principle - remove the driver and the
fibrosis/ECM regresses - and asks what it buys in a system that ALSO has an irreversible-damage
compartment.

Hepatology and cardiology reverse because the damaged tissue (fibrosis, plaque lipid) sits in a
REMODELLABLE compartment. AD's problem is that exposure to pathology also drives an IRREVERSIBLE
compartment (neuron loss), which has no liver-regeneration analog. This toy splits the two:

    dP/dt = s - c*P     reversible pathology load; s = production / the "driver"
    dD/dt = k*P         irreversible damage accrued from cumulative exposure (monotone up)
    f = 1 - (wP*P + wD*D)   a cognition-like function score, floored at 0

"Treat" = remove the driver at the symptomatic point (set s -> 0), the hepatology move. P then
decays (reversible), but D is frozen at whatever already accrued. The symptomatic constraint forces
the real question: starting treatment at mild vs later disease, what is the CEILING on recovered
function, set by the D already banked? A structural illustration of why "reverse it like the liver"
has a hard ceiling in AD; not calibrated to any patient. Synthetic illustration only.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

S, C, K = 1.0, 1.0, 0.15  # driver, clearance, damage-accrual rate
WP, WD = 0.5, 0.5  # weight of reversible load vs irreversible damage on function


def trajectory(treat_at: float, t_end: float = 60.0):
    def rhs(t, y):
        p = max(y[0], 0.0)
        s = 0.0 if t >= treat_at else S  # remove the driver at treat_at
        return [s - C * p, K * p]

    ts = np.linspace(0, t_end, 1200)
    sol = solve_ivp(rhs, (0, t_end), [0.0, 0.0], t_eval=ts, method="LSODA", rtol=1e-8, atol=1e-10)
    p, d = sol.y[0], sol.y[1]
    f = np.clip(1 - (WP * p + WD * d), 0.0, 1.0)
    return ts, p, d, f


def main() -> None:
    print("Remove the driver (the hepatology move) at different disease stages.")
    print(f"{'treat at t':>10} {'D banked':>9} {'f at Rx':>8} {'f final':>8} {'ceiling':>8}")
    for treat_at in (3.0, 6.0, 10.0, 20.0):
        ts, p, d, f = trajectory(treat_at=treat_at)
        i_rx = int(np.argmin(np.abs(ts - treat_at)))
        ceiling = 1 - WD * d[-1]  # best function once P is fully cleared (P->0)
        print(f"{treat_at:>10.1f} {d[i_rx]:>9.2f} {f[i_rx]:>8.2f} {f[-1]:>8.2f} {ceiling:>8.2f}")

    print()
    print("Reading: removing the driver always recovers the REVERSIBLE part (P decays, function")
    print("rebounds) - the hepatology win is real for that compartment. But the recovered ceiling")
    print("falls the later you start: the irreversible-damage compartment D keeps whatever it")
    print("banked. So 'reverse it like the liver' is partly true in AD, and the cross-domain")
    print("principle (remove the driver, start early) holds - but the symptomatic stage sets a")
    print("hard ceiling no clearance lifts - what the liver analogy lacks (the liver regenerates;")
    print("lost neurons do not). Structural toy, not calibrated to any patient.")


if __name__ == "__main__":
    main()
