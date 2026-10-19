"""
Virtual patients matching a generic PROFILE, and what each class of treatment could do for them.

  python3 model/scenarios.py --calib ensemble/calib_<member>.json --profile mci_moderate_amyloid_70s
  python3 model/scenarios.py --calib results/calib_<member>.json --patient patients/<local>.yaml   # local only, never committed

A profile (profiles/profiles.yaml) is a set of RANGES: age, Centiloid, CDR-SB, tau status, atrophy. Every virtual person gets a
target age inside the age range; their simulated state at that age is kept if it falls inside every other range.

Outputs (results/scen_<profile>_<member>.json + .npz):
  decomposition — today's Alzheimer-related impairment split into 'neurons gone' vs 'surviving neurons impaired',
                  by three attribution methods (remainder = optimistic, Shapley, proportional = linear mapping); report RANGES
  scenarios     — 10-year CDR-SB trajectories (Alzheimer part) under available, delayed and hypothetical treatments
  window        — the best outcome still possible if a full restoration of surviving neurons began s years from now,
                  with and without an antibody bridge
Every number is a modeled hypothesis for a TYPE of patient, not a prediction for a person.
"""
import numpy as np, json, sys, time, argparse, os
import yaml
from brain_sim import *

SCENARIOS = {
    "none":          dict(label="No treatment", scen={}),
    "ab_now":        dict(label="Antibody now (donanemab-style finite course)", scen={"ab": "donanemab"}),
    "lec_now":       dict(label="Antibody now (lecanemab-style, continuous)", scen={"ab": "lecanemab"}),
    "ab_1y":         dict(label="Antibody delayed 1 year", scen={"ab": "donanemab", "ab_start": 1.0}),
    "ab_2y":         dict(label="Antibody delayed 2 years", scen={"ab": "donanemab", "ab_start": 2.0}),
    "ab_tauhalf_3y": dict(label="Antibody + a drug that halves NEW tangle formation, from year 3 (hypothetical)",
                          scen={"ab": "donanemab", "tau_block": 0.5, "tau_start": 3.0}),
    "ab_tauhalf_now": dict(label="Antibody + a drug that halves new tangle formation, now (hypothetical)",
                           scen={"ab": "donanemab", "tau_block": 0.5}),
    "ab_taustop_now": dict(label="Antibody + no new tangles at all, now (hypothetical; existing tangles still harm)",
                           scen={"ab": "donanemab", "tau_block": 1.0}),
    "ab_freeze_now": dict(label="Antibody + no new tangles + no further neuron death (hypothetical)",
                          scen={"ab": "donanemab", "tau_block": 1.0, "stop_neuron": 1.0}),
    "ab_freeze_repair": dict(label="... + toxic effects on surviving neurons removed, natural repair pace (hypothetical)",
                             scen={"ab": "donanemab", "tau_block": 1.0, "stop_neuron": 1.0, "fix_local": 1.0}),
    "ab_freeze_fastrepair": dict(label="... + a drug that speeds synaptic repair to 2/yr (hypothetical)",
                                 scen={"ab": "donanemab", "tau_block": 1.0, "stop_neuron": 1.0, "fix_local": 1.0, "rho_abs": 2.0}),
    "ceiling_now":   dict(label="Theoretical ceiling: every surviving neuron fully restored incl. rewiring; nothing further lost",
                          scen={"ab": "donanemab", "tau_block": 1.0, "stop_neuron": 1.0, "S_one": True, "fix_start": 0.0}),
    "fix_nonAD":     dict(label="Fix non-Alzheimer contributors only (sleep, medication, mood, hearing...)", scen={"eps_fix_at": 0.25}),
}
WINDOW_STARTS = [0, 1, 2, 3, 4, 5, 6]


def load_profile(args):
    if args.patient:
        prof = yaml.safe_load(open(args.patient))
        name = "local_patient"
    else:
        allp = yaml.safe_load(open(args.profiles))["profiles"]
        prof = allp[args.profile]; name = args.profile
    return name, prof


def match_profile(pp, g, prof, seed=3, dt=0.1):
    """Simulate everyone to a person-specific target age inside the profile's age range; keep those inside every range."""
    rng = np.random.default_rng(seed)
    P = len(pp["rA"])
    a0, a1 = prof["age"]
    target = rng.uniform(a0, a1, P)
    st = run_to(pp, g, 48.0, float(a0), dt=dt)
    snap = copy_state(st)
    taken = np.zeros(P, bool)
    while True:
        due = (~taken) & (st["age"] >= target - dt / 2)
        if due.any():
            for k in ("A", "T", "N", "S", "age"):
                snap[k][due] = st[k][due]
            taken |= due
        if taken.all() or st["age"][0] > a1 + dt:
            break
        step(st, pp, g, dt)
    cdr = cognition(snap, pp, g)
    m = (snap["A"] >= prof["centiloid"][0]) & (snap["A"] <= prof["centiloid"][1]) & \
        (cdr >= prof["cdr_sb"][0]) & (cdr <= prof["cdr_sb"][1])
    taupos, hitau = tau_status_arr(snap["T"], g)
    tau = prof.get("tau", "unknown")
    if tau == "negative":
        m &= ~taupos
    elif tau == "positive":
        m &= taupos & ~hitau
    elif tau == "high":
        m &= hitau
    atro = prof.get("atrophy", "unknown")
    if atro == "present":
        m &= snap["N"][:, IX["EC"]] < 0.95
    elif atro == "absent":
        m &= snap["N"][:, IX["EC"]] >= 0.95
    return m, snap, cdr


