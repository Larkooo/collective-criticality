"""Shared pieces for the distributed-clue benchmark: graph, instance, cascade rules."""
import re

import numpy as np

# measured in results/clue_pilot2.md with gemma3:4b: how a relay handles one correct and one
# corrupted copy of the same clue
RELAY_CONFLICT = {"both": 13 / 18, "wrong_only": 4 / 18, "right_only": 1 / 18}
# measured target accuracy with all three true clues present, against the number of corrupted variants
CONFUSION = {0: 12 / 12, 1: 8 / 12, 2: 6 / 12, 3: 3 / 12, 4: 0.0}


def confusion(m):
    return CONFUSION[min(int(m), 4)] if m != 3 else CONFUSION[3]


def random_regular_graph(n, d, rng, tries=2000):
    """Simple d-regular graph on n nodes: pairing model with local re-pairing of bad pairs."""
    for _ in range(tries):
        stubs = list(np.repeat(np.arange(n), d)); rng.shuffle(stubs)
        edges = set(); bad = []
        pairs = [(int(stubs[i]), int(stubs[i + 1])) for i in range(0, len(stubs), 2)]
        for a, b in pairs:
            if a == b or (min(a, b), max(a, b)) in edges:
                bad.append((a, b))
            else:
                edges.add((min(a, b), max(a, b)))
        # try to fix bad pairs by swapping with random good edges
        fixed = True
        for a, b in bad:
            done = False
            for _ in range(200):
                c, e = list(edges)[int(rng.integers(len(edges)))]
                if len({a, b, c, e}) == 4 and (min(a, c), max(a, c)) not in edges and (min(b, e), max(b, e)) not in edges:
                    edges.remove((min(c, e), max(c, e))); edges.add((min(a, c), max(a, c))); edges.add((min(b, e), max(b, e))); done = True; break
            if not done:
                fixed = False; break
        if fixed and len(edges) == n * d // 2:
            adj = [[] for _ in range(n)]
            for a, b in edges:
                adj[a].append(b); adj[b].append(a)
            if all(len(x) == d for x in adj):
                return adj
    raise RuntimeError("no simple regular graph found")


def bfs_dist(adj, s):
    n = len(adj); dist = [-1] * n; dist[s] = 0; q = [s]
    for u in q:
        for v in adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1; q.append(v)
    return dist


def layout(n, d, depth, rng, tries=500):
    """Graph, target, and three sources all at distance `depth` from the target."""
    for _ in range(tries):
        adj = random_regular_graph(n, d, rng)
        t = int(rng.integers(n)); dist = bfs_dist(adj, t)
        cand = [v for v in range(n) if dist[v] == depth]
        if len(cand) >= 3:
            src = [int(x) for x in rng.choice(cand, 3, replace=False)]
            return adj, t, src
    raise RuntimeError("no layout with three sources at that depth")


def instance(rng):
    a, b, c = int(rng.integers(11, 60)), int(rng.integers(3, 20)), int(rng.integers(2, 5))
    clues = [f"The base number is {a}.", f"The key is the base number plus {b}.", f"The code is the key multiplied by {c}."]
    return clues, (a + b) * c, [a, b, c]


def corrupt_number(text, true_nums, rng):
    nums = [int(x) for x in re.findall(r"\d+", text) if int(x) in true_nums]
    if not nums:
        return text
    n = int(rng.choice(nums)); return text.replace(str(n), str(n + int(rng.choice([-7, -3, 2, 5, 9]))), 1)
