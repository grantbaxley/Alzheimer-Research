"""Does tau really self-amplify? Let a dose ladder of a production-lowering drug answer
(night of 2026-11-20, reversal-biology lens, "combine two catalogue ideas" constraint:
identify-autocatalysis-rate x tau-antisense-dose-inversion).

Our older idea asked whether tau pathology in people grows by local self-amplification or is
only carried along connections into vulnerable regions, and found that fitting scans passively
struggles to tell the two apart. A drug that lowers tau PRODUCTION by a known fraction is a
direct experiment instead. This script asks what each world predicts for a ladder of knock-down
fractions, region by region, on a synthetic brain network (alzres.spreading).

GROWTH world (self-amplifying, the network FKPP form with an explicit clearance term):
    dx/dt = -rho * L x  +  g * (1 - f) * x * (1 - x)  -  c * x
    x   tau load per region (0 to 1), L the network Laplacian, f the knock-down fraction
    g   gross self-amplification rate (needs tau supply, so it scales with 1 - f)
    c   clearance rate; kappa = c / g is the unknown share of amplification that clearance
        already cancels. Net growth g - c is set to a five-year doubling time, the human
        estimate of Meisl et al. (Sci Adv 2021, doi 10.1126/sciadv.abh1448).
    Net growth under treatment is g(1 - f) - c, which crosses zero at f* = 1 - kappa.

SOURCE world (no self-amplification): each region makes misfolded tau at its own fixed rate
(a "vulnerability map"), tau moves along connections and is cleared:
    dx/dt = -rho * L x  +  s_i * (1 - f)  -  c * x

Both worlds are run to a stage where untreated load rises about 12% in 18 months, then
treated for 18 months at f = 0.25, 0.50 and 0.65. We report the change in load in regions that
were already heavily loaded ("early") and in lightly loaded regions ("frontier"). Then the
strongest dose is STOPPED and re-growth is followed for three years: self-amplifying tau should
re-grow slowly at first and then accelerate; tau from fixed sources should re-grow fastest
straight away and then level off.

Synthetic network and assumed rates; shows what a dose ladder could distinguish, not what any
drug does. Not medical advice.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

from alzres.spreading import graph_laplacian, synthetic_connectome

NET_GROWTH = np.log(2) / 5.0  # per year: five-year doubling
RHO = 0.02  # spread rate along connections (assumed)
LADDER = (0.0, 0.25, 0.50, 0.65)
TREAT_YEARS = 1.5


def growth_rhs(lap, g, c, f):
    def rhs(_t, x):
        return -RHO * (lap @ x) + g * (1 - f) * x * (1 - x) - c * x

    return rhs


def source_rhs(lap, s, c, f):
    def rhs(_t, x):
        return -RHO * (lap @ x) + s * (1 - f) - c * x

    return rhs


def run(rhs, x0, years):
    sol = solve_ivp(rhs, (0, years), x0, method="LSODA", rtol=1e-8, atol=1e-10)
    return np.clip(sol.y[:, -1], 0, None)


def to_stage(make_rhs, x0, target, step=0.25, max_years=200):
    """Run untreated until the mean load reaches the target; return the state."""
    x, t = x0.copy(), 0.0
    while x.mean() < target and t < max_years:
        x = run(make_rhs(0.0), x, step)
        t += step
    return x, t


def summarise(x_start, x_end):
    early, frontier = x_start > np.quantile(x_start, 0.8), x_start < np.quantile(x_start, 0.4)
    pct = [100 * (x_end[m].mean() / x_start[m].mean() - 1) for m in (early, frontier)]
    return pct[0], pct[1], 100 * (x_end.mean() / x_start.mean() - 1)


def regrowth(make_rhs, start):
    """Treat at the strongest dose, stop, and return the load regained in each of 3 years."""
    x = run(make_rhs(LADDER[-1]), start, TREAT_YEARS)
    gains = []
    for _ in range(3):
        nxt = run(make_rhs(0.0), x, 1.0)
        gains.append(100 * (nxt.mean() - x.mean()) / start.mean())
        x = nxt
    return gains


def main() -> None:
    adj, coords = synthetic_connectome(n_regions=60, seed=0)
    lap = graph_laplacian(adj, normalized=False)
    seed = int(np.argmin(coords[:, 0]))
    dist = np.linalg.norm(coords - coords[seed], axis=1)

    print(f"Change in tau load after {TREAT_YEARS} years of treatment, by knock-down fraction f.")
    print("Columns: heavily loaded regions / lightly loaded regions / whole brain.\n")

    for kappa in (0.2, 0.5, 0.7):
        g = NET_GROWTH / (1 - kappa)
        c = kappa * g
        x0 = np.full(60, 1e-4)
        x0[seed] = 0.05
        capacity = 1 - kappa
        start, _ = to_stage(lambda f, g=g, c=c: growth_rhs(lap, g, c, f), x0, 0.35 * capacity)
        print(f"GROWTH world, clearance cancels {kappa:.0%} of amplification")
        print(f"  (net growth turns negative above f* = {1 - kappa:.0%})")
        for f in LADDER:
            end = run(growth_rhs(lap, g, c, f), start, TREAT_YEARS)
            e, fr, w = summarise(start, end)
            print(f"    f={f:.2f}:  early {e:+6.1f}%   frontier {fr:+6.1f}%   whole {w:+6.1f}%")
        print()

    regrow = {}
    c = 0.25  # per year (assumed): a four-year clearance time
    s = 0.25 * np.exp(-dist / 0.35)  # vulnerability map, highest near the first-affected region
    x0 = np.zeros(60)
    start, _ = to_stage(lambda f: source_rhs(lap, s, c, f), x0, 0.72 * (s / c).mean())
    print("SOURCE world, no self-amplification (fixed regional production, 4-year clearance)")
    for f in LADDER:
        end = run(source_rhs(lap, s, c, f), start, TREAT_YEARS)
        e, fr, w = summarise(start, end)
        print(f"    f={f:.2f}:  early {e:+6.1f}%   frontier {fr:+6.1f}%   whole {w:+6.1f}%")
    regrow["SOURCE"] = regrowth(lambda f: source_rhs(lap, s, c, f), start)

    kappa = 0.5
    g = NET_GROWTH / (1 - kappa)
    x0 = np.full(60, 1e-4)
    x0[seed] = 0.05
    make = lambda f: growth_rhs(lap, g, kappa * g, f)  # noqa: E731
    start, _ = to_stage(make, x0, 0.35 * (1 - kappa))
    regrow["GROWTH (50%)"] = regrowth(make, start)

    print("\nStop the strongest dose after 18 months and watch for three years.")
    print("Whole-brain load regained in each year, as % of the pre-treatment load:")
    for name, (y1, y2, y3) in regrow.items():
        shape = "accelerating" if y3 > y1 else "levelling off"
        print(
            f"    {name:<14} year 1 {y1:+5.1f}   year 2 {y2:+5.1f}   year 3 {y3:+5.1f}   ({shape})"
        )

    print("\nReading. (1) In BOTH worlds the response to dose is graded, and a ladder of doses")
    print("locates the smallest knock-down that halts build-up; in the GROWTH world that dose")
    print("is about 1 minus the share of amplification that clearance already cancels. (2) The")
    print("18-month region-by-dose pattern separates the worlds only weakly: heavily loaded")
    print("regions fall before lightly loaded ones in the GROWTH world, and move more nearly")
    print("in parallel in the SOURCE world. (3) The shape of re-growth after stopping differs")
    print("in the expected direction, but only modestly over three years. So a dose ladder")
    print("does not prove self-amplification, and even a stop-and-watch phase would need")
    print("precise scans. The practical answer - which dose halts build-up - comes out of the")
    print("ladder in either world. Synthetic network, assumed rates.")


if __name__ == "__main__":
    main()
