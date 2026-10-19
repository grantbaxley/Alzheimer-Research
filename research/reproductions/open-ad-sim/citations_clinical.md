# open-ad-sim: fact-check of clinical-trial and cohort calibration and validation targets

> Prepared 2026-10-19 with AI research assistance for the [open-ad-sim vetting record](README.md). Each item names the source that was actually opened. The two most consequential items were then re-checked independently against the primary sources (README §5). Not peer reviewed: verify against the primary source before citing any number.

Checked 2026-10-19. Each number below comes from a source that was actually opened (URLs and DOIs are listed per item). Text marked "fetch-tool rendering" was read through a summarising web-fetch tool and not as raw text, so treat its wording as near-verbatim. Every other quote was grep'd from the downloaded full text or PDF.

## Summary

Almost all of the 19 targets match their cited sources: items 1, 2, 4 (low/medium tau), 5, 7, 8, 9, 10, 12, 13, 14, 15, 17 and 19, plus the odds ratios in item 11. The problems are these.

**MISMATCH, item 3 (`dCDR_pbo_TB_hi`).** The model uses 3.56, which it derived by n-weighting. But a high-tau placebo CDR-SB change *was* published: **3.34** (MMRM; donanemab 2.64; difference −0.69, 95% CI −1.19 to −0.20; 21% slowing). It appears in Lilly's FDA advisory-committee briefing document, Tables 1.1 and 6.8. The derived value is 0.22 points (about 7%) too high. The combined-population 2.42 and the FDA's high-tau difference of −0.7 (−1.2 to −0.2) are both confirmed.

**MISMATCH (rule detail), item 16 dose-stopping rule.** TRAILBLAZER-ALZ 2 switched to placebo if amyloid was **<11 CL on any single scan, or 11 to <25 CL on two consecutive scans**. The model keeps only the <11 CL arm of that rule. The cumulative share meeting the criteria was 17%, 47% and 69% at weeks 24, 52 and 76. Dosing ran up to 72 weeks, so "stop at 18 months regardless" is close to the trial.

**NOT FOUND, three sub-items:**
- **Medial temporal tau PET in TRAILBLAZER-ALZ 2 (item 6).** No source reports it. Frontal, parietal, posterior lateral temporal and AD-signature tau PET were all null, which confirms the model's assumption.
- **Mean Centiloid values at 24 and 52 weeks (donanemab) and at 6 and 12 months (lecanemab) (item 16).** These appear only in figures. The end-of-trial means and clearance proportions *were* found, and the model's kinetics reproduce them.
- **COULD NOT ACCESS:** the JAMA supplement eTables for TRAILBLAZER-ALZ 2 (reCAPTCHA or Cloudflare) and the NEJM full text for Clarity AD (HTTP 403). FDA documents, labels and open-access copies were used instead.

**Method caveats (not mismatches):**
- **Item 11.** The 35% risk for A+T− MCI comes from mixing CSF-defined odds ratios with a tau-PET-defined absolute risk. The same Moscoso 2025 paper reports a direct 5-year estimate for A+T− MCI of **30.4% (95% CI 15.9–47.8%)**, which is the better target.
- **Items 10 and 13.** These use different definitions of tau-positive: a visual read for item 10 and a temporal-ROI threshold (mean + 2 SD) for item 13.
- **Item 18.** The noise SD of 0.85 comes from pairing ICCs measured in narrow-SD populations (the 0.68 source had a baseline SD of 0.79) with an SD of about 2. The directly published SEm for CDR-SB in early AD is **0.69–0.71** (0.46–0.47 in MCI-AD). So 0.85 is plausible but at the high end.
- **Item 17.** DIAN-TU showed no FDG effect, but gantenerumab only partly lowered amyloid (64.6 to 46.6 CL in completers). It was not amyloid *removal*.

## Summary table

