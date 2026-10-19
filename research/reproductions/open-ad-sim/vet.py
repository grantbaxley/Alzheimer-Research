#!/usr/bin/env python3
"""Independent vetting checks for models/open-ad-sim (write-up: README.md in this folder).

    python research/reproductions/open-ad-sim/vet.py all --out results.json [--jobs 4]
    python research/reproductions/open-ad-sim/vet.py all --tasks recovery --members v6_r05,q1_r01 \
        --out recovery.json
    python research/reproductions/open-ad-sim/vet.py worker --member v6_r01 --task validation

Checks, per ensemble member:
  validation   re-run model/validate.py (P=8000, seed 33) and compare with the committed
               ensemble/valid_<member>.json; then re-run on fresh seeds 34-38.
  calibration  re-evaluate the committed parameters with calibrate.evaluate (P=4000, seed 11,
               the settings the fit used) and compare with the stored fit metrics; then evaluate on
               fresh seeds and a 4x larger population; then one-at-a-time +/-10% and +/-30%
               parameter perturbations (common random numbers) to see which parameters the data
               constrain.
  recovery     replace the targets by the model's own output at the fitted parameters, start the
               optimiser from a random 20% perturbation, and see whether it finds them again.

Each member runs in its own process because brain_sim reads ADSIM_VARIANT at import time.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import contextlib
import io
import json
import math
import numbers
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SIM = ROOT / "models" / "open-ad-sim"
MODEL = SIM / "model"
ENSEMBLE = SIM / "ensemble"

CALIB_P, CALIB_SEED, CALIB_EVAL_SEED = 4000, 11, 7
VALID_P, VALID_SEED = 8000, 33
FRESH_VALID_SEEDS = (34, 35, 36, 37, 38)
FRESH_CALIB_SEEDS = (101, 102, 103, 104, 105)
LARGE_P, LARGE_SEED = 16000, 201
PERTURB = (0.7, 0.9, 1.1, 1.3)


def members() -> list[str]:
    return sorted(p.stem.replace("calib_", "") for p in ENSEMBLE.glob("calib_*.json"))


def calib_file(member: str) -> Path:
    return ENSEMBLE / f"calib_{member}.json"


def variant_of(member: str) -> str:
    return json.loads(calib_file(member).read_text()).get("variant", "base")


def _numeric_diff(a: dict, b: dict) -> tuple[float, list[str]]:
    """Max absolute difference over shared numeric keys, and keys whose values differ at all."""
    worst, differing = 0.0, []
    for k, v in b.items():
        if _is_number(v) and _is_number(a.get(k)):
            d = abs(float(a[k]) - float(v))
            worst = max(worst, d)
            if d != 0.0:
                differing.append(k)
    return worst, differing


def _is_number(x) -> bool:
    return isinstance(x, numbers.Real) and not isinstance(x, bool)


def _json_default(o):
    item = getattr(o, "item", None)  # numpy scalars
    if callable(item):
        return item()
    raise TypeError(f"not JSON serializable: {type(o)}")


def _quiet(fn, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kwargs)


def task_validation(member: str) -> dict:
    import validate  # imported here, after sys.path and ADSIM_VARIANT are set

    path = str(calib_file(member))
    committed = json.loads((ENSEMBLE / f"valid_{member}.json").read_text())
    out = _quiet(validate.main, path, VALID_P, VALID_SEED)
    worst, differing = _numeric_diff(out, committed)
    fresh = {}
    for s in FRESH_VALID_SEEDS:
        o = _quiet(validate.main, path, VALID_P, s)
        fresh[s] = {
            k: o[k]
            for k in ("V1_dona_3y_vs_untreated", "V2_lec_diff_4.0y", "V3_ATpos_mci_dementia_5y")
        } | {"oos_loss": o["oos_loss"]}
    return {
        "reproduced_bit_identical": not differing,
        "max_abs_diff_vs_committed": worst,
        "differing_keys": differing,
        "committed": {k: committed[k] for k in fresh[FRESH_VALID_SEEDS[0]]},
        "fresh_seeds": fresh,
    }


def task_calibration(member: str) -> dict:
    import calibrate

    cal = json.loads(calib_file(member).read_text())
    g = dict(cal["g"])
    z = calibrate.sample_people(CALIB_P, seed=CALIB_SEED)
    t0 = time.time()
    m = calibrate.evaluate(g, z, seed=CALIB_EVAL_SEED)
    t_eval = time.time() - t0
    worst, differing = _numeric_diff(m, cal["m"])

    def zscores(metrics):
        return {k: (metrics[k] - v) / s for k, (v, s) in calibrate.TARGETS.items()}

    fresh = {}
    for s in FRESH_CALIB_SEEDS:
        mf = calibrate.evaluate(g, calibrate.sample_people(CALIB_P, seed=s), seed=s + 1000)
        fresh[s] = mf["loss"]
    z_large = calibrate.sample_people(LARGE_P, seed=LARGE_SEED)
    ml = calibrate.evaluate(g, z_large, seed=LARGE_SEED + 1000)

    fixed = set(cal.get("fixed", {}))
    sens = []
    base_loss = m["loss"]
    for k in calibrate.PARAM_KEYS:
        if k in fixed:
            continue
        lo, hi = calibrate.BOUNDS[k]
        row = {
            "param": k,
            "value": g[k],
            "at_lower_bound": g[k] <= lo * (1 + 1e-3),
            "at_upper_bound": g[k] >= hi * (1 - 1e-3),
        }
        for f in PERTURB:
            g2 = dict(g)
            g2[k] = g[k] * f
            row[f"dloss_x{f}"] = calibrate.evaluate(g2, z, seed=CALIB_EVAL_SEED)["loss"] - base_loss
        sens.append(row)

    return {
        "stored_loss": cal["loss"],
        "reproduced_loss": m["loss"],
        "reproduced_bit_identical": not differing,
        "max_abs_diff_vs_stored_metrics": worst,
        "differing_metrics": differing,
        "seconds_per_evaluate": t_eval,
        "fresh_seed_loss": fresh,
        "large_population_loss": ml["loss"],
        "large_population_z": zscores(ml),
        "fitted_z": zscores(m),
        "sensitivity": sens,
    }


RECOVERY_SPREAD, RECOVERY_SEED, RECOVERY_MAXFEV = 0.2, 0, 400


def task_recovery(member: str) -> dict:
    """Parameter recovery: can the calibration find known parameters again?

    Targets are replaced by the model's own output at the fitted parameters (same tolerances),
    the optimiser starts from a random perturbation of them, and we compare where it ends up.
    """
    import calibrate
    import numpy as np
    from scipy.optimize import minimize

    cal = json.loads(calib_file(member).read_text())
    calibrate.FIXED.clear()
    calibrate.FIXED.update(cal.get("fixed", {}))
    g_true = dict(cal["g"])
    z = calibrate.sample_people(CALIB_P, seed=CALIB_SEED)
    m_true = calibrate.evaluate(g_true, z, seed=CALIB_EVAL_SEED)
    calibrate.TARGETS = {k: (float(m_true[k]), s) for k, (_, s) in calibrate.TARGETS.items()}
    rng = np.random.default_rng(RECOVERY_SEED)
    x_true = calibrate.pack(g_true)
    x0 = x_true + RECOVERY_SPREAD * rng.standard_normal(len(x_true))
    g0 = calibrate.unpack(x0, g_true)
    best = {"loss": math.inf, "g": g0}

    def f(x):
        g = calibrate.unpack(x, g_true)
        loss = calibrate.evaluate(g, z, seed=CALIB_EVAL_SEED)["loss"]
        if loss < best["loss"]:
            best.update(loss=loss, g=g)
        return loss

    start_loss = f(calibrate.pack(g0))
    minimize(
        f,
        calibrate.pack(g0),
        method="Nelder-Mead",
        options={"maxfev": RECOVERY_MAXFEV, "xatol": 1e-3, "fatol": 1e-3, "adaptive": True},
    )
    keys = calibrate.active_keys()
    rel = {k: best["g"][k] / g_true[k] - 1 for k in keys}
    rel0 = {k: g0[k] / g_true[k] - 1 for k in keys}
    return {
        "loss_at_truth": m_true["loss"],
        "start_loss": start_loss,
        "final_loss": best["loss"],
        "start_rel_error": rel0,
        "final_rel_error": rel,
        "recovered_within_10pct": sorted(k for k in keys if abs(rel[k]) <= 0.10),
        "not_recovered": sorted(k for k in keys if abs(rel[k]) > 0.10),
        "settings": [RECOVERY_SPREAD, RECOVERY_SEED, RECOVERY_MAXFEV],
    }


IMPACT_PROFILE, IMPACT_P, IMPACT_SEED = "mci_moderate_amyloid_70s", 40000, 21


def _decomposition_shares(g: dict) -> dict:
    """Share of the default profile's Alzheimer-related CDR-SB carried by lost neurons."""
    import scenarios
    import yaml

    prof = yaml.safe_load((SIM / "profiles" / "profiles.yaml").read_text())["profiles"]
    pp = scenarios.realize(scenarios.sample_people(IMPACT_P, seed=IMPACT_SEED), g)
    m, snap, _ = scenarios.match_profile(pp, g, prof[IMPACT_PROFILE])
    stc = {k: v[m] for k, v in snap.items()}
    dec, _ = scenarios.decompose(stc, scenarios.subset(pp, m), g)
    taupos, _ = scenarios.tau_status_arr(stc["T"], g)
    cad = dec["cad"].sum()
    out = {f"share_lost_{k}": float(dec[k].sum() / cad) for k in ("shapley_N", "prop_N")}
    out |= {"n_matched": int(m.sum()), "tau_negative_share": float((~taupos).mean())}
    return out


