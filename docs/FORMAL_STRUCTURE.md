# The task-set gap: formal structure

Status: definitions, theorems, and proofs. Each theorem states its assumptions. Section 8 says which statements are rigorous, which rest on a classical asymptotic lemma, and which are hypotheses about particular systems. Section 9 applies the theorems to exact computations and to simulations, and records the evidence that goes against them. Verification script: `scripts/verify_theorems.py`, output in `results/theorems/verification.md`.

## 1. Definitions

**Definition 1 (propagation family).** A propagation family is a one-parameter family of stochastic processes indexed by a multiplier σ > 0, together with a delivery law P_D(σ) ∈ [0, 1] defined for depths D ≥ 1, nonincreasing in D. The family has a transition at σ_c = 1 if, for every D, P_D is continuous in σ, and lim_{D→∞} P_D(σ) = 0 for σ < 1 while lim_{D→∞} P_D(σ) > 0 for σ > 1.

The canonical example is the Galton–Watson process with offspring mean σ, with P_D(σ) the probability that a cascade started by one unit survives to generation D.

**Definition 2 (gap).** For σ < 1 write δ = 1 − σ; for σ > 1 write ε = σ − 1. The gap of a policy is its distance |σ − 1| from the transition.

**Definition 3 (task-set objective).** Given a propagation family, a task depth D, a value function V: [0, 1] → ℝ nondecreasing and bounded, and a cost function C: (0, ∞) → [0, ∞], the objective is

    J(σ; D) = V(P_D(σ)) − C(σ).

A policy is a choice of σ. An optimum is σ*(D) ∈ argmax_σ J(σ; D). The gap function is g(D) = |σ*(D) − 1|.

**Definition 4 (one-shot and rate objectives).** The objective is *one-shot* if it has the form of Definition 3 with C not depending on D. It is a *rate objective* if it is the value delivered per unit cost, J_rate(σ; D) = V(P_D(σ)) / C(σ), or equivalently the cost per delivered unit.

**Definition 5 (scaling form).** An objective has scaling form with exponent ν > 0 on a range of δ if there exist A(D) > 0, B(D) ∈ ℝ, and F: (0, ∞) → ℝ with a unique maximiser x* ∈ (0, ∞), such that J(1 − δ; D) = A(D) · F(δ D^{1/ν}) + B(D) for all δ in that range.

## 2. Positivity of the gap

**Theorem 1 (a divergent cost keeps the optimum away from the transition).** Fix D. Suppose V is bounded and continuous, C is continuous on (0, 1), C(σ) → +∞ as σ → 1⁻, and J(σ₀; D) > −∞ for some σ₀ ∈ (0, 1). Then a maximiser of J(·; D) over (0, 1) exists, and every maximiser satisfies σ* ≤ 1 − η for some η = η(D) > 0.

*Proof.* Since V ≤ V_max and C(σ) → ∞ as σ → 1⁻, there is η > 0 with J(σ; D) < J(σ₀; D) for all σ ∈ (1 − η, 1). The set {σ ∈ (0, 1 − η] : J(σ; D) ≥ J(σ₀; D)} is closed in the compact interval (0 excluded is handled by C ≥ 0 and V bounded: J is bounded above, and if the set accumulated at 0 we replace the lower end by any σ₁ > 0 with J(σ₁) ≥ J(σ₀) and note continuity on [σ₁, 1 − η]). A continuous function on a compact set attains its maximum, and no point of (1 − η, 1) can compete. ∎

**Corollary 1.** Under the hypotheses of Theorem 1, criticality is never optimal: g(D) > 0 for every D.

**Remark (why this is not vacuous).** For the Galton–Watson family the expected cascade size is 1/δ, so any cost proportional to expected size diverges at the transition and Theorem 1 applies. A cost that stays bounded at the transition does not give positivity by this argument; positivity then depends on the derivative of V at the transition, which is the content of Theorems 3 to 5 for specific families.

## 3. Scaling form gives a power-law gap

