"""What carries the decline that continues after plaque removal? Three accounts, three shapes
(night of 2026-11-19, causal-chain lens, "already symptomatic" constraint).

In the pivotal lecanemab trial, people on the drug declined 1.21 points on the CDR-SB scale over
18 months against 1.66 on placebo: a difference of 0.45, or 27% (van Dyck et al., NEJM 2023,
doi 10.1056/NEJMoa2212948). The difference was already 0.17 at 6 months (95% interval 0.05 to
0.29). In the uncontrolled extension, compared with an outside natural-history cohort, the
reported differences were 0.52, 1.01 and 1.75 at 18, 36 and 48 months (conference abstract,
doi 10.1002/alz70861_108905). So roughly 73% of the decline continues. Why? This script puts
numbers on three accounts and asks what each predicts that the others do not.

PART 1 - the shape of the benefit over time. Three worlds, each calibrated to the same 0.45 at
18 months:
    SWITCH          a fixed share of the decline rate is turned off within weeks (as if the drug
                    neutralises a soluble toxic form; plaque mass is beside the point)
    PLAQUE-PROMPT   the amyloid-driven part of decline tracks the plaque still present, which
                    clears gradually (time constant TAU months) down to a floor
    PLAQUE-LAGGED   the same, but damage downstream responds only after a further delay
Each world implies a different difference at 6, 36 and 48 months, and a different share of the
decline that amyloid is driving once clearance is complete.

PART 2 - a ceiling for the co-pathology account. If other brain diseases (Lewy bodies, TDP-43,
vessel damage) carry a share c of the decline and the drug cannot touch that share, how much of
the Alzheimer-specific decline must amyloid be driving to produce the observed 27%?

PART 3 - can the trials already run tell? Power of a "treatment x co-pathology marker" test in
one trial of the size of the lecanemab trial, and in two such trials pooled, if marker-positive
people benefit less.

Inputs that are ASSUMED, not measured: the clearance time constant, the lag, the speed-up of
natural decline after 18 months, the share of people who are marker-positive and their benefit.
The person-to-person spread is derived from the trial's reported confidence interval. This is an
aggregate-numbers exercise; it says what to look for, not what is true. Not medical advice.
"""

from __future__ import annotations

import numpy as np
from scipy import stats

PLACEBO_18, DIFF_18 = 1.66, 0.45
REPORTED = {6: 0.17, 18: 0.45, 36: 1.01, 48: 1.75}  # 36 and 48 are versus an outside cohort
FLOOR = 0.30  # share of plaque remaining after treatment (about 23 of 76 Centiloids)
TAU = 6.0  # months; ASSUMED time constant of plaque clearance
LAG = 9.0  # months; ASSUMED extra downstream delay in the lagged world
SPEEDUP = {18: 1.0, 36: 1.3, 48: 1.6}  # ASSUMED natural decline rate relative to months 0-18
N_ARM = (859, 875)  # analysed per arm in the trial


def derive_sd() -> float:
    """SD of individual 18-month change implied by the reported interval (-0.67 to -0.23)."""
    se = (0.67 - 0.23) / (2 * 1.96)
    return float(se / np.sqrt(1 / N_ARM[0] + 1 / N_ARM[1]))


def control_rate(t: np.ndarray, speedup: bool) -> np.ndarray:
    """Natural decline rate (points per month); optionally faster later in the disease."""
    base = PLACEBO_18 / 18
    if not speedup:
        return np.full_like(t, base)
    return base * np.where(t < 18, SPEEDUP[18], np.where(t < 36, SPEEDUP[36], SPEEDUP[48]))


def removed(t: np.ndarray, world: str) -> np.ndarray:
    """Effective share of the amyloid-driven decline that is switched off at time t."""
    if world == "SWITCH":
        return np.ones_like(t)
    prompt = (1 - FLOOR) * (1 - np.exp(-t / TAU))
    if world == "PLAQUE-PROMPT":
        return prompt
    # first-order lag applied to the prompt curve (closed form for two exponentials)
    return (1 - FLOOR) * (1 - (TAU * np.exp(-t / TAU) - LAG * np.exp(-t / LAG)) / (TAU - LAG))


def difference(months: float, world: str, share: float, speedup: bool = True) -> float:
    t = np.linspace(0, months, 4001)
    y = share * removed(t, world) * control_rate(t, speedup)
    return float(np.sum((y[1:] + y[:-1]) / 2 * np.diff(t)))


def calibrated_share(world: str) -> float:
    return DIFF_18 / difference(18, world, 1.0)


def interaction_power(benefit_neg: float, benefit_pos: float, pos_share: float, trials: float):
    sd = derive_sd()
    n_pos = [n * pos_share * trials for n in N_ARM]
    n_neg = [n * (1 - pos_share) * trials for n in N_ARM]
    se = sd * np.sqrt(sum(1 / n for n in n_pos + n_neg))
    z = (benefit_neg - benefit_pos) / se
    return float(stats.norm.sf(1.96 - z) + stats.norm.cdf(-1.96 - z))


