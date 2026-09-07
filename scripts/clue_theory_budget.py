"""Theory scan for a MEASURABLE interior optimum under a shared relay budget: which numbers of
clues, depths, and budgets give a peak accuracy high enough and a drop at full forwarding large
enough that a local-model run of a few dozen instances per point could resolve it. No model calls.
Measured Gemma curves (relay conflict behaviour, confusion) enter through clue_common."""
import sys

import numpy as np

sys.path.insert(0, "scripts")
from clue_common import RELAY_CONFLICT, confusion, layout  # noqa: E402

N, DEG = 40, 3


def layout_k(n, d, depth, k, rng, tries=500):
    from clue_common import bfs_dist, random_regular_graph
    for _ in range(tries):
        adj = random_regular_graph(n, d, rng); t = int(rng.integers(n)); dist = bfs_dist(adj, t)
        cand = [v for v in range(n) if dist[v] == depth]
        if len(cand) >= k:
            return adj, t, [int(x) for x in rng.choice(cand, k, replace=False)]
    raise RuntimeError("layout")


def simulate(depth, k, phi, sigma, cap, rng, n_inst=300, max_relays=2):
    q = sigma / (DEG - 1); acc = []
    for _ in range(n_inst):
        adj, t, src = layout_k(N, DEG, depth, k, rng)
        faulty = set(int(v) for v in np.where(rng.random(N) < phi)[0]) - set(src) - {t}
        inbox = [dict() for _ in range(N)]
        for i, s in enumerate(src):
            inbox[s][i] = {"ok"}
        fresh = {s: set(inbox[s]) for s in src}; relayed = [0] * N; calls = 0
        for _ in range(depth + 2):
            nxt = {}
            for u in list(fresh):
                if u == t or relayed[u] >= max_relays or calls >= cap:
                    continue
                relayed[u] += 1; calls += 1
                note = {}
                for ci, versions in inbox[u].items():
                    v = set(versions)
                    if len(v) > 1:
                        r = rng.random(); v = {"ok", "bad"} if r < RELAY_CONFLICT["both"] else ({"bad"} if r < RELAY_CONFLICT["both"] + RELAY_CONFLICT["wrong_only"] else {"ok"})
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
        all_true = all(i in got and "ok" in got[i] for i in range(k))
        n_bad = sum(1 for i in got if "bad" in got[i])
        acc.append(confusion(n_bad) if all_true else 0.0)
    return float(np.mean(acc))


def main():
    rng = np.random.default_rng(3)
    sig = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
    print("| clues | depth | budget | " + " | ".join(f"s={s}" for s in sig) + " | peak sigma | peak acc | acc at 2.0 | drop |")
    print("|---|---|---|" + "---|" * len(sig) + "---|---|---|---|")
    for k, depth, cap in [(2, 3, 12), (2, 3, 16), (2, 3, 20), (2, 4, 16), (2, 4, 22), (3, 3, 16), (3, 3, 22), (3, 3, 30), (3, 4, 30), (3, 4, 40)]:
        row = [simulate(depth, k, 0.0, s, cap, rng) for s in sig]
        j = int(np.argmax(row))
        print(f"| {k} | {depth} | {cap} | " + " | ".join(f"{a:.2f}" for a in row) + f" | {sig[j]} | {row[j]:.2f} | {row[-1]:.2f} | {row[j] - row[-1]:+.2f} |", flush=True)


if __name__ == "__main__":
    main()
