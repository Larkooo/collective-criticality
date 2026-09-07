# task-set-gap-2: notebook

## 2026-09-07, design

Supersedes task-set-gap@1, refuted on the island monotonicity clause with the exponent on target.
Two derivations replaced: Proposition 8 for the population edge (agents, not groups; t0 subtracted)
and the interference conjecture for the reservoir. Design pilot on seed base 5151 sets tolerances.

Self-adversarial review, written before the freeze in place of Codex's review, which was requested
but cannot arrive without the user relaying it:
- Proposition 8 uses t0 and the holders growth from the same trajectory as the measured gap; the
  independence claim rests on C_req coming from fitness, not from holders, and on N and T being
  set. If the geometric-growth assumption fails near saturation, the ratio will be biased below 1
  at short horizons where saturation is a large fraction of the run.
- Changing N at fixed G changes island size, and hence the endpoint distribution and the plateau;
  Proposition 8 absorbs that through C_req and Delta, but a residual dependence would show as a
  ratio trend with N rather than with T.
- The ridge prediction is a conjecture with a heuristic argument, not a theorem; it is non-critical.
- Tolerances were chosen after the pilot on excluded seeds and are fixed before the confirmatory run.
