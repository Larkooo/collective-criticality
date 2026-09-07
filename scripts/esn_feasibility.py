"""Which delays are feasible (max R^2 over radii) at intermediate noise levels; decides the noise-dominated cell."""
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from critpop.reservoir import run_esn

RHOS = [float(x) for x in np.linspace(0.5, 1.25, 31)]; KS = [1, 2, 4, 8, 16]


def cell(args):
    noise, si = args
    return [(noise, si, k, rho, run_esn(rho, k, noise, np.random.default_rng([k, int(noise * 1e6), si, 200, 6, 5151]), n=200).r2) for k in KS for rho in RHOS]


if __name__ == "__main__":
    with ProcessPoolExecutor() as ex:
        rows = [r for res in ex.map(cell, [(nz, si) for nz in [0.1, 0.15, 0.2] for si in range(4)]) for r in res]
    R = np.array(rows, dtype=[("noise", float), ("seed", int), ("k", int), ("rho", float), ("r2", float)])
    for nz in [0.1, 0.15, 0.2]:
        line = []
        for k in KS:
            sel = (R["noise"] == nz) & (R["k"] == k)
            best = max(np.mean(R["r2"][sel & (R["rho"] == r)]) for r in RHOS)
            line.append(f"k={k}: {best:.2f}")
        print(f"noise {nz}: " + "  ".join(line))
