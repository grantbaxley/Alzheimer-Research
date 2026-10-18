"""Checks pySuStaIn against synthetic ground truth. Run with: pytest -m integration"""

import numpy as np
import pytest

pytest.importorskip("pySuStaIn")

from alzres.integrations.pysustain import run_zscore_sustain  # noqa: E402
from alzres.synthetic import simulate_cohort  # noqa: E402


@pytest.mark.integration
def test_pysustain_recovers_single_subtype_order():
    order = np.array([2, 0, 3, 1])
    c = simulate_cohort(n_patients=200, n_controls=80, n_biomarkers=4, orders=[order], seed=1)
    r = run_zscore_sustain(c, n_startpoints=5, n_iterations_mcmc=5000, seed=0)
    assert r.kendall_tau[0] >= 0.66
