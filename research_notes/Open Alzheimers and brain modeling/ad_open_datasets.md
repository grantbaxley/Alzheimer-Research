# Open and Accessible Datasets, Cohorts, and Data Platforms for Alzheimer's Disease Research (as of Oct 2026)

Scope: the access model (fully open, application/DUA, or controlled), data types, size, how to get access, and redistribution limits for a new public GitHub project. Research date: 2026-10-18. Around 20 search/fetch calls. Primary portals were used where they could be fetched.

Access-tier legend used below:
- **OPEN**: anyone can download, at most with a free account, and no project review.
- **REGISTERED/OPEN-WITH-TERMS**: free download under terms of use (citation, no re-identification). No project review.
- **DUA/APPLICATION**: needs an online application, review by a committee, and acceptance of a DUA.
- **CONTROLLED**: needs a DUC/DUA plus an institutional signature and/or NIH dbGaP-style review, or access only inside a secure enclave.

---

## 1. Major cohorts and their access terms

### Takeaway
Almost every major AD cohort (ADNI, OASIS, AIBL, NACC, A4/LEARN, UK Biobank, ROSMAP/Mayo/MSBB via the AD Knowledge Portal, ADSP/NIAGADS, EPAD, GNPC, DPUK cohorts) needs an application and a DUA. Many also forbid redistributing individual-level data, and some forbid redistributing derived data. None of them can be committed to a public GitHub repo. SEA-AD is the main exception: its processed data is free to download.

### Cited Findings

