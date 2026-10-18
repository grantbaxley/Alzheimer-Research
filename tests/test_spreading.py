import numpy as np
import pytest
from scipy.linalg import expm

from alzres.spreading import (
    fit_diffusion_time,
    fkpp,
    graph_laplacian,
    network_diffusion,
    null_test,
    rewire_preserving_degree,
    synthetic_connectome,
)


@pytest.fixture(scope="module")
def connectome():
    return synthetic_connectome(n_regions=40, seed=0)


def test_laplacian_properties(connectome):
    A, _ = connectome
    L = graph_laplacian(A)
    np.testing.assert_allclose(L, L.T)
    evals = np.linalg.eigvalsh(L)
    assert evals.min() > -1e-10 and evals.max() < 2 + 1e-10


def test_ndm_matches_matrix_exponential(connectome):
    A, _ = connectome
    x0 = np.zeros(len(A))
    x0[3] = 1.0
    L = graph_laplacian(A)
    np.testing.assert_allclose(network_diffusion(A, x0, 2.5), expm(-2.5 * L) @ x0, atol=1e-10)


def test_fit_recovers_diffusion_time(connectome):
    A, _ = connectome
    x0 = np.zeros(len(A))
    x0[5] = 1.0
    target = network_diffusion(A, x0, 4.0)
    t_best, r_best, _ = fit_diffusion_time(A, x0, target, t_grid=np.linspace(0.5, 10, 96))
    assert abs(t_best - 4.0) < 0.2
    assert r_best > 0.999


def test_fkpp_bounded_and_saturates(connectome):
    A, _ = connectome
    x0 = np.zeros(len(A))
    x0[0] = 0.1
    out = fkpp(A, x0, np.linspace(0, 30, 31), rho=0.5, alpha=0.5)
    assert out.min() >= -1e-6 and out.max() <= 1 + 1e-6
    assert out[-1].min() > 0.9  # logistic growth drives every connected region toward 1


def test_rewire_preserves_degree(connectome):
    A, _ = connectome
    R = rewire_preserving_degree(A, seed=1)
    np.testing.assert_array_equal((A > 0).sum(axis=1), (R > 0).sum(axis=1))
    np.testing.assert_allclose(R, R.T)
    assert not np.array_equal(A > 0, R > 0)


def test_true_connectome_beats_nulls(connectome):
    A, coords = connectome
    rng = np.random.default_rng(2)
    x0 = np.zeros(len(A))
    x0[7] = 1.0
    target = network_diffusion(A, x0, 3.0) + rng.normal(0, 0.005, len(A))
    res = null_test(A, x0, target, coords=coords, n_null=30, seed=3)
    assert res.beats_nulls()


def test_unrelated_pattern_does_not_beat_nulls(connectome):
    A, coords = connectome
    rng = np.random.default_rng(4)
    x0 = np.zeros(len(A))
    x0[7] = 1.0
    target = rng.normal(size=len(A))
    res = null_test(A, x0, target, coords=coords, n_null=30, seed=5)
    assert not res.beats_nulls()
