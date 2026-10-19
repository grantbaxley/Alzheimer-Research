"""
Pool ensemble members (equal weight) for one profile and summarize: trajectories, decomposition ranges, window, conditional table.
Ranges across members are reported alongside pooled values (structural uncertainty).
Usage: python3 model/pool.py results/pooled_<profile>.json results/scen_<profile>_A.json results/scen_<profile>_B.json ...
"""
import numpy as np, json, sys

TRAJ = ["none", "ab_now", "lec_now", "ab_1y", "ab_2y", "ab_tauhalf_3y", "ab_tauhalf_now", "ab_taustop_now",
        "ab_freeze_now", "ab_freeze_repair", "ab_freeze_fastrepair", "ceiling_now", "fix_nonAD"]


def main(out_path, paths, per_member=3000):
    members, P = [], {}
    for j, p in enumerate(paths):
        res = json.load(open(p)); arr = dict(np.load(p.replace(".json", ".npz")))
        n = len(arr["cad"]); rng = np.random.default_rng(j)
        idx = rng.choice(n, size=min(per_member, n), replace=False)
        for k, v in arr.items():
            P.setdefault(k, []).append(v[idx])
        members.append(dict(path=p, variant=res.get("variant", "base"), rho=res["g"]["rho"], q=res["g"]["q"], loss=res["loss"], n=n,
                            profile=res["profile"], composition=res["survivor_insult_composition"],
                            decomposition=res["decomposition"],
                            years_to_mild={k: res["scenarios"][k]["years_to_mild_dementia_median"] for k in TRAJ},
                            window=res["window"]))
        t = np.array(res["t"])
    P = {k: np.concatenate(v) for k, v in P.items()}
    out = {"n": int(len(P["cad"])), "members": members, "t": t.tolist()}
    # ---- trajectories (pooled) ----
    out["traj"] = {}
    for k in TRAJ:
        c = P[f"traj_{k}"]; base = P["cad"] if k != "fix_nonAD" else P["cad"] + P["eps"]
        crossed = c >= 4.5
        yrs = np.where(crossed.any(1), t[crossed.argmax(1)], np.inf)
        out["traj"][k] = dict(
            series=[dict(year=float(t[i]), p25=float(np.percentile(c[:, i], 25)), p50=float(np.median(c[:, i])),
                         p75=float(np.percentile(c[:, i], 75))) for i in range(0, len(t), 2)],
            years_to_mild_median=float(np.median(yrs)), years_to_mild_p25=float(np.percentile(yrs, 25)),
            years_to_mild_p75=float(np.percentile(yrs, 75)), p_mild_5y=float((yrs <= 5).mean()),
            better_y1=float((c[:, 4] < base - 0.5).mean()), better_y2=float((c[:, 8] < base - 0.5).mean()),
            member_range_years_to_mild=[float(min(m["years_to_mild"][k] for m in members)), float(max(m["years_to_mild"][k] for m in members))],
            by_tau={})
        for lab, msk in (("tau_neg", ~P["taupos"]), ("tau_pos", P["taupos"] & ~P["hitau"]), ("tau_high", P["hitau"])):
            if msk.sum() >= 30:
                cc = c[msk]; cr = cc >= 4.5
                yy = np.where(cr.any(1), t[cr.argmax(1)], np.inf)
                out["traj"][k]["by_tau"][lab] = dict(years_to_mild_median=float(np.median(yy)), n=int(msk.sum()),
                                                     y3=float(np.median(cc[:, 12])), y5=float(np.median(cc[:, 20])))
    # ---- decomposition: ranges across methods, mappings and members ----
    groups = {"all": np.ones(len(P["cad"]), bool), "tau_neg": ~P["taupos"], "tau_pos": P["taupos"] & ~P["hitau"],
              "tau_high": P["hitau"], "stereo": P["stereo"]}
    dec = {}
    for gname, msk in groups.items():
        if msk.sum() < 30:
            continue
        cad = P["cad"][msk]
        shares = {meth: float(P[meth][msk].sum() / cad.sum()) for meth in ("remainder_N", "shapley_N", "prop_N")}
        mname = "tau_pos_low" if gname == "tau_pos" else gname      # group name used in the per-member files
        mem_shapley = [m["decomposition"].get(mname, {}).get("share_neurons_shapley_N") for m in members]
        mem_prop = [m["decomposition"].get(mname, {}).get("share_neurons_prop_N") for m in members]
        vals = [v for v in mem_shapley + mem_prop if v is not None]
        dec[gname] = dict(n=int(msk.sum()), share=float(msk.mean()), cdr_ad_mean=float(cad.mean()), **{f"pooled_{k}": v for k, v in shares.items()},
                          low=float(min(vals)) if vals else None, high=float(max(vals)) if vals else None,
                          mid=float(np.median(vals)) if vals else None,
                          p_below05_model=float((P["remainder_N"][msk] < 0.5).mean()),
                          p_below05_linear=float((P["prop_N"][msk] < 0.5).mean()))
    out["decomposition"] = dec
    # ---- conditional table: what each pending test result would mean ----
    tot = P["cad"] + P["eps"]
    tau_lab = np.where(P["hitau"], "high", np.where(P["taupos"], "positive", "negative"))
    cdr_lab = np.where(tot < 1.25, "0.5-1.0", "1.5-2.5")
    hc_lab = np.where(P["N_HC"] >= 0.8, "hc_mild_loss", np.where(P["N_HC"] >= 0.65, "hc_moderate_loss", "hc_marked_loss")) if "N_HC" in P else None

    def ytm(c):
        cr = c >= 4.5
        return np.where(cr.any(1), t[cr.argmax(1)], np.inf)

    cond = []
    keys = [("tau", tau_lab), ("cdr", cdr_lab)] + ([("hc", hc_lab)] if hc_lab is not None else [])
    combos = [("tau",), ("cdr",), ("hc",), ("cdr", "tau"), ("hc", "tau")]
    lab = dict(keys)
    for combo in combos:
        if any(c not in lab for c in combo):
            continue
        vals = sorted(set(zip(*[lab[c] for c in combo])))
        for v in vals:
            msk = np.ones(len(tot), bool)
            for c, vv in zip(combo, v):
                msk &= lab[c] == vv
            if msk.sum() < 60:
                continue
            cad = P["cad"][msk]
            y0 = ytm(P["traj_none"][msk]); y1 = ytm(P["traj_ab_now"][msk])
            cond.append(dict(by="+".join(combo), value="+".join(v), n=int(msk.sum()), share_of_cohort=float(msk.mean()),
                             cdr_ad_mean=float(cad.mean()),
                             lost_share_prop=float(P["prop_N"][msk].sum() / cad.sum()),
                             lost_share_shapley=float(P["shapley_N"][msk].sum() / cad.sum()),
                             lost_share_remainder=float(P["remainder_N"][msk].sum() / cad.sum()),
                             best_possible_model=float(P["remainder_N"][msk].mean()), best_possible_linear=float(P["prop_N"][msk].mean()),
                             years_to_mild_none=float(np.median(y0)), years_to_mild_ab=float(np.median(y1)),
                             p_mild_5y_none=float((y0 <= 5).mean()), p_mild_5y_ab=float((y1 <= 5).mean())))
    out["conditional"] = cond
    # ---- window ----
    win = {}
    for s0 in range(0, 7):
        row = {}
        for b in ("ab_now", "none"):
            bm = P.get(f"win_{b}_{s0}_bestmodel"); bl = P.get(f"win_{b}_{s0}_bestlin"); ca = P.get(f"win_{b}_{s0}_cad")
            if bm is None:
                continue
            row[b] = dict(cad_median=float(np.median(ca)), best_model_median=float(np.median(bm)), best_lin_median=float(np.median(bl)),
                          best_model_mean=float(bm.mean()), best_lin_mean=float(bl.mean()),
                          best_low=float(min(np.median(bm), np.median(bl))), best_high=float(max(np.median(bm), np.median(bl))))
        win[str(s0)] = row
    out["window"] = win
    json.dump(out, open(out_path, "w"), indent=1)
    print("n", out["n"])
    for m in members:
        print(f"member {m['path']}: variant {m['variant']} rho {m['rho']} q {m['q']:.2f} loss {m['loss']:.1f} n {m['n']} "
              f"composition tau/amy/disc {m['composition']['tau']:.2f}/{m['composition']['amyloid']:.2f}/{m['composition']['disconnection']:.2f}")
    for k in TRAJ:
        r = out["traj"][k]
        print(f"{k:22s} to CDR-SB 4.5: {r['years_to_mild_median']:.1f}y (IQR {r['years_to_mild_p25']:.1f}-{r['years_to_mild_p75']:.1f}; members {r['member_range_years_to_mild']}) "
              f"better y1 {r['better_y1']:.2f}")
    for gname, d in dec.items():
        print(f"decomp {gname:9s} n {d['n']:5d} share-in-dead-neurons: remainder {d['pooled_remainder_N']:.2f} shapley {d['pooled_shapley_N']:.2f} "
              f"prop {d['pooled_prop_N']:.2f} | member range {d['low']:.2f}-{d['high']:.2f} | P(<0.5 if restored) model {d['p_below05_model']:.2f} linear {d['p_below05_linear']:.2f}")
    for s0, row in win.items():
        print(f"window +{s0}: " + " | ".join(f"{b}: AD now {v['cad_median']:.2f}, best {v['best_low']:.2f}-{v['best_high']:.2f}" for b, v in row.items()))
    for c in cond:
        print(f"cond {c['by']:8s} {c['value']:28s} n {c['n']:5d} ({c['share_of_cohort']:.2f}) AD {c['cdr_ad_mean']:.2f} lost-share "
              f"prop {c['lost_share_prop']:.2f} shap {c['lost_share_shapley']:.2f} rem {c['lost_share_remainder']:.2f} | to mild: none "
              f"{c['years_to_mild_none']:.1f} ab {c['years_to_mild_ab']:.1f} | P(mild 5y) {c['p_mild_5y_none']:.2f}->{c['p_mild_5y_ab']:.2f}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
