# spread-vs-search: results

3672 runs in 137s. K [2, 6, 12], n_trials [1, 2, 4], m grid 14 points, T grid 9 points, 4 landscapes x 6 seeds, 500 steps, N=100, G=10.

## Optimum location m* (parabolic refinement in log10 m)

| K | m*(nt=1) | m*(nt=2) | m*(nt=4) | ratio m*(4)/m*(1) | bootstrap 90% of ratio |
|---|---|---|---|---|---|
| 2 | 0.0053 | 0.0017 | 0.0212 | 4.00 | [1.12, 23.33] |
| 6 | 0.0032 | 0.0113 | 0.0199 | 6.26 | [0.38, 6.51] |
| 12 | 0.0031 | 0.0029 | 0.0016 | 0.53 | [0.03, 43.16] |

P1 ratios [4.0, 6.26, 0.53] -> **inconclusive**. P3 max/min of m* across K at nt=1 = 1.71 -> **inconclusive**.

## Interior optimum (nt = 1)

| K | perf(m=0) | perf(m=1) | best interior | gain over both endpoints |
|---|---|---|---|---|
| 2 | 0.9512 | 0.9792 | 0.9948 | +0.0156 |
| 6 | 0.8797 | 0.9280 | 0.9536 | +0.0256 |
| 12 | 0.8436 | 0.8735 | 0.9286 | +0.0551 |

P2 -> **pass**.

## Connectivity vs temperature at matched spread rate r (nt = 1)

| K | r range, m sweep | r range, T sweep | coverage | mean abs perf difference |
|---|---|---|---|---|
| 2 | 0.0116 to 0.0142 | 0.0077 to 0.0091 | 0.00 | nan |
| 6 | 0.0082 to 0.0117 | 0.0051 to 0.0064 | 0.00 | nan |
| 12 | 0.0054 to 0.0090 | 0.0034 to 0.0042 | 0.00 | nan |

P4 -> **inconclusive**.

## Collapse across n_trials against r / n_trials

| K | spread vs r | spread vs r/n_trials | ratio |
|---|---|---|---|
| 2 | 0.0054 | nan | nan |
| 6 | 0.0083 | nan | nan |
| 12 | 0.0061 | nan | nan |

P5 -> **inconclusive**.

## Outcomes, applied literally

- P1: inconclusive
- P2: pass
- P3: inconclusive
- P4: inconclusive
- P5: inconclusive
