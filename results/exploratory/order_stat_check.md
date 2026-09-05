# Exploratory order-statistic check (not preregistered)

Isolated islands (m = 0), G = 10 islands of 10, 4 landscapes x 6 seeds, 500 steps.
Endpoint = each island's best final fitness. E[max of G] is exact from the empirical endpoint CDF per landscape, then averaged over landscapes.

| K | mean endpoint mu_L | endpoint sd sigma_L | sd of population mean at m=0 | E[max of 10] exact | study-2 plateau (max over interior m, biased up) | study-2 perf at m = 0.0316 (fixed grid point) | study-2 perf at m = 1 |
|---|---|---|---|---|---|---|---|
| 2 | 0.9512 | 0.0326 | 0.0127 | 0.9913 | 0.9948 | 0.9924 | 0.9792 |
| 6 | 0.8797 | 0.0475 | 0.0152 | 0.9492 | 0.9536 | 0.9362 | 0.9280 |
| 12 | 0.8436 | 0.0410 | 0.0100 | 0.9083 | 0.9286 | 0.8993 | 0.8735 |

Reading: the exact expected best-of-10 of isolated endpoints is within about 0.003 to 0.016 of the mean-fitness plateau, and the gap is largest at K = 12. Whether that gap is selection bias on the plateau, a real bonus from copying a higher mid-climb point, or the mean-versus-best metric difference is exactly what study 3 must separate with a best-found metric, ancestry-measured lineage counts, and an out-of-sample prediction.

