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

## 2026-09-07, second design pilot (seed base 5151)

The exponential-saturation island constant ln(C_req G) = 2.2 was off by 2 to 4 times in all 16 cells;
the measured island gap x (T - t0) sat at a median near 5.4. Spread among a finite set of islands is
logistic, and the logistic time from one island to 93 percent coverage is ln((G-1) x 0.93/0.07) = 4.8.
Replaced. This is the third form of the island constant at the design stage (ln G in version one,
ln(C_req G), now logistic); the confirmatory run is on fresh seeds and this history is the reason the
prior stays at 0.5. The ln G slope test was replaced by a timing test because the geometric fit is
unreliable for G = 5 (only a few islands to fit). Noise-dominated reservoir cell at 0.15: exponent 0.98.
Size effect 0.03, unresolvable, removed as a prediction. No further pilots; freeze next.
