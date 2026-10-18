"""Subject-level (grouped) data splits.

Splitting scans, slices or visits instead of subjects is the most common
source of inflated accuracy in AD machine learning (Wen et al. 2020;
Yagis et al. 2021: +29-55 points, ~96% on random labels). Every split here is
made over unique subject IDs, and ``assert_no_subject_leakage`` is meant to be
called in every evaluation script and test.
"""

from __future__ import annotations

from collections.abc import Iterator

import numpy as np


class LeakageError(AssertionError):
    """Raised when the same subject appears on both sides of a split."""


def assert_no_subject_leakage(train_subjects, test_subjects) -> None:
    """Raise LeakageError if any subject ID is in both train and test."""
    overlap = set(np.asarray(train_subjects).tolist()) & set(np.asarray(test_subjects).tolist())
    if overlap:
        sample = sorted(overlap)[:5]
        raise LeakageError(f"{len(overlap)} subject(s) in both train and test, e.g. {sample}")


def group_train_test_split(
    subject_ids, test_size: float = 0.2, seed: int | None = None
) -> tuple[np.ndarray, np.ndarray]:
    """Return boolean (train_mask, test_mask) over rows, splitting by subject."""
    if not 0 < test_size < 1:
        raise ValueError("test_size must be in (0, 1)")
    subject_ids = np.asarray(subject_ids)
    unique = np.unique(subject_ids)
    if len(unique) < 2:
        raise ValueError("need at least two subjects to split")
    rng = np.random.default_rng(seed)
    n_test = min(len(unique) - 1, max(1, round(test_size * len(unique))))
    test_subjects = rng.choice(unique, size=n_test, replace=False)
    test_mask = np.isin(subject_ids, test_subjects)
    train_mask = ~test_mask
    assert_no_subject_leakage(subject_ids[train_mask], subject_ids[test_mask])
    return train_mask, test_mask


def group_kfold(
    subject_ids, n_splits: int = 5, seed: int | None = None
) -> Iterator[tuple[np.ndarray, np.ndarray]]:
    """Yield (train_mask, test_mask) for k folds over unique subjects."""
    subject_ids = np.asarray(subject_ids)
    unique = np.unique(subject_ids)
    if n_splits < 2 or n_splits > len(unique):
        raise ValueError("n_splits must be in [2, number of subjects]")
    rng = np.random.default_rng(seed)
    folds = np.array_split(rng.permutation(unique), n_splits)
    for fold in folds:
        test_mask = np.isin(subject_ids, fold)
        train_mask = ~test_mask
        assert_no_subject_leakage(subject_ids[train_mask], subject_ids[test_mask])
        yield train_mask, test_mask
