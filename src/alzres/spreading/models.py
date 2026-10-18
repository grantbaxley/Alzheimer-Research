"""Reference implementations of connectome spreading models, written from the equations.

Network diffusion model (NDM; Raj, Kuceyeski & Weiner, Neuron 2012):
    dx/dt = -beta * L x          =>  x(t) = expm(-beta L t) x0
Fisher-Kolmogorov / FKPP (e.g. Weickenmeier et al. 2019; Schafer et al. 2021):
    dx/dt = -rho * L x + alpha * x * (1 - x)

These are re-implementations, not ports of any group's code, so results can be
cross-checked against the published toolboxes (UCL network_spreading_models,
UCSF Nexis) during vetting.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

from .graph import graph_laplacian


def network_diffusion(A, x0, t, beta: float = 1.0, normalized: bool = True) -> np.ndarray:
    """Closed-form NDM solution.

    Args:
        A: (n, n) symmetric non-negative connectome.
        x0: (n,) initial pathology (e.g. 1 at the seed region).
        t: scalar time or 1-D array of times.
    Returns:
        (n,) for scalar t, else (len(t), n).
    """
    L = graph_laplacian(A, normalized=normalized)
    evals, evecs = np.linalg.eigh(L)
    coeffs = evecs.T @ np.asarray(x0, dtype=float)
    ts = np.atleast_1d(np.asarray(t, dtype=float))
    out = np.exp(-beta * np.outer(ts, evals)) * coeffs[None, :] @ evecs.T
    return out[0] if np.ndim(t) == 0 else out


def fkpp(A, x0, t_eval, rho: float = 1.0, alpha: float = 1.0) -> np.ndarray:
    """Integrate the network FKPP model; returns (len(t_eval), n) with values in [0, 1].

    Uses the combinatorial Laplacian D - A. The symmetric normalized Laplacian
    does not map the all-ones vector to zero, so full saturation (x = 1) would
    not be a fixed point and concentrations could overshoot 1.
    """
    L = graph_laplacian(A, normalized=False)
    x0 = np.asarray(x0, dtype=float)
    if (x0 < 0).any() or (x0 > 1).any():
        raise ValueError("FKPP concentrations must start in [0, 1]")
    t_eval = np.asarray(t_eval, dtype=float)

    def rhs(_t, x):
        return -rho * (L @ x) + alpha * x * (1.0 - x)

    sol = solve_ivp(rhs, (0.0, float(t_eval.max())), x0, t_eval=t_eval, method="LSODA")
    if not sol.success:
        raise RuntimeError(f"FKPP integration failed: {sol.message}")
    return sol.y.T


def fit_diffusion_time(A, x0, target, t_grid=None, beta: float = 1.0):
    """Fit NDM diffusion time by maximising Pearson r with an observed regional pattern.

    Returns (t_best, r_best, prediction). Pearson r is scale-free, matching the
    usual practice of comparing NDM patterns to regional tau or atrophy maps.
    """
    if t_grid is None:
        t_grid = np.linspace(0.05, 20.0, 200)
    target = np.asarray(target, dtype=float)
    preds = network_diffusion(A, x0, np.asarray(t_grid), beta=beta)
    rs = np.array([_pearson(p, target) for p in preds])
    best = int(np.nanargmax(rs))
    return float(t_grid[best]), float(rs[best]), preds[best]


def _pearson(a: np.ndarray, b: np.ndarray) -> float:
    if np.std(a) == 0 or np.std(b) == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])
