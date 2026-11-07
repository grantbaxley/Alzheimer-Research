"""A vascular tipping point and its reversal window (night of 2026-11-07, inversion lens, "start
from blood vessels and the BBB" constraint). A minimal reduction of the published cerebrovascular
saddle-node model (Ahern, Thompson, Oliveri, Lorthois & Goriely, Proc. R. Soc. A 2025,
doi 10.1098/rspa.2024.0548), which formalises the two-hit vascular positive-feedback loop
(amyloid-beta -> pericyte constriction -> hypoperfusion -> more amyloid + worse clearance) and finds
an S-shaped bifurcation with hysteresis. The loop's first arm is empirically real in HUMAN tissue
(Nortley/Attwell 2019, Science, doi 10.1126/science.aav9518: amyloid-beta ~halves cortical CBF via
pericytes, reversibly). This toy asks what that structure implies for REVERSAL (the inversion lens):
if perfusion can collapse into a second stable state, how far must you unwind the driver to climb
back out?

Two variables (dimensionless, 0..1): P = perfusion (1 healthy), D = vascular/tissue damage.

    dP/dt = 1/(1+(D/Dc)^m) - P              perfusion relaxes to a D-dependent set-point
    dD/dt = s + kd/(1+(P/Pc)^n)*(1-D) - D    low P drives damage (Hill); repair rate 1

The control parameter s is a chronic vascular stressor / amyloid load that raises the damage rate
(maps to the model's basic reproduction number). kd is the strength of the hypoperfusion->damage
feedback.

Three results, all honest about what a toy can and cannot establish:
 (1) For STRONG feedback there is a bistable window in s (healthy and collapsed states coexist),
     bounded by two saddle-node bifurcations; for WEAK feedback the system is monostable and P just
     declines smoothly. Whether the brain sits in the bistable region is exactly what the model
     CANNOT decide - only an empirical test can (see the log's next-steps: amyloid-matched CBF
     bimodality; post-clearance CBF path-dependence).
 (2) Hysteresis: ramping s up collapses perfusion at the UPPER saddle-node; ramping s back down
     recovers it only at the LOWER saddle-node. The reversal window = you must push the driver BELOW
     the lower node, past where it collapsed - removing just the proximate trigger is not enough.
 (3) Even a full perfusion recovery is capped elsewhere: the durable floor in AD is neuron loss
     (~60% of entorhinal layer-II neurons gone by very-mild dementia, Gomez-Isla 1996, PMID
     8699259), so the vascular route still caps at "freeze" past that point - the toy bounds the
     vascular sub-problem only.

Structural illustration; assumed rates; not calibrated to any patient, and not evidence that human
vascular dynamics are in fact bistable.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

DC, M, PC, N = 0.4, 4.0, 0.45, 4.0


def d_steady(p: float, s: float, kd: float) -> float:
    h = kd / (1 + (p / PC) ** N)
    return (s + h) / (1 + h)


def perfusion_balance(p: float, s: float, kd: float) -> float:
    return 1 / (1 + (d_steady(p, s, kd) / DC) ** M) - p


def fixed_points(s: float, kd: float) -> list[float]:
    ps = np.linspace(1e-4, 1.0, 3000)
    fv = np.array([perfusion_balance(p, s, kd) for p in ps])
    roots = []
    for i in range(len(ps) - 1):
        if fv[i] * fv[i + 1] < 0:
            roots.append(brentq(perfusion_balance, ps[i], ps[i + 1], args=(s, kd)))
    return roots


def bistable_window(kd: float) -> tuple[float, float] | None:
    svals = np.linspace(0.0, 0.5, 501)
    bis = [s for s in svals if len(fixed_points(s, kd)) == 3]
    return (min(bis), max(bis)) if bis else None


def settle(s: float, kd: float, y0, t_end: float = 400.0) -> float:
    def rhs(t, y):
        p, d = max(y[0], 0.0), np.clip(y[1], 0.0, 1.0)
        return [1 / (1 + (d / DC) ** M) - p, s + kd / (1 + (p / PC) ** N) * (1 - d) - d]

    sol = solve_ivp(rhs, (0, t_end), y0, method="LSODA", rtol=1e-9, atol=1e-11)
    return float(sol.y[0, -1])


def main() -> None:
    print("(1) Does a vascular tipping point exist? Fixed-point count vs stressor s.")
    for kd, label in ((1.0, "strong feedback (kd=1.0)"), (0.3, "weak feedback (kd=0.3)")):
        win = bistable_window(kd)
        counts = {len(fixed_points(s, kd)) for s in np.linspace(0, 0.5, 51)}
        if win:
            print(
                f"    {label}: BISTABLE for s in [{win[0]:.2f}, {win[1]:.2f}] "
                f"(healthy + collapsed states coexist)"
            )
        else:
            print(
                f"    {label}: monostable throughout (max fixed points = {max(counts)}); "
                f"perfusion just declines"
            )
    print("    -> bistability needs strong-enough feedback; the model cannot say which regime a")
    print("       real brain is in - only an empirical test can.\n")

    kd = 1.0
    win = bistable_window(kd)
    print(
        f"(2) Hysteresis and the reversal window (strong feedback, bistable in s~[{win[0]:.2f},"
        f" {win[1]:.2f}])."
    )
    up = np.linspace(0.0, 0.4, 41)
    p = 1.0
    collapse_s = None
    for s in up:
        p = settle(s, kd, [p, d_steady(p, s, kd)])
        if collapse_s is None and p < 0.5:
            collapse_s = s
    p = 0.1
    recover_s = None
    for s in up[::-1]:
        p = settle(s, kd, [p, d_steady(p, s, kd)])
        if recover_s is None and p > 0.5:
            recover_s = s
    print(f"    ramp s UP from healthy: perfusion collapses near s = {collapse_s:.2f} (upper node)")
    print(
        f"    ramp s DOWN from collapsed: perfusion recovers only near s = {recover_s:.2f} "
        f"(lower node)"
    )
    gap = collapse_s - recover_s
    overcorr = collapse_s / recover_s
    print(f"    hysteresis gap = {gap:.2f}: reverse needs the driver below {recover_s:.2f},")
    print(f"    not just below the collapse {collapse_s:.2f} - over-correction ~{overcorr:.1f}x.")
    print("")

    print("Reading: IF the vascular feedback is strong enough to be bistable (unproven in humans),")
    print(
        "two things follow for reversal. (a) There is a latest point - the upper saddle-node - past"
    )
    print("which removing the driver no longer helps; and (b) climbing back out needs the driver")
    print(
        "pushed well below where it collapsed (the hysteresis gap), i.e. over-correction, not just"
    )
    print(
        "trigger removal. BUT whether the brain is in the bistable regime is exactly what this toy"
    )
    print(
        "cannot decide (weak feedback gives a smooth, fully reversible decline instead), and even a"
    )
    print(
        "full perfusion recovery is still capped by neuron loss (Gomez-Isla 1996). A reduction of"
    )
    print("Ahern 2025; assumed rates; not a measured basin and not a claim about any patient.")


if __name__ == "__main__":
    main()
