"""Synthetic biomarker cohorts with a known disease-progression ground truth.

No real participant data is used. Each patient has a latent disease time
t in [0, 1] and a subtype; each biomarker in that subtype becomes abnormal at
an onset time and then rises linearly to ``z_max`` (in z-score units relative
to controls). Controls sit at t = 0. Observations add unit Gaussian noise.

Because the event ordering, subtype and stage of every subject are known,
these cohorts can test whether a progression model (pySuStaIn, kde_ebm,
Leaspy, ...) actually recovers the truth before it is trusted on real data.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class SyntheticCohort:
    """Cross-sectional or longitudinal synthetic cohort.

    Attributes:
        data: (n_observations, n_biomarkers) z-scores.
        subject_id: (n_observations,) integer subject identifier.
        visit: (n_observations,) visit index within subject.
        is_patient: (n_observations,) True for patients, False for controls.
        subtype: (n_observations,) subtype index, -1 for controls.
        disease_time: (n_observations,) latent disease time in [0, 1].
        orders: per-subtype true event order (biomarker indices, earliest first).
        biomarker_labels: names for the biomarker columns.
        params: generator parameters, for provenance.
    """

    data: np.ndarray
    subject_id: np.ndarray
    visit: np.ndarray
    is_patient: np.ndarray
    subtype: np.ndarray
    disease_time: np.ndarray
    orders: list[np.ndarray]
    biomarker_labels: list[str]
    params: dict = field(default_factory=dict)

    @property
    def n_biomarkers(self) -> int:
        return self.data.shape[1]


def _onsets(order: np.ndarray, spread: float) -> np.ndarray:
    """Onset times for biomarkers given an order; evenly spaced over [0, 1 - spread]."""
    n = len(order)
    onsets = np.empty(n)
    onsets[order] = np.linspace(0.0, 1.0 - spread, n)
    return onsets


def simulate_cohort(
    n_patients: int = 300,
    n_controls: int = 100,
    n_biomarkers: int = 6,
    n_subtypes: int = 1,
    orders: list[np.ndarray] | None = None,
    z_max: float = 4.0,
    rise_duration: float = 0.3,
    noise_sd: float = 1.0,
    visits_per_subject: int = 1,
    visit_interval: float = 0.05,
    seed: int | None = None,
) -> SyntheticCohort:
    """Simulate a cohort with known event orders, subtypes and disease times.

    Args:
        n_patients: number of patient subjects.
        n_controls: number of control subjects (disease time 0, no subtype).
        n_biomarkers: number of biomarkers.
        n_subtypes: number of progression subtypes.
        orders: optional explicit event order per subtype; random otherwise.
        z_max: z-score each biomarker reaches at the end of its rise.
        rise_duration: disease-time span over which a biomarker rises to z_max.
        noise_sd: standard deviation of observation noise.
        visits_per_subject: >1 makes the cohort longitudinal.
        visit_interval: disease-time step between visits.
        seed: random seed for reproducibility.
    """
    if n_biomarkers < 2:
        raise ValueError("need at least two biomarkers")
    if not 0 < rise_duration < 1:
        raise ValueError("rise_duration must be in (0, 1)")
    rng = np.random.default_rng(seed)

    if orders is None:
        orders = [rng.permutation(n_biomarkers) for _ in range(n_subtypes)]
    else:
        orders = [np.asarray(o) for o in orders]
        if len(orders) != n_subtypes:
            raise ValueError("len(orders) must equal n_subtypes")
        for o in orders:
            if sorted(o.tolist()) != list(range(n_biomarkers)):
                raise ValueError("each order must be a permutation of biomarker indices")
    onsets = [_onsets(o, rise_duration) for o in orders]

    patient_subtype = rng.integers(0, n_subtypes, size=n_patients)
    max_start = max(0.0, 1.0 - visit_interval * (visits_per_subject - 1))
    patient_t0 = rng.uniform(0.0, max_start, size=n_patients)

    rows, sids, visits, patient, subtypes, times = [], [], [], [], [], []
    for sid in range(n_controls + n_patients):
        is_pt = sid >= n_controls
        k = sid - n_controls
        for v in range(visits_per_subject):
            if is_pt:
                s = int(patient_subtype[k])
                t = min(1.0, patient_t0[k] + v * visit_interval)
                mean = z_max * np.clip((t - onsets[s]) / rise_duration, 0.0, 1.0)
            else:
                s, t, mean = -1, 0.0, np.zeros(n_biomarkers)
            rows.append(mean + rng.normal(0.0, noise_sd, size=n_biomarkers))
            sids.append(sid)
            visits.append(v)
            patient.append(is_pt)
            subtypes.append(s)
            times.append(t)

    return SyntheticCohort(
        data=np.vstack(rows),
        subject_id=np.asarray(sids),
        visit=np.asarray(visits),
        is_patient=np.asarray(patient),
        subtype=np.asarray(subtypes),
        disease_time=np.asarray(times),
        orders=orders,
        biomarker_labels=[f"biomarker_{i}" for i in range(n_biomarkers)],
        params=dict(
            n_patients=n_patients,
            n_controls=n_controls,
            n_biomarkers=n_biomarkers,
            n_subtypes=n_subtypes,
            z_max=z_max,
            rise_duration=rise_duration,
            noise_sd=noise_sd,
            visits_per_subject=visits_per_subject,
            visit_interval=visit_interval,
            seed=seed,
        ),
    )
