"""EXPLORATORY demonstration with a local language model (Ollama): a relay cascade whose
per-hop survival is set by the model's paraphrase fidelity, used to test Theorems 3 and 4 of
docs/FORMAL_STRUCTURE.md on a real, non-synthetic failure process. Not preregistered.

Setup. A briefing with five facts must cross D relay hops. Each carrier that still holds an
intact briefing forwards it to each of 2 next-hop agents with probability q; every forward is a
model call that paraphrases the briefing; a copy is intact if all five facts survive. With per-hop
fidelity p, the number of intact copies per generation is a branching process with binomial(2, qp)
offspring, mean sigma = 2 q p. We measure p, then run cascades at several sigma and compare the
empirical cost per delivery (calls per intact arrival at depth D) with the exact prediction for
that offspring law, and locate both optima.

Run:  uv run python scripts/gemma_relay.py --model gemma3:4b --depth 5 --relays 16
"""
import argparse
import json
import re
import time
import urllib.request

import numpy as np

FACTS = ["dock 47", "18:35", "thursday", "saffron heron", "12 crates", "okafor"]
BRIEFING = ("The convoy leaves from dock 47 at 18:35 on Thursday; the password is 'saffron heron'; "
            "bring 12 crates; the contact is Dr. Okafor.")
PROMPT = ("You are a relay agent. Restate the following briefing for the next agent in your own words, "
          "in at most 30 words, preserving every detail exactly. Output only the restated briefing.\n\n"
          "Briefing: {msg}")


def gen(model, prompt, temp=0.8, max_tokens=90):
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "options": {"temperature": temp, "num_predict": max_tokens}}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=body, headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=300))["response"].strip()


NUMBER_WORDS = {"twelve": "12", "forty-seven": "47", "forty seven": "47"}


def intact(text):
    t = text.lower()
    for w, d in NUMBER_WORDS.items():
        t = t.replace(w, d)
    t = re.sub(r"[^a-z0-9: ]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return all(f in t for f in FACTS)


def relay_hop(model, msg):
    out = gen(model, PROMPT.format(msg=msg))
    return out, intact(out)


def cascade(model, depth, q, rng, cap=40):
    """Returns (delivered, calls). Generation 0 holds the original briefing."""
    carriers = [BRIEFING]
    calls = 0
    for _ in range(depth):
        nxt = []
        for msg in carriers:
            for _ in range(2):
                if rng.random() < q:
                    if calls >= cap:
                        return False, calls
                    out, ok = relay_hop(model, msg); calls += 1
                    if ok:
                        nxt.append(out)
        carriers = nxt
        if not carriers:
            return False, calls
    return True, calls


def exact_prediction(p, depth, sigmas):
    """Exact reach probability, expected calls, and cost per delivery for binomial(2, qp) offspring
    with q = sigma / (2p). Calls are attempted forwards: each intact carrier at generation t makes
    2q forwards on average, so expected calls = (sigma / p) * sum_{t<D} sigma^t."""
    rows = []
    for s in sigmas:
        r = s / 2.0  # per-forward intact probability q * p
        f = lambda x: (1 - r + r * x) ** 2
        qext = 0.0
        for _ in range(depth):
            qext = f(qext)
        reach = 1 - qext
        calls = (s / p) * sum(s ** t for t in range(depth))
        rows.append((s, reach, calls, calls / max(reach, 1e-12)))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gemma3:4b"); ap.add_argument("--depth", type=int, default=5)
    ap.add_argument("--relays", type=int, default=16); ap.add_argument("--p-trials", type=int, default=40)
    ap.add_argument("--sigmas", default="0.6,0.85,1.1"); ap.add_argument("--lam", type=float, default=0.02)
    ap.add_argument("--out", default="results/gemma_relay.md")
    a = ap.parse_args()
    rng = np.random.default_rng(0); t0 = time.time()
    L = [f"# Relay cascade with a local model: {a.model} (exploratory, not preregistered)\n"]

    # 1. per-hop fidelity
    ok = 0; samples = []
    for i in range(a.p_trials):
        out, good = relay_hop(a.model, BRIEFING); ok += good
        if i < 3: samples.append(out)
    p = ok / a.p_trials
    L.append(f"Per-hop fidelity p = {p:.3f} ({ok}/{a.p_trials} single-hop paraphrases kept all {len(FACTS)} facts). Examples:\n")
    L += [f"> {s}\n" for s in samples]

    # 2. cascades at chosen sigma
    sigmas = [float(x) for x in a.sigmas.split(",")]
    L.append(f"\n## Cascades, depth D = {a.depth}, {a.relays} relays per sigma, forwards to 2 next-hop agents with probability q = sigma / (2p)\n")
    L.append("| sigma | q | delivered fraction | mean calls | empirical cost per delivery | exact reach (binomial law, measured p) | exact cost per delivery |")
    L.append("|---|---|---|---|---|---|---|")
    pred = {r[0]: r for r in exact_prediction(p, a.depth, sigmas)}
    emp = {}
    for s in sigmas:
        q = min(s / (2 * p), 1.0)
        res = [cascade(a.model, a.depth, q, rng) for _ in range(a.relays)]
        deliv = np.mean([d for d, _ in res]); calls = np.mean([c for _, c in res])
        cpd = calls / max(deliv, 1e-12); emp[s] = (deliv, calls, cpd)
        L.append(f"| {s} | {q:.3f} | {deliv:.2f} | {calls:.1f} | {cpd:.1f} | {pred[s][1]:.3f} | {pred[s][3]:.1f} |")
    best_emp = min(emp, key=lambda s: emp[s][2]); best_pred = min(pred, key=lambda s: pred[s][3])
    fine = [round(x, 3) for x in np.linspace(0.3, 1.4, 111)]
    fine_pred = exact_prediction(p, a.depth, fine)
    s_thr = min(fine_pred, key=lambda r: r[3])[0]
    one_shot = [(r[0], r[1] - a.lam * (r[2] - 1)) for r in fine_pred]
    s_os, j_os = max(one_shot, key=lambda r: r[1])
    L.append(f"\nThroughput optimum: empirical over the tested grid at sigma = {best_emp}; exact prediction over the tested grid at {best_pred}, over a fine grid at {s_thr:.2f} "
             f"(Theorem 3 asymptotic 1 - 1.59/D = {1 - 1.59 / a.depth:.2f}).")
    L.append(f"One-shot optimum with cost lambda = {a.lam} per call: exact sigma* = {s_os:.2f}, objective {j_os:+.3f}" + (" (silence would be optimal)" if j_os < 0 else "") + ".")
    L.append(f"\nCalls: about {int(a.p_trials + sum(emp[s][1] for s in sigmas) * a.relays)}; elapsed {time.time() - t0:.0f}s.\n")
    L.append("Caveat: this is a demonstration on one briefing with one model. Per-hop failures may be correlated with message content, which the branching law assumes away.\n")
    open(a.out, "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main()
