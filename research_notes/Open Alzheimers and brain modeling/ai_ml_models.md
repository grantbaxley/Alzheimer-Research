# Open AI/ML Models, Foundation Models, and Toolkits for Alzheimer's Disease (as of Oct 2026)

Scope note: These notes catalog freely available code and weights. Licenses were checked on primary repository or model-card pages where possible. Performance numbers are the authors' own claims unless noted. Items I could not verify in this session are listed under Gaps rather than stated as fact.

Vetting method (requested by user): Each section ends with a "Vetting assessments" sub-heading under Inferences. It rates every model on five criteria:
- (PR) Peer-reviewed?
- (EXT) Externally validated on an independent cohort?
- (AVAIL) Are the weights or code actually available and runnable? This was checked only by reading repo pages, not by running the code.
- (CRIT) Known critiques or failed replications.
- (LIC) License limits.

Each assessment also lists RED FLAGS and "To verify". Default stance: no claim below has been independently reproduced by us. Every model needs to be re-run on held-out data with subject-level, site-aware splits before any number is trusted.

Generic verification protocol applied to every item (referenced as "STD-VERIFY"):
1. Pin the exact commit or weights hash and record the license.
2. Run the provided inference on a cohort that was not used in pretraining or training. Examples: train on ADNI and test on NACC, AIBL, OASIS-3 or A4/HABS. Pretraining-set overlap must be checked.
3. Use subject-level splits with one subject in exactly one fold. Keep visits of the same subject together. Fit preprocessing and feature selection inside the folds.
4. Compare against simple baselines: logistic regression or SVM on FreeSurfer/FastSurfer volumes, hippocampal volume alone, age+APOE, and PCA/HVG for single-cell.
5. Report calibration and subgroup performance by site, scanner, sex, race and ethnicity, and amyloid status.
6. Check for confounds such as site, scanner, recording conditions and age.

## Q1. Open imaging models and toolkits for AD (preprocessing, segmentation, brain age, MRI/PET foundation models)

### Takeaway
The mature, permissively licensed backbone of open AD neuroimaging is the pipeline layer: Clinica (MIT), ClinicaDL, FastSurfer (Apache-2.0) and SynthSeg (Apache-2.0). Newer 3D brain-MRI foundation models are a different story. BrainIAC (Nature Neuroscience 2026) is open-weights but restricted to non-commercial academic use, and BrainSegFounder releases code and weights but is oriented toward segmentation. Brain-age models such as pyment/SFCN are mostly released under CC-BY-NC. I found no open-weights amyloid or tau PET foundation model.

### Cited Findings