**Theorem 2 (scaling form ⇒ g(D) = x* D^(−1/ν)).** If an objective has scaling form with exponent ν and scaling function F on a range that contains x* D^(−1/ν), then the gap is exactly g(D) = x* D^(−1/ν).

*Proof.* argmax_δ [A(D) F(δ D^{1/ν}) + B(D)] = argmax_δ F(δ D^{1/ν}) because A(D) > 0 and B(D) does not depend on δ. F has the unique maximiser x*, so δ D^{1/ν} = x*. ∎

The theorem is elementary. Its content is the classification it induces: whether a system's objective has scaling form, with which ν, is what has to be shown case by case, and that is what Sections 4 to 6 do.

## 4. The near-critical branching process

**Lemma 1 (near-critical survival law; classical).** Let Z_t be a Galton–Watson process with offspring mean σ = 1 − δ and offspring variance v, started from one individual, and let u_t = P(Z_t > 0). As δ → 0 and t → ∞ with x = δt fixed,

    u_t ≈ 2δ / (v (e^{δt} − 1)).

*Derivation.* With offspring generating function f, extinction probabilities satisfy q_{t+1} = f(q_t), q_0 = 0, and u_t = 1 − q_t. Expanding f(1 − u) = 1 − f′(1) u + f″(1) u²/2 + O(u³) with f′(1) = σ and f″(1) = v + σ² − σ = v + O(δ) gives u_{t+1} − u_t = −δ u_t − (v/2) u_t² + O(u_t³, δ u_t²). The continuum approximation du/dt = −δu − (v/2)u² is a Bernoulli equation with solution u(t) = 2δ / ((2δ/u₀ + v) e^{δt} − v). With u₀ = 1 and δ → 0 this is the stated law. The rigorous statement, including the critical case u_t ≈ 2/(vt), is the Kolmogorov–Yaglom asymptotic; see Athreya and Ney, *Branching Processes* (1972), Chapter I. ∎

**Theorem 3 (throughput objective has scaling form with ν = 1).** Under Lemma 1, take the cost per attempt to be λ times the expected cascade size, λ/δ, and the rate objective to be delivered value per unit cost, R(δ; L) = I₀ u_L(δ) / (λ/δ). Then R(δ; L) = (2I₀/(λ v L²)) · x²/(e^x − 1) with x = δL. Hence R has scaling form with ν = 1, A(L) = 2I₀/(λvL²), and F(x) = x²/(e^x − 1), whose unique maximiser x* solves

    x e^x = 2 (e^x − 1),   x* = 1.5936…,

and the gap is g(L) = x*/L. The cost weight λ does not enter g.

*Proof.* Substitute Lemma 1 into R: I₀ δ · 2δ/(v(e^{δL} − 1)) / λ = (2I₀/(λv)) δ²/(e^{δL} − 1) = (2I₀/(λvL²)) x²/(e^x − 1). F(x) = x²/(e^x − 1) is positive, tends to 0 at both ends, and F′(x) = [2x(e^x − 1) − x² e^x]/(e^x − 1)², which vanishes where x e^x = 2(e^x − 1); the left side minus the right side, h(x) = x e^x − 2e^x + 2, has h(0) = 0, h′(x) = (x − 1)e^x < 0 on (0, 1) and > 0 beyond, so h has exactly one positive zero, at x* ≈ 1.5936. Theorem 2 gives the gap. ∎

**Theorem 4 (one-shot objective has a depth-independent gap and a silence threshold).** Under Lemma 1, let J(δ; L) = I₀ u_L(δ) − λ(1/δ − 1), where the cost counts activations beyond the source. In the regime δL → 0,

    δ*(L) = √(λ v / I₀) · (1 + O(δ* L)),

independent of L to leading order, and the gap doubles when λ is multiplied by four. Moreover, there is a depth L_s ≈ 2 √(I₀/(λv)) beyond which max_δ J(δ; L) < 0, so that not transmitting (J = 0) is optimal.

