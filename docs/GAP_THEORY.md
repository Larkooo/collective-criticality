# The task-set gap: a candidate equation for adaptive communication

Status: theory draft for the study `task-set-gap`, 2026-09-06. Sections 2 and 3 are derivations under stated assumptions. Section 5 says what is proved, assumed, and measured. Nothing is a result until the study has a verdict.

## 1. Objective

A system of units propagates activity or information. Let σ be the propagation multiplier: the expected number of units activated per activating unit per generation, or, for smooth dynamics, the largest multiplier of the linearized map. The transition is at σ_c = 1. Let D be the propagation depth that the task fixes: a range L that a message must reach, a delay k that must be remembered, or a horizon T within which a population must be covered. The communication policy π chooses σ (and targeting, which is held fixed here). The objective is

    J(σ) = V(σ; D) − C(σ),

where V is the value of information delivered as the task requires and C is the cost of propagation: bandwidth, instability, or loss of independent search. Wherever V or C is singular or saturating at σ_c, the optimum takes the form

    σ* = σ_c ± A · D^(−α),

with the sign fixed by which side of the transition makes the task feasible and the exponent α fixed by the functional forms of V and C. The claim of the study is not that σ* = σ_c. It is that the gap is positive, that it shrinks with D as a power law, and that α takes the value the forms predict, in three systems measured with the same quantity.

## 2. Subcritical side: delivery to depth L

**Record of a correction.** The first draft of this section assumed drift-dominated survival, P(reach L) ≈ e^(−δL), and derived δ* ∝ L^(−1/(β+1)). An exact evaluation of the branching process before any pilot run showed the optimum barely moves with L (0.038 at L = 4, 0.037 at L = 16 for a bandwidth cost of 0.001, then silence at L = 64). The reason: at the optimum, δL is small and survival is fluctuation-dominated, not drift-dominated. The derivation below replaces the old one. The correction happened at the design stage and before any preregistration, which is what the design stage is for.

Assumptions. A Galton–Watson branching process with offspring mean σ = 1 − δ < 1 and offspring variance v. Near the transition the survival probability to depth L is

    P_L(δ) ≈ 2δ / (v (e^(δL) − 1)),

which is 2/(vL) as δ → 0 (the critical law) and (2δ/v) e^(−δL) for δL ≫ 1 (the drift law). Expected cascade size is 1/δ; size variance is v/δ³.

**2a. One-shot delivery with a cost per attempt.** J(δ) = I₀ P_L(δ) − λ/δ. For δL ≪ 1, P_L ≈ (2/(vL))(1 − δL/2), so dV/dδ ≈ −I₀/v, a constant independent of L. Balancing against the cost slope λ/δ² gives

    δ* = √(λ v / I₀),   independent of L.

Approaching the transition does not help a single cascade reach far, because near criticality survival is limited by early extinction, not by drift. The deliverable value 2I₀/(vL) falls with L until it no longer covers the cost λ/δ*, beyond L_silence ≈ 2/(v δ*): the optimal policy is not to transmit. So α = 0, the gap scales as the square root of the cost, and there is a range threshold for silence. All three appear in the exact evaluation.

**2b. Throughput: cost per delivered message.** If attempts repeat until delivery, or many sources send, the relevant objective is the expected cost per delivered message, E[size]/P_L = v (e^(δL) − 1)/(2δ²) in the near-critical approximation. Minimizing over δ gives x e^x = 2(e^x − 1) with x = δL, so

    δ* = x*/L,   x* ≈ 1.59,   α = 1,

independent of the cost weight, which only scales the objective. Here the gap does shrink with range, as 1/L, with a dimensionless constant fixed by the objective's shape.

**2c. Reservoir with input noise (delayed recall at depth k).** The component of the state carrying the input from k steps ago decays as ρ^k = e^(−δk) with δ = 1 − ρ, while accumulated noise power scales as Σ ρ^(2t) = 1/(1 − ρ²) ≈ 1/(2δ). Recall quality is monotone in the signal-to-noise ratio ∝ δ e^(−2δk), maximized at

    δ* = 1/(2k),   α = 1,

independent of the noise level to first order; noise sets the achieved quality, not the location of the optimum. Nonlinearity and interference from other delays can shift this, which is what the pilot measures.

**The general form.** When the objective is a rate, value per unit time or per unit cost, and depth enters through an exponential decay e^(−δD), the optimum satisfies gap × depth = a constant of order one set by the objective's shape (1.59 for branching throughput, 1/2 for reservoir recall, ln G plus logarithmic terms for time-limited coverage in Section 3a). When the objective is a one-shot probability with a cost per attempt, the gap is set by cost alone and does not depend on depth. Both give a positive gap, and δ* → 0 only as D → ∞ in the rate case.

## 3. Supercritical side: coverage of a population

Two sub-cases, distinguished by what limits coverage.

