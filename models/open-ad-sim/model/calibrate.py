"""
Calibration of the open-ad-sim disease model against published human data (v6).
Usage: python3 calibrate.py <rho> <P> <n_random> <n_nm> [start.json]
Targets (value, tolerance) are in TARGETS and documented in the dossier.
"""
import numpy as np, json, sys, time, os
from brain_sim import *
OUT_DIR = os.environ.get("ADSIM_RESULTS", "results")

TARGETS = {
    # ---- pathology at the MCI stage (CDR 0.5; evaluated at a random CDR-SB between 0.5 and 3.5, amyloid-positive) ----
    "N_EC_mci":   (0.66, 0.10),   # EC neurons -32 to -35% at CDR 0.5 (Gomez-Isla 1996; Price 2001); von Gunten 2006 much less -> wide
    "N_HC_mci":   (0.65, 0.10),   # CA1 -46% (Price 2001), -26% (von Gunten 2006), -48% AD mixed (West 2004)
    "S_EC_mci":   (0.92, 0.06),   # EC volume x FDG ~ neuron loss alone -> survivors near-normal
    "S_HC_mci":   (0.97, 0.05),   # CA1 synapses only -18% while neurons -46%: survivors compensate (Scheff 2007; DeKosky 2002)
    "N_PCC_mci":  (0.98, 0.02),   # no neuron loss measured in PCC at MCI
    "S_PCC_mci":  (0.85, 0.05),   # FDG -11 to -22%, SV2A -7%: hypometabolism exceeds atrophy (Chetelat 2008; La Joie 2012)
    "S_IT_mci":   (0.82, 0.10),   # inferior temporal synapses -36% at aMCI (Scheff 2011); FDG temporal -11% (Chen 2019)
    "S_PFC_mci":  (0.92, 0.06),   # frontal: synaptophysin -25% but active compensation; smallest FDG/atrophy W-scores
    "disc_share_PCC": (0.30, 0.20),  # share of PCC dysfunction from lost hippocampal input (Villain 2008/2010 large; Strom 2022 small)
    "N_EC_mild":  (0.45, 0.10),   # EC at mild dementia (CDR 1)
    "S_HC_mild":  (0.87, 0.07),   # hippocampal survivors decompensate by mild AD (CA1 synapses -55%, Scheff 2007)
    # ---- tau staging ----
    "tau_pos_mci": (0.58, 0.08),  # temporal tau-PET positive among amyloid+ MCI (Ossenkoppele 2025: 58.1%)
    "hi_tau_TB":   (0.32, 0.07),  # high-tau share of TRAILBLAZER-ALZ 2 (552/1736)
    # ---- progression ----
    "dCDR_pbo_TB_lo": (1.88, 0.25),  # TB-ALZ 2 placebo, low/medium tau, 76 wk
    "dCDR_pbo_TB_hi": (3.56, 0.7),   # derived (n-weighted) from combined 2.42; FDA: difference -0.7 (-1.2,-0.2)
    "dCDR_pbo_CL":    (1.66, 0.25),  # Clarity AD placebo, 18 mo
    "prog3_AN_mci":   (0.59, 0.08),  # A+N+ MCI -> dementia at 3 yr (Vos 2015)
    "prog5_ATpos_mci": (0.70, 0.056), # A+T+ MCI -> dementia within 5 yr: 70% (59-81%) (Moscoso 2025, JAMA). Added in v6 after v5
                                      # failed it out of sample (0.92-0.98); no longer an independent check
    "prog5_ATneg_mci": (0.35, 0.12),  # A+T- MCI: derived [extrapolated] from meta-analysis odds ratios vs A-T- (A+T+ 11.6, A+T- 2.73;
                                      # Huszar 2024, CSF-defined T) applied to the 70% A+T+ risk -> ~35%; wide tolerance
    "chron_dem": (13.6, 2.5),        # years from amyloid positivity to dementia, ADNI median 13.6 (Betthauser 2022)
    "nodecl_pbo_TB_lo": (0.29, 0.06),  # TB-ALZ 2: no CDR-SB worsening at 52 wk, low/medium tau, placebo (with measurement noise)
    "nodecl_act_TB_lo": (0.47, 0.06),  # ... donanemab
    # ---- antibody effect ----
    "slow_TB_lo": (0.36, 0.06),
    "slow_TB_hi": (0.20, 0.08),
    "slow_CL":    (0.27, 0.05),
    "tau_slow_neo_TB": (0.05, 0.12),   # TB-ALZ 2: no detectable slowing of frontal/parietal/lateral temporal tau at 76 wk
    "dS_PCC_ab": (0.0, 0.04),          # no FDG recovery shown after amyloid removal (gantenerumab DIAN-TU 4 y; no lecanemab/donanemab FDG data)
    "S_PCC_ApTn_CU": (0.97, 0.03),      # amyloid+ but tau-negative, cognitively unimpaired: little or no PCC hypometabolism;
                                        # hypometabolism tracks tau (spatial r .55-.76) far more than amyloid (.22-.28) (Strom 2022)
}
NOISE_SD = 0.85          # single-visit CDR-SB measurement noise (ICC 0.68-0.83 with baseline SD ~2 -> SEM ~0.8-1.1)
TB_BASE = (3.9, 2.1)     # TRAILBLAZER-ALZ 2 baseline CDR-SB, combined population (Sims 2023)
CL_BASE = (3.2, 1.3)     # Clarity AD baseline CDR-SB


