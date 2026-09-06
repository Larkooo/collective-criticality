"""DESIGN PILOT for study task-set-gap (docs/GAP_THEORY.md). Excluded seeds throughout.
Not a confirmatory run. Its job: check that the gap can be measured, that exponents can be
resolved, and that the derived forms are the right ones to preregister."""
import os
import time
from concurrent.futures import ProcessPoolExecutor

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from critpop.analyze import peak  # noqa: E402
from critpop.branching import optimum_gap, throughput_gap  # noqa: E402
from critpop.landscape import NK  # noqa: E402
from critpop.model import run  # noqa: E402
from critpop.reservoir import run_esn  # noqa: E402

OUT = "results/pilot_gap"
LS = [2, 4, 8, 16, 32, 64]
TS = [125, 250, 500, 1000, 2000]
MS = [float(x) for x in np.logspace(-3.5, -0.5, 13)]
PS = [float(x) for x in np.logspace(-2.2, -0.5, 12)]
KS_ESN, ETAS, RHOS = [1, 2, 4, 8, 16, 32], [0.001, 0.01, 0.1], [float(x) for x in np.linspace(0.5, 1.25, 25)]
K, G, N, N_LAND, N_SEED, N_ESN_SEED = 6, 10, 100, 3, 4, 4
LAND_BASE = 7777  # excluded from every earlier study


def loglog_slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(y) & (y > 0)
    if ok.sum() < 3:
        return np.nan
    return float(np.polyfit(np.log(x[ok]), np.log(y[ok]), 1)[0])


def growth_factor(h: np.ndarray, n: int) -> float:
    on = h >= 1
    if not on.any():
        return np.nan
    t0 = int(np.argmax(on))
    half = np.where(h >= n / 2)[0]
    t1 = int(half[0]) if half.size else len(h) - 1
    if t1 - t0 < 2:
        return np.nan
    t = np.arange(t0, t1 + 1)
    return float(np.exp(np.polyfit(t, np.log(np.maximum(h[t0:t1 + 1], 1)), 1)[0]))


def pop_task(args):
    topo, T, li = args
    land = NK(20, K, np.random.default_rng([K, li, LAND_BASE]))
    rows = []
    dial = MS if topo == "islands" else PS
    for si in range(N_SEED):
        for v in dial:
            rng = np.random.default_rng([K, li, si, T, int(round(v * 1e6)), 21 if topo == "islands" else 22])
            if topo == "islands":
                r = run(land, N, 0.0, 0.0, T, rng, islands=G, migration=v)
            else:
                r = run(land, N, v, 0.0, T, rng)
            rows.append((topo, T, li, si, v, float(r.mean_f[-1]), growth_factor(r.holders_traj, N), r.n_copies))
    return rows


def esn_task(args):
    k, eta = args
    rows = []
    for si in range(N_ESN_SEED):
        for rho in RHOS:
            r = run_esn(rho, k, eta, np.random.default_rng([k, int(eta * 1e6), si, 100 + si]))
            rows.append((k, eta, si, rho, r.r2, r.sigma_meas))
    return rows


