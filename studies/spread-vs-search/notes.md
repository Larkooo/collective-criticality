# spread-vs-search: notebook

## 2026-09-05

Successor to optimum-at-transition@1. Written after seeing the first sweep, so P2 and P3 are
partly expected from that data (they replicate in a new topology). P1, P4 and P5 are the
predictions the first sweep does not contain. Frozen before any island-model code is run.

## 2026-09-05, after the run

3672 runs, 137 s. P2 passed with room to spare. P1, P3, P4, P5 all inconclusive, each for a
design reason: argmax on a flat plateau (P1, P3), a spread-rate measure dominated by transients
with non-overlapping ranges (P4, P5). Verdict: inconclusive. The theory is untested on its
central claim. Next version is a design fix (resolution, window edges, a pre-convergence spread
rate), not a theory change, plus one exploratory hypothesis that goes against the formal model:
collapse against r alone.
