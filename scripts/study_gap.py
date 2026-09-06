"""Confirmatory script for study task-set-gap (studies/task-set-gap/study.yaml). Evaluates each
prediction's criteria literally and writes results/study_gap/summary.md. The pilot used seed
base 7777; the confirmatory run uses 4242. Run:  uv run python scripts/study_gap.py"""
import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from critpop.branching import optimum_gap, throughput_gap  # noqa: E402
from critpop.landscape import NK  # noqa: E402
from critpop.model import run  # noqa: E402
from critpop.reservoir import run_esn  # noqa: E402

K, N, TOL, R2_FLOOR, N_BOOT = 6, 100, 0.005, 0.5, 200
TS = [250, 500, 1000, 2000, 4000]
GS = [5, 10, 20, 50]
MS = [float(x) for x in np.logspace(-4, -0.5, 25)]
PS = [float(x) for x in np.logspace(-2.2, -0.5, 25)]
KS_ESN, ETAS = [1, 2, 4, 8, 16, 32], [0.001, 0.01, 0.1]
RHOS = [float(x) for x in np.linspace(0.5, 1.25, 31)]
CFG = dict(n_land=8, n_seed=6, n_esn_seed=8, seed_base=4242)
T_G = 1000  # horizon for the ln G sweep; must be in TS


def growth_factor(h, n):
    on = h >= 1
    if not on.any():
        return np.nan
    t0 = int(np.argmax(on)); half = np.where(h >= n / 2)[0]
    t1 = int(half[0]) if half.size else len(h) - 1
    if t1 - t0 < 2:
        return np.nan
    t = np.arange(t0, t1 + 1)
    return float(np.exp(np.polyfit(t, np.log(np.maximum(h[t0:t1 + 1], 1)), 1)[0]))


def loglog_slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(y) & (y > 0)
    return float(np.polyfit(np.log(x[ok]), np.log(y[ok]), 1)[0]) if ok.sum() >= 3 else np.nan


def left_edge(dial, curve, tol=TOL):
    if not np.isfinite(curve).any():
        return float("nan"), 0
    top = np.nanmax(curve); j = int(np.where(curve >= top - tol)[0][0])
    if j == 0:
        return float(dial[0]), 0
    x0, x1, y0, y1 = np.log(dial[j - 1]), np.log(dial[j]), curve[j - 1], curve[j]
    return float(np.exp(x0 + (top - tol - y0) / (y1 - y0) * (x1 - x0))), j


def edge_gap(P, sel, dial):
    curve = np.array([P["perf"][sel & (P["v"] == v)].mean() for v in dial])
    edge, j = left_edge(dial, curve)
    lo, hi = dial[max(j - 1, 0)], dial[j]
    s_lo = np.nanmean(P["sigma"][sel & (P["v"] == lo)]); s_hi = np.nanmean(P["sigma"][sel & (P["v"] == hi)])
    if j == 0 or not np.isfinite(s_lo):
        return edge, s_hi - 1.0
    w = (np.log(edge) - np.log(lo)) / (np.log(hi) - np.log(lo))
    return edge, (1 - w) * s_lo + w * s_hi - 1.0


def pop_task(args):
    topo, T, G, li, cfg = args
    land = NK(20, K, np.random.default_rng([K, li, cfg["seed_base"]]))
    rows, dial = [], (MS if topo == "islands" else PS)
    for si in range(cfg["n_seed"]):
        for v in dial:
            rng = np.random.default_rng([K, li, si, T, G, int(round(v * 1e6)), 41 if topo == "islands" else 42])
            r = run(land, N, 0.0, 0.0, T, rng, islands=G, migration=v) if topo == "islands" else run(land, N, v, 0.0, T, rng)
            rows.append((topo, T, G, li, si, v, float(r.mean_f[-1]), growth_factor(r.holders_traj, N)))
    return rows


def esn_task(args):
    k, eta, n, cfg = args
    rows = []
    for si in range(cfg["n_esn_seed"] if n == 200 else 4):
        for rho in RHOS:
            r = run_esn(rho, k, eta, np.random.default_rng([k, int(eta * 1e6), si, n, cfg["seed_base"]]), n=n)
            rows.append((k, eta, n, si, rho, r.r2, r.sigma_meas))
    return rows