*Proof.* For δL → 0, e^{δL} − 1 = δL (1 + δL/2 + O((δL)²)), so u_L = (2/(vL)) (1 − δL/2 + O((δL)²)) and ∂u_L/∂δ = −1/v + O(δL). Stationarity, I₀ ∂u_L/∂δ + λ/δ² = 0, gives λ/δ² = I₀/v (1 + O(δL)), which is the stated δ*. At δ*, the value is I₀ u_L(δ*) ≈ 2I₀/(vL) and the cost is ≈ λ/δ* = √(λ I₀/v); the value falls below the cost when L > 2I₀/(v √(λI₀/v)) = 2√(I₀/(λv)) =: L_s. For L > L_s the optimum over δ has negative objective and silence dominates. ∎

## 5. An exactly solvable recall system

**Theorem 5 (leaky integrator: gap 1/(2k), independent of noise).** Let x_{t+1} = ρ x_t + u_t + η_t with 0 ≤ ρ < 1, inputs u_t i.i.d. with variance s², and noise η_t i.i.d. with variance n², independent of the inputs. Let R²(ρ; k) be the coefficient of determination of the best linear predictor of u_{t−k} from x_t, for k ≥ 1. Then

    R²(ρ; k) = ρ^{2(k−1)} (1 − ρ²) · s²/(s² + n²),

so the optimal radius satisfies ρ*² = (k − 1)/k, the gap is δ*(k) = 1 − √((k−1)/k) = 1/(2k) + O(1/k²), and neither the noise level nor the input variance enters ρ*.

*Proof.* Unrolling, x_t = Σ_{i≥1} ρ^{i−1}(u_{t−i} + η_{t−i}). Then Cov(x_t, u_{t−k}) = ρ^{k−1} s² and Var(x_t) = (s² + n²)/(1 − ρ²). For a linear predictor of a scalar from a scalar, R² = Cov²/(Var(x) Var(u)) = ρ^{2(k−1)} s⁴ (1 − ρ²) / ((s² + n²) s²), which is the stated product. The factor a(ρ) = ρ^{2(k−1)}(1 − ρ²) has derivative ρ^{2k−3}[2(k−1)(1 − ρ²) − 2ρ²], zero at ρ² = (k−1)/k, positive below and negative above, so it is the unique maximiser on (0, 1). The noise enters only through the constant factor s²/(s² + n²). ∎

**Corollary 2.** The leaky integrator's recall objective has scaling form with ν = 1 asymptotically: δ*(k) · k → 1/2.

## 6. Coverage on the supercritical side

**Theorem 6 (time-limited coverage).** Let G groups be covered within horizon T by a process whose coverage fraction is C(ε, T) = 1 − exp(−(εT − ln G)) for εT ≥ ln G and 0 otherwise, let the value be Q · C, and let the cost be cε with c > 0. Then the optimum is

    ε*(T) = (ln G + ln(QT/c)) / T,

so ε* T = ln G + ln(QT/c): the gap scales as 1/T up to a logarithmic correction, increases with ln G, and decreases only logarithmically with the cost weight.

*Proof.* On εT > ln G, J(ε) = Q(1 − exp(−(εT − ln G))) − cε is concave in ε with J′(ε) = QT exp(−(εT − ln G)) − c, which vanishes at exp(−(εT − ln G)) = c/(QT), that is, εT = ln G + ln(QT/c). For this to lie in the region εT ≥ ln G we need QT ≥ c, which holds for any T ≥ c/Q. ∎

**Theorem 7 (component-limited coverage).** If the value is V(σ) = Q · S(σ) with S independent of T and the cost C(σ) is independent of T, then σ* is independent of T: the gap has exponent 0 in T.

*Proof.* J does not depend on T. ∎

**Remark (the side rule).** On the subcritical side the cost term diverges toward the transition while the value saturates (Theorems 3, 4, 5); on the supercritical side the value saturates just beyond the transition while the cost grows away from it (Theorem 6). In both, the optimum sits on the side where the task is feasible, and the two terms balance at a distance that shrinks with the depth demand in the rate cases. This is a description of the four theorems, not a further theorem.