def hist_cdr(hist, pp, g):
    NS = hist["N"].astype(float) * hist["S"].astype(float)
    D = 1 - NS @ W_COG
    c = np.minimum(g["a_cdr"] * pp["fres"][:, None] * np.clip(D - pp["R"][:, None], 0, None) ** g["q"], 18.0)
    return c + pp["eps"][:, None]


def first_idx(ok):
    has = ok.any(1)
    return np.where(has, ok.argmax(1), -1)


NEO_TB = [IX[r] for r in ["LT", "IP", "PFC", "OCC"]]


def trial(st0, pp, g, years, kind, seed, tau=False):
    pbo = project(st0, pp, g, years, dt=0.05, rec=years, scen={}, seed=seed)
    act = project(st0, pp, g, years, dt=0.05, rec=years, scen={"ab": kind}, seed=seed)
    c0 = pbo["cdr"][:, 0]
    if tau:
        t0 = st0["T"][:, NEO_TB].mean(1)
        dS = act["final"]["S"][:, IX["PCC"]] - pbo["final"]["S"][:, IX["PCC"]]
        return (pbo["cdr"][:, -1] - c0, act["cdr"][:, -1] - c0,
                pbo["final"]["T"][:, NEO_TB].mean(1) - t0, act["final"]["T"][:, NEO_TB].mean(1) - t0, dS)
    return pbo["cdr"][:, -1] - c0, act["cdr"][:, -1] - c0


