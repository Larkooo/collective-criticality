"""Finite-size check. The main sweep found the performance optimum at mean degree ~3-4
while the diversity transition (graph percolation) sits at mean degree ~1.5. If the
optimum approaches the transition as the population grows, the optimum is "at the edge"
in the thermodynamic limit. If the ratio stays fixed, it is merely near it."""
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from critpop.analyze import peak
from critpop.landscape import NK
from critpop.model import run

K = 6
NS = [50, 100, 200, 400]
DEGREES = np.logspace(np.log10(0.3), np.log10(30), 15)
N_LAND, N_SEED, STEPS = 4, 4, 300


def task(args):
    li, n = args
    land = NK(20, K, np.random.default_rng([K, li, 1234]))
    out = []
    for d in DEGREES:
        p = min(d / (n - 1), 1.0)
        for si in range(N_SEED):
            r = run(land, n, p, 0.0, STEPS, np.random.default_rng([K, li, si, n, int(d * 1e4), 3]))
            out.append((li, n, d, si, float(r.mean_f[-1]), float(r.diversity[-1]), float(r.diversity.mean())))
    return out


def half_drop(x, y):
    d0 = y[0]
    below = np.where(y < d0 / 2)[0]
    if not below.size or below[0] == 0:
        return np.nan
    j = below[0]
    x0, x1, y0, y1 = np.log10(x[j - 1]), np.log10(x[j]), y[j - 1], y[j]
    return 10 ** (x0 + (d0 / 2 - y0) / (y1 - y0) * (x1 - x0))


def main():
    t0 = time.time()
    tasks = [(li, n) for n in NS for li in range(N_LAND)]
    with ProcessPoolExecutor() as ex:
        rows = [r for res in ex.map(task, tasks) for r in res]
    arr = np.array(rows)
    _, N, d, _, perf, div, _ = arr.T
    print(f"{len(rows)} runs in {time.time() - t0:.0f}s; K={K}, {N_LAND} landscapes x {N_SEED} seeds, {STEPS} steps\n")
    print("| N agents | degree* of mean fitness | degree at diversity half-drop | ratio | gain of peak over degree 30 |")
    print("|---|---|---|---|---|")
    for n in NS:
        m = N == n
        pf = np.array([perf[m & (d == dd)].mean() for dd in DEGREES])
        dv = np.array([div[m & (d == dd)].mean() for dd in DEGREES])
        ds, hd = peak(DEGREES, pf), half_drop(DEGREES, dv)
        print(f"| {n} | {ds:.2f} | {hd:.2f} | {ds / hd:.2f} | {pf.max() - pf[-1]:+.3f} |")
    np.savez_compressed("results/finite_size.npz", rows=arr, degrees=DEGREES, ns=np.array(NS), k=K)


if __name__ == "__main__":
    main()
