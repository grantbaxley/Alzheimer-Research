"""Ecological regime-shift illustration for the night of 2026-10-24 (trial-design lens,
brain-as-ecosystem constraint).

Night 2026-10-22 found the repo's tau-spreading model (FKPP + clearance) is NOT bistable:
restoring clearance always reverses it, because the logistic term is zero at saturation. That
raised the question of what feedback structure WOULD make "a point of no return" real. Ecology's
answer is alternative stable states: a system with strong positive feedback can sit in either a
healthy or a degraded basin, and flipping back requires pushing the driver past a LOWER threshold
than the one that caused the flip (hysteresis).

Here is the simplest such model - one homeostatic state variable h in [0,1] (think: fraction of the
local glia/neuron community in a healthy, homeostatic configuration) under a stress driver s, with
a positive-feedback recovery term:

    dh/dt = r * h * (1 - h)        # homeostasis reinforces itself (healthy state is "sticky")
            - s                     # stress pushes the community out of homeostasis
            + b                     # a small baseline restorative drive

This is a fold/saddle-node system: for intermediate s there are two stable states. We sweep s UP
(stress rising) and then DOWN (an intervention lowering stress) and look for hysteresis: the s at
which the system collapses on the way up differs from the s at which it recovers on the way down.

The trial-design message, IF the brain behaves like this: an intervention strong enough to STOP
progression (hold the system where it is) is not strong enough to REVERSE it - you must push the
driver past the lower recovery threshold. That gap is a quantity a trial could, in principle, aim
to measure. This is a concept illustration on a toy equation, NOT a disease model and NOT evidence
that the brain has alternative stable states.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

R = 1.0
B = 0.10


def equilibrium_h(s: float, h_start: float) -> float:
    def rhs(_t, h):
        hh = float(np.clip(h[0], 0.0, 1.0))
        return [R * hh * (1 - hh) - s + B]

    sol = solve_ivp(rhs, (0.0, 400.0), [h_start], method="LSODA", rtol=1e-8, atol=1e-10)
    return float(np.clip(sol.y[0, -1], 0.0, 1.0))


def sweep(s_values, h_start):
    h = h_start
    out = []
    for s in s_values:
        h = equilibrium_h(s, h)  # start from where the last step left us (path dependence)
        out.append(h)
    return out


def main() -> None:
    up = np.round(np.arange(0.00, 0.401, 0.02), 3)
    down = up[::-1]

    h_up = sweep(up, h_start=0.95)  # start healthy, raise stress
    h_down = sweep(down, h_start=h_up[-1])  # from the collapsed state, lower stress back

    def collapse_point(svals, hvals):
        for s, h in zip(svals, hvals, strict=True):
            if h < 0.2:
                return float(s)
        return None

    s_collapse = collapse_point(up, h_up)
    s_recover = collapse_point(down[::-1], h_down[::-1])  # scanning recovery low->high

    print(f"{'stress s':>9} {'h (up)':>8} {'h (down)':>9}")
    for s, hu, hd in zip(up, h_up, h_down[::-1], strict=True):
        print(f"{s:>9.2f} {hu:>8.2f} {hd:>9.2f}")

    print()
    if s_collapse is not None and s_recover is not None and s_collapse > s_recover + 1e-9:
        print(
            f"Hysteresis: the community collapses on the way UP at s~{s_collapse:.2f}, "
            f"but only recovers on the way DOWN once s falls to ~{s_recover:.2f}."
        )
        print(
            f"Trial-design reading: holding stress at {s_collapse:.2f} (enough to have caused "
            f"collapse) does NOT restore health; an intervention must drive the driver down to "
            f"~{s_recover:.2f} - a measurable gap between 'stop' and 'reverse'."
        )
    else:
        print("No hysteresis in this sweep (single stable state).")
    print("Concept illustration on a toy equation; not a disease model, not evidence.")


if __name__ == "__main__":
    main()
