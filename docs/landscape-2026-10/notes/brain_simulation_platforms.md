# Open Brain Simulation / Modeling Platforms for an Open-Source Alzheimer's Project (status as of 2026-10-18)

Method notes for the report writer:
- GitHub API was blocked in this session, so repo stars and last-push dates come from the ecosyste.ms GitHub mirror (`repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/<owner>%2F<repo>`), queried 2026-10-18. Latest-release versions and dates come from the PyPI JSON API (`pypi.org/pypi/<pkg>/json`), and license text from `raw.githubusercontent.com` LICENSE files, both queried the same day. Mirror numbers may lag GitHub by days.
- Items tagged **[DOI, not re-fetched]** are canonical papers cited by DOI from background knowledge. I did not open them this session, so check them before publishing.
- **Vetting key** (added at the coordinator's request): PR = peer-reviewed; IV = independently used or validated by groups outside the developers; AM = actively maintained (commit or release in the last 6 months); SELF = claims come mainly from the authors' or institution's own press; RF = red flag.

## Q1. Which whole-brain and large-scale simulation platforms exist and are freely usable?

### Takeaway
The open simulation stack is mature and active at the cellular and circuit scale (NEURON, NEST, Brian2, Arbor, NetPyNE, BMTK, all with commits or releases in 2026) and at the whole-brain neural-mass scale (TVB, neurolib, VBI). The Blue Brain Project ended in 2024. Its code was archived under github.com/BlueBrain and partly forked by the new Open Brain Institute (OBI), a freemium, credit-based cloud platform that is mouse-only. "Digital twin" and "foundation model" claims are the least independently verified category.

### Cited Findings

**A. Cellular and circuit simulators (biophysical or spiking neurons)**

| Resource | Scale | License | Activity (2026-10-18) | Vetting |
|---|---|---|---|---|
| NEURON (neuronsimulator/nrn) | Molecular (rxd reaction-diffusion), cellular, circuit | BSD-3-style ("three clause" BSD per `Copyright` file) | 559★, pushed 2026-10-17; PyPI `neuron` 9.0.2 released 2026-08-10 | PR, IV (decades of use, ModelDB), AM. No RF. |
| NEST (nest/nest-simulator) | Point-neuron circuit up to large networks | GPL-2.0 | 671★, pushed 2026-10-09; 3.10.0 released 2026-06-10 | PR, IV, AM. EBRAINS core tool. |
| Brian2 (brian-team/brian2) | Spiking circuit (equation-defined) | CeCILL 2.1 (GPL-compatible) | 1,246★, pushed 2026-10-15; 2.10.1 released 2025-12-05 | PR, IV, AM. |
| Arbor (arbor-sim/arbor) | Multicompartment cells and networks, GPU/HPC | BSD-3-Clause | 136★, pushed 2026-10-09; 0.12.2 released 2026-05-19 | PR, AM. Smaller user base than NEURON. |
| NetPyNE (suny-downstate-medical-center/netpyne) | Circuit (NEURON front-end) | MIT | 175★, pushed 2026-09-15; 1.1.1 released 2025-09-12 | PR, IV, AM. |
| BMTK, Allen Brain Modeling Toolkit (AllenInstitute/bmtk) | Cellular, circuit, region (SONATA format) | BSD-3-Clause | 338★, pushed 2026-10-08; 1.2.0 released 2026-06-24 | PR, AM. Used for the Fugaku cortex model (below). |
| PyNN (NeuralEnsemble/PyNN) | Simulator-independent network description | CeCILL 2.1 | 314★, pushed 2026-09-10; 0.13.0 released 2026-07-06 | PR, AM. |
| GeNN (genn-team/genn) | GPU spiking networks | LGPL-2.1 | 283★, pushed 2026-10-05 | PR, AM. |
| BrainPy (brainpy/BrainPy) | Spiking and rate dynamics on JAX | GPL-3.0 | 717★, pushed 2026-08-13; 2.8.2 released 2026-07-23 | PR, AM. |
| Nengo (nengo/nengo) | Large-scale functional (NEF) models | GPL-2.0 per LICENSE file | 953★, pushed 2026-08-02; 4.1.0 released 2025-05-29 | PR, AM (slower). Nengo has historically offered separate commercial licensing; check before any commercial use. |
| pyNeuroML / NeuroML (NeuroML/pyNeuroML) | Model-description standard, all scales | LGPL-3.0 | 53★, pushed 2026-07-31; 1.3.22 released 2026-06-02 | PR, AM. |
| Open Source Brain v2 (OpenSourceBrain/OSBv2) | Hosted workspaces (NetPyNE, NWB Explorer, JupyterLab; ModelDB and DANDI integration) | "other" | 23★, pushed 2026-10-13 | AM. Described as "free to use, collaborative, web based" ([OSB v2 announcement](https://lists.cnsorg.org/hyperkitty/list/comp-neuro%40lists.cnsorg.org/thread/H55MUZ3JYZ55KEL6SR2F7WVUPH4OW4LR/); [OSB docs](https://docs.opensourcebrain.org/Landing.html)). |

Sources for the table: activity and license data from the ecosyste.ms mirror (e.g. [nrn record](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/neuronsimulator%2Fnrn)) and PyPI ([neuron](https://pypi.org/pypi/neuron/json), [nest-simulator](https://pypi.org/pypi/nest-simulator/json), [brian2](https://pypi.org/pypi/brian2/json), [arbor](https://pypi.org/pypi/arbor/json), [bmtk](https://pypi.org/pypi/bmtk/json)). License texts: [Brian2 LICENSE](https://raw.githubusercontent.com/brian-team/brian2/master/LICENSE), [NEURON Copyright](https://raw.githubusercontent.com/neuronsimulator/nrn/master/Copyright), [Nengo LICENSE](https://raw.githubusercontent.com/nengo/nengo/main/LICENSE.rst), [PyNN LICENSE](https://raw.githubusercontent.com/NeuralEnsemble/PyNN/master/LICENSE).

**B. Whole-brain, neural-mass and connectome-based platforms**
- **The Virtual Brain (TVB)** (the-virtual-brain/tvb-root). Scale: whole-brain, with neural-mass nodes coupled by a structural connectome. License: GPL-3.0-or-later, (c) 2012-2025 Baycrest and others ([TVB LICENSE](https://raw.githubusercontent.com/the-virtual-brain/tvb-root/master/LICENSE)). Activity: 192★, pushed 2026-10-05; PyPI `tvb-library` 2.10.0 released 2025-07-22 ([PyPI](https://pypi.org/pypi/tvb-library/json)). Vetting: PR, IV (many outside groups, including the AD papers in Q2), AM, distributed via EBRAINS. The core library's last PyPI release is 15 months old even though commits continue.
- **TVB-Multiscale** (TVB co-simulated with NEST/ANNarchy/NetPyNE; the-virtual-brain/tvb-multiscale). 47★, pushed 2026-08-04 ([ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/the-virtual-brain%2Ftvb-multiscale)). Related repos are stale: `multiscale-cosim/EBRAINS-cosim` was last pushed 2023-05-24 (4★) and `BrainModes/fast_tvb` 2022-02-28 (6★). Treat those two as dormant.
- **VBI, Virtual Brain Inference** (ins-amu/vbi). Simulation-based Bayesian inference for TVB-style models. Apache-2.0, 24★, pushed 2026-10-07, PyPI 0.4.4 released 2026-08-04 ([PyPI](https://pypi.org/pypi/vbi/json)). Vetting: AM; small user base; check for a peer-reviewed methods paper.
- **Virtual Aging Brain** (ins-amu/virtual_aging_brain). MIT. Last pushed 2023-03-10, 6★. **RF: dormant.** Its description says "the code will be a[vailable]…", so the code may be incomplete ([ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/ins-amu%2Fvirtual_aging_brain)).
- **neurolib** (neurolib-dev/neurolib). Whole-brain modeling in Python. MIT, 498★. Last push 2025-11-13; last PyPI release 0.6.2 on 2022-06-23 ([PyPI](https://pypi.org/pypi/neurolib/json)). **RF: releases stalled for 4 years. Install from source.**
- **CBIG** (ThomasYeoLab/CBIG). Includes the parcellations and the relevant-mean-field-model code used in many whole-brain studies. MIT, 750★, pushed 2026-03-25 ([LICENSE](https://raw.githubusercontent.com/ThomasYeoLab/CBIG/master/LICENSE.md)).
- **EBRAINS research infrastructure** (successor to the Human Brain Project; HBP ended in 2023). EBRAINS 2.0 has €38M under Horizon Europe grant 101147319, runs January 2024 to December 2026, and has 59 partners in 16 countries. Its stated aims include digital-twin approaches ([EBRAINS news](https://ebrains.eu/news-and-events/2024/ebrains-research-infrastructure-secures-eu38-million-in-funding-for-new-phase)). A June 2026 booklet still describes the 2024-2026 term and shows no confirmed successor funding ([EBRAINS 2.0 booklet 2026](https://ebrains.eu/sites/default/files/downloads/2026/06/EBRAINS%202.0%20A5%20Booklet_2026.pdf)). **RF (sustainability): the funded phase ends 2026-12. Whether hosted EBRAINS services continue in 2027 is unconfirmed.** The open-source tools (TVB, NEST, siibra) would keep working regardless.

**C. Blue Brain Project legacy and the Open Brain Institute**
- The Blue Brain Project (EPFL) concluded in 2024. It previewed a "Blue Brain Open Platform" with more than 260 public repositories, more than 5,000 reconstructed morphologies and hundreds of e-models, drawn from about 300 publications and 1 PB of data ([BBP "Next Steps and Mission Accomplished"](https://bbp.epfl.ch/bbp/research/domains/bluebrain/index.html%3Fp=12290.html); [BBP GitHub org](https://www.github.com/BlueBrain)).
- Archived BBP repos (read-only) include `BlueBrain/BluePyOpt` (218★, archived 2025-02-26), `BlueBrain/neurodamus` (archived 2025-02-26) and `BlueBrain/CoreNeuron` (archived; last push 2023-03-20; CoreNEURON was merged into NEURON). Maintained forks live at `openbraininstitute/BluePyOpt` (LGPL, pushed 2026-08-24, PyPI 1.14.25 released 2026-08-24) and `openbraininstitute/neurodamus` (Apache-2.0, pushed 2026-10-12) ([ecosyste.ms BluePyOpt](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/BlueBrain%2FBluePyOpt); [BluePyOpt LICENSE](https://raw.githubusercontent.com/openbraininstitute/BluePyOpt/master/LICENSE.txt)). The forks have very few stars (2-10), which suggests a small community outside OBI.
- **Open Brain Institute** is a not-for-profit set up by Henry and Kamila Markram ([Walder Wyss](https://www.walderwyss.com/en/news/2025-05-13_walder-wyss-advised-on-the-setup-of-the-open-brain-institute); [WEF profile](https://cn.weforum.org/people/henry-markram)). Founding dates conflict: a Swiss registry gives 2024-11-20 ([fundraiso](https://www.fundraiso.ch/en/organisations/open-brain-institute)), WEF says launched January 2025 with 43 ex-BBP staff, and Walder Wyss says March 2025.
- The OBI platform offers cloud "Virtual Labs" across subcellular (ion channels, metabolism, neuro-glia-vascular units), cellular, circuit, system and whole-brain scales. Only mouse is mentioned, with a mouse atlas. **Freemium**: a free plan with limited credits, a Pro plan, and a Premium plan priced on request. The site states no open-source license and names no specific Alzheimer's content ([openbraininstitute.org](https://www.openbraininstitute.org/)). Its workflow package `obi-one` is Apache-2.0, with PyPI 2026.10.16 released 2026-10-16 ([PyPI](https://pypi.org/pypi/obi-one/json)).
- Vetting of the BBP models: the 2015 neocortical microcircuit (about 31k neurons, about 37M synapses; Markram et al., Cell 2015, [doi:10.1016/j.cell.2015.09.029](https://doi.org/10.1016/j.cell.2015.09.029) **[DOI, not re-fetched]**) was peer-reviewed and its data released. Critics argued it offered little new insight for its cost ([Jaeger blog, opinion](https://larsjaeger.ch/?p=10043)). Jirsa (eNeuro 2021) wrote that a central open question is "whether and how we will know if a simulation truly provides the right end result" and called for cross-validation against empirical data ([eNeuro commentary](https://www.eneuro.org/content/eneuro/8/2/ENEURO.0128-21.2021.full.pdf)). I found no formal failed replication, but also no independent re-simulation.

**D. Large "digital twin" and whole-cortex simulations**
- **Allen Institute / UEC, Fugaku mouse cortex**: about 9-10M multicompartment neurons, 26B synapses and 86 regions, built from the Allen Cell Types Database and Connectivity Atlas via BMTK and run on the Neulite simulator. It was presented as a peer-reviewed SC25 conference paper, and the press cites Alzheimer's and epilepsy as future uses ([UEC announcement](https://www.uec.ac.jp/eng/news/announcement/2025/20251118_7309.html); [ScienceAlert](https://www.sciencealert.com/?p=183652)). Vetting: an HPC venue rather than neuroscience peer review; coverage is press-release-driven; no biological-validation results found; disease use is aspirational. Neulite code availability is unverified.
- **Digital Twin Brain (DTB, Fudan; Lu, Feng et al.)**: claims spiking-network simulation at human scale (up to 86B neurons) from personalized MRI, published in Nature Computational Science 2024 ([arXiv 2211.15963](https://arxiv.org/abs/2211.15963v1); [Lu et al. 2024 PDF](https://www.oxcns.org/papers/691%20Lu%20et%20al%202024%20Simulation%20and%20assimilation%20of%20the%20digital%20human%20brain.pdf)). The 2025 State of Brain Emulation report notes that only about 0.72% of possible connections were realized and that parameters were fit by "hierarchical mesoscopic data assimilation" ([arXiv 2510.15745](https://arxiv.org/pdf/2510.15745)). Papers-with-Code lists "no code implementations" for the consortium's work ([PwC](https://cs.paperswithcode.com/author/dtb-consortium)). **RF: no public code found; scale claims are mainly from the authors and press; heavy connection sparsification.** A Warwick-led review in Nature Reviews Electrical Engineering argues that digital-twin fidelity is limited by measurement and validation, not compute ([Warwick](https://warwick.ac.uk/fac/sci/wmg/news-and-events/news/wmg-academic-leads-digital-twin-brain-review/)).

**E. Foundation models of neural activity**
- **MICrONS digital twin / foundation model** (Wang et al., Nature 2025, vol. 640, p. 470, [doi:10.1038/s41586-025-08829-y](https://doi.org/10.1038/s41586-025-08829-y)). Trained on recordings from 14 mice viewing natural video, it predicts responses to new stimulus types, and its predictions were checked against MICrONS electron microscopy ([Stanford](https://med.stanford.edu/ophthalmology/news-and-media/news-archive/2025-stories/digital-twins.html); [Bernstein](https://bernstein-network.de/en/newsroom/news/visual-system-through-eyes-ai/)). Code at `cajal/fnn` under the MIT license; 28★, last push 2026-01-08 ([LICENSE](https://raw.githubusercontent.com/cajal/fnn/main/LICENSE)). Vetting: PR, code released; covers mouse visual cortex only, with no disease relevance.
- **torch_brain / POYO** (neuro-galaxy). torch_brain is Apache-2.0, 100★, PyPI 0.2.1 released 2026-10-14. POYO has no license file and was last pushed 2025-09-11 ([PyPI](https://pypi.org/pypi/torch_brain/json)). **RF for POYO: no license means no legal right to reuse.**
- **BrainLM** (vandijklab/BrainLM): an fMRI foundation model. **License is CC BY-NC-ND 4.0** (non-commercial, *no derivatives*) ([LICENSE](https://raw.githubusercontent.com/vandijklab/BrainLM/main/LICENSE)). 6★ on the mirror, last push 2025-11-22. **RF: ND forbids distributing modified or fine-tuned versions, so it is unsuitable as a base for an open AD project without permission.**

### Inferences
- The most reusable base for an open AD project is TVB plus VBI (whole-brain, GPL/Apache) alongside NEURON, NEST or Brian2 (cellular and circuit), all integrated via EBRAINS and siibra. TVB's GPL-3.0 copyleft would carry over to derived code distributed with it.
- OBI is the practical heir to BBP tooling, but its hosted platform is freemium and mouse-only, and its forks have small communities. Rely on the Apache/LGPL libraries, not the hosted service.
- Claims at "full human brain" or "digital twin" scale (DTB, Fugaku) are computing milestones, not validated disease models.

### Gaps
- I could not confirm Neulite's (Fugaku) public code or license.
- I could not confirm OBI pricing, credit amounts, or whether its whole-brain models are downloadable and openly licensed.
- No 2026 decision on EBRAINS funding after 2026 was found.
- No public code was found for the Fudan DTB. No independent replication of its claims was found.
- I did not check Arbor, GeNN or BrainPy for independent benchmark comparisons.

## Q2. Which have been applied specifically to Alzheimer's disease or neurodegeneration?

### Takeaway
Two families of AD modeling exist. The first is TVB-based whole-brain dynamics, driven by amyloid and tau PET from ADNI; these are peer-reviewed but use small cohorts and have little independent replication. The second, more mature and more widely replicated, is connectome-based spreading models (network diffusion, FKPP, SIR, epidemic-type) predicting tau and atrophy progression. Code availability is uneven, and some well-known AD code repos are dormant.

### Cited Findings
**TVB / whole-brain dynamics in AD**
- Stefanovski et al., 2019 (Front. Comput. Neurosci.): personalized TVB virtual brains built from ADNI-3 amyloid PET (healthy controls, MCI, AD). Amyloid reduced regional inhibition, which produced simulated LFP/EEG slowing in the AD group. Uniform amyloid controls did not slow, and modeled memantine (NMDA antagonism) reversed the slowing ([Frontiers](https://frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2019.00054/full)). Vetting: PR, small n, from the developer-affiliated group (Charité/Ritter).
- Triebkorn et al. (bioRxiv 2021, published 2022): on 33 ADNI3 participants, adding TVB-simulated features to empirical amyloid/tau PET and MRI raised the weighted F1 score from 64.34% to 74.28%. The authors say a larger cohort with an independent test set is needed ([bioRxiv](https://www.biorxiv.org/content/10.1101/2021.02.27.433161v2.full.pdf)). **RF: n = 33 with no held-out external cohort, and the gain is modest.**
- Patow, Stefanovski, Ritter, Deco and Kobeleva, 2023 (Alzheimer's Research & Therapy 15:210): a whole-brain balanced excitation-inhibition model fit to ADNI resting-state fMRI. Amyloid has the stronger influence at the MCI stage and tau at the dementia stage. The work is in silico, and the authors note that E/I balance cannot be measured directly in vivo ([PMC10696890](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10696890/)). Vetting: PR, open access; code availability not checked.
- Monteverdi et al., 2023 (Front. Aging Neurosci.): TVB simulations of AD and FTD patients from MRI. The parameter patterns differed by disease and correlated with clinical profiles ([DOAJ](https://doaj.org/article/39a95b4fdf674b15b26504978fee403e)). A 2022 Front. Aging Neurosci. TVB study extracted single-subject E/I estimates using Wong-Wang nodes ([DOAJ](https://doaj.org/article/fd057b97d6584926a5652659ce574e67)).
- Review: "Bridging Scales in Alzheimer's Disease" (Front. Neuroinform. 2021) surveys AD models from molecular cascades to TVB ([Frontiers](https://frontiersin.org/articles/10.3389/fninf.2021.630172/full)).
- The Jirsa group's 2025 Nature Computational Science "virtual brain twins" paper targets **epilepsy**, not AD. An EBRAINS 2.0 digital-twin job posting lists aging, Parkinson's and psychiatric uses ([INS-AMU job](https://ins-amu.fr/jobs/job-posting4-w8aj8); [TVB publications list](https://hub.thevirtualbrain.org/tvb/zwei/neuroscience-publications)). I found no validated TVB *tau-spreading* simulation ([search summary of TVB AD literature, above sources]).

**Connectome spreading models (tau, amyloid, atrophy)**
- Raj, Kuceyeski & Weiner, 2012, Neuron: the "network diffusion model" of dementia progression on the connectome, the foundational paper ([doi:10.1016/j.neuron.2011.12.040](https://doi.org/10.1016/j.neuron.2011.12.040)) **[DOI, not re-fetched]**. This family has since been reproduced by many groups (see below).
- Raj Lab's Aggregation-Network-Diffusion: MATLAB code for joint amyloid-tau diffusion with cross-species interaction terms, bundled with connectomes. BSD-3 per the README ([GitHub](https://github.com/Raj-Lab-UCSF/Aggregation-Network-Diffusion)). Activity: 12★, **last push 2020-12-02 (dormant)**, and no license file was detected by the mirror. Its manuscript was "under review" when the README was written; the published paper is unconfirmed.
- Network transport model (arXiv 2401.02407): adds active axonal transport to diffusion; no code link found ([arXiv](https://arxiv.org/abs/2401.02407v2)).
- Thompson et al. (UCL), AAIC/Alzheimer's & Dementia 2024 abstract: an "open-source toolbox for network spreading models" comparing network diffusion, FKPP and weighted-FKPP on ADNI tau and amyloid PET. It reports that regional amyloid promotes tau production ([PMC11716492](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11716492/)). **RF: conference abstract only, with no public repo URL found.**
- networkAD (EU MSCA project 101153323): patient-specific connectome model with regional vulnerability from gene expression. It *promises* an open-source package; none was found ([CORDIS](https://cordis.europa.eu/project/id/101153323)).
- Fornari, Goriely et al., 2019, J. R. Soc. Interface: prion-like FKPP spreading on the human connectome ([doi:10.1098/rsif.2019.0356](https://doi.org/10.1098/rsif.2019.0356)) **[DOI, not re-fetched]**.
- Vogel et al., 2020, Nature Communications: tau-PET spread follows functional and structural connectivity in an epidemic-spreading model across multiple cohorts ([doi:10.1038/s41467-020-16588-7](https://doi.org/10.1038/s41467-020-16588-7)) **[DOI, not re-fetched]**. Vogel et al., 2021, Nature Medicine: four tau trajectories via SuStaIn ([doi:10.1038/s41591-021-01309-6](https://doi.org/10.1038/s41591-021-01309-6)) **[DOI, not re-fetched]**. The open-source pySuStaIn is at github.com/ucl-pond/pySuStaIn (activity not checked).

**AD cellular data usable for cellular-scale models**
- SEA-AD (Seattle Alzheimer's Disease Brain Cell Atlas; Allen Institute and partners): an integrated multimodal single-cell atlas of AD (Gabitto et al., Nature Neuroscience 2024, [doi:10.1038/s41593-024-01774-5](https://doi.org/10.1038/s41593-024-01774-5)) **[DOI, not re-fetched]**. Its access terms and license were not checked in this session.

### Inferences
- Network spreading models are the most reproducible on-ramp for an open AD project. They are simple (a linear ODE or FKPP on a graph), have been tested by several independent groups on ADNI, and can be re-implemented in a few hundred lines. The open-source re-implementation itself is the missing piece, since the best-known code is dormant or unreleased.
- TVB-AD results come mostly from one consortium (Charité/Ritter plus collaborators), use small ADNI subsets, and lack external validation. A new project would need to re-run them on independent cohorts (e.g. A4, OASIS-3, BioFINDER, if access is granted).

### Gaps
- I did not verify code or data availability for Patow 2023, Stefanovski 2019 or Monteverdi 2023, or whether any of them was independently replicated.
- No public repo was found for the UCL toolbox or for networkAD.
- No AD-specific work on the OBI platform, or on molecular-scale (rxd) AD models in NEURON, was found in this session. Molecular-scale AD models (Aβ/tau kinetics, ODE/QSP) are outside what I covered.

## Q3. What brain atlases and connectomes are open?

### Takeaway
High-quality atlases and connectomes are freely downloadable: siibra/Julich-Brain, BigBrain, Allen atlases, FlyWire and MICrONS. Human cohort imaging data, however, sits behind data-use agreements or approved-researcher processes: HCP-Aging via NDA, UK Biobank, and ADNI. That data is "freely available" in cost to academics, but it is not redistributable openly. Several analysis toolkits carry non-commercial licenses.

### Cited Findings
- **siibra-python / siibra-explorer** (EBRAINS multilevel atlas framework: Julich-Brain cytoarchitectonic maps, BigBrain, connectivity and receptor data). Apache-2.0. siibra-python has 64★, pushed 2026-10-09, latest PyPI 1.0.1a25 released 2026-10-13 (pre-release); siibra-explorer has 31★, pushed 2026-10-07 ([PyPI](https://pypi.org/pypi/siibra/json); [ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/FZJ-INM1-BDA%2Fsiibra-python)). Vetting: AM, but the 1.0 line is still an alpha.
- **Julich-Brain** (Amunts et al., Science 2020, [doi:10.1126/science.abb4588](https://doi.org/10.1126/science.abb4588)) and **BigBrain** (20 µm 3D histology, Amunts et al., Science 2013, [doi:10.1126/science.1235381](https://doi.org/10.1126/science.1235381)) **[DOI, not re-fetched]**. Both are distributed via EBRAINS/siibra and are PR and widely used.
- **Allen Human Brain Atlas** (microarray expression in 6 donor brains; Hawrylycz et al., Nature 2012, [doi:10.1038/nature11405](https://doi.org/10.1038/nature11405)) **[DOI, not re-fetched]**. It underpins many models of gene-expression-based regional vulnerability. Limitation: only 6 donors.
- **Allen SDK / ABC Atlas access**: the AllenSDK license is "2-clause BSD plus a third clause that prohibits redistribution for commercial purposes without further permission" ([AllenSDK LICENSE](https://raw.githubusercontent.com/AllenInstitute/AllenSDK/master/LICENSE.txt)). Latest PyPI is 2.16.2 from 2023-11-30, though the repo was pushed 2026-07-06 ([PyPI](https://pypi.org/pypi/allensdk/json)). `abc_atlas_access` (Allen Brain Cell Atlas) has 120★ and was pushed 2026-09-02. **RF: non-commercial redistribution clause; AllenSDK releases stalled since 2023.**
- **Human Connectome Project**: HCP pipelines are BSD-style, 660★, pushed 2026-10-08 ([LICENSE](https://raw.githubusercontent.com/Washington-University/HCPpipelines/master/LICENSE.md)). HCP-Aging (ages 36-100+) is shared only through NIMH Data Archive collection #2847. Access requires an NDA Data Use Certification signed by an eRA-Commons-registered institution and annual renewal, which the HCP describes as "more restrictive than the HCP Open Access terms" ([HCP-Aging data use terms](https://humanconnectome.org/study/hcp-lifespan-aging/data-use-terms); [LS Release 2.0 instructions](https://www.humanconnectome.org/storage/app/media/documentation/data_release/LS_Release_2.0_Access_Instructions.pdf)).
- **UK Biobank imaging**: imaging was completed in July 2025, with more than 1 billion scans from 100,000 participants. Access is limited to approved researchers via a cloud platform ([UK Biobank news](https://ukbiobank.ac.uk/learn-more-about-uk-biobank/news/world-s-largest-imaging-study-scans-50-000th-participant)). Fees were not confirmed this session.
- **FlyWire** (whole adult *Drosophila* connectome, about 140k neurons; Dorkenwald et al., Nature 2024, [doi:10.1038/s41586-024-07558-y](https://doi.org/10.1038/s41586-024-07558-y)) **[DOI, not re-fetched]**. `flyconnectome/flywire_annotations` has 81★ and was pushed 2026-09-29, but **no license file** was detected. CAVEclient (MIT, 43★, PyPI 8.2.1 released 2026-07-10) and navis (GPL-3.0, PyPI 1.12.0 released 2026-07-13) are the access and analysis tools ([ecosyste.ms flywire_annotations](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/flyconnectome%2Fflywire_annotations)). neuPrint's import tools repo was **archived** in 2023.
- **MICrONS** (cubic-millimetre mouse visual cortex, functional plus EM connectome; Nature 2025 package, see Q1-E). The `cajal/microns-nda-access` Docker repo is GPL-3.0 and was last pushed 2023-06-29, so it is stale ([ecosyste.ms](https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/cajal%2Fmicrons-nda-access)).
- **Map-comparison and analysis toolkits**: neuromaps (348★) is licensed **CC BY-NC-SA 4.0 (non-commercial)** ([LICENSE](https://raw.githubusercontent.com/netneurolab/neuromaps/main/LICENSE)). netneurotools is BSD-3. The ENIGMA Toolbox (BSD-3, 190★, pushed 2026-01-15) gives access to 100+ ENIGMA case-control summary maps. BrainSpace is BSD-3 (PyPI 0.2.1, 2026-05-05). For connectome construction from diffusion MRI: MRtrix3 (MPL-2.0, pushed 2026-10-07), MRtrix3_connectome BIDS-App (Apache-2.0), and Connectome Mapper 3 (pushed 2026-03-20). For data formats and archives: DANDI (Apache-2.0) and pynwb (both active) (all from [ecosyste.ms mirror](https://repos.ecosyste.ms/)).

### Inferences
- For an AD project, the open "backbone" is: siibra/Julich-Brain or a standard parcellation, plus an HCP-derived template connectome (HCP Young Adult open-access tier), plus AHBA gene expression, plus ADNI PET (under its DUA) for fitting. Individual-level cohort data cannot be redistributed. The project should therefore publish code and derived group-level summaries only, with users obtaining raw data themselves.
- Check licenses carefully: neuromaps (NC-SA), AllenSDK (no commercial redistribution), BrainLM (NC-ND), and no license at all for POYO and flywire_annotations are real constraints on an "open" project.

### Gaps
- I did not verify current access fees for UK Biobank or ADNI, or the ADNI DUA terms for 2026.
- I did not check the data licenses (as opposed to code licenses) for MICrONS, FlyWire, BigBrain or the Allen ABC Atlas. They are commonly stated as CC BY 4.0, but that is unverified this session.
- I did not check HCP Young Adult open-access terms for 2026.

## Q4. How active are these projects, and what are their licenses?

### Takeaway
Most core simulators and atlas tools had commits in September-October 2026 and releases in 2025-2026. Dormant or archived items: all BlueBrain-org repos (archived), CoreNEURON (merged into NEURON), Raj Lab AD diffusion code (2020), Virtual Aging Brain (2023), EBRAINS-cosim (2023), fast_tvb (2022), neuPrint import tools (archived 2023), and neurolib releases (2022). Licenses range from permissive to copyleft to non-commercial or no license.

### Cited Findings
(All data from the [ecosyste.ms GitHub mirror](https://repos.ecosyste.ms/) and [PyPI JSON API](https://pypi.org/), queried 2026-10-18, plus the LICENSE files cited above.)

| Status | Projects |
|---|---|
| Very active (push within ~2 weeks and 2026 release) | NEURON 9.0.2, NEST 3.10.0, BMTK 1.2.0, siibra 1.0.1a25, torch_brain 0.2.1, obi-one 2026.10.16, Arbor 0.12.2, PyNN 0.13.0, VBI 0.4.4, MRtrix3, fMRIPrep, FreeSurfer, HCPpipelines, DANDI, pynwb |
| Active (push in 2026, older release) | TVB (release 2025-07), Brian2 (release 2025-12), NetPyNE (release 2025-09), Nengo (release 2025-05), AllenSDK (release 2023-11), neuromaps, ENIGMA, BrainSpace, CBIG, cajal/fnn |
| Archived or dormant (RF) | BlueBrain/* (archived 2025-02), CoreNeuron (last push 2023-03), Raj-Lab-UCSF/Aggregation-Network-Diffusion (2020-12), ins-amu/virtual_aging_brain (2023-03), multiscale-cosim/EBRAINS-cosim (2023-05), BrainModes/fast_tvb (2022-02), connectome-neuprint/neuPrint (archived), cajal/microns-nda-access (2023-06), neurolib PyPI (2022-06) |

| License class | Projects |
|---|---|
| Permissive (MIT/BSD/Apache) | NEURON, Arbor, NetPyNE, BMTK, siibra, obi-one, neurodamus (OBI), torch_brain, VBI, CBIG, cajal/fnn, CAVEclient, netneurotools, ENIGMA, BrainSpace, HCPpipelines |
| Weak copyleft | BluePyOpt (LGPL), pyNeuroML (LGPL-3), GeNN (LGPL-2.1), MRtrix3 (MPL-2.0) |
| Strong copyleft | TVB (GPL-3+), NEST (GPL-2), BrainPy (GPL-3), Nengo (GPL-2), navis (GPL-3); Brian2 and PyNN (CeCILL 2.1, GPL-compatible) |
| Non-commercial or restricted (RF) | neuromaps (CC BY-NC-SA 4.0), BrainLM (CC BY-NC-ND 4.0), AllenSDK (BSD plus no-commercial-redistribution clause) |
| No license detected (RF: no reuse rights) | neuro-galaxy/poyo, flyconnectome/flywire_annotations, Raj-Lab Aggregation-Network-Diffusion (README claims BSD-3, but no license file was detected by the mirror) |

### Inferences
- Stars are a weak proxy for use. Domain tools such as NEURON (559★) are used far more widely than their star counts suggest, while new OBI forks show 1-10★ because they are recent forks. Commits, releases and citations are better activity signals.
- A GPL-3 TVB dependency makes the combined distributed work GPL. Decide the project's license with this in mind (e.g. GPL-3 for simulation code, CC BY for derived data).

### Gaps
- No commit-count or contributor-count data could be collected, because the GitHub API was blocked.
- Mirror data may lag by a few days.
- I did not check citation counts.

## Q5. What are the known limitations and gaps?

### Takeaway
The main limitations are validation, not tooling. Large simulations (BBP, Fugaku, DTB) are rarely validated against independent empirical data. AD whole-brain models use small ADNI subsets from one consortium. Spreading-model code is fragmented or unreleased. Human data is gated. Major infrastructure (EBRAINS 2.0) faces a funding cliff at the end of 2026.

### Cited Findings
- Validation gap: "whether and how we will know if a simulation truly provides the right end result" is unresolved, and cross-validation against empirical data is a "justified request" ([Jirsa, eNeuro 2021](https://www.eneuro.org/content/eneuro/8/2/ENEURO.0128-21.2021.full.pdf)).
- Digital-twin fidelity is limited by "how much of the living brain we can measure, validate, and update over time", and full synaptic mapping at human scale is "far beyond technical and economic feasibility" ([Warwick / Nat Rev Electr Eng review](https://warwick.ac.uk/fac/sci/wmg/news-and-events/news/wmg-academic-leads-digital-twin-brain-review/)).
- The DTB realized only about 0.72% of possible connections ([State of Brain Emulation 2025](https://arxiv.org/pdf/2510.15745)), and no public DTB code was found ([PwC](https://cs.paperswithcode.com/author/dtb-consortium)).
- The BBP microcircuit omitted glia ([Generative Models of Brain Dynamics review, arXiv 2112.12147](https://arxiv.org/pdf/2112.12147)), and critics question its scientific payoff ([Jaeger, opinion](https://larsjaeger.ch/?p=10043)).
- TVB-AD classification used n = 33 with no external test set ([Triebkorn bioRxiv](https://www.biorxiv.org/content/10.1101/2021.02.27.433161v2.full.pdf)). Patow 2023 notes that E/I balance cannot be measured directly in vivo, so its inferred E/I parameters cannot be directly checked ([PMC10696890](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10696890/)).
- Infrastructure risk: EBRAINS 2.0 funding ends December 2026 ([EBRAINS](https://ebrains.eu/news-and-events/2024/ebrains-research-infrastructure-secures-eu38-million-in-funding-for-new-phase)). BBP closed in 2024, and its successor OBI is a freemium platform ([OBI](https://www.openbraininstitute.org/)).
- Data gating: HCP-Aging requires an NDA DUC and an institutional signatory ([HCP](https://humanconnectome.org/study/hcp-lifespan-aging/data-use-terms)). UK Biobank is limited to approved researchers ([UK Biobank](https://ukbiobank.ac.uk/learn-more-about-uk-biobank/news/world-s-largest-imaging-study-scans-50-000th-participant)).

### Inferences
**What each resource needs before an open AD project relies on it:**
- **TVB AD models (Stefanovski, Patow, Triebkorn)**: re-implement them from the papers in TVB or VBI; refit on a held-out ADNI split plus at least one external cohort; compare against null models (shuffled connectome, uniform amyloid); pre-register the metrics.
- **Network diffusion / FKPP**: re-implement them; reproduce Raj 2012 and Vogel 2020 fits on ADNI tau PET; benchmark against null and spatial-autocorrelation-preserving controls (e.g. spin tests), noting neuromaps' NC license.
- **Fugaku and DTB scale claims**: treat them as unverified for disease use until code and validation data are public.
- **Foundation models (fnn, BrainLM, POYO)**: fnn is reusable under MIT but covers mouse V1 only. Do not build on BrainLM (NC-ND) or POYO (no license) without written permission.
- **OBI models**: confirm the download and license terms of each model artifact; compare against the archived BBP releases.
- **Atlas data**: record versions (siibra pre-release tags), data licenses and DUAs per dataset.
- No retractions were found for any resource listed. That reflects targeted, not exhaustive, checks; run Retraction Watch and PubPeer checks on the final shortlist.

### Gaps
- I did not search PubPeer or Retraction Watch systematically.
- I found no independent replication studies of the TVB-AD papers. Their absence is not proven.
- Molecular-scale AD simulation (Aβ aggregation kinetics, QSP models) and glial or vascular (NGV) AD models are not covered here.
- I could not confirm whether OBI's neuro-glia-vascular and metabolism models (which are relevant to AD) are downloadable or openly licensed.
