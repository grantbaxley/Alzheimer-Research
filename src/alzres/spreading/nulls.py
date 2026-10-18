"""Null models every spreading-model result must be reported against.

A connectome model only means something if it beats (1) the same model on
degree-preserving rewired graphs and (2) purely spatial (Euclidean distance)
spread. In amyloid mouse models the network model was "not necessarily better
than a model of spatial spread" (PMC6331437), and results depend on which
connectome is used (PMC11211996).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.spatial.distance import cdist

from .models import fit_diffusion_time


def rewire_preserving_degree(A, swaps_per_edge: int = 10, seed: int | None = None) -> np.ndarray:
    """Maslov-Sneppen double-edge swaps; preserves each region's binary degree.

    Edge weights travel with their edges, so the weight distribution is kept
    but region strengths are only approximately preserved.
    """
    A = np.asarray(A, dtype=float)
    rng = np.random.default_rng(seed)
    iu, ju = np.nonzero(np.triu(A, k=1))
    edges = np.column_stack([iu, ju])
    weights = A[iu, ju].copy()
    m = len(edges)
    if m < 2:
        return A.copy()
    present = {(int(a), int(b)) for a, b in edges}
    present |= {(b, a) for a, b in present}
    for _ in range(swaps_per_edge * m):
        e1, e2 = rng.choice(m, size=2, replace=False)
        a, b = (int(v) for v in edges[e1])
        c, d = (int(v) for v in edges[e2])
        if rng.random() < 0.5:
            c, d = d, c
        if len({a, b, c, d}) < 4 or (a, d) in present or (c, b) in present:
            continue
        for p in ((a, b), (c, d)):
            present.discard(p)
            present.discard(p[::-1])
        for p in ((a, d), (c, b)):
            present.add(p)
            present.add(p[::-1])
        edges[e1] = (a, d)
        edges[e2] = (c, b)
    R = np.zeros_like(A)
    R[edges[:, 0], edges[:, 1]] = weights
    R[edges[:, 1], edges[:, 0]] = weights
    return R


def distance_null(coords, total_weight: float, length_scale: float = 0.2) -> np.ndarray:
    """Fully connected graph, weights exp(-distance / length_scale), rescaled to total_weight."""
    d = cdist(np.asarray(coords, dtype=float), np.asarray(coords, dtype=float))
    W = np.exp(-d / length_scale)
    np.fill_diagonal(W, 0.0)
    return W * (total_weight / W.sum())


@dataclass
class NullTestResult:
    r_observed: float
    r_rewired: np.ndarray
    p_rewired: float
    r_distance: float | None

    def beats_nulls(self, alpha: float = 0.05) -> bool:
        """True only if the connectome beats rewired nulls and (if given) the distance null."""
        ok = self.p_rewired < alpha
        if self.r_distance is not None:
            ok = ok and self.r_observed > self.r_distance
        return bool(ok)


def null_test(
    A,
    x0,
    target,
    coords=None,
    n_null: int = 100,
    t_grid=None,
    seed: int | None = None,
) -> NullTestResult:
    """Compare the NDM fit on the real connectome against rewired and spatial nulls.

    The p-value is the fraction of rewired graphs fitting at least as well,
    with the +1 correction so it is never exactly zero.
    """
    A = np.asarray(A, dtype=float)
    rng = np.random.default_rng(seed)
    _, r_obs, _ = fit_diffusion_time(A, x0, target, t_grid)
    r_null = np.array(
        [
            fit_diffusion_time(
                rewire_preserving_degree(A, seed=int(rng.integers(2**31))), x0, target, t_grid
            )[1]
            for _ in range(n_null)
        ]
    )
    p = (1 + np.sum(r_null >= r_obs)) / (n_null + 1)
    r_dist = None
    if coords is not None:
        D = distance_null(coords, total_weight=np.triu(A, 1).sum() * 2)
        r_dist = fit_diffusion_time(D, x0, target, t_grid)[1]
    return NullTestResult(r_observed=r_obs, r_rewired=r_null, p_rewired=float(p), r_distance=r_dist)
