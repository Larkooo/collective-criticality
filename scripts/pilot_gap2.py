"""DESIGN PILOT, second iteration, population systems only. The first iteration used an
argmax on a two-decade plateau and could not resolve the island gap. This one measures the
LEFT WINDOW EDGE: the smallest dial value whose mean performance is within 0.005 of the
grid maximum, refined by log-linear interpolation, with sigma measured at that edge from the
growth of holders of the eventual best genotype. Excluded seeds. Not confirmatory."""
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from critpop.landscape import NK
from critpop.model import run
from pilot_gap import growth_factor, loglog_slope  # noqa: E402  (scripts/ is sys.path[0] when run as a script)

OUT = "results/pilot_gap"
TS = [250, 500, 1000, 2000]
MS = [float(x) for x in np.logspace(-3.5, -0.5, 21)]
PS = [float(x) for x in np.logspace(-2.2, -0.5, 21)]
K, G, N, N_LAND, N_SEED, LAND_BASE, TOL = 6, 10, 100, 6, 4, 7777, 0.005


def task(args):
    topo, T, li = args
    land = NK(20, K, np.random.default_rng([K, li, LAND_BASE]))
    rows, dial = [], (MS if topo == "islands" else PS)
    for si in range(N_SEED):
        for v in dial:
            rng = np.random.default_rng([K, li, si, T, int(round(v * 1e6)), 31 if topo == "islands" else 32])
            r = run(land, N, 0.0, 0.0, T, rng, islands=G, migration=v) if topo == "islands" else run(land, N, v, 0.0, T, rng)
            rows.append((topo, T, li, si, v, float(r.mean_f[-1]), float(r.max_f[-1]), growth_factor(r.holders_traj, N)))
    return rows


def left_edge(dial, curve, tol=TOL):
    top = np.nanmax(curve)
    idx = np.where(curve >= top - tol)[0]
    j = int(idx[0])
    if j == 0:
        return float(dial[0]), 0
    x0, x1, y0, y1 = np.log(dial[j - 1]), np.log(dial[j]), curve[j - 1], curve[j]
    return float(np.exp(x0 + (top - tol - y0) / (y1 - y0) * (x1 - x0))), j


def sigma_at(P, sel, dial, edge, j):
    """sigma measured at the bracketing grid points, log-linearly weighted."""
    lo, hi = dial[max(j - 1, 0)], dial[j]
    s_lo = np.nanmean(P["sigma"][sel & (P["v"] == lo)]); s_hi = np.nanmean(P["sigma"][sel & (P["v"] == hi)])
    if j == 0 or not np.isfinite(s_lo):
        return s_hi
    w = (np.log(edge) - np.log(lo)) / (np.log(hi) - np.log(lo))
    return (1 - w) * s_lo + w * s_hi


def main():
    t0 = time.time()
    tasks = [(topo, T, li) for topo in ["islands", "er"] for T in TS for li in range(N_LAND)]
    with ProcessPoolExecutor() as ex:
        rows = [r for res in ex.map(task, tasks) for r in res]
    P = np.array(rows, dtype=[("topo", "U7"), ("T", int), ("land", int), ("seed", int), ("v", float), ("perf", float), ("best", float), ("sigma", float)])
    np.save(f"{OUT}/population2.npy", P)
    L = [f"# Design pilot 2: window-edge estimator for the population systems ({N_LAND} excluded landscapes x {N_SEED} seeds, K={K})\n"]
    for topo, dial, pred, band in [("islands", MS, 1.0, (np.log(G), 15 * np.log(G))), ("er", PS, 0.0, None)]:
        L.append(f"## {topo}\n")
        L.append("| T | left edge (mean-agent) | sigma at edge | gap | LOO gap range | gap x T | left edge (best-found) | plateau height | range of perf over grid |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        gaps = []
        for T in TS:
            sel = (P["topo"] == topo) & (P["T"] == T)
            curve = np.array([P["perf"][sel & (P["v"] == v)].mean() for v in dial])
            bcurve = np.array([P["best"][sel & (P["v"] == v)].mean() for v in dial])
            edge, j = left_edge(dial, curve)
            bedge, _ = left_edge(dial, bcurve)
            sig = sigma_at(P, sel, dial, edge, j)
            gap = sig - 1.0
            gaps.append(gap)
            loo = []
            for li in range(N_LAND):
                s2 = sel & (P["land"] != li)
                c2 = np.array([P["perf"][s2 & (P["v"] == v)].mean() for v in dial])
                e2, j2 = left_edge(dial, c2)
                loo.append(sigma_at(P, s2, dial, e2, j2) - 1.0)
            L.append(f"| {T} | {edge:.4g} | {sig:.3f} | {gap:+.4f} | [{min(loo):+.4f}, {max(loo):+.4f}] | {gap * T:.1f} | {bedge:.4g} | {np.nanmax(curve):.4f} | {np.nanmin(curve):.4f} to {np.nanmax(curve):.4f} |")
        a = -loglog_slope(TS, gaps)
        L.append(f"\nfitted alpha of edge gap vs T: {a:+.2f}  predicted {pred:.0f}" + (f"; predicted band for gap x T: [{band[0]:.1f}, {band[1]:.1f}]" if band else "") + "\n")
    L.append(f"Elapsed {time.time() - t0:.0f}s.\n")
    open(f"{OUT}/summary2.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
