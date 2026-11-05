"""Do network "firebreaks" buy tau-spread resilience? (night of 2026-11-05, resilience lens,
"use a field outside medicine" constraint). Tests a cross-domain idea borrowed from wildfire
firebreaks / power-grid islanding / percolation theory: that a resilient brain arrests a
prion-like tau front at network bottlenecks. Built on the repo's own spreading tools
(alzres.spreading): FKPP reaction-diffusion (autocatalytic growth + transport; HAS an invasion
threshold) versus the linear network-diffusion model (NDM; transport only, NO threshold).

The cross-domain insight under test (from tonight's research): a "resilience threshold" is a
property of the DYNAMICS, not the connectome - it can exist only if tau growth is autocatalytic
(FKPP), because linear diffusion floods every connected node eventually. So two questions:

  (1) Is there an invasion threshold in the GROWTH rate alpha under FKPP, and is it absent for NDM?
  (2) Given an above-threshold front, can down-weighting the top "bottleneck" edges (high edge
      effective resistance = bridges) CONTAIN it - and does WHERE you cut beat how MUCH you cut
      (targeted bottlenecks vs the same number of random edges)? This is the firebreak/islanding
      claim.

Honest spoiler recorded in the reading: (1) holds - FKPP has a sharp threshold in alpha, NDM has
none. (2) FAILS as a resilience mechanism: partial weakening of even the top bottleneck edges does
not contain a supercritical front (each region self-amplifies once seeded); only a FULL cut
contains, and that merely disconnects the epicenter node (and contains NDM equally), i.e. it is
trivial disconnection a brain cannot do, not a dynamical firebreak. Conclusion: against an
autocatalytic spreader, resilience lives in the GROWTH term (the lithium/GSK3-beta and
disease-tolerance levers explored tonight), not in edge topology.

Structural toy on a synthetic connectome; dimensionless; validates the logic, says nothing about
any real brain.
"""

from __future__ import annotations

import numpy as np
from scipy.sparse.csgraph import connected_components

import alzres.spreading as s

N_REGIONS, K_NEIGHBORS, N_LONG_RANGE = 200, 6, 40
RHO = 1.0
T_EVAL = np.linspace(0.0, 25.0, 51)
M_EDGES = 60  # how many top-bottleneck (or random) edges to down-weight


def build():
    A, coords = s.synthetic_connectome(
        n_regions=N_REGIONS, k_neighbors=K_NEIGHBORS, n_long_range=N_LONG_RANGE, seed=0
    )
    seed = int(np.argmin(coords.sum(axis=1)))  # peripheral, entorhinal-like epicenter
    x0 = np.zeros(A.shape[0])
    x0[seed] = 1.0
    return A, seed, x0


def edge_bottleneck_order(A):
    """Rank edges by effective resistance (bridge-ness) via the Laplacian pseudoinverse."""
    lp = np.linalg.pinv(s.graph_laplacian(A, normalized=False))
    iu, ju = np.where(np.triu(A, 1) > 0)
    diag = np.diag(lp)
    er = diag[iu] + diag[ju] - 2 * lp[iu, ju]
    return iu, ju, np.argsort(-er)


def down_weight(A, iu, ju, edges, g):
    B = A.copy()
    for e in edges:
        i, j = iu[e], ju[e]
        B[i, j] *= 1 - g
        B[j, i] *= 1 - g
    return B


def fkpp_extent(A, x0, alpha):
    return float((s.fkpp(A, x0, T_EVAL, rho=RHO, alpha=alpha)[-1] > 0.5).mean())


def ndm_reach(A, x0):
    return float((s.network_diffusion(A, x0, T_EVAL, beta=1.0)[-1] > 1e-4).mean())


def main() -> None:
    A, seed, x0 = build()
    iu, ju, order = edge_bottleneck_order(A)
    rng = np.random.default_rng(0)

    print("(1) Invasion threshold in GROWTH rate alpha (FKPP) vs linear diffusion (NDM)")
    print("    FKPP: fraction of regions with tau>0.5 at t_end")
    for alpha in (0.1, 0.2, 0.3, 0.4, 0.8):
        print(f"      alpha={alpha}: extent {fkpp_extent(A, x0, alpha):.2f}")
    print(
        f"    NDM has no growth term and floods every connected node: reach {ndm_reach(A, x0):.2f}"
    )
    print("    -> a threshold exists only for the autocatalytic (FKPP) dynamics.\n")

    alpha = 0.4  # just above threshold: the front invades
    print(
        f"(2) Firebreak/islanding test at supercritical alpha={alpha} (baseline extent "
        f"{fkpp_extent(A, x0, alpha):.2f})"
    )
    print(f"    Down-weight the top-{M_EDGES} bottleneck edges vs {M_EDGES} random edges:")
    for g in (0.5, 0.9, 1.0):
        tgt = fkpp_extent(down_weight(A, iu, ju, order[:M_EDGES], g), x0, alpha)
        rnd = np.mean(
            [
                fkpp_extent(
                    down_weight(A, iu, ju, rng.choice(len(iu), M_EDGES, replace=False), g),
                    x0,
                    alpha,
                )
                for _ in range(10)
            ]
        )
        print(f"      g={g}: targeted bottlenecks {tgt:.2f} | random edges {rnd:.2f}")

    cut = down_weight(A, iu, ju, order[:M_EDGES], 1.0)
    _, labels = connected_components(cut > 0, directed=False)
    seed_mod = int(np.bincount(labels)[labels[seed]])
    print(
        f"    Full cut (g=1.0) isolates the epicenter: its component is {seed_mod} of "
        f"{N_REGIONS} nodes,"
    )
    print(f"    and it contains NDM too (NDM reach after full cut {ndm_reach(cut, x0):.2f}).\n")

    print("Reading: (1) FKPP shows a sharp invasion threshold in the GROWTH rate (alpha 0.2 -> 0%,")
    print("   0.4 -> 100%); NDM, being linear transport, has none and floods every connected node.")
    print(
        "   So a 'resilience threshold' is a property of autocatalytic dynamics, not of the wiring."
    )
    print(
        "   (2) The firebreak/islanding analogy FAILS as a resilience mechanism: partial weakening"
    )
    print("   of even the top bottleneck edges does NOT contain a supercritical front (each region")
    print(
        "   self-amplifies once seeded), and the only thing that contains it - a full cut - merely"
    )
    print("   disconnects the epicenter node (and contains linear diffusion equally), i.e. trivial")
    print(
        "   disconnection a brain cannot perform, not a dynamical firebreak. Conclusion: against an"
    )
    print(
        "   autocatalytic spreader, resilience lives in the GROWTH term (the lithium/GSK3-beta and"
    )
    print(
        "   disease-tolerance levers), not in edge topology. A night that kills a borrowed analogy."
    )
    print(
        "   Synthetic connectome; assumed rates; validates the logic, not any claim about brains."
    )


if __name__ == "__main__":
    main()