## 7. The structure, in one statement

Let a system be a propagation family with a transition, together with a task depth D and an objective of Definition 3 or 4. Then:

(i) With a divergent cost at the transition, the optimum has positive gap for every D (Theorem 1).
(ii) If the objective has scaling form with exponent ν, the gap is exactly x* D^(−1/ν) (Theorem 2).
(iii) Rate objectives on the near-critical branching process (Theorem 3), recall in the leaky integrator (Theorem 5), and time-limited coverage (Theorem 6) have ν = 1, with constants 1.5936, 1/2, and ln G + ln(QT/c) respectively.
(iv) One-shot objectives on the branching process (Theorem 4) and component-limited coverage (Theorem 7) have a depth-independent gap, with a silence threshold in the first case.

Criticality, g = 0, is the limit D → ∞ in (iii) and is never attained at finite D under (i).

## 8. Rigor

| Statement | Status |
|---|---|
| Theorem 1, Corollary 1 | rigorous, elementary |
| Theorem 2 | rigorous, elementary |
| Lemma 1 | classical asymptotic; derivation given, rigorous form cited |
| Theorems 3, 4 | rigorous given Lemma 1; finite-L corrections are visible in exact computation (Section 9) |
| Theorem 5, Corollary 2 | rigorous, exact |
| Theorems 6, 7 | rigorous given the assumed coverage and value forms; whether real populations realise those forms is a hypothesis |
| Section 7 (iii) as a statement about tanh reservoirs or island populations | hypothesis, under test in study task-set-gap |

## 9. Application and opposing evidence

**Exact branching process (application of Theorems 3 and 4).** With the exact generating-function recursion, no approximation: the throughput gap times depth rises through 0.80, 1.04, 1.23, 1.38, 1.47, 1.52 at L = 2, 4, 8, 16, 32, 64 and approaches 1.5936 from below; the one-shot gap at λ = 10⁻³ is 0.043, 0.038, 0.036, 0.037, 0.043 at L = 2 to 32 (exponent 0.01), the ratio of gaps for a fourfold cost is 2.01, and silence sets in between L = 32 and L = 64 against the predicted L_s = 2/√(λ v) ≈ 63. The theorems hold for the exact process up to finite-L corrections that Lemma 1 does not capture.

**Leaky integrator (application of Theorem 5).** Simulated with least-squares readout: ρ*² tracks (k − 1)/k at every noise level tested; see the verification output.

**Opposing evidence, stated plainly.**
1. The tanh echo-state reservoir with n = 200 units is not the leaky integrator. In the design pilot its gap fell with delay with exponent 0.69 to 0.80, not 1, and its constant gap × k was 1.13, 0.51, 0.32 at noise 0.001, 0.01, 0.1. Theorem 5 predicts noise-independence. So Theorem 5 does not describe the n-dimensional nonlinear reservoir's constant, and may not describe its exponent. This is registered as prediction P-C2 in the study file so that the model is tested, not patched. If P-C2 passes, Section 7 (iii) is wrong for that system as stated and needs an interference term that Theorem 5 lacks.
2. The random-graph population's edge gap was not monotone in horizon in the pilot (1.28, 3.45, 1.49, 0.41) with exponent 0.62 against Theorem 7's 0. Wide spread, but not the predicted flatness. If the confirmatory run shows a clear horizon dependence, Theorem 7's assumption that coverage is component-limited fails for that system.
3. The throughput exponent fitted over L = 2 to 64 is 0.82, not 1, because of finite-L corrections. Theorem 3 is an asymptotic statement; at small depth the exact gap is smaller than x*/L. Any test of ν = 1 must be made at L ≥ 16 or with the finite-L form.

None of these three is fatal to the structure of Section 7, but each one limits a specific claim, and the second and third are precisely where a confirmatory run could kill Section 7 (iii) or (iv) for the population system. If that happens, it will be recorded as such.
