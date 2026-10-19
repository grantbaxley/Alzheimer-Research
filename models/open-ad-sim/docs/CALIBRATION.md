# Calibration

Each ensemble member is fitted to the same published targets. Loss = sum of squared z-scores, z = (model − target) / tolerance.
Measurement noise on a single CDR-SB visit: SD 0.85 (test–retest). Trial-like cohorts are enrolled at baseline CDR-SB ~N(3.9, 2.1) (TRAILBLAZER-ALZ 2) and ~N(3.2, 1.3) (Clarity AD).

Tolerances express how far apart published sources are, not statistical standard errors.

| Target | Value | Tolerance | Source | z (v6_r01) | z (v6_r05) | z (q1_r01) | z (flatcog_r05) | z (late40_r01) | z (nolate_r05) |
|---|---|---|---|---|---|---|---|---|---|
| `N_EC_mci` | 0.66 | 0.1 | Entorhinal neurons about one-third fewer at CDR 0.5 (Gómez-Isla 1996; Price 2001); smaller losses in von Gunten 2006, hence a wide tolerance | +0.8 | -0.3 | +1.2 | -0.4 | +0.8 | -0.2 |
| `N_HC_mci` | 0.65 | 0.1 | CA1 neurons −46% (Price 2001), −26% (von Gunten 2006); −48% in mixed AD (West 2004) | +1.4 | +0.8 | +1.6 | +0.6 | +1.4 | +0.9 |
| `S_EC_mci` | 0.92 | 0.06 | Entorhinal volume and FDG declines are explained by neuron loss alone, so survivors near normal [extrapolated] | +0.0 | -0.1 | -0.1 | -0.6 | +0.0 | -0.2 |
| `S_HC_mci` | 0.97 | 0.05 | CA1 synapses only −18% in MCI while neurons are −46%: survivors compensate (Scheff 2007; DeKosky 2002) | -1.0 | -1.1 | -1.2 | -1.6 | -1.0 | -1.2 |
| `N_PCC_mci` | 0.98 | 0.02 | No measurable neuron loss in posterior cingulate/precuneus at MCI | -1.1 | +0.2 | -1.2 | -0.9 | -1.0 | +0.1 |
| `S_PCC_mci` | 0.85 | 0.05 | FDG −11 to −22% and SV2A −7%: hypometabolism exceeds atrophy (Chételat 2008; La Joie 2012) | +0.5 | +0.9 | +0.7 | +1.3 | +0.5 | +1.1 |
| `S_IT_mci` | 0.82 | 0.1 | Inferior temporal synapses −36% in amnestic MCI (Scheff 2011); temporal FDG −11% (Chen 2019) | +0.8 | +1.0 | +0.9 | +1.0 | +0.8 | +1.0 |
| `S_PFC_mci` | 0.92 | 0.06 | Frontal synaptophysin −25% with compensation; smallest FDG/atrophy deviations | -0.5 | -0.1 | -0.2 | +0.3 | -0.5 | +0.0 |
| `disc_share_PCC` | 0.3 | 0.2 | Share of PCC dysfunction caused by lost hippocampal input: large in Villain 2008/2010, small in Strom 2022 — wide tolerance | -1.0 | -1.4 | -0.4 | -1.4 | -1.0 | -1.4 |
| `N_EC_mild` | 0.45 | 0.1 | Entorhinal neurons at mild dementia (CDR 1) (Gómez-Isla 1996) | +0.7 | -1.6 | +1.7 | -1.2 | +0.6 | -1.3 |
| `S_HC_mild` | 0.87 | 0.07 | Hippocampal survivors decompensate by mild AD: CA1 synapses −55% (Scheff 2007) | +0.1 | +0.3 | -0.1 | -0.3 | +0.1 | +0.2 |
| `tau_pos_mci` | 0.58 | 0.08 | Temporal tau-PET positive among amyloid-positive MCI: 58.1% (Ossenkoppele 2025) | +1.7 | +0.1 | +2.3 | +0.4 | +1.6 | +0.3 |
| `hi_tau_TB` | 0.32 | 0.07 | High-tau share of TRAILBLAZER-ALZ 2 (552 of 1736; Sims 2023) | +0.5 | +0.0 | -0.1 | -0.2 | +0.4 | -0.1 |
| `dCDR_pbo_TB_lo` | 1.88 | 0.25 | TRAILBLAZER-ALZ 2 placebo, low/medium tau, CDR-SB change at 76 weeks (Sims 2023) | -1.6 | -0.8 | +0.4 | +0.4 | -1.6 | -0.8 |
| `dCDR_pbo_TB_hi` | 3.56 | 0.7 | TRAILBLAZER-ALZ 2 placebo, high tau: derived (n-weighted) from the combined 2.42 [extrapolated] | -2.8 | -2.8 | -2.9 | -3.3 | -2.8 | -2.8 |
| `dCDR_pbo_CL` | 1.66 | 0.25 | Clarity AD placebo, CDR-SB change at 18 months (van Dyck 2023) | -1.3 | -0.2 | +0.3 | -0.4 | -1.3 | -0.3 |
| `prog3_AN_mci` | 0.59 | 0.08 | Amyloid-positive, neurodegeneration-positive MCI progressing to dementia within 3 years (Vos 2015) | +0.0 | -0.0 | -0.6 | -0.8 | -0.2 | -0.0 |
| `prog5_ATpos_mci` | 0.7 | 0.056 | Amyloid- and tau-PET-positive MCI reaching dementia within 5 years: 70% (95% CI 59–81%) (Moscoso 2025, JAMA). Added in v6 after v5 failed it out of sample | +3.3 | +1.9 | +0.8 | +1.4 | +3.3 | +1.6 |
| `prog5_ATneg_mci` | 0.35 | 0.12 | Amyloid-positive, tau-negative MCI reaching dementia within 5 years: ~35% [extrapolated] from meta-analysis odds ratios vs A−T− (A+T+ 11.6, A+T− 2.73; Huszár 2024, CSF-defined tau) applied to the 70% A+T+ risk; wide tolerance | +1.2 | +2.4 | -0.2 | +1.9 | +1.1 | +2.5 |
| `chron_dem` | 13.6 | 2.5 | Years from amyloid positivity to dementia, ADNI median (Betthauser 2022) | +1.8 | +2.6 | +1.6 | +1.4 | +1.8 | +2.0 |
| `nodecl_pbo_TB_lo` | 0.29 | 0.06 | No CDR-SB worsening at 52 weeks, low/medium tau, placebo (TRAILBLAZER-ALZ 2); modeled with measurement noise | -0.2 | -0.3 | -0.1 | -0.6 | -0.2 | -0.4 |
| `nodecl_act_TB_lo` | 0.47 | 0.06 | Same, donanemab arm | -1.8 | -1.6 | -1.4 | -1.8 | -1.7 | -1.7 |
| `slow_TB_lo` | 0.36 | 0.06 | Donanemab slowing of CDR-SB decline, low/medium tau, 76 weeks: 36% (Sims 2023) | -0.9 | -0.6 | -0.0 | +0.0 | -0.9 | -0.7 |
| `slow_TB_hi` | 0.2 | 0.08 | Donanemab slowing, high tau: difference −0.7 (−1.2 to −0.2) over a derived placebo decline [extrapolated] | +0.5 | +1.3 | +0.5 | +0.8 | +0.4 | +1.3 |
| `slow_CL` | 0.27 | 0.05 | Lecanemab slowing of CDR-SB decline at 18 months: 27% (van Dyck 2023) | -0.2 | -0.5 | +0.5 | +0.5 | -0.2 | -0.5 |
| `tau_slow_neo_TB` | 0.05 | 0.12 | No detectable slowing of frontal/parietal/lateral temporal tau-PET accumulation at 76 weeks (TRAILBLAZER-ALZ 2) | +1.4 | +2.4 | +0.4 | +1.5 | +1.4 | +2.2 |
| `dS_PCC_ab` | 0.0 | 0.04 | No FDG recovery shown after amyloid removal (gantenerumab, DIAN-TU, 4 years); no lecanemab/donanemab FDG data | +0.5 | +0.9 | +0.5 | +0.7 | +0.5 | +0.8 |
| `S_PCC_ApTn_CU` | 0.97 | 0.03 | Amyloid-positive, tau-negative, cognitively unimpaired people show little PCC hypometabolism; hypometabolism tracks tau (spatial r 0.55–0.76) far more than amyloid (0.22–0.28) (Strom 2022) | -2.5 | -1.7 | -2.0 | -1.0 | -2.5 | -1.6 |

