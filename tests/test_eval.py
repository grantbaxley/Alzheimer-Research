import numpy as np
import pytest

from alzres.eval import (
    LeakageError,
    assert_no_subject_leakage,
    group_kfold,
    group_train_test_split,
    kendall_tau_order,
    predict_last_value,
    predict_train_mean,
)
from alzres.synthetic import simulate_cohort


def test_split_keeps_subjects_together():
    c = simulate_cohort(n_patients=80, n_controls=20, visits_per_subject=4, seed=0)
    train, test = group_train_test_split(c.subject_id, test_size=0.25, seed=0)
    assert not set(c.subject_id[train]) & set(c.subject_id[test])
    assert train.sum() + test.sum() == len(c.subject_id)
    assert len(set(c.subject_id[test])) == 25


def test_kfold_covers_every_subject_once():
    ids = np.repeat(np.arange(30), 3)
    seen = []
    for train, test in group_kfold(ids, n_splits=5, seed=1):
        assert not set(ids[train]) & set(ids[test])
        seen.extend(np.unique(ids[test]).tolist())
    assert sorted(seen) == list(range(30))


def test_leakage_is_detected():
    with pytest.raises(LeakageError):
        assert_no_subject_leakage([1, 2, 3], [3, 4])


def test_visit_level_split_would_leak():
    # Demonstrates the failure mode the grouped split prevents.
    c = simulate_cohort(n_patients=50, n_controls=0, visits_per_subject=3, seed=2)
    rng = np.random.default_rng(0)
    rows = rng.permutation(len(c.subject_id))
    naive_train, naive_test = rows[:100], rows[100:]
    with pytest.raises(LeakageError):
        assert_no_subject_leakage(c.subject_id[naive_train], c.subject_id[naive_test])


def test_last_value_carried_forward():
    sids = [1, 1, 2, 2, 2]
    visits = [0, 1, 0, 2, 1]
    vals = [10.0, 11.0, 20.0, 22.0, 21.0]
    out = predict_last_value(sids, visits, vals, [2, 1, 9])
    np.testing.assert_array_equal(out[:2], [22.0, 11.0])
    assert np.isnan(out[2])


def test_train_mean():
    np.testing.assert_array_equal(predict_train_mean([1.0, 3.0], 3), [2.0, 2.0, 2.0])


def test_kendall_tau_order():
    assert kendall_tau_order([0, 1, 2, 3], [0, 1, 2, 3]) == pytest.approx(1.0)
    assert kendall_tau_order([0, 1, 2, 3], [3, 2, 1, 0]) == pytest.approx(-1.0)
    with pytest.raises(ValueError):
        kendall_tau_order([0, 1, 2], [0, 1, 3])
