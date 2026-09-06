# Design pilot: task-set gap (excluded seeds; not confirmatory)

## A. Branching process (exact generating function)

| L | one-shot delta*, lambda=1e-3 | one-shot delta*, lambda=4e-3 | throughput delta* | throughput delta* x L |
|---|---|---|---|---|
| 2 | 0.0428 | 0.0847 | 0.3991 | 0.798 |
| 4 | 0.0382 | 0.0770 | 0.2589 | 1.036 |
| 8 | 0.0362 | 0.0758 | 0.1541 | 1.233 |
| 16 | 0.0367 | nan | 0.0859 | 1.375 |
| 32 | 0.0429 | nan | 0.0458 | 1.467 |
| 64 | nan | nan | 0.0238 | 1.523 |

fitted alpha (one-shot, lambda=1e-3, where an optimum exists): +0.01  predicted 0; sqrt(lambda) = 0.0316 vs mean delta* 0.0394; ratio of gaps for 4x cost: 2.01 (predicted 2.0)
fitted alpha (throughput): +0.82  predicted 1; delta* x L -> 1.239 (predicted 1.59 near-critical; exact differs at small L)

## B. Population model, islands (K=6, N=100, 3 excluded landscapes x 4 seeds)

| T | dial* | sigma_meas at dial* | gap = sigma-1 | gap x T | ln G / T | dial* with adoption cost 0.002 | with 0.005 |
|---|---|---|---|---|---|---|---|
| 125 | 0.03196 | 1.743 | +0.743 [+0.645, +0.875] | 92.9 | 0.0184 | 0.03258 | 0.03352 |
| 250 | 0.01894 | 1.333 | +0.333 [+0.016, +0.300] | 83.1 | 0.0092 | 0.0188 | 0.01859 |
| 500 | 0.001813 | 1.014 | +0.014 [+0.012, +0.017] | 6.8 | 0.0046 | 0.001816 | 0.001819 |
| 1000 | 0.01093 | 1.096 | +0.096 [+0.016, +0.103] | 95.6 | 0.0023 | 0.011 | 0.01109 |
| 2000 | 0.001146 | 1.013 | +0.013 [+0.010, +0.017] | 26.4 | 0.0012 | 0.001138 | 0.001127 |

fitted alpha of gap vs T: +1.34  predicted 1

## B. Population model, er (K=6, N=100, 3 excluded landscapes x 4 seeds)

| T | dial* | sigma_meas at dial* | gap = sigma-1 | gap x T | ln G / T | dial* with adoption cost 0.002 | with 0.005 |
|---|---|---|---|---|---|---|---|
| 125 | 0.03935 | 2.922 | +1.922 [+0.903, +3.542] | 240.2 | 0.0184 | 0.04522 | 0.04984 |
| 250 | 0.03385 | 3.142 | +2.142 [+1.213, +3.939] | 535.5 | 0.0092 | 0.03217 | 0.02932 |
| 500 | 0.01997 | 1.419 | +0.419 [+0.411, +1.089] | 209.5 | 0.0046 | 0.01981 | 0.1062 |
| 1000 | 0.02488 | 1.637 | +0.637 [+0.593, +7.321] | 636.8 | 0.0023 | 0.02265 | 0.0206 |
| 2000 | 0.03691 | 3.254 | +2.254 [+2.197, +8.414] | 4507.2 | 0.0012 | 0.03694 | 0.3162 |

fitted alpha of gap vs T: +0.13  predicted 0

## C. Reservoir, delayed recall (n=200, 4 seeds)

| noise | k=1 | k=2 | k=4 | k=8 | k=16 | k=32 | alpha (pred 1) | gap x k (pred 0.5) |
|---|---|---|---|---|---|---|---|---|
| 0.001 | +0.477 | +0.385 | +0.264 | +0.206 | +0.096 | +0.041 | +0.69 | 1.13 |
| 0.01 | +0.294 | +0.206 | +0.092 | +0.097 | +0.033 | +0.022 | +0.76 | 0.51 |
| 0.1 | +0.222 | +0.145 | +0.061 | +0.025 | +0.030 | +0.014 | +0.80 | 0.32 |

Elapsed 58s.

