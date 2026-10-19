"""
open-ad-sim — a 10-region model of the Alzheimer's disease process (v6).

WHAT THIS IS: a disease-process model of a TYPE of brain (see profiles/), not a simulation of any person's brain.
It tracks, in 10 regions wired along the routes tau spreads in humans:
  A  amyloid (Centiloid; one value per person — plaque is diffuse across cortex)
  T  tau tangle burden per region (0 = none, 1 = maximal)
  N  fraction of neurons still alive per region (1 = none lost)            -> loss is permanent
  S  functional integrity of the SURVIVING neurons per region (synapses,
     activity; 1 = normal)                                                 -> can recover in principle
Cognition (CDR-SB) is computed from network function F = N x S with a reserve threshold.

EQUATIONS (per person, per region r; time in years):
  amyloid:   dA/dt = rA (A+15)(1-(A+15)/(Amax+15))  - k_ab (A - 5)   [antibody term while on]
  h(A)     = A^4/(A^4 + 45^4)       amyloid "permission" for tau growth/spread (switches on ~35-65 CL)
  age:       tau growth/spread and tau-driven neuron death scale with exp(0.046*(age-70)) (rates double per 15 y)
  tau:       dT_r/dt = [ (k0*m0_r + kA*h*mA_r + kauto*T_r) T_r + (b0 + bA*h) sum_j W_rj T_j ] (1 - T_r)(1 - tau_block)
             k0 = age-related (medial temporal) growth; kA = amyloid-driven growth;
             kauto = self-propagation once tau is established; b0, bA = spread without / with amyloid
  neurons:   dN_r/dt = - delta * vuln_r * T_r^pN * N_r  - LATE_r(t) * N_r   (pN calibrated)
             LATE = TDP-43 co-pathology: present in a fraction of people, adds medial temporal neuron loss
  survivors: S*_r = 1 / (1 + sT*T_r + sA*amy_r*O + sD*Din_r),  O = A/100 (soluble amyloid proxy),
             Din_r = sum_j Wn_rj (1 - N_j)  (inputs lost because upstream neurons died: disconnection)
             dS_r/dt = k_down (S*_r - S_r) if S_r > S*_r  else  rho (S*_r - S_r)     [rho = recovery capacity]
  cognition: D = 1 - sum_r w_r N_r S_r ;  CDR_AD = a * f_res * max(D - R, 0)^q  (R = reserve; f_res = person-level
             resilience, lognormal with SD sdres) ;  CDR = CDR_AD + eps
  v6: tau self-propagation kauto also varies between people (lognormal, SD hetK); added after v5 failed an
      out-of-sample check (progression of amyloid+/tau+ MCI too fast and too uniform: 92-98% vs 70% at 5 years)
             eps = non-Alzheimer contributors (sleep, medication, mood, hearing...) — fully reversible
"""
import numpy as np

REG = ["EC", "HC", "PHG", "IT", "LT", "PCC", "IP", "PFC", "OCC", "PRIM"]
REG_LONG = ["Entorhinal cortex", "Hippocampus (CA1/subiculum)", "Parahippocampal/amygdala",
            "Inferior temporal/fusiform", "Lateral temporal", "Posterior cingulate/precuneus",
            "Inferior parietal", "Prefrontal", "Occipital association", "Primary sensory/motor"]
R = len(REG)
IX = {r: i for i, r in enumerate(REG)}

EDGES = {("EC", "HC"): 1.0, ("EC", "PHG"): 0.8, ("HC", "PHG"): 0.5, ("PHG", "IT"): 0.8, ("EC", "IT"): 0.3,
         ("IT", "LT"): 0.8, ("HC", "PCC"): 0.4, ("PHG", "PCC"): 0.4, ("LT", "IP"): 0.6, ("PCC", "IP"): 0.7,
         ("PCC", "PFC"): 0.6, ("LT", "PFC"): 0.5, ("IP", "OCC"): 0.6, ("IT", "OCC"): 0.4,
         ("PFC", "PRIM"): 0.4, ("OCC", "PRIM"): 0.5, ("IP", "PRIM"): 0.4}
