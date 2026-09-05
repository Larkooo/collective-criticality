"""Analysis of a sweep: peak coincidence, data collapse, connectivity-vs-temperature,
and non-predictive information. Writes figures and a markdown summary."""
import json
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

MEAN_F, MAX_F, DIV, NU = 0, 1, 2, 3


def load(path):
    z = np.load(path)
    cfg = json.loads(str(z["cfg"]))
    meta = {k: z[k] for k in ["sweep", "k", "land", "seed", "p", "T", "i_mem", "i_pred", "i_np", "t_conv"]}
    return cfg, meta, z["traj"]


def within_landscape_var(x, lands):
    vs = [x[lands == l].var(ddof=1) for l in np.unique(lands) if (lands == l).sum() > 1]
    return float(np.mean(vs)) if vs else np.nan


def aggregate(meta, traj, sweep, key, horizons):
    """Returns ks, vals, and dict name -> array (len(ks), len(vals), len(horizons))."""
    sel = meta["sweep"] == sweep
    ks = np.unique(meta["k"][sel])
    vals = np.unique(meta[key][sel])
    H = len(horizons)
    out = {n: np.full((len(ks), len(vals), H), np.nan) for n in
           ["perf", "perf_max", "div", "chi_perf", "chi_div", "n_unique"]}
    info = {n: np.full((len(ks), len(vals)), np.nan) for n in ["i_np", "i_mem", "i_pred", "t_conv", "frac_conv"]}
    for i, k in enumerate(ks):
        for j, v in enumerate(vals):
            m = sel & (meta["k"] == k) & (meta[key] == v)
            if not m.any():
                continue
            tr, lands = traj[m], meta["land"][m]
            for h_i, h in enumerate(horizons):
                out["perf"][i, j, h_i] = tr[:, h, MEAN_F].mean()
                out["perf_max"][i, j, h_i] = tr[:, h, MAX_F].mean()
                out["div"][i, j, h_i] = tr[:, h, DIV].mean()
                out["n_unique"][i, j, h_i] = tr[:, h, NU].mean()
                out["chi_perf"][i, j, h_i] = within_landscape_var(tr[:, h, MEAN_F], lands)
                out["chi_div"][i, j, h_i] = within_landscape_var(tr[:, h, DIV], lands)
            for n in ["i_np", "i_mem", "i_pred"]:
                info[n][i, j] = meta[n][m].mean()
            tc = meta["t_conv"][m]
            info["frac_conv"][i, j] = (tc >= 0).mean()
            info["t_conv"][i, j] = tc[tc >= 0].mean() if (tc >= 0).any() else np.nan
    return ks, vals, out, info


def peak(vals, y):
    """Argmax over vals > 0 with 3-point parabolic refinement in log10(vals)."""
    pos = vals > 0
    lv, yy = np.log10(vals[pos]), y[pos]
    if np.all(np.isnan(yy)):
        return np.nan
    j = int(np.nanargmax(yy))
    if 0 < j < len(yy) - 1 and np.isfinite(yy[j - 1:j + 2]).all():
        y0, y1, y2 = yy[j - 1:j + 2]
        denom = y0 - 2 * y1 + y2
        if denom < 0:
            off = 0.5 * (y0 - y2) / denom
            step = lv[j] - lv[j - 1]
            return 10 ** (lv[j] + off * step)
    return 10 ** lv[j]


def xgrid_collapse(vals, curves, scales):
    """Score how well curves (list over K) overlap after x -> x/scale. Lower = better.
    Returns (score, common log-x grid)."""
    logs, ys = [], []
    for c, s in zip(curves, scales):
        pos = (vals > 0) & np.isfinite(c)
        logs.append(np.log10(vals[pos] / s))
        ys.append(c[pos])
    lo, hi = max(l.min() for l in logs), min(l.max() for l in logs)
    if hi <= lo:
        return np.nan, None
    g = np.linspace(lo, hi, 40)
    Y = np.stack([np.interp(g, l, y) for l, y in zip(logs, ys)])
    return float(Y.std(0).mean()), g


