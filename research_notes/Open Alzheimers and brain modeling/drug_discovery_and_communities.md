# Open Drug Discovery / Repurposing Resources and Open-Science Communities for Alzheimer's Disease (as of Oct 2026)

Research method note: about 25 web searches and fetches, run 2026-10-18. GitHub API search was **blocked in this session** because the session is bound to its configured repositories, so I could not verify repo names, stars, licenses or activity. Every GitHub-specific claim below comes from web sources or is listed as a gap. Items marked "(unverified this session)" are background knowledge that no source fetched here confirmed. The report writer should treat them as leads, not facts.

**Skepticism requirement:** Section 6 gives a per-resource and per-claim vetting assessment: peer review, replication, RCT vs observational evidence, retractions and controversies, conflicts of interest, and what would be needed to verify each item. RED FLAGS are marked explicitly. Nothing in Sections 1–5 should be used without reading Section 6.

## 1. Open target and drug resources (Agora, TREAT-AD, Open Targets, AlzPED, Alzforum, knowledge graphs)

### Takeaway
A new AD project has an unusually rich open layer to build on, mostly from NIA. Agora gives target-level evidence for more than 950 nominated targets. TREAT-AD distributes probes and "Target Enabling Packages". AlzPED has about 1,400 curated preclinical efficacy studies. Alzforum Therapeutics catalogs Phase 2+ agents. Open Targets ranks targets genome-wide. Open knowledge graphs (AlzKB, PrimeKG, Hetionet-style) support computational repurposing. Most of these are browsable portals with downloadable data. Few have a formal process for outside code contributions.

