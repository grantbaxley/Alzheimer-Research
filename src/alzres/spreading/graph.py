"""Connectome utilities: Laplacians and a synthetic connectome for tests and demos."""

from __future__ import annotations

import numpy as np
from scipy.spatial.distance import cdist


def _check_adjacency(A) -> np.ndarray:
    A = np.asarray(A, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("adjacency must be a square matrix")
    if not np.allclose(A, A.T):
        raise ValueError("adjacency must be symmetric (undirected connectome)")
    if (A < 0).any():
        raise ValueError("adjacency weights must be non-negative")
    return A


def graph_laplacian(A, normalized: bool = True) -> np.ndarray:
    """Graph Laplacian of a weighted undirected connectome.

    normalized=True gives L = I - D^-1/2 A D^-1/2, the form used for the
    network diffusion model (Raj et al., Neuron 2012). Isolated regions get a
    zero row and column, so nothing spreads into or out of them.
    """
    A = _check_adjacency(A).copy()
    np.fill_diagonal(A, 0.0)
    degree = A.sum(axis=1)
    if not normalized:
        return np.diag(degree) - A
    inv_sqrt = np.zeros_like(degree)
    nz = degree > 0
    inv_sqrt[nz] = 1.0 / np.sqrt(degree[nz])
    L = -(inv_sqrt[:, None] * A * inv_sqrt[None, :])
    L[np.diag_indices_from(L)] = nz.astype(float)
    return L


def synthetic_connectome(
    n_regions: int = 60,
    k_neighbors: int = 5,
    n_long_range: int = 40,
    length_scale: float = 0.3,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Random spatial connectome: k-nearest-neighbour edges plus long-range edges.

    Returns (A, coords). Long-range edges make network spread distinguishable
    from purely spatial spread, as in real connectomes. This is a test
    fixture, not a model of any real brain.
    """
    rng = np.random.default_rng(seed)
    coords = rng.uniform(0.0, 1.0, size=(n_regions, 3))
    d = cdist(coords, coords)
    A = np.zeros((n_regions, n_regions))
    nearest = np.argsort(d, axis=1)[:, 1 : k_neighbors + 1]
    for i in range(n_regions):
        for j in nearest[i]:
            A[i, j] = A[j, i] = np.exp(-d[i, j] / length_scale)
    added = 0
    while added < n_long_range:
        i, j = rng.integers(0, n_regions, size=2)
        if i != j and A[i, j] == 0:
            A[i, j] = A[j, i] = rng.uniform(0.5, 1.0)
            added += 1
    return A, coords
