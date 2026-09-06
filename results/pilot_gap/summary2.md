# Design pilot 2: window-edge estimator for the population systems (6 excluded landscapes x 4 seeds, K=6)

## islands

| T | left edge (mean-agent) | sigma at edge | gap | LOO gap range | gap x T | left edge (best-found) | plateau height | range of perf over grid |
|---|---|---|---|---|---|---|---|---|
| 250 | 0.003009 | 1.052 | +0.0517 | [+0.0152, +0.2084] | 12.9 | 0.0003384 | 0.9482 | 0.8989 to 0.9482 |
| 500 | 0.003214 | 1.036 | +0.0359 | [+0.0066, +0.0352] | 18.0 | 0.000474 | 0.9532 | 0.9020 to 0.9532 |
| 1000 | 0.001863 | 1.017 | +0.0168 | [+0.0083, +0.0211] | 16.8 | 0.001863 | 0.9530 | 0.9217 to 0.9530 |
| 2000 | 0.000401 | 1.004 | +0.0036 | [+0.0032, +0.0267] | 7.1 | 0.000395 | 0.9514 | 0.9214 to 0.9514 |

fitted alpha of edge gap vs T: +1.27  predicted 1; predicted band for gap x T: [2.3, 34.5]

## er

| T | left edge (mean-agent) | sigma at edge | gap | LOO gap range | gap x T | left edge (best-found) | plateau height | range of perf over grid |
|---|---|---|---|---|---|---|---|---|
| 250 | 0.02888 | 2.279 | +1.2786 | [+0.9875, +1.4901] | 319.7 | 0.006776 | 0.9259 | 0.8725 to 0.9259 |
| 500 | 0.05153 | 4.454 | +3.4536 | [+0.6621, +3.6290] | 1726.8 | 0.00631 | 0.9256 | 0.8722 to 0.9256 |
| 1000 | 0.0335 | 2.492 | +1.4924 | [+0.7432, +1.7166] | 1492.4 | 0.00631 | 0.9237 | 0.8741 to 0.9237 |
| 2000 | 0.02037 | 1.405 | +0.4052 | [+0.3443, +0.6748] | 810.4 | 0.00631 | 0.9265 | 0.8721 to 0.9265 |

fitted alpha of edge gap vs T: +0.62  predicted 0

Elapsed 93s.