W = np.zeros((R, R))
for (a, b), w in EDGES.items():
    W[IX[a], IX[b]] = W[IX[b], IX[a]] = w
WN = W / W.sum(1, keepdims=True)

W_COG = np.array([.18, .22, .10, .08, .10, .10, .07, .10, .03, .02]); W_COG = W_COG / W_COG.sum()
M0 = np.array([1.0, 0.8, 0.3, 0.06, 0.03, 0.03, 0.02, 0.02, 0.01, 0.0])
# amyloid-driven tau growth is demonstrable in medial/inferior temporal cortex (lecanemab slowed MTL/meta-temporal tau);
# established neocortical tau accumulates largely independently of amyloid (no frontal/parietal slowing in TRAILBLAZER-ALZ 2)
MA = np.array([1, 1, 1, 0.8, 0.5, 0.4, 0.3, 0.3, 0.2, 0.1])
VULN = np.array([1.5, 1.4, 1.1, 1.0, 0.9, 0.8, 0.8, 0.8, 0.6, 0.3])
AMY = np.array([.4, .4, .6, .8, 1.0, 1.2, 1.1, 1.1, .8, .4])
LATE_M = np.array([0.5, 1.0, 0.6, 0.1, 0, 0, 0, 0.05, 0, 0])   # TDP-43: amygdala/hippocampus -> EC -> temporal/frontal
# tau-PET definitions, fixed before calibration from Braak correspondence:
#   temporal meta-ROI positivity corresponds to Braak >= IV-like spread (IT/LT tau), not EC tau alone
POS_IDX = [IX["IT"], IX["LT"]]
NEO = [IX[r] for r in ["IP", "PFC", "OCC"]]
TAU_POS, TAU_HIGH = 0.15, 0.12
A50, A_SHIFT, A_FLOOR, K_DOWN = 45.0, 15.0, 5.0, 2.0
LATE_P, LATE_RATE = 0.25, 0.04   # [assumption] TDP-43 (LATE) co-pathology in ~25% of this age band; ~4%/yr medial temporal loss once present
GAMMA_AGE = np.log(2) / 15.0     # [assumption] downstream (tau, neuron-loss) rates double every 15 years of age

# Structural variants for the uncertainty ensemble (set ADSIM_VARIANT before import; recorded in each calibration file)
import os
VARIANT = os.environ.get("ADSIM_VARIANT", "base")
if VARIANT == "flatcog":      # everyday cognition less dependent on medial temporal memory circuits
    W_COG = np.array([.12, .14, .10, .10, .10, .10, .09, .12, .07, .06]); W_COG = W_COG / W_COG.sum()
elif VARIANT == "nolate":     # no TDP-43 co-pathology
    LATE_P = 0.0
elif VARIANT == "late40":     # more co-pathology (upper range of autopsy series)
    LATE_P = 0.40

def require_variant(cal, source="calibration file"):
    """Stop if a fitted member is run under a structural variant it was not fitted with.

    VARIANT is fixed at import time from ADSIM_VARIANT, so running e.g. a 'flatcog' member without
    ADSIM_VARIANT=flatcog would silently simulate the wrong model. run_ensemble.py sets it per member.
    """
    want = cal.get("variant", "base")
    if want != VARIANT:
        raise SystemExit(f"{source} was fitted with ADSIM_VARIANT={want}, but this process has "
                         f"ADSIM_VARIANT={VARIANT}. Re-run with ADSIM_VARIANT={want}, or use "
                         "model/run_ensemble.py, which sets it for every member.")


DEFAULT_G = dict(pN=2.0, thr_pos=0.15, thr_hi=0.12, k0=0.10, kA=0.12, kauto=0.40, b0=0.01, bA=0.05, delta=0.12,
                 sT=0.10, sA=0.25, sD=0.15, a_cdr=100.0, q=2.0, R0=0.15, rho=0.5, het=0.35, sdR=0.05, hetK=0.3, sdres=0.3)