| # | Parameter (model value) | Claimed source | Source found | What the source reports | Verdict |
|---|---|---|---|---|---|
| 1 | `hi_tau_TB` = 0.32 | Sims 2023 JAMA, "552 of 1736" | Sims et al. JAMA 2023;330:512-527, doi:10.1001/jama.2023.13239 | 552 [31.8%] high tau, 1182 [68.1%] low/medium tau, of 1736 randomized | CONFIRMED |
| 2 | `dCDR_pbo_TB_lo` = 1.88 | TRAILBLAZER-ALZ 2 (TB2), low/medium tau, 76 wk | Sims 2023 | Placebo LSM CDR-SB change 1.88 (1.68–2.08), MMRM, 76 wk (NCS2 model: 1.84) | CONFIRMED |
| 3 | `dCDR_pbo_TB_hi` = 3.56 (derived from combined 2.42); FDA high-tau difference −0.7 (−1.2, −0.2) | TB2, FDA | Sims 2023; FDA briefing document (fda.gov/media/179166); Lilly briefing document (fda.gov/media/179167) | Combined placebo 2.42 (2.24–2.60). **High-tau placebo 3.34**, donanemab 2.64, difference −0.69 (−1.19, −0.20), 21% slowing (MMRM, post hoc). FDA: −0.7 (−1.2, −0.2) | 2.42 and −0.7 CONFIRMED; **3.56 MISMATCH (published 3.34)** |
| 4 | `slow_TB_lo` = 0.36; `slow_TB_hi` = 0.20 (derived) | TB2 | Sims 2023; Lilly briefing | Low/medium tau 36.0% (20.76–51.15%) CDR-SB, MMRM; high tau 21% | 0.36 CONFIRMED; 0.20 APPROXIMATELY CONSISTENT (published 21%) |
| 5 | `nodecl_pbo_TB_lo` = 0.29; `nodecl_act_TB_lo` = 0.47 | TB2, about 52 wk | Sims 2023; Lilly briefing | 29% placebo vs 47% donanemab with CDR-SB change ≤0 at 52 wk, low/medium tau (combined population: 23% vs 36%) | CONFIRMED |
| 6 | `tau_slow_neo_TB` ≈ 0 | TB2 tau PET at 76 wk | Sims 2023; FDA briefing Table 7 | No significant effect on frontal, posterior lateral temporal, parietal or AD-signature-weighted SUVR; medial temporal not reported | CONFIRMED (frontal, parietal, lateral temporal); medial temporal NOT FOUND |
| 7 | Baseline CDR-SB: TB2 3.9 (2.1); Clarity AD 3.2 (1.3) | TB2, Clarity AD | Sims 2023 Table 1; Eisai briefing (fda.gov/media/169264) | TB2 combined: placebo 3.9 (2.1), donanemab 4.0 (2.1). Clarity AD: placebo 3.22 (1.336), lecanemab 3.18 (1.344) | CONFIRMED |
| 8 | `dCDR_pbo_CL` = 1.66; `slow_CL` = 0.27 | van Dyck 2023 NEJM | PubMed abstract PMID 36449413; Leqembi label; FDA briefing | Placebo 1.66, lecanemab 1.21, difference −0.45 (−0.67, −0.23), −27% at 18 months | CONFIRMED |
| 9 | `prog3_AN_mci` = 0.59 | Vos 2015 | Vos et al. Brain 2015;138:1327-38, doi:10.1093/brain/awv029 | 59% three-year progression to AD-type dementia in the NIA-AA "high AD likelihood" group (A+N+, n=353) | CONFIRMED (amyloid defined by CSF; outcome AD-type dementia) |
| 10 | `prog5_ATpos_mci` = 0.70 (59–81%) | Moscoso 2025 JAMA | Moscoso et al. JAMA 2025;334:229-242, doi:10.1001/jama.2025.7817 | A+T+ MCI: 5-year absolute risk of dementia 70% (59–81%); Table 2: 69.9 (59.3–81.2) | CONFIRMED (tau defined by visual read) |
| 11 | `prog5_ATneg_mci` ≈ 0.35 from ORs 11.6 and 2.73 | Huszár 2024 | Huszár et al. Alzheimers Res Ther 2024;16:81, doi:10.1186/s13195-024-01455-2; Moscoso 2025 Table 2 | OR A+T+ 11.60 (7.96–16.91); A+T− 2.73 (1.65–4.52) vs A−T−, tau by CSF p-tau181. Moscoso direct estimate for A+T− MCI: 30.4% (15.9–47.8) | ORs CONFIRMED; 0.35 APPROXIMATELY CONSISTENT, but the derivation is not sound |
| 12 | `chron_dem` = 13.6 y | Betthauser 2022 | Betthauser et al. Brain 2022;145:4065-79, doi:10.1093/brain/awac213 | Median time from estimated amyloid onset age to CDR ≥1: 13.57 (12.98–14.08) y, ADNI n=595 | CONFIRMED (A+ threshold about 33 CL; outcome CDR ≥1) |
| 13 | `tau_pos_mci` = 0.581 | Ossenkoppele 2025 | Ossenkoppele et al. Nat Neurosci 2025;28:1610-21, doi:10.1038/s41593-025-02000-6 | 58.1% (731/1,258) of Aβ+ MCI were tau-positive in the temporal ROI | CONFIRMED (raw pooled prevalence; age-dependent) |
| 14 | V1: −1.2 (−1.7, −0.7) at 3 y vs ADNI | TB2 long-term extension (LTE) | Zimmer et al. J Prev Alzheimers Dis 2026;13:100446, doi:10.1016/j.tjpad.2025.100446 | Early-start vs weighted ADNI control: −1.2 (−1.7, −0.7) at 3 y (154 wk) | CONFIRMED (exploratory external control) |
| 15 | V2: 1.75 (ADNI) to 2.17 (BioFINDER) at 4 y | Clarity AD open-label extension (OLE) | van Dyck et al. AAIC 2025 abstract, Alzheimers Dement 2025;21(S7):e108905; BioArctic press release 31 Jul 2025 | 1.75 vs ADNI at 48 mo; 2.17 vs BioFINDER at 4 y (1.40 at 3 y). No CIs | CONFIRMED (conference abstract and press release only) |
| 16 | Antibody kinetics; stopping rule | TB2, Clarity AD | Sims 2023; FDA/Lilly briefing documents; Kisunla and Leqembi labels; Eisai briefing | Donanemab: clearance <24.1 CL in 29.7/66.1/76.4% at wk 24/52/76; mean 104.0 to 15.0 CL at wk 76. Lecanemab: 77.9 to 23.0 CL at 18 mo; 67% <30 CL. Stopping rule: <11 CL once, or 11 to <25 CL twice | Kinetics APPROXIMATELY CONSISTENT; stopping rule MISMATCH (simplified); intermediate means NOT FOUND |
| 17 | `dS_PCC_ab` ≈ 0 | DIAN-TU gantenerumab | Salloway et al. Nat Med 2021;27:1187-96, doi:10.1038/s41591-021-01369-8; McCullough et al. Alzheimers Dement 2025;21:e70347 | No significant FDG-PET differences for either drug; no regional FDG effect after 4 y | CONFIRMED (caveat: amyloid only partly reduced; DIAD population) |
| 18 | CDR-SB noise SD ≈ 0.85 (ICC 0.68–0.83, SD about 2) | not specified | McDougall 2021 JPAD; Lansdall 2023 JPAD; Lansdall 2024 Alzheimers Dement | ICC 0.83 (prodromal AD, about 8 wk); ICC 0.68 (MCI, baseline vs month 6, baseline SD 0.79); published SEm 0.69–0.71 (early AD), 0.46–0.47 (MCI-AD) | APPROXIMATELY CONSISTENT (high end; derivation mixes populations) |
| 19 | ARIA-E by APOE ε4 (documentation only) | none | Sims 2023 Table 3; Eisai briefing / Honig 2024; Kisunla label 7/2025 | Donanemab 15.7/22.8/40.6%; lecanemab 5.4/10.9/32.6% (non-carrier/heterozygote/homozygote) | Values reported with sources below |

