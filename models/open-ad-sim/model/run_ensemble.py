"""
Run every ensemble member for one profile (or a local patient file), pool them, and write a results summary.

  python3 model/run_ensemble.py --profile mci_moderate_amyloid_70s                 # writes docs/RESULTS_<profile>.md
  python3 model/run_ensemble.py --patient patients/my_relative.yaml                 # writes results/RESULTS_local.md (git-ignored)

Each member is run with its own structural variant (ADSIM_VARIANT), read from its calibration file in ensemble/.
"""
import argparse, glob, json, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def pct(x):
    return f"{100 * x:.0f}%"


def prange(a, b):
    a, b = round(100 * min(a, b)), round(100 * max(a, b))
    return f"{a}%" if a == b else f"{a}–{b}%"


def yr(x):
    return "beyond 10" if not np.isfinite(x) else f"{x:.1f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default="mci_moderate_amyloid_70s")
    ap.add_argument("--patient", default=None)
    ap.add_argument("--P", type=int, default=150000)
    ap.add_argument("--jobs", type=int, default=2)
    a = ap.parse_args()
    members = sorted(glob.glob(os.path.join(ROOT, "ensemble", "calib_*.json")))
    if not members:
        sys.exit("no ensemble members in ensemble/ — fit some with model/calibrate.py first")
    name = "local" if a.patient else a.profile
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    outs, procs = [], []
    for m in members:
        variant = json.load(open(m)).get("variant", "base")
        tag = os.path.basename(m).replace("calib_", "").replace(".json", "")
        out = os.path.join(ROOT, "results", f"scen_{name}_{tag}.json")
        outs.append(out)
        cmd = [sys.executable, os.path.join(HERE, "scenarios.py"), "--calib", m, "--P", str(a.P), "--out", out]
        cmd += ["--patient", a.patient] if a.patient else ["--profile", a.profile]
        env = dict(os.environ, ADSIM_VARIANT=variant)
        procs.append(subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        while sum(p.poll() is None for p in procs) >= a.jobs:
            procs[[p.poll() is None for p in procs].index(True)].wait()
    for p in procs:
        p.wait()
    pooled = os.path.join(ROOT, "results", f"pooled_{name}.json")
    subprocess.run([sys.executable, os.path.join(HERE, "pool.py"), pooled] + outs, check=True, stdout=subprocess.DEVNULL)
    P = json.load(open(pooled))
    T, D, W = P["traj"], P["decomposition"], P["window"]
    L = [f"# Results — {name}", "",
         "*Modeled hypotheses for virtual patients who fit the profile's ranges; not predictions for any person. "
         f"{len(P['members'])} ensemble members, equal weight.*", "",
         "## Where the impairment sits", "",
         "| Group | Share of matches | In neurons already lost (range across methods and members) |", "|---|---|---|"]
    for g, lab in (("all", "All"), ("tau_neg", "Tau PET negative"), ("tau_pos", "Tau PET positive"), ("tau_high", "Widespread tau"),
                   ("stereo", "Autopsy-like entorhinal loss")):
        if g in D and D[g]["low"] is not None:
            L.append(f"| {lab} | {pct(D[g]['share'])} | {prange(D[g]['low'], D[g]['high'])} |")
    L += ["", "## Course under each treatment class (Alzheimer part of CDR-SB)", "",
          "| Scenario | Median years to mild dementia | Members | Mild dementia within 5 years | Truly better than today at 1 year |",
          "|---|---|---|---|---|"]
    for k, r in T.items():
        lo, hi = r["member_range_years_to_mild"]
        L.append(f"| {k} | {yr(r['years_to_mild_median'])} | {yr(lo)}–{yr(hi)} | {pct(r['p_mild_5y'])} | {pct(r['better_y1'])} |")
    L += ["", "## The window: best possible if every surviving neuron were restored at that time", "",
          "| Repair starts | Impairment then (untreated) | Best possible (untreated until then) | Best possible (antibody now) |", "|---|---|---|---|"]
    for s in sorted(W, key=int):
        n, b = W[s].get("none"), W[s].get("ab_now")
        L.append(f"| +{s} yr | {n['cad_median']:.2f} | {n['best_low']:.2f}–{n['best_high']:.2f} | {b['best_low']:.2f}–{b['best_high']:.2f} |")
    L += ["", "Ranges are across two symptom mappings (model and linear). See docs/VALIDATION.md for what the model reproduces and where it fails."]
    dest = os.path.join(ROOT, "results", "RESULTS_local.md") if a.patient else os.path.join(ROOT, "docs", f"RESULTS_{name}.md")
    open(dest, "w").write("\n".join(L) + "\n")
    print("wrote", dest)


if __name__ == "__main__":
    main()
