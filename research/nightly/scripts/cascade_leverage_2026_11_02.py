"""Which link in the causal chain is most leverageable? (night of 2026-11-02, causal-chain lens,
approved-drug constraint). A structural toy of amyloid -> tau -> neurodegeneration -> cognition,
to ask where blocking the chain most protects cognition - and to show how the answer flips with the
ONE number the data do not pin down: how much neurodegeneration is already irreversible at symptom
onset.

Linear-cascade toy (rates, dimensionless). Each node is driven by the one upstream of it; cognition
falls as neurodegeneration rises, with a share of neurodegeneration already "banked" (irreversible)
before treatment starts:

    A' = pA - kA*A                      amyloid (production pA, clearance kA)
    T' = gA*A - kT*T                    tau, driven by amyloid
    N' = gT*T                           neurodegeneration, driven by tau (monotone up = damage)
    cognition = 1 - (N_banked + N)      floored at 0

"Treat at link X" = cut the transmission INTO that node by 80% from t=treat onward:
  - block amyloid: raise kA (clear amyloid)
  - block A->T: cut gA (stop amyloid driving tau)
  - block T->N: cut gT (stop tau driving degeneration - the neuroprotection link)
We compare final cognition for each, at two assumptions about how much damage is already banked at
treatment. The point is not a number but the ORDERING and how it depends on the banked fraction.
Structural illustration; not calibrated to any patient or drug.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

PA, KA0, GA0, KT, GT0 = 1.0, 1.0, 1.0, 1.0, 0.035
TREAT = 5.0
T_END = 20.0


def run(block: str, n_banked: float) -> float:
    def rhs(t, y):
        a, tau, n = (max(v, 0.0) for v in y)
        on = t >= TREAT
        kA = KA0 * (5.0 if (on and block == "amyloid") else 1.0)
        gA = GA0 * (0.2 if (on and block == "A->T") else 1.0)
        gT = GT0 * (0.2 if (on and block == "T->N") else 1.0)
        return [PA - kA * a, gA * a - KT * tau, gT * tau]

    sol = solve_ivp(rhs, (0, T_END), [0.0, 0.0, 0.0], method="LSODA", rtol=1e-8, atol=1e-10)
    n_final = float(sol.y[2, -1])
    return float(np.clip(1 - (n_banked + n_final), 0.0, 1.0))


def main() -> None:
    for n_banked, label in ((0.1, "early (little damage banked)"), (0.5, "late (much banked)")):
        print(f"{label}: banked irreversible N = {n_banked}")
        rows = [(b, run(b, n_banked)) for b in ("none", "amyloid", "A->T", "T->N")]
        for b, cog in rows:
            print(f"    block {b:>8}: final cognition {cog:.2f}")
        best = max((r for r in rows if r[0] != "none"), key=lambda r: r[1])
        print(f"    -> most leverageable here: block {best[0]} (cognition {best[1]:.2f})\n")
    print("Reading: two honest results. (1) Which LINK you block barely matters here - blocking")
    print("T->N (closest to the damage) is only marginally best (~0.03 over clearing amyloid), and")
    print("all three beat no-treatment by a lot. (2) WHEN you start dominates: the same step")
    print("gives cognition ~0.66-0.69 started early vs ~0.26-0.29 started late, because banked")
    print("irreversible damage sets the ceiling. So in this toy, timing (the banked fraction) is a")
    print("far bigger lever than the choice of node - consistent with the recurring start-early")
    print("finding. Linear toy with assumed rates; not a claim about any drug or node.")


if __name__ == "__main__":
    main()
