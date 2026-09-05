"""EXPLORATORY, not preregistered. Saves the check that was previously run inline and unsaved.

For each landscape used in study spread-vs-search, run the island model at m = 0 (isolated
islands), collect each island's final best fitness (the isolated-endpoint distribution F_L),
and compute the exact expected maximum of G i.i.d. draws from the empirical F_L:

    E[M_G | L] = sum_i x_(i) * [(i/n)^G - ((i-1)/n)^G]

which is the discrete form of  integral (1 - F_L(x)^G) dx. Compare with the study-2 plateau of
final MEAN fitness at n_trials = 1. Two cautions, both raised in external review: the plateau
value is a maximum over noisy grid points and is biased upward; and the plateau is a mean-agent
metric while the order-statistic reference is a best-found quantity, so agreement requires the
best to have spread to (nearly) everyone. Also reports the endpoint spread sigma_L against the
spread of the population mean, which are different quantities."""
import numpy as np

from critpop.landscape import NK
from critpop.model import run

KS, G, N, STEPS, N_LAND, N_SEED = [2, 6, 12], 10, 100, 500, 4, 6
MS = [0.0] + [float(x) for x in np.logspace(-3, 0, 13)]


def exact_expected_max(pool: np.ndarray, g: int) -> float:
    x = np.sort(pool)
    n = x.size
    i = np.arange(1, n + 1)
    return float((x * ((i / n) ** g - ((i - 1) / n) ** g)).sum())


def main():
    d = np.load("results/study2/runs.npy")
    lines = ["# Exploratory order-statistic check (not preregistered)\n",
             f"Isolated islands (m = 0), G = {G} islands of {N // G}, {N_LAND} landscapes x {N_SEED} seeds, {STEPS} steps.",
             "Endpoint = each island's best final fitness. E[max of G] is exact from the empirical endpoint CDF per landscape, then averaged over landscapes.\n",
             "| K | mean endpoint mu_L | endpoint sd sigma_L | sd of population mean at m=0 | E[max of 10] exact | study-2 plateau (max over interior m, biased up) | study-2 perf at m = 0.0316 (fixed grid point) | study-2 perf at m = 1 |",
             "|---|---|---|---|---|---|---|---|"]
    store, gaps = {}, []
    for k in KS:
        ex, mu, sd, popsd = [], [], [], []
        for li in range(N_LAND):
            land = NK(20, k, np.random.default_rng([k, li, 1234]))
            pool, means = [], []
            for si in range(N_SEED):
                r = run(land, N, 0.0, 0.0, STEPS, np.random.default_rng([k, li, si, 1, 0, 11]),
                        islands=G, migration=0.0, n_trials=1, return_state=True)
                isl = np.arange(N) // (N // G)
                pool += [float(r.final_f[isl == g].max()) for g in range(G)]
                means.append(float(r.final_f.mean()))
            pool = np.array(pool)
            store[f"K{k}_L{li}_endpoints"] = pool
            ex.append(exact_expected_max(pool, G)); mu.append(pool.mean()); sd.append(pool.std(ddof=1)); popsd.append(np.std(means, ddof=1))
        sel = (d["sweep"] == "A") & (d["k"] == k) & (d["nt"] == 1)
        curve = np.array([d["perf"][sel & (d["m"] == m)].mean() for m in MS])
        fixed = curve[np.argmin(np.abs(np.array(MS) - 0.0316))]
        lines.append(f"| {k} | {np.mean(mu):.4f} | {np.mean(sd):.4f} | {np.mean(popsd):.4f} | {np.mean(ex):.4f} | {curve[1:-1].max():.4f} | {fixed:.4f} | {curve[-1]:.4f} |")
        gaps.append((float(np.mean(ex)), float(curve[1:-1].max()), float(fixed)))
    gaps_plateau = [row[1] - row[0] for row in gaps]
    gaps_fixed = [row[2] - row[0] for row in gaps]
    lines.append("\nGaps against the exact reference, in units of the global maximum:")
    lines.append(f"- plateau maximum minus reference: {', '.join(f'{g:+.4f}' for g in gaps_plateau)} for K = {KS} (biased upward by selection over the grid)")
    lines.append(f"- fixed grid point m = 0.0316 minus reference: {', '.join(f'{g:+.4f}' for g in gaps_fixed)} for K = {KS}")
    lines.append("Not all gaps lie within 0.010. Whether the discrepancy is selection bias, a real bonus from copying a higher "
                 "mid-climb point, or the mean-versus-best metric difference is what study 3 must separate, with a best-found "
                 "metric, ancestry-measured lineage counts, disjoint calibration runs, and an out-of-sample prediction.\n")
    np.savez_compressed("results/exploratory/island_endpoints.npz", **store)
    open("results/exploratory/order_stat_check.md", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
