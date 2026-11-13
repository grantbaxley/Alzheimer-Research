"""Which way does the signal point? A first test of early-warning-direction-test on open EEG
(night of 2026-11-13; analysis approved by the project owner on 2026-11-12).

Critical-slowing-down theory says a system losing resilience shows LONGER timescales and MORE
variability; a brain losing neurons and synapses might instead show SHORTER timescales. Before
anyone builds an early-warning detector, measure the sign. This script does that on an open,
CC0 resting-EEG dataset (OpenNeuro ds004504: Alzheimer's disease, frontotemporal dementia and
healthy controls, eyes closed, 19 channels, 500 Hz; doi 10.18112/openneuro.ds004504.v1.0.9; data
descriptor doi 10.3390/data8060095). It uses the dataset's own preprocessed recordings.

IMPORTANT LIMITS: these are SYMPTOMATIC patients, not preclinical; one site; 88 people. The result
can show whether the method works and which sign appears at the dementia stage - nothing about the
years before symptoms.

Usage:  python eeg_direction_test_2026_11_13.py /path/to/ds004504
The recordings are never copied into this repository; only this code and the printed group-level
summary statistics are kept. Nothing per-person is printed.

Per person (median over channels):
  peak_cog      centre-of-gravity frequency of the 4-13 Hz spectrum (the "EEG slowing" covariate)
  acw50_ms      broadband autocorrelation window: lag at which the signal's autocorrelation falls
                to 0.5 (a standard intrinsic-timescale measure; trivially lengthened by slowing)
  env_tau_s     persistence of the rhythm's amplitude envelope: lag at which the envelope's
                autocorrelation falls to 1/e, with the band centred on that person's own peak
  env_cv        variability of that envelope (SD / mean)
Group contrast: Cohen's d (patients minus controls) with a bootstrap 95% interval, then the same
contrast adjusted for peak frequency, age and sex. Pre-stated rule: |adjusted d| < 0.2 means "no
direction to exploit in this signal".
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
from scipy.fft import next_fast_len
from scipy.io import loadmat
from scipy.signal import butter, hilbert, sosfiltfilt, welch

MEASURES = ("peak_cog", "acw50_ms", "env_tau_s", "env_cv")


def acf_fft(x: np.ndarray) -> np.ndarray:
    x = x - x.mean()
    n = len(x)
    f = np.fft.rfft(x, next_fast_len(2 * n))
    ac = np.fft.irfft(f * np.conj(f))[:n]
    return ac / ac[0]


def first_crossing(ac: np.ndarray, level: float, dt: float) -> float:
    below = np.nonzero(ac < level)[0]
    if len(below) == 0:
        return float("nan")
    i = below[0]
    frac = (ac[i - 1] - level) / (ac[i - 1] - ac[i])  # linear interpolation between samples
    return float((i - 1 + frac) * dt)


def person_measures(path: Path) -> dict[str, float]:
    m = loadmat(path, squeeze_me=True, struct_as_record=False)
    x = np.asarray(m["data"], dtype=np.float64)
    fs = float(m["srate"])
    f, pxx = welch(x, fs=fs, nperseg=int(4 * fs), axis=1)
    band = (f >= 4) & (f <= 13)
    cog = float(np.median((pxx[:, band] * f[band]).sum(1) / pxx[:, band].sum(1)))

    win = int(10 * fs)
    acw = []
    for ch in x:
        segs = ch[: len(ch) // win * win].reshape(-1, win)
        ac = np.mean([acf_fft(s) for s in segs], axis=0)
        acw.append(first_crossing(ac, 0.5, 1000 / fs))

    sos = butter(4, [max(cog - 2, 1.0), cog + 2], btype="band", fs=fs, output="sos")
    filt = sosfiltfilt(sos, x, axis=1)
    n = filt.shape[1]
    env = np.abs(hilbert(filt, N=next_fast_len(n), axis=1))[:, :n]
    step = int(fs // 50)  # envelope at 50 Hz
    env = env[:, : n // step * step].reshape(len(env), -1, step).mean(2)
    env = env[:, 100:-100]  # drop filter edges (2 s each side)
    tau = [first_crossing(acf_fft(e), 1 / np.e, 1 / 50) for e in env]
    cv = env.std(1) / env.mean(1)
    return {
        "peak_cog": cog,
        "acw50_ms": float(np.nanmedian(acw)),
        "env_tau_s": float(np.nanmedian(tau)),
        "env_cv": float(np.median(cv)),
    }


def cohen_d(a: np.ndarray, b: np.ndarray) -> float:
    sp = np.sqrt(
        ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2)
    )
    return float((a.mean() - b.mean()) / sp)


def adjusted_d(y, is_patient, covars) -> float:
    """Group coefficient from y ~ group + covariates, in units of the residual SD."""
    design = np.column_stack([np.ones(len(y)), is_patient, covars])
    beta, *_ = np.linalg.lstsq(design, y, rcond=None)
    resid = y - design @ beta
    return float(beta[1] / resid.std(ddof=design.shape[1]))


def boot_ci(fn, n: int, rng, reps: int = 2000) -> tuple[float, float]:
    vals = [fn(rng.integers(0, n, n)) for _ in range(reps)]
    lo, hi = np.nanpercentile(vals, [2.5, 97.5])
    return float(lo), float(hi)


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    root = Path(sys.argv[1])
    with open(root / "participants.tsv", newline="") as fh:
        people = list(csv.DictReader(fh, delimiter="\t"))
    rows = []
    for p in people:
        pid = p["participant_id"]
        rec = root / "derivatives" / pid / "eeg" / f"{pid}_task-eyesclosed_eeg.set"
        vals = person_measures(rec)
        vals.update(group=p["Group"], age=float(p["Age"]), male=float(p["Gender"] == "M"))
        rows.append(vals)

    names = {"A": "Alzheimer's", "F": "frontotemporal", "C": "controls"}
    print(
        f"People analysed: {len(rows)}  "
        + ", ".join(f"{names[g]} n={sum(r['group'] == g for r in rows)}" for g in "AFC")
    )
    print("\nGroup means (SD):")
    print(f"  {'measure':<10}" + "".join(f"{names[g]:>22}" for g in "AFC"))
    for k in MEASURES:
        cells = []
        for g in "AFC":
            v = np.array([r[k] for r in rows if r["group"] == g])
            cells.append(f"{v.mean():.3g} ({v.std(ddof=1):.2g})")
        print(f"  {k:<10}" + "".join(f"{c:>22}" for c in cells))

    rng = np.random.default_rng(0)
    for g in "AF":
        sub = [r for r in rows if r["group"] in (g, "C")]
        pat = np.array([r["group"] == g for r in sub], dtype=float)
        age = np.array([r["age"] for r in sub])
        male = np.array([r["male"] for r in sub])
        cog = np.array([r["peak_cog"] for r in sub])
        print(f"\n{names[g]} minus controls (n={len(sub)}): Cohen's d [95% bootstrap interval]")
        print(
            f"  {'measure':<10}{'unadjusted':>24}{'adjusted: age, sex':>26}{'+ peak frequency':>26}"
        )
        for k in MEASURES:
            y = np.array([r[k] for r in sub])

            def raw(i, y=y, pat=pat):
                return cohen_d(y[i][pat[i] == 1], y[i][pat[i] == 0])

            def adj1(i, y=y, pat=pat, age=age, male=male):
                return adjusted_d(y[i], pat[i], np.column_stack([age[i], male[i]]))

            def adj2(i, y=y, pat=pat, age=age, male=male, cog=cog):
                return adjusted_d(y[i], pat[i], np.column_stack([age[i], male[i], cog[i]]))

            idx = np.arange(len(sub))
            cells = []
            for fn in (raw, adj1) + ((adj2,) if k != "peak_cog" else ()):
                lo, hi = boot_ci(fn, len(sub), rng)
                cells.append(f"{fn(idx):+.2f} [{lo:+.2f}, {hi:+.2f}]")
            widths = (24, 26, 26)
            print(f"  {k:<10}" + "".join(f"{c:>{w}}" for c, w in zip(cells, widths, strict=False)))

    print("\nHow to read this: positive d = larger in patients. acw50_ms and env_tau_s are")
    print("timescales (critical slowing down predicts positive; neuron-loss 'subcritical drift'")
    print("predicts negative); env_cv is variability. The last column removes the part explained")
    print("by plain EEG slowing. Symptomatic single-site data: shows the sign at the dementia")
    print("stage only, and says nothing about the years before symptoms.")


if __name__ == "__main__":
    main()