**ADNI (Alzheimer's Disease Neuroimaging Initiative)**: DUA/APPLICATION
- Data is shared through the LONI Image and Data Archive (IDA). Access is for "scientific investigation, teaching, or planning clinical research studies." Applicants accept the DUA and submit an online form giving their institutional affiliation and proposed use. The Data Sharing and Publications Committee generally reviews within about 2 weeks. Applicants must be affiliated with a scientific or educational institution. Accounts expire unless renewed each year. No fee is mentioned. — [ADNI Data page](https://adni.loni.usc.edu/data-samples/adni-data/)
- Data types: longitudinal clinical, structural/functional/molecular imaging (MRI, PET), biofluid biomarkers, cognitive assessments, genetics, demographics, neuropathology, and remotely collected data from ADNI4. The most comprehensive genomics/omics data is reached through NIAGADS and NACC, which have their own approvals. — [ADNI Data page](https://adni.loni.usc.edu/data-samples/adni-data/)
- DUA clauses (verbatim), which matter for a public repo:
  - "I understand that redistribution of individual participant-level data in any manner is prohibited."
  - "I will not further disclose these data beyond the uses outlined in this agreement and my data use application."
  - "I am not allowed to distribute ADNI data outside of my team."
  - "I understand derived datasets should only be shared through the ADNI-LONI and/or other NIA-designated data repository."
  - Using AI tools "which may release ADNI participant level data to others, is in direct violation."
  - Publications must list "ADNI" as an author on the by-line, be submitted to the ADNI Data and Publications Committee (DPC) before journal submission, and acknowledge ADNI funding. — [ADNI DUA on LONI IDA](https://ida.loni.usc.edu/collaboration/access/appApply.jsp?project=ADNI)
- The ADNI site has a banner saying the repository is "under review for potential modification in compliance with Administration directives." — [ADNI Data page](https://adni.loni.usc.edu/data-samples/adni-data/). A search summary also reported an IDA notice about the review and a November 2025 maintenance outage. — [IDA login](https://ida.loni.usc.edu/login.jsp?project=A4)
- TADPOLE challenge data (derived from ADNI) can be downloaded only from the IDA "Download | Study Data | Test" section, so it falls under the ADNI DUA. — [ADNI TADPOLE announcement](https://adni.loni.usc.edu/tadpole-challenge-dataset-available/)

**OASIS-1/2/3/4 (Open Access Series of Imaging Studies, WashU)**: DUA/APPLICATION for all four
- OASIS-1: 416 subjects aged 18–96 (100 over 60 with very mild to moderate AD), T1w MRI. OASIS-2: 150 subjects, 373 longitudinal MRI sessions, ages 60–96. OASIS-3: 1,378 participants, 2,842 MR sessions (T1w, T2w, FLAIR, ASL, SWI, TOF, rs-BOLD, DTI) with FreeSurfer outputs, and 2,157+ PET scans (PIB, AV45, FDG) with PUP-processed files. Of the participants, 755 are cognitively normal and 622 are at various stages of decline. OASIS-3 Tau: 451 flortaucipir (AV1451) PET sessions. OASIS-4: 663 subjects aged 21–94 with MR, clinical, CSF, and neuropsychology data. — [OASIS Brains site](https://sites.wustl.edu/oasisbrains/)
- Access: all datasets are hosted on NITRC-IR. Users register with NITRC and apply, and OASIS staff review the request. OASIS-3 Tau needs a separate request. The site does not describe any download that skips the application. — [OASIS Brains site](https://sites.wustl.edu/oasisbrains/)
- Terms: use is limited to "non-commercial, academic research purposes only," and commercial use needs prior written authorization. Re-identification is prohibited, as is generating face or head renderings. OASIS-3/4 data, and derivatives that could reconstruct a face, may not be shared beyond what the agreement allows. Data must be destroyed or returned when the work ends. Publications using AV45 or AV1451 data must go to Avid Radiopharmaceuticals 30 days before submission. No Creative Commons license is stated. — [OASIS Brains site](https://sites.wustl.edu/oasisbrains/)
- The name "Open Access" is misleading: today OASIS is DUA-gated, non-commercial data. Note: one older Scientific-Data-style description calls OASIS-3 "available as an open access data set to the scientific community" (1,098 participants). This conflicts with the current site's figure of 1,378 participants and its gated access. — [KARI paper (PMC11716975)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11716975/)
- The related Knight Alzheimer Research Imaging (KARI) dataset (MRI+PET) "can be accessed upon request." — [KARI data descriptor](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11716975/)

**AIBL (Australian Imaging, Biomarker & Lifestyle)**: DUA/APPLICATION
- Access is through a LONI IDA application form under AIBL terms of use. A combined ADNI+AIBL form exists. Use is limited to scientific investigation, teaching, or planning clinical studies. Commercial use is not permitted, and publications must cite AIBL. — [AIBL Study ADNI data page](https://data.aibl.org.au/adni/index.html); [LONI AIBL+ADNI application](https://ida.loni.usc.edu/collaboration/access/appApply.jsp?project=AIBL&project=ADNI)

**NACC (National Alzheimer's Coordinating Center)**: DUA/APPLICATION, free
- More than 56,000 participants from US ADRCs and more than 217,000 visits (about 3.7 per participant). Data includes clinical assessments (CDR, GDS, NPI-Q, FAS), neuropsych battery, diagnoses, neuropathology for 8,400+, structural MRI for 12,000+ (computed MRI measures for 2,800), amyloid PET for 455, CSF biomarkers for 2,200+, and APOE for 40,900+. GWAS (26,600+) are reached through ADGC/NIAGADS, and biosamples (27,000+) through NCRAD. — [NACC data request process](https://naccdata.org/requesting-data/data-request-process)
- Process: review the Researcher's Guide, check publications for overlap, submit an online request (acknowledged within 3 business days), and accept the DUA. The DUA limits use to the individuals named in the request and requires NACC acknowledgment. NACC says the data is "Available free to researchers worldwide." — [NACC data request process](https://naccdata.org/requesting-data/data-request-process)

**A4 / LEARN (Anti-Amyloid Treatment in Asymptomatic AD; Longitudinal Evaluation of Amyloid Risk and Neurodegeneration)**: DUA/APPLICATION
- Hosted on the LONI IDA (project "A4"). The DUA grants a "one-time, non-exclusive, non-transferable license" to anonymized participant-level data, limited to the stated purpose. Users may not re-identify or contact participants and must follow IRB rules. — [A4 Data Use Agreement](https://ida.loni.usc.edu/collaboration/access/appApply.jsp?project=A4)
- Pre-randomization data was released in December 2018. By May 2024 there had been about 1,500 requests and 49 publications. Data is also distributed through A4StudyData.org and the ACTC Global Research & Imaging Platform (GRIP). — [JPAD paper (PMC11266269)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11266269/); [ATRI news](https://atrinews.usc.edu/a4-learn-studies-sharing-data-to-maximize-utility-of-ad-trial-data)
- There is an R-package ecosystem ("alzverse") for A4/LEARN/ADNI clinical data. The packages need the user to have approved data access; they don't contain the data. — [alzverse arXiv 2510.02318](https://arxiv.org/pdf/2510.02318)

**UK Biobank**: DUA/APPLICATION with fees and enclave-only access
- Fees for the first 3 years: Tier 1 (questionnaire, physical measures, health outcomes, linked health records) £3,000; Tier 2 (adds assays and genotypes) £6,000; Tier 3 (adds imaging and sequence data) £9,000. Extension years cost £1,000, £2,000, or £3,000. Lower-income-country and student researchers pay £500. Access is only through the Research Analysis Platform (RAP). — [UK Biobank fees](https://www.ukbiobank.ac.uk/use-our-data/fees/)
- New projects get £1,000 in platform credits (the programme ran until Summer 2026). Separately, compute, storage, and egress are charged on RAP. — [UKB financial support](https://www.ukbiobank.ac.uk/use-our-data/fees/financial-support/); [UKB RAP](https://www.ukbiobank.ac.uk/enable-your-research/research-analysis-platform)
- Conflict: an older cached fee page said imaging came at no extra cost over Tier 2. The current page puts imaging in Tier 3. — [cached UKB page](https://www2.ukbiobank.ac.uk/?p=88) vs [current fees](https://www.ukbiobank.ac.uk/use-our-data/fees/)

**AD Knowledge Portal / AMP-AD (Sage Bionetworks, Synapse): ROSMAP, Mayo RNAseq, MSBB, and others**: mixed OPEN and CONTROLLED, with individual-level human data CONTROLLED
- There are two tiers. Open data is available to any registered Synapse user. Controlled Use data needs a registered and certified Synapse user, a signed Data Use Certificate (DUC), and an Intended Data Use Statement of up to 500 words. The DUC text cannot be changed and is renewed each year. Anyone can browse the portal, but downloading needs a Synapse account. — [AD Portal: Navigating the Portal](https://help.adknowledgeportal.org/apd/navigating-the-portal); [AD Portal: Data Use Certificates](https://help.adknowledgeportal.org/apd/Data-Use-Certificates.2623373330.html)
- Redistribution: "Individual-level data in any form (raw, processed, derived) must not be redistributed outside the AD Knowledge Portal." — [AD Portal DUC page](https://help.adknowledgeportal.org/apd/Data-Use-Certificates.2623373330.html) (via search summary)
- Individual-level human data is controlled access. — [AD Portal glossary](https://help.adknowledgeportal.org/apd/glossary) (via search summary)
- ROSMAP is listed on AWS Open Data as **controlled access**. It covers genomic variants, gene expression, epigenetics, proteomics, metabolomics, imaging, and metadata from the Religious Orders Study and the Rush Memory and Aging Project. — [AWS Registry: ROSMAP](https://registry.opendata.aws/rosmap/)
- The MIT ROSMAP single-nucleus multiomics study is also controlled access. MIT says its data and human metadata must be accessed through Synapse with a DUC. — [AWS Registry: MIT ROSMAP Multiomics](https://registry.opendata.aws/mit-rosmap/); [MIT compbio aging-brain atlas](https://compbio.mit.edu/ad_aging_brain/)
- MIT also hosts directory listings of multiregion AD snRNA/snATAC h5ad files. — [compbio.mit.edu AD_Multiomic_MultiRegion snRNA](https://compbio.mit.edu/AD_Multiomic_MultiRegion/02_snRNA_h5ad). The terms on these listings were not confirmed. Treat them as subject to the ROSMAP DUC.

**SEA-AD (Seattle Alzheimer's Disease Brain Cell Atlas, Allen Institute)**: processed data REGISTERED/OPEN-WITH-TERMS, raw data CONTROLLED
- Free downloads: processed snRNA-seq and snATAC-seq with cell-type assignments, covering 11 brain regions (AWS Open Data). MERFISH and Xenium spatial transcriptomics (`sea-ad-spatial-transcriptomics` S3 bucket). Raw and HALO-annotated neuropathology images (`sea-ad-quantitative-neuropathology`). A quantitative neuropathology summary (.xlsx). Donor metadata (.xlsx, 44 KB). MRI volumetrics (.xlsx). Continuous Pseudoprogression Scores (.xlsx). A cell ID conversion table for the ABC Atlas (233 MB). A microglia h5ad (3 GB; 240,651 nuclei × 36,601 genes). — [SEA-AD download page](https://brain-map.org/explore/seattle-alzheimers-disease/seattle-alzheimers-disease-brain-cell-atlas-download)
- Terms: use is governed by the Allen Institute Terms of Use and the terms of external partners, not a Creative Commons license. Users must cite both the primary publication and the specific dataset. — [SEA-AD download page](https://brain-map.org/explore/seattle-alzheimers-disease/seattle-alzheimers-disease-brain-cell-atlas-download); [AWS Registry: SEA-AD](https://registry.opendata.aws/allen-sea-ad-atlas/) (its license field links to alleninstitute.org/legal/terms-use/)
- Controlled parts: raw 10x snRNA-seq, snATAC-seq, and Multiome data (AD Knowledge Portal syn26223298). IAC uniformly reprocessed data (syn64410371; listed as controlled on AWS). WGS and SNP arrays (NIAGADS). Ante-mortem scans (contact ACT / UW ADRC). — [SEA-AD download page](https://brain-map.org/explore/seattle-alzheimers-disease/seattle-alzheimers-disease-brain-cell-atlas-download); [AWS Registry: SEA-AD IAC](https://registry.opendata.aws/sea-ad-iac/)
- The page also has the "under review for potential modification in compliance with Administration directives" banner. Several files were updated in June 2026, with archived versions linked. — [SEA-AD download page](https://brain-map.org/explore/seattle-alzheimers-disease/seattle-alzheimers-disease-brain-cell-atlas-download)
- SEA-AD transcriptomic and epigenomic data were also released through the AD Knowledge Portal. — [AD Portal news](https://news.adknowledgeportal.org/sea-ad/)

**NIAGADS / ADSP (Alzheimer's Disease Sequencing Project)**: CONTROLLED
- ADSP sequence data is available by application to dbGaP or through the NIAGADS Data Storage Site (DSS). NIAGADS is the ADSP Data Coordinating Center. Older NIAGADS material says applications are reviewed by NIH and need a secondary-data return plan, a signed NIA Data Sharing Plan, and a NIAGADS Data Distribution Agreement. These are older (2014–2015) slides and may be out of date. — [NIAGADS 2015 slides](https://files.alz.washington.edu/presentations/2015/fall/Wang.pdf); [NIH NOT-AG-16-033 ADSP publication policy](https://grants.nih.gov/grants/guide/notice-files/NOT-AG-16-033.html)
- ADSP Build 38 data is shared through NIAGADS DSS and has its own application instructions. — [data.gov NIAGADS record](https://catalog.data.gov/dataset/the-national-institute-on-aging-genetics-of-alzheimers-disease-data-storage-site-niagads)

**AD Data Initiative / AD Workbench / AD Discovery Portal (alzheimersdata.org)**: DUA/APPLICATION, data used inside workspaces
- GNPC (Global Neurodegeneration Proteomics Consortium) Harmonized Dataset v1 has about 250 million protein measurements from about 35,000 plasma, serum, and CSF samples, contributed by 23 cohorts. Other sources say more than 40,000 biosamples or more than 300 million measurements. It was opened to the wider research community on about 15 July 2025, through AD Workbench workspaces with individual permissions. About 600 users applied in the first 9 months. — [Alzheimer Europe news](https://www.alzheimer-europe.org/news/global-neurodegeneration-proteomics-consortium-releases-its-v1-dataset-including-250-million); [AD Data Initiative GNPC case study](https://www.alzheimersdata.org/case-studies/ad-workbench-powers-the-world-s-largest-protein-biomarker-discovery-effort-the-global-neurodegeneration-proteomics-consortium-gnpc); [GNPC v1 HDS page](https://www.alzheimersdata.org/gnpc-v1-harmonized-dataset); [GNPC paper (PMC11712936)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11712936/)
- A multiplatform GNPC expansion is planned: consortium-member release in Summer 2026 and public release in Summer 2027. — [GNPC case study](https://www.alzheimersdata.org/case-studies/ad-workbench-powers-the-world-s-largest-protein-biomarker-discovery-effort-the-global-neurodegeneration-proteomics-consortium-gnpc)
- At least one GNPC cohort page describes access as free of charge to qualified researchers. — [KU ADRC GNPC dataset](https://www.alzheimersdata.org/university-of-kansas-adrc-gnpc-longitudinal-data)
- SEA-AD also has a listing on the AD Discovery Portal. — [alzheimersdata.org SEA-AD](https://www.alzheimersdata.org/sea-ad)

**EPAD (European Prevention of Alzheimer's Dementia)**: DUA/APPLICATION through AD Workbench
- Users create an AD Data Initiative Portal account and request a Workspace. Imaging requests must specify sequences and formats. EPAD genomic data is also on AD Workbench. — [EPAD open-source data page](https://ep-ad.org/index.php/open-source-data/); [IMI Neuronet](https://www.imi-neuronet.org/explore-the-ad-workbench-to-access-the-european-prevention-of-alzheimers-dementia-study-data/); [Edinburgh news: EPAD genomic data on AD Workbench](https://clinical-brain-sciences.ed.ac.uk/edinburgh-dementia-prevention/news/epad-genomic-data-now-available-alzheimers-disease-workbench)

**Dementias Platform UK (DPUK) Data Portal**: DUA/APPLICATION, enclave access
- At the time of the paper: 3,370,929 individuals in 42 cohorts, with access through a "secure, fully auditable, remote access environment." Projects are by default collaborations with the cohort teams. Data is usually free at point of use, though a few cohorts charge access fees. Multi-cohort requests are routed to each data controller. — [DPUK Data Portal paper (PMC7320955)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7320955/)

**Alzheimer's Prevention Initiative (API)**: an application-based request page exists. — [API Request Data](https://alzheimerspreventioninitiative.com/request-data/)

### Inferences
- For a public repo, the safe pattern for every cohort above is to publish code, loaders, schemas, and documentation. Users bring their own approved credentials and data. No participant-level rows, and for ADNI no derived per-subject tables, can live in the repo. The ADNI DUA's "derived datasets should only be shared through ADNI-LONI" clause probably covers model outputs indexed by subject (for example, per-subject predictions or embeddings).
- ADNI's AI-tool clause means sending ADNI rows to a cloud LLM API that could expose them is a stated DUA violation. Contributors should be warned in CONTRIBUTING docs.
- OASIS's non-commercial clause conflicts with permissive OSS licenses only if data is bundled. Code under MIT or Apache is fine. Bundling any OASIS-derived face-reconstructable image would violate the terms.
- Aggregate statistics such as group means or published effect sizes are generally treated as publishable results, since the DUAs target individual-level data. Even so, the ADNI DPC pre-submission review applies to manuscripts, not to code repos. Check with the DPC before posting aggregate tables.
- The "under review ... Administration directives" banners on ADNI/IDA and on SEA-AD (both partly federally funded) are an availability risk for 2026–2027. A project should not hard-depend on URLs staying stable and should pin dataset versions and DOIs.

### Gaps
- **DIAN** (Dominantly Inherited Alzheimer Network): no current data-request page was found in this session. From background knowledge, not verified this session: DIAN data is requested through a WashU/DIAN data-request form with DIAN steering-committee review, and there is no public download.
- **GAAIN**: no source retrieved on current status. GAAIN was a federated discovery network funded by the Alzheimer's Association. Whether it is still active or has been folded into the AD Discovery Portal is unverified.
- **AD Atlas** (adatlas.org, a network-based multi-omics resource): not researched. Access terms are unknown.
- **Mayo RNAseq and MSBB specifically**: the access tier was inferred from the portal-wide rule (individual-level human data is controlled). Study-specific pages were not fetched.
- **NIAGADS current (2026) application workflow**: only 2014–2016 material was found. The current DSS and dbGaP steps, and whether NIAGADS summary statistics (GWAS sumstats) are open, were not confirmed. NIAGADS GWAS summary statistics are widely believed to be openly downloadable, but this was not verified this session.
- **UK Biobank redistribution and "return of results" rules** and which tier covers dementia outcome fields were not confirmed.
- **A4 post-randomization / full trial data**: whether the full A4 data (beyond pre-randomization) has been released was not confirmed.
- **ADNI cohort size** (total participants across ADNI1/GO/2/3/4) is not stated on the fetched page.
- **AD Workbench DUA text**, including redistribution clauses, was not retrieved.
- **PPMI-like AD efforts**: none were specifically researched. PPMI itself is Parkinson's, application-based through LONI.

---

## 2. Freely downloadable resources and redistribution limits for a public repo

### Takeaway
Few AD resources are truly no-application downloads: SEA-AD processed data (Allen Terms of Use, citation required), OpenNeuro datasets (CC0 by platform rule), and openly browsable knowledge portals such as Agora. Of these, only CC0 OpenNeuro data is clearly redistributable inside a public repo without license friction. Even then, the usual practice is to link and fetch rather than vendor the data.

### Cited Findings
- **OpenNeuro**: all uploads must be BIDS-formatted and released under CC0 (public domain). The platform supports MRI, PET, MEG, EEG, and iEEG. — [BRAIN Initiative: OpenNeuro](https://www.braininitiative.org/toolmakers/resources/openneuro/)
- One 2026 MRI-linkage paper used OpenNeuro accessions ds000206, ds004937, ds005664, and ds005360 alongside ADNI. Their AD relevance and contents were not confirmed. — [arXiv 2602.10043](https://arxiv.org/pdf/2602.10043)
- **SEA-AD**: processed single-cell, spatial, neuropathology, and donor-metadata files are free to download with no application. Use is governed by the Allen Institute Terms of Use plus citation of the publication and the dataset. Data is hosted on public AWS S3 buckets. — [SEA-AD download page](https://brain-map.org/explore/seattle-alzheimers-disease/seattle-alzheimers-disease-brain-cell-atlas-download); [AWS Registry SEA-AD](https://registry.opendata.aws/allen-sea-ad-atlas/)
- **AD Knowledge Portal "Open" tier**: available to any registered Synapse user without limitations, with no DUC. Individual-level human data is not in this tier. — [AD Portal navigation help](https://help.adknowledgeportal.org/apd/navigating-the-portal)
- **Agora** (Sage Bionetworks): an openly available web app with target-based evidence for more than 950 nominated targets from AMP-AD and TREAT-AD. Users can access the data underlying the visualizations. — [Agora paper (PMC11709802)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11709802/); [Agora 2025 paper (PMC12726812)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12726812/). The code is on GitHub. — [Sage-Bionetworks/magora](https://github.com/Sage-Bionetworks/magora)
- **Redistribution prohibitions (verbatim or near-verbatim)**:
  - ADNI: "redistribution of individual participant-level data in any manner is prohibited". Derived datasets go only through ADNI-LONI or an NIA-designated repository. — [ADNI DUA](https://ida.loni.usc.edu/collaboration/access/appApply.jsp?project=ADNI)
  - AD Knowledge Portal controlled data: no redistribution of individual-level data "in any form (raw, processed, derived)" outside the portal. — [AD Portal DUC](https://help.adknowledgeportal.org/apd/Data-Use-Certificates.2623373330.html)
  - OASIS: non-commercial only; no sharing of OASIS-3/4 data or face-reconstructable derivatives beyond the agreement. — [OASIS](https://sites.wustl.edu/oasisbrains/)
  - A4/LEARN: license is "non-transferable" and purpose-limited. — [A4 DUA](https://ida.loni.usc.edu/collaboration/access/appApply.jsp?project=A4)
  - NACC: use is limited to the individuals named in the request. — [NACC](https://naccdata.org/requesting-data/data-request-process)

### Inferences
- **Green-light for public demos (link and fetch, attribute)**: OpenNeuro CC0 datasets; SEA-AD processed h5ad/xlsx (fetch from S3 at runtime, cite, don't re-host large files without reading the Allen ToU); Agora/AD Portal open-tier summary data.
- **Never in repo**: ADNI, OASIS, AIBL, NACC, A4/LEARN, UKB, ROSMAP/Mayo/MSBB individual-level data, ADSP/NIAGADS genotypes, GNPC/EPAD (workspace-bound), DPUK (enclave-bound).
- The Allen Institute Terms of Use have historically had a non-commercial or attribution flavor and are not an OSI or CC license. A project should not relabel SEA-AD files under its own license. Keep data and code licenses separate and document upstream terms in a DATA_LICENSES file.

### Gaps
- The full text of the Allen Institute Terms of Use (commercial use and redistribution clauses) was not fetched this session.
- No specific AD-focused OpenNeuro dataset (AD patients with MRI/PET under CC0) was confirmed by accession number. A search for one returned nothing.
- Agora's data download license was not found. Whether Agora's displayed data falls under the Synapse open tier or under specific terms is unconfirmed.

---

## 3. Open single-cell and spatial atlases of AD brain

### Takeaway
SEA-AD is the flagship openly downloadable AD single-cell and spatial atlas: processed snRNA/snATAC across 11 regions, MERFISH and Xenium, and quantitative neuropathology. Most other major AD single-nucleus atlases (MIT ROSMAP multiregion and multiomics, SEA-AD raw, IAC reprocessed) are controlled access through Synapse DUCs.

### Cited Findings
- SEA-AD open components: processed 10x snRNA-seq and snATAC-seq with cell-type labels for 11 brain regions; MERFISH and Xenium spatial; neuropathology images and quantification; donor metadata; MRI volumetrics; pseudoprogression scores; a microglia h5ad with 240,651 nuclei. — [SEA-AD download page](https://brain-map.org/explore/seattle-alzheimers-disease/seattle-alzheimers-disease-brain-cell-atlas-download)
- SEA-AD raw data and the IAC harmonized multi-study snRNA/multiome data are controlled access (Synapse syn26223298, syn64410371). — [SEA-AD download page](https://brain-map.org/explore/seattle-alzheimers-disease/seattle-alzheimers-disease-brain-cell-atlas-download); [AWS SEA-AD IAC](https://registry.opendata.aws/sea-ad-iac/)
- The MIT ROSMAP single-nucleus multiomics and aging-PFC atlas are controlled access and need a Synapse DUC. — [AWS MIT ROSMAP](https://registry.opendata.aws/mit-rosmap/); [MIT compbio aging brain](https://compbio.mit.edu/ad_aging_brain/)
- SEA-AD transcriptomic and epigenomic data are also mirrored in the AD Knowledge Portal. — [AD Portal news](https://news.adknowledgeportal.org/sea-ad/)

### Inferences
- For an open demo pipeline (QC, cell typing, differential abundance against pathology), the SEA-AD MTG processed h5ad plus donor metadata and continuous pseudoprogression scores is the best fully downloadable choice. The microglia h5ad (3 GB) is a manageable smaller subset.

### Gaps
- Other atlases were not researched this session: CZ CELLxGENE Discover AD collections (usually CC BY 4.0, unverified here), the Human Cell Atlas, GEO-deposited AD snRNA datasets (for example Mathys 2019 summary matrices, Grubman 2019, Leng 2021), spatial AD datasets (for example Chen 2020 mouse ST), and the ABC Atlas. Their licenses and AD relevance still need verifying.
- Total SEA-AD donor and nucleus counts were not stated in the page text.

---

## 4. Synthetic or fully open benchmark datasets for public demos

### Takeaway
No ready-made, openly redistributable synthetic ADNI or TADPOLE dataset was confirmed. TADPOLE itself is ADNI-DUA-gated. Published synthetic-data methods exist, so the project would probably need to generate its own synthetic data, from open-source generators or from published aggregate statistics, and should not train generators on DUA data without checking the ADNI derived-data clause.

### Cited Findings
- TADPOLE challenge data is downloadable only through the ADNI IDA, so the ADNI DUA applies. — [ADNI TADPOLE](https://adni.loni.usc.edu/tadpole-challenge-dataset-available/); [TADPOLE MELBA paper](https://www.melba-journal.org/papers/2021:019.html)
- A medRxiv preprint provides an open-source R method to generate synthetic data for a hypothetical AD trial. It recreates a real observational dataset synthetically and applies a treatment effect, intended as a benchmark. — [medRxiv 2024.02.05.24302140](https://www.medrxiv.org/content/10.1101/2024.02.05.24302140.full.pdf)
- Synthetic AD-progression data has been used in ML studies. Whether the data was released is unconfirmed. — [PMC11784714](https://pmc.ncbi.nlm.nih.gov/articles/PMC11784714/)
- LDM100K is a synthetic neuroimaging dataset (latent-diffusion brain MRIs) generated from a model trained on UK Biobank-derived data. It is a precedent for shareable synthetic brain MRI. — [arXiv 2602.10043](https://arxiv.org/pdf/2602.10043)
- A 2025 tabular foundation-model paper on longitudinal AD progression uses TADPOLE/ADNI-type data. It shows the benchmark is still in use, but it is not open. — [arXiv 2508.17649](https://arxiv.org/html/2508.17649)

### Inferences
- For a public repo, the most defensible demo data, in order:
  1. Fully synthetic tabular cohorts generated from published summary statistics (no DUA data touched).
  2. CC0 OpenNeuro MRI.
  3. SEA-AD processed files fetched at runtime.
  4. Synthetic brain MRIs from publicly released generators such as the LDM100K-style UKB-trained model, after checking that model's license.
- Training a generator on ADNI and releasing its synthetic outputs would arguably be "derived datasets" under the ADNI DUA and need ADNI's approval.

### Gaps
- Whether the medRxiv synthetic AD-trial dataset or its generator is posted with a permissive license was not confirmed.
- The license and terms of LDM100K and its generator were not verified.
- No widely used Kaggle-style "Alzheimer MRI" datasets were assessed. Many are re-uploads of OASIS or ADNI slices with unclear provenance and likely violate upstream DUAs, but this was not verified this session.

---

## 5. Data-quality issues, controversies, bias/harmonization problems, leakage risks, and what independent vetting each resource needs

(Added at the coordinator's request: be skeptical, and treat everything brought into the project as needing independent vetting.)

### Takeaway
The cohort datasets above are not implicated in the big AD misconduct cases. Lesné's Aβ*56 and Masliah's images concern published lab figures, not ADNI, OASIS, NACC, or the other cohort data. But the literature built on these datasets is heavily inflated by data leakage and by non-representative samples. Over half of 32 surveyed CNN-on-MRI AD papers may have leaked data. Slice-level splits inflate accuracy by roughly 30–55 percentage points. ADNI is about 89% White. Snapshot AD snRNA-seq findings shrank by a factor of 549 under donor-level reanalysis. Proteomic platforms often disagree (median cross-platform r about 0.3). Any claim, model, or derived file brought into the project should be re-derived from the primary data with subject-level splits and documented provenance.

### Cited Findings

**Research-integrity controversies (literature level, relevant to priors, target lists and knowledge graphs)**
- **Lesné / Aβ*56:** the 2006 Nature paper claiming Aβ*56 causes memory impairment was retracted in 2024. The notice cited "signs of excessive manipulation, including splicing, duplication and the use of an eraser tool." All authors except Lesné agreed. A 2022 Science investigation first raised the concerns, and the inquiry grew to at least 20 other Lesné papers. Researchers have since questioned whether Aβ*56 can be reliably detected, or even exists. Senior author Karen Ashe maintains the conclusions are robust. — [Wikipedia: Sylvain Lesné](https://en.wikipedia.org/wiki/Sylvain_Lesn%C3%A9) (secondary source; the original reporting is Science 2022 and the Nature retraction notice 2024); [Minnesota Reformer on Lesné leaving UMN](https://minnesotareformer.com/briefs/alzheimers-researcher-alleged-to-have-doctored-images-is-leaving-umn/)
  - Sources conflict on whether it is the most-cited or second most-cited retracted paper (per Retraction Watch). — [Modern Discontent Substack](https://moderndiscontent.substack.com/p/the-most-seminal-paper-in-alzheimers) vs [Wikipedia](https://en.wikipedia.org/wiki/Sylvain_Lesn%C3%A9). Both are low-tier sources.
- **Masliah:** in September 2024 NIH reported that it had found research misconduct by Eliezer Masliah, former director of NIA's Division of Neuroscience. The finding covered two publications where figure panels showing different experimental results were reused or relabeled. A Science-reported 300-page dossier flagged suspect images in 132 papers from 1997 to 2023. — [Coast Reporter (AP wire): NIH finds misconduct](https://www.coastreporter.net/health/a-top-government-scientist-engaged-in-research-misconduct-nih-finds-9575595)
  - A count of 18 retractions as of December 2025 appears only on Wikipedia and is unverified. — [Wikipedia: Eliezer Masliah](https://en.wikipedia.org/wiki/Eliezer_Masliah)

**Data leakage and inflated performance (imaging ML)**
- Wen et al. 2020 (Medical Image Analysis) did a systematic review and found that "more than half of the surveyed papers may have suffered from data leakage" (half of 32 studies in the preprint wording). In their experiment, leakage inflated validation balanced accuracy to 1.00, against 0.75 on the ADNI test set and 0.80 on the AIBL test set. 3D CNNs did not beat a voxel-based SVM, and models generalized poorly to cohorts with different inclusion criteria or demographics. They released Clinica/ClinicaDL, an open framework that converts ADNI, AIBL, and OASIS to BIDS. — [Wen et al., arXiv 1904.07773](https://arxiv.org/pdf/1904.07773); [ADNI-hosted PDF](https://adni.loni.usc.edu/adni-publications/Wen-2020-Convolutional%20neural%20networks%20for%20cla.pdf)
- Yagis et al. 2021 (Scientific Reports): slice-level cross-validation inflated slice-level test accuracy by 30% (OASIS), 29% (ADNI), 48% (PPMI), and 55% (a local PD dataset). On *randomly labeled* OASIS data, slice-level splitting gave about 96% accuracy against the 50% chance level with subject-level splits. — [Effect of data leakage in brain MRI classification (PMC8604922)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8604922/)
- Kaggle-hosted 2D-slice OASIS-1 datasets are used in the wild. One self-reported repo shows 99.9% accuracy with image-level splits against 80.8% with subject-level splits. This is not peer-reviewed. — (search summary of an AttentionMS-Net repo; [contra.com project page](https://contra.com/p/YEvcqWbb-attention-ms-net-alzheimers-disease-classification-from-mri))
- **Longitudinal leakage:** a 2026 preprint on ADNI MCI-conversion prediction lists leakage sources including post-conversion visit contamination. A naive pipeline scored AUC 0.934 against a corrected 0.859. — [arXiv 2607.17442](https://arxiv.org/pdf/2607.17442) (preprint)
- **Label circularity:** ADNI-style MCI and AD labels are defined from CDR and MMSE thresholds, for example MCI as MMSE 24–30 with CDR 0.5. Those same instruments are often used as predictors. CDR/MMSE targets have been called "noisy and unreliable," and most AD subjects stay at CDR 0.5 across visits. — [arXiv 1104.5458](https://arxiv.org/pdf/1104.5458); [PMC8761739](https://pmc.ncbi.nlm.nih.gov/articles/PMC8761739)

**Sampling bias and generalizability**
- The ADNI sample is about 89% White, 5% Black, 8% Hispanic/Latino, and 3% Asian, and only 15% have 12 or fewer years of education. ADNI4 aims to diversify. — [ADNI4 / JPAD 2022 (link.springer.com/10.14283/jpad.2022.50)](https://link.springer.com/article/10.14283/jpad.2022.50); [PMC9402812](https://pmc.ncbi.nlm.nih.gov/articles/PMC9402812)
- ADNI recruitment from 2004 to 2020: 15% from underrepresented ethnocultural groups and 15% with under 12 years of education. The authors conclude "ADNI results may not be entirely generalizable to ethnoculturally diverse and low education populations." — [PMC10042173](https://pmc.ncbi.nlm.nih.gov/articles/PMC10042173)
- An ARIC-linked analysis says some ADNI-estimated associations "may not be generalizable to the larger US population." — [ARIC MP3493](https://aric.cscc.unc.edu/aric9/system/files/aricprops/priv/MP3493.pdf)
- About 90% of ADNI-4 participants have at least a high-school degree and half hold an advanced degree. About half of US adults 65 and older completed 12 years of school. — [Being Patient](https://beingpatient.com/alzheimers-adni-dei/) (journalism)

**Multi-site / scanner harmonization**
- Scanner and site effects are a known confound in ADNI MRI. Longitudinal ComBat applied to cortical thickness for 663 ADNI participants improved power and type-I-error control in simulations. — [PMC8232807 / longitudinal ComBat](https://pmc.ncbi.nlm.nih.gov/articles/PMC8232807)
- Volumes differ between 1.5T and 3T. 3T contrast can inflate gray-matter estimates. Field strength is often confounded with ADNI phase (ADNI1 was mostly 1.5T), so harmonization risks removing biological signal. — [PMC7605103](https://pmc.ncbi.nlm.nih.gov/articles/PMC7605103); [PMC10353821](https://pmc.ncbi.nlm.nih.gov/articles/PMC10353821/); [Tensor-ComBat, arXiv 2604.01546](https://arxiv.org/pdf/2604.01546)

**Single-nucleus atlases: analysis-driven false positives**
- Reanalysis of the first AD snRNA-seq dataset (Mathys et al. 2019: about 80,000 PFC nuclei from 48 donors) with donor-level pseudobulk found 549 times fewer DEGs at FDR 0.05 than the original. Reviewers cautioned that QC and annotation also changed, so not every lost gene is necessarily a false positive. — [Murphy, Fancy & Skene, eLife 2023 (90214)](https://elifesciences.org/articles/90214); [eLife peer reviews](https://elifesciences.org/articles/90214/peer-reviews)

**Proteomics cross-platform discordance (relevant to GNPC and multi-cohort proteomics)**
- SomaScan 7k against Olink Explore 3072 across 2,157 overlapping proteins: correlations are bimodal, with median r = 0.30. — [medRxiv 2024.07.11.24310161](https://medrxiv.org/content/10.1101/2024.07.11.24310161.full.pdf) (preprint)
- SomaScan v4 against Olink (871 proteins): 36.3% of protein–phenotype associations appeared on only one platform. The genetically predicted effect direction was discordant for PILRA in AD. — [Katz/Pietzner et al., Nat Commun 2021 (s41467-021-27164-0)](https://link.springer.com/10.1038/s41467-021-27164-0)
- In CSF (Ace Alzheimer Center Barcelona), more than 600 proteins were well reproduced across SomaScan 7k and Olink Explore 3k, and significant associations mainly involved the reproducible proteins. — (search summary; Broad-listed publication [broad1373346](https://www.broadinstitute.org/publications/broad1373346), not fetched)

### Inferences
- **Misconduct scope:** none of the sources link Lesné or Masliah to the cohort datasets cataloged here. The risk is to literature-derived assets: curated pathway or target lists, knowledge graphs, text-mined relations, and "known biology" priors. Any such resource the project imports should be checked for dependence on retracted or flagged papers, for example against the Retraction Watch database and PubPeer.
- **Masliah's role as former NIA neuroscience director** creates no evidence of tampering with NIA-funded datasets. No source suggests that, and the notes should not imply it.
- **Per-resource vetting checklist** (what the project would need before trusting a resource or a third-party derivative of it):

| Resource | Known quality/bias/leakage issues | Minimum vetting before use |
|---|---|---|
| ADNI | Mostly White and highly educated; 1.5T vs 3T and multi-vendor scanner effects; diagnosis is circular with MMSE/CDR; repeated visits per subject; many published models leak | Subject-level (RID) splits and no visit leakage; exclude label-defining instruments from features, or report with and without them; harmonize while preserving biological covariates; check against the ADNIMERGE version and date; external test on AIBL/OASIS/NACC |
| TADPOLE | ADNI-derived; same issues; fixed historical snapshot | Same as ADNI; pin the TADPOLE release; don't mix with fresh ADNI pulls without de-duplicating RIDs |
| OASIS-1/2/3/4 | Single site (WashU Knight ADRC); overlap between OASIS-3 and KARI; Kaggle slice re-uploads with unknown provenance that probably breach the DUA | Use NITRC-IR originals only; subject-level splits; never use Kaggle mirrors; check overlap across OASIS releases and KARI |
| AIBL | Australian cohort; partly ADNI-harmonized protocol; restricted to non-commercial use | Confirm protocol and scanner differences against ADNI before pooling; subject-level splits |
| NACC | Clinic-referral (ADRC) sample, not population-based; UDS version changes over time (v1–v4); clinician diagnoses vary by center | Stratify or adjust by ADRC and UDS version; check against neuropath-confirmed subsets |
| A4/LEARN | Trial population with amyloid-PET-screened preclinical participants; mostly White and educated (not verified this session) | Know which release you have (pre-randomization vs later); don't generalize to clinic populations |
| UK Biobank | Healthy-volunteer bias (well documented; not sourced this session); dementia defined from linked records (misclassification) | Validate case definitions; consider weighting; follow UKB's return-of-results rules |
| AD Knowledge Portal (ROSMAP/Mayo/MSBB) | Post-mortem RNA quality (RIN), batch effects, sample swaps or mislabeling reported in some omics releases (not verified this session) | Check the portal release notes and data-version IDs; run sex-check and genotype-concordance QC; analyze at donor level |
| SEA-AD | Files changed in June 2026 with archived versions; federal-review banner; donor counts not stated in text | Pin file versions and checksums; donor-level pseudobulk for DE; check against the IAC harmonized release |
| MIT ROSMAP snRNA/multiomics | The original Mathys 2019 DE results were heavily inflated under donor-level reanalysis | Re-derive with pseudobulk and donor-level statistics; don't import published DEG lists as ground truth |
| GNPC (AD Workbench) | Multi-cohort, multi-fluid (plasma, serum, CSF), possibly multi-platform; SomaScan/Olink discordance; cohort-specific pre-analytics | Model the cohort and batch; restrict to platform-concordant proteins when pooling; don't treat cross-platform measurements as interchangeable |
| ADSP/NIAGADS genomics | Ancestry imbalance; sequencing-center and batch artifacts typical of large WGS/WES (not verified this session) | Ancestry-stratified QC; use official QC-passed call sets and versions |
| OpenNeuro AD-adjacent datasets | Heterogeneous provenance; CC0 does not guarantee quality or correct labels | Run BIDS validation; check against the source publication; visual QC; check for subject overlap with other datasets |
| Synthetic data (medRxiv R generator, LDM100K-style) | Fidelity and privacy vary; may memorize training subjects; may encode biases of the source cohort | Membership-inference and nearest-neighbor checks; compare marginals and joint distributions to the source; record the generator license and training data |

- **General rules for the repo:**
  1. Split by subject, never by slice or visit.
  2. Lock the test sets.
  3. Record dataset version, download date, and checksum.
  4. Report external-cohort validation.
  5. Treat any third-party preprocessed AD dataset (Kaggle, Hugging Face, GitHub mirrors) as untrusted until it is traced to the original source and its license.

### Gaps
- No primary-source documentation was retrieved for sample swaps or mislabeling in AMP-AD/ROSMAP omics, UK Biobank healthy-volunteer bias, or ADSP batch artifacts. The table flags these as unverified.
- The GNPC v1 platform composition (SomaScan-only or mixed) was not confirmed. This determines how much cross-platform discordance applies.
- No systematic audit was found of leakage in multimodal or tabular ADNI/TADPOLE ML beyond the 2026 preprint.
- The Lesné and Masliah facts here come from secondary sources (Wikipedia, AP wire via local outlet, Substack). The primary Nature retraction notice, the Science articles, and the NIH/ORI statements were not fetched directly.
- Whether any AD Knowledge Portal, Agora, or AD Atlas resource ingests literature-derived evidence that depends on Lesné- or Masliah-flagged papers was not assessed.
