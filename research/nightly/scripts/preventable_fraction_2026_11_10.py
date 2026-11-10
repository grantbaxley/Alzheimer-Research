"""How much "preventable dementia" survives when you restrict a population-attributable fraction to
CAUSAL evidence? (night of 2026-11-10, prevention-population lens, single-cell-type constraint). The
lens asks whether a "preventable fraction" is a causal estimate or an observational
population-attributable fraction (PAF), and how much survives under Mendelian-randomization / RCT
restriction. This toy quantifies the gap and translates it into the thing prevention actually cares
about - years of delayed onset.

PAF (Levin): PAF = p*(RR-1) / (1 + p*(RR-1)), for prevalence p and relative risk RR.
Onset delay from removing a causal hazard, under Gompertz incidence (dementia incidence roughly
doubles every ~5.5 years, so the rate beta = ln(2)/5.5 ~ 0.126/yr): a hazard ratio HR shifts onset
age by delay = ln(1/HR) / beta.

Two real worked examples from tonight's research, where a large OBSERVATIONAL signal nearly vanishes
under causal restriction:
  - Network hyperexcitability / epilepsy: observational late-onset-epilepsy -> dementia HR ~3.05
    (ARIC, PMC7836657), but Mendelian randomization runs mainly AD -> epilepsy with the reverse
    near-null (OR ~1.05; Fang 2023, PMID 37225432), and three low-dose-levetiracetam trials were
    null on cognition (HOPE4MCI CDR-SB null, NCT03486938; LEV-AD, PMID 34570177).
  - Myelin / white-matter hyperintensity: WMH -> AD-liability MR OR ~1.43, but the same paper's
    genetic-WMH score -> ALL-CAUSE dementia was null (HR 1.02, p=0.07; PMID 38776079), and
    SPRINT-MIND slowed WMH yet missed its dementia primary (PMID 30688979).

Illustration with assumed prevalences; the RRs are literature values but the PAFs here are
structural, not calibrated epidemiology. Not medical advice.
"""

from __future__ import annotations

import numpy as np

BETA = np.log(2) / 5.5  # Gompertz rate: dementia incidence doubles ~every 5.5 years


def paf(prevalence: float, rr: float) -> float:
    return prevalence * (rr - 1) / (1 + prevalence * (rr - 1))


def onset_delay_years(hr: float) -> float:
    return float(np.log(1 / hr) / BETA)


def main() -> None:
    print(f"Gompertz rate beta = {BETA:.3f}/yr (dementia incidence doubles ~every 5.5 yr)\n")

    print("(1) PAF collapse: observational RR vs causal RR (MR/RCT), at prevalence p.")
    print("    factor (p)                 observational          causal (MR/RCT)")
    rows = [
        ("epilepsy / hyperexcitability (0.03)", 0.03, 3.05, 1.05),
        ("white-matter hyperintensity (0.25)", 0.25, 1.43, 1.02),
        ("a generic 'risk factor' (0.30)", 0.30, 2.00, 1.20),
    ]
    for label, p, rr_obs, rr_causal in rows:
        print(
            f"    {label:34} RR={rr_obs:<4} PAF {paf(p, rr_obs) * 100:5.1f}%   "
            f"RR={rr_causal:<4} PAF {paf(p, rr_causal) * 100:4.1f}%"
        )
    print("    -> the observational PAF is mostly confounding: under causal RRs it nearly vanishes")
    print("       (WMH all-cause-dementia MR and the epilepsy reverse-MR are both ~null).\n")

    print("(2) What causal effect does a 5-year onset delay actually require?")
    for hr in (0.95, 0.9, 0.8, 0.7, 0.5):
        print(f"    causal HR={hr}: onset delayed ~{onset_delay_years(hr):.1f} yr")
    hr_for_5yr = float(np.exp(-5 * BETA))
    print(
        f"    -> a 5-year delay (the lens's bar) needs HR ~ {hr_for_5yr:.2f} - about HALVING risk."
    )
    print(
        "       A modest causal RR of 1.2 (HR ~0.83) buys only ~1.5 yr even if you eliminate it.\n"
    )

    print(
        "Reading: a 'preventable fraction' headline is almost always an OBSERVATIONAL PAF, and for"
    )
    print("the two structural/functional axes tonight (network hyperexcitability; myelin/WMH) the")
    print("causal fraction surviving MR/RCT restriction is close to zero - the big association is")
    print(
        "mostly reverse causation and confounding. And because dementia incidence rises so steeply"
    )
    print(
        "with age, even a genuine causal factor must roughly HALVE risk to delay onset five years;"
    )
    print("modest causal effects move the population onset age by months, not years. The sober")
    print(
        "implication: prevention bets should be sized by CAUSAL effect, and a marker that fails MR"
    )
    print("and RCT (as WMH and hyperexcitability so far do for dementia) is not yet a lever.")
    print(
        "Structural illustration; assumed prevalences; literature RRs; not calibrated epidemiology."
    )


if __name__ == "__main__":
    main()
