"""Checks on models/open-ad-sim (vetting write-up: research/reproductions/open-ad-sim/README.md).

* The documented equations (brain_sim.py docstring, docs/MODEL.md) are re-implemented here
  independently, with plain loops, and compared with the model's vectorised step().
* Physical invariants hold over a full simulated life course.
* Committed calibration metrics and validation outputs reproduce from the committed code.
* Profiles stay generic: ranges only, nothing person-like (policy/PRIVACY.md).
"""

import json
import math
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "models" / "open-ad-sim"
MODEL = SIM / "model"
ENSEMBLE = SIM / "ensemble"
MEMBERS = sorted(p.stem.replace("calib_", "") for p in ENSEMBLE.glob("calib_*.json"))
# Cross-platform tolerance: BLAS and NumPy versions can move a borderline virtual person across
# a threshold, which shifts a proportion by ~1/n. Bit-identity on the reference environment is
# recorded in the vetting write-up.
TOL = 0.02


def calib(member):
    return json.loads((ENSEMBLE / f"calib_{member}.json").read_text())


@pytest.fixture(scope="module")
def sim():
    saved = os.environ.pop("ADSIM_VARIANT", None)
    sys.path.insert(0, str(MODEL))
    try:
        import brain_sim
        import calibrate

        assert brain_sim.VARIANT == "base"
        yield SimpleNamespace(bs=brain_sim, cal=calibrate)
    finally:
        sys.path.remove(str(MODEL))
        if saved is not None:
            os.environ["ADSIM_VARIANT"] = saved


def documented_step(st, pp, g, dt, bs):
    """One step of the model written from its documentation, one person and region at a time."""
    P, R = st["T"].shape
    out = {k: np.array(v, dtype=float, copy=True) for k, v in st.items()}
    for p in range(P):
        A = st["A"][p]
        a, amax = A + 15.0, pp["Amax"][p] + 15.0
        out["A"][p] = A + pp["rA"][p] * a * (1 - a / amax) * dt  # logistic rise toward Amax
        Ap = max(A, 0.0)
        h = Ap**4 / (Ap**4 + 45.0**4)  # amyloid "permission" for tau
        fa = math.exp(math.log(2) / 15 * (st["age"][p] - 70.0))  # rates double per 15 years
        for r in range(R):
            T = st["T"][p, r]
            growth = (
                g["k0"] * pp["fk0"][p] * bs.M0[r]
                + g["kA"] * pp["fkA"][p] * h * bs.MA[r]
                + g["kauto"] * pp["fka"][p] * T
            ) * T
            spread = (g["b0"] + g["bA"] * pp["fbA"][p] * h) * sum(
                bs.W[r, j] * st["T"][p, j] for j in range(R)
            )
            out["T"][p, r] = min(max(T + fa * (growth + spread) * (1 - T) * dt, 0.0), 1.0)
            late = bs.LATE_RATE * bs.LATE_M[r] if st["age"][p] >= pp["late_on"][p] else 0.0
            death = fa * g["delta"] * pp["fdel"][p] * bs.VULN[r] * T ** g["pN"] + late
            out["N"][p, r] = st["N"][p, r] * math.exp(-death * dt)
            lost_inputs = sum(bs.WN[r, j] * (1 - st["N"][p, j]) for j in range(R))
            insult = (
                g["sT"] * pp["fsT"][p] * T
                + g["sA"] * bs.AMY[r] * Ap / 100.0
                + g["sD"] * lost_inputs
            )
            target = 1.0 / (1.0 + insult)
            S = st["S"][p, r]
            rate = 2.0 if S > target else g["rho"]  # falls fast, recovers at rho
            out["S"][p, r] = min(max(target + (S - target) * math.exp(-rate * dt), 0.0), 1.0)
        out["age"][p] = st["age"][p] + dt
    return out


def documented_cdr(st, pp, g, bs):
    D = 1 - (st["N"] * st["S"]) @ bs.W_COG
    return [
        min(g["a_cdr"] * pp["fres"][p] * max(D[p] - pp["R"][p], 0.0) ** g["q"], 18.0) + pp["eps"][p]
        for p in range(len(D))
    ]


def random_state(bs, P, rng):
    R = len(bs.REG)
    return dict(
        A=rng.uniform(-10, 130, P),
        T=rng.uniform(0, 0.7, (P, R)),
        N=rng.uniform(0.4, 1.0, (P, R)),
        S=rng.uniform(0.5, 1.0, (P, R)),
        age=rng.uniform(55, 90, P),
    )


def test_code_matches_documented_equations(sim):
    bs = sim.bs
    rng = np.random.default_rng(0)
    for member in ("v6_r01", "v6_r05", "q1_r01"):  # the base-variant members
        g = calib(member)["g"]
        pp = bs.realize(bs.sample_people(12, seed=3), g)
        st = random_state(bs, 12, rng)
        expected = documented_step(st, pp, g, 0.1, bs)
        got = bs.step(bs.copy_state(st), pp, g, 0.1)
        for k in ("A", "T", "N", "S", "age"):
            np.testing.assert_allclose(got[k], expected[k], rtol=1e-12, atol=1e-12, err_msg=k)
        np.testing.assert_allclose(bs.cognition(got, pp, g), documented_cdr(got, pp, g, bs))


