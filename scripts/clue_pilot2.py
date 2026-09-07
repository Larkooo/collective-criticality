"""PILOT 2: does contradiction hurt? The target receives the 3 correct clues plus m corrupted
variants (one number changed, same wording), shuffled. Also: when a relay receives a correct and a
corrupted version of the same clue, which does it pass on? Exploratory; ~90 calls."""
import json
import re
import time
import urllib.request

import numpy as np

from clue_pilot import ANSWER, RELAY, gen, instance, parse_int


def corrupt(clue, nums, rng):
    n = [x for x in nums if str(x) in clue][0]
    return clue.replace(str(n), str(n + int(rng.choice([-7, -3, 2, 5, 9]))))


def main():
    rng = np.random.default_rng(2); t0 = time.time(); L = ["# Distributed-clue pilot 2: contradictions (exploratory)\n"]
    L.append("| corrupted variants alongside the 3 correct clues | correct answers |"); L.append("|---|---|")
    for m in [0, 1, 2, 4, 8]:
        ok = 0
        for _ in range(12):
            clues, ans, nums = instance(rng)
            notes = list(clues) + [corrupt(clues[int(rng.integers(3))], nums, rng) for _ in range(m)]
            rng.shuffle(notes)
            ok += parse_int(gen(ANSWER.format(notes="\n".join("- " + n for n in notes)), max_tokens=300)) == ans
        L.append(f"| {m} | {ok}/12 |")
    L.append("\n| relay receives | passes on the correct number | passes on the corrupted number | passes on both or neither |"); L.append("|---|---|---|---|")
    good = bad = both = 0
    for _ in range(18):
        clues, ans, nums = instance(rng)
        i = int(rng.integers(3)); c = corrupt(clues[i], nums, rng)
        wrong = [x for x in re.findall(r"\d+", c) if int(x) not in nums][0]
        pair = [clues[i], c]; rng.shuffle(pair)
        out = gen(RELAY.format(notes="\n".join("- " + n for n in pair)), max_tokens=60)
        found = re.findall(r"\d+", out)
        has_ok, has_bad = str(nums[i]) in found, wrong in found
        good += has_ok and not has_bad; bad += has_bad and not has_ok; both += has_ok == has_bad
    L.append(f"| one correct and one corrupted copy of a clue | {good}/18 | {bad}/18 | {both}/18 |")
    L.append(f"\nElapsed {time.time() - t0:.0f}s.\n")
    open("results/clue_pilot2.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main()
