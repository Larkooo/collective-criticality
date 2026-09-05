# Sweep summary

config: `{"n_bits": 16, "n_agents": 100, "steps": 150, "ks": [2, 6], "p_links": [0.0, 0.01, 0.03, 0.1, 0.3, 1.0], "temps": [0.0, 0.01, 0.1, 1.0], "n_landscapes": 2, "n_seeds": 2}`

runs: 80, horizons: ['t=25', 't=50', 't=100', 't=149']

## Peak coincidence (horizon t=149, connectivity as p_link)

| K | p* of mean fitness | p* of chi(fitness) | p* of chi(diversity) | p at diversity half-drop | ratio p*perf / p*chi |
|---|---|---|---|---|---|
| 2 | 0.0425 | 0.1281 | 0.0100 | 0.0157 | 0.33 |
| 6 | 0.0269 | 0.3539 | 0.0100 | 0.0172 | 0.08 |

## Data collapse (spread across K after rescaling x; lower is tighter)

| curve | no rescale | x = p / p*_chi | x = p / p_half-drop |
|---|---|---|---|
| diversity | 0.0095 | 0.0263 | 0.0061 |
| mean fitness / its max | 0.0087 | 0.0108 | 0.0086 |

## Connectivity vs temperature (final horizon)

Mean distance from each temperature-sweep point to the nearest connectivity-sweep point in the (diversity, mean fitness) plane, per K. Small = the two dials trace the same curve.

| K | mean nearest distance | perf range (p sweep) | perf range (T sweep) |
|---|---|---|---|
| 2 | 0.0065 | 0.949 to 0.987 | 0.946 to 0.964 |
| 6 | 0.0183 | 0.867 to 0.923 | 0.877 to 0.953 |

## Non-predictive information (Still et al. 2012 proxy)

| K | p* of I_np | Spearman(I_np, final mean fitness) over p | Spearman(I_np, chi) |
|---|---|---|---|
| 2 | 0.0487 | 0.77 | 0.54 |
| 6 | 0.0361 | 0.43 | 0.60 |

## Convergence to a single solution (final horizon)

| K | p=0 | p=0.01 | p=0.03 | p=0.1 | p=0.3 | p=1 |
|---|---|---|---|---|---|---|
| 2 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 |
| 6 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 |

Entries are the fraction of runs that collapsed to one distinct solution before the end of the run.
