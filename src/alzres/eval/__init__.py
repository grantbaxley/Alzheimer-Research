"""Leakage-proof evaluation: subject-level splits, naive baselines, ordering metrics."""

from .baselines import mean_rank_event_order, predict_last_value, predict_train_mean
from .metrics import kendall_tau_order
from .splits import LeakageError, assert_no_subject_leakage, group_kfold, group_train_test_split

__all__ = [
    "LeakageError",
    "assert_no_subject_leakage",
    "group_kfold",
    "group_train_test_split",
    "kendall_tau_order",
    "mean_rank_event_order",
    "predict_last_value",
    "predict_train_mean",
]
