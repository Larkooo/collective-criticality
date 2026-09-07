"""Theory side of the distributed-clue benchmark: the same cascade with mechanical relays whose
conflict behaviour and target confusion are the MEASURED curves from the pilots. No model calls.
Predicts accuracy, calls, and the objective against sigma for each depth and fault rate, and the
location of the optimum. This is J = V - C with V and C fixed independently of the confirmatory
data, as the method requires."""
import sys

import numpy as np

sys.path.insert(0, "scripts")
from clue_common import RELAY_CONFLICT, bfs_dist, confusion, layout  # noqa: E402

N, DEG = 40, 3


def simulate(depth, phi, sigma, rng, n_inst=400, lam=0.002):
    q = sigma / (DEG - 1)
    acc, calls_all = [], []
    for _ in range(n_inst):
        adj, t, src = layout(N, DEG, depth, rng)
        faulty = set(int(v) for v in np.where(rng.random(N) < phi)[0]) - set(src) - {t}
        # each note is a dict clue_index -> set of versions ('ok' or 'bad'); agents hold a merged inbox
        inbox = [dict() for _ in range(N)]
        for i, s in enumerate(src):
            inbox[s][i] = {"ok"}
        fresh = {s: set(inbox[s]) for s in src}   # agents with unrelayed new clues
        relayed = [0] * N; calls = 0
        for _ in range(depth + 2):
            nxt = {}
            for u, new_clues in fresh.items():
                if u == t or relayed[u] >= 2:
                    continue
                relayed[u] += 1; calls += 1  # one relay note per activation
                note = {}
                for ci, versions in inbox[u].items():
                    v = set(versions)
                    if len(v) > 1:  # conflicting copies: measured relay behaviour
                        r = rng.random()
                        v = {"ok", "bad"} if r < RELAY_CONFLICT["both"] else ({"bad"} if r < RELAY_CONFLICT["both"] + RELAY_CONFLICT["wrong_only"] else {"ok"})
                    if u in faulty:
                        v = {"bad"} if v == {"ok"} else v
                    note[ci] = v
                for w in adj[u]:
                    if rng.random() < q:
                        changed = set()
                        for ci, v in note.items():
                            before = inbox[w].get(ci, set())
                            if not v <= before:
                                changed.add(ci)
                            inbox[w][ci] = before | v
                        if changed and w != t:
                            nxt.setdefault(w, set()).update(changed)
            fresh = nxt
        got = inbox[t]
        all_true = all(i in got and "ok" in got[i] for i in range(3))
        n_bad = sum(1 for i in got if "bad" in got[i])
        acc.append(confusion(n_bad) if all_true else 0.0)
        calls_all.append(calls + 1)
    return float(np.mean(acc)), float(np.mean(calls_all)), float(np.mean(acc) - lam * np.mean(calls_all))


def main():
    rng = np.random.default_rng(0)
    sig = [0.5, 0.7, 0.9, 1.0, 1.1, 1.3, 1.5, 1.8, 2.0]
    L = ["# Theory prediction for the distributed-clue benchmark (mechanical cascade, measured curves)\n"]
    for depth in [3, 4, 6]:
        for phi in [0.0, 0.15, 0.3]:
            L.append(f"## depth {depth}, fault rate {phi}\n")
            L.append("| sigma | predicted accuracy | predicted calls | objective (acc - 0.002 calls) |"); L.append("|---|---|---|---|")
            rows = [(s, *simulate(depth, phi, s, rng)) for s in sig]
            for s, a, c, j in rows:
                L.append(f"| {s} | {a:.3f} | {c:.1f} | {j:+.3f} |")
            best_acc = max(rows, key=lambda r: r[1]); best_j = max(rows, key=lambda r: r[3])
            L.append(f"\npredicted optimum: accuracy at sigma = {best_acc[0]} ({best_acc[1]:.3f}); objective at sigma = {best_j[0]}\n")
    open("results/clue_theory.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main()
