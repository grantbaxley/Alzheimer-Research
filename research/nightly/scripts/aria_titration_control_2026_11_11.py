"""ARIA as an actuator-saturation control problem: clear amyloid fast without breaking the vessels
(night of 2026-11-11, combination-timing lens, ENGINEER constraint - feedback loops, failure modes,
redundancy). ARIA (amyloid-related imaging abnormalities) is the iatrogenic failure mode of
anti-amyloid antibodies: mobilising vascular/CAA amyloid transiently weakens vessel walls (edema =
ARIA-E, microbleeds = ARIA-H), worst in APOE4 homozygotes.

The engineering crux comes from TRAILBLAZER-ALZ6 (NCT05738486; Alz & Dementia 2025,
doi 10.1002/alz.70062): at EQUAL cumulative antibody exposure and EQUAL amyloid + p-tau217 lowering,
a gentler early escalation ramp cut ARIA-E 24% -> ~14% (and far more in APOE4 homozygotes), and FDA
approved the gentler titration label. So ARIA is governed by the clearance RATE/trajectory, not the
total dose - the failure mode is decoupleable from efficacy.

Model (dimensionless; amyloid in Centiloid-like units):
    dA/dt = -D(t)                       clearance (linear: any schedule reaching target delivers the
                                        SAME total exposure, matching arms on exposure + final A)
    binding flux  J(t) = D(t) * A(t)    antibody binding to still-present vascular amyloid
    ARIA hazard   h(t) = g * J^2 / R    CONVEX in flux (the wall fails nonlinearly above a stress
                                        rate), buffered by vascular reserve R
    P_ARIA = 1 - exp(-integral of h)

Why convex and not linear: integral(D*A) over a run from A0 to A_target equals (A0^2 - A_tgt^2)/2 -
PATH-INDEPENDENT, identical for every schedule. So a hazard LINEAR in flux could never reproduce the
ALZ6 shape effect; only a convex (peak-sensitive) hazard makes front-loading worse at equal dose.
That convexity IS the testable assumption, and the real ALZ6 result (equal exposure, different ARIA)
is the evidence for it.

Three schedules at matched exposure and efficacy, differing only in SHAPE: front-loaded (full dose
early, peak flux while amyloid is high), ramped (the ALZ6 gentle ramp), and reserve-set (hold the
binding flux at a safe cap scaled by reserve). Then a reserve sweep shows the safe clearance rate
scales with R - the redundancy margin a per-patient dosing stratifier would set.

Structural control illustration; assumed rates; reproduces the ALZ6 equal-exposure/lower-ARIA result
qualitatively (magnitudes are illustrative), and is not calibrated to any drug or patient. Not
medical advice.
"""

from __future__ import annotations

import numpy as np

A0, A_TGT = 100.0, 24.0  # amyloid start and target (Centiloid-like)
D_MAX = 4.0
DT = 0.005
T_END = 600.0


def integrate(dose_fn, g: float, reserve: float = 1.0):
    a, hazard, exposure, t = A0, 0.0, 0.0, 0.0
    while t < T_END and a > A_TGT + 1e-9:
        d = max(dose_fn(t, a, reserve), 0.0)
        d = min(d, (a - A_TGT) / DT)  # don't overshoot the target
        flux = d * a
        hazard += g * flux * flux / reserve * DT
        exposure += d * DT
        a -= d * DT
        t += DT
    return dict(final=a, exposure=exposure, t=t, p_aria=100 * (1 - np.exp(-hazard)))


def front(t, a, r):
    return D_MAX


def ramp(t, a, r):
    return min(D_MAX, 0.3 + 0.6 * t)


def reserve_set(t, a, r, flux_cap=160.0):
    return min(D_MAX, flux_cap * r / a)  # hold binding flux J=D*A at a reserve-scaled safe cap


def main() -> None:
    # Calibrate the gain so the front-loaded arm sits near a 55% ARIA probability (a visible level).
    g = -np.log(1 - 0.55) / _hazard_integral(front)

    print("Three schedules at MATCHED exposure and efficacy, differing only in SHAPE:")
    print("  schedule        final_A   exposure   time_to_target   P(ARIA)")
    for name, fn in (("front-loaded", front), ("ramped", ramp), ("reserve-set", reserve_set)):
        r = integrate(fn, g)
        print(
            f"  {name:14}  {r['final']:6.1f}   {r['exposure']:7.1f}   {r['t']:10.1f}      "
            f"{r['p_aria']:5.1f}%"
        )
    print("  -> same exposure and final amyloid, yet reshaping the trajectory cuts ARIA: front-")
    print("     loading (peak flux while amyloid is high) is the failure mode; the reserve-set")
    print("     schedule nearly halves it - the ALZ6 equal-exposure/lower-ARIA result.\n")

    print("Reserve sweep (reserve-set arm): safe clearance rate scales with vascular reserve R.")
    print("  reserve R   time_to_target   P(ARIA)")
    for reserve in (1.0, 0.6, 0.35):
        r = integrate(reserve_set, g, reserve=reserve)
        print(f"  {reserve:6.2f}      {r['t']:10.1f}      {r['p_aria']:5.1f}%")
    print(
        "  -> lower reserve (APOE4-homozygote / high-CAA proxy) forces a slower safe clearance to"
    )
    print(
        "     hold ARIA at the same level - the redundancy margin a per-patient dosing rule sets.\n"
    )

    print("Reading: ARIA is an actuator-saturation problem - a fragile plant (vessels), a fast")
    print("actuator (antibody) - and the hazard is CONVEX in clearance flux, so concentrating the")
    print(
        "dose early overshoots. Because integral(D*A) is path-independent, only that convexity lets"
    )
    print(
        "schedule shape matter at equal exposure; the real ALZ6 result is the evidence for it. The"
    )
    print("'reserve-set' arm is FEED-FORWARD (safe rate from baseline reserve + the PET-measurable")
    print("amyloid trajectory), NOT closed-loop on ARIA - the only in-vivo ARIA signal is the")
    print("microbleed itself, a lagging failure, so true closed-loop would detect the crash, not")
    print("prevent it. The safe rate scales with reserve, so a reserve readout is a per-patient")
    print("SETPOINT - but baseline microbleed count already gives that cheaply, which any fluid-")
    print("biomarker rule must beat. Structural toy; assumed convex hazard; not calibrated.")


def _hazard_integral(dose_fn, reserve: float = 1.0) -> float:
    a, s, t = A0, 0.0, 0.0
    while t < T_END and a > A_TGT + 1e-9:
        d = min(max(dose_fn(t, a, reserve), 0.0), (a - A_TGT) / DT)
        s += (d * a) ** 2 / reserve * DT
        a -= d * DT
        t += DT
    return s


if __name__ == "__main__":
    main()
