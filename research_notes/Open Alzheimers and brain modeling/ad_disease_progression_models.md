# Open computational and mechanistic disease-progression models of Alzheimer's disease (state as of Oct 2026)

Method note: GitHub metadata (license, last push, stars) was pulled live via the GitHub search API on 2026-10-18. Items marked "(prior knowledge, not re-fetched)" are canonical references I am confident in but did not re-open in this session; the report writer may want to spot-check them. Several areas (BioModels entries, QSP code) returned no confirmable open artifacts and are recorded as gaps.

## 1. Data-driven disease progression models (DPMs) with open code

### Takeaway
The open, maintained core of AD data-driven progression modelling is two ecosystems: UCL POND (pySuStaIn, kde_ebm, pyebm, network spreading toolbox; MIT/GPL) and Inria/Paris Brain Institute ARAMIS (Leaspy for disease-course mapping, Clinica/ClinicaDL for data pipelines; BSD-3-Clause-Clear / MIT / custom). pySuStaIn is the most adopted (222 stars, pushed Mar 2026) and Leaspy is under active development (pushed Sep 2026). GP-based models (GPPM, DIVE) exist but are less maintained.

### Cited Findings

**UCL POND group (Event-Based Model family, SuStaIn)**
- `ucl-pond/pySuStaIn`: "Subtype and Stage Inference (SuStaIn) algorithm with an example using simulated data"; MIT license; last push 2026-03-30; 222 stars, 91 forks, 53 open issues; not archived — [GitHub](https://github.com/ucl-pond/pySuStaIn)
- `ucl-pond/kde_ebm` ("Newer version of the KDEEBM code", kernel-density Event-Based Model): GPL-3.0; last push 2025-11-13; 18 stars — [GitHub](https://github.com/ucl-pond/kde_ebm)
- `ucl-pond/ebm` (original EBM code): MIT, archived (last push 2023-07-25) — [GitHub](https://github.com/ucl-pond/ebm)
- `ucl-pond/SuStaInMatlab`: MATLAB SuStaIn implementation [Young+, Nature Communications 2018]; no license declared; last push 2021 — [GitHub](https://github.com/ucl-pond/SuStaInMatlab)
- `88vikram/pyebm` ("A toolbox for Event Based Models", includes discriminative EBM, Venkatraghavan et al.): 30 stars, repo updated 2026-03 — [GitHub](https://github.com/88vikram/pyebm)
- SuStaIn original paper: Young et al., "Uncovering the heterogeneity and temporal complexity of neurodegenerative diseases with Subtype and Stage Inference," Nature Communications 2018 — [Nat Commun](https://doi.org/10.1038/s41467-018-05892-0) (prior knowledge, not re-fetched)
- Major validated AD application of SuStaIn: Vogel et al., "Four distinct trajectories of tau deposition identified in Alzheimer's disease," Nature Medicine 2021 (tau-PET, >1,000 participants across cohorts) — [Nat Med](https://doi.org/10.1038/s41591-021-01309-6) (prior knowledge, not re-fetched)
- pySuStaIn software paper: Aksman et al., "pySuStaIn: a Python implementation of the Subtype and Stage Inference algorithm," SoftwareX 2021 — [SoftwareX](https://doi.org/10.1016/j.softx.2021.100811) (prior knowledge, not re-fetched)
- Review of the whole field: Young, Oxtoby et al., "Data-driven modelling of neurodegenerative disease progression: thinking outside the black box" (Nature Reviews Neurology 2024); arXiv preprint "Data-Driven Disease Progression Modelling" — [arXiv 2211.05786](https://arxiv.org/pdf/2211.05786)
- Teaching material: `ucl-pond/MedICSS-TADPOLE` (MIT) and `ucl-pond/tadpole-medicss` (summer-school projects on TADPOLE) — [GitHub](https://github.com/ucl-pond/MedICSS-TADPOLE)

**ARAMIS Lab (Inria / Paris Brain Institute): Leaspy / Disease Course Mapping**
- `aramis-lab/leaspy` ("LEArning Spatiotemporal Patterns in Python"): BSD-3-Clause-Clear license; repo created on GitHub 2025-02-25 (previously hosted on Inria GitLab); last push 2026-09-17; 29 stars, 21 open issues — [GitHub](https://github.com/aramis-lab/leaspy)
- Leaspy README: models scalar multivariate longitudinal data with "a logistic model, linear, joint or mixture model"; supports fit, personalize, estimate, simulate; Python 3.9–3.13; docs at leaspy.readthedocs.io; core reference Schiratti, Allassonnière, Colliot & Durrleman (JMLR 2017) Bayesian mixed-effects model; newer joint model with latent disease age (Ortholand et al., arXiv:2401.17249, 2024) and mixture model for subtypes (Kaisaridi et al., ISCB 2025) — [GitHub README](https://github.com/aramis-lab/leaspy)
- AD Course Map (Koval et al., Scientific Reports 2021) built with this framework — [Sci Rep](https://doi.org/10.1038/s41598-021-87434-1) (prior knowledge, not re-fetched)
- `aramis-lab/clinica` ("Software platform for clinical neuroimaging studies"; BIDS converters for ADNI/AIBL/OASIS etc., FreeSurfer/SPM/ANTs pipelines): license field "Other" (NOASSERTION); last push 2026-10-02; 293 stars, 137 open issues — [GitHub](https://github.com/aramis-lab/clinica)
- `aramis-lab/clinicadl` ("Open-source Python library for reproducible deep learning in neuroimaging"): MIT; last push 2026-10-16; 191 stars — [GitHub](https://github.com/aramis-lab/clinicadl)
- `aramis-lab/AD-ML` ("Framework for the reproducible classification of Alzheimer's disease using machine learning"): 43 stars, updated 2026-03 — [GitHub](https://github.com/aramis-lab/AD-ML)

**Gaussian-process and spatiotemporal models**
- GPPM (Lorenzi et al. 2017/2019): GP approach jointly modelling imaging and clinical biomarkers "formulated to account for individual random effects and time reparameterization," with uncertainty for staging unseen patients — [arXiv 1701.01668](https://arxiv.org/html/1701.01668); [EURECOM](https://www.eurecom.fr/en/node/4902906)
- Garbarino & Lorenzi extended GP progression with nonlinear dynamical systems of misfolded-protein spread across brain networks, applied to amyloid deposition (stochastic variational inference) — [arXiv 1901.10545](https://arxiv.org/pdf/1901.10545)
- Monotonic GP spatiotemporal DPM for imaging — [arXiv 1902.10952](https://ar5iv.labs.arxiv.org/html/1902.10952)
- `razvanmarinescu/dive` ("Data-Driven Inference of Vertexwise Evolution", vertex-wise cortical progression clustering): 8 stars; repo updated 2025-04 — [GitHub](https://github.com/razvanmarinescu/dive)
- `razvanmarinescu/brain-coloring` (BrainPainter visualisation for progression model outputs): 74 stars — [GitHub](https://github.com/razvanmarinescu/brain-coloring)
- `LemuelPuglisi/BrLP` (Brain Latent Progression; MICCAI 2024 oral; "Enhancing Spatiotemporal Disease Progression Models via Latent Diffusion and Prior Knowledge"; generates future 3D MRIs per individual): 140 stars; updated 2026-10 — [GitHub](https://github.com/LemuelPuglisi/BrLP)

### Inferences
- For a new open project, pySuStaIn (MIT) and Leaspy (BSD-3-Clause-Clear, permissive but note "Clear" variant explicitly excludes patent grants) are the safest permissive bases; kde_ebm is GPL-3.0 (copyleft, constrains re-licensing).
- The natural reuse pattern: Clinica (data harmonisation to BIDS/ClinicaDL) -> EBM/SuStaIn (population ordering and subtypes) -> Leaspy (individual-level continuous trajectories and simulation) -> network spreading (mechanistic interpretation). These components already share ADNI-centric inputs.
- Leaspy's recent move from GitLab to GitHub means GitHub star counts understate its maturity.

### Gaps
- Could not locate a currently maintained public repo for Lorenzi's GPPM (likely on Inria GitLab "GP_progression_model_V2"); not confirmed.
- No license declared for SuStaInMatlab, pyebm (not confirmed), DIVE; reuse terms unclear.
- "pyDPM"/other UCL DPM packages were not found.

## 2. Mechanistic / network models (spreading, ODE cascade, QSP, metabolism, SBML)

### Takeaway
Open mechanistic code exists mainly for connectome-based spreading models (NDM, FKPP, amyloid-weighted FKPP, eNDM/Nexis, SIR agent-based) with MIT licenses; cellular/molecular ODE and QSP models of AD are mostly published as equations or proprietary-platform implementations, with little confirmed SBML/BioModels deposition. An exception is the LCSB astrocyte energy-metabolism model with GitLab code.

### Cited Findings

**Connectome spreading models (tau / amyloid)**
- `ucl-pond/network_spreading_models` (moved from `ethompson93/network_spreading_models`, originally a CMICHACKS 2023 project): MIT; last push 2025-12-02; 13 stars — [GitHub](https://github.com/ucl-pond/network_spreading_models); [original](https://github.com/ethompson93/network_spreading_models)
- Thompson et al. (Alzheimer's & Dementia 2024 conference abstract, "Demonstration of an open-source toolbox for network spreading models: regional amyloid burden promotes tau production in AD"): toolbox implements network diffusion model (NDM), Fisher-Kolmogorov-Petrovsky-Piscounov (FKPP) and weighted-FKPP with regional amyloid weighting the production term; fit to ADNI regional tau-PET and amyloid-PET SUVRs (downloaded Sept 2023) grouped by A/T stage; amyloid weighting improved fit in all groups, significantly only in A+T+; all groups beat null (p<1e-10). Code statement: "All models are available in our toolbox: https://github.com/ethompson93/network_spreading_models" — [PMC11716492](https://pmc.ncbi.nlm.nih.gov/articles/PMC11716492/)
- `ethompson93/multimodal_ndm` (multimodal network diffusion model): 3 stars, updated 2024-11 — [GitHub](https://github.com/ethompson93/multimodal_ndm)
- `Raj-Lab-UCSF/Nexis` ("Code for running the extended Network Diffusion Model (eNDM)", MATLAB): MIT; last push 2025-01-15 — [GitHub](https://github.com/Raj-Lab-UCSF/Nexis); original NDM: Raj, Kuceyeski & Weiner, Neuron 2012 — [Neuron](https://doi.org/10.1016/j.neuron.2011.12.040) (prior knowledge, not re-fetched)
- `DeMONLab-BioFINDER/Xiao_Tau_simulation_SIR` (SIR agent-based tau spreading simulation from the BioFINDER/Vogel group): Python; updated 2026-04 — [GitHub](https://github.com/DeMONLab-BioFINDER/Xiao_Tau_simulation_SIR)
- `ejcorn/tau-spread` (Cornblath et al., network spread of tau in mouse models): updated 2025-09 — [GitHub](https://github.com/ejcorn/tau-spread)
- Fornari et al. (J R Soc Interface 2019), "Prion-like spreading of Alzheimer's disease within the brain's connectome": simulates misfolded protein spread with Fisher-Kolmogorov, heterodimer, and Smoluchowski kinetic models on a weighted graph Laplacian from 418 Human Connectome Project brains — [PMC6833337](https://pmc.ncbi.nlm.nih.gov/articles/PMC6833337); (author attribution from prior knowledge)
- Numerical study of protein misfolding models (FK/heterodimer) in neurodegeneration — [arXiv 2401.15747](https://arxiv.org/pdf/2401.15747)
- Vazquez-Palomo et al. 2026 (arXiv 2603.19829): coupled amyloid-beta/tau Fisher-Kolmogorov in a 3D finite-element framework; supplementary mentions a COMSOL implementation (likely not open) — [arXiv](https://arxiv.org/pdf/2603.19829)
- Graph heterodimer-FK inverse solver calibrated from a single MRI/PET snapshot (Brain Informatics 2025); no code link found — [Brain Informatics](https://braininformatics.springeropen.com/articles/10.1186/s40708-025-00264-z)

**Amyloid cascade / multiscale ODE models**
- Bulai, Ferraresso & Gladiali (J Math Biol 2025): ODE model of Aβ monomers, proto-oligomers, oligomers with optimal control; targeting oligomers more effective than monomers — [PMC12334554](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12334554/); [Springer](https://www.link.springer.com/article/10.1007/s00285-025-02256-3)
- 2024 multiscale ODE model spanning nano (proteins), micro (cell populations) and macro (organ) scales over a 50-year lifespan with amyloid, tau, inflammation, neuronal death — [PMC10995318](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10995318/); sensitivity analysis of a 19-variable, 75-parameter multiscale AD ODE model — [PMC12325246](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12325246/); Frontiers in Neuroinformatics 2025 paper describing it as "a recent and comprehensive multiscale ODE-based model of AD" — [Frontiers](https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2025.1590968/pdf)
- "The amyloid cascade hypothesis and Alzheimer's disease: A mathematical model" (Eur J Appl Math 2020), Smoluchowski-type ODEs from monomer to plaque — [Cambridge](https://www.cambridge.org/core/product/E50BFDFB2F4D59A79FC1F4FC5F5E5385)
- Prion-based AD ODE model — [arXiv 1302.7013](https://arxiv.org/pdf/1302.7013)

**Quantitative systems pharmacology (QSP)**
- Biogen/Applied BioMath QSP model of production, aggregation and inter-compartment transport of Aβ and tau, with plaque-dependent tau hyperphosphorylation driving NFTs (2025 abstract) — [PMC11713532](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11713532/); Certara poster: calibrated with >70 datasets, covers four anti-Aβ mAbs and an anti-tau ASO — [Certara](https://www.certara.com/poster/quantitative-systems-pharmacology-model-for-therapies-targeting-a%ce%b2-and-tau-pathologies-in-alzheimers-disease/)
- Geerts et al. mechanistic QSP on how anti-amyloid therapies affect tau biomarkers and function (Frontiers in Pharmacology) — [Certara publication page](https://www.certara.com/publication/understanding-quantitative-effects-of-anti-amyloid-therapies-on-tau-biomarkers-and-functional-outcome/)
- InSysBio/AbbVie ODE QSP model of intraneuronal pathways regulating toxic protein accumulation (PAGE abstract) — [PAGE](https://www.page-meeting.org/Abstracts/quantitative-systems-pharmacology-model-of-key-intraneuronal-pathways-regulating-toxic-protein-accumulation-in-alzheimers-disease/)
- Applied BioMath NIA grant for AD QSP model development — [Applied BioMath](https://www.appliedbiomath.com/news-resources/news/applied-biomath-llc-awarded-grant-national-institute-aging-nih-development)

**Glia / metabolism**
- Farina et al. (PLoS Comp Biol 2023): mechanistic multiscale reaction-diffusion model of energy metabolism in realistic 3D human astrocyte morphologies from AD and control samples; argues prior ODE models neglect spatial dimensions — [PMC10545114](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10545114/); [bioRxiv](https://www.biorxiv.org/content/10.1101/2022.07.21.500921.full.pdf)
- Code on LCSB GitLab ("contains the code to replicate the results presented in the paper"; Python 3.9.2 + FEniCS 2019.1.0, plus legacy Python 2.7/FEniCS 1.5) — [GitLab](https://gitlab.lcsb.uni.lu/ICS-lcsb/energy-metabolism-model-astrocyte/-/commit/26bb5572e546160167907462fff904de319fa019)

### Inferences
- Network spreading is the most "plug-and-play" mechanistic layer: MIT-licensed Python (UCL) and MATLAB (UCSF) code, validated against ADNI tau-PET at group level; a new project could combine it with SuStaIn subtypes (different epicentres per subtype, as Vogel 2021 suggested) or with Leaspy individual timing.
- QSP models are the most relevant to therapy simulation (anti-Aβ mAbs) but appear to be industry/consultancy-owned; an open project would likely need to re-implement from published equations.
- The 19-variable multiscale ODE model is a candidate for open re-implementation (e.g., in SBML via Tellurium/COPASI) since its equations and parameter tables are published in PMC.

### Gaps
- BioModels: search returned no confirmable curated AD/amyloid entries; I could not verify specific BIOMD IDs (e.g., Proctor et al. Aβ/tau/GSK3 models). Needs a direct BioModels query.
- No open code located for the QSP models (Biogen/Applied BioMath, Certara/Geerts, InSysBio) — likely proprietary.
- Code availability for the 2024 multiscale ODE model and the Brain Informatics graph-HFK solver not confirmed.
- License of the LCSB astrocyte GitLab repo not confirmed.

## 3. Multiscale / "digital twin" models of AD patients

### Takeaway
The main open digital-twin effort is the EBRAINS / The Virtual Brain (TVB) ecosystem, notably the Horizon Europe eBRAIN-Health project (2022–Jul 2026, ~13M EUR), which built TVB-based AD brain twins from MRI/EEG. TVB code is open and actively maintained; peer-reviewed clinical validation of AD twins is not evident.

### Cited Findings
- `the-virtual-brain/tvb-root` ("Main TVB codebase"): license field "Other" (TVB is GPL-3.0-based per project, not confirmed here); last push 2026-10-16; 195 stars, 153 forks — [GitHub](https://github.com/the-virtual-brain/tvb-root)
- eBRAIN-Health: Horizon Europe project launched July 2022, budget almost 13M EUR, coordinated by Charité Berlin, running to July 2026; builds digital twins on The Virtual Brain — [CORDIS](https://cordis.europa.eu/project/id/101058516); [Alzheimer Europe](https://www.alzheimer-europe.org/our-work/current-work/ebrain-health)
- At the EBRAINS Summit, Brussels (8–11 Dec 2025), the team presented TVB digital twins of AD patients' brains combining MRI, EEG and AI, aimed at earlier diagnosis and personalised treatment; mentions simulation of "thousands of multilevel virtual brains" and GDPR-compliant data sharing across ten European units; hundreds of EEG/MEG/neuroimaging datasets made available via EBRAINS — [EBRAINS news 2026](https://ebrains.eu/news-and-events/2026/from-digital-twins-to-telemonitoring-ebrain-health-highlights-from-ebrains)
- Related EU projects: CORDIS project 101147319 (digital-twin related; details not fetched) — [CORDIS](https://www.cordis.europa.eu/project/id/101147319/reporting/fr); UPF "MAXIMIZED" project page — [UPF](https://www.upf.edu/web/cns/projects/-/asset_publisher/zAfKADYSGtBx/content/upcoming-project/maximized)
- Conceptual framing: Wang, Jirsa et al., "Virtual brain twins: from basic neuroscience to clinical use," National Science Review 2024 — [NSR](https://doi.org/10.1093/nsr/nwae079) (prior knowledge, not re-fetched)
- TVB-AD multiscale model linking molecular pathology (Aβ) to large-scale neural mass dynamics: Stefanovski et al., Frontiers in Computational Neuroscience 2019 — [Frontiers](https://doi.org/10.3389/fncom.2019.00054) (prior knowledge, not re-fetched)
- Leaspy's "simulate" function can generate synthetic patient trajectories (a statistical "digital twin" capability) — [GitHub README](https://github.com/aramis-lab/leaspy)
- A curated list of medical world models / patient digital twins exists (2026) — [Awesome-World-Models-for-Healthcare](https://github.com/chengwang96/Awesome-World-Models-for-Healthcare)

### Inferences
- "Digital twin" for AD currently splits into (a) mechanistic brain-network twins (TVB, electrophysiology-focused) and (b) statistical trajectory twins (Leaspy, BrLP image generation). An open project could bridge them by driving TVB regional parameters with Leaspy/SuStaIn-derived stage and network-spreading pathology loads.
- Since eBRAIN-Health ended July 2026, its final deliverables (code, data on EBRAINS) may now be publicly listed; worth checking.

### Gaps
- No peer-reviewed validation of eBRAIN-Health AD twins against outcomes found; final project outputs not located.
- TVB exact license not verified in this session (GitHub reports NOASSERTION).

## 4. Benchmarks / challenges for AD prediction

### Takeaway
TADPOLE (2017–2019) remains the reference prospective benchmark for AD progression forecasting, with code collated in TADPOLE-SHARE; CADDementia covers diagnosis; the NIA PREPARE challenge (2024–2025, DrivenData) is the main newer open challenge but targets early prediction from diverse data rather than biomarker trajectories. I found no dedicated 2024–2026 MICCAI AD progression challenge.

### Cited Findings
- TADPOLE: 92 algorithms from 33 teams forecast 219 at-risk individuals; monthly predictions over 5 years of clinical diagnosis, ADAS-Cog13, ventricle volume; no single method best on all; top methods beat baselines for diagnosis and ventricles, but none beat random guessing for ADAS-Cog13; mean/median ensembles scored top on almost all tasks — [arXiv 2002.03419](https://arxiv.org/pdf/2002.03419); published Marinescu et al., Machine Learning for Biomedical Imaging 1 (2021) 1–60, DOI 10.59275/j.melba.2021-2dcc — [DZNE record](https://pub.dzne.de/record/288435)
- TADPOLE SHARE "collates code for submissions" at tadpole-share.github.io; submission system tadpole.grand-challenge.org — [DZNE record](https://pub.dzne.de/record/288435)
- `tadpole-share/tadpole-algorithms` ("Python package with tadpole algorithms"): 10 stars, 12 open issues, updated 2026-07 — [GitHub](https://github.com/tadpole-share/tadpole-algorithms)
- `noxtoby/TADPOLE` (helper scripts for TADPOLE Challenge 2017): no license; last push 2021-08 — [GitHub](https://github.com/noxtoby/TADPOLE)
- Recent work still uses TADPOLE as a benchmark: an Emory ML4H 2025 study applied TabPFN (L2C-TabPFN) vs XGBoost-based "Frog" model; comparable on diagnosis/cognition, TabPFN better on ventricles — [arXiv 2508.17649](https://www.arxiv.org/pdf/2508.17649)
- MICCAI 2025 paper on regression-based survival model for AD progression with longitudinal data (not a challenge) — [MICCAI 2025](https://papers.miccai.org/miccai-2025/paper/2717_paper.pdf)
- NIA PREPARE (Pioneering Research for Early Prediction of AD & Related Dementias), run on DrivenData: Phase 1 data-discovery winners used DementiaBank audio, synthetic EHR, Mexican Health and Aging Study, ADNI rs-fMRI, NHIS; Phase 2 model arena (incl. acoustic track); Phase 3 focused on making winning models "more fair, equitable, and generalizable" — [DrivenData Phase 1](https://blog.drivendata.org/blog/prepare-phase1-winners); [Phase 3 problem](https://www.drivendata.org/competitions/304/prepare-challenge-phase-3/page/957/); [Phase 3 winners](https://blog.drivendata.org/blog/prepare-phase3-winners)
- CADDementia (MICCAI 2014) computer-aided diagnosis of dementia from structural MRI: Bron et al., NeuroImage 2015 — [NeuroImage](https://doi.org/10.1016/j.neuroimage.2015.01.048) (prior knowledge, not re-fetched)

### Inferences
- A gap exists for a modern, open, prospective benchmark on biomarker trajectories in the anti-amyloid-therapy era (plasma p-tau217, tau-PET, treated vs untreated); TADPOLE's ADNI-based data and evaluation code are the obvious template for a new open project to extend.
- TADPOLE's finding that ADAS-Cog13 forecasting was no better than random is a key caution for any new progression model.

### Gaps
- Could not confirm a 2024–2026 dedicated AD-progression challenge (MICCAI or otherwise); Phase 2/3 PREPARE winner identities not retrieved.
- Licensing of TADPOLE data requires ADNI data-use agreement; not open data.

## 5. Maintenance and licensing summary

### Takeaway
Actively maintained (pushed within ~12 months) and permissively licensed: pySuStaIn (MIT), Leaspy (BSD-3-Clause-Clear), ClinicaDL (MIT), UCL network_spreading_models (MIT). Maintained but non-standard/copyleft license: Clinica (custom/"Other"), TVB (NOASSERTION on GitHub), kde_ebm (GPL-3.0). Stale or unlicensed: SuStaInMatlab, noxtoby/TADPOLE, DIVE, Nexis (MIT but last push Jan 2025).

### Cited Findings
| Repo | What it models | License | Last push | Stars | Source |
|---|---|---|---|---|---|
| ucl-pond/pySuStaIn | Subtypes + stages (SuStaIn) | MIT | 2026-03-30 | 222 | [GitHub](https://github.com/ucl-pond/pySuStaIn) |
| ucl-pond/kde_ebm | KDE Event-Based Model | GPL-3.0 | 2025-11-13 | 18 | [GitHub](https://github.com/ucl-pond/kde_ebm) |
| ucl-pond/network_spreading_models | NDM / FKPP / amyloid-weighted FKPP | MIT | 2025-12-02 | 13 | [GitHub](https://github.com/ucl-pond/network_spreading_models) |
| aramis-lab/leaspy | Mixed-effects disease course mapping (logistic/linear/joint/mixture) | BSD-3-Clause-Clear | 2026-09-17 | 29 | [GitHub](https://github.com/aramis-lab/leaspy) |
| aramis-lab/clinica | Neuroimaging pipelines, BIDS converters | Other (NOASSERTION) | 2026-10-02 | 293 | [GitHub](https://github.com/aramis-lab/clinica) |
| aramis-lab/clinicadl | Deep learning on neuroimaging | MIT | 2026-10-16 | 191 | [GitHub](https://github.com/aramis-lab/clinicadl) |
| the-virtual-brain/tvb-root | Whole-brain network simulation / twins | Other (NOASSERTION) | 2026-10-16 | 195 | [GitHub](https://github.com/the-virtual-brain/tvb-root) |
| Raj-Lab-UCSF/Nexis | Extended network diffusion (eNDM) | MIT | 2025-01-15 | 2 | [GitHub](https://github.com/Raj-Lab-UCSF/Nexis) |
| LemuelPuglisi/BrLP | Latent-diffusion 3D MRI progression | not checked | updated 2026-10 | 140 | [GitHub](https://github.com/LemuelPuglisi/BrLP) |
| 88vikram/pyebm | EBM / discriminative EBM | not checked | updated 2026-03 | 30 | [GitHub](https://github.com/88vikram/pyebm) |
| tadpole-share/tadpole-algorithms | TADPOLE challenge entries | not checked | updated 2026-07 | 10 | [GitHub](https://github.com/tadpole-share/tadpole-algorithms) |
| noxtoby/TADPOLE | TADPOLE helper scripts | none | 2021-08-12 | 54 | [GitHub](https://github.com/noxtoby/TADPOLE) |
| ucl-pond/SuStaInMatlab | SuStaIn (MATLAB) | none | 2021-05-06 | 14 | [GitHub](https://github.com/ucl-pond/SuStaInMatlab) |
| ucl-pond/ebm | Original EBM | MIT (archived) | 2023-07-25 | 5 | [GitHub](https://github.com/ucl-pond/ebm) |

("Updated" for some rows is GitHub's updated_at, which can reflect stars rather than commits.)

### Inferences
- Recommended permissive stack for a new open AD progression project: Clinica/ClinicaDL for data prep (check Clinica's custom license), pySuStaIn for staging/subtyping, Leaspy for individual trajectories and simulation, UCL network_spreading_models for mechanistic tau spread, TVB for electrophysiological twins, TADPOLE-SHARE for benchmarking.
- BSD-3-Clause-Clear (Leaspy) explicitly withholds patent rights; GPL-3.0 (kde_ebm) imposes copyleft on derivatives — relevant if the new project wants Apache-2.0/MIT.

### Gaps
- Licenses for BrLP, pyebm, tadpole-algorithms, LCSB astrocyte model, DIVE not confirmed.
- Exact Clinica and TVB license texts not inspected.

## 6. Vetting: peer review, independent replication, maintenance, red flags, and what is needed to verify each resource

### Takeaway
Only a few items reach "peer-reviewed + independently replicated + maintained": SuStaIn (MRI atrophy subtypes replicated across cohorts; tau subtypes partially replicated) and connectome-based tau spreading in general (multiple groups, but model-comparison caveats). Leaspy/AD Course Map is peer-reviewed and maintained but its strongest performance claim is self-reported and sits in tension with the TADPOLE organisers' summary. QSP models, digital-twin (eBRAIN-Health) claims, and several ODE models are unreplicated, closed, or press/abstract-only. Any amyloid-oligomer ODE/QSP parameterisation should be audited for dependence on the retracted Aβ*56 literature.

### Cited Findings

**Field-level red flag: retracted foundational amyloid-oligomer work**
- The 2006 Nature paper "A specific amyloid-β protein assembly in the brain impairs memory" (Lesné et al., Aβ*56) was retracted in July 2024; the note cites figures showing "excessive manipulation, including splicing, duplication and the use of an eraser tool" and states data cannot be verified; first author Lesné disagreed; senior author Ashe maintains conclusions — [UTMB record of retraction note](https://researchexperts.utmb.edu/en/publications/retraction-note-a-specific-amyloid-%CE%B2-protein-assembly-in-the-brai/); [Wikipedia: Sylvain Lesné](https://en.wikipedia.org/wiki/Sylvain_Lesn%C3%A9); 2022 Science investigation background reported by [NBC News](https://www.nbcnews.com/science/science-news/alzheimers-theory-undermined-accusations-fabricated-research-rcna39843)
- Other researchers questioned whether Aβ*56 could even be detected as described (replication doubts beyond image issues) — [Wikipedia: Karen Ashe](https://en.wikipedia.org/wiki/Karen_Ashe)

**SuStaIn / pySuStaIn (UCL)**
- Peer-reviewed (Nat Commun 2018; SoftwareX 2021; Nat Med 2021 tau application) — see Section 1 sources.
- Independent/inter-cohort validation: model trained on ADNI and tested on OASIS, Pharma-Cog, ViTA reported consistent subtyping over time (Frontiers in Big Data 2021; note UCL co-authors, so semi-independent) — [Frontiers](https://frontiersin.org/articles/10.3389/fdata.2021.661110/abstract); [UCL PDF](https://discovery.ucl.ac.uk/id/eprint/10129988/1/Alexander_Inter-Cohort%20Validation%20of%20SuStaIn%20Model%20for%20Alzheimer%E2%80%99s%20Disease_VoR.pdf)
- Reproducibility study across eight cohorts: the three original atrophy subtypes replicated in most cohorts, but extra clusters (outliers, PCA-like) appeared, and excluding controls during fitting often made Subcortical and/or Cortical subtypes disappear; authors call for longitudinal validation — [arXiv 2412.00160](https://arxiv.org/pdf/2412.00160)
- Large (5,000+) study found subtype robustness varied, Subcortical subtype most sensitive to cohort composition — [PMC12960741](https://pmc.ncbi.nlm.nih.gov/articles/PMC12960741/)
- Tau-PET subtypes: Knight ADRC (820 flortaucipir scans, 629 participants) found three spatiotemporal tau subtypes, described as replication in an independent sporadic AD cohort (Vogel 2021 reported four) — [PMC12734641](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12734641/)
- Robustness to initialisation reported in Vogel 2021 supplementary — [PMC8686688 figure](https://pmc.ncbi.nlm.nih.gov/articles/PMC8686688/figure/F11)
- Maintenance: active (push 2026-03), but 53 open issues — [GitHub](https://github.com/ucl-pond/pySuStaIn)

**Event-Based Models (kde_ebm, pyebm, ebm)**
- Peer-reviewed methods; original `ucl-pond/ebm` archived; kde_ebm maintained (2025-11) under GPL-3.0 — [GitHub](https://github.com/ucl-pond/kde_ebm). No independent replication study was retrieved this session.

**Leaspy / AD Course Map (ARAMIS)**
- Peer-reviewed: Maheux et al., Nature Communications Feb 2023 (DOI 10.1038/s41467-022-35712-5), AD Course Map for individual forecasting and trial sample-size reduction — [PMC9918533](https://pmc.ncbi.nlm.nih.gov/articles/PMC9918533); software paper on arXiv (2026) — [arXiv 2608.09365](https://arxiv.org/pdf/2608.09365)
- Self-reported claim: Leaspy docs state it "outperformed 56 alternative methods" at predicting cognitive decline in TADPOLE — [Leaspy docs](https://leaspy.readthedocs.io/en/dev/to_go_further.html). RED FLAG / tension: the TADPOLE organisers' paper concluded no method beat random guessing for ADAS-Cog13 forecasting — [arXiv 2002.03419](https://arxiv.org/pdf/2002.03419). A ranking win does not imply clinically meaningful accuracy.
- Only "independent" test found is an undergraduate thesis (ADNI, 551 sMCI / 425 pMCI / 358 dementia; ~78% pMCI detection; poor at exact conversion dates) — not peer-reviewed — [UPM thesis](https://oa.upm.es/93574/1/TFG_Jorge_S_C.pdf)
- Leaspy also deployed as a tool on neuGRID2 / EDADS — [neuGRID2](https://neugrid2.eu/index.php/ml-tools/leaspy/)
- Maintenance: active (push 2026-09) — [GitHub](https://github.com/aramis-lab/leaspy)

**Network spreading models (NDM / FKPP / eNDM / SIR)**
- Multi-group support: 2019 bioRxiv study (n=295) found connectome-based spread models far exceeded chance and outperformed Euclidean extracellular-spread models, explaining most variance in tau progression — [bioRxiv 555821](https://www.biorxiv.org/content/10.1101/555821v1.full-text)
- December 2025 study: individualised connectomes and epicentres outperformed population-based ones cross-sectionally and longitudinally ("strongest in vivo evidence to date" — the authors' own characterisation) — [PMC12690294](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12690294/)
- Caveats: in transgenic Aβ mouse models the network model was "not necessarily better than a model of spatial spread" — [Frontiers editorial PMC6331437](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6331437/); passive diffusion fails to capture directional bias from active axonal transport — [arXiv 2401.02407](https://arxiv.org/html/2401.02407v1); connectomes contain modality-specific false positives/negatives and results depend on connectome choice — [PMC11211996](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11211996/)
- UCL toolbox (amyloid-weighted FKPP) evidence is a conference abstract (Alzheimer's & Dementia supplement), not a full peer-reviewed paper, and fit is group-level cross-sectional — [PMC11716492](https://pmc.ncbi.nlm.nih.gov/articles/PMC11716492/)

**Mechanistic ODE / multiscale / QSP**
- Multiscale 19-variable/75-parameter ODE model: peer-reviewed and subjected to a published sensitivity analysis, but no external clinical validation found; 75 parameters vs. sparse human data implies identifiability risk — [PMC10995318](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10995318/); [PMC12325246](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12325246/)
- QSP models (Biogen/Applied BioMath, Certara/Geerts, InSysBio/AbbVie): evidence is conference abstracts, posters and vendor pages; code closed; calibration (">70 datasets") is vendor-reported — [Certara poster](https://www.certara.com/poster/quantitative-systems-pharmacology-model-for-therapies-targeting-a%ce%b2-and-tau-pathologies-in-alzheimers-disease/); [PAGE abstract](https://www.page-meeting.org/Abstracts/quantitative-systems-pharmacology-model-of-key-intraneuronal-pathways-regulating-toxic-protein-accumulation-in-alzheimers-disease/)
- LCSB astrocyte metabolism model: peer-reviewed (PLoS Comp Biol 2023), code public, but depends on legacy Python 2.7/FEniCS 1.5 for some experiments (reproducibility risk) — [PMC10545114](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10545114/); [GitLab](https://gitlab.lcsb.uni.lu/ICS-lcsb/energy-metabolism-model-astrocyte/-/commit/26bb5572e546160167907462fff904de319fa019)

**Digital twins (TVB / eBRAIN-Health)**
- TVB platform is peer-reviewed and actively maintained (push 2026-10) — [GitHub](https://github.com/the-virtual-brain/tvb-root)
- eBRAIN-Health AD "digital twin" claims come from project/funder pages and an EBRAINS news post (consortium's own communications); no outcome-validation paper located — [EBRAINS news](https://ebrains.eu/news-and-events/2026/from-digital-twins-to-telemonitoring-ebrain-health-highlights-from-ebrains); [CORDIS](https://cordis.europa.eu/project/id/101058516)

**Benchmarks**
- TADPOLE: peer-reviewed (MELBA 2021), prospective, organiser-independent evaluation of 92 algorithms — strongest benchmark evidence available — [DZNE record](https://pub.dzne.de/record/288435)
- TADPOLE helper repo unmaintained since 2021 and unlicensed — [GitHub](https://github.com/noxtoby/TADPOLE)
- PREPARE challenge results are communicated mainly via DrivenData blog posts and winners' press releases (e.g., IGC Pharma investor news) — treat winner claims as unreviewed — [DrivenData](https://blog.drivendata.org/blog/prepare-phase1-winners); [Newswire](https://www.newswire.com/news/igc-pharma-wins-2-prizes-in-phase-1-of-national-institutes-of-healths-22435880)

### Vetting matrix (assessment; based on findings above)

| Resource | Peer-reviewed | Independent / external validation | Maintained (2025–26) | Red flags | What is needed to verify |
|---|---|---|---|---|---|
| pySuStaIn | Yes | Partial: atrophy subtypes replicated in multiple cohorts; tau subtypes count differs (4 vs 3) | Yes | Subtypes sensitive to control inclusion and cohort mix; no longitudinal prospective validation | Re-run on simulated data with known ground truth; refit on ADNI + an external cohort (e.g., OASIS-3, A4, BioFINDER via DUA); test subtype stability with bootstrap and with/without controls; check longitudinal stage progression |
| kde_ebm / pyebm | Yes | Not found this session | kde_ebm yes; pyebm unclear | GPL-3.0 (kde_ebm); pyebm license unconfirmed | Reproduce published orderings on ADNI; check license files |
| Leaspy / AD Course Map | Yes | Weak: mostly authors' own cohorts; only a student thesis as independent test | Yes | Self-reported "outperformed 56 methods" vs TADPOLE finding of no method beating random on ADAS-Cog13 | Hold-out forecasting on a cohort not used by the authors; report calibrated errors vs. naive baselines (last-value, linear mixed model); re-score on TADPOLE D4 data |
| UCL network_spreading_models | Abstract only (toolbox); methods (NDM/FKPP) peer-reviewed elsewhere | Concept supported by several groups; toolbox results not independently reproduced | Yes (2025-12) | Group-level cross-sectional fits; connectome choice drives results; distance-null not always beaten (esp. Aβ in mice) | Reproduce on ADNI tau-PET; compare against Euclidean-distance and random-rewired nulls; longitudinal individual prediction; vary connectome (HCP structural vs functional) |
| Nexis / eNDM | Yes (Raj lab papers) | Partially (NDM concept) | Stale (last push 2025-01) | MATLAB dependency; few users (2 stars) | Port/replicate in Python; benchmark vs UCL toolbox on same data |
| BioFINDER SIR tau model | Associated paper not verified this session | Unknown | 2026-04 | Unknown paper status | Locate paper, confirm peer review, rerun |
| Multiscale 19-var ODE model | Yes | No clinical validation found | Code status unknown | 75 parameters, identifiability; possible reliance on oligomer literature | Obtain/re-implement from equations; identifiability and global sensitivity analysis; fit to human biomarker trajectories (ADNI CSF/PET); audit parameter sources against retracted Aβ*56 work |
| Aβ oligomer ODE models (Bulai 2025, Cambridge 2020) | Yes | No | N/A (equations) | Theoretical; parameters not human-calibrated; oligomer-centric assumptions | Re-implement; calibrate to human CSF/PET kinetics (e.g., SILK turnover data); check citations for Aβ*56 dependence |
| Industry QSP models | Abstracts/posters | No independent validation | Closed | Vendor-reported calibration; code closed | Not verifiable without code; would need full re-implementation from any published equations |
| LCSB astrocyte metabolism | Yes | No | Unclear | Legacy Python 2.7/FEniCS 1.5 | Rebuild environment (container), reproduce paper figures, confirm license |
| TVB platform | Yes | Platform validated in epilepsy etc.; AD use not clinically validated | Yes | AD twin claims project-communications only | Reproduce Stefanovski-type TVB-AD simulation; seek eBRAIN-Health final deliverables/papers |
| BrLP (MICCAI 2024) | Yes (conference) | Unknown | Yes | Generative MRI realism ≠ clinical validity; license unchecked | Check license; evaluate on held-out cohort with volumetric error vs. observed follow-up MRI |
| TADPOLE / TADPOLE-SHARE | Yes | Prospective, organiser-run | SHARE moderately; helper repo stale | ADNI DUA required; no license on helper scripts | Obtain ADNI access; rerun evaluation scripts; reproduce baseline scores |
| PREPARE challenge | No (blog/press) | No | Ended | Winner claims via press releases | Inspect released winning code (if any) and data provenance |

### Inferences
- Highest-confidence reusable items for a new open project: pySuStaIn, Leaspy, and the connectome spreading toolbox, because code is open, permissive, maintained, and the underlying methods are peer-reviewed; but each still needs independent re-fitting on an external cohort and comparison against simple baselines/nulls.
- Mechanistic amyloid-cascade and QSP models should be treated as hypotheses rather than validated models; their parameter provenance needs auditing given the Aβ*56 retraction and general uncertainty in amyloid-oligomer biology.
- A minimal reproducibility protocol for any imported model: (1) pin code version and container; (2) reproduce a published figure/table exactly; (3) refit on a cohort the authors did not use; (4) compare to naive baselines and null models; (5) report calibration and uncertainty; (6) check licenses and data-use agreements.

### Gaps
- Did not search Retraction Watch for retractions specifically affecting the modelling papers listed; none surfaced in searches, but absence is not confirmation.
- External validation sections of Maheux 2023 and Vogel 2021 not read in full.
- No systematic check of PubPeer comments for any listed paper.
