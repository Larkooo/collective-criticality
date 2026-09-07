"""Distributed-clue benchmark with a local model: the cascade of clue_theory.py, but every relay
note is written by the model and the target's answer is the model's. Records accuracy, calls, and
what reached the target. Usage: uv run python scripts/clue_network.py --depth 4 --phi 0.2 --sigmas 0.8,1.4 --inst 3"""
import argparse
import json
import re
import sys
import time
import urllib.request

import numpy as np

sys.path.insert(0, "scripts")
from clue_common import bfs_dist, corrupt_number, instance, layout  # noqa: E402

N, DEG, MODEL = 40, 3, "gemma3:4b"
RELAY = ("You are a relay agent. Combine the notes below into ONE note of at most 30 words for the next agent, "
         "preserving every number and every rule exactly. Output only the note.\n\nNotes:\n{notes}")
ANSWER = ("You are the target agent. Using only the notes below, compute the code step by step, then give the final "
          "line as 'ANSWER: <integer>'.\n\nNotes:\n{notes}")


def gen(prompt, temp=0.7, max_tokens=80):
    body = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": temp, "num_predict": max_tokens}}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=body, headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=300))["response"].strip()


def parse_int(s):
    m = re.findall(r"ANSWER:\s*(-?\d+)", s.replace(",", ""))
    if m:
        return int(m[-1])
    m = re.findall(r"-?\d+", s.replace(",", ""))
    return int(m[-1]) if m else None


def run_instance(depth, phi, sigma, rng, cap=120):
    q = sigma / (DEG - 1)
    adj, t, src = layout(N, DEG, depth, rng)
    clues, ans, nums = instance(rng)
    faulty = set(int(v) for v in np.where(rng.random(N) < phi)[0]) - set(src) - {t}
    inbox = [[] for _ in range(N)]
    for i, s in enumerate(src):
        inbox[s].append(clues[i])
    fresh = set(src); relayed = [0] * N; calls = 0
    for _ in range(depth + 2):
        nxt = set()
        for u in fresh:
            if u == t or relayed[u] >= 2 or calls >= cap:
                continue
            relayed[u] += 1
            note = gen(RELAY.format(notes="\n".join("- " + n for n in inbox[u][-12:])), max_tokens=70); calls += 1
            if u in faulty:
                note = corrupt_number(note, nums, rng)
            for w in adj[u]:
                if rng.random() < q:
                    inbox[w].append(note)
                    if w != t:
                        nxt.add(w)
        fresh = nxt
    notes_t = inbox[t]
    if not notes_t:
        return dict(correct=False, calls=calls, n_notes=0, n_bad=0, all_true=False)
    out = gen(ANSWER.format(notes="\n".join("- " + n for n in notes_t[-40:])), max_tokens=320); calls += 1
    found = set(int(x) for x in re.findall(r"\d+", " ".join(notes_t)))
    all_true = all(n in found for n in nums)
    n_bad = len([x for x in found if x not in nums])
    return dict(correct=parse_int(out) == ans, calls=calls, n_notes=len(notes_t), n_bad=n_bad, all_true=all_true)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--depth", type=int, default=4); ap.add_argument("--phi", type=float, default=0.2)
    ap.add_argument("--sigmas", default="0.8,1.4"); ap.add_argument("--inst", type=int, default=3); ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--out", default="results/clue_network_pilot.md")
    a = ap.parse_args(); rng = np.random.default_rng(a.seed); t0 = time.time()
    L = [f"# Distributed-clue network run with {MODEL}: depth {a.depth}, fault rate {a.phi}, {a.inst} instances per sigma\n",
         "| sigma | accuracy | mean calls | mean notes at target | mean corrupted numbers at target | all clues arrived |", "|---|---|---|---|---|---|"]
    for s in [float(x) for x in a.sigmas.split(",")]:
        rs = [run_instance(a.depth, a.phi, s, rng) for _ in range(a.inst)]
        L.append(f"| {s} | {np.mean([r['correct'] for r in rs]):.2f} | {np.mean([r['calls'] for r in rs]):.1f} | {np.mean([r['n_notes'] for r in rs]):.1f} | "
                 f"{np.mean([r['n_bad'] for r in rs]):.1f} | {np.mean([r['all_true'] for r in rs]):.2f} |")
        print(L[-1], flush=True)
    L.append(f"\nElapsed {time.time() - t0:.0f}s.\n")
    open(a.out, "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main()