def evaluate(g, z, seed=7):
    pp = realize(z, g)
    rng = np.random.default_rng(seed)
    ages, hist = run_history(pp, g, 48.0, 92.0, dt=0.1, rec=0.5)
    P = len(pp["rA"])
    cdr = hist_cdr(hist, pp, g)
    A = hist["A"]
    taupos, hitau = tau_status_arr(hist["T"], g)
    agemask = (ages >= 55)[None, :]
    m = {}
    thr = rng.uniform(0.5, 3.5, P)
    i = first_idx((cdr >= thr[:, None]) & (A > 30) & agemask); ok = i >= 0; r = np.arange(P)[ok]; ii = i[ok]
    Nm = hist["N"][r, ii].astype(float); Sm = hist["S"][r, ii].astype(float); Tm = hist["T"][r, ii].astype(float)
    for reg in ("EC", "HC", "PCC"):
        m[f"N_{reg}_mci"] = Nm[:, IX[reg]].mean()
    for reg in ("EC", "HC", "PCC", "IT", "PFC"):
        m[f"S_{reg}_mci"] = Sm[:, IX[reg]].mean()
    Din = ((1 - Nm) @ WN.T)[:, IX["PCC"]]
    loc = g["sT"] * pp["fsT"][r] * Tm[:, IX["PCC"]] + g["sA"] * AMY[IX["PCC"]] * np.clip(A[r, ii], 0, None) / 100.0
    m["disc_share_PCC"] = float((g["sD"] * Din).sum() / max((g["sD"] * Din + loc).sum(), 1e-9))
    m["age_mci"] = ages[ii].mean(); m["CL_mci"] = A[r, ii].mean(); m["n_mci"] = ok.sum()
    # amyloid-positive, tau-negative, cognitively unimpaired (CDR-SB < 0.5), age 65-80: PCC survivor function
    cu = (cdr < 0.5) & (A > 40) & (~taupos) & ((ages >= 65) & (ages <= 80))[None, :]
    m["S_PCC_ApTn_CU"] = float(hist["S"][:, :, IX["PCC"]][cu].mean()) if cu.any() else 1.0
    thr = rng.uniform(4.5, 9.0, P)
    i = first_idx((cdr >= thr[:, None]) & (A > 30) & agemask); ok = i >= 0
    m["N_EC_mild"] = hist["N"][np.arange(P)[ok], i[ok], IX["EC"]].mean() if ok.any() else 1.0
    m["S_HC_mild"] = hist["S"][np.arange(P)[ok], i[ok], IX["HC"]].mean() if ok.any() else 1.0
    thr = rng.uniform(0.5, 4.0, P)
    i = first_idx((cdr >= thr[:, None]) & (A > 30) & agemask); ok = i >= 0
    m["tau_pos_mci"] = taupos[np.arange(P)[ok], i[ok]].mean()
    thr = rng.uniform(0.5, 3.0, P)
    i = first_idx((cdr >= thr[:, None]) & (cdr < 4.5) & (A > 30) & (hist["N"][:, :, IX["HC"]] < 0.85) & agemask)
    ok = (i >= 0) & (i + 6 < len(ages))
    m["prog3_AN_mci"] = (cdr[np.arange(P)[ok], i[ok] + 6] >= 4.5).mean() if ok.any() else 1.0
    # TRAILBLAZER-ALZ 2-like trial: amyloid >= 37 CL, tau-PET positive, CDR-SB at enrollment ~ baseline distribution
    thr = np.clip(rng.normal(*TB_BASE, P), 1.0, 9.0)
    i = first_idx((cdr >= thr[:, None]) & (A > 37) & taupos & agemask & (ages <= 85)[None, :]); ok = i >= 0
    st0 = state_at(hist, np.where(ok, i, 0), ages); st0 = {k: v[ok] for k, v in st0.items()}; ppe = subset(pp, ok)
    hi = hitau[np.arange(P)[ok], i[ok]]
    m["hi_tau_TB"] = hi.mean(); m["age_TB"] = ages[i[ok]].mean(); m["n_TB"] = ok.sum()
    dp, da, tp, ta, dS = trial(st0, ppe, g, 76 / 52, "donanemab", seed, tau=True)
    m["tau_slow_neo_TB"] = 1 - ta[~hi].mean() / max(tp[~hi].mean(), 1e-6)
    m["dS_PCC_ab"] = float(dS[~hi].mean())
    for lab, msk in (("lo", ~hi), ("hi", hi)):
        m[f"dCDR_pbo_TB_{lab}"] = dp[msk].mean() if msk.any() else 0.0
        m[f"dCDR_act_TB_{lab}"] = da[msk].mean() if msk.any() else 0.0
        m[f"slow_TB_{lab}"] = 1 - da[msk].mean() / dp[msk].mean() if msk.any() else 0.0
    m["dCDR_pbo_TB_all"] = dp.mean(); m["slow_TB_all"] = 1 - da.mean() / dp.mean()
    # 'no decline' at ~12 months in low/medium tau, with single-visit measurement noise (TB-ALZ 2: 29% placebo vs 47% donanemab)
    dp1, da1 = trial(st0, ppe, g, 1.0, "donanemab", seed + 2)
    nrng = np.random.default_rng(seed + 3)
    e0 = nrng.normal(0, NOISE_SD, dp1.shape); e1 = nrng.normal(0, NOISE_SD, dp1.shape); e2 = nrng.normal(0, NOISE_SD, dp1.shape)
    lo = ~hi
    m["nodecl_pbo_TB_lo"] = float(((dp1 + e1 - e0)[lo] <= 0.25).mean())     # CDR-SB moves in 0.5 steps: <=0.25 rounds to no worsening
    m["nodecl_act_TB_lo"] = float(((da1 + e2 - e0)[lo] <= 0.25).mean())
    # Clarity AD-like trial: amyloid-positive, CDR-SB ~ baseline distribution, lecanemab continuous
    thr = np.clip(rng.normal(*CL_BASE, P), 0.5, 8.0)
    i = first_idx((cdr >= thr[:, None]) & (A > 30) & agemask & (ages <= 85)[None, :]); ok = i >= 0
    st0 = state_at(hist, np.where(ok, i, 0), ages); st0 = {k: v[ok] for k, v in st0.items()}; ppe = subset(pp, ok)
    dp, da = trial(st0, ppe, g, 1.5, "lecanemab", seed + 1)
    m["dCDR_pbo_CL"] = dp.mean(); m["dCDR_act_CL"] = da.mean(); m["slow_CL"] = 1 - da.mean() / dp.mean()
    m["age_CL"] = ages[i[ok]].mean()
    # amyloid chronicity: years from first amyloid positivity (>=20 CL, after age 48) to dementia (CDR-SB >= 4.5)
    pos = first_idx(A >= 20); dem = first_idx((cdr >= 4.5) & agemask)
    okc = (pos > 0) & (dem > pos)
    m["chron_dem"] = float(np.median(ages[dem[okc]] - ages[pos[okc]])) if okc.sum() > 50 else 30.0
    # A+T+ (and, descriptively, A+T-) MCI -> dementia (CDR-SB >= 4.5) within 5 years; separate generator keeps earlier draws unchanged
    r2 = np.random.default_rng(seed + 9)
    thr = r2.uniform(0.5, 3.5, P)
    for lab, tmask in (("prog5_ATpos_mci", taupos), ("prog5_ATneg_mci", ~taupos)):
        i = first_idx((cdr >= thr[:, None]) & (cdr < 4.5) & (A > 30) & tmask & agemask & (ages <= 85)[None, :])
        ok = (i >= 0) & (i + 10 < len(ages))
        m[lab] = float((cdr[np.arange(P)[ok], i[ok] + 10] >= 4.5).mean()) if ok.any() else 1.0
    loss = sum(((m[k] - v) / s) ** 2 for k, (v, s) in TARGETS.items())
    for k in ("dCDR_act_TB_lo", "dCDR_act_CL"):
        if m[k] < 0.2:
            loss += ((0.2 - m[k]) / 0.1) ** 2
    if not (68 <= m["age_mci"] <= 80):          # realistic age at MCI in amyloid+ people
        loss += ((m["age_mci"] - np.clip(m["age_mci"], 68, 80)) / 2) ** 2
    if not (60 <= m["CL_mci"] <= 110):
        loss += ((m["CL_mci"] - np.clip(m["CL_mci"], 60, 110)) / 10) ** 2
    m["loss"] = loss
    return m


