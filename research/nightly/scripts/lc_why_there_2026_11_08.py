"""Why does the locus coeruleus seed tau first - and which part is druggable? (night of 2026-11-08,
repurposing lens, "start from the earliest region and ask why there" constraint). A structural
ordering toy motivated by the LC's selective vulnerability (Braak & Del Tredici 2011,
doi 10.1097/NEN.0b013e318232a379) and the MAO-A -> DOPEGAL -> AEP/legumain -> tau-N368 cleavage
pathway specific to noradrenergic neurons (Kang/Ye, J Clin Invest 2020, doi 10.1172/JCI130513;
mouse/cell).

Each region crosses a tau-seeding threshold when accumulated stress passes theta; with a roughly
constant net stress rate r, the onset time is t = theta / r. We build r from:

    r = (structural load) / clearance   +   (MAO-A / DOPEGAL aldehyde term, noradrenergic only)

The structural load (long unmyelinated arbor x high tonic firing = metabolic/Ca load) is NOT
druggable - you cannot shrink the LC's arbor. The aldehyde term IS druggable (MAO-A inhibition).
The toy separates the two and asks what a repurposing lever can and cannot do.

Three honest results (see the reading): (1) the LC seeds first; (2) its STRUCTURAL load alone
already ranks it first, so you cannot stop the LC being the origin; but (3) the MAO-A/DOPEGAL term
is the one druggable accelerant, and lowering it (a MAO-A inhibitor - the isoform the field has NOT
trialed; rasagiline is MAO-B) delays the earliest seed. A clearly-labelled what-if then shows the
earliest-seed timing is sensitive to that accelerant, the only honest basis for a sex-/state-aware
TIMING clock - NOT a claim the accelerant is in fact sex-linked (human MAO-A dosage-compensation and
estrogen data are null/mixed/contradictory; the robust human sex effect is on the amyloid->tau
coupling step, not amyloid load: Coughlan 2025, PMID 40029638).

Dimensionless illustration; assumed factor values; not calibrated to any region or patient, and not
a drug claim.
"""

from __future__ import annotations

THETA = 1.0
MAOA_GAIN = 0.6  # DOPEGAL/aldehyde contribution to the rate, noradrenergic regions only

# region: structural load (arbor x firing), clearance, noradrenergic?
REGIONS = {
    "locus coeruleus": dict(load=1.00, clear=1.0, noradrenergic=True),
    "entorhinal": dict(load=0.70, clear=1.0, noradrenergic=False),
    "hippocampus": dict(load=0.50, clear=1.1, noradrenergic=False),
    "neocortex": dict(load=0.40, clear=1.2, noradrenergic=False),
}


def rate(p: dict, maoa: float = MAOA_GAIN) -> float:
    aldehyde = maoa if p["noradrenergic"] else 0.0
    return p["load"] / p["clear"] + aldehyde


def onset(p: dict, maoa: float = MAOA_GAIN) -> float:
    return THETA / rate(p, maoa)


def ordering(maoa: float):
    return sorted(REGIONS.items(), key=lambda kv: onset(kv[1], maoa))


def main() -> None:
    print("(1) Onset ordering (earliest first) - does the LC seed first?")
    for name, p in ordering(MAOA_GAIN):
        print(f"    {name:16} rate={rate(p):.2f}  onset={onset(p):.2f}")
    print("    -> LC first, then entorhinal -> hippocampus -> neocortex (the Braak-like order).\n")

    print("(2) Does the druggable accelerant make the LC first? Remove the MAO-A term (maoa=0):")
    first_name = ordering(0.0)[0][0]
    for name, p in ordering(0.0):
        tag = "  <- still first" if name == first_name else ""
        print(f"    {name:16} onset={onset(p, 0.0):.2f}{tag}")
    print(
        "    -> the LC's STRUCTURAL load alone still ranks it first: you cannot stop it being the"
    )
    print("       origin. The aldehyde term is an accelerant, not the reason it is first.\n")

    lc = REGIONS["locus coeruleus"]
    base = onset(lc, MAOA_GAIN)
    print("(3) Repurposing lever: MAO-A inhibition scales the DOPEGAL aldehyde term (LC onset):")
    for frac in (1.0, 0.7, 0.4, 0.0):
        t = onset(lc, MAOA_GAIN * frac)
        delay = 100 * (t / base - 1)
        print(f"    MAO-A activity x{frac:.1f}: LC onset={t:.2f}  (+{delay:.0f}% vs full activity)")
    print("    -> fully blocking the aldehyde branch delays the earliest seed by ~60% here; the")
    print(
        "       field trialed MAO-B (rasagiline), not the MAO-A isoform this pathway implicates.\n"
    )

    print("(WHAT-IF, heavily caveated) The earliest-seed timing is sensitive to the accelerant, so")
    print("IF MAO-A activity varied by sex or hormonal state the LC window would shift - the only")
    print(
        "honest basis for a sex-aware TIMING clock. But human data do NOT support a clean X-linked"
    )
    print("dose effect (MAO-A dosage compensation), and the estrogen link is contradictory (MAO-A")
    print("peaks in perimenopause, not with estrogen loss). The robust human sex effect is on the")
    print("amyloid->tau coupling step, not amyloid load. A mechanism to TEST, not a premise.\n")

    print("Reading: the LC is the earliest tau seed because of an UNDRUGGABLE structural load, but")
    print(
        "the one DRUGGABLE accelerant on top of it is the MAO-A/DOPEGAL aldehyde branch - exactly"
    )
    print(
        "where a safe approved drug (a MAO-A inhibitor, not the MAO-B one that was trialed) could"
    )
    print("act. Timing, not etiology: these genes are mechanistically hot but genetically cold for")
    print("AD. Dimensionless toy; assumed factors; not calibrated and not a drug claim.")


if __name__ == "__main__":
    main()
