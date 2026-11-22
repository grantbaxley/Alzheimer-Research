"""How much should we believe a repurposing idea? A base-rate calculator
(night of 2026-11-22, red-team lens, "approved for something else" constraint).

Most of the approved medicines ever tried against Alzheimer's disease in a randomised trial
failed. Before ranking any repurposing idea of our own, this script turns that track record into
numbers:

PART 1  the base rate: of N_TRIALS sizeable randomised trials of already-approved medicines (or
        widely used supplements) with a clinical primary endpoint, N_MET met it. A Beta posterior
        (Jeffreys prior) gives the plausible range for the chance that the next one succeeds.
PART 2  what a POSITIVE result is worth: the chance that a positive trial reflects a real effect,
        for a small trial (low power, several endpoints and subgroups to choose from) and for a
        pivotal-size trial, starting from the base rate.
PART 3  what supporting evidence is worth: how far the chance moves if an idea also has
        human-genetic support (about 2.6 times the success rate across drug development;
        Minikel et al., Nature 2024, doi 10.1038/s41586-024-07316-0) or has survived an
        active-comparator test, and how far it falls if it failed one.

The counts in PART 1 come from the scoreboard compiled on this night from abstracts and registry
records (see the log; a best-effort tally, not a systematic review). The multipliers in PART 3
other than the genetic one are ASSUMED for illustration. This is a way to hold claims to the
same standard, not a prediction about any drug. Not medical advice.
"""

from __future__ import annotations

from scipy import stats

N_TRIALS = 65  # sizeable randomised trials of approved medicines or supplements (the scoreboard)
N_MET = 8  # met the primary endpoint cleanly
N_REPLICATED = 0  # treatment wins confirmed by an independent second trial
PRIORS = (0.01, 0.03, 0.05)  # realistic chances that a repurposing candidate truly works


def posterior(k: int, n: int):
    dist = stats.beta(k + 0.5, n - k + 0.5)
    return dist.mean(), dist.ppf(0.025), dist.ppf(0.975)


def ppv(prior: float, power: float, false_pos: float) -> float:
    """Chance a positive result is real."""
    return prior * power / (prior * power + (1 - prior) * false_pos)


def shift(prior: float, ratio: float) -> float:
    odds = prior / (1 - prior) * ratio
    return odds / (1 + odds)


def main() -> None:
    mean, lo, hi = posterior(N_MET, N_TRIALS)
    r_mean, r_lo, r_hi = posterior(N_REPLICATED, N_TRIALS)
    print("PART 1. The base rate")
    print(f"  {N_MET} of {N_TRIALS} trials met their primary endpoint: {mean:.1%}")
    print(f"      (95% range {lo:.1%} to {hi:.1%})")
    print(f"  {N_REPLICATED} of {N_TRIALS} produced a win that an independent trial confirmed:")
    print(f"      {r_mean:.1%} (95% range {r_lo:.1%} to {r_hi:.1%})")
    by_chance = f"{N_TRIALS * 0.025:.0f}-{N_TRIALS * 0.05:.0f}"
    print(f"  With no real effects at all, about {by_chance} of {N_TRIALS} trials would still")
    print("  'meet' an endpoint by chance at the usual threshold, before any flexible analysis.")
    print("  So the first line overstates the chance of a REAL effect; the second line and the")
    print("  compiler's own estimate (2-5%) are the better guide. Used below: 1%, 3% and 5%.\n")

    print("PART 2. If a trial comes out positive, how likely is the effect real?")
    heads = "".join(f"{format(p, '.0%'):>8}" for p in PRIORS)
    print(f"  {'kind of trial':<52}  {heads}   <- starting chance")
    kinds = (
        ("small trial, one pre-set endpoint (power 30%)", 0.30, 0.025),
        ("small trial, best of several endpoints/subgroups", 0.45, 0.20),
        ("pivotal-size trial, one pre-set endpoint (power 80%)", 0.80, 0.025),
    )
    for name, power, fp in kinds:
        cells = "".join(f"{ppv(p, power, fp):>8.0%}" for p in PRIORS)
        print(f"  {name:<52}  {cells}")
    two = [ppv(ppv(p, 0.8, 0.025), 0.8, 0.025) for p in PRIORS]
    cells = "".join(f"{v:>8.0%}" for v in two)
    print(f"  {'two pivotal-size trials, both positive':<52}  {cells}\n")

    mid = PRIORS[1]
    print(f"PART 3. What supporting evidence does to a {mid:.0%} starting chance")
    rows = (
        ("observational support only (the usual case)", 1.0),
        ("+ human-genetic support for the drug's target", 2.6),
        ("+ survived an active-comparator test (assumed x1.5)", 1.5),
        ("+ both", 2.6 * 1.5),
        ("failed an active-comparator test (assumed x0.3)", 0.3),
    )
    for name, ratio in rows:
        print(f"  {name:<52}{shift(mid, ratio):>8.1%}")
    print("\nReading. About one trial in eight 'met' its endpoint, but none of those wins was")
    print("confirmed independently and two failed outright when repeated. Starting from a")
    print("realistic chance of a few percent, a positive small trial is far more likely a false")
    print("alarm than a real effect, and almost certainly so when the endpoint or subgroup was")
    print("chosen afterwards. One clean pivotal-size win makes a real effect roughly a coin")
    print("toss; two make it very likely. Supporting evidence helps less than hoped: the")
    print("active-comparator multiplier is an assumption, and its one clean prospective test (a")
    print("diabetes drug whose health-record comparison against sister drugs predicted benefit)")
    print("failed in two large trials. No realistic combination lifts an untested repurposing")
    print("idea much above one chance in ten. The counts are one night's best-effort tally from")
    print("abstracts, not a systematic review.")


if __name__ == "__main__":
    main()
