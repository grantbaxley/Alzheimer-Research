"""Does the TIMING of clearance matter, or only its average? (night of 2026-10-28,
combination-timing lens, sleep constraint, revisiting clearance-threshold-onset).

Sleep is the proposed physiological "high-clearance" window. The clearance-threshold model from
nights 3-4 used a constant clearance rate gamma. But sleep is intermittent: clearance is high
during sleep and low during wake. This script asks a narrow timing question: for the SAME
time-averaged clearance, does delivering it as a periodic square wave (sleep/wake) change whether
a seed is contained, versus delivering it constantly?

Model (one well-mixed region, to isolate timing from spread):
    dx/dt = alpha * x * (1 - x) - gamma(t) * x
  - constant:     gamma(t) = g_mean
  - intermittent: gamma(t) = g_hi for a fraction f of each 24h cycle (sleep), g_lo otherwise,
                  with f*g_hi + (1-f)*g_lo = g_mean  (same daily average)

Because the growth term alpha*x*(1-x) is concave in x, Jensen's inequality predicts the average
of the dynamics is not the dynamics of the average - so timing can matter even at equal mean. The
question is which way and how much. This is a property of the equation (a known nonlinear-averaging
effect), not evidence that sleep timing works this way in a brain. Synthetic illustration only.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

ALPHA = 1.0
PERIOD = 1.0  # one day
T_MAX = 60.0  # ~60 days


def final_burden(gamma_fn, x0=0.05):
    def rhs(t, x):
        xx = float(np.clip(x[0], 0.0, 1.0))
        return [ALPHA * xx * (1 - xx) - gamma_fn(t) * xx]

    sol = solve_ivp(rhs, (0.0, T_MAX), [x0], method="LSODA", rtol=1e-8, atol=1e-10, max_step=0.05)
    return float(np.clip(sol.y[0, -1], 0.0, 1.0))


def main() -> None:
    sleep_frac = 1.0 / 3.0  # ~8h of 24h is the high-clearance window
    print(
        f"alpha (growth) = {ALPHA}; sleep fraction = {sleep_frac:.2f}; equal daily mean each row.\n"
    )
    print(f"{'mean gamma':>11} {'constant':>10} {'intermittent':>13} {'timing effect':>14}")
    for g_mean in (0.90, 0.95, 1.00, 1.05, 1.10):
        g_hi = g_mean / sleep_frac  # all clearance concentrated into the sleep window, low=0
        phase = PERIOD * sleep_frac

        def gamma_const(_t, gm=g_mean):
            return gm

        def gamma_interm(t, ghi=g_hi, ph=phase):
            return ghi if (t % PERIOD) < ph else 0.0

        b_const = final_burden(gamma_const)
        b_interm = final_burden(gamma_interm)
        tag = (
            "worse"
            if b_interm > b_const + 1e-3
            else ("better" if b_interm < b_const - 1e-3 else "~same")
        )
        print(f"{g_mean:>11.2f} {b_const:>10.3f} {b_interm:>13.3f} {tag:>14}")

    print(
        "\nReading: at equal daily-average clearance, concentrating it into a short window (like\n"
        "sleep) with long low-clearance gaps changes the outcome - gaps let the seed regrow\n"
        "while awake, so timing, not just total clearance, affects containment. A nonlinear-\n"
        "averaging (Jensen) effect of the chosen equation, not evidence about sleep."
    )


if __name__ == "__main__":
    main()
