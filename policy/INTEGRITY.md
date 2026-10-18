# Research integrity policy

Alzheimer's research has had high-profile retractions and misconduct findings.
Literature-derived resources (knowledge graphs, target lists, preclinical databases,
model parameters) can silently inherit them. This project screens for that.

## Watchlist

Maintained in [`registry/integrity_watchlist.yaml`](../registry/integrity_watchlist.yaml).
Current entries:

- **Lesné et al. 2006 (Nature), Aβ\*56**: retracted 2024 for image manipulation.
- **Eliezer Masliah**: NIH research-misconduct finding (Sept 2024); 132 papers flagged.
- **Simufilam / Cassava Sciences**: two failed Phase 3 trials; SEC settlement; indicted collaborator.
- **Bredesen ReCODE "reversal"**: uncontrolled case series, no RCT.

The broader amyloid hypothesis does **not** rest on the retracted Aβ\*56 paper; it has
independent genetic and antibody-trial support. The rule targets specific dependencies,
not whole fields.

## Rules

1. Anything traced to a watchlist entry is excluded unless independently replicated by
   unaffiliated groups.
2. Model parameters must cite their source. Parameters derived from watchlisted work are
   re-derived or removed.
3. Before a literature-derived resource (AlzKB, PrimeKG, AlzPED, Agora, pipeline censuses)
   is used, filter its sources against retraction databases (Retraction Watch / Crossref)
   and the watchlist, and record the check date in the registry.
4. Every claim in `evidence/claims.yaml` carries a design grade, sources and a check date.
5. Prefer primary notices (journal retraction notice, ORI/NIH finding, SEC/DOJ filing)
   over news coverage when adding to the watchlist; several current facts came from
   secondary sources and should be upgraded.
6. Patterns that warrant extra scrutiny: single-lab foundations, image-based evidence
   without raw data, press releases ahead of peer review, subgroup results promoted
   after a missed primary endpoint, and undisclosed commercial interests.

## Adding to the watchlist

Open a PR with the primary source, what is affected, and the exclusion rule. Be factual
and cite official findings; do not speculate about individuals beyond what official
findings state.
