# Reviewing this repository

This is a research repository run under a preregistration method. The most useful review is one that tries to kill a claim. Here is where the claims are and how to attack them.

## What is claimed, in order of strength

1. **Established mathematics, cited, not claimed as new.** The expectation of a maximum of independent draws and the Hartley–David bound (`docs/FORMAL_NOTE.md`, Section 2).
2. **Recorded study outcomes.** `studies/*/verdict.yaml`, computed from `studies/*/study.yaml` by `sever verdict`. Study 1 is an exploratory rejection; study 2 is inconclusive. Neither supports the order-statistic account; study 2 supports only that an interior optimum exists in the island topology.
3. **Exploratory observations.** `results/exploratory/`, `results/*/summary.md` sections marked exploratory, and `results.exploratory` in each study file. These are hypotheses.
4. **Plans.** `docs/CONVERGENCE_FINAL.md`, `docs/FORMAL_NOTE.md`, `docs/PAPER_OUTLINE.md`. Nothing in them is a result.

If a sentence anywhere in the repository reads as stronger than its category, that is a defect. Please report it with the sentence.

## Check the preregistrations

```
uv run sever status
uv run sever check spread-vs-search        # the hash of the frozen sections must match the working copy and the named commit
git show <freeze commit>:studies/spread-vs-search/study.yaml   # read the predictions as they were before data
```

`studies/optimum-at-transition` was never frozen. It says so in its file and its verdict is excluded from calibration.

## Reproduce a number

Every number in `results/figures/summary.md`, `results/finite_size.md`, `results/study2/summary.md`, and `results/exploratory/order_stat_check.md` comes from one command listed in the README. Seeds are deterministic. If a rerun disagrees, that is a finding; open an issue with the command, platform, numpy version, and the two values.

## Attack the model

`critpop/model.py` is short. Things a reviewer has caught before and we would like caught again: dynamics where copying and climbing are mutually exclusive in a step, so migration changes the number of fitness evaluations at a fixed horizon; a mean-agent metric being compared with a best-found reference; terminal ancestry being read as a count of independent searches. The last two are now documented in the model file and the formal note. Similar mistakes elsewhere are likely.

## Attack the plan

`docs/FORMAL_NOTE.md` Section 4 states the assumptions A1 to A4 that connect interacting search to the reference distribution. A3 is load-bearing. If you can construct a case where A1 to A4 hold and the prediction in that section fails, or a case where the planned Control E cannot detect a violation of A3, that is the most valuable review this project can receive right now.

## How to object

Write the objection in the form the method uses: the strongest version of the objection, the confounds you checked, and what would change your mind. Open an issue, or add it under `review:` in the relevant study file in a pull request. Do not edit anything above `results:` in a frozen study; propose a new version instead.
