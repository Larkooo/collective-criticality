"""Version two of the gap study (studies/task-set-gap-2). Stable edge estimator, Proposition 8's
zero-parameter prediction across population sizes, and reservoir predictions at new noise, size,
and ridge settings. Pilot: --seed-base 5151. Confirmatory: --seed-base 6161 (default)."""
import argparse
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from critpop.landscape import NK
from critpop.model import run
from critpop.reservoir import run_esn

K, G, TOL, R2_FLOOR, N_BOOT = 6, 10, 0.005, 0.5, 200
NS = [50, 100, 200, 400]
TS = [250, 500, 1000, 2000]
MS = [float(x) for x in np.logspace(-4.7, -0.5, 25)]
GS = [5, 10, 20, 50]
N_G, T_G = 200, [500, 1000]
NOISE_DOM = 0.15
KS_ESN = [1, 2, 3, 4, 6, 8, 16]
RHOS = [float(x) for x in np.linspace(0.5, 1.25, 31)]
ESN_CELLS = [("noise", NOISE_DOM, 200, 1e-6), ("size", 0.01, 200, 1e-6), ("size", 0.01, 800, 1e-6),
             ("ridge", 0.001, 200, 1e-6), ("ridge", 0.001, 200, 1e-3), ("ridge", 0.001, 200, 1e-1)]
CFG = dict(n_land=8, n_seed=4, n_esn_seed=8, seed_base=6161)


def loglog_slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float); ok = np.isfinite(y) & (y > 0)
    return float(np.polyfit(np.log(x[ok]), np.log(y[ok]), 1)[0]) if ok.sum() >= 3 else np.nan


def growth_and_t0(h, n):
    """(growth factor over the window from first appearance to half coverage, t0, t_half)."""
    on = h >= 1
    if not on.any():
        return np.nan, np.nan, np.nan
    t0 = int(np.argmax(on)); half = np.where(h >= n / 2)[0]; t1 = int(half[0]) if half.size else len(h) - 1
    t_half = float(half[0]) if half.size else np.nan
    if t1 - t0 < 2:
        return np.nan, float(t0), t_half
    t = np.arange(t0, t1 + 1)
    return float(np.exp(np.polyfit(t, np.log(np.maximum(h[t0:t1 + 1], 1)), 1)[0])), float(t0), t_half


def smooth(curve):
    c = np.array(curve, float); out = c.copy()
    for i in range(1, len(c) - 1):
        out[i] = np.nanmean(c[i - 1:i + 2])
    return out


def left_edge(dial, curve, tol=TOL):
    c = smooth(curve)
    if not np.isfinite(c).any():
        return np.nan, 0
    top = np.nanmax(c); idx = np.where(c >= top - tol)[0]; j = int(idx[0])
    if j == 0:
        return float(dial[0]), 0
    x0, x1, y0, y1 = np.log(dial[j - 1]), np.log(dial[j]), c[j - 1], c[j]
    return float(np.exp(x0 + (top - tol - y0) / max(y1 - y0, 1e-12) * (x1 - x0))), j


def pop_task(args):
    n, T, g, li, cfg = args
    land = NK(20, K, np.random.default_rng([K, li, cfg["seed_base"]]))
    rows = []
    for si in range(cfg["n_seed"]):
        for m in MS:
            rng = np.random.default_rng([K, li, si, n, T, g, int(round(m * 1e7)), 52])
            r = run(land, n, 0.0, 0.0, T, rng, islands=g, migration=m)
            sig, t0, _ = growth_and_t0(r.holders_traj, n)
            isig, _, thalf = growth_and_t0(r.island_holders_traj, g)
            rows.append((n, T, g, li, si, m, float(r.mean_f[-1]), sig, isig, t0, thalf))
    return rows


def esn_task(args):
    kind, noise, n, ridge, si, cfg = args
    rows = []
    for _ in [0]:
        for rho in RHOS:
            for k in KS_ESN:
                r = run_esn(rho, k, noise, np.random.default_rng([k, int(noise * 1e6), si, n, int(-np.log10(ridge)), cfg["seed_base"]]), n=n, ridge=ridge)
                rows.append((kind, noise, n, ridge, k, si, rho, r.r2, r.sigma_meas))
    return rows


