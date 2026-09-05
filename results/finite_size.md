# Finite-size check

Does the performance optimum approach the diversity transition as the population grows? Run with `uv run python scripts/finite_size.py`.

960 runs in 23s; K=6, 4 landscapes x 4 seeds, 300 steps

| N agents | degree* of mean fitness | degree at diversity half-drop | ratio | gain of peak over degree 30 |
|---|---|---|---|---|
| 50 | 30.00 | 1.80 | 16.69 | +0.000 |
| 100 | 3.63 | 1.77 | 2.05 | +0.031 |
| 200 | 4.45 | 1.77 | 2.52 | +0.020 |
| 400 | 3.13 | 1.73 | 1.81 | +0.034 |