**3a. Time-limited coverage (island model).** G groups; a solution that has reached a group spreads to others at a per-generation growth factor 1 + ε with ε = σ − 1 > 0 small. Coverage of G groups within T generations requires (1 + ε)^T ≳ G, so ε ≳ ln G / T. Model the coverage fraction as C(ε, T) = 1 − exp(−(εT − ln G)) for εT > ln G, saturating exponentially beyond the minimum. The cost of over-propagation, the loss of independent searches, rises with ε: C_cost = c ε^γ. With value Q for a fully covered population, J′ = 0 gives exp(−(εT − ln G)) = cγ ε^(γ−1)/(QT). Writing ε = (ln G + y)/T, y = ln(QT / (cγ ε^(γ−1))), which grows only logarithmically. So

    ε* = (ln G + ln(QT/c′)) / T,

α = 1 in T up to logarithmic corrections; the gap increases with ln G; the gap decreases with cost, but only logarithmically. Cost pulls toward the transition on this side; demand pushes away. Both roles are reversed relative to Section 2, which is why the unified statement is about the balance and not about either term alone.

**3b. Component-limited coverage (random graph).** If the graph is static and copying is deterministic along edges, coverage is limited not by time but by the size of the giant component, S(σ), with S = 1 − e^(−σS) for an Erdős–Rényi graph. V = Q · S(σ) has no D dependence: α = 0 in T. σ* solves Q S′(σ) = C′(σ). S′ is large just above σ = 1 and small beyond σ ≈ 3, so with a cost rising in σ the optimum sits in the range 2 to 4. Study 1 measured 2.6 to 4.3 with no dependence on horizon from t = 25 to t = 499. That is exploratory and consistent; it is not a test of this section until preregistered.

The contrast between 3a and 3b is the sharpest cheap test in the program: the same agents and landscapes, and the theory predicts α = 1 for one topology and α = 0 for the other.

## 4. Measured quantity

σ is measured, not read off a parameter, in every system:

- Branching process: exact, via the generating-function recursion, with Monte Carlo as a check.
- Population model: the per-step growth factor of the number of agents holding the genotype that ends as best-found, fitted by least squares on log counts over the window from first appearance to half coverage.
- Reservoir: exp of the largest Lyapunov exponent, from the growth of a renormalized perturbation along the driven trajectory; the nominal spectral radius is reported alongside.

## 5. Proved, assumed, measured

| Item | Status |
|---|---|
| Survival asymptotics, expected size 1/δ, variance v/δ³ for subcritical Galton–Watson | standard, cited |
| One-shot: δ* = √(λv/I₀), independent of L, with silence beyond L ≈ 2/(vδ*) | derived here from the near-critical survival law; checked against the exact generating function |
| Throughput: δ* = x*/L with x* ≈ 1.59 | derived here from the near-critical survival law; checked against the exact generating function |
| Reservoir: δ* = 1/(2k), noise-independent to first order | derived here from a linear signal-to-noise argument; the pilot tests it under tanh nonlinearity |
| ε* = (ln G + ln(QT/c′))/T for time-limited coverage | derived here under the exponential-saturation form of C(ε, T) |
| α = 0 for component-limited coverage | follows from V having no T dependence; the location 2 to 4 assumes a cost rising in σ |
| That a reservoir with input noise realizes the β = 1 case | assumed; the study tests it |
| That population adoption cascades realize 3a (islands) and 3b (random graph) | assumed; the study tests it |
| Universality across systems | claimed only if each system's measured α matches its predicted α and the gaps are positive throughout |

## 6. Predictions and rivals, for the study file

- P1, critical. In every system and at every D in the grid, the measured gap at the optimum is positive with an interval excluding zero.
- P2, critical. The exponent of gap against depth is α = 1 for rate objectives (branching throughput in L, reservoir recall in k, island coverage in T) and α = 0 for one-shot objectives (branching one-shot in L, component-limited random-graph coverage in T), within a tolerance fixed at the design pilot. The rivals do not predict this dichotomy.
- P3, non-critical. The gap-times-depth constants match the derived values within a stated tolerance: 1.59 (branching throughput), 1/2 (reservoir), and ln G plus a logarithmic term (islands).
- P4, non-critical. Cost dependence per case: one-shot branching gap ∝ √λ; throughput branching gap independent of the cost weight; reservoir gap independent of noise level to first order; island gap decreasing logarithmically with an imposed per-adoption cost.
- P5, non-critical. The island gap at fixed T increases with ln G.

Rivals. Criticality is optimal (gap = 0 within resolution). Structure only (gap independent of D everywhere, including the rate cases). No shared form (gaps positive but exponents and constants unrelated to the derivations). Silence (for the cost weights used, the optimum is not to communicate; a regime the design must avoid for P1 and P2 to apply, and a prediction in its own right).