def sample_people(P, seed=0):
    """Standard-normal draws per person (common random numbers); realised by realize()."""
    rng = np.random.default_rng(seed)
    z = {k: rng.standard_normal(P) for k in ("rA", "Amax", "seed", "k0", "kA", "bA", "del", "sT", "R")}
    z["A0"] = rng.uniform(-15, 10, P)
    u = rng.random(P)
    z["eps"] = np.where(u < 0.30, rng.uniform(0.25, 1.0, P), 0.0)     # reversible non-AD contributors [assumption]
    z["late_on"] = np.where(rng.random(P) < LATE_P, rng.uniform(68, 88, P), np.inf)
    # v6: drawn last so that every earlier draw is unchanged (common random numbers across model versions)
    z["kauto"] = rng.standard_normal(P)     # person-to-person variation in tau self-propagation
    z["res"] = rng.standard_normal(P)       # person-to-person variation in resilience (symptoms per unit of network damage)
    return z


def realize(z, g):
    h = g.get("het", 0.35)
    return dict(
        rA=0.13 * np.exp(0.25 * z["rA"]), Amax=115 + 15 * z["Amax"], A0=z["A0"].copy(),
        seed=0.01 * np.exp(0.7 * z["seed"]),
        fk0=np.exp(h * z["k0"]), fkA=np.exp(h * z["kA"]), fbA=np.exp(h * z["bA"]),
        fdel=np.exp(h * z["del"]), fsT=np.exp(h * z["sT"]),
        R=np.clip(g["R0"] + g.get("sdR", 0.05) * z["R"], 0, None),
        eps=z["eps"].copy(), late_on=z["late_on"].copy(),
        fka=np.exp(g.get("hetK", 0.0) * z["kauto"]) if "kauto" in z else np.ones(len(z["rA"])),
        fres=np.exp(g.get("sdres", 0.0) * z["res"]) if "res" in z else np.ones(len(z["rA"])))


def subset(pp, mask):
    return {k: v[mask] for k, v in pp.items()}


def init_state(pp, age0=48.0):
    P = len(pp["rA"])
    T = np.zeros((P, R)); T[:, IX["EC"]] = pp["seed"]; T[:, IX["HC"]] = 0.5 * pp["seed"]
    return dict(A=pp["A0"].copy(), T=T, N=np.ones((P, R)), S=np.ones((P, R)), age=np.full(P, age0))


def copy_state(st):
    return {k: v.copy() for k, v in st.items()}


def step(st, pp, g, dt, ab_k=None, tau_block=0.0, fix_local=0.0, fix_disc=0.0, rho_mult=1.0, S_floor=None, stop_neuron=0.0):
    A, T, N, S = st["A"], st["T"], st["N"], st["S"]
    a = A + A_SHIFT
    amax = pp["Amax"] + A_SHIFT
    A_new = A + pp["rA"] * a * (1 - a / amax) * dt
    if ab_k is not None:
        A_new = A_FLOOR + (A_new - A_FLOOR) * np.exp(-ab_k * dt)
    Ap = np.clip(A, 0, None)
    h = (Ap ** 4 / (Ap ** 4 + A50 ** 4))[:, None]
    fa = np.exp(GAMMA_AGE * (st["age"] - 70.0))[:, None]
    grow = fa * (g["k0"] * pp["fk0"][:, None] * M0 + g["kA"] * pp["fkA"][:, None] * h * MA + g["kauto"] * pp["fka"][:, None] * T) * T
    spread = fa * (g["b0"] + g["bA"] * pp["fbA"][:, None] * h) * (T @ W)
    tb = tau_block if np.ndim(tau_block) == 0 else tau_block[:, None]
    T_new = np.clip(T + (grow + spread) * (1 - T) * (1 - tb) * dt, 0, 1)
    late = ((st["age"] >= pp["late_on"])[:, None] * LATE_RATE * LATE_M)
    sn = stop_neuron
    N_new = N * np.exp(-(1 - sn) * (fa * g["delta"] * pp["fdel"][:, None] * VULN * T ** g.get("pN", 2.0) + late) * dt)   # exact step
    O = (Ap / 100.0)[:, None]
    Din = (1 - N) @ WN.T
    fl = fix_local if np.ndim(fix_local) == 0 else fix_local[:, None]
    fd = fix_disc if np.ndim(fix_disc) == 0 else fix_disc[:, None]
    insult = (1 - fl) * (g["sT"] * pp["fsT"][:, None] * T + g["sA"] * AMY * O) + (1 - fd) * g["sD"] * Din
    S_tgt = 1.0 / (1.0 + insult)
    rm = rho_mult if np.ndim(rho_mult) == 0 else rho_mult[:, None]
    rate = np.where(S > S_tgt, K_DOWN, g["rho"] * rm)
    S_new = S_tgt + (S - S_tgt) * np.exp(-rate * dt)                                                     # exact relaxation step (stable)
    if S_floor is not None:
        S_new = np.maximum(S_new, S_floor)
    st["A"], st["T"], st["N"], st["S"] = A_new, T_new, N_new, np.clip(S_new, 0, 1)
    st["age"] = st["age"] + dt
    return st


