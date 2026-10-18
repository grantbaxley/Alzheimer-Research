"""Adapter for pySuStaIn (ucl-pond/pySuStaIn, MIT): run Z-score SuStaIn on a synthetic cohort.

Install with ``pip install -e .[progression]`` (pinned commit). This adapter
exists so pySuStaIn can be checked against known ground truth before it is
used on real, DUA-governed data.
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass

import numpy as np

from ..eval.metrics import kendall_tau_order
from ..synthetic.progression import SyntheticCohort


@dataclass
class SustainRecovery:
    estimated_orders: list[np.ndarray]
    kendall_tau: list[float]
    ml_subtype: np.ndarray
    ml_stage: np.ndarray


def _event_order_from_sequence(seq: np.ndarray, n_biomarkers: int, n_thresholds: int):
    """Collapse a Z-score SuStaIn stage sequence to a per-biomarker order (first threshold)."""
    # pySuStaIn orders (biomarker, threshold) pairs; index k maps to biomarker k % N
    # because Z_vals is flattened column-wise over thresholds.
    biomarker_of_stage = np.tile(np.arange(n_biomarkers), n_thresholds)
    seen, order = set(), []
    for stage_index in np.asarray(seq, dtype=int):
        b = int(biomarker_of_stage[stage_index])
        if b not in seen:
            seen.add(b)
            order.append(b)
    return np.asarray(order)


def run_zscore_sustain(
    cohort: SyntheticCohort,
    z_thresholds=(1.0, 2.0, 3.0),
    n_subtypes_max: int = 1,
    n_startpoints: int = 10,
    n_iterations_mcmc: int = 10_000,
    seed: int = 0,
    output_folder: str | None = None,
) -> SustainRecovery:
    """Fit Z-score SuStaIn and score recovered event orders against the truth.

    Recovered subtypes are matched to true subtypes greedily by Kendall tau,
    since SuStaIn's subtype labels are arbitrary.
    """
    from pySuStaIn import ZscoreSustain  # optional dependency

    n_b = cohort.n_biomarkers
    z_vals = np.tile(np.asarray(z_thresholds, dtype=float), (n_b, 1))
    z_max = np.full(n_b, float(cohort.params.get("z_max", 4.0)) + 1.0)
    with tempfile.TemporaryDirectory() as tmp:
        model = ZscoreSustain(
            cohort.data,
            z_vals,
            z_max,
            cohort.biomarker_labels,
            n_startpoints,
            n_subtypes_max,
            n_iterations_mcmc,
            output_folder or tmp,
            "synthetic",
            False,
            seed,
        )
        result = model.run_sustain_algorithm(plot=False)
    samples_sequence, _f, ml_subtype, _p_sub, ml_stage, _p_stage, _p_ss = result
    # samples_sequence: (n_subtypes, n_stages, n_samples). pySuStaIn seeds MCMC sample 0
    # with the EM maximum-likelihood sequence (AbstractSustain._perform_mcmc).
    est = [
        _event_order_from_sequence(samples_sequence[s, :, 0], n_b, len(z_thresholds))
        for s in range(samples_sequence.shape[0])
    ]
    taus, remaining = [], list(range(len(est)))
    for true in cohort.orders:
        if not remaining:
            break
        best = max(remaining, key=lambda k: kendall_tau_order(true, est[k]))
        taus.append(kendall_tau_order(true, est[best]))
        remaining.remove(best)
    return SustainRecovery(
        estimated_orders=est,
        kendall_tau=taus,
        ml_subtype=np.asarray(ml_subtype).ravel(),
        ml_stage=np.asarray(ml_stage).ravel(),
    )