def edge_stats(P, n, T, lands, g=G):
    """Edge, agent gap, island gap, t0, plateau, isolated mean, censored flag (multiplicity-weighted over landscapes)."""
    sel = (P["n"] == n) & (P["T"] == T) & (P["G"] == g)
    curve = np.zeros(len(MS)); cnt = 0
    for li in lands:
        s = sel & (P["land"] == li)
        curve += np.array([P["perf"][s & (P["m"] == m)].mean() for m in MS]); cnt += 1
    curve /= cnt
    edge, j = left_edge(MS, curve)
    lo, hi = MS[max(j - 1, 0)], MS[j]
    def at(field, m):
        return np.nanmean(np.concatenate([P[field][sel & (P["land"] == li) & (P["m"] == m)] for li in lands]))
    s_lo, s_hi, t_lo, t_hi = at("sigma", lo), at("sigma", hi), at("t0", lo), at("t0", hi)
    i_lo, i_hi, h_lo, h_hi = at("isigma", lo), at("isigma", hi), at("thalf", lo), at("thalf", hi)
    if j == 0 or not np.isfinite(s_lo):
        sig, isig, t0, thalf = s_hi, i_hi, t_hi, h_hi
    else:
        w = (np.log(edge) - np.log(lo)) / (np.log(hi) - np.log(lo)); sig = (1 - w) * s_lo + w * s_hi; isig = (1 - w) * i_lo + w * i_hi; t0 = (1 - w) * t_lo + w * t_hi; thalf = (1 - w) * h_lo + w * h_hi
    plateau, mu0 = float(np.nanmax(smooth(curve))), float(curve[0])
    censored = (j == 0)
    return edge, sig - 1.0, isig - 1.0, t0, plateau, mu0, censored, thalf


def c_required(plateau, mu0):
    delta = max(plateau - mu0, 1e-9); return max(1.0 - TOL / delta, 0.05)


def predicted_gap(n, T, t0, plateau, mu0):
    return np.log(c_required(plateau, mu0) * n) / max(T - t0, 1.0)


def predicted_island_gap(g, T, t0, plateau, mu0):
    """Logistic spread among G islands: time from one island to coverage C_req is ln((G-1) C/(1-C)) / epsilon."""
    c = min(c_required(plateau, mu0), 0.995)
    return np.log((g - 1) * c / (1 - c)) / max(T - t0, 1.0)


