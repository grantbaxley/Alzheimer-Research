"""Can you see a brain "losing resilience" before it fails - and with which measurement?
(night of 2026-11-12, earliest-signal lens, ECOLOGIST constraint).

Ecology detects ecosystems approaching collapse by "critical slowing down": as resilience falls, the
system recovers more slowly from small disturbances, so its fluctuations become larger (variance)
and more persistent (autocorrelation) (Scheffer et al., Nature 2009, doi 10.1038/nature08227;
applied to humans in Scheffer et al., PNAS 2018, doi 10.1073/pnas.1810630115). Our catalogue noted
(2026-10-29) that these signals have little human Alzheimer's precedent, "possibly because cognition
is sampled too sparsely". This toy turns that guess into numbers.

Model: a daily cognitive/physiological state fluctuating around its set-point as an
Ornstein-Uhlenbeck process, dx = -k x dt + s dW. Recovery time tau = 1/k. Three states:
    H  healthy            recovery time tau0, noise s0     (stationary SD = 1)
    S  slowed (the signal) recovery time 3*tau0, same noise (resilience lost)
    N  noisy life, NOT slowed: tau0, noise variance x3      (a confound: same variance as S)
Each observation adds measurement error set by the instrument's reliability.

Three detectors, each given the SAME budget of 30 measurements per person:
    variance         of 30 passive samples
    autocorrelation  lag-1, of 30 passive samples
    recovery probe   6 small standard disturbances (kick = 2 SD), 5 samples after each;
                     statistic = mean displacement remaining after the kick
We report AUC for telling S from H (can it see slowing?) and S from N (is it SPECIFIC to slowing,
or fooled by a merely noisier life?), with passive sampling either dense (interval = tau0/2) or
sparse (5*tau0) or clinic-like (50*tau0). The probe samples densely, but only in short bursts,
and is shown for kicks of 1, 2 and 4 SD.

Synthetic illustration; assumed parameters; says nothing about any person or any real instrument.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import rankdata

TAU0 = 1.0
N_SAMPLES = 30
N_KICKS, PER_KICK, KICK = 6, 5, 2.0
N_SIM = 3000
STATES = {
    "H": (1.0, 1.0),
    "S": (3.0, 1.0),
    "N": (1.0, 3.0),
}  # (tau multiple, noise-variance multiple)


def ou_path(rng, tau, noise_mult, dt, n, x0=None):
    """Exact OU samples at spacing dt. Healthy stationary variance is 1 by construction."""
    k = 1.0 / tau
    stat_var = noise_mult * tau / TAU0  # s^2/(2k) with s^2 = 2*noise_mult/TAU0
    phi = np.exp(-k * dt)
    step_sd = np.sqrt(stat_var * (1 - phi**2))
    x = np.empty(n)
    prev = rng.normal(0, np.sqrt(stat_var)) if x0 is None else x0
    for i in range(n):
        prev = prev * phi + rng.normal(0, step_sd)
        x[i] = prev
    return x


def observe(rng, x, reliability):
    err_sd = np.sqrt((1 - reliability) / reliability)  # relative to healthy variance of 1
    return x + rng.normal(0, err_sd, size=x.shape)


def passive_stats(rng, state, dt, reliability):
    tau_m, noise_m = STATES[state]
    y = observe(rng, ou_path(rng, tau_m * TAU0, noise_m, dt, N_SAMPLES), reliability)
    d = y - y.mean()
    ar1 = float(np.dot(d[:-1], d[1:]) / np.dot(d, d))
    return float(y.var(ddof=1)), ar1


def probe_stat(rng, state, reliability, kick=KICK):
    tau_m, noise_m = STATES[state]
    dt = TAU0 / 2
    vals = []
    for _ in range(N_KICKS):
        start = rng.normal(0, np.sqrt(noise_m * tau_m)) + kick  # resting state plus the disturbance
        x = ou_path(rng, tau_m * TAU0, noise_m, dt, PER_KICK, x0=start)
        vals.append(observe(rng, x, reliability).mean())
    return float(np.mean(vals))


def auc(pos, neg):
    r = rankdata(np.concatenate([pos, neg]))
    u = r[: len(pos)].sum() - len(pos) * (len(pos) + 1) / 2
    return u / (len(pos) * len(neg))


def main() -> None:
    rng = np.random.default_rng(0)
    print("Expected lag-1 autocorrelation actually OBSERVED (analytic), healthy -> slowed:")
    print("  sampling interval   reliability 0.9      reliability 0.6")
    for mult in (0.5, 1.0, 5.0, 50.0):
        cells = []
        for rel in (0.9, 0.6):
            err = (1 - rel) / rel
            h = (1 / (1 + err)) * np.exp(-mult)
            s = (3 / (3 + err)) * np.exp(-mult / 3)
            cells.append(f"{h:.2f} -> {s:.2f}")
        print(f"  {mult:>4.1f} x tau0          {cells[0]:<20} {cells[1]}")
    print("  -> persistence is only visible when samples are closer together than a few recovery")
    print("     times; at clinic-like spacing both states look like white noise.\n")

    regimes = (
        ("dense, 0.5 x tau0", TAU0 / 2),
        ("sparse, 5 x tau0", 5 * TAU0),
        ("clinic-like, 50 x tau0", 50 * TAU0),
    )
    for rel in (0.9, 0.6):
        print(f"AUC with {N_SAMPLES} measurements per person, instrument reliability {rel}:")
        print("  detector (sampling)                      slowed vs healthy   slowed vs noisy-life")
        rows = []
        for label, dt in regimes:
            st = {
                k: np.array([passive_stats(rng, k, dt, rel) for _ in range(N_SIM)]) for k in STATES
            }
            rows.append(
                (
                    f"variance ({label})",
                    auc(st["S"][:, 0], st["H"][:, 0]),
                    auc(st["S"][:, 0], st["N"][:, 0]),
                )
            )
            rows.append(
                (
                    f"autocorrelation ({label})",
                    auc(st["S"][:, 1], st["H"][:, 1]),
                    auc(st["S"][:, 1], st["N"][:, 1]),
                )
            )
        for kick in (1.0, 2.0, 4.0):
            pr = {
                k: np.array([probe_stat(rng, k, rel, kick) for _ in range(N_SIM)]) for k in STATES
            }
            rows.append(
                (
                    f"recovery probe (kick {kick:.0f} SD, bursts)",
                    auc(pr["S"], pr["H"]),
                    auc(pr["S"], pr["N"]),
                )
            )
        for name, a_h, a_n in rows:
            print(f"  {name:<40} {a_h:>10.2f} {a_n:>20.2f}")
        print()

    print("Reading (what this toy shows, and what it does not):")
    print("(1) Variance is the easiest signal to see and survives sparse sampling, but it is NOT")
    print(
        "    specific: a merely noisier life raises it just as much (AUC <= 0.5 vs that confound)."
    )
    print("(2) Autocorrelation is specific to slowing, but weakens as samples spread out and is")
    print(
        "    gone at clinic-like spacing (AUC ~0.5) - the signal cannot be seen at visit intervals"
    )
    print("    far longer than the recovery time, whether or not it exists.")
    print(
        "(3) A recovery probe (disturb, then time the return) is also specific. At a 2-SD kick it"
    )
    print(
        "    is only about as good as dense passive autocorrelation for the same 30 measurements;"
    )
    print("    its edge grows with kick size and it needs dense sampling only in short bursts.")
    print(
        "So sparse clinic visits cannot reveal critical slowing down even if it is present; dense"
    )
    print(
        "bursts or a standard stress test could. Whether cognition really slows before Alzheimer's"
    )
    print("is an empirical question this toy does not answer. Assumed parameters throughout.")


if __name__ == "__main__":
    main()