def report(m):
    lines = []
    for k, (v, s) in TARGETS.items():
        lines.append(f"  {k:16s} model {m[k]:7.3f}  target {v:6.3f} +/- {s:.3f}   z={(m[k]-v)/s:+.2f}")
    extra = ["age_mci", "CL_mci", "age_TB", "n_TB", "age_CL", "dCDR_act_TB_lo", "dCDR_act_TB_hi", "dCDR_act_CL",
             "dCDR_pbo_TB_all", "slow_TB_all", "nodecl_pbo_TB_lo", "nodecl_act_TB_lo", "prog5_ATneg_mci"]
    lines.append("  " + "  ".join(f"{k}={m[k]:.2f}" for k in extra))
    lines.append(f"  LOSS = {m['loss']:.2f}")
    return "\n".join(lines)


PARAM_KEYS = ["k0", "kA", "kauto", "b0", "bA", "delta", "sT", "sA", "sD", "a_cdr", "R0", "q", "het", "sdR", "pN", "thr_pos", "thr_hi",
              "hetK", "sdres"]
BOUNDS = {"k0": (0.03, 0.3), "kA": (0.02, 0.5), "kauto": (0.05, 2.0), "b0": (0.001, 0.08), "bA": (0.005, 0.3),
          "delta": (0.03, 0.6), "sT": (0.01, 1.0), "sA": (0.02, 1.0), "sD": (0.01, 1.0), "a_cdr": (20, 400),
          "R0": (0.005, 0.35), "q": (1.0, 3.5), "het": (0.15, 1.1), "sdR": (0.01, 0.15),
          "pN": (1.0, 4.0), "thr_pos": (0.05, 0.5), "thr_hi": (0.05, 0.5), "hetK": (0.05, 1.2), "sdres": (0.05, 1.0)}


