"""Does pySuStaIn recover known subtypes where a naive baseline cannot?

Two subtypes with opposite event orders: the subtype-blind baseline fails by design,
so this checks that SuStaIn earns its complexity. Needs `pip install -e .[progression]`.
Takes a few minutes.

    python examples/pysustain_synthetic_recovery.py
"""

import numpy as np

from alzres.eval import kendall_tau_order, mean_rank_event_order
from alzres.integrations.pysustain import run_zscore_sustain
from alzres.synthetic import simulate_cohort

order = np.array([0, 1, 2, 3, 4])
cohort = simulate_cohort(
    n_patients=400,
    n_controls=100,
    n_biomarkers=5,
    n_subtypes=2,
    orders=[order, order[::-1]],
    seed=0,
)

baseline = mean_rank_event_order(cohort.data, cohort.is_patient)
print(
    "baseline tau vs each subtype:",
    [round(kendall_tau_order(o, baseline), 2) for o in cohort.orders],
)

result = run_zscore_sustain(cohort, n_subtypes_max=2, n_startpoints=10, n_iterations_mcmc=20_000)
print("SuStaIn recovered orders:", [o.tolist() for o in result.estimated_orders])
print("SuStaIn tau per true subtype:", [round(t, 2) for t in result.kendall_tau])