**Pipelines and preprocessing**
- Clinica (ARAMIS Lab) is distributed under the MIT License. It processes BIDS-compliant datasets with pipelines for T1w MRI, diffusion MRI and PET (named pipelines include `t1-freesurfer`, `pet-surface` and `statistics-surface`). Its data converters cover ADNI, AIBL, OASIS, OASIS-3, HABS and NIFD. — [Clinica GitHub](https://github.com/aramis-lab/clinica)
- ClinicaDL (published in Computer Methods and Programs in Biomedicine, 2022) is open-source deep learning software built to address three problems: dataset formatting and preprocessing, evaluation contaminated by data leakage, and poor reproducibility. It checks for leakage when a trained network is applied to new data, and it stores the information needed to reproduce results. — [PubMed 35483271](https://pubmed.ncbi.nlm.nih.gov/35483271/)
- ClinicaDL began as the AD-DL codebase for an AD image-classification paper, and some of its functions remain AD-specific. — [ClinicaDL docs v1.6.0](https://clinicadl.readthedocs.io/en/v1.6.0/)
- FastSurfer (Deep-MI) is licensed Apache-2.0. Its modules are:
  - FastSurferVINN: 95-class whole-brain segmentation that mimics FreeSurfer's DKT atlas.
  - CerebNet: cerebellum.
  - HypVINN: hypothalamus, optionally with T2w.
  - Corpus callosum segmentation and shape analysis.
  - recon-surf: surfaces and thickness.

  Volumetric segmentation runs "within minutes" on GPU, and surface reconstruction takes about 20–40 minutes. The surface stream needs a FreeSurfer license file. Hippocampal subfields are not built in; FreeSurfer's subfield tools can be run on FastSurfer output. — [FastSurfer GitHub](https://github.com/deep-MI/FastSurfer)
- SynthSeg (Billot et al.) code is Apache-2.0. Its authors claim it is robust to "any contrast" and "any resolution up to 10mm slice spacing". A `--robust` variant (March 2022) handles low-SNR or low-contrast scans, and SynthSeg 2.0 (June 2022) adds cortical parcellation, automated QC and ICV estimation. It was announced as included in the FreeSurfer development version in October 2021. — [SynthSeg GitHub](https://github.com/BBillot/SynthSeg); [SynthSeg arXiv](https://arxiv.org/pdf/2107.09559)
- The SynthSeg paper states that FreeSurfer yields Dice scores of about 0.85–0.88 across independent T1 datasets. This is a whole-brain figure, not hippocampus-specific. — [SynthSeg arXiv 2107.09559](https://arxiv.org/pdf/2107.09559)
- A 2025 scan-rescan reproducibility benchmark found systematic differences between tools. Across 73 sessions, left hippocampal volume was 5.12±0.12 cm³ with FastSurfer versus 4.58±0.12 cm³ with SynthSeg. Absolute volumes are therefore not interchangeable across tools. — [arXiv 2504.15931](https://arxiv.org/pdf/2504.15931)
- In a study of 1,447 T1 scans, SynthSeg and TigerBx were on par with FreeSurfer aseg and FSL FIRST for hippocampal segmentation accuracy and reproducibility, while running much faster. — [IXICO hippocampus PDF](https://ixico.com/assets/Uploads/Automatic-segmentation-using-deep-learning-for-the-hippocampus.pdf)

**Brain-age models**
- The original SFCN (Peng/Han et al., Oxford) reported MAE = 2.14 y on UK Biobank (N = 14,503) and MAE = 2.90 y in the 2019 Predictive Analysis Challenge. Pretrained weights are released at github.com/ha-ha-ha-han/UKBiobank_deep_pretrain. — [PMC7610710](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7610710/)
- pyment (Leonardsen et al.) provides `multi-2025` (multi-task) and `reg-2025` (SFCN regression) models. On the ds000030 sanity check, the expected MAE is 4.58 (multi) and 5.19 (reg). The model metadata lists a cc-by-nc-4.0 license, meaning non-commercial use only. — [pyment-public GitHub](https://github.com/estenhl/pyment-public)
- An earlier Leonardsen model family (2022) was trained on n = 34,285, with an expected out-of-sample MAE of about 3.9 y for sfcn-reg. It is also released under CC-BY-NC. — [ecosyste.ms listing](https://science.ecosyste.ms/projects/53779)

**MRI foundation models**
- BrainIAC (Tak, Gormosa, Zapaishchykova et al., "A generalizable foundation model for analysis of human brain MRI", Nature Neuroscience 2026, DOI 10.1038/s41593-026-02202-6) is a self-supervised model pretrained on about 49k open-source brain MRIs. The preprint reports 48,519.
  - Downstream tasks: brain age, MCI classification, IDH mutation, glioma survival, MR sequence classification, time-to-stroke and tumor segmentation.
  - License: non-commercial academic research use only; commercial use needs a license from Mass General Brigham.
  - Access: weights are on Dropbox, and a hosted Brainiac Platform is available.

  — [BrainIAC GitHub](https://github.com/AIM-KannLab/BrainIAC); [medRxiv preprint](https://www.medrxiv.org/content/10.1101/2024.12.02.24317992.full.pdf); [Menon Lab blog](https://themenonlab.blog/blog/brainiac-self-supervised-brain-mri-foundation-model)
- The BrainIAC authors claim it outperforms localized supervised training and other pretrained models, especially in low-data and high-difficulty tasks. — [medRxiv preprint](https://www.medrxiv.org/content/10.1101/2024.12.02.24317992.full.pdf)
- BrainSegFounder (Cox, Liu, … Fang; Medical Image Analysis 2024, vol 97, 103301) uses two-stage self-supervised 3D pretraining: first on healthy UK Biobank anatomy, then on disease-related features. It outperformed prior fully supervised winners on BraTS and ATLAS v2.0. Code and pretrained models are at github.com/lab-smile/BrainSegFounder. — [arXiv 2406.10395](https://arxiv.org/html/2406.10395v3); [NSF PAR](https://par.nsf.gov/biblio/10539640-brainsegfounder-towards-foundation-models-neuroimage-segmentation)
- Newer 2026 preprints:
  - "Alcmaeon" (arXiv 2608.08319) is a continually expandable self-supervised brain MRI foundation model. It was trained on more than 425,000 3D volumes and derived maps (UK Biobank structural, diffusion and NODDI), with extensions to neurodegeneration and tumour imaging.
  - "BrainDINO" (arXiv 2604.27277) is a brain-MRI foundation model whose references include ADNI, OASIS and PPMI.

  Open-weights status for both was not confirmed. — [arXiv 2608.08319](https://arxiv.org/html/2608.08319v1); [arXiv 2604.27277](https://arxiv.org/pdf/2604.27277)

**Multimodal AD and dementia diagnosis model (imaging plus clinical)**
- The paper is Xue, Kolachalama et al., "AI-based differential diagnosis of dementia etiologies on multimodal data", Nature Medicine 2024 (DOI 10.1038/s41591-024-03118-z).
  - Data: 51,269 participants from 9 cohorts; the paper reports 10 etiologies, and the repo lists 13 diagnostic categories.
  - Performance: microaveraged AUROC 0.94 for NC/MCI/dementia and 0.96 for etiologies.
  - Code: github.com/vkola-lab/nmed2024 under AGPL-3.0, with an installable `adrd` package, a Hugging Face demo and a MONAI Swin UNETR SSL MRI encoder.
  - Caveat: the README does not state that the trained transformer weights are included. A hotfix dated 04/15/2025 fixed a performance degradation when nhead > 1.

  — [nmed2024 GitHub](https://github.com/vkola-lab/nmed2024); [Columbia bibliography](https://bibliography.cumc.columbia.edu/node/43314)

**PET**
- No open-weights amyloid or tau PET foundation model turned up. The relevant task-specific models are:
  - A 3D U-Net that synthesizes tau PET from MRI, demographics and blood biomarkers (5,191 participants, 13 cohorts), with R = 0.77–0.86 against real tau PET in AD regions.
  - RIED-Net for PiB↔florbetapir amyloid PET harmonization (Alzheimer's & Dementia 2022).
  - A 2025 J Nucl Med MRI-free flortaucipir spatial normalization network, transfer-learned from an amyloid-PET model.

  Weight availability for these was not confirmed. — [bioRxiv tau synthesis](https://www.biorxiv.org/content/10.1101/2022.09.07.507042.full.pdf); [RIED-Net PDF](https://www.public.asu.edu/~jgshah1/assets/documents/Deep%20residual%20inception%20encoder%E2%80%90decoder%20network%20for%20amyloid%20PET%20harmonization.pdf); [JNM](https://jnm.snmjournals.org/node/48430)

### Inferences
- For a commercial or translational project, the permissively licensed stack is Clinica (MIT), FastSurfer (Apache-2.0), SynthSeg (Apache-2.0) and MONAI. BrainIAC, pyment and the nmed2024 framework carry non-commercial or copyleft (AGPL) restrictions that matter for product use.
- Pipelines (Clinica, FastSurfer, SynthSeg) are mature, maintained and widely used. Brain-MRI foundation models are research-grade: BrainIAC is the first to appear in a top journal (2026), and AD is a minor downstream task within it (MCI classification only).
- Hippocampal volumes from different tools differ by about 10%, so tools should not be mixed within a longitudinal or multi-site study.

#### Vetting assessments (imaging)

**Clinica / ClinicaDL**
- Peer review: ClinicaDL was peer-reviewed in CMPB 2022 ([PubMed](https://pubmed.ncbi.nlm.nih.gov/35483271/)).
- External validation: not applicable; these are pipelines, not predictive models.
- Availability: on GitHub; Clinica is MIT ([GitHub](https://github.com/aramis-lab/clinica)).
- Critiques: none found.
- License limits: Clinica wraps third-party tools (FreeSurfer, SPM, ANTs) with their own licenses, which is an inference to check per pipeline.
- Red flags: none.
- To verify: reproduce `t1-linear` outputs on 10 ADNI subjects, and check the ClinicaDL leakage-check output.

**FastSurfer**
- Peer review: yes (NeuroImage 2020; arXiv [1910.03866](https://arxiv.org/pdf/1910.03866)).
- External validation: the authors evaluated on multiple datasets. Independent reproducibility work shows systematic volume offsets versus SynthSeg ([arXiv 2504.15931](https://arxiv.org/pdf/2504.15931)).
- Availability: Apache-2.0, Docker and Singularity. The surface stream needs a FreeSurfer license ([GitHub](https://github.com/deep-MI/FastSurfer)).
- Red flags: absolute volumes are not interchangeable with FreeSurfer or SynthSeg.
- To verify: scan-rescan ICC on in-house data, and agreement with FreeSurfer on hippocampus and entorhinal cortex in AD cases (atrophied brains are the hard case).

**SynthSeg**
- Peer review: yes; the repo directs citations to Medical Image Analysis and PNAS 2023 ([GitHub](https://github.com/BBillot/SynthSeg)).
- External validation: the authors tested on heterogeneous clinical scans ([arXiv 2209.02032](https://arxiv.org/pdf/2209.02032)). Independent hippocampal comparisons found it on par with aseg and FIRST ([IXICO](https://ixico.com/assets/Uploads/Automatic-segmentation-using-deep-learning-for-the-hippocampus.pdf)).
- Availability: Apache-2.0.
- Critiques: the authors themselves note the original model "sometimes falters" on low-SNR or low-contrast scans, which is why `--robust` exists.
- Red flags: the "any contrast, any resolution" claim is the authors'. Quality control is still required, using the built-in QC scores.
- To verify: run on clinical 2D FLAIR or thick-slice scans versus 3D T1 from the same subjects.

**SFCN (Peng et al.) brain-age**
- Peer review: yes (Medical Image Analysis; [PMC7610710](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7610710/)).
- External validation: the PAC 2019 challenge, MAE 2.90 y, is an independent test.
- Availability: weights on GitHub.
- Critiques: MAE of 2.14 y holds within the UK Biobank. Brain age is known to be scanner- and site-sensitive (generic concern; no AD-specific critique located).
- Red flags: a low MAE on healthy UKB does not imply AD sensitivity. The brain-age gap is also age-confounded, so a bias correction is needed.
- To verify: test MAE on ADNI and NACC controls, compute the bias-corrected brain-age gap in AD vs CN vs MCI, and compare its AUC to hippocampal volume alone.

**pyment (Leonardsen)**
- Peer review: the 2022 models are published.
- External validation: no AD-specific results on the repo ([GitHub](https://github.com/estenhl/pyment-public)). The sanity-check MAE is 4.58–5.19 on ds000030, which is worse than the UKB figures.
- License limits: CC-BY-NC-4.0, non-commercial only.
- Red flags: the MAE varies a lot across datasets.
- To verify: STD-VERIFY on AD cohorts.

**BrainIAC**
- Peer review: yes (Nature Neuroscience 2026, [GitHub citation](https://github.com/AIM-KannLab/BrainIAC)).
- External validation: not confirmed. The full preprint could not be retrieved (HTTP 403), so I could not check whether the downstream MCI test sets are independent cohorts or whether pretraining scans overlap with downstream test scans.
- Availability: weights on Dropbox and a hosted platform. Not run.
- License limits: non-commercial academic only; commercial use needs a Mass General Brigham license.
- Critiques: none found.
- Red flags:
  - AD is represented only as MCI classification.
  - Weights hosted on Dropbox are a durability and versioning risk.
  - Pretraining on ~49k "open-source" MRIs very likely includes ADNI/OASIS. This is an inference, and it would make leakage into AD downstream tests plausible if they are not explicitly excluded.
- To verify: obtain the pretraining subject list, de-duplicate it against the AD test cohort, run STD-VERIFY, and compare with a FastSurfer-volumes+logistic-regression baseline.

**BrainSegFounder**
- Peer review: yes (Medical Image Analysis 2024).
- External validation: BraTS and ATLAS benchmarks, which cover tumour and stroke rather than AD ([arXiv](https://arxiv.org/html/2406.10395v3)).
- Availability: GitHub (lab-smile). The license was not checked.
- Red flags: no AD evaluation. Pretraining on UKB "healthy" scans makes it unproven for AD atrophy.
- To verify: check the license, then fine-tune for hippocampal segmentation or AD classification with STD-VERIFY.

**Alcmaeon and BrainDINO (2026 preprints)**
- Peer review: no; arXiv preprints.
- External validation: unknown.
- Availability: unknown.
- Red flags: unreviewed, and the weights status is unknown.
- To verify: confirm the code and weights release, then run STD-VERIFY.

**nmed2024 (Xue/Kolachalama)**
- Peer review: yes (Nature Medicine 2024).
- External validation: yes. The repo describes internal NACC testing with external validation on ADNI and FHS, plus comparison against clinicians ([GitHub](https://github.com/vkola-lab/nmed2024)).
- Availability: code is AGPL-3.0, and a HF demo exists. Downloadable trained weights are not stated, and the 04/2025 hotfix changes model behavior when nhead > 1.
- License limits: AGPL is copyleft, so network use triggers source disclosure.
- Red flags:
  - NACC-dominant training may encode NACC-specific diagnostic conventions.
  - The microaveraged AUROC of 0.94/0.96 can mask poor performance on rare etiologies.
- To verify: obtain the weights or retrain, reproduce the per-etiology (not micro-averaged) AUROCs on ADNI and FHS, and test on a non-US cohort.

**Tau-PET synthesis U-Net, RIED-Net, JNM tau normalization**
- Peer review: RIED-Net was published (A&D 2022). The tau-synthesis paper was a preprint when retrieved.
- External validation: RIED-Net used a 46-subject external set, which is small.
- Availability: weights not confirmed.
- Red flags:
  - Synthetic tau PET (R 0.77–0.86) is not a substitute for real PET in diagnosis.
  - A synthesized image can hallucinate typical AD patterns from MRI atrophy plus plasma markers. This is an inference.
- To verify: test on an independent tracer, scanner, and population, and run a Braak-stage concordance analysis.

### Gaps
- Not verified this session:
  - MONAI Model Zoo AD-specific bundles.
  - BrainAGE (Franke/Gaser, CAT12) license and current distribution.
  - brainageR.
  - FreeSurfer 8.x release details, including whether `mri_synthseg` and SynthSeg-based recon are in stable releases.
  - Named 2024–2025 models (BrainMVP, AnatCL, SAM-Brain3D, BrainFM). A search did not surface them.
- BrainIAC's per-task AD/MCI performance numbers were not in the README; check the paper.
- Whether nmed2024 trained weights are downloadable (beyond the HF demo) is unclear.
- No independent head-to-head of brain-MRI foundation models on AD/MCI tasks was found.

## Q2. Blood-biomarker, speech and language, EHR, and digital-biomarker models

### Takeaway
Plasma p-tau217 modeling is mostly published as statistical or ML models in BioFINDER and ADNI cohorts, without released packages. The speech domain has the most benchmarked open work (ADReSS/ADReSSo on DementiaBank), but it carries a documented "Clever Hans" confound. EHR and digital-biomarker models are mostly unreleased, small-sample, or both.

### Cited Findings

**Plasma biomarkers**
- BioFINDER-2 ML models combining CSF, plasma and clinical variables predicted continuous amyloid PET with R² = 0.79 (about 7% mean error). Plasma p-tau217 and CSF Aβ42/40 were the top contributors. Plasma-only models reached R² = 0.73 with about 8% MAE. — [PMC12808103](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12808103/); [WUSTL profile](https://profiles.wustl.edu/en/publications/prediction-of-continuous-amyloid-positron-emission-tomography-wit/)
- Karlsson et al. (Alzheimer's & Dementia, Feb 2025) found that tau-PET prediction models including plasma biomarkers were the most accurate, with plasma p-tau217 contributing strongly. — [PMC11846480](https://pmc.ncbi.nlm.nih.gov/articles/PMC11846480/)

**Speech and language**
- On ADReSS-type benchmarks, the reported numbers are:
  - Wav2Vec2: 73.7% accuracy (F1 72.8%).
  - HuBERT: 74.2% (F1 73.6%).
  - Text-only BERT: 83.3%.

  — [arXiv 2502.08862](https://arxiv.org/pdf/2502.08862)
- Winning ADReSS systems reported 85–89.6% accuracy. A bilingual wav2vec2.0 fine-tuned on the 0–1000 Hz band reached 73.9% (ICASSP 2023). — [ICASSP 2023](https://rc.signalprocessingsociety.org/conferences/icassp-2023/spsicassp23vid2757); [Vector Institute](https://vectorinstitute.ai/unveiling-alzheimers-how-speech-and-ai-can-help-detect-disease/)
- Fine-tuned wav2vec 2.0 accuracy varied widely by subset (56.7% on one ADReSS subset, 77.7% on ADReSSo). Embedding-only approaches were more generalizable, and the best ADReSSo model beat the acoustic baseline by 2.8%. — [arXiv 2106.01555](https://arxiv.org/pdf/2106.01555); [UBA ICC](https://icc.fcen.uba.ar/?p=2309)
- LLM chain-of-thought approaches to speech-based AD detection appeared in 2025. — [arXiv 2506.01683](https://arxiv.org/pdf/2506.01683)

**EHR risk models**
- A NeurIPS 2025 paper compared statistical, GNN and LLM approaches for predicting dementia 5 years before diagnosis from UK Biobank medical history (n = 9,537). The listing shows no code link. — [NeurIPS 2025](https://neurips.cc/virtual/2025/132360)
- Stern & Linial (GeroScience 2025) built a CatBoost model on ICD-10 codes, APOE-ε4 and modifiable risk factors. It reached ROC-AUC 0.773 (2,878 AD cases vs 72,366 controls). Vascular dementia models outperformed AD models. — [UK Biobank publication page](https://www.ukbiobank.ac.uk/publications/integrative-machine-learning-approach-to-risk-prediction-for-dementia-and-alzheimers-disease/)
- A 2025 study trained on UK Biobank and externally validated in HUNT compared multi-state models, RSF, CatBoost and DeepHit. It reached AUC 0.785 at 3 y and 0.776 at 5 y. — [medRxiv 2025.06.02.25328770](https://www.medrxiv.org/content/10.1101/2025.06.02.25328770)
- The UKB Dementia Risk Score (Anatürk et al.) is a LASSO model: AUC 0.79 on the UKB hold-out and 0.83 in Whitehall II. — [Oxford Health ORKA](https://www.oxfordhealth.nhs.uk/orka/title/development-and-validation-of-a-novel-dementia-risk-score-in-the-uk-biobank-cohort/); [PMC9519470](https://pmc.ncbi.nlm.nih.gov/articles/PMC9519470)

**Digital biomarkers**
- TechSANS (UT Austin, 2026; n = 21 adults aged ≥65) used passive iOS sensing. Poorer memory was associated with slower typing, more typing errors, slower walking and higher gait asymmetry. — [PMC12784374](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12784374/)
- Neurokeys keystroke dynamics (JMIR 2024; n = 111, Korea) reported that inter-key latency gave 97.9% sensitivity and 96.9% specificity for MCI, outperforming MoCA-K. This is unreplicated and self-reported. — [JMIR 2024 e59247](https://jmir.org/2024/1/e59247/PDF)

### Inferences
- In this domain, "open" usually means the method is published and the data is accessible on request (DementiaBank, UK Biobank, ADNI), not that a ready-to-run model is released. Speech is the exception: models are typically wav2vec2, HuBERT, BERT or Whisper backbones (themselves open) fine-tuned on DementiaBank.
- High reported accuracies in keystroke and digital-biomarker studies come from very small samples and should be treated as hypothesis-generating.

#### Vetting assessments (fluid, speech, EHR, digital)

**BioFINDER plasma/CSF to amyloid-PET ML**
- Peer review: yes ([PMC12808103](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12808103/)).
- External validation: partial. BioFINDER-1 (n = 238) was used alongside BioFINDER-2, but both are from the same Swedish research group, so this is not a fully independent population.
- Availability: no released code or weights found.
- Red flags:
  - Assay-specific: plasma p-tau217 values differ by platform (Lilly MSD, ALZpath Simoa, Fujirebio and others). A model trained on one assay will not transfer. This is an inference based on known assay heterogeneity and was not sourced here.
  - Research-cohort populations.
- To verify: refit using the user's own assay, validate in a cohort of different ancestry and in a primary-care setting, and check calibration of the predicted centiloid.

**Karlsson 2025 tau-PET prediction**
- Peer review: yes (A&D).
- External validation, availability and red flags: same as the BioFINDER models above.

**ADReSS/ADReSSo speech models (wav2vec2, HuBERT, BERT)**
- Peer review: mostly conference papers (INTERSPEECH, ICASSP) and arXiv.
- External validation: rarely. Accuracy swings from 56.7% to 77.7% across subsets ([UBA ICC](https://icc.fcen.uba.ar/?p=2309)).
- Availability: the backbones are open, but fine-tuned checkpoints are rarely released.
- Critiques: the Clever Hans study found that silence-only segments of Pitt/DementiaBank give nearly 100% accuracy ([arXiv 2406.07410](https://arxiv.org/abs/2406.07410)).
- License limits: DementiaBank requires TalkBank membership. This is general knowledge and was not verified here.
- RED FLAGS:
  - Recording-condition confound.
  - Tiny test sets: ADReSS has about 156 speakers in total; the exact size was not verified this session.
  - Single picture-description task, English only.
- To verify:
  - Run silence-only and noise-only ablations.
  - Use ADReSS-preprocessed audio or re-record under matched conditions.
  - Test cross-corpus, for example train on Pitt and test on ADReSS-M or another language.
  - Use amyloid- or biomarker-confirmed labels instead of clinical diagnosis.

**UK Biobank EHR models (NeurIPS 2025, Stern & Linial, UKB→HUNT survival models, UKB-DRS)**
- Peer review: NeurIPS, GeroScience and UKB-DRS are peer-reviewed. The UKB→HUNT study was a medRxiv preprint when found.
- External validation:
  - UKB-DRS: yes, Whitehall II (AUC 0.83).
  - UKB→HUNT model: yes, HUNT.
  - Others: not found.
- Availability: no code links found.
- Red flags:
  - Modest AUCs of about 0.77–0.79.
  - UKB "healthy volunteer" bias.
  - ICD-coded dementia has low sensitivity.
  - Reverse causation: prodromal symptoms appear in the 5-year look-back window.
- To verify: re-implement using a frozen feature list, exclude codes recorded within 1–2 years before diagnosis, validate in a health-system EHR, and run decision-curve analysis.

**Digital biomarkers (TechSANS, Neurokeys)**
- Peer review: yes.
- External validation: no.
- Availability: no open models found.
- RED FLAGS:
  - Very small samples (n = 21 and n = 111).
  - 97.9% sensitivity / 96.9% specificity is implausibly high for keystroke-based MCI detection without replication.
- To verify: an independent prospective cohort with pre-registered features and a held-out site.

### Gaps
- I did not find a released, downloadable plasma p-tau217 prediction model or calculator with an open license. A follow-up search could check GitHub for BioFINDER or ADNI-derived code.
- No authoritative, current ADReSS/ADReSSo leaderboard was found, and the TAUKADIAL 2024 challenge results were not checked.
- Open EHR foundation models (e.g., CEHR-BERT, Foresight, ETHOS) and AD-specific EHR model releases were not verified in this session.

## Q3. Biology foundation models useful for AD (single-cell, protein, DNA) and AD-specific applications

### Takeaway
Licenses vary widely across these model families:
- Permissive: Geneformer (Apache-2.0), scGPT (MIT, including a 13.2M-cell brain checkpoint), Boltz-2 (MIT), OpenFold3 (Apache-2.0, gated sign-up), Evo 2 (Apache-2.0 code, weights on HF) and Chai-1 (Apache-2.0 per the repo; one secondary source disagrees).
- Restricted: AlphaFold 3 weights (obtained directly from Google under separate weights terms), AlphaGenome (non-commercial only, no clinical use, no training other models) and ESM3-open (non-commercial).

AD-specific in silico perturbation work with these models is sparse and mostly preprints or theses. Zero-shot single-cell FM performance is often no better than simple baselines.

### Cited Findings

**Single-cell foundation models**
- Geneformer is licensed Apache-2.0.
  - Versions: V1-10M (2021, about 30M cells) and V2-104M / V2-316M (Dec 2024, Genecorpus-104M). V2-316M is the default, and there is also a cancer-tuned V2.
  - In silico perturbation: deletion or overexpression, runnable zero-shot or with fine-tuned models.
  - Therapeutic-target validation: in silico treatment candidates for cardiomyopathy were validated in iPSC cardiomyocytes.

  — [Geneformer Hugging Face](https://huggingface.co/ctheodoris/Geneformer); [Geneformer docs](https://geneformer.readthedocs.io/en/latest/geneformer.in_silico_perturber.html)
- scGPT (Bowang Lab) is licensed MIT. Checkpoints include whole-human (33M normal cells), brain (13.2M brain cells), blood, heart, lung, kidney, pan-cancer and a continual-pretrained zero-shot model. — [scGPT GitHub](https://github.com/bowang-lab/scGPT)
- AD-specific applications found:
  - Mix-Geneformer (arXiv 2507.07454) simulated an AD shift in healthy human cells by overexpressing S100B, HSPB1 and HSP90AA1, producing a "robust transition toward the AD condition".
  - Reverse-Gene-Finder (arXiv 2502.03938) applied Gaussian-noise perturbation of AD gene-token embeddings with causal tracing to nominate causal genes.
  - A Chalmers master's thesis fine-tuned Geneformer on ROSMAP snRNA-seq. It classified cell types well but generalized poorly to patient-level AD classification.

  — [arXiv 2507.07454](https://arxiv.org/pdf/2507.07454); [arXiv 2502.03938](https://arxiv.org/pdf/2502.03938); [Chalmers thesis](https://odr.chalmers.se/items/fcef7244-0cb8-43c0-9d03-f9084d14cdf9/full)
- Limitations:
  - Kedzierska et al. (Genome Biology) found that zero-shot Geneformer and scGPT embeddings underperform scVI, Harmony and even HVG selection, including on data close to pretraining conditions.
  - A later 13-model benchmark found that PCA often matches or beats single-cell FMs in zero-shot settings.
  - PertEval-scFM (NeurIPS 2024) found that scFM embeddings do not consistently beat baselines for perturbation-effect prediction, especially under distribution shift.

  — [bioRxiv 2023.10.16.561085](https://www.biorxiv.org/content/10.1101/2023.10.16.561085.full.pdf); [Genome Biology s13059-025-03574-x](https://biomedcentral-genomebiology.publicaciones.saludcastillayleon.es/counter/pdf/10.1186/s13059-025-03574-x.pdf); [PertEval-scFM](https://neurips.cc/virtual/2024/102821)
- Ahlmann-Eltze, Huber & Anders (Nature Methods, Aug 2025; DOI 10.1038/s41592-025-02772-6) benchmarked five foundation models, including scGPT and scFoundation, plus GEARS and CPA, on predicting transcriptome changes after single or double perturbations. None beat deliberately simple baselines (no-change and additive models). Analysis code is on GitHub. — [PMC12328236](https://pmc.ncbi.nlm.nih.gov/articles/PMC12328236/); [code](https://github.com/const-ae/linear_perturbation_prediction-Paper)

**Protein and structure models**
- AlphaFold 3:
  - Code: Apache-2.0.
  - Weights: governed by a separate WEIGHTS_TERMS_OF_USE and Prohibited Use Policy, and may only be used if received directly from Google. Variants include SynthID-watermarked and AF3-LA (leaving-atom).
  - Commercial route: Google Cloud.
  - AlphaFold Server is non-commercial, and outputs are not for clinical use.

  — [AlphaFold 3 GitHub](https://github.com/google-deepmind/alphafold3)
- Secondary sources describe the AF3 weights as academic-only with no commercial use. — [implicator.ai](https://implicator.ai/when-google-locked-the-door-three-mit-students-picked-the-lock); [BioPharmaTrend](https://www.biopharmatrend.com/news/alphafold3-goes-open-source-1017/)
- Boltz-2: code and weights are MIT (PyPI `boltz`, github.com/jwohlwend/boltz). Boltz-1 was released fully open (code, weights, training data). Sources disagree on Boltz-1's license (MIT vs Apache-2.0). — [Scaling Biotech](https://scalingbiotech.substack.com/p/open-source-protein-models-openfold); [implicator.ai](https://implicator.ai/when-google-locked-the-door-three-mit-students-picked-the-lock)
- OpenFold3 (AlQuraishi Lab / OpenFold Consortium) is a reproduction of AlphaFold3 under Apache-2.0, for academic and commercial use. The weights are on Hugging Face behind an auto-approved access form. NVIDIA NIM lists OpenFold3 v1.0.0 with a release date of 13 March 2026. — [OpenFold3 HF card](https://huggingface.co/OpenFold/OpenFold3/blob/refs%2Fpr%2F12/README.md); [NVIDIA NIM](https://docs.api.nvidia.com/nim/reference/openfold-openfold3)
- Chai-1: the official repo says code and weights are Apache-2.0 for academic and commercial use. A third-party overview says non-commercial; the repo is more authoritative. — [chai-lab GitHub mirror](https://github.com/aiproteins/chai-lab); [nextomoro](https://nextomoro.com/chai-1/)
- ESM3-open (1.4B) carries a non-commercial license with gated download. The 7B and 98B models are available via the EvolutionaryScale Forge API. — [HF esm3-sm-open-v1](https://huggingface.co/EvolutionaryScale/esm3-sm-open-v1); [PyPI esm](https://pypi.org/project/esm)

**DNA models**
- Evo 2 (Arc Institute):
  - License: code is Apache-2.0.
  - Sizes: 1B, 7B, 20B and 40B checkpoints on HF (arcinstitute).
  - Context: 1M for 7B/20B/40B and 8K for the base models.
  - Demo: zero-shot BRCA1 variant-effect notebook.

  An NVIDIA BioNeMo card mentions the NVIDIA Open Model License, so the weights license should be confirmed. — [Evo 2 GitHub](https://github.com/ArcInstitute/evo2); [NVIDIA model card](https://build.nvidia.com/arc/evo2-40b/modelcard)
- AlphaGenome: code is Apache-2.0. Weights (Kaggle/HF) are under model terms of use that allow only non-commercial organizations and bar commercial use (including research for companies), clinical use, and training other ML models. — [AlphaGenome terms](https://deepmind.google.com/science/alphagenome/terms); [ScanCode license entry](https://scancode-licensedb.aboutcode.org/alphagenome-model-tou-2025.html)

### Inferences
- For AD target work (e.g., microglial TREM2/APOE pathways, ROSMAP/SEA-AD snRNA-seq), the most practical open route is Geneformer V2 or scGPT-brain plus in silico perturbation. Given the benchmark evidence, results should be validated against simple baselines and with wet-lab or orthogonal genetic evidence.
- For structural work on Aβ, tau, APOE or TREM2 ligands, Boltz-2, OpenFold3 and Chai-1 are the commercially usable alternatives to AF3 weights.

#### Vetting assessments (biology foundation models)

**Geneformer V1/V2**
- Peer review: yes; the original Nature 2023 paper is well established (citation not fetched this session).
- External validation for AD: none peer-reviewed. The AD uses are a preprint (Mix-Geneformer), an arXiv paper (Reverse-Gene-Finder) and a master's thesis that failed at patient-level ROSMAP classification ([Chalmers](https://odr.chalmers.se/items/fcef7244-0cb8-43c0-9d03-f9084d14cdf9/full)).
- Availability: Apache-2.0 on HF.
- Critiques:
  - Zero-shot embeddings underperform scVI, Harmony and HVG ([Kedzierska et al.](https://www.biorxiv.org/content/10.1101/2023.10.16.561085.full.pdf)).
  - Perturbation prediction from FMs does not beat linear baselines ([Ahlmann-Eltze 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12328236/)). Geneformer itself was not confirmed as one of the five models tested.
- RED FLAG: in silico AD target nominations are hypotheses, not evidence.
- To verify:
  - Benchmark against no-change, additive and PCA baselines.
  - Check concordance with AD GWAS genes (e.g., TREM2, APOE, BIN1) as positive controls.
  - Validate with CRISPR in iPSC-microglia.

**scGPT (whole-human and brain checkpoints)**
- Peer review: yes (Nature Methods 2024; citation not fetched this session).
- External validation for AD: none found.
- Availability: MIT, checkpoints on GitHub ([GitHub](https://github.com/bowang-lab/scGPT)).
- Critiques:
  - Zero-shot underperformance (Kedzierska).
  - Perturbation prediction does not beat simple baselines (Ahlmann-Eltze 2025, where scGPT was explicitly tested).
- RED FLAG: claims of perturbation prediction ability.
- To verify: same as Geneformer. For SEA-AD/ROSMAP cell-type annotation, compare against scVI + kNN.

**AlphaFold 3**
- Peer review: yes (Nature 2024; not fetched).
- Availability: weights only directly from Google, under separate terms ([GitHub](https://github.com/google-deepmind/alphafold3)).
- License limits: restrictive. Commercial use only via Google Cloud, no clinical use, and model outputs are watermarked in the SynthID variant.
- Red flags:
  - Intrinsically disordered proteins: tau and Aβ monomers are disordered, and structure predictors give low-confidence or misleading outputs for them. This is an inference from general knowledge and was not sourced here.
  - Fibril polymorphs are not predicted reliably.
- To verify: compare against cryo-EM fibril structures (PDB) for tau and Aβ, and check pLDDT/PAE.

**Boltz-2**
- Peer review: was a preprint at release; current status not verified.
- Availability: MIT code and weights.
- Critiques: affinity-prediction claims have not been independently checked here.
- To verify: retrospective docking/affinity benchmark on known BACE1, GSK3β and other AD-target ligands with held-out chemotypes.

**OpenFold3**
- Status: v1.0.0 released March 2026 per NVIDIA ([NIM](https://docs.api.nvidia.com/nim/reference/openfold-openfold3)).
- Availability: Apache-2.0, gated sign-up.
- Red flags: a "preview" version preceded 1.0, so check which weights are in use.
- To verify: benchmark versus AF3 and Boltz-2 on the same targets.

**Chai-1**
- License conflict: the repo says Apache-2.0, a secondary source says non-commercial. Read the LICENSE file before use.

**ESM3-open**
- License limits: non-commercial, gated ([HF](https://huggingface.co/EvolutionaryScale/esm3-sm-open-v1)).
- Red flag: the larger models are only available through an API.

**Evo 2**
- Peer review: Nature, per secondary coverage ([BioPharmaTrend](https://www.biopharmatrend.com/news/evo-2-open-source-ai-model-for-generative-genomics-validated-and-published-in-nature-1519/)).
- License limits: code is Apache-2.0, but the weights license is ambiguous (NVIDIA Open Model License is mentioned on the NVIDIA card).
- Red flags: the zero-shot variant-effect demo uses BRCA1, so no AD-specific validation exists. Noncoding AD GWAS variant scoring is untested.
- To verify: score known AD-associated coding variants (e.g., TREM2 R47H, APOE ε4 vs ε3, PSEN1 pathogenic vs benign ClinVar) as positive and negative controls.

**AlphaGenome**
- License limits: non-commercial organizations only. No commercial or clinical use, and no training of other models ([terms](https://deepmind.google.com/science/alphagenome/terms)).
- RED FLAG: these terms may block use in any company-affiliated project, and they block distillation.

### Gaps
- Not verified this session:
  - UCE (Universal Cell Embeddings) and CellFM licenses and checkpoints.
  - ESM2 and ESMFold licenses.
  - Enformer and Borzoi.
- No peer-reviewed, experimentally validated AD target from Geneformer or scGPT in silico perturbation was found. A microglia-specific AD perturbation study did not surface.
- The current exact AF3 weights terms (the WEIGHTS_TERMS_OF_USE.md text) were not retrieved.

## Q4. LLM and agent systems for AD research (knowledge graphs, agents)

### Takeaway
AlzKB, an open AD knowledge graph with about 119k entities and 1.3M relations in its published version, now backs LLM drug-repurposing agents (ESCARGOT, 2025). Stanford's open-source Biomni agent has an AD-focused variant, Biomni-AD (Mount Sinai and Stanford), which won the 2026 Alzheimer's Insights AI Prize. Evidence for both is mostly author-reported.

### Cited Findings
- AlzKB (Moore lab; JMIR 2024) is built from 22 external sources using an OWL2 ontology. It has 118,902 entities and 1,309,527 relationships, is freely available on the web, and has been used for drug repurposing and target proposals. — [PMC11066745](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11066745/); [PubMed 38635981](https://pubmed.ncbi.nlm.nih.gov/38635981/)
- In "Drug repurposing for AD using a graph-of-thoughts based LLM" (BioData Mining, Aug 2025), AlzKB significantly improved repurposing outcomes. ESCARGOT, which pairs a graph-of-thoughts LLM with AlzKB, improved performance further while reducing the need for Cypher or coding skills. — [PMC12326721](https://pmc.ncbi.nlm.nih.gov/articles/PMC12326721/)
- A trade article describes a newer AlzKB version with about 234k nodes and 1.67M edges and a natural-language-to-graph layer. This is secondary and unverified. — [BioPharmaTrend](https://www.biopharmatrend.com/post/1226-how-ai-graphs-and-graphrag-are-set-to-revolutionize-alzheimers-gene-research-and-treatment)
- Biomni (Stanford, Leskovec lab) is a general-purpose, open-source biomedical agent with a web interface. It combines LLM reasoning, retrieval-augmented planning and code execution, and a secondary report says it was tested on more than 400 tasks. — [Stanford HAI](https://hai.stanford.edu/news/stanford-scientists-build-an-ai-lab-partner); [SourcePulse listing](https://www.sourcepulse.org/projects/8382188)
- Biomni-AD (Mount Sinai team led by Kuan-lin Huang, with Stanford) won a share of the Alzheimer's Insights AI Prize in 2026; the prize was increased from $1M to $2M across two teams. It is described as a co-scientist built on a curated AD data lake with more than 180 specialized tools and human-approved research plans. — [Mount Sinai press release 2026](https://www.mountsinai.org/about/newsroom/2026/mount-sinai-scientists-recognized-with-global-ai-prize-for-novel-alzheimers-disease-research-platform); [Newswise](https://www.newswise.com/articles/mount-sinai-scientists-recognized-with-global-ai-prize-for-novel-alzheimer-s-disease-research-platform)

### Inferences
- The pattern is consistent: a curated AD knowledge graph or data lake, an LLM planner, and tool or code execution. The KG and agent frameworks are open, but the validation of AD-specific insights so far is press-release or self-reported.

#### Vetting assessments (KG and agents)

**AlzKB**
- Peer review: yes (JMIR 2024).
- Availability: freely available on the web.
- Critiques: none found.
- Red flags:
  - A KG reflects literature bias, so heavily studied genes dominate.
  - Version drift (119k vs 234k nodes) between the paper and later releases.
- To verify: pin the KG version, and run a time-split evaluation (build the KG from pre-2015 data, test whether it predicts later trial-supported repurposing candidates).

**ESCARGOT (AlzKB + LLM)**
- Peer review: yes (BioData Mining 2025).
- External validation: no independent benchmark found.
- Red flags:
  - LLM non-determinism.
  - The evaluation of repurposing "outcomes" may rely on literature already in the KG or LLM training data, which is leakage via pretraining. This is an inference.
- To verify: repeated runs with seeds, temporal holdout, and blinded expert review.

**Biomni / Biomni-AD**
- Peer review: Biomni was a preprint per press coverage; journal status not verified. Biomni-AD is a prize announcement only ([Mount Sinai](https://www.mountsinai.org/about/newsroom/2026/mount-sinai-scientists-recognized-with-global-ai-prize-for-novel-alzheimers-disease-research-platform)).
- Availability: base Biomni is open source. The release status of Biomni-AD is unknown.
- RED FLAGS:
  - Prize and press claims are not evidence of validated insights.
  - Agents can produce plausible but wrong analyses.
- To verify: audit agent-generated analyses by re-running the code by hand, and test reproducibility across runs and LLM versions.

### Gaps
- Not checked this session:
  - Whether Biomni-AD's code and data lake are publicly released (as opposed to base Biomni).
  - Who the second prize-winning team was.
  - Other AD-specific KGs or LLMs (e.g., PrimeKG/TxGNN AD use, AlzheimerRAG, AD-specific LLM fine-tunes).
- No independent benchmark of LLM agents on AD research tasks was found.

## Q5. Known reproducibility issues (data leakage and confounds in AD deep learning)

### Takeaway
Leakage is endemic and well documented:
- Wen et al. (2020) estimated that more than half of surveyed CNN-for-AD papers may have suffered data leakage, and properly evaluated CNNs did not beat an SVM baseline.
- Yagis et al. (2021) showed that slice-level splitting inflates accuracy by 29–55% and can give about 96% accuracy on random labels.
- In speech, the Pitt/DementiaBank corpus has a "Clever Hans" recording bias: silence alone yields near-100% accuracy.

### Cited Findings
- Wen et al. (Medical Image Analysis 2020, arXiv 1904.07773) stated that "more than half of the surveyed papers may have suffered from data leakage". With rigorous evaluation, 3D approaches performed similarly to each other, 2D slice approaches did worse, and the CNNs did not outperform an SVM on voxel features. They released an open-source evaluation framework, the predecessor of ClinicaDL. — [arXiv 1904.07773](https://arxiv.org/abs/1904.07773); [ClinicaDL docs](https://clinicadl.readthedocs.io/en/v1.6.0/)
- Yagis et al. (Scientific Reports 2021) used 2D CNNs on 3D MRI split into slices. Slice-level cross-validation inflated average test accuracy by 30% (OASIS), 29% (ADNI), 48% (PPMI) and 55% (local PD dataset). With randomly labeled OASIS data, slice-level splits gave about 96% accuracy versus 50% with subject-level splits. The effect was most severe for small datasets. Their Table 2 lists prior AD papers reporting 96.85–99.89% accuracy with slice-level splits. — [PMC8604922](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8604922/)
- The "Clever Hans" effect in speech AD detection (arXiv 2406.07410): on the Pitt corpus, models using only silent segments reach nearly 100% accuracy. The same methods give about 80% on other datasets and on preprocessed Pitt recordings, which points to a recording-level bias. — [arXiv 2406.07410](https://arxiv.org/abs/2406.07410)
- ClinicaDL was explicitly designed to prevent leakage, with automatic subject-level splitting and leakage checks. — [PubMed 35483271](https://pubmed.ncbi.nlm.nih.gov/35483271/); [SPIE profile](https://biomedicaloptics.spiedigitallibrary.org/profile/Ravi.HASSANALY-4416533)
- Benchmarks of single-cell FMs (Q3) are another reproducibility caution: zero-shot embeddings frequently fail to beat simple baselines. — [bioRxiv 2023.10.16.561085](https://www.biorxiv.org/content/10.1101/2023.10.16.561085.full.pdf)

### Inferences
- Any AD MRI classifier claiming more than 95% AD-vs-CN accuracy, especially with 2D slices, a Kaggle-style ADNI/OASIS slice dataset, or no subject-level split, should be presumed leaky until shown otherwise.
- Other likely leakage sources follow from the same mechanism: multiple visits per subject across folds, preprocessing or feature selection fit on the full dataset, and site or scanner confounds. Subject-level, site-aware splits and external validation (e.g., NACC→ADNI/FHS, as in nmed2024) are the minimum standard.

#### Red-flag checklist for any AD model the user brings in (derived from the findings above)
1. Reported AD vs CN accuracy above 95% from MRI, or above 90% from speech. Likely leakage or confounding ([Yagis](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8604922/); [Clever Hans](https://arxiv.org/abs/2406.07410)).
2. 2D slice-based models, or no explicit statement that splits are subject-level.
3. Multiple visits per subject with no grouping by subject ID.
4. Normalization, feature selection or hyperparameter tuning done before the train/test split.
5. Test data from the same cohort as training (e.g., ADNI-only) with no independent external cohort.
6. Foundation model pretraining corpus includes the downstream test cohort (ADNI, OASIS, UKB) with no de-duplication.
7. No simple baseline reported (hippocampal volume, SVM on volumes, age+APOE, PCA).
8. Labels are clinical diagnoses only, with no amyloid or tau confirmation, which mixes in non-AD dementias.
9. Micro-averaged metrics hiding minority-class performance.
10. No released weights, or weights on ephemeral hosting (Dropbox), or a license that bars the intended use (NC, AGPL, no-distillation).
11. Performance claims supported only by press releases or prizes.

### Gaps
- Not found:
  - A systematic 2024–2026 audit quantifying leakage in recent AD deep-learning or foundation-model papers.
  - Leakage analyses for 3D CNNs specifically.
  - Site or scanner confound studies for brain-age-gap AD biomarkers.
  - A study of pretraining-data overlap with ADNI/OASIS test sets in MRI foundation models such as BrainIAC.