def task_recovery_impact(member: str) -> dict:
    """Does the headline result depend on parameters the calibration cannot identify?

    Compares the lost-neuron share of impairment at the fitted parameters with the share at the
    parameters the recovery test ended at, which fit the same (synthetic) targets almost as well.
    """
    rec = json.loads(Path(__file__).with_name("recovery.json").read_text())
    r = rec["members"][member]["recovery"]
    g_true = json.loads(calib_file(member).read_text())["g"]
    g_rec = {k: v * (1 + r["final_rel_error"].get(k, 0.0)) for k, v in g_true.items()}
    return {
        "fitted": _decomposition_shares(g_true),
        "recovered": _decomposition_shares(g_rec),
        "recovered_fit_loss": r["final_loss"],
        "settings": [IMPACT_PROFILE, IMPACT_P, IMPACT_SEED],
    }


TASKS = {
    "validation": task_validation,
    "calibration": task_calibration,
    "recovery": task_recovery,
    "recovery_impact": task_recovery_impact,
}


def worker(member: str, task: str) -> None:
    sys.path.insert(0, str(MODEL))
    expected = variant_of(member)
    actual = os.environ.get("ADSIM_VARIANT", "base")
    if actual != expected:
        raise SystemExit(f"{member} needs ADSIM_VARIANT={expected}, got {actual}")
    t0 = time.time()
    result = TASKS[task](member)
    result["seconds"] = time.time() - t0
    print(json.dumps(result, default=_json_default))