def deficits(N, S):
    return 1 - N @ W_COG, (N * (1 - S)) @ W_COG


def decompose(stc, ppc, g):
    """Split today's Alzheimer-related CDR-SB into 'neurons gone' vs 'surviving neurons impaired' three ways."""
    N, S = stc["N"], stc["S"]
    cad = cognition(stc, ppc, g, include_eps=False)
    f_N = cognition(stc, ppc, g, include_eps=False, S=np.ones_like(S))     # neuron loss only
    f_S = cognition(stc, ppc, g, include_eps=False, N=np.ones_like(N))     # survivor impairment only
    shapley_N = 0.5 * f_N + 0.5 * (cad - f_S)
    D_N, D_S = deficits(N, S)
    prop_N = cad * D_N / np.maximum(D_N + D_S, 1e-9)
    Ap = np.clip(stc["A"], 0, None)[:, None] / 100.0
    Din = (1 - N) @ WN.T
    it = g["sT"] * ppc["fsT"][:, None] * stc["T"]; ia = g["sA"] * AMY * Ap; idc = g["sD"] * Din
    wgt = W_COG * N
    tot = ((it + ia + idc) * wgt).sum()
    comp = dict(tau=float((it * wgt).sum() / tot), amyloid=float((ia * wgt).sum() / tot), disconnection=float((idc * wgt).sum() / tot))
    return dict(cad=cad, remainder_N=f_N, shapley_N=shapley_N, prop_N=prop_N), comp


def summarize(c, t, base):
    res = {"series": [dict(year=float(t[i]), p25=float(np.percentile(c[:, i], 25)), p50=float(np.median(c[:, i])),
                           p75=float(np.percentile(c[:, i], 75)), mean=float(c[:, i].mean())) for i in range(len(t))]}
    for yr in (1, 2, 3, 5, 10):
        k = int(round(yr / (t[1] - t[0])))
        res[f"y{yr}_median"] = float(np.median(c[:, k])); res[f"y{yr}_mean"] = float(c[:, k].mean())
        res[f"better_y{yr}"] = float((c[:, k] < base - 0.5).mean())
    crossed = c >= 4.5
    yrs = np.where(crossed.any(1), t[crossed.argmax(1)], np.inf)
    res["years_to_mild_dementia_median"] = float(np.median(yrs))
    res["years_to_mild_dementia_p25"] = float(np.percentile(yrs, 25)); res["years_to_mild_dementia_p75"] = float(np.percentile(yrs, 75))
    res["p_mild_dementia_5y"] = float((yrs <= 5).mean())
    return res