def predicted_time_ratio(g, plateau, mu0):
    """At the edge, (T - t0) / (t_half - t0) = ln((G-1) C/(1-C)) / ln(G-1) under logistic spread."""
    c = min(c_required(plateau, mu0), 0.995)
    return np.log((g - 1) * c / (1 - c)) / np.log(g - 1)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="results/study_gap2"); ap.add_argument("--seed-base", type=int, default=CFG["seed_base"])
    ap.add_argument("--smoke", action="store_true"); a = ap.parse_args()
    cfg = dict(CFG, seed_base=a.seed_base)
    global NS, TS, MS, KS_ESN, RHOS, ESN_CELLS, GS, T_G, N_G
    if a.smoke:
        cfg.update(n_land=2, n_seed=2, n_esn_seed=2); NS = [50, 100]; TS = [250, 500]; MS = MS[::6]; KS_ESN = [1, 4, 16]; RHOS = RHOS[::6]; ESN_CELLS = ESN_CELLS[:3]; GS = [5, 10]; T_G = [250]; N_G = 100
    os.makedirs(a.out, exist_ok=True); t0 = time.time(); rng = np.random.default_rng(0)
    L = [f"# task-set-gap-2: results (seed base {cfg['seed_base']})\n"]; out = {}

    # ---- population ----
    tasks = [(n, T, G, li, cfg) for n in NS for T in TS for li in range(cfg["n_land"])] + \
            [(N_G, T, g, li, cfg) for g in GS if g != G for T in T_G for li in range(cfg["n_land"])]
    with ProcessPoolExecutor() as ex:
        prow = [r for res in ex.map(pop_task, tasks) for r in res]
    P = np.array(prow, dtype=[("n", int), ("T", int), ("G", int), ("land", int), ("seed", int), ("m", float), ("perf", float), ("sigma", float), ("isigma", float), ("t0", float), ("thalf", float)])
    np.save(f"{a.out}/population.npy", P)
    lands = list(range(cfg["n_land"]))
    L.append("## Islands: edge gaps against the zero-parameter predictions (G = 10, K = 6)\n")
    L.append("| N | T | edge m | censored | agent gap | 90% interval | in | island gap | 90% interval | t0 | pred agent | ratio | pred island | ratio | island gap x (T - t0) |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    rat_a, rat_i, gaps_by_n, ints_by_n, cens = {}, {}, {}, {}, {}
    for n in NS:
        for T in TS:
            edge, gap, igap, t_0, plateau, mu0, censored, thalf = edge_stats(P, n, T, lands)
            pa, pi = predicted_gap(n, T, t_0, plateau, mu0), predicted_island_gap(G, T, t_0, plateau, mu0)
            bs, bi = [], []
            for _ in range(N_BOOT):
                pick = list(rng.choice(lands, len(lands), replace=True)); r2 = edge_stats(P, n, T, pick); bs.append(r2[1]); bi.append(r2[2])
            lo, hi = np.nanpercentile(bs, [5, 95]); ilo, ihi = np.nanpercentile(bi, [5, 95]); inside = lo <= gap <= hi
            cens[(n, T)] = censored; rat_a[(n, T)] = gap / pa; rat_i[(n, T)] = igap / pi
            gaps_by_n.setdefault(n, []).append(gap); ints_by_n.setdefault(n, []).append((lo, hi, gap))
            L.append(f"| {n} | {T} | {edge:.3g} | {censored} | {gap:+.4f} | [{lo:+.4f}, {hi:+.4f}] | {inside} | {igap:+.4f} | [{ilo:+.4f}, {ihi:+.4f}] | {t_0:.0f} | {pa:.4f} | {rat_a[(n, T)]:.2f} | {pi:.4f} | {rat_i[(n, T)]:.2f} | {igap * (T - t_0):.2f} |")
    n_cens = sum(cens.values())
    def band_outcome(rat, lo_b, hi_b, lo_x, hi_x):
        rv = np.array([v for k, v in rat.items() if not cens[k]]); ok = np.isfinite(rv)
        n_in = int(np.sum((rv >= lo_b) & (rv <= hi_b))); n_out = int(np.sum((rv < lo_x) | (rv > hi_x) | ~ok)); n_tot = len(rv)
        if n_cens > 2 or n_tot < 12:
            return "inconclusive", n_in, n_out, n_tot
        return ("pass" if (n_in >= n_tot - 2 and n_out == 0) else ("fail" if (n_out >= 2 or n_in < n_tot // 2) else "inconclusive")), n_in, n_out, n_tot
    o1, i1, x1, t1 = band_outcome(rat_a, 0.65, 1.5, 0.4, 2.5); o2, i2, x2, t2 = band_outcome(rat_i, 0.6, 1.6, 0.4, 2.5)
    L.append(f"\nP-B1 (agent, Proposition 8): {i1}/{t1} ratios in [0.65, 1.5], {x1} outside [0.4, 2.5], censored cells {n_cens}")
    L.append(f"P-B2 (island, logistic Theorem 6): {i2}/{t2} ratios in [0.6, 1.6], {x2} outside [0.4, 2.5]")
    out["P-B1"], out["P-B2"] = o1, o2
    # P-B3: decrease in T by mutual exclusion of point estimates, and exponent band
    dec_all, exps = True, []
    for n in NS:
        (lo0, hi0, g0), (lo3, hi3, g3) = ints_by_n[n][0], ints_by_n[n][-1]
        dec_all &= (hi3 < g0) and (lo0 > g3); exps.append(-loglog_slope(TS, gaps_by_n[n]))
    L.append(f"P-B3: T = 2000 below T = 250 by mutual exclusion at every N: {dec_all}; exponents by N: {[round(e, 2) for e in exps]} (band [0.7, 1.3])")
    exps = np.array(exps); out["P-B3"] = "pass" if (dec_all and np.all((exps >= 0.7) & (exps <= 1.3))) else ("fail" if (not dec_all or np.any(exps < 0.4) or np.any(exps > 1.6)) else "inconclusive")
    # P-B4: timing at the edge across G at N = 200: (T - t0)/(t_half - t0) against the logistic prediction
    L.append(f"\n## Islands: edge timing against ln G at N = {N_G}\n"); L.append("| G | T | edge m | censored | t0 | t_half | (T - t0)/(t_half - t0) | predicted | ratio |"); L.append("|---|---|---|---|---|---|---|---|---|")
    rat_t = []
    for g in GS:
        for T in T_G:
            edge, gap, igap, t_0, plateau, mu0, censored, thalf = edge_stats(P, N_G, T, lands, g=g)
            meas = (T - t_0) / max(thalf - t_0, 1.0) if np.isfinite(thalf) else np.nan
            pred = predicted_time_ratio(g, plateau, mu0)
            if not censored and np.isfinite(meas):
                rat_t.append(meas / pred)
            L.append(f"| {g} | {T} | {edge:.3g} | {censored} | {t_0:.0f} | {thalf:.0f} | {meas:.2f} | {pred:.2f} | {meas / pred:.2f} |")
    rt = np.array(rat_t); n_in4 = int(np.sum((rt >= 0.7) & (rt <= 1.4))); n_out4 = int(np.sum((rt < 0.5) | (rt > 2.0)))
    L.append(f"\nP-B4: {n_in4}/{len(rt)} timing ratios in [0.7, 1.4], {n_out4} outside [0.5, 2.0]")
    out["P-B4"] = "inconclusive" if len(rt) < 6 else ("pass" if (n_in4 >= len(rt) - 2 and n_out4 == 0) else ("fail" if (n_out4 >= 2 or n_in4 < len(rt) // 2) else "inconclusive"))

    # ---- reservoir ----
    tasks = [(kind, noise, n, ridge, si, cfg) for kind, noise, n, ridge in ESN_CELLS for si in range(cfg["n_esn_seed"])]
    with ProcessPoolExecutor() as ex:
        erow = [r for res in ex.map(esn_task, tasks) for r in res]
    E = np.array(erow, dtype=[("kind", "U6"), ("noise", float), ("n", int), ("ridge", float), ("k", int), ("seed", int), ("rho", float), ("r2", float), ("sigma", float)])
    np.save(f"{a.out}/reservoir.npy", E)

    def alpha_cell(noise, n, ridge, seeds):
        feas, gaps = [], []
        floor = 0.4 if noise == NOISE_DOM else R2_FLOOR
        for k in KS_ESN:
            sel = (E["noise"] == noise) & (E["n"] == n) & (E["ridge"] == ridge) & (E["k"] == k) & np.isin(E["seed"], seeds)
            if not sel.any():
                continue
            curve = np.array([E["r2"][sel & (E["rho"] == r)].mean() for r in RHOS])
            if np.nanmax(curve) < floor:
                continue
            feas.append(k); gaps.append(1.0 - E["sigma"][sel & (E["rho"] == RHOS[int(np.argmax(curve))])].mean())
        return (-loglog_slope(feas, gaps) if len(feas) >= 3 else np.nan), feas, gaps

    seeds_all = np.unique(E["seed"])
    L.append("\n## Reservoir\n"); L.append("| cell | noise | n | ridge | feasible k | gaps | alpha | 90% interval |"); L.append("|---|---|---|---|---|---|---|---|")
    A = {}
    for kind, noise, n, ridge in ESN_CELLS:
        al, feas, gaps = alpha_cell(noise, n, ridge, seeds_all)
        ab = [alpha_cell(noise, n, ridge, rng.choice(seeds_all, len(seeds_all), replace=True))[0] for _ in range(N_BOOT)]
        lo, hi = np.nanpercentile(ab, [5, 95]); A[(noise, n, ridge)] = (al, lo, hi, feas)
        L.append(f"| {kind} | {noise} | {n} | {ridge:g} | {feas} | {', '.join(f'{g:+.3f}' for g in gaps)} | {al:+.2f} | [{lo:+.2f}, {hi:+.2f}] |")
    def get(noise, n, ridge):
        return A.get((noise, n, ridge), (np.nan, np.nan, np.nan, []))
    # P-C1: alpha at noise 0.3 in [0.85, 1.05]; fail if interval wholly outside [0.7, 1.2] or too few feasible delays
    al, lo, hi, feas = get(NOISE_DOM, 200, 1e-6)
    out["P-C1"] = "pass" if (len(feas) >= 3 and 0.85 <= al <= 1.05) else ("fail" if (len(feas) >= 3 and (hi < 0.7 or lo > 1.2)) else "inconclusive")
    # P-C2: alpha(n=800) - alpha(n=200) at noise 0.01 >= 0.05 with a bootstrap interval excluding 0
    d = get(0.01, 800, 1e-6)[0] - get(0.01, 200, 1e-6)[0]
    db = []
    for _ in range(N_BOOT):
        s = rng.choice(seeds_all, len(seeds_all), replace=True); db.append(alpha_cell(0.01, 800, 1e-6, s)[0] - alpha_cell(0.01, 200, 1e-6, s)[0])
    dlo, dhi = np.nanpercentile(db, [5, 95])
    L.append(f"\nP-C2: alpha(800) - alpha(200) at noise 0.01 = {d:+.3f}, interval [{dlo:+.3f}, {dhi:+.3f}]")
    L.append("(size effect is exploratory in version two; not a prediction)")
    # P-C3: ridge ordering at noise 0.001
    r6, r3, r1 = get(0.001, 200, 1e-6)[0], get(0.001, 200, 1e-3)[0], get(0.001, 200, 1e-1)[0]
    L.append(f"P-C3: alpha by ridge at noise 0.001: 1e-6 -> {r6:+.2f}, 1e-3 -> {r3:+.2f}, 1e-1 -> {r1:+.2f}")
    out["P-C3"] = "pass" if (r6 < r3 < r1) else ("fail" if (r6 > r3 > r1) else "inconclusive")
    L.append("\n## Outcomes, applied literally\n")
    for pid in ["P-B1", "P-B2", "P-B3", "P-B4", "P-C1", "P-C3"]:
        L.append(f"- {pid}: {out[pid]}")
    L.append(f"\nElapsed {time.time() - t0:.0f}s.\n")
    open(f"{a.out}/summary.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main()
