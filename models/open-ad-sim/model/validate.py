"""
Out-of-sample checks: quantities NOT used in calibration, compared with published data (v2).
  V1 donanemab, 3 years, early start vs untreated: CDR-SB -1.2 (95% CI -1.7 to -0.7)
     [TRAILBLAZER-ALZ 2 long-term extension vs weighted ADNI external control; grade C: open-label, external control, ~half dropout]
  V2 lecanemab continuous, 4 years, treated vs untreated: 1.75 (vs ADNI) to 2.17 (vs BioFINDER) CDR-SB points, no CI published
     [Clarity AD open-label extension vs external natural-history cohorts; grade C]
  V3 amyloid-positive, tau-PET-positive MCI: dementia within 5 years 70% (95% CI 59-81%)
     [Moscoso et al., JAMA 2025, pooled cohorts; dementia approximated as CDR-SB >= 4.5; grade B: observational cohorts]
     v5 FAILED this check (0.92-0.98); since v6 it is a calibration target and is reported here only as in-sample
  Descriptive only (no published target or already used in calibration): early vs delayed start at 3 years;
     'true improvement' at 12 months; years of amyloid positivity at the MCI stage.
Scoring: z = (model - target) / tolerance; V1 tolerance = CI half-width / 1.96 = 0.26; V2 tolerance = 0.4 (assumed, no CI; target = midpoint 1.96).
Usage: python3 validate.py calib_X.json [P]
"""
import numpy as np, json, sys
from brain_sim import *
from calibrate import hist_cdr, first_idx, TB_BASE, CL_BASE, NOISE_SD

OOS = {"V1_dona_3y_vs_untreated": (-1.2, 0.26), "V2_lec_diff_4.0y": (1.96, 0.40)}   # V3 became a calibration target in v6


def main(path, P=8000, seed=33):
    cal = json.load(open(path))
    require_variant(cal, path)
    g = cal["g"]
    z = sample_people(P, seed=seed)
    pp = realize(z, g)
    rng = np.random.default_rng(seed)
    ages, hist = run_history(pp, g, 48.0, 92.0, dt=0.1, rec=0.5)
    cdr = hist_cdr(hist, pp, g)
    A = hist["A"]
    taupos, hitau = tau_status_arr(hist["T"], g)
    agemask = (ages >= 55)[None, :]
    out = {}
    # TB-like enrollment (amyloid >= 37 CL, tau-positive, baseline CDR-SB distribution of the trial)
    thr = np.clip(rng.normal(*TB_BASE, P), 1.0, 9.0)
    i = first_idx((cdr >= thr[:, None]) & (A > 37) & taupos & agemask & (ages <= 85)[None, :]); ok = i >= 0
    st0 = state_at(hist, np.where(ok, i, 0), ages); st0 = {k: v[ok] for k, v in st0.items()}; ppe = subset(pp, ok)
    hi = hitau[np.arange(P)[ok], i[ok]]
    pbo = project(st0, ppe, g, 3.0, dt=0.05, rec=0.25, scen={}, seed=3)
    early = project(st0, ppe, g, 3.0, dt=0.05, rec=0.25, scen={"ab": "donanemab"}, seed=3)
    delayed = project(st0, ppe, g, 3.0, dt=0.05, rec=0.25, scen={"ab": "donanemab", "ab_start": 76 / 52}, seed=3)
    k3 = int(round(3.0 / 0.25)); k1 = 4
    out["V1_dona_3y_vs_untreated"] = float(early["cdr"][:, k3].mean() - pbo["cdr"][:, k3].mean())
    out["desc_dona_3y_early_vs_delayed"] = float(early["cdr"][:, k3].mean() - delayed["cdr"][:, k3].mean())
    c0 = pbo["cdr"][:, 0]
    lo = ~hi
    out["desc_true_improved_12m_dona_lo"] = float((early["cdr"][lo, k1] < c0[lo] - 0.25).mean())
    out["desc_true_improved_12m_pbo_lo"] = float((pbo["cdr"][lo, k1] < c0[lo] - 0.25).mean())
    n0 = rng.normal(0, NOISE_SD, c0.shape); n1 = rng.normal(0, NOISE_SD, c0.shape)
    out["desc_measured_improved_12m_dona_lo"] = float(((early["cdr"][lo, k1] + n1[lo]) - (c0[lo] + n0[lo]) <= -0.5).mean())
    # Clarity-like, lecanemab continuous for 4 years
    thr = np.clip(rng.normal(*CL_BASE, P), 0.5, 8.0)
    i = first_idx((cdr >= thr[:, None]) & (A > 30) & agemask & (ages <= 85)[None, :]); ok = i >= 0
    st0 = state_at(hist, np.where(ok, i, 0), ages); st0 = {k: v[ok] for k, v in st0.items()}; ppe = subset(pp, ok)
    pbo = project(st0, ppe, g, 4.0, dt=0.05, rec=0.5, scen={}, seed=4)
    lec = project(st0, ppe, g, 4.0, dt=0.05, rec=0.5, scen={"ab": "lecanemab"}, seed=4)
    for yr in (1.5, 3.0, 4.0):
        k = int(round(yr / 0.5))
        out[f"V2_lec_diff_{yr}y"] = float(pbo["cdr"][:, k].mean() - lec["cdr"][:, k].mean())
    # V3: amyloid-positive, tau-PET-positive MCI -> dementia (CDR-SB >= 4.5) within 5 years: 70% (59-81%) (Moscoso 2025, JAMA)
    thr = rng.uniform(0.5, 3.5, P)
    i = first_idx((cdr >= thr[:, None]) & (cdr < 4.5) & (A > 30) & taupos & agemask & (ages <= 85)[None, :])
    ok = (i >= 0) & (i + 10 < len(ages))
    out["V3_ATpos_mci_dementia_5y"] = float((cdr[np.arange(P)[ok], i[ok] + 10] >= 4.5).mean())
    i = first_idx((cdr >= thr[:, None]) & (cdr < 4.5) & (A > 30) & ~taupos & agemask & (ages <= 85)[None, :])
    ok = (i >= 0) & (i + 10 < len(ages))
    out["desc_ATneg_mci_dementia_5y"] = float((cdr[np.arange(P)[ok], i[ok] + 10] >= 4.5).mean())
    # amyloid chronicity at MCI (descriptive)
    i = first_idx((cdr >= 1.5) & (A > 30) & agemask); ok = i >= 0
    pos = first_idx(A >= 20)
    both = ok & (pos >= 0)
    out["desc_years_amyloid_pos_at_mci_median"] = float(np.median(ages[i[both]] - ages[pos[both]]))
    out["desc_age_at_mci_median"] = float(np.median(ages[i[ok]]))
    zs = {k: (out[k] - v) / s for k, (v, s) in OOS.items()}
    out["oos_z"] = zs
    out["oos_loss"] = float(sum(v ** 2 for v in zs.values()))
    print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    res = main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8000)
    json.dump(res, open(sys.argv[1].replace("calib_", "valid_"), "w"), indent=1)