def run_all(out: Path, jobs: int, tasks: list[str], only: list[str] | None = None) -> None:
    def launch(member: str, task: str):
        env = dict(os.environ, ADSIM_VARIANT=variant_of(member))
        cmd = [sys.executable, __file__, "worker", "--member", member, "--task", task]
        r = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=SIM)
        if r.returncode != 0:
            return member, task, {"error": r.stderr[-4000:]}
        return member, task, json.loads(r.stdout.strip().splitlines()[-1])

    results: dict = {
        "settings": {
            "calibration": [CALIB_P, CALIB_SEED, CALIB_EVAL_SEED],
            "validation": [VALID_P, VALID_SEED],
            "fresh_validation_seeds": FRESH_VALID_SEEDS,
            "fresh_calibration_seeds": FRESH_CALIB_SEEDS,
            "large_population": [LARGE_P, LARGE_SEED],
            "perturbation_factors": PERTURB,
            "python": sys.version.split()[0],
        },
        "members": {},
    }
    try:
        import numpy
        import scipy

        results["settings"]["numpy"] = numpy.__version__
        results["settings"]["scipy"] = scipy.__version__
    except ImportError:
        pass
    work = [(m, t) for t in tasks for m in members() if not only or m in only]
    with cf.ThreadPoolExecutor(max_workers=jobs) as pool:
        for member, task, res in pool.map(lambda mt: launch(*mt), work):
            results["members"].setdefault(member, {"variant": variant_of(member)})[task] = res
            status = "error" if "error" in res else f"{res.get('seconds', math.nan):.0f}s"
            print(f"{member:12s} {task:12s} {status}", flush=True)
    out.write_text(json.dumps(results, indent=1, sort_keys=True))
    print(f"wrote {out}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("all")
    a.add_argument("--out", type=Path, default=Path(__file__).with_name("results.json"))
    a.add_argument("--jobs", type=int, default=2)
    a.add_argument("--tasks", default="calibration,validation", help="comma-separated")
    a.add_argument("--members", default="", help="comma-separated; default all")
    w = sub.add_parser("worker")
    w.add_argument("--member", required=True)
    w.add_argument("--task", choices=sorted(TASKS), required=True)
    args = ap.parse_args()
    if args.cmd == "all":
        only = [m for m in args.members.split(",") if m]
        run_all(args.out, args.jobs, args.tasks.split(","), only)
    else:
        worker(args.member, args.task)


if __name__ == "__main__":
    main()