## Per-item notes

### 1. `hi_tau_TB` = 0.32. CONFIRMED
- **Source:** Sims JR, Zimmer JA, Evans CD, et al. Donanemab in Early Symptomatic Alzheimer Disease: The TRAILBLAZER-ALZ 2 Randomized Clinical Trial. *JAMA* 2023;330(6):512-527. doi:10.1001/jama.2023.13239. Opened at https://pmc.ncbi.nlm.nih.gov/articles/PMC10352931/
- **Quote (abstract):** "Among 1736 randomized participants (mean age, 73.0 years; 996 [57.4%] women; 1182 [68.1%] with low/medium tau pathology and 552 [31.8%] with high tau pathology), 1320 (76%) completed the trial."
- 552/1736 = 0.318. Minor point: 1182 + 552 = 1734, so 2 randomized participants are in neither subgroup. Lilly's briefing gives high-tau N = 281 placebo + 271 donanemab.
- The Kisunla label says the same: "68% had low/medium tau level and 32% had high tau level".

### 2. `dCDR_pbo_TB_lo` = 1.88. CONFIRMED
- **Quote (Sims 2023 abstract):** "LSM change in CDR-SB score at 76 weeks was 1.20 (95% CI, 1.00-1.41) with donanemab and 1.88 (95% CI, 1.68-2.08) with placebo (difference, −0.67 [95% CI, −0.95 to −0.40]; P < .001) in the low/medium tau population".
- **Definition:** MMRM least-squares mean change at 76 weeks. The NCS2 model gives placebo 1.84 and donanemab 1.16 (Table 2). Low/medium tau means flortaucipir SUVR 1.10–1.46 with a visual read consistent with moderate AD (FDA slides).