FIXED = {}      # parameters held fixed for a structural variant (e.g. mapping convexity q)


def active_keys():
    return [k for k in PARAM_KEYS if k not in FIXED]


def pack(g):
    return np.log([g[k] for k in active_keys()])


def unpack(x, base):
    g = dict(base)
    for k, v in zip(active_keys(), np.exp(x)):
        lo, hi = BOUNDS[k]
        g[k] = float(np.clip(v, lo, hi))
    g.update(FIXED)
    return g


if __name__ == "__main__":
    from scipy.optimize import minimize
    rho = float(sys.argv[1]); P = int(sys.argv[2]); n_rand = int(sys.argv[3]); n_nm = int(sys.argv[4])
    start = sys.argv[5] if len(sys.argv) > 5 else None
    tag = sys.argv[6] if len(sys.argv) > 6 else f"rho{rho}"
    if len(sys.argv) > 7 and sys.argv[7]:
        for kv in sys.argv[7].split(","):
            k, v = kv.split("="); FIXED[k] = float(v)
    base = dict(DEFAULT_G); base["rho"] = rho
    if start and start != "none":
        base.update(json.load(open(start))["g"]); base["rho"] = rho
    base.update(FIXED)
    z = sample_people(P, seed=11)
    best = {"loss": np.inf}
    t0 = time.time()

    def consider(g, label=""):
        try:
            m = evaluate(g, z)
        except Exception as e:
            return 1e6
        if m["loss"] < best["loss"]:
            best.update(loss=m["loss"], g=g, m=m)
            json.dump({"g": g, "loss": m["loss"], "variant": VARIANT, "fixed": FIXED, "m": {k: float(v) for k, v in m.items()}},
                      open(os.path.join(OUT_DIR, f"calib_{tag}.json"), "w"), indent=1)
        return m["loss"]

    consider(base)
    print(f"[{tag}] start loss {best['loss']:.2f}", flush=True)
    rng = np.random.default_rng(int(rho * 1000) + 5)
    x0 = pack(base)
    for j in range(n_rand):           # local random search in log space around the current best
        scale = 0.5 if j < n_rand // 2 else 0.25
        xb = pack(best["g"])
        x = xb + scale * rng.standard_normal(len(xb))
        consider(unpack(x, base))
        if (j + 1) % 25 == 0:
            print(f"[{tag}] random {j+1}/{n_rand} best {best['loss']:.2f}  ({time.time()-t0:.0f}s)", flush=True)
    it = [0]

    def f(x):
        it[0] += 1
        L = consider(unpack(x, base))
        if it[0] % 50 == 0:
            print(f"[{tag}] NM {it[0]} best {best['loss']:.2f}  ({time.time()-t0:.0f}s)", flush=True)
        return L

    if n_nm > 0:
        minimize(f, pack(best["g"]), method="Nelder-Mead",
                 options={"maxfev": n_nm, "xatol": 1e-3, "fatol": 1e-3, "adaptive": True})
    print(f"[{tag}] FINAL loss {best['loss']:.2f}", flush=True)
    print(json.dumps(best["g"], indent=1))
    print(report(best["m"]), flush=True)
