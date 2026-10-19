"""
Write docs/CALIBRATION.md and docs/VALIDATION.md from the calibration targets and the ensemble members' fit files.
Usage: python3 model/make_docs.py results/calib_A.json results/calib_B.json ...
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from calibrate import TARGETS, NOISE_SD, TB_BASE, CL_BASE

SOURCES = {
    "N_EC_mci": "Entorhinal neurons about one-third fewer at CDR 0.5 (Gómez-Isla 1996; Price 2001); smaller losses in von Gunten 2006, hence a wide tolerance",
    "N_HC_mci": "CA1 neurons −46% (Price 2001), −26% (von Gunten 2006); −48% in mixed AD (West 2004)",
    "S_EC_mci": "Entorhinal volume and FDG declines are explained by neuron loss alone, so survivors near normal [extrapolated]",
    "S_HC_mci": "CA1 synapses only −18% in MCI while neurons are −46%: survivors compensate (Scheff 2007; DeKosky 2002)",
    "N_PCC_mci": "No measurable neuron loss in posterior cingulate/precuneus at MCI",
    "S_PCC_mci": "FDG −11 to −22% and SV2A −7%: hypometabolism exceeds atrophy (Chételat 2008; La Joie 2012)",
    "S_IT_mci": "Inferior temporal synapses −36% in amnestic MCI (Scheff 2011); temporal FDG −11% (Chen 2019)",
    "S_PFC_mci": "Frontal synaptophysin −25% with compensation; smallest FDG/atrophy deviations",
    "disc_share_PCC": "Share of PCC dysfunction caused by lost hippocampal input: large in Villain 2008/2010, small in Strom 2022 — wide tolerance",
    "N_EC_mild": "Entorhinal neurons at mild dementia (CDR 1) (Gómez-Isla 1996)",
    "S_HC_mild": "Hippocampal survivors decompensate by mild AD: CA1 synapses −55% (Scheff 2007)",
    "tau_pos_mci": "Temporal tau-PET positive among amyloid-positive MCI: 58.1% (Ossenkoppele 2025)",
    "hi_tau_TB": "High-tau share of TRAILBLAZER-ALZ 2 (552 of 1736; Sims 2023)",
    "dCDR_pbo_TB_lo": "TRAILBLAZER-ALZ 2 placebo, low/medium tau, CDR-SB change at 76 weeks (Sims 2023)",
    "dCDR_pbo_TB_hi": "TRAILBLAZER-ALZ 2 placebo, high tau: derived (n-weighted) from the combined 2.42 [extrapolated]",
    "dCDR_pbo_CL": "Clarity AD placebo, CDR-SB change at 18 months (van Dyck 2023)",
    "prog3_AN_mci": "Amyloid-positive, neurodegeneration-positive MCI progressing to dementia within 3 years (Vos 2015)",
    "chron_dem": "Years from amyloid positivity to dementia, ADNI median (Betthauser 2022)",
    "prog5_ATpos_mci": "Amyloid- and tau-PET-positive MCI reaching dementia within 5 years: 70% (95% CI 59–81%) (Moscoso 2025, JAMA). Added in v6 after v5 failed it out of sample",
    "prog5_ATneg_mci": "Amyloid-positive, tau-negative MCI reaching dementia within 5 years: ~35% [extrapolated] from meta-analysis odds ratios vs A−T− (A+T+ 11.6, A+T− 2.73; Huszár 2024, CSF-defined tau) applied to the 70% A+T+ risk; wide tolerance",
    "nodecl_pbo_TB_lo": "No CDR-SB worsening at 52 weeks, low/medium tau, placebo (TRAILBLAZER-ALZ 2); modeled with measurement noise",
    "nodecl_act_TB_lo": "Same, donanemab arm",
    "slow_TB_lo": "Donanemab slowing of CDR-SB decline, low/medium tau, 76 weeks: 36% (Sims 2023)",
    "slow_TB_hi": "Donanemab slowing, high tau: difference −0.7 (−1.2 to −0.2) over a derived placebo decline [extrapolated]",
    "slow_CL": "Lecanemab slowing of CDR-SB decline at 18 months: 27% (van Dyck 2023)",
    "tau_slow_neo_TB": "No detectable slowing of frontal/parietal/lateral temporal tau-PET accumulation at 76 weeks (TRAILBLAZER-ALZ 2)",
    "dS_PCC_ab": "No FDG recovery shown after amyloid removal (gantenerumab, DIAN-TU, 4 years); no lecanemab/donanemab FDG data",
    "S_PCC_ApTn_CU": "Amyloid-positive, tau-negative, cognitively unimpaired people show little PCC hypometabolism; hypometabolism tracks tau (spatial r 0.55–0.76) far more than amyloid (0.22–0.28) (Strom 2022)",
}


def main(paths):
    mem = [json.load(open(p)) for p in paths]
    names = [os.path.basename(p).replace("calib_", "").replace(".json", "") for p in paths]
    L = ["# Calibration", "",
         "Each ensemble member is fitted to the same published targets. Loss = sum of squared z-scores, z = (model − target) / tolerance.",
         f"Measurement noise on a single CDR-SB visit: SD {NOISE_SD} (test–retest). Trial-like cohorts are enrolled at baseline CDR-SB "
         f"~N{TB_BASE} (TRAILBLAZER-ALZ 2) and ~N{CL_BASE} (Clarity AD).", "",
         "Tolerances express how far apart published sources are, not statistical standard errors.", "",
         "| Target | Value | Tolerance | Source | " + " | ".join(f"z ({n})" for n in names) + " |",
         "|---|---|---|---|" + "---|" * len(names)]
    for k, (v, s) in TARGETS.items():
        zs = []
        for m in mem:
            mv = m["m"].get(k)
            zs.append(f"{(mv - v) / s:+.1f}" if mv is not None else "—")
        L.append(f"| `{k}` | {v} | {s} | {SOURCES.get(k, '')} | " + " | ".join(zs) + " |")
    L += ["", "| Member | Variant | Fixed | Recovery capacity rho | Loss |", "|---|---|---|---|---|"]
    for n, m in zip(names, mem):
        L.append(f"| {n} | {m.get('variant', 'base')} | {m.get('fixed', {})} | {m['g']['rho']} | {m['loss']:.1f} |")
    L += ["", "Fitted parameters:", "", "| Parameter | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    for k in mem[0]["g"]:
        L.append(f"| `{k}` | " + " | ".join(f"{m['g'][k]:.4g}" for m in mem) + " |")
    open(os.path.join("docs", "CALIBRATION.md"), "w").write("\n".join(L) + "\n")
    V = ["# Validation (out of sample)", "",
         "Quantities never used in fitting, compared with published long-term data. The two drug comparisons are open-label extensions against "
         "external natural-history controls (evidence grade C: no randomized control after 18 months, about half of participants dropped out); "
         "the progression check comes from pooled observational cohorts, with dementia approximated as CDR-SB ≥ 4.5. Version 5 failed that "
         "progression check (92–98% vs 70%), so version 6 added person-to-person variation in tau propagation and resilience and was refit "
         "with it as a target; it is shown here for completeness but is no longer an independent test.", "",
         "| Check | Published | Tolerance used | " + " | ".join(names) + " |", "|---|---|---|" + "---|" * len(names)]
    vals = []
    for p in paths:
        vp = p.replace("calib_", "valid_")
        vals.append(json.load(open(vp)) if os.path.exists(vp) else {})
    V.append("| Donanemab early start vs untreated, CDR-SB at 3 years | −1.2 (95% CI −1.7 to −0.7), TRAILBLAZER-ALZ 2 extension vs ADNI | 0.26 | "
             + " | ".join(f"{v.get('V1_dona_3y_vs_untreated', float('nan')):+.2f}" for v in vals) + " |")
    V.append("| Lecanemab continuous vs untreated, CDR-SB at 4 years | 1.75 (vs ADNI) to 2.17 (vs BioFINDER), Clarity AD extension | 0.40 (assumed; no CI) | "
             + " | ".join(f"{v.get('V2_lec_diff_4.0y', float('nan')):.2f}" for v in vals) + " |")
    V.append("| (in-sample since v6) Amyloid- and tau-PET-positive MCI reaching dementia (CDR-SB ≥ 4.5) within 5 years | 70% (95% CI 59–81%), Moscoso 2025, pooled cohorts | 0.056 | "
             + " | ".join(f"{v.get('V3_ATpos_mci_dementia_5y', float('nan')):.2f}" for v in vals) + " |")
    V.append("| Out-of-sample loss (sum of z²) | | | " + " | ".join(f"{v.get('oos_loss', float('nan')):.1f}" for v in vals) + " |")
    open(os.path.join("docs", "VALIDATION.md"), "w").write("\n".join(V) + "\n")
    print("wrote docs/CALIBRATION.md and docs/VALIDATION.md")


if __name__ == "__main__":
    main(sys.argv[1:])