def run(calib_path, prof_name, prof, P=150000, seed=21, out_path=None, years=10.0):
    cal = json.load(open(calib_path)); require_variant(cal, calib_path); g = cal["g"]
    z = sample_people(P, seed=seed)
    pp = realize(z, g)
    t0 = time.time()
    m, snap, cdr = match_profile(pp, g, prof)
    stc = {k: v[m] for k, v in snap.items()}; ppc = subset(pp, m)
    n = int(m.sum()); base_tot = cdr[m]
    if n < 100:
        raise SystemExit(f"only {n} virtual patients match profile {prof_name}; widen its ranges or raise P")
    taupos, hitau = tau_status_arr(stc["T"], g)
    dec, comp = decompose(stc, ppc, g)
    cad = dec["cad"]
    stereo = stc["N"][:, IX["EC"]] <= 0.75
    print(f"{calib_path} / {prof_name}: {n} matched virtual patients ({time.time()-t0:.0f}s)", flush=True)
    out = {"calib": os.path.basename(calib_path), "profile_name": prof_name, "profile_ranges": prof,
           "variant": cal.get("variant", "base"), "loss": cal["loss"], "g": g, "n": n,
           "profile": dict(cdr_total_mean=float(base_tot.mean()), cdr_ad_mean=float(cad.mean()),
                           eps_present=float((ppc["eps"] > 0).mean()), tau_pos=float(taupos.mean()), hi_tau=float(hitau.mean()),
                           N_EC=float(stc["N"][:, IX["EC"]].mean()), N_HC=float(stc["N"][:, IX["HC"]].mean()),
                           S_PCC=float(stc["S"][:, IX["PCC"]].mean()), stereo_share=float(stereo.mean())),
           "survivor_insult_composition": comp,
           "note": "No side effects (ARIA) are modeled and APOE genotype has no effect in this simulation: "
                   "treatment scenarios show modeled benefit only, not harms."}
    groups = {"all": np.ones(n, bool), "stereo": stereo, "tau_neg": ~taupos, "tau_pos_low": taupos & ~hitau, "tau_high": hitau}
    decomp = {}
    for gname, msk in groups.items():
        if msk.sum() < 30:
            continue
        c = cad[msk]
        D = dict(n=int(msk.sum()), cdr_ad_mean=float(c.mean()))
        for meth in ("remainder_N", "shapley_N", "prop_N"):
            D[f"share_neurons_{meth}"] = float(dec[meth][msk].sum() / max(c.sum(), 1e-9))
        decomp[gname] = D
    out["decomposition"] = decomp
    arrays = {"cad": cad, "eps": ppc["eps"], "taupos": taupos, "hitau": hitau, "stereo": stereo,
              "remainder_N": dec["remainder_N"], "prop_N": dec["prop_N"], "shapley_N": dec["shapley_N"],
              "N_EC": stc["N"][:, IX["EC"]].astype(np.float32), "N_HC": stc["N"][:, IX["HC"]].astype(np.float32)}
    out["scenarios"] = {}
    for key, sc in SCENARIOS.items():
        o = project(stc, ppc, g, years, dt=0.05, rec=0.25, scen=sc["scen"], seed=5, keep=False)
        c = o["cdr"] if key == "fix_nonAD" else o["cdr_ad"]
        b = base_tot if key == "fix_nonAD" else cad
        arrays[f"traj_{key}"] = c.astype(np.float32)
        out["scenarios"][key] = dict(label=sc["label"], measure="total CDR-SB" if key == "fix_nonAD" else "Alzheimer part of CDR-SB",
                                     **summarize(c, o["t"], b))
        out["t"] = o["t"].tolist()
    win = {}
    for s0 in WINDOW_STARTS:
        row = {}
        for bridge in ("ab_now", "none"):
            o = project(stc, ppc, g, max(s0, 0.25), dt=0.05, rec=0.25, scen=SCENARIOS[bridge]["scen"], seed=5, keep=True)
            k = int(round(s0 / 0.25))
            Nk, Sk = o["N"][:, k], o["S"][:, k]
            st_k = {**stc, "N": Nk, "S": Sk}
            cad_k = cognition(st_k, ppc, g, include_eps=False)
            best_model = cognition(st_k, ppc, g, include_eps=False, S=np.ones_like(Sk))
            D_N, D_S = deficits(Nk, Sk)
            best_lin = cad_k * D_N / np.maximum(D_N + D_S, 1e-9)
            row[bridge] = dict(cad_median=float(np.median(cad_k)), best_model_median=float(np.median(best_model)),
                               best_lin_median=float(np.median(best_lin)))
            arrays[f"win_{bridge}_{s0}_cad"] = cad_k.astype(np.float32)
            arrays[f"win_{bridge}_{s0}_bestmodel"] = best_model.astype(np.float32)
            arrays[f"win_{bridge}_{s0}_bestlin"] = best_lin.astype(np.float32)
        win[str(s0)] = row
    out["window"] = win
    if out_path:
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        json.dump(out, open(out_path, "w"), indent=1)
        np.savez_compressed(out_path.replace(".json", ".npz"), **arrays)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--calib", required=True)
    ap.add_argument("--profile", default="mci_moderate_amyloid_70s")
    ap.add_argument("--profiles", default=os.path.join(os.path.dirname(__file__), "..", "profiles", "profiles.yaml"))
    ap.add_argument("--patient", default=None, help="local YAML in patients/ (git-ignored); never commit it")
    ap.add_argument("--P", type=int, default=150000)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    name, prof = load_profile(a)
    member = os.path.basename(a.calib).replace("calib_", "").replace(".json", "")
    out = a.out or os.path.join("results", f"scen_{name}_{member}.json")
    res = run(a.calib, name, prof, a.P, out_path=out)
    print(json.dumps({k: v for k, v in res["decomposition"].get("all", {}).items()}, indent=1))
    for k, r in res["scenarios"].items():
        print(f"  {k:22s} y1 {r['y1_median']:.2f} y3 {r['y3_median']:.2f} y5 {r['y5_median']:.2f} | to CDR-SB 4.5: "
              f"{r['years_to_mild_dementia_median']:.1f}y | better than today at y1 {r['better_y1']:.2f}")
