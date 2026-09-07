"""PILOT for a distributed-clue benchmark with local models. Measures (1) whether one Gemma can
answer with one clue (it should not), with all clues (it should), (2) relay fidelity when an agent
must compress 1 to 3 received notes into one short note, and (3) flooding: answer accuracy when the
target receives the clues buried among M redundant paraphrases. Exploratory; ~130 calls."""
import json
import re
import time
import urllib.request

import numpy as np

MODEL = "gemma3:4b"


def gen(prompt, temp=0.7, max_tokens=80):
    body = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": temp, "num_predict": max_tokens}}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=body, headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=300))["response"].strip()


def instance(rng):
    a, b, c = int(rng.integers(11, 60)), int(rng.integers(3, 20)), int(rng.integers(2, 5))
    clues = [f"The base number is {a}.", f"The key is the base number plus {b}.", f"The code is the key multiplied by {c}."]
    return clues, (a + b) * c, [a, b, c]


ANSWER = ("You are the target agent. Using only the notes below, compute the code step by step, then give the final "
          "line as 'ANSWER: <integer>'.\n\nNotes:\n{notes}")
RELAY = ("You are a relay agent. Combine the notes below into ONE note of at most 25 words for the next agent, "
         "preserving every number and every rule exactly. Output only the note.\n\nNotes:\n{notes}")


def parse_int(s):
    m = re.findall(r"ANSWER:\s*(-?\d+)", s.replace(",", ""))
    if m:
        return int(m[-1])
    m = re.findall(r"-?\d+", s.replace(",", ""))
    return int(m[-1]) if m else None


def main():
    rng = np.random.default_rng(1); t0 = time.time(); L = [f"# Distributed-clue pilot with {MODEL} (exploratory)\n"]
    # 1. single agent with one clue vs all clues
    one, all3 = 0, 0
    for _ in range(12):
        clues, ans, _ = instance(rng)
        one += parse_int(gen(ANSWER.format(notes="- " + clues[0]), max_tokens=200)) == ans
        all3 += parse_int(gen(ANSWER.format(notes="\n".join("- " + c for c in clues)), max_tokens=200)) == ans
    L.append(f"Single agent, one clue: {one}/12 correct. Single agent, all three clues: {all3}/12 correct.\n")
    # 2. relay fidelity
    L.append("| notes received | relays | all numbers preserved |"); L.append("|---|---|---|")
    fid = {}
    for k in [1, 2, 3]:
        ok = 0
        for _ in range(12):
            clues, ans, nums = instance(rng)
            idx = rng.choice(3, k, replace=False)
            out = gen(RELAY.format(notes="\n".join("- " + clues[i] for i in idx)), max_tokens=60)
            ok += all(str(nums[i]) in re.findall(r"\d+", out) for i in idx)
        fid[k] = ok / 12
        L.append(f"| {k} | 12 | {ok}/12 |")
    # 3. flooding: clues among M-3 redundant paraphrases (correct content, varied wording)
    L.append("\n| notes in inbox (3 clues + duplicates) | correct answers |"); L.append("|---|---|")
    para = ["Note: {c}", "Reminder that {c}", "As relayed earlier, {c}", "From another agent: {c}", "Confirming: {c}", "Heard that {c}"]
    flood = {}
    for M in [3, 6, 12, 24, 48]:
        ok = 0
        for _ in range(12):
            clues, ans, _ = instance(rng)
            notes = list(clues)
            while len(notes) < M:
                notes.append(rng.choice(para).format(c=clues[int(rng.integers(3))].lower()))
            rng.shuffle(notes)
            ok += parse_int(gen(ANSWER.format(notes="\n".join("- " + n for n in notes)), max_tokens=260)) == ans
        flood[M] = ok / 12
        L.append(f"| {M} | {ok}/12 |")
    L.append(f"\nElapsed {time.time() - t0:.0f}s.\n")
    open("results/clue_pilot.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main()
