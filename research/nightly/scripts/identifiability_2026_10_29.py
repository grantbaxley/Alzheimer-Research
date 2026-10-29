"""Can the tau "growth rate" be recovered, or does pure diffusion fit the same data equally well?
(night of 2026-10-29, earliest-signal lens; revisits idea identify-autocatalysis-rate.)

The repo's FKPP model assumes tau grows autocatalytically: dx/dt = -rho*L*x + alpha*x*(1-x).
Idea identify-autocatalysis-rate asks whether that growth rate alpha is identifiable from a few
human-like tau-PET timepoints, or whether a model with NO self-amplification fits the same data
equally well (so a good fit would not prove autocatalytic spread).

The RIGHT comparison is NESTED and network-aware: FKPP with alpha=0 is pure network diffusion, so
the honest test is whether allowing alpha>0 improves the fit beyond the alpha=0 (diffusion-only)
restriction on the SAME connectome. (An earlier draft of this script used a null with no network
term at all - a strawman the growth model trivially beat; that told us nothing. This version fixes
that: both models carry the network; they differ only in the growth term.)

Procedure on SYNTHETIC data with a known answer:
  1. Generate FKPP trajectories (known alpha_true>0, rho_true) on a synthetic connectome, sampled
     at a few noisy timepoints.
  2. Fit the FULL model (free rho, free alpha) and the NESTED NULL (free rho, alpha=0).
  3. If the diffusion-only null fits about as well as the full model, the growth term is NOT
     identifiable from this sampling.

Synthetic ground truth, so this tests identifiability of the METHOD, not anything about real tau.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize, minimize_scalar

from alzres.spreading import fkpp, synthetic_connectome

SEED = 20261029
rng = np.random.default_rng(SEED)


def gen(A, x0, t_eval, alpha, rho, noise):
    x = fkpp(A, x0, t_eval, rho=rho, alpha=alpha)
    return np.clip(x + rng.normal(0, noise, size=x.shape), 0, 1)


def sse_full(A, x0, t_eval, obs):
    def f(params):
        rho, alpha = params
        if rho < 0 or alpha < 0:
            return 1e6
        return float(((fkpp(A, x0, t_eval, rho=rho, alpha=alpha) - obs) ** 2).sum())

    r = minimize(f, x0=[1.0, 1.0], method="Nelder-Mead")
    return r.fun, r.x


def sse_diffusion_only(A, x0, t_eval, obs):
    def f(rho):
        return float(((fkpp(A, x0, t_eval, rho=max(rho, 0.0), alpha=0.0) - obs) ** 2).sum())

    r = minimize_scalar(f, bounds=(0.0, 5.0), method="bounded")
    return r.fun, r.x


def main() -> None:
    A, _ = synthetic_connectome(n_regions=40, seed=SEED)
    n = A.shape[0]
    x0 = np.zeros(n)
    x0[0] = 0.05
    alpha_true, rho_true, noise = 1.2, 1.0, 0.02

    for n_times, label in ((3, "sparse (3 scans, human-like)"), (12, "dense (12 scans)")):
        t_eval = np.linspace(0.5, 6.0, n_times)
        obs = gen(A, x0, t_eval, alpha_true, rho_true, noise)
        s_full, (rho_hat, alpha_hat) = sse_full(A, x0, t_eval, obs)
        s_null, rho_null = sse_diffusion_only(A, x0, t_eval, obs)
        rmse_full = (s_full / obs.size) ** 0.5
        rmse_null = (s_null / obs.size) ** 0.5
        print(f"{label}:")
        print(f"  true (rho, alpha) = ({rho_true}, {alpha_true})")
        print(f"  full fit: rho_hat={rho_hat:.2f} alpha_hat={alpha_hat:.2f}  RMSE={rmse_full:.4f}")
        print(f"  diffusion-only null (alpha=0): rho={rho_null:.2f}  RMSE={rmse_null:.4f}")
        ratio = rmse_null / max(rmse_full, 1e-9)
        verdict = (
            "diffusion-only fits ~as well -> GROWTH NOT identifiable here"
            if ratio <= 1.5
            else f"growth term improves fit {ratio:.1f}x -> identifiable"
        )
        print(f"  -> {verdict}\n")

    print(
        "Reading: this nested test asks whether the autocatalytic growth term earns its keep over\n"
        "pure diffusion on the same network. Where it does not, a good spatial fit does not prove\n"
        "self-amplifying spread. Synthetic test of the method; not a result about real tau."
    )


if __name__ == "__main__":
    main()
