# Exploratory order-statistic check (not preregistered)

Isolated islands (m = 0), G = 10 islands of 10, 4 landscapes x 6 seeds, 500 steps.
Endpoint = each island's best final fitness. E[max of G] is exact from the empirical endpoint CDF per landscape, then averaged over landscapes.

| K | mean endpoint mu_L | endpoint sd sigma_L | sd of population mean at m=0 | E[max of 10] exact | study-2 plateau (max over interior m, biased up) | study-2 perf at m = 0.0316 (fixed grid point) | study-2 perf at m = 1 |
|---|---|---|---|---|---|---|---|
| 2 | 0.9512 | 0.0326 | 0.0127 | 0.9913 | 0.9948 | 0.9924 | 0.9792 |
| 6 | 0.8797 | 0.0475 | 0.0152 | 0.9492 | 0.9536 | 0.9362 | 0.9280 |
| 12 | 0.8436 | 0.0410 | 0.0100 | 0.9083 | 0.9286 | 0.8993 | 0.8735 |

Gaps against the exact reference, in units of the global maximum:
- plateau maximum minus reference: +0.0034, +0.0044, +0.0204 for K = [2, 6, 12] (biased upward by selection over the grid)
- fixed grid point m = 0.0316 minus reference: +0.0011, -0.0130, -0.0090 for K = [2, 6, 12]
Not all gaps lie within 0.010. Whether the discrepancy is selection bias, a real bonus from copying a higher mid-climb point, or the mean-versus-best metric difference is what study 3 must separate, with a best-found metric, ancestry-measured lineage counts, disjoint calibration runs, and an out-of-sample prediction.