def boot_pop(P, topo, keys, key_name, G_fixed, dial, cfg, rng):
    """Bootstrap over landscapes: per-key gap intervals and the log-log slope interval."""
    lands = np.arange(cfg["n_land"])
    gaps_b, alpha_b = [], []
    for _ in range(N_BOOT):
        pick = rng.choice(lands, cfg["n_land"], replace=True)
        gaps = []
        for kv in keys:
            sel_base = (P["topo"] == topo) & ((P["T"] == kv) if key_name == "T" else ((P["G"] == kv) & (P["T"] == G_fixed)))
            # weight resampled landscapes by multiplicity
            curve = np.zeros(len(dial)); wsum = 0
            for li in pick:
                s = sel_base & (P["land"] == li)
                curve += np.array([P["perf"][s & (P["v"] == v)].mean() for v in dial]); wsum += 1
            curve /= wsum
            edge, j = left_edge(dial, curve)
            lo, hi = dial[max(j - 1, 0)], dial[j]
            sig = []
            for li in pick:
                s = sel_base & (P["land"] == li)
                s_lo = np.nanmean(P["sigma"][s & (P["v"] == lo)]); s_hi = np.nanmean(P["sigma"][s & (P["v"] == hi)])
                if j == 0 or not np.isfinite(s_lo):
                    sig.append(s_hi)
                else:
                    w = (np.log(edge) - np.log(lo)) / (np.log(hi) - np.log(lo)); sig.append((1 - w) * s_lo + w * s_hi)
            gaps.append(np.nanmean(sig) - 1.0)
        gaps_b.append(gaps)
        alpha_b.append(-loglog_slope(keys, gaps) if key_name == "T" else np.polyfit(np.log(keys), gaps, 1)[0])
    gaps_b = np.array(gaps_b)
    return np.nanpercentile(gaps_b, [5, 95], axis=0), np.nanpercentile(alpha_b, [5, 95])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="results/study_gap"); ap.add_argument("--smoke", action="store_true")
    a = ap.parse_args()
    cfg = dict(CFG)
    global TS, GS, MS, PS, KS_ESN, ETAS, RHOS, T_G
    if a.smoke:
        cfg.update(n_land=2, n_seed=2, n_esn_seed=2, seed_base=1); TS = [125, 250, 500]; GS = [5, 10]; MS = MS[::6]; PS = PS[::6]; T_G = 250
        KS_ESN = [1, 4, 16]; ETAS = [0.01]; RHOS = RHOS[::6]
    os.makedirs(a.out, exist_ok=True); t0 = time.time(); rng = np.random.default_rng(0)
    L, out = [f"# task-set-gap: results (seed base {cfg['seed_base']})\n"], {}

    # ---- derivation checks, exact branching process (reported, not predictions) ----
    L.append("## Derivation checks: exact branching process\n")
    L.append("| L | one-shot delta* (lambda 1e-3) | one-shot delta* (lambda 4e-3) | throughput delta* x L |"); L.append("|---|---|---|---|")
    for l in [2, 4, 8, 16, 32, 64, 128]:
        L.append(f"| {l} | {optimum_gap(l, 1e-3, 0.0)[0]:.4f} | {optimum_gap(l, 4e-3, 0.0)[0]:.4f} | {throughput_gap(l) * l:.3f} |")
    L.append("")

    # ---- population ----
    tasks = [("islands", T, 10, li, cfg) for T in TS for li in range(cfg["n_land"])] + \
            [("er", T, 0, li, cfg) for T in TS for li in range(cfg["n_land"])] + \
            [("islands", T_G, G, li, cfg) for G in GS if G != 10 for li in range(cfg["n_land"])]
    with ProcessPoolExecutor() as ex:
        prow = [r for res in ex.map(pop_task, tasks) for r in res]
    P = np.array(prow, dtype=[("topo", "U7"), ("T", int), ("G", int), ("land", int), ("seed", int), ("v", float), ("perf", float), ("sigma", float)])
    np.save(f"{a.out}/population.npy", P)

    # P-B1, P-B2: islands vs T
    L.append("## Islands: left window edge against horizon (G = 10)\n")
    L.append("| T | edge m | gap | 90% interval | gap x T | band [ln G, 15 ln G] |"); L.append("|---|---|---|---|---|---|")
    gaps = []
    for T in TS:
        sel = (P["topo"] == "islands") & (P["T"] == T) & (P["G"] == 10)
        edge, gap = edge_gap(P, sel, MS); gaps.append(gap)
    gi, ai = boot_pop(P, "islands", TS, "T", 10, MS, cfg, rng)
    band = (np.log(10), 15 * np.log(10))
    for i, T in enumerate(TS):
        L.append(f"| {T} | {edge_gap(P, (P['topo'] == 'islands') & (P['T'] == T) & (P['G'] == 10), MS)[0]:.4g} | {gaps[i]:+.4f} | [{gi[0, i]:+.4f}, {gi[1, i]:+.4f}] | {gaps[i] * T:.1f} | {'in' if band[0] <= gaps[i] * T <= band[1] else 'out'} |")
    alpha_i = -loglog_slope(TS, gaps)
    mono = all(gaps[i] > gaps[i + 1] for i in range(len(gaps) - 1)); positive = all(gi[0] > 0)
    L.append(f"\nalpha = {alpha_i:+.2f}, 90% interval [{ai[0]:+.2f}, {ai[1]:+.2f}]; monotone decreasing: {mono}; all intervals exclude 0: {positive}\n")
    if positive and mono and 0.7 <= alpha_i <= 1.3:
        out["P-B1"] = "pass"
    elif (not positive) or (not mono) or alpha_i < 0.4 or alpha_i > 1.6:
        out["P-B1"] = "fail"
    else:
        out["P-B1"] = "inconclusive"
    inband = [band[0] <= g * T <= band[1] for g, T in zip(gaps, TS)]
    out["P-B2"] = "pass" if all(inband) else ("fail" if sum(inband) <= len(TS) - 2 else "inconclusive")

    # P-B3: ER contrast
    L.append("## Random graph: left window edge against horizon\n")
    L.append("| T | edge p | gap | 90% interval |"); L.append("|---|---|---|---|")
    gaps_e = []
    for T in TS:
        sel = (P["topo"] == "er") & (P["T"] == T)
        edge, gap = edge_gap(P, sel, PS); gaps_e.append(gap)
    ge, ae = boot_pop(P, "er", TS, "T", 0, PS, cfg, rng)
    for i, T in enumerate(TS):
        L.append(f"| {T} | {edge_gap(P, (P['topo'] == 'er') & (P['T'] == T), PS)[0]:.4g} | {gaps_e[i]:+.3f} | [{ge[0, i]:+.3f}, {ge[1, i]:+.3f}] |")
    alpha_e = -loglog_slope(TS, gaps_e)
    L.append(f"\nalpha = {alpha_e:+.2f}, 90% interval [{ae[0]:+.2f}, {ae[1]:+.2f}]\n")
    out["P-B3"] = "pass" if (-0.4 <= alpha_e <= 0.4 and out["P-B1"] == "pass") else ("fail" if alpha_e > 0.7 else "inconclusive")

    # P-B5: gap vs ln G at T = 1000
    L.append(f"## Islands: gap against ln G at T = {T_G}\n")
    L.append("| G | edge m | gap | 90% interval |"); L.append("|---|---|---|---|")
    gaps_g = []
    for G in GS:
        sel = (P["topo"] == "islands") & (P["T"] == T_G) & (P["G"] == G)
        edge, gap = edge_gap(P, sel, MS); gaps_g.append(gap)
        L.append(f"| {G} | {edge:.4g} | {gap:+.4f} | see slope |")
    gg, sg = boot_pop(P, "islands", GS, "G", T_G, MS, cfg, rng)
    slope = np.polyfit(np.log(GS), gaps_g, 1)[0]
    L.append(f"\nslope of gap vs ln G = {slope:+.4f}, 90% interval [{sg[0]:+.4f}, {sg[1]:+.4f}]\n")
    out["P-B5"] = "pass" if sg[0] > 0 else ("fail" if sg[1] < 0 else "inconclusive")

    # ---- reservoir ----
    tasks = [(k, eta, 200, cfg) for k in KS_ESN for eta in ETAS] + [(k, 0.01, 400, cfg) for k in KS_ESN]
    with ProcessPoolExecutor() as ex:
        erow = [r for res in ex.map(esn_task, tasks) for r in res]
    E = np.array(erow, dtype=[("k", int), ("eta", float), ("n", int), ("seed", int), ("rho", float), ("r2", float), ("sigma", float)])
    np.save(f"{a.out}/reservoir.npy", E)
    L.append("## Reservoir: gap at the recall optimum against delay (n = 200)\n")
    L.append("| noise | feasible k | gaps | 90% intervals exclude 0 | monotone | alpha | 90% interval | gap x k |"); L.append("|---|---|---|---|---|---|---|---|")
    c1 = []; constants = []
    for eta in ETAS:
        feas, gaps_r, lo_all = [], [], []
        seeds = np.unique(E["seed"][(E["n"] == 200)])
        for k in KS_ESN:
            sel = (E["k"] == k) & (E["eta"] == eta) & (E["n"] == 200)
            curve = np.array([E["r2"][sel & (E["rho"] == r)].mean() for r in RHOS])
            if np.nanmax(curve) < R2_FLOOR:
                continue
            feas.append(k)
            rstar = RHOS[int(np.argmax(curve))]
            gaps_r.append(1.0 - E["sigma"][sel & (E["rho"] == rstar)].mean())
            bs = []
            for _ in range(N_BOOT):
                pick = rng.choice(seeds, len(seeds), replace=True)
                cb = np.array([np.mean([E["r2"][sel & (E["rho"] == r) & (E["seed"] == s)].mean() for s in pick]) for r in RHOS])
                rb = RHOS[int(np.argmax(cb))]
                bs.append(1.0 - np.mean([E["sigma"][sel & (E["rho"] == rb) & (E["seed"] == s)].mean() for s in pick]))
            lo_all.append(np.percentile(bs, 5))
        if len(feas) < 3:
            L.append(f"| {eta} | {feas} | too few feasible delays | | | | | |"); c1.append("inconclusive"); continue
        al = -loglog_slope(feas, gaps_r)
        ab = []
        for _ in range(N_BOOT):
            pick = rng.choice(seeds, len(seeds), replace=True)
            gb = []
            for k in feas:
                sel = (E["k"] == k) & (E["eta"] == eta) & (E["n"] == 200)
                cb = np.array([np.mean([E["r2"][sel & (E["rho"] == r) & (E["seed"] == s)].mean() for s in pick]) for r in RHOS])
                rb = RHOS[int(np.argmax(cb))]
                gb.append(1.0 - np.mean([E["sigma"][sel & (E["rho"] == rb) & (E["seed"] == s)].mean() for s in pick]))
            ab.append(-loglog_slope(feas, gb))
        mono = all(gaps_r[i] > gaps_r[i + 1] for i in range(len(gaps_r) - 1)); pos = all(l > 0 for l in lo_all)
        const = float(np.mean([g * k for g, k in zip(gaps_r, feas)])); constants.append(const)
        L.append(f"| {eta} | {feas} | {', '.join(f'{g:+.3f}' for g in gaps_r)} | {pos} | {mono} | {al:+.2f} | [{np.nanpercentile(ab, 5):+.2f}, {np.nanpercentile(ab, 95):+.2f}] | {const:.2f} |")
        if pos and mono and 0.5 <= al <= 1.0:
            c1.append("pass")
        elif (not pos) or (not mono) or al < 0.3 or al > 1.2:
            c1.append("fail")
        else:
            c1.append("inconclusive")
    out["P-C1"] = "fail" if "fail" in c1 else ("inconclusive" if "inconclusive" in c1 else "pass")
    if len(constants) == len(ETAS):
        dec = all(constants[i] > constants[i + 1] for i in range(len(constants) - 1))
        inc = all(constants[i] < constants[i + 1] for i in range(len(constants) - 1))
        out["P-C2"] = "pass" if dec else ("fail" if inc else "inconclusive")
    else:
        out["P-C2"] = "inconclusive"
    # exploratory: n = 400 at noise 0.01
    gaps4 = []
    for k in KS_ESN:
        sel = (E["k"] == k) & (E["eta"] == 0.01) & (E["n"] == 400)
        curve = np.array([E["r2"][sel & (E["rho"] == r)].mean() for r in RHOS])
        if np.nanmax(curve) >= R2_FLOOR:
            gaps4.append((k, 1.0 - E["sigma"][sel & (E["rho"] == RHOS[int(np.argmax(curve))])].mean()))
    if len(gaps4) >= 3:
        L.append(f"\nexploratory, n = 400 at noise 0.01: alpha = {-loglog_slope([g[0] for g in gaps4], [g[1] for g in gaps4]):+.2f}\n")

    L.append("## Outcomes, applied literally\n")
    for pid in ["P-B1", "P-B2", "P-B3", "P-B5", "P-C1", "P-C2"]:
        L.append(f"- {pid}: {out[pid]}")
    L.append(f"\nElapsed {time.time() - t0:.0f}s.\n")
    open(f"{a.out}/summary.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main()
