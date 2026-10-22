"""Hysteresis test for `clearance-threshold-onset` (night of 2026-10-22, inversion lens,
engineering constraint).

Night 2026-10-21 added a clearance term to the FKPP spreading model:

    dx/dt = -rho * L @ x + alpha * x * (1 - x) - gamma * x

and found a sharp clearance threshold. The engineering question for reversal is whether
the system is BISTABLE: if clearance (gamma) drops below threshold, pathology establishes;
if clearance is then RESTORED, does burden fall back to baseline (reversible, no hysteresis)
or stay high (a self-sustaining high state that clearance alone cannot undo)?

Two experiments, one fixed seed throughout:

Experiment 1 (fixed clearance): drop gamma below threshold so pathology grows, then restore
gamma above threshold and see whether burden collapses back to the never-ill baseline.

Experiment 2 (clearance impaired BY pathology): the engineering reframing. Make effective
clearance fall as burden rises, gamma_eff = gamma_base - k * mean(x), a positive-feedback
failure loop (pathology clogs the very clearance that removes it). Then restore gamma_base and
test for hysteresis again.

The contrast is the point. Result: NEITHER experiment shows hysteresis. Restoring clearance
reverses the high state even when pathology strongly suppresses clearance, because the logistic
growth term alpha*x*(1-x) is zero at saturation, so any positive clearance drains it. The lesson
is that clearance/aggregation dynamics in this model family are reversible by construction; the
irreversibility of real disease, if it exists, must come from something this model lacks -
actual loss of substrate (neuron death), not the clearance-vs-aggregation balance. Both results
are properties of the chosen equations, not of any brain. Synthetic illustration only.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

from alzres.spreading.graph import graph_laplacian, synthetic_connectome

SEED = 20261022
RHO = 1.0
ALPHA = 1.0


def integrate(L, x0, gamma, t_span, feedback_k=0.0, n=200):
    """Integrate the model. feedback_k>0 makes clearance fall as mean burden rises."""

    def rhs(_t, x):
        gamma_eff = gamma - feedback_k * float(np.clip(x, 0, 1).mean())
        gamma_eff = max(gamma_eff, 0.0)
        return -RHO * (L @ x) + ALPHA * x * (1.0 - x) - gamma_eff * x

    t_eval = np.linspace(t_span[0], t_span[1], n)
    sol = solve_ivp(rhs, t_span, x0, t_eval=t_eval, method="LSODA", rtol=1e-7, atol=1e-9)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y[:, -1]


def main() -> None:
    A, _ = synthetic_connectome(n_regions=60, seed=SEED)
    L = graph_laplacian(A, normalized=False)
    n = A.shape[0]
    seed = np.zeros(n)
    seed[0] = 0.05

    gamma_low, gamma_high = 0.6, 1.1  # below and above last night's threshold (~0.8-0.9)

    def mean_burden(v):
        return float(np.clip(v, 0, 1).mean())

    def run(feedback_k):
        control = integrate(L, seed, gamma_high, (0.0, 60.0), feedback_k)
        established = integrate(L, seed, gamma_low, (0.0, 30.0), feedback_k)
        restored = integrate(L, established, gamma_high, (0.0, 60.0), feedback_k)
        return mean_burden(control), mean_burden(established), mean_burden(restored)

    print(f"Protocol: seed, drop to gamma={gamma_low}, restore to gamma={gamma_high}.\n")
    for label, k in (("Exp 1: fixed clearance", 0.0), ("Exp 2: pathology impairs clearance", 1.0)):
        b_control, b_est, b_restored = run(k)
        print(f"{label} (feedback_k={k}):")
        print(f"  never impaired (control):    {b_control:.3f}")
        print(f"  after low-clearance episode: {b_est:.3f}")
        print(f"  then clearance restored:     {b_restored:.3f}")
        if b_restored > b_control + 0.05:
            print(
                "  -> HYSTERESIS: restoring clearance does not undo it; high state self-sustains.\n"
            )
        else:
            print("  -> no hysteresis: restoring clearance reverses it.\n")
    print("Properties of the chosen equations, not evidence about the disease.")


if __name__ == "__main__":
    main()
