"""Parameter sweeps, run in parallel across (k, landscape) tasks, saved as one .npz.

Two sweeps share every landscape and seed:
  'p'  connectivity sweep: p_link varies, temperature = 0
  'T'  temperature sweep:  p_link = 1 (complete graph), temperature varies
"""
import json
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from .landscape import NK
from .model import run


def default_config(quick: bool = False) -> dict:
    cfg = dict(
        n_bits=20, n_agents=100, steps=500,
        ks=[0, 2, 4, 6, 8, 12],
        p_links=[0.0] + [float(x) for x in np.round(np.logspace(-2.5, 0, 21), 5)],
        temps=[0.0, 0.003, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0],
        n_landscapes=6, n_seeds=8,
    )
    if quick:
        cfg.update(n_bits=16, steps=150, ks=[2, 6],
                   p_links=[0.0, 0.01, 0.03, 0.1, 0.3, 1.0],
                   temps=[0.0, 0.01, 0.1, 1.0], n_landscapes=2, n_seeds=2)
    return cfg


def _task(args):
    cfg, k, li = args
    land = NK(cfg["n_bits"], k, np.random.default_rng([k, li, 1234]))
    rows, trajs = [], []
    for si in range(cfg["n_seeds"]):
        for p in cfg["p_links"]:
            rng = np.random.default_rng([k, li, si, int(round(p * 1e6)), 1])
            r = run(land, cfg["n_agents"], p, 0.0, cfg["steps"], rng)
            rows.append(("p", k, li, si, p, 0.0, r.i_mem, r.i_pred, r.i_np, r.t_converge))
            trajs.append(np.stack([r.mean_f, r.max_f, r.diversity, r.n_unique.astype(np.float32)], 1))
        for T in cfg["temps"]:
            rng = np.random.default_rng([k, li, si, int(round(T * 1e6)), 2])
            r = run(land, cfg["n_agents"], 1.0, T, cfg["steps"], rng)
            rows.append(("T", k, li, si, 1.0, T, r.i_mem, r.i_pred, r.i_np, r.t_converge))
            trajs.append(np.stack([r.mean_f, r.max_f, r.diversity, r.n_unique.astype(np.float32)], 1))
    return rows, trajs


def run_sweep(cfg: dict, out: str, workers: int | None = None) -> None:
    tasks = [(cfg, k, li) for k in cfg["ks"] for li in range(cfg["n_landscapes"])]
    per_task = cfg["n_seeds"] * (len(cfg["p_links"]) + len(cfg["temps"]))
    print(f"{len(tasks)} tasks x {per_task} runs x {cfg['steps']} steps", flush=True)
    t0 = time.time()
    all_rows, all_trajs = [], []
    with ProcessPoolExecutor(workers) as ex:
        for i, (rows, trajs) in enumerate(ex.map(_task, tasks), 1):
            all_rows += rows
            all_trajs += trajs
            print(f"  task {i}/{len(tasks)} done  ({time.time() - t0:.0f}s)", flush=True)
    cols = list(zip(*all_rows))
    np.savez_compressed(
        out,
        cfg=json.dumps(cfg),
        sweep=np.array(cols[0]), k=np.array(cols[1]), land=np.array(cols[2]), seed=np.array(cols[3]),
        p=np.array(cols[4]), T=np.array(cols[5]),
        i_mem=np.array(cols[6]), i_pred=np.array(cols[7]), i_np=np.array(cols[8]), t_conv=np.array(cols[9]),
        traj=np.stack(all_trajs).astype(np.float32),
    )
    print(f"saved {out}  ({len(all_rows)} runs, {time.time() - t0:.0f}s)")