def cognition(st, pp, g, include_eps=True, N=None, S=None):
    N = st["N"] if N is None else N
    S = st["S"] if S is None else S
    D = 1 - (N * S) @ W_COG
    c = np.minimum(g["a_cdr"] * pp["fres"] * np.clip(D - pp["R"], 0, None) ** g["q"], 18.0)
    return c + (pp["eps"] if include_eps else 0.0)


def tau_status_arr(T, g=None):
    """T (..., R) -> (tau-PET temporal positive, high/neocortical tau). Thresholds map model tau to PET cut-points
    and are calibrated (g['thr_pos'], g['thr_hi']) because model tau units are arbitrary."""
    tp = g.get("thr_pos", TAU_POS) if g else TAU_POS
    th = g.get("thr_hi", TAU_HIGH) if g else TAU_HIGH
    return T[..., POS_IDX].mean(-1) > tp, T[..., NEO].mean(-1) > th


def run_history(pp, g, age0=48.0, age1=90.0, dt=0.1, rec=0.5):
    st = init_state(pp, age0)
    P = len(pp["rA"])
    nrec = int(round((age1 - age0) / rec)) + 1
    ages = age0 + rec * np.arange(nrec)
    out = dict(A=np.zeros((P, nrec), np.float32), T=np.zeros((P, nrec, R), np.float32),
               N=np.zeros((P, nrec, R), np.float32), S=np.zeros((P, nrec, R), np.float32))
    per = int(round(rec / dt))
    for k in range(nrec):
        out["A"][:, k] = st["A"]; out["T"][:, k] = st["T"]; out["N"][:, k] = st["N"]; out["S"][:, k] = st["S"]
        if k < nrec - 1:
            for _ in range(per):
                step(st, pp, g, dt)
    return ages, out


def run_to(pp, g, age0=48.0, age1=75.0, dt=0.1):
    st = init_state(pp, age0)
    for _ in range(int(round((age1 - age0) / dt))):
        step(st, pp, g, dt)
    return st


def state_at(hist, k_idx, ages):
    P = hist["A"].shape[0]
    r = np.arange(P)
    return dict(A=hist["A"][r, k_idx].astype(float), T=hist["T"][r, k_idx].astype(float),
                N=hist["N"][r, k_idx].astype(float), S=hist["S"][r, k_idx].astype(float), age=ages[k_idx].astype(float))


def antibody_rates(P, kind, rng):
    if kind == "donanemab":
        return 2.28 * np.exp(0.84 * rng.standard_normal(P))     # Model B fit to TB-ALZ 2 clearance
    if kind == "lecanemab":
        return 1.08 * np.exp(0.87 * rng.standard_normal(P))     # Model B fit to Clarity AD
    raise ValueError(kind)


