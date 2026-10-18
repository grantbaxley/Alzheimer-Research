"""Naive baselines every model in this repo must be compared against.

TADPOLE found no submitted method beat random guessing on ADAS-Cog13 and that
simple ensembles topped most tasks. A model that cannot beat these baselines
on held-out subjects is not an improvement, whatever its headline metric.
"""

from __future__ import annotations

import numpy as np


def predict_train_mean(y_train, n_test: int) -> np.ndarray:
    """Predict the training-set mean for every test observation."""
    y_train = np.asarray(y_train, dtype=float)
    return np.full((n_test,) + y_train.shape[1:], y_train.mean(axis=0))


def predict_last_value(subject_ids, visits, values, query_subjects) -> np.ndarray:
    """Last observation carried forward: each query subject's latest known value.

    Subjects with no history get NaN, so callers must handle them explicitly
    rather than silently scoring them.
    """
    subject_ids = np.asarray(subject_ids)
    visits = np.asarray(visits)
    values = np.asarray(values, dtype=float)
    latest: dict = {}
    for sid, v, val in zip(subject_ids.tolist(), visits.tolist(), values, strict=True):
        if sid not in latest or v > latest[sid][0]:
            latest[sid] = (v, val)
    out_shape = (len(query_subjects),) + values.shape[1:]
    out = np.full(out_shape, np.nan)
    for i, sid in enumerate(np.asarray(query_subjects).tolist()):
        if sid in latest:
            out[i] = latest[sid][1]
    return out


def mean_rank_event_order(data, is_patient) -> np.ndarray:
    """Baseline event ordering: biomarkers with higher mean patient z-score come first.

    This ignores subtypes and staging entirely; a real progression model
    should beat it, especially when there is more than one subtype.
    """
    data = np.asarray(data, dtype=float)
    patients = data[np.asarray(is_patient, dtype=bool)]
    return np.argsort(-patients.mean(axis=0), kind="stable")
