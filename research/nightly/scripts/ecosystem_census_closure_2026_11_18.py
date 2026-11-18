"""Did the glia expand, or did the neurons just leave? A census-closure toy
(night of 2026-11-18, cross-domain lens, "brain as an ecosystem: cause or marker?" constraint).

Ecologists learned long ago that a census reported as SHARES of a community cannot, by itself,
say which species changed: if one species dies back, every other species' share rises even though
not one individual was added (the "closure" problem of compositional data; Gloor et al., Front
Microbiol 2017, doi 10.3389/fmicb.2017.02224). Single-nucleus atlases of the Alzheimer's brain
report cell types the same way - as shares of the nuclei sequenced. The usual remedy is to pick a
REFERENCE cell type assumed not to change (the approach of scCODA; Buttner et al., Nat Commun
2021, doi 10.1038/s41467-021-27150-6). This toy asks what each style of analysis concludes about
one question - "do microglia increase with disease severity?" - in three synthetic worlds:

    LOSS ONLY      neurons are lost with severity; no glial cell is added
    TRUE GLIOSIS   neurons are lost AND microglia really multiply
    OLIGO LOSS     neurons are lost, oligodendrocytes are also lost, microglia unchanged
                   (the world in which the usual reference cell type is itself changing)

Severity is a continuum per donor (0 to 1), not a two-state label. Each simulated study has 84
donors and about 6,000 nuclei per donor. Analyses:
    A  share of nuclei that are microglia, regressed on severity
    B  log ratio microglia / oligodendrocytes (oligodendrocytes as the reference)
    C  log ratio microglia / astrocytes (astrocytes as the reference)
    D  absolute density (cells per unit tissue, e.g. stereology or spatial counts), with its
       own, larger, measurement error
Scored by how often each "finds microglia increasing" (p < 0.05, positive slope) over 400
simulated studies, and by the apparent change in microglia at maximum severity.

Synthetic cell counts with assumed effect sizes; shows what each analysis can be fooled by, not
what happens in any real brain.
"""

from __future__ import annotations

import numpy as np
from scipy import stats

TYPES = ("exc", "inh", "astro", "oligo", "micro", "opc")
BASE = np.array([40.0, 10.0, 15.0, 25.0, 5.0, 5.0])  # absolute density, arbitrary units
DONORS, NUCLEI, REPS = 84, 6000, 400
BIO_SD, ABS_ERR_SD = 0.15, 0.25  # donor-to-donor spread; error of an absolute count (log scale)

WORLDS = {
    "LOSS ONLY": {"exc": -0.35, "inh": -0.25},
    "TRUE GLIOSIS": {"exc": -0.35, "inh": -0.25, "micro": +0.30},
    "OLIGO LOSS": {"exc": -0.35, "inh": -0.25, "oligo": -0.20},
}


def study(rng, effects):
    sev = rng.random(DONORS)
    dens = BASE * np.exp(rng.normal(0, BIO_SD, (DONORS, len(TYPES))))
    for name, eff in effects.items():
        dens[:, TYPES.index(name)] *= 1 + eff * sev
    share = dens / dens.sum(1, keepdims=True)
    counts = np.array([rng.multinomial(NUCLEI, p) for p in share])
    micro, oligo, astro = (counts[:, TYPES.index(t)] for t in ("micro", "oligo", "astro"))
    measured_abs = dens[:, TYPES.index("micro")] * np.exp(rng.normal(0, ABS_ERR_SD, DONORS))
    readouts = (
        (micro / NUCLEI, False),
        (np.log(micro / oligo), True),
        (np.log(micro / astro), True),
        (np.log(measured_abs), True),
    )
    out = []
    for y, is_log in readouts:
        fit = stats.linregress(sev, y)
        found = fit.pvalue < 0.05 and fit.slope > 0
        change = np.expm1(fit.slope) if is_log else fit.slope / fit.intercept
        out.append((found, change))
    return out


def main() -> None:
    rng = np.random.default_rng(0)
    names = (
        "A share of nuclei",
        "B ratio to oligodendrocytes",
        "C ratio to astrocytes",
        "D absolute density (noisier)",
    )
    print(f"{REPS} simulated studies per world, {DONORS} donors each. For each analysis: share of")
    print("studies that 'find microglia increasing', and the apparent change at top severity.\n")
    print(f"  {'analysis':<30}" + "".join(f"{w:>20}" for w in WORLDS))
    res = {w: np.array([study(rng, eff) for _ in range(REPS)]) for w, eff in WORLDS.items()}
    for i, name in enumerate(names):
        cells = []
        for w in WORLDS:
            cells.append(f"{res[w][:, i, 0].mean():.2f} ({res[w][:, i, 1].mean():+.0%})")
        print(f"  {name:<30}" + "".join(f"{c:>20}" for c in cells))
    print("\n  true change in microglia at maximum severity:   0%, +30%, 0%")
    print("\nReading: an analysis is trustworthy only if it fires in TRUE GLIOSIS and stays quiet")
    print("in the other two worlds. Raw shares report an increase whenever neurons are lost. A")
    print("reference cell type fixes that only while the reference itself is stable, and no")
    print("atlas can know that from shares alone. Absolute counts are right on average in all")
    print("three worlds but, being noisier, miss part of a real change. Synthetic, with assumed")
    print("effect sizes: this is a checklist for reading atlas claims, not a finding about them.")


if __name__ == "__main__":
    main()