def project(st0, pp, g, years, dt=0.05, rec=0.25, scen=None, seed=1, keep=False):
    """Run forward from a state under a scenario. scen keys:
       ab: None|'donanemab'|'lecanemab'; ab_start (yr); ab_stop_rule (default True for donanemab: stop when <11 CL at 6/12/18-mo scans, max 18 mo)
       tau_block (0-1) from tau_start; fix_local / fix_disc (0-1: share of survivor insult removed) from fix_start;
       rho_mult (recovery capacity multiplier) from fix_start; S_one: survivors held at full function from fix_start (ceiling);
       stop_neuron (0-1) from tau_start; eps_fix_at: time non-AD contributors are removed
    """
    scen = scen or {}
    rng = np.random.default_rng(seed)
    st = copy_state(st0)
    P = len(pp["rA"])
    nrec = int(round(years / rec)) + 1
    per = int(round(rec / dt))
    times = rec * np.arange(nrec)
    cdr = np.zeros((P, nrec)); cdr_ad = np.zeros((P, nrec)); Atr = np.zeros((P, nrec))
    if keep:
        Ntr = np.zeros((P, nrec, R)); Str = np.zeros((P, nrec, R)); Ttr = np.zeros((P, nrec, R))
    ab = scen.get("ab"); ab_start = scen.get("ab_start", 0.0)
    kab = antibody_rates(P, ab, rng) if ab else None
    stopped = np.zeros(P, bool)
    stop_rule = scen.get("ab_stop_rule", ab == "donanemab")
    eps_fix_at = scen.get("eps_fix_at", None)
    pp_now = dict(pp)
    t = 0.0
    for k in range(nrec):
        cdr[:, k] = cognition(st, pp_now, g); cdr_ad[:, k] = cognition(st, pp_now, g, include_eps=False)
        Atr[:, k] = st["A"]
        if keep:
            Ntr[:, k] = st["N"]; Str[:, k] = st["S"]; Ttr[:, k] = st["T"]
        if k == nrec - 1:
            break
        for _ in range(per):
            if eps_fix_at is not None and t >= eps_fix_at - 1e-9:
                pp_now["eps"] = np.zeros(P)
            ab_k = None
            if ab:
                started = t >= ab_start - 1e-9
                on = started & ~stopped
                if stop_rule:
                    tt = t - ab_start
                    for scan in (0.5, 1.0, 1.5):
                        if abs(tt - scan) < dt / 2:
                            stopped |= on & (st["A"] < 11.0)
                    if tt >= 1.5 - 1e-9:
                        stopped |= on
                    on = started & ~stopped
                ab_k = np.where(on, kab, 0.0)
            ts = scen.get("tau_start", 0.0)
            tb = scen.get("tau_block", 0.0) if t >= ts - 1e-9 else 0.0
            sn = scen.get("stop_neuron", 0.0) if t >= ts - 1e-9 else 0.0
            fs = scen.get("fix_start", 0.0)
            fl = scen.get("fix_local", 0.0) if t >= fs - 1e-9 else 0.0
            fd = scen.get("fix_disc", 0.0) if t >= fs - 1e-9 else 0.0
            rm_on = scen.get("rho_abs", None)
            rm_on = (rm_on / g["rho"]) if rm_on is not None else scen.get("rho_mult", 1.0)
            rm = rm_on if t >= fs - 1e-9 else 1.0
            S_floor = 1.0 if (scen.get("S_one") and t >= fs - 1e-9) else None
            step(st, pp_now, g, dt, ab_k=ab_k, tau_block=tb, fix_local=fl, fix_disc=fd, rho_mult=rm,
                 S_floor=S_floor, stop_neuron=sn)
            t += dt
    out = dict(t=times, cdr=cdr, cdr_ad=cdr_ad, A=Atr, final=st)
    if keep:
        out.update(N=Ntr, S=Str, T=Ttr)
    return out
