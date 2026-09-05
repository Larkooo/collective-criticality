"""Study spread-vs-search (studies/spread-vs-search/study.yaml). Runs sweeps A and B from the
frozen analysis plan, evaluates each prediction's criteria literally, and writes
results/study2/summary.md plus figures. The criteria here mirror the frozen study file."""
import os
import time
from concurrent.futures import ProcessPoolExecutor

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from critpop.analyze import peak  # noqa: E402
from critpop.landscape import NK  # noqa: E402
from critpop.model import run  # noqa: E402

KS, NTS = [2, 6, 12], [1, 2, 4]
MS = [0.0] + [float(x) for x in np.logspace(-3, 0, 13)]
TEMPS = [0.0, 0.003, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
N_LAND, N_SEED, STEPS, N, G = 4, 6, 500, 100, 10
OUT = "results/study2"
DT = [("sweep", "U1"), ("k", int), ("land", int), ("seed", int), ("nt", int), ("m", float), ("T", float),
      ("perf", float), ("r", float), ("visited", float), ("tconv", int)]


def task(args):
    k, li = args
    land = NK(20, k, np.random.default_rng([k, li, 1234]))
    rows = []
    for si in range(N_SEED):
        for nt in NTS:
            for m in MS:
                rng = np.random.default_rng([k, li, si, nt, int(round(m * 1e6)), 11])
                r = run(land, N, 0.0, 0.0, STEPS, rng, islands=G, migration=m, n_trials=nt)
                rows.append(("A", k, li, si, nt, m, 0.0, float(r.mean_f[-1]), r.copy_rate, r.visited, r.t_converge))
        for T in TEMPS:
            rng = np.random.default_rng([k, li, si, 1, int(round(T * 1e6)), 12])
            r = run(land, N, 1.0, T, STEPS, rng)
            rows.append(("B", k, li, si, 1, 1.0, T, float(r.mean_f[-1]), r.copy_rate, r.visited, r.t_converge))
    return rows


def per_land_curves(d, k, nt, key, vals, field="perf"):
    """(N_LAND, len(vals)) mean over seeds, per landscape."""
    sel = (d["sweep"] == ("A" if key == "m" else "B")) & (d["k"] == k) & (d["nt"] == nt)
    return np.array([[d[field][sel & (d["land"] == li) & (d[key] == v)].mean() for v in vals] for li in range(N_LAND)])


def mstar_from(curves):
    return peak(np.array(MS), curves.mean(0))


def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    tasks = [(k, li) for k in KS for li in range(N_LAND)]
    with ProcessPoolExecutor() as ex:
        rows = [r for res in ex.map(task, tasks) for r in res]
    d = np.array(rows, dtype=DT)
    np.save(f"{OUT}/runs.npy", d)
    L = [f"# spread-vs-search: results\n", f"{len(d)} runs in {time.time() - t0:.0f}s. K {KS}, n_trials {NTS}, "
         f"m grid {len(MS)} points, T grid {len(TEMPS)} points, {N_LAND} landscapes x {N_SEED} seeds, {STEPS} steps, N={N}, G={G}.\n"]
    outcomes = {}
    rng = np.random.default_rng(0)
    boot_idx = rng.integers(0, N_LAND, (200, N_LAND))

    # ---- m* table, P1, P3 ----
    mstar = {(k, nt): mstar_from(per_land_curves(d, k, nt, "m", MS)) for k in KS for nt in NTS}
    L.append("## Optimum location m* (parabolic refinement in log10 m)\n")
    L.append("| K | m*(nt=1) | m*(nt=2) | m*(nt=4) | ratio m*(4)/m*(1) | bootstrap 90% of ratio |")
    L.append("|---|---|---|---|---|---|")
    ratios = {}
    for k in KS:
        c1, c4 = per_land_curves(d, k, 1, "m", MS), per_land_curves(d, k, 4, "m", MS)
        bs = np.array([mstar_from(c4[b]) / mstar_from(c1[b]) for b in boot_idx])
        ratios[k] = mstar[(k, 4)] / mstar[(k, 1)]
        lo, hi = np.nanpercentile(bs, [5, 95])
        L.append(f"| {k} | {mstar[(k, 1)]:.4f} | {mstar[(k, 2)]:.4f} | {mstar[(k, 4)]:.4f} | {ratios[k]:.2f} | [{lo:.2f}, {hi:.2f}] |")
    rv = np.array([ratios[k] for k in KS])
    if (rv >= 1.5).sum() >= 2 and (rv >= 1.0).all():
        outcomes["P1"] = "pass"
    elif (rv <= 1.1).sum() >= 2:
        outcomes["P1"] = "fail"
    else:
        outcomes["P1"] = "inconclusive"
    m1 = np.array([mstar[(k, 1)] for k in KS])
    r3 = m1.max() / m1.min()
    outcomes["P3"] = "pass" if r3 <= 1.5 else ("fail" if r3 >= 3 else "inconclusive")
    L.append(f"\nP1 ratios {np.round(rv, 2).tolist()} -> **{outcomes['P1']}**. P3 max/min of m* across K at nt=1 = {r3:.2f} -> **{outcomes['P3']}**.\n")

    # ---- P2 ----
    L.append("## Interior optimum (nt = 1)\n")
    L.append("| K | perf(m=0) | perf(m=1) | best interior | gain over both endpoints |")
    L.append("|---|---|---|---|---|")
    gains = {}
    for k in KS:
        c = per_land_curves(d, k, 1, "m", MS).mean(0)
        best_int = c[1:-1].max()
        gains[k] = best_int - max(c[0], c[-1])
        L.append(f"| {k} | {c[0]:.4f} | {c[-1]:.4f} | {best_int:.4f} | {gains[k]:+.4f} |")
    if all(gains[k] >= 0.005 for k in (6, 12)):
        outcomes["P2"] = "pass"
    elif any(gains[k] < 0.002 for k in (6, 12)):
        outcomes["P2"] = "fail"
    else:
        outcomes["P2"] = "inconclusive"
    L.append(f"\nP2 -> **{outcomes['P2']}**.\n")

    # ---- P4 ----
    L.append("## Connectivity vs temperature at matched spread rate r (nt = 1)\n")
    L.append("| K | r range, m sweep | r range, T sweep | coverage | mean abs perf difference |")
    L.append("|---|---|---|---|---|")
    cov, mad = {}, {}
    fig, axes = plt.subplots(1, len(KS), figsize=(4 * len(KS), 3.6), sharey=False)
    for ax, k in zip(axes, KS):
        rA = per_land_curves(d, k, 1, "m", MS, "r").mean(0); pA = per_land_curves(d, k, 1, "m", MS).mean(0)
        rB = per_land_curves(d, k, 1, "T", TEMPS, "r").mean(0); pB = per_land_curves(d, k, 1, "T", TEMPS).mean(0)
        o = np.argsort(rA)
        lo, hi = max(rA.min(), rB.min()), min(rA.max(), rB.max())
        cov[k] = max(0.0, hi - lo) / (rA.max() - rA.min())
        inside = (rB >= rA.min()) & (rB <= rA.max())
        mad[k] = float(np.abs(np.interp(np.log10(rB[inside]), np.log10(rA[o]), pA[o]) - pB[inside]).mean()) if inside.any() else np.nan
        L.append(f"| {k} | {rA.min():.4f} to {rA.max():.4f} | {rB.min():.4f} to {rB.max():.4f} | {cov[k]:.2f} | {mad[k]:.4f} |")
        ax.plot(rA[o], pA[o], "o-", ms=3, label="island m sweep"); ax.plot(rB, pB, "s--", ms=3, label="complete graph, T sweep")
        ax.set_xscale("log"); ax.set_xlabel("spread rate r (agents adopting a different solution per step)"); ax.set_title(f"K={k}")
    axes[0].set_ylabel("final mean fitness / global max"); axes[0].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(f"{OUT}/p4_spread_rate.png", dpi=130); plt.close(fig)
    if all(cov[k] >= 0.5 for k in KS) and all(mad[k] < 0.005 for k in KS):
        outcomes["P4"] = "pass"
    elif all(cov[k] >= 0.5 for k in KS) and any(mad[k] > 0.01 for k in KS):
        outcomes["P4"] = "fail"
    else:
        outcomes["P4"] = "inconclusive"
    L.append(f"\nP4 -> **{outcomes['P4']}**.\n")

    # ---- P5 ----
    L.append("## Collapse across n_trials against r / n_trials\n")
    L.append("| K | spread vs r | spread vs r/n_trials | ratio |")
    L.append("|---|---|---|---|")
    ratio5 = {}
    fig, axes = plt.subplots(2, len(KS), figsize=(4 * len(KS), 6.8))
    for j, k in enumerate(KS):
        curves = {nt: (per_land_curves(d, k, nt, "m", MS, "r").mean(0), per_land_curves(d, k, nt, "m", MS).mean(0)) for nt in NTS}
        spreads = {}
        for row, scale in enumerate([False, True]):
            xs = {nt: (r / nt if scale else r) for nt, (r, p) in curves.items()}
            lo = max(np.log10(x.min()) for x in xs.values()); hi = min(np.log10(x.max()) for x in xs.values())
            if hi > lo:
                g = np.linspace(lo, hi, 30)
                Y = np.stack([np.interp(g, np.log10(np.sort(xs[nt])), curves[nt][1][np.argsort(xs[nt])]) for nt in NTS])
                spreads[scale] = float(Y.std(0).mean())
            else:
                spreads[scale] = np.nan
            ax = axes[row, j]
            for nt in NTS:
                o = np.argsort(xs[nt]); ax.plot(xs[nt][o], curves[nt][1][o], "o-", ms=3, label=f"n_trials={nt}")
            ax.set_xscale("log"); ax.set_xlabel("r / n_trials" if scale else "r"); ax.set_title(f"K={k}" if row == 0 else "")
        ratio5[k] = spreads[True] / spreads[False] if spreads[False] else np.nan
        L.append(f"| {k} | {spreads[False]:.4f} | {spreads[True]:.4f} | {ratio5[k]:.2f} |")
    axes[0, 0].legend(fontsize=7); axes[0, 0].set_ylabel("final mean fitness"); axes[1, 0].set_ylabel("final mean fitness")
    fig.tight_layout(); fig.savefig(f"{OUT}/p5_collapse.png", dpi=130); plt.close(fig)
    r5 = np.array([ratio5[k] for k in KS])
    if np.all(r5 <= 0.5):
        outcomes["P5"] = "pass"
    elif (r5 >= 0.8).sum() >= 2:
        outcomes["P5"] = "fail"
    else:
        outcomes["P5"] = "inconclusive"
    L.append(f"\nP5 -> **{outcomes['P5']}**.\n")

    # ---- performance vs m figure ----
    fig, axes = plt.subplots(1, len(KS), figsize=(4 * len(KS), 3.6))
    for ax, k in zip(axes, KS):
        for nt in NTS:
            c = per_land_curves(d, k, nt, "m", MS).mean(0)
            ax.plot(MS, c, "o-", ms=3, label=f"n_trials={nt}")
            ax.axvline(mstar[(k, nt)], ls=":", lw=1, color=ax.lines[-1].get_color())
        ax.set_xscale("symlog", linthresh=1e-3); ax.set_xlabel("cross-island observation rate m"); ax.set_title(f"K={k}")
    axes[0].set_ylabel("final mean fitness / global max"); axes[0].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(f"{OUT}/perf_vs_m.png", dpi=130); plt.close(fig)

    L.append("## Outcomes, applied literally\n")
    for pid in ["P1", "P2", "P3", "P4", "P5"]:
        L.append(f"- {pid}: {outcomes[pid]}")
    with open(f"{OUT}/summary.md", "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