### 3. `dCDR_pbo_TB_hi` = 3.56 (derived). MISMATCH; 2.42 and the FDA −0.7 CONFIRMED
- **Combined population (Sims 2023 abstract):** placebo "2.42 (95% CI, 2.24-2.60)", donanemab 1.72, difference "−0.7 [95% CI, −0.95 to −0.45]".
- **High tau, JAMA text (post hoc):** "Analysis of the smaller (n = 552) high tau population alone ... was completed post hoc. The difference between the donanemab and placebo groups in the LSM change from baseline at 76 weeks was 1.26 (95% CI, −1.77 to 4.28; P = .42) for the iADRS score and −0.69 (95% CI −1.19 to −0.20; P = .006) for the CDR-SB score." The group means are said to be in eTables 4, 5 and 10 of Supplement 3. **COULD NOT ACCESS** those: the PMC PDF is behind reCAPTCHA and jamanetwork.com is behind Cloudflare.
- **High tau, FDA:** the FDA Briefing Document for BLA 761248, PCNS Advisory Committee 2024-06-10 (https://www.fda.gov/media/179166/download), §3.2.1.5: "subjects with a high tau level had an estimate favoring treatment with donanemab on iADRS (1.3; 95% CI -1.8, 4.3) and CDR-SB (-0.7, 95% CI -1.2, -0.2)." This confirms the model's −0.7 (−1.2 to −0.2).
- **High-tau placebo change is published.** Source: Eli Lilly, Donanemab PCNS Advisory Committee Sponsor Briefing Document (approved 15 May 2024), https://www.fda.gov/media/179167/download, Table 1.1 (p. 20) and Table 6.8 (p. 67). For high tau (placebo N = 281, donanemab N = 271), CDR-SB (MMRM):
  - mean baseline 4.43 (placebo) and 4.36 (donanemab);
  - change from baseline **3.34** (placebo) and **2.64** (donanemab);
  - difference −0.69 (−1.19, −0.20), 21%, p = 0.006.
  - Text: "the absolute difference from placebo was similar across these subgroups (-0.67 and -0.69, for low-medium and high tau groups respectively)".
- **Labels:** neither the Kisunla label (2024 nor 7/2025) gives high-tau group means. Table 8 covers the combined population only.
- **Why the derivation is off:** (2.42×876 − 1.88×594)/282 = 3.56 is correct arithmetic. But MMRM least-squares means are covariate-adjusted model estimates; the combined analysis also adjusts for tau category. So the combined LSM is not an n-weighted average of the subgroup LSMs.
- **Recommendation:** set `dCDR_pbo_TB_hi` = 3.34, cite fda.gov/media/179167 Table 1.1, and mark it post hoc. If the model enrols high-tau virtual participants separately, the high-tau baseline CDR-SB (about 4.4) is also available.

### 4. `slow_TB_lo` = 0.36 CONFIRMED; `slow_TB_hi` = 0.20 APPROXIMATELY CONSISTENT
- **Sims 2023:** "In the low/medium tau population, the differences between treatment groups in the LSM change from baseline at 76 weeks was −0.67 (95% CI, −0.95 to −0.40) (36.0% [95% CI, 20.76%-51.15%] slowing of clinical progression) for CDR-SB".
- **High tau:** Lilly Tables 1.1 and 6.8 give "-0.69 (21%)", p = 0.006. Computing 0.69/3.34 gives 0.207. The model's 0.20 (about 0.7/3.56) is within rounding, but should be re-derived from 3.34.
- **Definition check:** the model uses CDR-SB, which is correct. The primary iADRS slowing (NCS2) was 35.1% for low/medium tau and 22.3% combined, and must not be swapped in. Combined CDR-SB slowing was 28.9%.

### 5. `nodecl_pbo_TB_lo` = 0.29, `nodecl_act_TB_lo` = 0.47. CONFIRMED
- **Sims 2023:** "in the low/medium tau population, an estimated 47% of participants were stable (showed no decline in CDR-SB from baseline) with donanemab at 1 year compared with 29% of participants receiving placebo (P < .001) (eTable 6 in Supplement 3)."
- **Definition (Lilly briefing, fda.gov/media/179167):** "Patients' status was classified as 'no progression' if their CDR-SB change from baseline was less than or equal to 0 at 52 weeks." It was tested with a GLMM, so these are model-estimated probabilities. Overall population: "36% donanemab-treated patients were stable versus 23% placebo-treated patients".
- **Modelling note:** because CDR-SB moves in 0.5-point steps and is noisy, "≤0 change" counts noise-driven improvement as stable. The simulated statistic should be computed on noisy *observed* scores at week 52 (see item 18).

### 6. `tau_slow_neo_TB` ≈ 0. CONFIRMED for frontal, parietal and lateral temporal; medial temporal NOT FOUND
- **Sims 2023 (frontal was the only tau secondary outcome):** "The difference in LSM change in tau SUVR from placebo in the frontal lobe at 76 weeks was −0.0002 (95% CI, −0.01 to 0.01; P = .97) in the low/medium tau population and −0.0041 (95% CI, −0.01 to 0.01; P = .45) in the combined population." Also: "The lack of response in frontal tau-PET is inconsistent with the TRAILBLAZER-ALZ phase 2 results. Additional regions have yet to be analyzed and reported."
- **FDA Briefing Document (fda.gov/media/179166), Tau PET and Table 7:** "No treatment effect was observed in change from baseline to Week 76 in frontal tau deposition ... Similarly, no treatment effect was observed in either population in AD-signature-weighted SUVR tau deposition or in exploratory regional (i.e., posterior lateral temporal and parietal) tau endpoints."
- **Table 7, LS mean change at week 76 (donanemab vs placebo; difference with 95% CI):**

  | Population | Region | Donanemab | Placebo | Difference (95% CI) |
  |---|---|---|---|---|
  | Low/medium tau (N 404/452) | Frontal | 0.0273 | 0.0271 | 0.0002 (−0.0100, 0.0104) |
  | Low/medium tau | Posterior lateral temporal | 0.0634 | 0.0698 | −0.0064 (−0.0207, 0.0078) |
  | Low/medium tau | Parietal | 0.0521 | 0.0555 | −0.0034 (−0.0160, 0.0091) |
  | Low/medium tau | AD-signature-weighted | 0.0692 | 0.0706 | −0.0015 (−0.0154, 0.0124) |
  | Overall (N 578/654) | Frontal | 0.0401 | 0.0442 | −0.0041 (−0.0148, 0.0066) |
  | Overall | Posterior lateral temporal | 0.0503 | 0.0617 | −0.0114 (−0.0257, 0.0029) |
  | Overall | Parietal | 0.0478 | 0.0553 | −0.0074 (−0.0206, 0.0058) |
  | Overall | AD-signature-weighted | 0.0636 | 0.0701 | −0.0065 (−0.0208, 0.0078) |

- **Medial temporal:** not in the JAMA paper, the FDA briefing, the Lilly briefing or the labels. A search found no later TRAILBLAZER-ALZ 2 regional tau publication. NOT FOUND.
- **Caution:** "≈0" is the null point estimate, but the CIs do not exclude modest slowing. For example, the overall posterior lateral temporal estimate is −0.0114/0.0617 ≈ −18% relative (about −42% to +5%). Note also that the model's "lateral temporal" is the source's "posterior lateral temporal". For contrast, the Leqembi label reports lecanemab slowing tau PET in medial temporal (P<0.01), meta-temporal and temporal regions, but not frontal or parietal.

### 7. Baseline CDR-SB distributions. CONFIRMED
- **TB2 (Sims 2023 Table 1), CDR-SB mean (SD):**
  - low/medium tau: donanemab 3.7 (2.1), placebo 3.7 (2.0);
  - combined: donanemab 4.0 (2.1), placebo **3.9 (2.1)**.
  - Lilly's MMRM table gives 3.92 and 3.89 combined, and 4.36 and 4.43 for high tau.
  - The model's 3.9 (2.1) is the combined placebo arm, which is appropriate. If virtual participants are enrolled by tau subgroup, use the subgroup means (about 3.7 vs about 4.4).
- **Clarity AD (Eisai PCNS briefing document, BLA 761269 S-001, June 9, 2023, https://www.fda.gov/media/169264/download):** "The mean Baseline value and standard deviation (SD) for CDR-SB was similar between placebo (3.22 [1.336]) and lecanemab (3.18 [1.344])." The FDA briefing (https://www.fda.gov/media/169263/download) gives means of 3.22 and 3.17, and the NEJM abstract says "approximately 3.2 in both groups".
- **Note:** both trials truncate the distribution through eligibility (TB2: MMSE 20–28; Clarity AD: global CDR 0.5–1). A normal distribution with these moments needs truncation at 0 or at the eligibility limits.

### 8. `dCDR_pbo_CL` = 1.66, `slow_CL` = 0.27. CONFIRMED
- **Source:** van Dyck CH, et al. Lecanemab in Early Alzheimer's Disease. *N Engl J Med* 2023;388:9-21. doi:10.1056/NEJMoa2212948. The PubMed abstract (PMID 36449413) was opened; the NEJM full text returned HTTP 403.
- **Quote:** "The adjusted least-squares mean change from baseline at 18 months was 1.21 with lecanemab and 1.66 with placebo (difference, -0.45; 95% confidence interval [CI], -0.67 to -0.23; P<0.001)."
- **Leqembi label** (https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/761269s012s015lbl.pdf), Table 10: placebo 1.66, lecanemab 1.21, "-0.45 (-27%)".
- **FDA briefing note:** the FDA's own analysis set gave a slightly smaller effect: "(-0.45[-27%], p=0.00005) ... and the FDA FAS population (-0.39[-25%], p=0.0004)". The primary timepoint was week 79.

### 9. `prog3_AN_mci` = 0.59. CONFIRMED
- **Source:** Vos SJB, Verhey F, Frölich L, et al. Prevalence and prognosis of Alzheimer's disease at the mild cognitive impairment stage. *Brain* 2015;138(Pt 5):1327-38. doi:10.1093/brain/awv029 (PMID 25693589; PMC5013930).
- **Quote (abstract):** "353 (46%) subjects were in the high Alzheimer's disease likelihood group ... The 3-year progression rate to Alzheimer's disease-type dementia was 59% in the high Alzheimer's disease likelihood group, 22% in the isolated amyloid pathology group, 24% in the suspected non-Alzheimer pathophysiology group, and 5% in the low Alzheimer's disease likelihood group."
- **Definitions (fetch-tool rendering of the full text):**
  - amyloid = "CSF amyloid-β1-42" only; the paper says "use of amyloid-PET could have led to different results";
  - neuronal injury = "CSF tau, cerebral glucose metabolism on FDG-PET, medial temporal lobe atrophy score or hippocampal volume";
  - the rate is an "Estimated 3-year progression (cumulative incidence) rate" from adjusted Cox models;
  - mean follow-up was 2.4 years overall, and about 2.3 years in this group (fetch tool);
  - the outcome is AD-type dementia, not all-cause dementia;
  - no CI is given for the 59%.

### 10. `prog5_ATpos_mci` = 0.70 (59–81%). CONFIRMED
- **Source:** Moscoso A, Heeman F, Raghavan S, et al. Frequency and Clinical Outcomes Associated With Tau Positron Emission Tomography Positivity. *JAMA* 2025;334(3):229-242. doi:10.1001/jama.2025.7817 (PMID 40522652; PMC12848857).
- **Quote (abstract):** "Among participants with MCI at the time of the tau PET scan, an Aβ PET-positive/tau PET-positive profile was associated with a 5-year absolute risk of progression to dementia of 70% (95% CI, 59%-81%)." Table 2 (fetch-tool rendering): 69.9 (59.3 to 81.2).
- **Definitions and caveats:**
  - Pooled convenience sample of 21 cohorts.
  - Flortaucipir **visual read** "designed to indicate the presence of advanced neurofibrillary tangle pathology (Braak stages V-VI)".
  - Aβ+ = Centiloid >24.4 or a positive visual read.
  - MCI median follow-up for the diagnosis outcome was 2.9 y (maximum 6.8 y), per Table 1 (fetch tool), so the 5-year figure leans on model extrapolation.
  - In this dataset 74% (511/695) of Aβ+ MCI were tau-positive on visual read. That is a different T+ definition from item 13.

### 11. `prog5_ATneg_mci` ≈ 0.35. ORs CONFIRMED; value APPROXIMATELY CONSISTENT; method questionable
- **Source:** Huszár Z, Engh MA, Pavlekovics M, et al. Risk of conversion to mild cognitive impairment or dementia among subjects with amyloid and tau pathology: a systematic review and meta-analysis. *Alzheimers Res Ther* 2024;16:81. doi:10.1186/s13195-024-01455-2 (PMID 38610055; PMC11015617).
- **Quote (abstract):** "The OR for conversion in A+T+ MCI subjects (11.60 [95% CI 7.96; 16.91]) was significantly higher than in A+T- subjects (2.73 [95% CI 1.65; 4.52])."
- **Details (fetch-tool rendering of the full text):**
  - The reference is A−T−.
  - The MCI A/T tables use CSF p-tau181; tau PET was used only in the cognitively unimpaired analysis.
  - The outcome is AD or unspecified dementia, pooled.
  - Follow-up in the included studies ranged from "20 months to more than 10 years".
  - No absolute risks are reported.
- **How 0.35 is reached:** anchor A+T+ at 70% (Moscoso), giving odds 2.33. Dividing by 11.6 gives A−T− odds of 0.201 (p = 0.167). Multiplying by 2.73 gives odds of 0.549 (**p = 0.354**).
- **Why the method is weak:**
  1. It mixes a tau-PET visual-read absolute risk with CSF-p-tau odds ratios. CSF p-tau turns abnormal earlier, so CSF "A+T−" is a less advanced group than PET "A+T−".
  2. The ORs pool studies with very different follow-up, so they are not tied to a 5-year horizon. ORs are also non-collapsible and not risk ratios.
  3. Heterogeneity and cut-offs vary across studies.
- **Better source:** Moscoso 2025 Table 2 (fetch-tool rendering) reports the 5-year risk of dementia for MCI directly:
  - Aβ−/vTAU− 15.3% (9.5–22.2);
  - **Aβ+/vTAU− 30.4% (15.9–47.8)**;
  - Aβ+/vTAU+ 69.9% (59.3–81.2).

  The implied ORs from these (about 12.9 and 2.4) happen to agree with Huszár. Recommendation: use 0.30 (CI 0.16–0.48) from Moscoso, so that the definition matches item 10.

### 12. `chron_dem` = 13.6 years. CONFIRMED
- **Source:** Betthauser TJ, Bilgel M, Koscik RL, et al. Multi-method investigation of factors influencing amyloid onset and impairment in three cohorts. *Brain* 2022;145(11):4065-4079. doi:10.1093/brain/awac213. ADNI-hosted PDF: https://adni.loni.usc.edu/adni-publications/Betthauser-2022-Multi-method%20investigation%20of.pdf
- **Quote:** "The median survival time from EAOA to CDR ≥1 was 13.57 (12.98–14.08) years with a 10-year post-EAOA survival rate of 0.744 (0.703–0.786)". The sample was 595 ADNI participants "that were not impaired before amyloid onset". Here EAOA means estimated amyloid onset age.
- **Definitions:**
  - "Florbetapir SUVRWM > 0.8 (33.1 Centiloids)" defines A+.
  - EAOA is model-estimated (the average of SILA and ODE–GP).
  - The outcome is global CDR ≥1, a mild-dementia level of impairment, not a dementia diagnosis.
- **Strong dependence on covariates:** female 12.89 y vs male 14.08 y; APOE ε4+ 12.73 y vs ε4− 14.42 y. Risk also rises nonlinearly for onset age over 65.
- **Modelling note:** the model's amyloid-positivity threshold must match about 33 CL. A lower threshold (for example 24 CL) would lengthen the chronicity.

### 13. `tau_pos_mci` = 0.581. CONFIRMED
- **Source:** Ossenkoppele R, Coomans EM, et al. Tau PET positivity in individuals with and without cognitive impairment varies with age, amyloid-β status, APOE genotype and sex. *Nat Neurosci* 2025;28(8):1610-1621. doi:10.1038/s41593-025-02000-6. Full text read through Europe PMC (PMC12321570).
- **Quote:** "the prevalence of tau positivity in the temporal cortex was ... 6.4% (55 of 863) in Aβ-negative participants with MCI versus 58.1% (731 of 1,258) in Aβ-positive participants with MCI".
- **Definitions:** "cohort-specific threshold of mean + 2 s.d. in Aβ-negative CU individuals who were aged ≥50 years" in an ROI "covering medial and lateral parts of the temporal cortex". Data came from 42 cohorts and four tracers.
- **Age dependence:** the age-modelled estimate for Aβ+ MCI "decreased from 68.0% (95% CI 60.4–75.6%) to 52.9% (95% CI 46.3–59.5%)" between ages 60 and 80. The 58.1% is the crude pooled prevalence.
- **Consistency flag:** this T+ (temporal ROI threshold) is not the same as the T+ behind item 10's 70% risk (visual read, where 74% of Aβ+ MCI were positive in Moscoso's data).

### 14. Validation V1 (donanemab LTE, −1.2 at 3 years). CONFIRMED
- **Source:** Zimmer JA, Sims JR, Evans CD, et al. Donanemab in early symptomatic Alzheimer's disease: results from the TRAILBLAZER-ALZ 2 long-term extension. *J Prev Alzheimers Dis* 2026;13(2):100446. doi:10.1016/j.tjpad.2025.100446 (PMID 41330788; PMC12869028).
- **Quote (abstract):** "At 3 years, donanemab slowed disease progression on the Clinical Dementia Rating Scale (CDR)-Sum of Boxes (CDR-SB) in early-start participants versus a weighted ADNI control (-1.2 points; 95 % confidence interval [CI], -1.7, -0.7)." Delayed start vs ADNI at 76 weeks after starting donanemab: −0.8 (−1.3, −0.3). Early vs delayed start, CDR-Global hazard ratio 0.73.
- **Details (fetch-tool rendering of the full text):**
  - The model timepoint was 154 weeks.
  - ADNI controls had cognitive impairment and CSF t-tau/Aβ42 >0.28; 534 were eligible.
  - Propensity-score IPW (ATT), weights trimmed at the 95th percentile; effective sample size 268.
  - Analyses were exploratory, and participants were limited to those who entered the LTE.
- **Modelling note:** the simulated "untreated" comparator should copy this selection: impaired, CSF-defined, and conditioned on completing 76 weeks.

### 15. Validation V2 (lecanemab OLE, 1.75 to 2.17 at 4 years). CONFIRMED
- **ADNI comparison:** van Dyck CH, Li D, Kanekiyo M, et al. The Lecanemab Clarity AD Open-Label Extension in Early Alzheimer's Disease: Initial Findings From the 48-Month Analysis. *Alzheimers Dement* 2025;21(Suppl 7):e108905. doi:10.1002/alz70861_108905 (https://pmc.ncbi.nlm.nih.gov/articles/PMC12725329/). Quote (fetch-tool rendering): "differences in CDR‐SB increasing over 18 months (0.52), 36 months (1.01), and 48 months (1.75)." No CIs are given.
- **BioFINDER comparison:** BioArctic press release, 31 July 2025, "Latest data presented at AAIC 2025 reinforces lecanemab's clinical effect..." (https://www.bioarctic.com/en/latest-data-presented-at-aaic-2025-reinforces-lecanemabs-clinical-effect-with-consistent-safety-profile/). Quote (fetch-tool rendering): "when benchmarked against the expected decline in the BioFINDER cohort, lecanemab showed a 1.40-point difference over three years and 2.17-point difference at the four-year mark."
- **Independent report:** Alzforum, 7 Aug 2025 (https://www.alzforum.org/news/conference-coverage/signs-lasting-benefit-amyloid-immunotherapy), a secondary source. It gives 0.57/1.4/2.17 vs BioFINDER-1 and reports that "the lecanemab group had dropped from 859 to 478 people" and "matched ADNI controls dropped from 436 to 98".
- **Caveats:** conference abstract and press release only; no peer-reviewed full paper was found. The design is open-label against an external control, with heavy attrition.

### 16. Antibody kinetics and dose-stopping. Kinetics APPROXIMATELY CONSISTENT; stopping rule MISMATCH; intermediate means NOT FOUND

**Published donanemab data (TRAILBLAZER-ALZ 2):**
- Clearance (<24.1 CL), overall population: **29.7% (226/761) at week 24, 66.1% (443/670) at week 52, 76.4% (469/614) at week 76** (Lilly briefing Table 6.11). Low/medium tau: 34.2% at week 24 and 80.1% at week 76 (Sims 2023).
- Mean Centiloid: baseline 104.0 (SD 34.4), and at week 76 **15.0 (SD 22.8)** observed. Adjusted change −87.0 vs −0.7 for placebo (FDA briefing Table 6; Kisunla label Table 7). Sims 2023: −88.0 low/medium tau, −87.0 combined.
- Mean Centiloid at weeks 24 and 52 appears only in figures (JAMA Fig. 3A, label Fig. 1). **NOT FOUND** as numbers.
- Context from TRAILBLAZER-ALZ 6, same standard regimen (Wang H, et al. *Alzheimers Dement* 2025;21(4):e70062, doi:10.1002/alz.70062; Europe PMC PMC11963282). Screening mean 85.3 CL (SD 36.6); "adjusted mean (standard error [SE]) change of 58.8 (1.8) CL in the standard arm"; 56.7% <24.1 CL and 34.0% <11 CL at week 24. That is faster than TRAILBLAZER-ALZ 2's 29.7% at week 24, so clearance rates depend on the population and baseline.

**Published lecanemab data (Clarity AD):**
- Eisai briefing: "The mean level at Baseline for lecanemab was 77.9 Centiloids, and at the end of the study was 23.0 Centiloids"; adjusted change −55.5 vs +3.6 for placebo, difference −59.1 (also NEJM abstract and the CTAD 2022 press release).
- Leqembi label: "After Week 79 ... 67% of patients had amyloid levels less than 30 Centiloids".
- Means at 6 and 12 months appear only in figures. **NOT FOUND** as numbers.

**My check of the model's kinetics.** I simulated the model's lognormal rate distribution, decaying to a 5 CL floor, with 200,000 draws (a short simulation script, not included). These are my calculations, not published numbers.

| Drug, baseline | Week | Model mean (median) CL | Model P(<threshold) | Published |
|---|---|---|---|---|
| Donanemab, 104 CL | 24 | 41 (40) | 30% <24.1 CL | 29.7% <24.1 CL |
| Donanemab, 104 CL | 52 | 22 (15) | 65% <24.1 CL | 66.1% <24.1 CL |
| Donanemab, 104 CL | 76 | 15.4 (8.6) | 80% <24.1 CL | 76.4% <24.1 CL; mean 15.0 |
| Lecanemab, 77.9 CL | 79 | 23.2 | 68.5% <30 CL | mean 23.0 CL; 67% <30 CL |

- The aggregate fit is good.
- The model's quoted "~35 CL at 6 months, ~15 CL at 12 months" and "~24 CL at 18 months" are *median-rate* paths from 100 CL. Population means are higher (about 22 CL at 52 weeks). The lecanemab "~24 CL" is from 100 CL, not Clarity AD's 77.9 CL baseline. Applied to 100 CL, the model's lecanemab mean at 18 months is about 29 CL.
- At TRAILBLAZER-ALZ 6's 85 CL baseline, the model gives 35% <24.1 CL at week 24, against the observed 56.7%.

**Dose-stopping rule.**
- Sims 2023 Methods: "If amyloid plaque level (assessed at 24 weeks and 52 weeks) was less than 11 Centiloids on any single PET scan or less than 25 but greater than or equal to 11 Centiloids on 2 consecutive PET scans ..., donanemab was switched to placebo in a blinded procedure." Treatment ran "for up to 72 weeks".
- The FDA slides (https://www.fda.gov/media/179239/download) and the label list scans at Weeks 24, 52 and 76.
- Share meeting the criteria: 17.1% (130/761), 46.6% (313/672) and 69.2% (429/620) at weeks 24, 52 and 76 (Lilly Table 6.10). The label rounds these to 17%, 47% and 69%; the FDA slides give 17%, 42% and 60% on a different denominator.
- **The model drops the "11 to <25 CL on two consecutive scans" criterion.** A short simulation (script not included) gives:

  | Rule | Week 24 | Week 52 | Week 76 |
  |---|---|---|---|
  | Model rule (<11 CL only) | 12–14% | 41–42% | 59–60% |
  | Full trial rule | 12–14% | 41–43% | 67–69% |

- "Stop at 18 months regardless" roughly matches the 72-week maximum dosing.
- The current label (7/2025, https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/761248s004lbl.pdf) says to "Consider stopping dosing ... based on reduction of amyloid plaques to minimal levels on amyloid PET imaging".

**Reaccumulation after stopping** (the model does not appear to include it):
- donanemab, median 2.80 CL/yr (2024 label), updated to 2.4 CL/yr in the LTE paper;
- lecanemab, mean 2.6 CL/yr off treatment (Leqembi label, Study 201).

### 17. `dS_PCC_ab` ≈ 0 (no FDG recovery). CONFIRMED, with caveats
- **Source:** Salloway S, Farlow M, McDade E, et al. A trial of gantenerumab or solanezumab in dominantly inherited Alzheimer's disease. *Nat Med* 2021;27:1187-1196. doi:10.1038/s41591-021-01369-8 (PMC8988051).
- **Quote (fetch-tool rendering, reproduced in pieces):** "There were no significant between-group differences in biological measures of brain cortical metabolism 18F-FDG-PET or atrophy (precuneus thickness and hippocampal volume by volumetric magnetic resonance imaging (MRI) for either drug group compared to placebo". Mean treatment was about 4.0 years.
- **Regional follow-up:** McCullough A, Chen CD, Gordon BA, et al. Regional effects of gantenerumab on neuroimaging biomarkers in the DIAN-TU-001 trial. *Alzheimers Dement* 2025;21(7):e70347. doi:10.1002/alz.70347 (PMC12260115). Quotes: "Gantenerumab significantly reduced PiB‐PET uptake overall and in most regions and showed no changes in FDG‐PET or MRI measures." and "We did not find any evidence of improvement in downstream metabolic or neurodegeneration imaging biomarkers over the 4‐year trial period."
- **Caveats:**
  - Amyloid was not removed. In gantenerumab completers mean PiB went from "64.6 Centiloids at baseline to ... 46.6 Centiloids at Year 4". The donanemab and lecanemab trials reach about 15–23 CL.
  - Solanezumab did not lower plaque.
  - The population is DIAD, partly presymptomatic, with n = 92 in the imaging analysis.
  - A null result is weak evidence that FDG never recovers.

### 18. CDR-SB measurement noise (SD ≈ 0.85). APPROXIMATELY CONSISTENT; derivation mixes populations
- **ICC 0.83:** McDougall F, Edgar C, Mertes M, et al. Psychometric Properties of the CDR-SB and Other Cognitive and Functional Outcomes in a Prodromal AD Population. *J Prev Alzheimers Dis* 2021;8(2):151-160. doi:10.14283/jpad.2020.73 (PMID 33569561). Abstract: "For the CDR-SB, test-retest reliability was good (intra-class correlation coefficient [ICC]=0.83)". This was screening vs baseline, "an interval approximately 8 Weeks" (fetch tool), in SCarlet RoAD prodromal AD.
- **ICC 0.68:** Lansdall CJ, McDougall F, Butler LM, et al. Establishing Clinically Meaningful Change on Outcome Assessments Frequently Used in Trials of MCI Due to AD. *J Prev Alzheimers Dis* 2023;10(1):9-18. doi:10.14283/jpad.2022.102. Quote: "ICC values (CDR-SB, 0.68; ADAS-Cog 11, 0.66; ADAS-Cog 13, 0.76)". The ICC was computed from baseline and Month 6 among participants rated "no change" on the MCI-CGIC, n = 769 at baseline. **Baseline CDR-SB mean (SD) was 1.82 (0.79)**, not about 2.
- **Direct SEm:** Lansdall CJ, Teng E, Chague J, et al. Care partner-informed meaningful change thresholds for the CDR-SB for trials of early AD. *Alzheimers Dement* 2024;20. doi:10.1002/alz.14050 (PMC11497679), Tauriel trial. Quote: "SEm was derived from the formula SEm = SD × √1− r ... The reliability coefficient for SEm was r = 0.8." Table 2 SEm:

  | Group | Week 49 | Week 73 |
  |---|---|---|
  | Early AD | **0.71** (0.5 SD = 0.80) | 0.69 |
  | MCI-AD | 0.47 | 0.46 |
  | Mild AD | 0.66 | 0.64 |

- **Assessment:** SEm = SD × √(1 − ICC). ICCs measured in narrow-SD samples should not be paired with an SD of about 2 from another population. The best direct estimate for an early-AD trial population is about 0.7, so the model's 0.85 is roughly 20% high. Suggest 0.7 (sensitivity range 0.5–0.9) and allow for heteroscedasticity, since SEm is lower in MCI.

### 19. ARIA-E by APOE ε4 (for documentation; the model has no side-effect module)

| Trial and regimen | Non-carrier | Heterozygote | Homozygote | Overall | Source |
|---|---|---|---|---|---|
| Donanemab TB2, 76 wk (700 mg ×3, then 1400 mg) | 40/255 (15.7%) vs placebo 2/250 (0.8%) | 103/452 (22.8%) vs 9/474 (1.9%) | 58/143 (40.6%) vs 5/146 (3.4%) | 205 (24.0%) vs 18 (2.1%) | Sims 2023 Table 3 |
| Lecanemab Clarity AD core, 18 mo | 15/278 (5.4%) vs placebo 1/286 (0.3%) | 52/479 (10.9%) vs 9/478 (1.9%) | 46/141 (32.6%) vs 5/133 (3.8%) | 113/898 (12.6%) vs 15 (1.7%) | Eisai briefing (fda.gov/media/169264); Honig LS et al. *Alzheimers Res Ther* 2024;16:105, doi:10.1186/s13195-024-01441-8, Table 2 |
| Donanemab TB6, 52 wk, standard regimen (Regimen 1) | 11/72 (15.6%) | 27/112 (25.0%) | 12/21 (57.1%) | 50/207 (24.9%) | Kisunla label 7/2025, Table 10 (Kaplan-Meier) |
| Donanemab TB6, 52 wk, modified titration (Regimen 2, now recommended) | 10/75 (13.8%) | 18/115 (16.4%) | 5/21 (24.4%) | 33/212 (16.2%) | Kisunla label 7/2025, Table 10 |

- **Labels report *any* ARIA (E or H) by genotype:**
  - Kisunla (TB2): 25%, 36% and 55% vs placebo 12%, 13% and 22% (non-carrier, heterozygote, homozygote).
  - Leqembi (Clarity AD): 13%, 19% and 45% vs placebo 4%, 9% and 22%.
- **Symptomatic ARIA-E:**
  - donanemab 4%, 7% and 8%;
  - lecanemab 1%, 2% and 9%.
- In TB2 the genotype rows sum to 201 cases, vs 205 overall; the label quotes 201/853.

## Sources that could not be accessed
- **JAMA Supplement 3 for Sims 2023 (eTables 4–6 and 10):** PMC PDF behind reCAPTCHA; jamanetwork.com behind Cloudflare.
- **NEJM full text for van Dyck 2023:** HTTP 403. The PubMed abstract, FDA label, FDA and Eisai briefing documents, and Honig 2024 were used instead.
- **Wiley page for Lansdall 2024:** HTTP 403; read through Europe PMC.
- **Nature page for Ossenkoppele 2025:** login redirect; read through Europe PMC.
- **Biogen investor pages:** HTTP 403; BioSpace and BioArctic copies of the releases were used.