def simulated_power(benefit_neg, benefit_pos, pos_share, trials, rng, reps=2000) -> float:
    sd, hits = derive_sd(), 0
    for _ in range(reps):
        est, var = [], []
        for share, benefit in ((1 - pos_share, benefit_neg), (pos_share, benefit_pos)):
            n0, n1 = (int(n * share * trials) for n in N_ARM)
            drug, placebo = rng.normal(-benefit, sd, n0), rng.normal(0, sd, n1)
            est.append(placebo.mean() - drug.mean())
            var.append(drug.var(ddof=1) / n0 + placebo.var(ddof=1) / n1)
        hits += abs(est[0] - est[1]) / np.sqrt(sum(var)) > 1.96
    return hits / reps


def main() -> None:
    print("PART 1. Three shapes of benefit, each calibrated to 0.45 points at 18 months")
    print("  (difference in CDR-SB points, drug versus no drug)\n")
    print(f"  {'world':<15}{'6 mo':>7}{'18 mo':>7}{'36 mo':>7}{'48 mo':>7}   amyloid-driven share")
    print(f"  {'':<15}{'':>7}{'':>7}{'':>7}{'':>7}   of decline it implies")
    for world in ("SWITCH", "PLAQUE-PROMPT", "PLAQUE-LAGGED"):
        share = calibrated_share(world)
        cells = "".join(f"{difference(m, world, share):>7.2f}" for m in (6, 18, 36, 48))
        flag = "  (over 100%: impossible)" if share > 1 else ""
        print(f"  {world:<15}{cells}   {share:>6.0%}{flag}")
    cells = "".join(f"{REPORTED[m]:>7.2f}" for m in (6, 18, 36, 48))
    print(f"  {'reported':<15}{cells}")
    print("  6 months: randomised, 95% interval 0.05 to 0.29. 36 and 48 months: uncontrolled")
    print("  extension against an outside cohort, people who stayed on treatment only.")
    print("  The 36- and 48-month rows assume natural decline speeds up by 1.3x and 1.6x.")
    print("  With NO speed-up they read:")
    for world in ("SWITCH", "PLAQUE-PROMPT"):
        share = calibrated_share(world)
        late = "".join(f"{difference(m, world, share, False):>7.2f}" for m in (36, 48))
        print(f"  {world:<15}{'':>14}{late}")
    print("  So the late numbers cannot separate SWITCH from PLAQUE-PROMPT without knowing the")
    print("  outside cohort's own decline; the randomised 6-month value leans to SWITCH but its")
    print("  interval includes both. Only a long (nine-month) downstream lag is excluded.\n")

    print("PART 2. If co-pathology carries a share c of decline that the drug cannot touch,")
    print("  the share of ALZHEIMER-SPECIFIC decline that amyloid must be driving is:")
    print(f"  {'world':<15}" + "".join(f"{'c=' + format(c, '.0%'):>9}" for c in (0, 0.2, 0.3, 0.4)))
    for world in ("SWITCH", "PLAQUE-PROMPT"):
        share = calibrated_share(world)
        cells = ""
        for c in (0, 0.2, 0.3, 0.4):
            need = share / (1 - c)
            cells += f"{need:>9.0%}" if need <= 1 else f"{'>100%':>9}"
        print(f"  {world:<15}{cells}")
    print("  Reading across: under SWITCH, even 40% co-pathology leaves amyloid driving under")
    print("  half of the Alzheimer-specific decline. Under PLAQUE-PROMPT the same data mean")
    print("  amyloid drives most of it, and co-pathology above about 40% would explain ALL the")
    print("  rest. The 27% figure alone cannot tell these apart; the timing in Part 1 can.\n")

    sd = derive_sd()
    rng = np.random.default_rng(0)
    print("PART 3. Could a re-analysis of stored trial samples show that marker-positive people")
    print(f"  benefit less? (spread of 18-month change implied by the trial: SD {sd:.2f} points;")
    print("  assumed 25% marker-positive; average benefit held at 0.45)\n")
    print("  benefit, marker-neg / marker-pos     one trial   two trials pooled   (simulated)")
    for pos in (0.30, 0.15, 0.0):
        neg = (DIFF_18 - 0.25 * pos) / 0.75
        p1, p2 = (interaction_power(neg, pos, 0.25, k) for k in (1, 2))
        s2 = simulated_power(neg, pos, 0.25, 2, rng)
        print(f"  {neg:>10.2f} / {pos:<4.2f}{'':<18}{p1:>8.0%}{p2:>15.0%}{s2:>17.0%}")
    print("\n  The same test in a spinal-fluid SUBSTUDY (the only people with stored fluid):")
    for n_total in (281, 410):
        frac = n_total / sum(N_ARM)
        p0 = interaction_power(0.60, 0.0, 0.25, frac)
        print(f"    {n_total} people, marker-positive get NO benefit: power {p0:.0%}")
    print("\n  Even if marker-positive people got NO benefit, one whole trial would show it only")
    print("  about two times in three, and a substudy of a few hundred about one time in six to")
    print("  one in five. A partial difference is close to invisible. So a 'no difference by")
    print("  marker status' result from a substudy says almost nothing; the question needs every")
    print("  participant (a marker from the baseline scan) and trials pooled.")


if __name__ == "__main__":
    main()