def test_life_course_invariants(sim):
    bs = sim.bs
    g = calib("v6_r05")["g"]
    pp = bs.realize(bs.sample_people(300, seed=5), g)
    st = bs.init_state(pp, 48.0)
    prev_N = st["N"].copy()
    for _ in range(420):  # age 48 to 90
        bs.step(st, pp, g, 0.1)
        assert (st["T"] >= 0).all() and (st["T"] <= 1).all()
        assert (st["S"] >= 0).all() and (st["S"] <= 1).all()
        assert (st["N"] > 0).all() and (st["N"] <= prev_N + 1e-15).all()  # loss is permanent
        prev_N = st["N"].copy()
    assert (st["A"] <= pp["Amax"] + 1e-6).all()


def test_interventions_do_what_they_say(sim):
    bs = sim.bs
    g = calib("v6_r05")["g"]
    pp = bs.realize(bs.sample_people(200, seed=6), g)
    st0 = bs.run_to(pp, g, 48.0, 75.0)
    frozen = bs.step(bs.copy_state(st0), pp, g, 0.1, tau_block=1.0, stop_neuron=1.0)
    np.testing.assert_array_equal(frozen["T"], st0["T"])
    np.testing.assert_array_equal(frozen["N"], st0["N"])
    cleared = bs.copy_state(st0)
    for _ in range(40):
        bs.step(cleared, pp, g, 0.1, ab_k=np.full(200, 2.0))
    pos = st0["A"] > 30  # antibodies are given to amyloid-positive people; the clearance term
    # relaxes toward the 5 CL floor from either side, so it would nudge sub-floor values up
    assert pos.sum() > 50
    assert (cleared["A"][pos] < st0["A"][pos]).all() and (cleared["A"][pos] > 5.0 - 1e-9).all()
    ceiling = bs.step(bs.copy_state(st0), pp, g, 0.1, S_floor=1.0)
    assert (ceiling["S"] == 1.0).all()
    worse = bs.copy_state(st0)
    worse["N"] = worse["N"] * 0.9
    assert (bs.cognition(worse, pp, g) >= bs.cognition(st0, pp, g) - 1e-12).all()


def test_calibration_fit_reproduces(sim):
    for member in ("v6_r01", "v6_r05"):
        cal = calib(member)
        m = sim.cal.evaluate(cal["g"], sim.cal.sample_people(4000, seed=11))
        assert abs(m["loss"] - cal["loss"]) < 0.05 * cal["loss"]
        for k in sim.cal.TARGETS:
            assert abs(float(m[k]) - cal["m"][k]) < TOL, k


def run_validate(member, tmp_path, variant):
    tmp = tmp_path / f"calib_{member}.json"
    tmp.write_text((ENSEMBLE / f"calib_{member}.json").read_text())
    env = (
        dict(os.environ, ADSIM_VARIANT=variant)
        if variant
        else {k: v for k, v in os.environ.items() if k != "ADSIM_VARIANT"}
    )
    r = subprocess.run(
        [sys.executable, str(MODEL / "validate.py"), str(tmp)],
        cwd=SIM, env=env, capture_output=True, text=True,
    )  # fmt: skip
    return r, tmp_path / f"valid_{member}.json"


def assert_validation_matches(path, member):
    got = json.loads(path.read_text())
    ref = json.loads((ENSEMBLE / f"valid_{member}.json").read_text())
    for k, v in ref.items():
        if isinstance(v, float):
            assert abs(got[k] - v) < (0.5 if k == "oos_loss" else TOL), k


def test_validation_reproduces_for_a_base_member(tmp_path):
    r, out = run_validate("v6_r01", tmp_path, "base")
    assert r.returncode == 0, r.stderr
    assert_validation_matches(out, "v6_r01")


def test_variant_mismatch_is_refused(tmp_path):
    r, _ = run_validate("flatcog_r05", tmp_path, None)
    assert r.returncode != 0
    assert "ADSIM_VARIANT=flatcog" in (r.stderr + r.stdout)


@pytest.mark.integration
@pytest.mark.parametrize("member", MEMBERS)
def test_every_member_validation_reproduces(member, tmp_path):
    r, out = run_validate(member, tmp_path, calib(member).get("variant", "base"))
    assert r.returncode == 0, r.stderr
    assert_validation_matches(out, member)


def test_profiles_are_generic_ranges():
    profiles = yaml.safe_load((SIM / "profiles" / "profiles.yaml").read_text())["profiles"]
    assert profiles
    for name, prof in profiles.items():
        assert "apoe" not in prof, f"{name}: APOE is not used by the model; keep genotype out"
        assert "e4" not in name and "apoe" not in prof.get("description", "").lower(), name
        for field in ("age", "centiloid", "cdr_sb"):
            lo, hi = prof[field]
            assert lo < hi, (name, field)
        assert prof["age"][1] - prof["age"][0] >= 5, f"{name}: age band too narrow to be generic"
