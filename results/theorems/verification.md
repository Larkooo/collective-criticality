# Verification of the formal structure

## Theorem 3

x* solving x e^x = 2(e^x - 1): **1.593624**

| L | exact throughput gap x L | x* |
|---|---|---|
| 2 | 0.7982 | 1.5936 |
| 4 | 1.0356 | 1.5936 |
| 8 | 1.2327 | 1.5936 |
| 16 | 1.3748 | 1.5936 |
| 32 | 1.4671 | 1.5936 |
| 64 | 1.5227 | 1.5936 |
| 128 | 1.5546 | 1.5936 |
| 256 | 1.5725 | 1.5936 |
| 512 | 1.5823 | 1.5936 |
| 1024 | 1.5875 | 1.5936 |

The exact gap times depth approaches x* from below; the deficit is the finite-L correction to Lemma 1.

## Theorem 4

| lambda | predicted sqrt(lambda v) (v = sigma ~ 1) | exact gap at L = 2, 4, 8, 16 | predicted L_s = 2/sqrt(lambda v) | exact silence onset (first L with no interior optimum) |
|---|---|---|---|---|
| 0.00025 | 0.0158 | 0.0215, 0.0191, 0.0178, 0.0174 | 126 | 70 |
| 0.001 | 0.0316 | 0.0428, 0.0382, 0.0362, 0.0367 | 63 | 34 |
| 0.004 | 0.0632 | 0.0847, 0.0770, 0.0758, nan | 32 | 16 |
| 0.016 | 0.1265 | 0.1662, 0.1584, nan, nan | 16 | 7 |

Gap ratio for a fourfold cost, predicted 2.0: 2.004, 2.014

## Lemma 1 against the exact recursion

| delta | t | exact u_t | 2 delta / (v (e^(delta t) - 1)) with v = sigma |
|---|---|---|---|
| 0.01 | 50 | 0.02879 | 0.03114 |
| 0.01 | 200 | 0.00302 | 0.00316 |
| 0.01 | 500 | 0.00013 | 0.00014 |
| 0.03 | 16 | 0.08151 | 0.10040 |
| 0.03 | 66 | 0.00873 | 0.00991 |
| 0.03 | 166 | 0.00037 | 0.00043 |
| 0.1 | 5 | 0.19723 | 0.34255 |
| 0.1 | 20 | 0.02367 | 0.03478 |
| 0.1 | 50 | 0.00091 | 0.00151 |

## Theorem 5, leaky integrator by simulation (least-squares readout, 200k steps)

| k | noise | predicted rho*^2 = (k-1)/k | simulated argmax rho^2 | predicted gap 1 - sqrt((k-1)/k) | simulated gap |
|---|---|---|---|---|---|
| 2 | 0.01 | 0.5000 | 0.4970 | 0.2929 | 0.2950 |
| 2 | 0.3 | 0.5000 | 0.4970 | 0.2929 | 0.2950 |
| 2 | 1.0 | 0.5000 | 0.5041 | 0.2929 | 0.2900 |
| 4 | 0.01 | 0.7500 | 0.7482 | 0.1340 | 0.1350 |
| 4 | 0.3 | 0.7500 | 0.7482 | 0.1340 | 0.1350 |
| 4 | 1.0 | 0.7500 | 0.7569 | 0.1340 | 0.1300 |
| 8 | 0.01 | 0.8750 | 0.8742 | 0.0646 | 0.0650 |
| 8 | 0.3 | 0.8750 | 0.8742 | 0.0646 | 0.0650 |
| 8 | 1.0 | 0.8750 | 0.8742 | 0.0646 | 0.0650 |
| 16 | 0.01 | 0.9375 | 0.9409 | 0.0318 | 0.0300 |
| 16 | 0.3 | 0.9375 | 0.9312 | 0.0318 | 0.0350 |
| 16 | 1.0 | 0.9375 | 0.9409 | 0.0318 | 0.0300 |
| 32 | 0.01 | 0.9688 | 0.9702 | 0.0157 | 0.0150 |
| 32 | 0.3 | 0.9688 | 0.9702 | 0.0157 | 0.0150 |
| 32 | 1.0 | 0.9688 | 0.9702 | 0.0157 | 0.0150 |

The simulated optimum tracks (k-1)/k and does not move with noise, as the theorem states.

## Theorem 6, closed form against numerical maximisation

| G | T | Q | c | closed-form eps* T | numerical eps* T |
|---|---|---|---|---|---|
| 10 | 250 | 1 | 0.01 | 12.429 | 12.429 |
| 10 | 2000 | 1 | 0.01 | 14.509 | 14.509 |
| 50 | 1000 | 1 | 0.01 | 15.425 | 15.426 |
| 10 | 1000 | 1 | 0.1 | 11.513 | 11.512 |

