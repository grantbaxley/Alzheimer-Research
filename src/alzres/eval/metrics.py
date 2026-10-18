"""Metrics for comparing recovered progression structure to ground truth."""

from __future__ import annotations

import numpy as np
from scipy.stats import kendalltau


def kendall_tau_order(true_order, estimated_order) -> float:
    """Kendall's tau between two event orders (biomarker indices, earliest first).

    1.0 means identical orders, -1.0 means reversed.
    """
    true_order = np.asarray(true_order)
    estimated_order = np.asarray(estimated_order)
    if sorted(true_order.tolist()) != sorted(estimated_order.tolist()):
        raise ValueError("orders must be permutations of the same biomarkers")
    n = len(true_order)
    true_pos = np.empty(n, dtype=int)
    est_pos = np.empty(n, dtype=int)
    true_pos[true_order] = np.arange(n)
    est_pos[estimated_order] = np.arange(n)
    return float(kendalltau(true_pos, est_pos).statistic)
