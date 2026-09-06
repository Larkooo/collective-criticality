# The task-set gap: a candidate equation for adaptive communication

Status: theory draft for the study `task-set-gap`, 2026-09-06. Sections 2 and 3 are derivations under stated assumptions. Section 5 says what is proved, assumed, and measured. Nothing is a result until the study has a verdict.

## 1. Objective

A system of units propagates activity or information. Let σ be the propagation multiplier: the expected number of units activated per activating unit per generation, or, for smooth dynamics, the largest multiplier of the linearized map. The transition is at σ_c = 1. Let D be the propagation depth that the task fixes: a range L that a message must reach, a delay k that must be remembered, or a horizon T within which a population must be covered. The communication policy π chooses σ (and targeting, which is held fixed here). The objective is

    J(σ) = V(σ; D) − C(σ),

where V is the value of information delivered as the task requires and C is the cost of propagation: bandwidth, instability, or loss of independent search. Wherever V or C is singular or saturating at σ_c, the optimum takes the form

    σ* = σ_c ± A · D^(−α),

with the sign fixed by which side of the transition makes the task feasible and the exponent α fixed by the functional forms of V and C. The claim of the study is not that σ* = σ_c. It is that the gap is positive, that it shrinks with D as a power law, and that α takes the value the forms predict, in three systems measured with the same quantity.

## 2. Subcritical side: delivery to depth L

Assumptions. A Galton–Watson branching process with offspring mean σ < 1 and gap δ = 1 − σ. A message is delivered if the cascade it starts survives to depth L. Cost is a power of the expected cascade size.

Delivery. For a subcritical branching process the survival probability to depth L is asymptotically c₁σ^L, and for small δ, σ^L = exp(L ln(1 − δ)) ≈ e^(−δL). Value V = I₀ e^(−δL).

Cost. Expected total size is Σ_t σ^t = 1/δ (bandwidth, β = 1). Variance of total size for fixed offspring variance v is v/δ³ (instability, β = 3). Write C = c δ^(−β).

Optimum. J(δ) = I₀ e^(−δL) − c δ^(−β). Setting J′ = 0 with x = δL gives x^(β+1) e^(−x) = cβ L^β / I₀. The left side is bounded above by ((β+1)/e)^(β+1). Two regimes follow.

- Cheap communication, cβL^β/I₀ small: x is small and δ* = (cβ/I₀)^(1/(β+1)) · L^(−1/(β+1)). So α = 1/(β+1): one half for bandwidth cost, one quarter for variance cost. At the optimum, delivery probability e^(−x) is near one; the gap is set by cost, not by failure to deliver.
- Expensive communication, cβL^β/I₀ > ((β+1)/e)^(β+1): no interior optimum; the best policy is not to transmit. This is the "should I transmit at all" threshold, and it is a prediction, not a defect.

Also: δ* → 0 only as L → ∞ at fixed cost, or as c → 0. Criticality is the limit, never the optimum, for finite L and positive cost.

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
| δ* = (cβ/I₀)^(1/(β+1)) L^(−1/(β+1)) in the cheap regime; silence regime beyond the bound | derived here under the stated forms of V and C |
| ε* = (ln G + ln(QT/c′))/T for time-limited coverage | derived here under the exponential-saturation form of C(ε, T) |
| α = 0 for component-limited coverage | follows from V having no T dependence; the location 2 to 4 assumes a cost rising in σ |
| That a reservoir with input noise realizes the β = 1 case | assumed; the study tests it |
| That population adoption cascades realize 3a (islands) and 3b (random graph) | assumed; the study tests it |
| Universality across systems | claimed only if each system's measured α matches its predicted α and the gaps are positive throughout |

## 6. Predictions and rivals, for the study file

- P1, critical. In every system and at every D in the grid, the measured gap at the optimum is positive with an interval excluding zero.
- P2, critical. The fitted exponent of gap against D matches the prediction per system: 1/2 and 1/4 for the two branching-process cost models, 1 for the island model in T, 1/2 for the reservoir with input noise, within a tolerance fixed at the design pilot.
- P3, non-critical. Cost direction per side: gap increases with cost on the subcritical side (branching process, reservoir noise); gap decreases with an imposed per-adoption cost on the supercritical side.
- P4, non-critical. The random-graph optimum does not move with T (α within tolerance of 0) while the island optimum does.
- P5, non-critical. The island gap at fixed T increases with ln G.

Rivals. Criticality is optimal (gap = 0 within resolution). Structure only (gap independent of D everywhere). No shared form (gaps positive but exponents unrelated to the predictions). Silence (for the cost weights used, the optimum is not to communicate; a regime, not a refutation, but the study must land in the cheap regime for P1 and P2 to apply).
