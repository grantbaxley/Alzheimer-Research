import numpy as np
import pytest

from alzres.eval import kendall_tau_order, mean_rank_event_order
from alzres.synthetic import simulate_cohort


def test_shapes_and_labels():
    c = simulate_cohort(n_patients=50, n_controls=20, n_biomarkers=5, visits_per_subject=3, seed=0)
    assert c.data.shape == (70 * 3, 5)
    assert len(np.unique(c.subject_id)) == 70
    assert (c.subtype[~c.is_patient] == -1).all()
    assert (c.disease_time[~c.is_patient] == 0).all()


def test_reproducible_with_seed():
    a = simulate_cohort(seed=42)
    b = simulate_cohort(seed=42)
    np.testing.assert_array_equal(a.data, b.data)


def test_controls_are_standard_normal():
    c = simulate_cohort(n_patients=10, n_controls=4000, seed=1)
    controls = c.data[~c.is_patient]
    assert np.abs(controls.mean(axis=0)).max() < 0.1
    assert np.abs(controls.std(axis=0) - 1).max() < 0.1


def test_longitudinal_disease_time_never_decreases():
    c = simulate_cohort(n_patients=40, n_controls=0, visits_per_subject=4, seed=3)
    for sid in np.unique(c.subject_id):
        t = c.disease_time[c.subject_id == sid]
        assert (np.diff(t) >= 0).all()


def test_baseline_recovers_single_subtype_order():
    order = np.array([3, 0, 4, 1, 2])
    c = simulate_cohort(n_patients=500, n_controls=0, n_biomarkers=5, orders=[order], seed=7)
    est = mean_rank_event_order(c.data, c.is_patient)
    assert kendall_tau_order(order, est) == pytest.approx(1.0)


def test_baseline_fails_on_opposing_subtypes():
    # Two subtypes with reversed orders: a subtype-blind baseline cannot recover either.
    order = np.arange(6)
    c = simulate_cohort(
        n_patients=1000,
        n_controls=0,
        n_biomarkers=6,
        n_subtypes=2,
        orders=[order, order[::-1]],
        seed=11,
    )
    est = mean_rank_event_order(c.data, c.is_patient)
    assert abs(kendall_tau_order(order, est)) < 0.8


def test_rejects_invalid_orders():
    with pytest.raises(ValueError):
        simulate_cohort(n_biomarkers=3, orders=[np.array([0, 0, 1])])
