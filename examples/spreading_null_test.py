"""Fit the network diffusion model and test it against rewired and spatial nulls.

Runs on a synthetic connectome, so it is safe to share. Replace A, coords and target
with your own connectome and regional tau/atrophy map (kept outside the repo).

    python examples/spreading_null_test.py
"""

import numpy as np

from alzres.spreading import fit_diffusion_time, network_diffusion, null_test, synthetic_connectome

A, coords = synthetic_connectome(n_regions=60, seed=0)
seed_region = 7
x0 = np.zeros(len(A))
x0[seed_region] = 1.0

rng = np.random.default_rng(1)
target = network_diffusion(A, x0, 3.0) + rng.normal(0, 0.01, len(A))  # stand-in for a tau map

t_best, r_best, _ = fit_diffusion_time(A, x0, target)
res = null_test(A, x0, target, coords=coords, n_null=200, seed=2)

print(f"NDM fit: t = {t_best:.2f}, r = {r_best:.3f}")
print(f"rewired nulls: median r = {np.median(res.r_rewired):.3f}, p = {res.p_rewired:.4f}")
print(f"spatial (distance) null: r = {res.r_distance:.3f}")
print("beats nulls:", res.beats_nulls())
