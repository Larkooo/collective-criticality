# task-set-gap: results (seed base 4242)

## Derivation checks: exact branching process

| L | one-shot delta* (lambda 1e-3) | one-shot delta* (lambda 4e-3) | throughput delta* x L |
|---|---|---|---|
| 2 | 0.0428 | 0.0847 | 0.798 |
| 4 | 0.0382 | 0.0770 | 1.036 |
| 8 | 0.0362 | 0.0758 | 1.233 |
| 16 | 0.0367 | nan | 1.375 |
| 32 | 0.0429 | nan | 1.467 |
| 64 | nan | nan | 1.523 |
| 128 | nan | nan | 1.555 |

## Islands: left window edge against horizon (G = 10)

| T | edge m | gap | 90% interval | gap x T | band [ln G, 15 ln G] |
|---|---|---|---|---|---|
| 250 | 0.00295 | +0.0250 | [+0.0137, +0.0442] | 6.2 | in |
| 500 | 0.001348 | +0.0148 | [+0.0136, +0.0225] | 7.4 | in |
| 1000 | 0.002195 | +0.0234 | [+0.0279, +0.0696] | 23.4 | in |
| 2000 | 0.0003325 | +0.0026 | [+0.0018, +0.0300] | 5.3 | in |
| 4000 | 0.0001742 | +0.0015 | [+0.0007, +0.0055] | 6.1 | in |

alpha = +1.06, 90% interval [+0.35, +1.41]; monotone decreasing: False; all intervals exclude 0: True

## Random graph: left window edge against horizon

| T | edge p | gap | 90% interval |
|---|---|---|---|
| 250 | 0.02569 | +0.559 | [+0.242, +2.468] |
| 500 | 0.01959 | +0.275 | [+0.225, +0.608] |
| 1000 | 0.03002 | +1.174 | [+0.296, +1.819] |
| 2000 | 0.02276 | +0.403 | [+0.337, +1.453] |
| 4000 | 0.02148 | +0.508 | [+0.315, +0.699] |

alpha = -0.03, 90% interval [-0.39, +0.49]

## Islands: gap against ln G at T = 1000

| G | edge m | gap | 90% interval |
|---|---|---|---|
| 5 | 0.0002288 | +0.0076 | see slope |
| 10 | 0.002195 | +0.0234 | see slope |
| 20 | 0.001287 | +0.0053 | see slope |
| 50 | 0.004257 | +0.0072 | see slope |

slope of gap vs ln G = -0.0026, 90% interval [-0.0363, +0.0020]

## Reservoir: gap at the recall optimum against delay (n = 200)

| noise | feasible k | gaps | 90% intervals exclude 0 | monotone | alpha | 90% interval | gap x k |
|---|---|---|---|---|---|---|---|
| 0.001 | [1, 2, 4, 8, 16] | +0.434, +0.360, +0.289, +0.193, +0.086 | True | True | +0.56 | [+0.46, +0.59] | 1.05 |
| 0.01 | [1, 2, 4, 8, 16] | +0.312, +0.217, +0.127, +0.066, +0.055 | True | True | +0.67 | [+0.52, +0.71] | 0.53 |
| 0.1 | [1, 2, 4, 8] | +0.211, +0.133, +0.084, +0.035 | True | True | +0.84 | [+0.78, +1.01] | 0.27 |

exploratory, n = 400 at noise 0.01: alpha = +0.75

## Outcomes, applied literally

- P-B1: fail
- P-B2: pass
- P-B3: inconclusive
- P-B5: inconclusive
- P-C1: pass
- P-C2: pass

Elapsed 1025s.

