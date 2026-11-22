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

The counts in PART 1 come from the scoreboard compiled on this night (see the log; the list is
the compiler's best effort, not a systematic review). The multipliers in PART 3 other than the
genetic one are ASSUMED for illustration. This is a way to hold claims to the same standard, not
a prediction about any drug. Not medical advice.
"""

from __future__ import annotations

from scipy import stats

N_TRIALS = 40  # sizeable randomised trials of approved medicines, clinical primary endpoint
N_MET = 2  # met the primary endpoint
N_REPLICATED = 0  # wins confirmed by a second trial


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
    print(f"  {N_MET} of {N_TRIALS} trials met their primary endpoint: chance the next one does")
    print(f"  = {mean:.1%} (95% range {lo:.1%} to {hi:.1%})")
    print(f"  {N_REPLICATED} of {N_TRIALS} produced a win that was then confirmed: {r_mean:.1%}")
    print(f"  (95% range {r_lo:.1%} to {r_hi:.1%})\n")

    print("PART 2. If a trial comes out positive, how likely is the effect real?")
    heads = "".join(f"{format(p, '.0%'):>8}" for p in (lo, mean, hi))
    print(f"  {'kind of trial':<52}  {heads}   <- starting chance")
    kinds = (
        ("small trial, one pre-set endpoint (power 30%)", 0.30, 0.025),
        ("small trial, best of several endpoints/subgroups", 0.45, 0.20),
        ("pivotal-size trial, one pre-set endpoint (power 80%)", 0.80, 0.025),
    )
    for name, power, fp in kinds:
        cells = "".join(f"{ppv(p, power, fp):>8.0%}" for p in (lo, mean, hi))
        print(f"  {name:<52}  {cells}")
    two = [ppv(ppv(p, 0.8, 0.025), 0.8, 0.025) for p in (lo, mean, hi)]
    cells = "".join(f"{v:>8.0%}" for v in two)
    print(f"  {'two pivotal-size trials, both positive':<52}  {cells}")
    print("  (columns: low end, middle and high end of the base-rate range from Part 1)\n")

    print("PART 3. What supporting evidence does to the chance of success")
    rows = (
        ("observational support only (the usual case)", 1.0),
        ("+ human-genetic support for the drug's target", 2.6),
        ("+ survived an active-comparator test (assumed x2)", 2.0),
        ("+ both", 2.6 * 2.0),
        ("failed an active-comparator test (assumed x0.3)", 0.3),
    )
    for name, ratio in rows:
        print(f"  {name:<52}{shift(mean, ratio):>8.1%}")
    print("\nReading. Starting from this track record, a positive small trial of a repurposed")
    print("drug is more likely to be a false alarm than a real effect, and much more so when the")
    print("endpoint or subgroup was chosen afterwards. One clean pivotal-size win makes a real")
    print("effect about as likely as not; it takes two to be confident. Supporting evidence")
    print("helps, but no realistic combination lifts an untested repurposing idea above roughly")
    print("one chance in four. The counts are a best-effort tally; the multipliers other than")
    print("the genetic one are assumptions.")


if __name__ == "__main__":
    main()