def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    L = ["# Design pilot: task-set gap (excluded seeds; not confirmatory)\n"]

    # ---- A. branching process, exact ----
    L.append("## A. Branching process (exact generating function)\n")
    L.append("| L | one-shot delta*, lambda=1e-3 | one-shot delta*, lambda=4e-3 | throughput delta* | throughput delta* x L |")
    L.append("|---|---|---|---|---|")
    os1, os4, thr = [], [], []
    for l in LS:
        a, _ = optimum_gap(l, 1e-3, 0.0); b, _ = optimum_gap(l, 4e-3, 0.0); c = throughput_gap(l)
        os1.append(a); os4.append(b); thr.append(c)
        L.append(f"| {l} | {a:.4f} | {b:.4f} | {c:.4f} | {c * l:.3f} |")
    L.append(f"\nfitted alpha (one-shot, lambda=1e-3, where an optimum exists): {-loglog_slope(LS, os1):+.2f}  predicted 0; "
             f"sqrt(lambda) = {np.sqrt(1e-3):.4f} vs mean delta* {np.nanmean(os1):.4f}; ratio of gaps for 4x cost: {np.nanmean(os4)/np.nanmean(os1):.2f} (predicted 2.0)")
    L.append(f"fitted alpha (throughput): {-loglog_slope(LS, thr):+.2f}  predicted 1; delta* x L -> {np.mean([c*l for c, l in zip(thr, LS)]):.3f} (predicted 1.59 near-critical; exact differs at small L)\n")

    # ---- B. population model ----
    tasks = [(topo, T, li) for topo in ["islands", "er"] for T in TS for li in range(N_LAND)]
    with ProcessPoolExecutor() as ex:
        prow = [r for res in ex.map(pop_task, tasks) for r in res]
    P = np.array(prow, dtype=[("topo", "U7"), ("T", int), ("land", int), ("seed", int), ("v", float), ("perf", float), ("sigma", float), ("copies", int)])
    np.save(f"{OUT}/population.npy", P)
    for topo, dial, pred in [("islands", MS, 1.0), ("er", PS, 0.0)]:
        L.append(f"## B. Population model, {topo} (K={K}, N={N}, {N_LAND} excluded landscapes x {N_SEED} seeds)\n")
        L.append("| T | dial* | sigma_meas at dial* | gap = sigma-1 | gap x T | ln G / T | dial* with adoption cost 0.002 | with 0.005 |")
        L.append("|---|---|---|---|---|---|---|---|")
        gaps, gaps_lo = [], []
        for T in TS:
            sel = (P["topo"] == topo) & (P["T"] == T)
            curve = np.array([P["perf"][sel & (P["v"] == v)].mean() for v in dial])
            vstar = peak(np.array(dial), curve)
            j = int(np.argmin(np.abs(np.log(np.array(dial)) - np.log(vstar))))
            sig = np.nanmean(P["sigma"][sel & (P["v"] == dial[j])])
            gap = sig - 1.0
            gaps.append(gap)
            # leave-one-landscape-out spread of the gap
            loo = []
            for li in range(N_LAND):
                s2 = sel & (P["land"] != li)
                c2 = np.array([P["perf"][s2 & (P["v"] == v)].mean() for v in dial])
                j2 = int(np.argmin(np.abs(np.log(np.array(dial)) - np.log(peak(np.array(dial), c2)))))
                loo.append(np.nanmean(P["sigma"][s2 & (P["v"] == dial[j2])]) - 1.0)
            gaps_lo.append((min(loo), max(loo)))
            costed = []
            for lam in [0.002, 0.005]:
                cc = np.array([(P["perf"][sel & (P["v"] == v)] - lam * P["copies"][sel & (P["v"] == v)] / N).mean() for v in dial])
                costed.append(peak(np.array(dial), cc))
            L.append(f"| {T} | {vstar:.4g} | {sig:.3f} | {gap:+.3f} [{loo and min(loo):+.3f}, {max(loo):+.3f}] | {gap * T:.1f} | {np.log(G)/T:.4f} | {costed[0]:.4g} | {costed[1]:.4g} |")
        L.append(f"\nfitted alpha of gap vs T: {-loglog_slope(TS, gaps):+.2f}  predicted {pred:.0f}\n")

    # ---- C. reservoir ----
    tasks = [(k, eta) for k in KS_ESN for eta in ETAS]
    with ProcessPoolExecutor() as ex:
        erow = [r for res in ex.map(esn_task, tasks) for r in res]
    E = np.array(erow, dtype=[("k", int), ("eta", float), ("seed", int), ("rho", float), ("r2", float), ("sigma", float)])
    np.save(f"{OUT}/reservoir.npy", E)
    L.append(f"## C. Reservoir, delayed recall (n=200, {N_ESN_SEED} seeds)\n")
    L.append("| noise | " + " | ".join(f"k={k}" for k in KS_ESN) + " | alpha (pred 1) | gap x k (pred 0.5) |")
    L.append("|---|" + "---|" * (len(KS_ESN) + 2))
    fig, axes = plt.subplots(1, len(ETAS), figsize=(4 * len(ETAS), 3.4), sharey=True)
    for ax, eta in zip(axes, ETAS):
        gaps = []
        for k in KS_ESN:
            sel = (E["k"] == k) & (E["eta"] == eta)
            curve = np.array([E["r2"][sel & (E["rho"] == r)].mean() for r in RHOS])
            rstar = float(RHOS[int(np.argmax(curve))])
            sig = E["sigma"][sel & (E["rho"] == rstar)].mean()
            gaps.append(1.0 - sig)
            ax.plot(RHOS, curve, "o-", ms=2, label=f"k={k}")
        ax.set_title(f"noise {eta}"); ax.set_xlabel("spectral radius"); ax.axvline(1.0, ls=":", color="k")
        L.append(f"| {eta} | " + " | ".join(f"{g:+.3f}" for g in gaps) + f" | {-loglog_slope(KS_ESN, gaps):+.2f} | {np.nanmean([g*k for g, k in zip(gaps, KS_ESN)]):.2f} |")
    axes[0].set_ylabel("recall R^2"); axes[0].legend(fontsize=6)
    fig.tight_layout(); fig.savefig(f"{OUT}/reservoir_curves.png", dpi=120); plt.close(fig)
    L.append(f"\nElapsed {time.time() - t0:.0f}s.\n")
    open(f"{OUT}/summary.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