def spearman(a, b):
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def analyze(path, figdir):
    os.makedirs(figdir, exist_ok=True)
    cfg, meta, traj = load(path)
    steps, m = cfg["steps"], cfg["n_agents"]
    horizons = sorted({min(h, steps - 1) for h in [25, 50, 100, 200, steps - 1]})
    hnames = [f"t={h}" for h in horizons]
    final = len(horizons) - 1

    ks, ps, P, Pinfo = aggregate(meta, traj, "p", "p", horizons)
    _, Ts, Tg, Tinfo = aggregate(meta, traj, "T", "T", horizons)
    deg = ps * (m - 1)
    colors = plt.cm.viridis(np.linspace(0, 0.9, len(ks)))
    lines = []

    # ---- 1. performance and diversity vs connectivity, by horizon ----
    for name, key, ylabel in [("perf", "perf", "mean fitness / global max"),
                              ("perf_max", "perf_max", "best fitness / global max"),
                              ("div", "div", "diversity (mean pairwise Hamming / n)")]:
        fig, axes = plt.subplots(1, len(horizons), figsize=(3.4 * len(horizons), 3.4), sharey=True)
        for h_i, ax in enumerate(np.atleast_1d(axes)):
            for i, k in enumerate(ks):
                ax.plot(deg, P[key][i, :, h_i], "o-", ms=3, color=colors[i], label=f"K={k}")
            ax.set_xscale("symlog", linthresh=0.5)
            ax.set_title(hnames[h_i]); ax.set_xlabel("mean degree (connectivity)")
        np.atleast_1d(axes)[0].set_ylabel(ylabel); np.atleast_1d(axes)[0].legend(fontsize=8)
        fig.tight_layout(); fig.savefig(f"{figdir}/{name}_vs_connectivity.png", dpi=130); plt.close(fig)

    # ---- 2. susceptibility vs connectivity, peak coincidence ----
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    rows = []
    for i, k in enumerate(ks):
        chi, perf, div = P["chi_perf"][i, :, final], P["perf"][i, :, final], P["div"][i, :, final]
        axes[0].plot(deg, chi * m, "o-", ms=3, color=colors[i], label=f"K={k}")
        axes[1].plot(deg, P["chi_div"][i, :, final] * m, "o-", ms=3, color=colors[i])
        p_chi, p_perf, p_chid = peak(ps, chi), peak(ps, perf), peak(ps, P["chi_div"][i, :, final])
        # where diversity crosses half of its p=0 value: the order-parameter transition
        d0 = div[0]
        cross = np.nan
        pos = ps > 0
        below = np.where(div[pos] < d0 / 2)[0]
        if below.size and below[0] > 0:
            j = below[0]
            x0, x1 = np.log10(ps[pos][j - 1]), np.log10(ps[pos][j])
            y0, y1 = div[pos][j - 1], div[pos][j]
            cross = 10 ** (x0 + (d0 / 2 - y0) / (y1 - y0) * (x1 - x0))
        rows.append((k, p_perf, p_chi, p_chid, cross))
        for ax, pk in [(axes[0], p_chi), (axes[1], p_chid)]:
            if np.isfinite(pk):
                ax.axvline(pk * (m - 1), color=colors[i], ls=":", lw=1)
    for ax, t in zip(axes, ["susceptibility of mean fitness  (N x run-to-run var, within landscape)",
                            "susceptibility of diversity"]):
        ax.set_xscale("symlog", linthresh=0.5); ax.set_xlabel("mean degree"); ax.set_title(t, fontsize=9)
    axes[0].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(f"{figdir}/susceptibility_vs_connectivity.png", dpi=130); plt.close(fig)

    lines.append(f"## Peak coincidence (horizon {hnames[final]}, connectivity as p_link)\n")
    lines.append("| K | p* of mean fitness | p* of chi(fitness) | p* of chi(diversity) | p at diversity half-drop | ratio p*perf / p*chi |")
    lines.append("|---|---|---|---|---|---|")
    for k, pp, pc, pcd, cr in rows:
        ratio = pp / pc if np.isfinite(pp) and np.isfinite(pc) else np.nan
        lines.append(f"| {k} | {pp:.4f} | {pc:.4f} | {pcd:.4f} | {cr:.4f} | {ratio:.2f} |")
    lines.append("")

    # ---- 3. data collapse across K ----
    kk = [i for i, k in enumerate(ks) if k > 0]
    scales_chi = [rows[i][2] for i in kk]
    scales_cross = [rows[i][4] for i in kk]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
    for i in kk:
        axes[0].plot(ps[ps > 0], P["div"][i, ps > 0, final], "o-", ms=3, color=colors[i], label=f"K={ks[i]}")
    axes[0].set_xscale("log"); axes[0].set_title("diversity vs p (raw)", fontsize=9); axes[0].legend(fontsize=8)
    for ax, scales, t in [(axes[1], scales_chi, "x = p / p*_chi(K)"), (axes[2], scales_cross, "x = p / p_half-drop(K)")]:
        for i, s in zip(kk, scales):
            if np.isfinite(s):
                ax.plot(ps[ps > 0] / s, P["div"][i, ps > 0, final], "o-", ms=3, color=colors[i])
        ax.set_xscale("log"); ax.set_title(f"diversity, {t}", fontsize=9)
    for ax in axes:
        ax.set_xlabel("connectivity (rescaled)")
    fig.tight_layout(); fig.savefig(f"{figdir}/collapse_diversity.png", dpi=130); plt.close(fig)

    div_curves = [P["div"][i, :, final] for i in kk]
    perf_curves = [P["perf"][i, :, final] / np.nanmax(P["perf"][i, :, final]) for i in kk]
    ok = [np.isfinite(s) for s in scales_chi]
    lines.append("## Data collapse (spread across K after rescaling x; lower is tighter)\n")
    lines.append("| curve | no rescale | x = p / p*_chi | x = p / p_half-drop |")
    lines.append("|---|---|---|---|")
    for nm, curves in [("diversity", div_curves), ("mean fitness / its max", perf_curves)]:
        s_raw, _ = xgrid_collapse(ps, curves, [1.0] * len(curves))
        s_chi, _ = xgrid_collapse(ps, [c for c, o in zip(curves, ok) if o], [s for s, o in zip(scales_chi, ok) if o])
        okc = [np.isfinite(s) for s in scales_cross]
        s_cr, _ = xgrid_collapse(ps, [c for c, o in zip(curves, okc) if o], [s for s, o in zip(scales_cross, okc) if o])
        lines.append(f"| {nm} | {s_raw:.4f} | {s_chi:.4f} | {s_cr:.4f} |")
    lines.append("")

    # ---- 4. connectivity vs temperature: parametric (diversity, performance) curves ----
    fig, axes = plt.subplots(1, len(ks), figsize=(3.2 * len(ks), 3.4), sharey=True)
    lines.append("## Connectivity vs temperature (final horizon)\n")
    lines.append("Mean distance from each temperature-sweep point to the nearest connectivity-sweep point in the (diversity, mean fitness) plane, per K. Small = the two dials trace the same curve.\n")
    lines.append("| K | mean nearest distance | perf range (p sweep) | perf range (T sweep) |")
    lines.append("|---|---|---|---|")
    for i, (k, ax) in enumerate(zip(ks, np.atleast_1d(axes))):
        dp, fp = P["div"][i, :, final], P["perf"][i, :, final]
        dt, ft = Tg["div"][i, :, final], Tg["perf"][i, :, final]
        ax.plot(dp, fp, "o-", ms=3, color="tab:blue", label="connectivity sweep (T=0)")
        ax.plot(dt, ft, "s--", ms=3, color="tab:red", label="temperature sweep (p=1)")
        ax.set_title(f"K={k}"); ax.set_xlabel("diversity")
        pts_p = np.stack([dp, fp], 1); pts_t = np.stack([dt, ft], 1)
        okp, okt = np.isfinite(pts_p).all(1), np.isfinite(pts_t).all(1)
        d = np.sqrt(((pts_t[okt][:, None, :] - pts_p[okp][None, :, :]) ** 2).sum(-1)).min(1).mean()
        lines.append(f"| {k} | {d:.4f} | {np.nanmin(fp):.3f} to {np.nanmax(fp):.3f} | {np.nanmin(ft):.3f} to {np.nanmax(ft):.3f} |")
    np.atleast_1d(axes)[0].set_ylabel("mean fitness / global max"); np.atleast_1d(axes)[0].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(f"{figdir}/connectivity_vs_temperature.png", dpi=130); plt.close(fig)
    lines.append("")

    # ---- 5. non-predictive information ----
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
    for i, k in enumerate(ks):
        axes[0].plot(deg, Pinfo["i_np"][i], "o-", ms=3, color=colors[i], label=f"K={k}")
        axes[1].plot(deg, Pinfo["i_mem"][i], "o-", ms=3, color=colors[i])
        axes[1].plot(deg, Pinfo["i_pred"][i], "s--", ms=3, color=colors[i])
        axes[2].scatter(Pinfo["i_np"][i], P["perf"][i, :, final], color=colors[i], s=14)
    axes[0].set_title("non-predictive information (bits)", fontsize=9); axes[0].legend(fontsize=8)
    axes[1].set_title("memory (o) and predictive power (s)", fontsize=9)
    axes[2].set_title("final mean fitness vs non-predictive info", fontsize=9)
    for ax in axes[:2]:
        ax.set_xscale("symlog", linthresh=0.5); ax.set_xlabel("mean degree")
    axes[2].set_xlabel("non-predictive information (bits)")
    fig.tight_layout(); fig.savefig(f"{figdir}/nonpredictive_info.png", dpi=130); plt.close(fig)

    lines.append("## Non-predictive information (Still et al. 2012 proxy)\n")
    lines.append("| K | p* of I_np | Spearman(I_np, final mean fitness) over p | Spearman(I_np, chi) |")
    lines.append("|---|---|---|---|")
    for i, k in enumerate(ks):
        inp, pf, chi = Pinfo["i_np"][i], P["perf"][i, :, final], P["chi_perf"][i, :, final]
        okk = np.isfinite(inp) & np.isfinite(pf) & np.isfinite(chi)
        lines.append(f"| {k} | {peak(ps, inp):.4f} | {spearman(inp[okk], pf[okk]):.2f} | {spearman(inp[okk], chi[okk]):.2f} |")
    lines.append("")

    # ---- 6. convergence ----
    lines.append("## Convergence to a single solution (final horizon)\n")
    lines.append("| K | " + " | ".join(f"p={p:g}" for p in ps) + " |")
    lines.append("|---|" + "---|" * len(ps))
    for i, k in enumerate(ks):
        lines.append(f"| {k} | " + " | ".join(f"{fc:.2f}" for fc in Pinfo["frac_conv"][i]) + " |")
    lines.append("\nEntries are the fraction of runs that collapsed to one distinct solution before the end of the run.\n")

    head = [f"# Sweep summary\n", f"config: `{json.dumps(cfg)}`\n",
            f"runs: {len(meta['k'])}, horizons: {hnames}\n"]
    with open(f"{figdir}/summary.md", "w") as fh:
        fh.write("\n".join(head + lines))
    print("\n".join(head + lines))
