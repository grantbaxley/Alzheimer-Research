"""The silent-engram reversal window (night of 2026-11-04, reversal-biology lens, "focus on
women" constraint). A structural toy of the one thing the engram literature says is actually
reversible: memories held in neurons that are still ALIVE but synaptically SILENCED can be
recovered (Roy/Tonegawa 2016, Nature, doi 10.1038/nature17172); memories whose neurons are
DEAD are gone. So "reversal" is recovery of the silenced pool, never resurrection of the lost
pool.

Two compartments of an engram ensemble as disease advances along a stage axis s in [0, 1]:

    silenced(s) = S0 * exp(-s / TAU_SIL)        alive-but-silenced fraction (recoverable)
    lost(s)     = 1 - exp(-s / TAU_LOSS)         dead neurons (not recoverable)
    functional(s) = max(0, 1 - silenced(s) - lost(s))   what is working untreated

A reactivation therapy (optogenetic-engram analogue; also the OSK-engram 2026 Neuron result in
amyloid mice) restores a fraction EFF of the SILENCED pool only:

    recovered(s) = functional(s) + EFF * silenced(s)      capped at 1 - lost(s)

The ceiling is 1 - lost(s): you can never beat the surviving-neuron fraction. The point is the
SHAPE - recoverable benefit is large early (big silenced pool, little loss) and collapses as
loss overtakes silencing, which is exactly the "treat early" wall seen on other nights, but here
derived from alive-vs-dead rather than reversible-vs-banked damage.

Women constraint: rodent plasticity/reactivation capacity is estrogen-gated (Galea reviews, Mol
Brain 2019 doi 10.1186/s41041-019-0442-7; Vitam Horm 2022 PMID 35180925), and the female second-X
reserve is age-reactivated (Gadek 2025, Sci Adv). We represent this only as EFF depending on a
hormonal-context knob - NOT a claim about any person, just to show the lever the biology points
at: if reactivation efficiency itself falls at menopause, the recoverable window shrinks for a
reason that is modifiable in principle (restore the context) rather than fixed (neuron loss).

Dimensionless structural illustration; assumed rates; not calibrated to any patient, drug, or sex.
"""

from __future__ import annotations

import numpy as np

S0 = 0.6  # fraction of the ensemble that starts as silenceable (vs always-functional)
TAU_SIL = 0.35  # stage-scale over which engrams fall silent
TAU_LOSS = 0.9  # stage-scale over which neurons die (slower than silencing early on)


def curves(eff: float, stages: np.ndarray):
    silenced = S0 * np.exp(-stages / TAU_SIL)
    lost = 1.0 - np.exp(-stages / TAU_LOSS)
    functional = np.clip(1.0 - silenced - lost, 0.0, 1.0)
    ceiling = np.clip(1.0 - lost, 0.0, 1.0)
    recovered = np.minimum(functional + eff * silenced, ceiling)
    gain = recovered - functional
    return functional, recovered, gain, ceiling


def main() -> None:
    stages = np.linspace(0.0, 1.0, 11)
    print("Reactivation restores the SILENCED pool only; ceiling = surviving-neuron fraction.\n")
    for eff, label in (
        (0.8, "high reactivation efficiency (eff=0.8)"),
        (0.4, "low efficiency (eff=0.4) - e.g. a collapsed plasticity context"),
    ):
        print(f"{label}")
        functional, recovered, gain, ceiling = curves(eff, stages)
        print("   stage  untreated  treated  gain  ceiling")
        for i in (0, 2, 4, 6, 8, 10):
            s = stages[i]
            print(
                f"   {s:4.1f}    {functional[i]:6.2f}   {recovered[i]:6.2f}  "
                f"{gain[i]:5.2f}  {ceiling[i]:6.2f}"
            )
        best = int(np.argmax(gain))
        print(
            f"   -> biggest recoverable gain at stage {stages[best]:.1f} (gain {gain[best]:.2f})\n"
        )

    _, _, gain_hi, _ = curves(0.8, stages)
    peak_stage = stages[int(np.argmax(gain_hi))]
    print("Reading: two honest results plus one caveat. (1) Recoverable gain is front-loaded -")
    print(f"   it peaks early (around stage {peak_stage:.1f}) and falls to near zero late, as the")
    print("   silenced (recoverable) pool shrinks while the dead (unrecoverable) pool grows; the")
    print("   treated curve can never exceed the surviving-neuron ceiling. (2) This reproduces the")
    print("   recurring 'treat early' wall from a NEW mechanism - alive-but-silent vs dead, not")
    print("   reversible vs banked damage. CAVEAT: recovered gain is eff*silenced, LINEAR in")
    print("   reactivation efficiency, so halving eff halves benefit by construction - not a")
    print("   finding, just arithmetic. The only real point is that efficiency (the knob the")
    print("   sex/hormonal-context biology points at) is a multiplier acting ON TOP of timing, so")
    print("   a collapsed plasticity context and a late start compound. Structural toy; assumed")
    print("   rates; not a drug or sex claim, and 'reactivation' has never raised human synaptic")
    print("   density in a trial (SV2A PET).")


if __name__ == "__main__":
    main()
