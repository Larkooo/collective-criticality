# task-set-gap: notebook

## 2026-09-06, design

- Theory in docs/GAP_THEORY.md. The first subcritical derivation assumed drift-dominated survival and
  predicted delta* ~ L^(-1/(beta+1)). Exact evaluation of the branching process before any pilot showed
  a depth-independent gap; the derivation was rewritten: one-shot gives alpha = 0 with gap ~ sqrt(cost)
  and a silence threshold; throughput gives alpha = 1 with gap x L -> 1.59. Both then matched the exact
  process (pilot 1, part A).
- Pilot 1 (seed base 7777): reservoir gap positive and decreasing in k at every noise level, alpha 0.69
  to 0.80 against a first-order 1, constant depends on noise. Islands unusable with an argmax on the
  plateau (the study-2 failure again). Random graph gap of order one, no horizon trend, wide spread.
- Pilot 2 (seed base 7777, window-edge estimator, 6 landscapes): island edge gap 0.052, 0.036, 0.017,
  0.0036 at T = 250 to 2000, alpha 1.27, gap x T inside [2.3, 34.5] at every T. Random-graph edge gap
  not monotone, alpha 0.62, wide leave-one-out spread; the contrast is kept non-critical with a wide
  band. The confirmatory m grid extends down to 1e-4 because the T = 2000 edge sat near the pilot's
  floor; T = 4000 is added.
- Tolerances were set after the pilots, on excluded seeds, and are fixed here before the confirmatory
  run on seed base 4242. The prior credence of 0.5 is a judgement made after the pilots.
- Not frozen. Awaiting Codex's adversarial review and the user's review of criteria and margins.

## 2026-09-07, freeze

Frozen on the user's instruction to proceed with the classical study, without Codex's adversarial
review, which had been requested but not yet returned. The user's review of criteria was the
instruction to proceed. If the review later identifies a flaw in a criterion, it is handled as a
successor version, not as an edit. Confirmatory command unchanged: uv run python scripts/study_gap.py.

## 2026-09-07, after the run

1025 s. P-B1 failed on the monotonicity clause with the exponent on target; P-C1 passed at every
noise level; P-B2 and P-C2 passed; P-B3 and P-B5 inconclusive. Verdict by rules: refuted. The
heuristic forecast score moves the other way (most likelihood ratios favour the theory), which is
exactly why status is decided by rules and the score is labelled a heuristic.