### Cited Findings
**Agora (AMP-AD / Sage Bionetworks target explorer)**
- Agora (agora.adknowledgeportal.org) is "an openly available web application" for AD researchers. It lists "over 950 potential therapeutic targets" with harmonized genome-wide transcriptomic, proteomic and metabolomic analyses. — [Agora paper, PMC12726812](https://pmc.ncbi.nlm.nih.gov/articles/PMC12726812/)
- Targets are nominated by the NIA AMP-AD consortium, the TREAT-AD centers and "the broader AD research community". Recent updates added new TREAT-AD nominations. Users can access the data underlying the visualizations. The paper does not describe an API, a code license or a formal contribution process. — [PMC12726812](https://pmc.ncbi.nlm.nih.gov/articles/PMC12726812/)
- An earlier Agora paper describes it as built around target evidence from NIA's translational portfolio, with access to related reagents and bioinformatics packages. — [Agora paper, PMC11709802](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11709802/)

**TREAT-AD centers (Emory-Sage-SGC-JAX and others)**
- The Emory-Sage-SGC-JAX TREAT-AD Center generates and **openly distributes validated experimental tools**, including chemical and biological probes and "Target Enabling Packages" (TEPs), to test target predictions from omics of diseased human brain tissue. — [TREAT-AD TEP paper, PMC11712476](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11712476/)
- In 2019 Sage Bionetworks joined the Open-AD Drug Discovery Center, which aims to find new AD drugs. — [Wikipedia: Sage Bionetworks](https://en.wikipedia.org/wiki/Sage_Bionetworks) (secondary source)

**AMP-AD / AD Knowledge Portal**
- NIH launched AMP AD 2.0 in 2021, with about $61.4M over 5 years. It funds a data coordinating center at Sage Bionetworks and six academic teams. More than 3,000 researchers worldwide had used AMP-AD data resources. — [NIH news release](https://www.nih.gov/news-events/news-releases/nih-invests-next-iteration-public-private-partnership-advance-precision-medicine-research-alzheimers-disease)
- FNIH's 2025 update says AMP AD 2.0 released its first multi-omic dataset (WGS, RNA-seq, proteomics, metabolomics) on brain tissue from **multiethnic** donors, and defined the first molecular subtypes of AD. It also says "new data policies," plus funding and communication changes, "have tested our perseverance". — [FNIH AMP Updates](https://fnih.org/?p=22506)
- The AD Knowledge Portal is built on Sage's Synapse platform. — [AD Knowledge Portal news](https://news.adknowledgeportal.org/nih-invests-in-next-iteration-of-public-private-partnership-to-advance-precision-medicine-research-for-alzheimers-disease)

**AlzPED (NIA Alzheimer's Disease Preclinical Efficacy Database)**
- AlzPED is a public, searchable knowledgebase of curated summaries of preclinical therapeutic studies in AD animal models. A 2025 description reports about 1,400 studies, about 274 targets, 1,206 agents and 226 animal models. — [AlzPED paper, PMC11713837](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11713837/)
- Its rigor report cards show methodological details are often missing: power calculations in only 4% of studies, blinding in 10%, randomization in 32%. Two experts curate each study. A stated long-term goal is to add unpublished and negative studies. — [PMC11713837](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11713837/); [AlzPED analytics summary 2023](https://alzped.nia.nih.gov/sites/default/files/2023-09/AlzPED%20Analytics%20Summary_SC_09-07-2023.pdf)
- Conflict: the RRID/dkNET record (SCR_021230) lists AlzPED's availability as "restricted". The NIA paper describes it as public. — [RRID record](https://rrid.site/data/record/nlx_144509-1/SCR_021230/resolver)

**Alzforum Therapeutics database**
- It catalogs AD and related-disorder therapeutics that reached **Phase 2 or beyond** in U.S. trials, grouped by therapy and target type. Each agent has synonyms, FDA status, sponsor and target type. Alzforum asks for updates at therapeutics@alzforum.org. — [Alzforum Therapeutics](https://alzforum.org/therapeutics); [search page](https://alzforum.org/therapeutics/search)
- **AlzPipeline** (UNLV + Cleveland Clinic) is a continuously updated database of AD trials on ClinicalTrials.gov. At launch it covered 141 drugs in 187 active trials. — [FDAnews](https://www.fdanews.com/articles/212774-141-investigatory-alzheimers-drugs-187-clinical-trials-described-in-new-database)

**Open Targets Platform**
- Open Targets is a "freely available, open-source web portal" for identifying and prioritizing drug targets. It gives disease-level target rankings with an evidence breakdown by data source. — [EMBL-EBI Open Targets training](https://www.ebi.ac.uk/training/online/courses/open-targets-quick-tour/open-targets-platform/)
- Past releases added AD-specific evidence: systems-biology key-driver gene lists (release 18.12) and a rare ABCA7 missense variant (rs143718918) (19.04). — [OT blog 18.12](https://blog.opentargets.org/new-open-targets-platform-release); [OT blog 19.04](https://blog.opentargets.org/open-targets-platform-release-19-04-is-out/)
- Claude has an Open Targets connector, with "What are the top five targets associated with Alzheimer's disease?" as a sample query. — [Claude Open Targets connector tutorial](https://claude.com/resources/tutorials/using-the-open-targets-connector-in-claude)

**Knowledge graphs**
- **AlzKB** (Romano et al., JMIR 2024, Dartmouth/Penn) is a freely available AD knowledge graph built from 22 sources with an OWL2 ontology. It has 118,902 entities and 1,309,527 relationships. Graph ML on it recovered known drug-AD associations and proposed new repurposing candidates. — [AlzKB, PMC11066745](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11066745/); [PubMed 38635981](https://pubmed.ncbi.nlm.nih.gov/38635981/)
- **PrimeKG** (Chandak, Huang & Zitnik, Scientific Data 2023) integrates 20 resources: 129,375 nodes, 4,050,249 edges and 17,080 diseases. Its many drug-disease edges are labeled as indication, contraindication or off-label. — [PrimeKG, PMC9893183](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9893183/); [Zitnik Lab project page](https://zitniklab.hms.harvard.edu/projects/PrimeKG)
- PrimeKG is ingested as a knowledge source by Every Cure's open drug-repurposing data platform. — [Every Cure data page](https://data.dev.everycure.org/versions/v0.15.12/evidence/Knowledge%20Sources/infores:primekg)
- **TxGNN** (Zitnik lab) is a graph foundation model for zero-shot drug repurposing across 17,080 diseases and 7,957 drugs. It reports +49.2% indication and +35.1% contraindication accuracy over 8 baselines and has an Explainer module for multi-hop paths. It is installable from PyPI. — [TxGNN medRxiv](https://www.medrxiv.org/content/10.1101/2023.03.19.23287458.full.pdf); [PyPI txgnn](https://pypi.org/project/TxGNN/)

### Inferences
- The most practical "plug-in" points for a GitHub project:
  - pull Agora / AD Knowledge Portal data via Synapse;
  - query Open Targets via its API or the Claude connector;
  - load AlzKB or PrimeKG as graph inputs and run repurposing models such as TxGNN;
  - cross-reference candidates against AlzPED (preclinical evidence and rigor) and Alzforum Therapeutics (clinical status).
- AlzPED's rigor gaps (4% power calculations, 10% blinding) point to a meta-research niche: tooling that scores or flags rigor in preclinical AD studies.
- The FNIH line about "new data policies" suggests changes to U.S. federal data-sharing in 2025 may affect access. This should be checked before relying on AMP-AD data access paths.

### Gaps
- **ChEMBL, DrugBank, SPOKE, Hetionet**: not verified this session. Background (unverified this session): ChEMBL is CC BY-SA and open; DrugBank's full data needs a free academic or paid commercial license; Hetionet (hetio) is a public integrative network with an earlier repurposing project (Project Rephetio); SPOKE is UCSF's large biomedical KG with access by request.
- Agora's GitHub repo, API and license; Open Targets' latest 2025/2026 release notes for AD; the exact TREAT-AD probe/TEP catalog and its distribution terms (e.g., via the SGC or the AD Knowledge Portal "Tools" pages). None of these were confirmed.
- Specific ADDF open resources (e.g., Cognitive Vitality ratings and the Biomarker Observatory's public outputs) were not detailed in the fetched pages.

## 2. Real-world-data drug repurposing and the clinical pipeline (Cheng lab, sildenafil, GLP-1/semaglutide EVOKE, Cummings 2025/2026)

### Takeaway
Real-world-data repurposing (Cheng lab network medicine plus claims analyses; Xu lab EHR analyses of GLP-1 drugs) produced strong hypotheses. The flagship test, oral semaglutide in EVOKE/EVOKE+, **failed** its primary endpoint in Nov 2025. Repurposed drugs remain a growing share of the pipeline: 56 agents, 35% of 158 drugs in 2026. The Cummings pipeline review is co-authored with Cheng's Cleveland Clinic group, which ties the two efforts together.

### Cited Findings
**Cummings pipeline review 2026** ("Alzheimer's disease drug development pipeline: 2026", *Alzheimer's & Dementia: TRCI*, May 5, 2026, DOI 10.1002/trc2.70251)
- Size: **192 trials** testing **158 drugs**, up from 182 trials / 138 drugs in 2025 and 164 / 127 in 2024. There were 59 new trials in the past year. Since 2016, trials rose 35% and agents 40%. — [UNLV release](https://www.unlv.edu/news/release/alzheimers-drug-development-pipeline-shows-impressive-growth-and-diversity-therapies)
- (Vetting: a peer-reviewed annual census of ClinicalTrials.gov, not an efficacy claim. Counts depend on the authors' inclusion rules. See Section 6 for COI notes.)
- **56 repurposed agents (35% of drugs)**. Amyloid-targeting drugs are 18% of the pipeline, down from about a third in 2016. Inflammation/immune targets rose from 6% to 18%. 29 Phase 2 trials report in 2026. — [UNLV release](https://www.unlv.edu/news/release/alzheimers-drug-development-pipeline-shows-impressive-growth-and-diversity-therapies)
- Co-authors include Yadi Zhou, Yuxin Yang and **Feixiong Cheng** (Cleveland Clinic / Case Western). — [UNLV release](https://www.unlv.edu/news/release/alzheimers-drug-development-pipeline-shows-impressive-growth-and-diversity-therapies)
- ADDF: 158 therapies vs 93 ten years ago. 75% of trials target pathways beyond amyloid and tau. **83% of active trials include a biomarker**. ADDF backs this work through its "Biomarker Observatory". — [ADDF announcement](https://www.alzdiscovery.org/news-room/announcements/goodes-prize-recipient-dr-jeff-cummings-2026-alzheimers-drug-pipeline-report-signals-new-era-of-biology-driven-approaches)
- Eight Phase 3 trials reach primary completion in 2026. Repurposed examples include metformin and BMS's Cobenfy (xanomeline-trospium). — [GeneOnline](https://www.geneonline.com/eight-phase-3-trials-29-phase-2-readouts-and-a-diversifying-pipeline-eyes-on-alzheimers-in-2026/); [PharmaVoice](https://www.pharmavoice.com/news/amyloid-alzheimers-bms-cobenfy-drug-research/821647/)
- ADDF has awarded nearly $400M to 792 programs in 21 countries since 1998. — [ADDF](https://www.alzdiscovery.org/news-room/announcements/goodes-prize-recipient-dr-jeff-cummings-2026-alzheimers-drug-pipeline-report-signals-new-era-of-biology-driven-approaches)

**Cummings pipeline 2025** (DOI 10.1002/trc2.70098)
- **182 trials / 138 drugs**: Phase 3 had 48 trials / 31 drugs, Phase 2 had 86 / 75, Phase 1 had 48 / 45. Disease-targeted therapies were 74% of drugs, amyloid 18%. There were 46 repurposed drugs and more than 50,000 participants. — [2025 paper PDF via NIHR](https://www.dementiaresearcher.nihr.ac.uk/wp-content/uploads/2025/06/A-D-Transl-Res-Clin-Interv-2025-Cummings-Alzheimer-s-disease-drug-development-pipeline-2025.pdf); [UNLV 2025 release](https://www.unlv.edu/news/release/annual-alzheimers-clinical-trials-pipeline-report-shows-increased-reason-optimism)

**Semaglutide EVOKE / EVOKE+ (Novo Nordisk)**
- Topline on Nov 24, 2025: oral semaglutide showed **no statistically significant slowing on CDR-SB** vs placebo in either trial. The trials enrolled 3,808 people with MCI or mild AD over 2 years. Biomarkers improved but clinical outcomes did not. The 1-year extension was discontinued. — [Alzheimer Europe](https://www.alzheimer-europe.org/news/novo-nordisk-announces-topline-results-evoke-and-evoke-trials-semaglutide-early-ad); [NeurologyLive](https://www.neurologylive.com/view/glp-1-semaglutide-fails-outperform-placebo-phase-3-evoke-trial-ad)
- CDR-SB change over 2 years: EVOKE was +2.2 in both arms. EVOKE+ was +2.1 on semaglutide vs +2.0 on placebo. — [Precision Medicine Online](https://www.precisionmedicineonline.com/node/44766); [Alzheimer's News Today](https://alzheimersnewstoday.com/news/oral-semaglutide-fails-slow-alzheimers-pair-clinical-trials/)
- Fuller data were presented at CTAD in Dec 2025 and at AAN 2026. — [NeurologyLive CTAD](https://www.neurologylive.com/view/ctad-presentation-lays-insights-disappointing-phase-3-evoke-trial-of-glp-1-semaglutide-alzheimers); [AAN 2026 abstract](https://index.mirasmart.com/AAN2026/PDFfiles/AAN2026-004189.html)
- The prior EHR signal came from Rong Xu's group at Case Western, not the Cheng lab. In 17,104 new semaglutide users vs 1,077,657 users of other antidiabetics, semaglutide was associated with a **40–70% lower risk** of first AD diagnosis over 3 years (Alzheimer's & Dementia, Oct 2024). The authors cautioned against causal conclusions. — [Psychiatric News](https://alert.psychnews.org/2024/10/semaglutide-linked-to-lower-risk-of.html); [Lab Manager](https://www.labmanager.com/weight-loss-drug-may-lower-alzheimer-s-risk-in-diabetic-patients-33028)
- A UK trial (ISRCTN71283871) is testing semaglutide's effect on AD proteins and inflammation in high-risk people. — [ISRCTN](https://www.isrctn.com/ISRCTN71283871)

**Cheng lab (Cleveland Clinic) network medicine / sildenafil**
- Their 2021 *Nature Aging* work combined gene expression, protein networks and patient/insurance data and nominated sildenafil. A 2024 *J Alzheimer's Dis* follow-up used MarketScan Medicare Supplemental (2012–2017) and Clinformatics (2007–2020). It found sildenafil associated with a **30–54% lower AD prevalence** vs four comparator drugs. In iPSC-derived neurons, sildenafil reduced pTau181/pTau205 in a dose-dependent way. The authors call for RCTs and advise against using it for prevention. — [Cleveland Clinic ConsultQD](https://consultqd.clevelandclinic.org/sildenafil-as-an-alzheimers-candidate-drug-further-support-from-insurance-database-and-mechanistic-studies); [JAD 2024](https://journals.sagepub.com/doi/reader/10.3233/JAD-231391); [Inside Precision Medicine](https://www.insideprecisionmedicine.com/topics/precision-medicine/viagra-might-be-able-to-prevent-and-treat-alzheimers)

### Inferences
- EVOKE is a key cautionary case. A large, consistent RWD association (40–70% risk reduction) did not translate into a disease-slowing effect in a 3,808-person RCT, although biomarkers moved. Any open repurposing project should frame RWD and KG hits as hypotheses. It should build in confounding and indication-bias checks, such as negative controls and target-trial emulation.
- The share of repurposed agents (35%) and the shift to inflammation/immune targets (18%) suggest where computational repurposing work has the most traction with trialists.
- Cummings' review draws on ClinicalTrials.gov (via AlzPipeline/Cheng lab co-authorship). A machine-readable, versioned open mirror of the pipeline tables on GitHub would plausibly be a useful community contribution, if one does not already exist.

### Gaps
- Phase-by-phase counts for 2026, and whether AlzPipeline is still publicly online and downloadable.
- Cheng lab 2025–2026 outputs (e.g., AlzGPS status, newer EHR emulation studies) were not retrieved.
- Whether sildenafil has entered a registered AD RCT as of 2026 was not found.

## 3. Open-science initiatives, communities and the funding landscape

### Takeaway
The best-funded open community hub is the **Alzheimer's Disease Data Initiative (ADDI, Gates Ventures-linked)**. It runs AD Workbench and prize competitions; the 2025–26 AI Prize paid out $2M and feeds "AI Collaboratories". AMP-AD/Sage (Synapse, DREAM), the Allen Institute's SEA-AD, CZI's Neurodegeneration Challenge Network and citizen-science projects (Stall Catchers, Folding@home) complete the picture. Many of these date from 2016–2020, and their current activity levels are unclear.

### Cited Findings
**ADDI / AD Workbench / Gates**
- The Alzheimer's Insights AI Prize launched Aug 2025 for agentic AI tools and drew more than 180 submissions. Ten semifinalists pitched at CTAD in Dec 2025. Five finalists presented on Mar 17, 2026 in Copenhagen. On Mar 20, 2026 two winners were named, each receiving **$1M**: **Biomni-AD** (Stanford + Icahn Mount Sinai, an AI "co-scientist") and **Prima Mente** (PARTHENON virtual wet lab with the "Athena" co-scientist). — [ADDI announcement](https://www.alzheimersdata.org/news/alzheimer-s-disease-data-initiative-doubles-1m-prize-competition-for-agentic-ai-solutions-to-accelerate-alzheimer-s-research); [HPCwire](https://www.hpcwire.com/aiwire/2026/03/25/alzheimers-disease-data-initiative-doubles-1m-prize-competition-for-agentic-ai-solutions/)
- Winning tools will be made **freely available to researchers worldwide via AD Workbench**. All 10 semifinalists are invited to "AI Collaboratories" that pair AI developers with AD researchers. The announcement states no open-source requirement. — [ADDI](https://www.alzheimersdata.org/news/alzheimer-s-disease-data-initiative-doubles-1m-prize-competition-for-agentic-ai-solutions-to-accelerate-alzheimer-s-research)
- Gates ties: ADDI's interim Executive Director, Niranjan Bose, is MD of Health & Life Sciences at Gates Ventures. Gates Ventures' Gregory Moore chaired the judges. Bill Gates and a coalition of partners funded the prize. — [ADDI](https://www.alzheimersdata.org/news/alzheimer-s-disease-data-initiative-doubles-1m-prize-competition-for-agentic-ai-solutions-to-accelerate-alzheimer-s-research); [AI Business](https://aibusiness.com/generative-ai/bill-gates-backs-1m-ai-prize-to-tackle-alzheimer-s)
- Source-quality note: some CO/AI pages carry 2026 dates on content that matches the Aug 2025 launch. — [getcoai](https://getcoai.com/news/gates-backed-1m-prize-targets-ai-systems-for-alzheimers-research/)

**DREAM / Sage / Allen SEA-AD challenges**
- The **SEA-AD DREAM Challenge**, hosted on Synapse and listed by the Allen Institute, asked participants to predict AD neuropathological burden from single-cell gene expression. It is now marked "completed". Related publications are Gabitto, Travaglini et al. 2024 and Lai et al. 2026. — [Allen Brain Map data challenges](https://brain-map.org/bkp/analyze/data-challenges)
- The earlier **AD Big Data DREAM Challenge #1** (Sage + Global CEO Initiative on AD, hosted on Synapse) focused on genetics, imaging and biomarkers. — [BrightFocus](https://www.brightfocus.org/grant/support-sage-bionetworks-alzheimers-big-data-dream-challenge-1); [Alzforum](https://alzforum.org/node/290851)

**CZI Neurodegeneration Challenge Network (NDCN)**
- NDCN brings together biologists, computational scientists, engineers and physicians, with "open science" as a stated cultural goal. Funding included Ben Barres Early Career Acceleration Awards (17 investigators, $2.5M each) and Collaborative Science Awards ($1.05M per group). A Sept 2025 impact report ("A Model for Collaborative Scientific Impact") is now hosted on biohub.org. The original 2018 RFA is closed. — [CZI NDCN impact report (Sept 2025)](https://biohub.org/wp-content/uploads/sites/32/2025/09/czi-ndcn-impact-report.pdf); [Biohub NDCN page](https://biohub.org/life-science/neurodegeneration-challenge-network); [CZI project page](https://chanzuckerberg.com/science/projects-challenge-network)

**Citizen science**
- **Stall Catchers / EyesOnALZ** (Human Computation Institute + Cornell Schaffer-Nishimura lab; funded by BrightFocus) asks volunteers to classify mouse-brain capillary segments as flowing or stalled. Crowd answers are aggregated by a "wisdom of the crowd" algorithm. Stalled capillaries are linked to AD in mice. — [BrightFocus](https://brightfocus.org/news/crowdsourcing-alzheimers-data-through-new-eyesonalz-game-will-accelerate-research-brightfocus); [SciStarter](https://scistarter.org/citizen-science-stall-catchers)
- An arXiv paper reports more than 42,000 registered users and more than 12M annotations (date of counts unclear). — [arXiv 2208.07960](https://arxiv.org/pdf/2208.07960)
- **Folding@home** lists Alzheimer's among its neurological disease targets. Its historical AD work includes Aβ oligomerization simulations (2008) and the design of Aβ aggregation inhibitors (J Med Chem 2012). — [Folding@home diseases](https://foldingathome.org/diseases); [F@h Aβ inhibitors post](https://old.foldingathome.org/?p=13076)

### Inferences
- ADDI is the most active community-facing funder for computational and AI work in 2025–26. Its model is prizes plus platform hosting (AD Workbench) plus collaboratories, not open-source code. An open GitHub project would be most visible if it became an AD Workbench-compatible tool or entered a future ADDI challenge.
- Synapse-hosted DREAM challenges are the main historical on-ramp for independent computational researchers in AD. No active AD DREAM challenge was confirmed as of Oct 2026.

### Gaps
- **Not verified this session:** EBRAINS, Neuromatch, OHBM Open Science SIG, Foldit AD puzzles, Kaggle AD competitions, Alzheimer's Association open-science programs (e.g., GAAIN, Part the Cloud), current AD Workbench dataset counts and the ADDI data challenge schedule for 2026–27.
- Whether Stall Catchers is still active in 2026, and whether Folding@home has a current AD/tau project. No 2024–2026 sources were found.
- The specific 2025 NIH data-policy changes that FNIH mentioned.

## 4. GitHub organizations, repositories and awesome-lists

### Takeaway
I found **no dedicated, maintained "awesome-alzheimers" list** in web search results, and GitHub search was blocked here, so this is an open niche. The known code ecosystem is scattered across lab orgs: aramis-lab for ADNI ML/ClinicaDL, Zitnik lab for PrimeKG/TxGNN, Sage Bionetworks for Agora/Synapse, and others.

### Cited Findings
- No AD-specific awesome-list surfaced. The closest curated list is a general "Awesome Machine Learning in Biomedical (Healthcare) Imaging". — [ecosyste.ms awesome search results](https://awesome.ecosyste.ms/projects/github.com%2Fbintangyosua%2Falzheimer)
- **aramis-lab/ad-ml** is a reproducible ML framework for AD classification from multimodal MRI/PET (ADNI, AIBL, OASIS). **aramis-lab/ad-dl** is archived and points users to **ClinicaDL**. — [ecosyste.ms](https://awesome.ecosyste.ms/projects/1463366)
- GitHub's `alzheimer` topic page aggregates many repos, mostly small classification projects. — [GitHub topic: alzheimer](https://github.com/topics/alzheimer?o=desc&s=updated)
- TxGNN's official implementation is distributed via PyPI from the Zitnik lab. — [PyPI TxGNN](https://pypi.org/project/TxGNN/)
- AlzKB is described as freely available. Its code is reportedly from the Penn/EpistasisLab group, but the repo is unverified this session. — [AlzKB paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11066745/)

### Inferences
- A curated, maintained "awesome-alzheimers-open-science" list would fill a visible gap: data portals, KGs, pipelines, challenges and citizen science. It is a low-barrier first contribution for a new public GitHub project.

### Gaps
- Exact GitHub org/repo names, stars, licenses and activity for Sage-Bionetworks (Agora, synapsePythonClient), EpistasisLab/AlzKB, mims-harvard/PrimeKG and TxGNN, hetio/hetionet, opentargets, aramis-lab/clinicadl. Verification attempts returned HTTP 403 because the session is bound to its configured repositories. These should be checked manually.

## 5. How outsiders and independent contributors realistically contribute

### Takeaway
Realistic routes for unaffiliated contributors, roughly from easiest to hardest:
- citizen science;
- reporting corrections to curated databases (Alzforum asks for this by email);
- competing in data challenges and prizes (ADDI, DREAM/Synapse);
- building reproducible analyses on open data (Agora/AD Knowledge Portal, Open Targets, AlzKB/PrimeKG);
- nominating targets to Agora;
- joining collaboratories or consortia, which usually means partnering with a funded lab.
Controlled-access human data (AMP-AD individual-level omics, AD Workbench datasets) generally requires a data-use agreement and an institutional affiliation.

### Cited Findings
- Agora accepts target nominations from "the broader AD research community," not only consortium members. — [PMC12726812](https://pmc.ncbi.nlm.nih.gov/articles/PMC12726812/)
- Alzforum Therapeutics invites public update reports via therapeutics@alzforum.org. — [Alzforum Therapeutics](https://alzforum.org/therapeutics)
- ADDI's prize was open to outside teams. The winners included a startup (Prima Mente), and semifinalists get AI Collaboratory pairings with AD researchers. — [ADDI](https://www.alzheimersdata.org/news/alzheimer-s-disease-data-initiative-doubles-1m-prize-competition-for-agentic-ai-solutions-to-accelerate-alzheimer-s-research)
- DREAM challenges on Synapse are crowdsourced and open to registered participants. — [Allen data challenges](https://brain-map.org/bkp/analyze/data-challenges); [BrightFocus on AD DREAM #1](https://www.brightfocus.org/grant/support-sage-bionetworks-alzheimers-big-data-dream-challenge-1)
- Stall Catchers is open to anyone on a laptop, tablet or phone. — [BrightFocus](https://brightfocus.org/news/crowdsourcing-alzheimers-data-through-new-eyesonalz-game-will-accelerate-research-brightfocus)
- AlzPED aims to take in unpublished and negative preclinical studies, which is a channel for labs to deposit results. — [PMC11713837](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11713837/)

### Inferences
- The highest-leverage open GitHub contributions for an independent project are likely:
  1. reproducible pipelines that join public, non-controlled resources (Open Targets plus Agora summary data plus AlzKB/PrimeKG plus Alzforum/ClinicalTrials.gov status) to rank and triage repurposing candidates, with explicit caveats drawn from the EVOKE lesson;
  2. a versioned, machine-readable tracker of the AD clinical pipeline;
  3. a curated awesome-list;
  4. rigor-checking or meta-research tools that build on AlzPED.
- Unaffiliated contributors cannot easily use controlled-access human data. Designing on open or summary-level data first, and partnering with an academic lab for controlled data, is the realistic route.

### Gaps
- No primary source fetched here describes Synapse/AD Knowledge Portal access tiers or the AD Workbench approval process in 2026. Background (unverified this session): Synapse needs a free account, plus a certified-user quiz and DUAs for controlled data.
- Funding open to independent or non-institutional researchers (e.g., ADDF, Alzheimer's Association, BrightFocus eligibility rules) was not verified.

## 6. Vetting: evidence quality, integrity red flags and conflicts of interest

### Takeaway
The AD field has documented, high-profile integrity failures:
- simufilam/Cassava: SEC settlement, DOJ indictment of the co-developer, two failed Phase 3 trials;
- the 2006 Lesné Aβ*56 *Nature* paper: retracted June 2024;
- Eliezer Masliah: NIH misconduct finding in Sept 2024, with a dossier of 132 papers flagged.

The field also has a clear pattern of observational repurposing signals that fail or conflict under stronger designs: semaglutide/EVOKE, and sildenafil with a null active-comparator cohort. Every resource and claim in these notes must therefore be treated as "unverified until checked". Curated databases (AlzPED, knowledge graphs, Agora literature evidence) can silently contain retracted or compromised studies and need retraction filtering before use.

### Cited Findings
**Documented red flags (contamination risk for any literature-derived resource)**
- RED FLAG, simufilam (Cassava Sciences):
  - Both Phase 3 trials (RETHINK-ALZ, REFOCUS-ALZ) failed and Cassava ended the AD program. — [Clinical Trials Arena](https://www.clinicaltrialsarena.com/news/cassava-sciences-simufilam-flops-phase-iii/); [Being Patient](https://beingpatient.com/cassava-gives-up-on-simufilam-alzheimers-drug/)
  - Cassava paid **$40M to settle SEC charges** over allegedly misleading Phase 2b data. Ex-CEO Remi Barbier and ex-SVP Lindsay Burns also settled with the SEC. — [Xtalks](https://xtalks.com/cassava-sciences-ends-simufilam-alzheimers-program-after-another-phase-iii-failure-4168); [Cassava 10-K FY2024](https://www.sec.gov/Archives/edgar/data/1069530/000143774925005919/sava20241231c_10k.htm)
  - Co-developer and paid adviser **Hoau-Yan Wang was indicted by DOJ** for fraud and charged by the SEC with manipulating results. The sources here do not say Burns was criminally indicted, so do not claim that. — [Clinical Trials Arena](https://www.clinicaltrialsarena.com/?p=221574)
  - Implication: the Cummings **2025** pipeline listed simufilam among expected Phase 3 readouts ([NIHR summary](https://www.dementiaresearcher.nihr.ac.uk/2025-alzheimers-drug-pipeline-shows-growth-and-diversity)). Pipeline inclusion is **not** evidence of scientific validity.
- RED FLAG, Lesné *Nature* 2006 (Aβ*56):
  - Retracted June 2024 over image manipulation. All authors except Lesné agreed to the retraction. Concerns extend to at least 20 other Lesné papers. — [Wikipedia: Sylvain Lesné](https://en.wikipedia.org/wiki/Sylvain_Lesn%C3%A9) (secondary); [Minnesota Reformer](https://minnesotareformer.com/2025/02/07/alzheimers-researcher-alleged-to-have-doctored-images-is-leaving-umn/)
  - Senior author Karen Ashe maintains the conclusions hold and cites a 2024 *iScience* paper. — [Wikipedia: Karen Ashe](https://en.wikipedia.org/wiki/Karen_Ashe) (secondary)
  - Lesné left UMN effective March 1, 2025. — [Minnesota Reformer](https://minnesotareformer.com/2025/02/07/alzheimers-researcher-alleged-to-have-doctored-images-is-leaving-umn/)
- RED FLAG, Eliezer Masliah:
  - The NIH found research misconduct in Sept 2024 (reused or relabeled figures). A *Science* dossier flagged **132 papers (1997–2023)** with apparent duplicated or doctored images. Masliah, the former NIA neuroscience director, is no longer in that role. — [Alzforum](https://alzforum.org/news/community-news/data-fabrication-ousted-nia-neuroscience-director-eliezer-masliah)
  - Masliah's work is heavily cited in neurodegeneration, including α-synuclein and AD neuropathology and animal-model studies. Any KG or preclinical database built from the literature may include his findings. Retraction counts as of 2026 were not confirmed.

**Observational vs RCT evidence for repurposing claims**
- Semaglutide:
  - EHR studies associated semaglutide with 40–70% lower AD risk ([Psychiatric News](https://alert.psychnews.org/2024/10/semaglutide-linked-to-lower-risk-of.html)). The Phase 3 RCTs EVOKE/EVOKE+ (n=3,808) showed **no clinical benefit** ([Alzheimer Europe](https://www.alzheimer-europe.org/news/novo-nordisk-announces-topline-results-evoke-and-evoke-trials-semaglutide-early-ad)).
  - Verdict: the observational signal was **refuted by RCT** for oral semaglutide in early symptomatic AD. Prevention in at-risk diabetics remains untested.
- Sildenafil:
  - The Cheng lab's claims-data association (30–54% lower prevalence) is observational, plus iPSC mechanistic data. No RCT was found. — [Cleveland Clinic](https://consultqd.clevelandclinic.org/sildenafil-as-an-alzheimers-candidate-drug-further-support-from-insurance-database-and-mechanistic-studies)
  - **Conflicting evidence:** Desai et al. (*Brain Communications* 2022) ran an active-comparator Medicare cohort of PAH patients, PDE5 inhibitors vs endothelin receptor antagonists, with 76-confounder propensity matching. They found **no reduced ADRD risk**, with HRs from 0.67 to 1.15 across four bias-handling analyses. Sildenafil also failed to correct AD-relevant phenotypes in most cell assays. — [Brain Communications](https://academic.oup.com/braincomms/article/6731685); [PubMed 36330433](https://pubmed.ncbi.nlm.nih.gov/36330433/)
  - A 2025 meta-analysis of 5 observational studies (885,380 patients) reported HR 0.47. It pools confounding-prone designs, and its authors call for RCTs. — [Aging 2025](https://aging-us.com/article/206222); [PMC11984433](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11984433/)
  - Verdict: **unconfirmed and contested**. Stronger-design studies give null results.
- KG and ML repurposing (AlzKB, PrimeKG/TxGNN): both are peer-reviewed resource papers (JMIR 2024; *Sci Data* 2023). Their AD repurposing outputs are **in-silico hypotheses**, validated retrospectively against known associations, not prospectively. — [AlzKB](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11066745/); [PrimeKG](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9893183/)
- Preclinical evidence base: AlzPED's own audit shows only 4% of AD animal studies report power calculations, 10% blinding and 32% randomization. Preclinical efficacy claims are therefore weak by default. — [PMC11713837](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11713837/)

**Conflicts of interest and governance (as found)**
- Cummings pipeline: ADDF has a "long-standing collaboration" with Cummings and gave him its Goodes Prize. ADDF is a drug-development funder with its own portfolio. — [ADDF](https://www.alzdiscovery.org/news-room/announcements/goodes-prize-recipient-dr-jeff-cummings-2026-alzheimers-drug-pipeline-report-signals-new-era-of-biology-driven-approaches)
- The 2026 review is co-authored with Cheng's group, whose repurposing work it may cover. — [UNLV](https://www.unlv.edu/news/release/alzheimers-drug-development-pipeline-shows-impressive-growth-and-diversity-therapies)
- The individual industry disclosures of Cummings and co-authors were not retrieved. They are printed in the paper and should be checked.
- ADDI AI Prize: ADDI leadership and the judging chair are Gates Ventures staff, and the prize is Gates-backed. — [ADDI](https://www.alzheimersdata.org/news/alzheimer-s-disease-data-initiative-doubles-1m-prize-competition-for-agentic-ai-solutions-to-accelerate-alzheimer-s-research)
- One winner, Prima Mente, is a company. The announcement gives no open-source or independent-benchmark requirement, so winning tools' performance claims are **not independently validated** in what was found.
- EVOKE results come from the sponsor (Novo Nordisk topline and CTAD). A peer-reviewed full publication was not confirmed, though in this case the sponsor-reported result is negative, which lowers spin risk.

### Vetting table (per resource or claim)
| Item | Peer-reviewed? | Replicated / independent? | Evidence tier | Controversies / COI | What's needed to verify |
|---|---|---|---|---|---|
| Agora (950+ targets) | Yes (resource papers, PMC11709802/PMC12726812) | Target nominations are hypotheses from AMP-AD/TREAT-AD omics; replication per target varies | Hypothesis-generating omics | Nominations come from consortium teams that also study them; no formal outside review of each nomination found | Check each target's nomination source, cohort sizes, cross-cohort consistency; screen any cited literature for retractions |
| TREAT-AD probes/TEPs | Yes (PMC11712476) | Tools themselves are QC'd per the paper; target-disease links unproven | Research tools, not efficacy | None found | Confirm probe selectivity data, distribution terms; independent use reports |
| AMP-AD / AD Knowledge Portal data | Data releases + consortium papers | Molecular subtypes "first defined"; independent replication not confirmed | Primary data (strong) / subtypes (emerging) | 2025 "new data policies" note (FNIH) | Check current access policy; verify subtypes replicate in independent cohorts |
| AlzPED | Yes (PMC11713837) | Curates studies, does not replicate them | Preclinical, mostly low rigor | RRID lists "restricted" vs NIA says public (conflict) | Check access; cross-check included studies against Retraction Watch DB / PubPeer (Masliah, Lesné-linked papers) |
| Alzforum Therapeutics | Editorial (journalistic), not peer-reviewed | N/A | Status catalog | Alzforum is a news and community site; check its funding sources | Cross-check each entry against ClinicalTrials.gov and sponsor filings |
| Open Targets | Yes (NAR papers) | Aggregates many sources | Integrated evidence scores | Pharma consortium partners (EMBL-EBI, Sanger, GSK and others; unverified this session) | Inspect per-datasource evidence and avoid relying on the literature-mining score alone |
| AlzKB, PrimeKG, Hetionet | Yes (resource papers) | Benchmarks are retrospective | In-silico | Literature-derived edges may include retracted findings | Version-pin, run a retraction filter over provenance, and test prospective or held-out-time predictions |
| TxGNN predictions | Yes (later published; medRxiv preprint fetched) | Retrospective plus clinician evaluation | In-silico | — | Independent re-runs; AD-specific predictions not found |
| Cummings pipeline 2025/2026 | Yes (A&D:TRCI) | Annual series, consistent methods | Census of trials | ADDF partnership; co-authors' industry disclosures need checking; inclusion of simufilam shows listing ≠ validity | Read the disclosures section; spot-check counts against ClinicalTrials.gov |
| Semaglutide → AD | EHR studies peer-reviewed; EVOKE sponsor-reported | RCT run | **RCT: negative** | Sponsor-run trials | Peer-reviewed EVOKE paper; prevention-population trials |
| Sildenafil → AD | Yes (Nat Aging 2021, JAD 2024) | **Contradicted** by active-comparator cohort (Desai 2022) | Observational + cell models | Possible confounding (healthy user, indication) | Registered RCT; target-trial emulations with active comparators |
| Simufilam | Early data compromised | Phase 3 ×2 failed | **RCT: negative; RED FLAG fraud** | SEC $40M settlement; DOJ indictment of co-developer | Exclude from evidence bases; flag in any KG |
| Aβ*56 (Lesné 2006) | Retracted | Ashe 2024 iScience claims replication, not independently confirmed | **RED FLAG** | Image manipulation | Treat Aβ*56-specific claims as unsupported unless independently replicated |
| Masliah-authored findings | 132 papers flagged | — | **RED FLAG** | NIH misconduct finding | PubPeer/Science dossier lookup for any cited paper |
| ADDI AI Prize winners (Biomni-AD, Prima Mente) | Not as prize outputs | Not found | Unvalidated tools | Gates-linked judges; commercial winner | Independent benchmarks, code/model availability, published evaluations |
| Stall Catchers crowd accuracy | arXiv/peer-reviewed reports exist | Claimed expert-level accuracy; one validation snippet came from a poor source | Methodological | — | Check the primary validation paper (HCI/Cornell) |
| CZI NDCN impact report | Self-published impact report | N/A | Grey literature | Self-assessment | Look for the underlying peer-reviewed outputs |

### Inferences
- An open AD repurposing project should build in **integrity hygiene** as a core feature:
  - retraction filtering of all literature-derived edges and evidence (Retraction Watch database, now hosted by Crossref, plus PubPeer flags; unverified this session);
  - evidence-tier labels on every claim (in-silico / preclinical / observational / RCT);
  - explicit tracking of known-fraud entities (simufilam, Aβ*56, Masliah-authored studies).
- The EVOKE and sildenafil cases show that claims data and EHR associations, even with large effect sizes and mechanistic support, have repeatedly failed to replicate under stronger designs. Active-comparator, new-user, target-trial-emulation designs should be the minimum standard before calling a repurposing signal promising.
- Pipeline counts are reliable as a census. "Repurposed agents in trials" signals investigator interest, not efficacy.
- Anything the user brings in (papers, datasets, drug claims) needs the same checks: a peer-review and retraction check, an independent-replication search, the evidence tier, sponsor and author COI disclosures, and a pre-registration or ClinicalTrials.gov match for trial claims.

### Gaps
- Exact current retraction counts for Masliah and Lesné papers, and whether AlzPED, Agora or AlzKB contain any of them. This needs a provenance scan, which was not attempted.
- COI disclosures of the Cummings 2026 authors, and Alzforum's funding sources. Not retrieved.
- A peer-reviewed full EVOKE/EVOKE+ publication was not confirmed as of Oct 2026.
- Whether Wang's DOJ case has concluded (verdict or plea) was not found.
