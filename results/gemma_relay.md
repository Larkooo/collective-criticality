# Relay cascade with a local model: gemma3:4b (exploratory, not preregistered)

Per-hop fidelity p = 1.000 (40/40 single-hop paraphrases kept all 6 facts). Examples:

> Convoy departs dock 47, Thursday at 18:35 with 'saffron heron' as the password. Transport 12 crates to Dr. Okafor’s contact.

> Convoy departs dock 47, Thursday at 18:35 with ‘saffron heron’ as the password. Transport 12 crates to meet Dr. Okafor.

> The convoy departs dock 47 on Thursday at 18:35 with the password ‘saffron heron’. Transport 12 crates and meet Dr. Okafor.


## Cascades, depth D = 5, 20 relays per sigma, forwards to 2 next-hop agents with probability q = sigma / (2p)

| sigma | q | delivered fraction | mean calls | empirical cost per delivery | exact reach (binomial law, measured p) | exact cost per delivery |
|---|---|---|---|---|---|---|
| 0.6 | 0.300 | 0.05 | 1.1 | 22.0 | 0.056 | 24.6 |
| 0.85 | 0.425 | 0.10 | 2.1 | 21.5 | 0.232 | 13.6 |
| 1.1 | 0.550 | 0.55 | 5.3 | 9.7 | 0.521 | 12.9 |

Throughput optimum: empirical over the tested grid at sigma = 1.1; exact prediction over the tested grid at 1.1, over a fine grid at 1.00 (Theorem 3 asymptotic 1 - 1.59/D = 0.68).
One-shot optimum with cost lambda = 0.02 per call: exact sigma* = 1.39, objective +0.540.

Calls: about 212; elapsed 631s.

Caveat: this is a demonstration on one briefing with one model. Per-hop failures may be correlated with message content, which the branching law assumes away.


## Reading (written after the run)

This run does not test the theorems, for two reasons that are recorded here rather than fixed after the fact.

1. **The model made no single-hop errors.** After the checker accepted number words, Gemma kept all six facts in 40 of 40 single-hop paraphrases. Every failure in the cascades therefore came from the synthetic forwarding probability q, not from the model. The cascade is a binomial(2, q) branching process with the model as an expensive identity map. Delivered fractions match the exact binomial computation at two of three rates (0.05 against 0.056; 0.55 against 0.52) and fall short at the middle rate (0.10 against 0.23, two deliveries in twenty), which may be multi-hop drift the checker does not see, or noise.

2. **Depth five is outside the regime of Theorems 3 and 4.** With the cascade capped at depth 5, the cost is bounded by 2^5 calls, so Theorem 1's hypothesis (a cost that diverges at the transition) fails and there is no reason for a positive gap. The exact computation for this offspring law says so: the throughput optimum sits at sigma = 1.00 with a nearly flat curve (cost per delivery 12.5 at 1.0, 12.9 at 1.1, 13.0 at 0.9), and the one-shot optimum with a per-call cost of 0.02 is supercritical at 1.39, because reach dominates when over-propagation is cheap. That is the side rule of the formal structure operating in the direction the bounded cost dictates; it is not the subcritical gap of Theorem 4, whose assumption is not met here.

What a test with a local model would need: a relay task on which the model's own per-hop fidelity is well below one (a longer briefing, a tighter word budget, or a computation at each hop so errors accumulate); cascades that run to extinction rather than to a fixed depth, so that expected calls scale as 1/delta and the cost diverges at the transition; and a delivery depth of at least 16. At two seconds per call that is roughly 800 to 1500 calls, thirty to fifty minutes. Until then this file is a working pipeline and a negative design result, not evidence.