| Member | Variant | Fixed | Recovery capacity rho | Loss |
|---|---|---|---|---|
| v6_r01 | base | {} | 0.1 | 50.6 |
| v6_r05 | base | {} | 0.5 | 46.6 |
| q1_r01 | base | {'q': 1.0} | 0.1 | 35.9 |
| flatcog_r05 | flatcog | {} | 0.5 | 37.8 |
| late40_r01 | late40 | {} | 0.1 | 49.5 |
| nolate_r05 | nolate | {} | 0.5 | 42.9 |

Fitted parameters:

| Parameter | v6_r01 | v6_r05 | q1_r01 | flatcog_r05 | late40_r01 | nolate_r05 |
|---|---|---|---|---|---|---|
| `pN` | 1 | 3.683 | 4 | 4 | 1 | 3.592 |
| `thr_pos` | 0.1331 | 0.1911 | 0.0587 | 0.1092 | 0.1311 | 0.1671 |
| `thr_hi` | 0.2445 | 0.1911 | 0.431 | 0.1509 | 0.2419 | 0.1852 |
| `k0` | 0.2658 | 0.2316 | 0.2082 | 0.2831 | 0.2708 | 0.2963 |
| `kA` | 0.03265 | 0.03265 | 0.02266 | 0.02271 | 0.0318 | 0.02598 |
| `kauto` | 0.4621 | 0.06778 | 0.4647 | 0.07831 | 0.4594 | 0.05528 |
| `b0` | 0.05673 | 0.04074 | 0.07566 | 0.0593 | 0.0555 | 0.04551 |
| `bA` | 0.0367 | 0.03026 | 0.01691 | 0.02014 | 0.03578 | 0.02936 |
| `delta` | 0.03408 | 0.09966 | 0.03689 | 0.1969 | 0.03338 | 0.09864 |
| `sT` | 0.01413 | 0.04572 | 0.01217 | 0.1206 | 0.01367 | 0.05633 |
| `sA` | 0.1562 | 0.1053 | 0.1259 | 0.07485 | 0.1567 | 0.09956 |
| `sD` | 0.2079 | 0.0285 | 0.4278 | 0.02254 | 0.2054 | 0.02156 |
| `a_cdr` | 50.58 | 27.27 | 31.39 | 30.53 | 50.05 | 29.32 |
| `q` | 1.757 | 1.501 | 1 | 1.166 | 1.752 | 1.449 |
| `R0` | 0.006224 | 0.006018 | 0.01978 | 0.00556 | 0.005987 | 0.006138 |
| `rho` | 0.1 | 0.5 | 0.1 | 0.5 | 0.1 | 0.5 |
| `het` | 0.2436 | 1.1 | 0.5152 | 0.9649 | 0.2409 | 1.1 |
| `sdR` | 0.0621 | 0.03565 | 0.15 | 0.0495 | 0.0608 | 0.03994 |
| `hetK` | 0.4311 | 0.1628 | 0.7203 | 0.4474 | 0.4284 | 0.1629 |
| `sdres` | 0.4075 | 0.5418 | 1 | 0.9272 | 0.4223 | 0.5829 |
