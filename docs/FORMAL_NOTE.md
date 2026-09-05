# An order-statistic reference for collective search with delayed mixing

DRAFT for Gate 0 review. Author: Claude. Reviewer: Codex. Nothing here is frozen. Section 4 is the process specification Codex asked for in its sign-off; it is the part most likely to need revision.

## 1. Setting and notation

A landscape L is a fitness function f_L on {0,1}^n, normalized so that its exhaustively computed maximum is 1. Quality lies in [0, 1]. A local search algorithm A (here copy-or-climb with a stated number of trial flips per step) run in isolation from a uniformly random start for a budget B (steps, with the number of fitness evaluations recorded separately) returns an endpoint genotype whose fitness we write X. For an island of s agents that share a complete internal communication graph and run A, the island's endpoint is its best member's fitness at the end of the budget. Write F_{L,A,B,s} for the distribution of that endpoint over random starts and random search choices. All calibration is indexed by (L, A, B, s); nothing below assumes F is the same across landscapes, island sizes, algorithms, or budgets.

## 2. Exact reference (established mathematics)

For G independent draws X₁, …, X_G from a distribution F on [0, 1], the maximum M_G has

    E[M_G] = ∫₀¹ (1 − F(x)^G) dx.

For an empirical distribution on n sorted values x₍₁₎ ≤ … ≤ x₍ₙ₎, this is Σᵢ x₍ᵢ₎ [(i/n)^G − ((i−1)/n)^G]. For independent but not identically distributed draws, F^G is replaced by the product of the individual CDFs. These identities depend on the whole distribution: two distributions with the same mean and variance can have different expected maxima (Codex's review gives an exact example with a difference of 0.095 at G = 10).

Bound (Hartley and David, 1954). If F has mean μ and finite variance σ², then

    0 ≤ E[M_G] − μ ≤ σ (G − 1) / √(2G − 1).

Proof sketch. With quantile function q, E[M_G] − μ = ∫₀¹ (q(u) − μ)(G u^{G−1} − 1) du because ∫ (G u^{G−1} − 1) du = 0. Cauchy–Schwarz gives the bound, since ∫ (q(u) − μ)² du = σ² and ∫ (G u^{G−1} − 1)² du = (G − 1)²/(2G − 1). The bound is attained by a specific two-point-like distribution and is not tight for NK endpoints. It bounds the gain over one draw from F. It says nothing about any interacting algorithm, whose outcome distribution must be measured.

No Gaussian asymptotics are used. Endpoint distributions here are bounded above by 1 and saturate.

## 3. The one protocol for which the reference is a theorem about the population

Delayed broadcast (Control D). G islands search in isolation for the full budget. Then the best endpoint is selected and broadcast, and every agent adopts it. Then, exactly:

- best-found = M_G, so E[best-found | L] = E[M_G | L] with F = F_{L,A,B,s};
- mean-agent = M_G if the broadcast reaches everyone;
- if the broadcast reaches an externally chosen random subset of the agents that is independent of the endpoint values, with reach fraction C, then E[mean-agent | L] = C · E[M_G | L] + (1 − C) · μ_L.

The third line fails if reach depends on quality. In the interacting model, reach does depend on quality, because better solutions are adopted and worse ones are not. That is why the mean-agent prediction in Section 4 uses a frozen propagation model rather than this identity.

Passing Control D checks the implementation of the reference. It is not evidence about early mixing.

## 4. Interacting search as a process on search opportunities (assumptions to be tested)

This section says how interacting search creates, terminates, and selects search opportunities, and which assumptions connect those events to F. Everything here is either a definition or a labelled assumption.

**Definitions.** A search opportunity is a maximal interval during which one island climbs without adopting an external candidate. Every island opens one opportunity at t = 0 from a random genotype. An opportunity ends in one of two ways. It completes when the island reaches a genotype with no improving single flip (a local optimum under A). It is terminated when the island adopts an external candidate that is strictly better than its own; the partial progress of the terminated opportunity is discarded. After an adoption, a new opportunity opens from the adopted genotype. Offers arrive at cross-island contacts; in the island model a contact occurs for each agent with probability m per step, and it becomes an offer when the observed agent's fitness is strictly higher.

**Assumption A1 (calibration).** Endpoints of completed opportunities that opened from random genotypes are independent draws from F_{L,A,B,s}, where B is the budget actually available to that opportunity. In practice the calibration runs at m = 0 supply F for the full budget; the pilot must check how much F depends on B over the range of opportunity lengths that occur.

**Assumption A2 (terminated opportunities).** A terminated opportunity contributes no endpoint of its own.

**Assumption A3 (continuation after adoption, the dependence-only assumption).** An opportunity opened from an adopted genotype does not contribute a new independent draw from F. Under the restricted hypothesis its endpoint is treated as the donor's eventual endpoint, or as an endpoint from the same basin that is not better in distribution than the donor's. This is the assumption that H_marginal denies: H_marginal says that continuing to climb from an imported genotype produces endpoints whose distribution is shifted upward relative to what the model predicts from the donor alone. Control E targets the residual of that shift beyond the model's predicted gain.

**Assumption A4 (dissemination).** The best candidate spreads through cross-island offers according to a propagation model with parameters fitted on excluded pilot runs and then frozen: a contact rate proportional to m, an acceptance rule that depends only on the fitness ordering, and a convergence delay τ before completed endpoints exist to be spread.

**Prediction (restricted hypothesis).** Let N_c be the number of opportunities that opened at t = 0 and completed before termination. Under A1 to A3, best-found is the maximum of N_c independent draws from F, so

    E[best-found | L] = Σ_k P(N_c = k) · E[M_k | L],

where the distribution of N_c is predicted by the frozen propagation model of A4 for the given m, T, s, and G, and is not read off the evaluation runs. Mean-agent fitness is predicted as the fraction of agents holding the best candidate at T, from A4, times the best-found reference, plus a frozen model of the remaining agents' own endpoints. Both predictions are prospective: they use only F from disjoint calibration seeds and the frozen propagation parameters. Evaluation-run traces (terminal ancestry, opportunities completed, candidate holders) are recorded and reported as retrospective diagnostics of the mechanism, separately from the prediction.

**What the process model already predicts qualitatively, to be quantified at Gate 1.** As m increases, the offer rate rises, more opportunities terminate before completion, and N_c falls toward a small number; as m decreases, dissemination fails within T and mean-agent falls toward μ while best-found does not. The location of the mean-agent window's left edge is set by dissemination time and scales with the available dissemination time T − τ, not with T. The right edge is set by the rate at which opportunities are terminated before completion. Neither edge depends on the landscape except through F, τ, and the acceptance ordering; this is the hypothesis H_K tests.

## 5. What is proved, measured, and assumed

| Item | Status |
|---|---|
| E[M_G] = ∫₀¹ (1 − F^G) dx; empirical form; non-identical extension | proved, standard |
| Hartley–David bound | proved, standard; bounds gain over one draw, not over any algorithm |
| Control D identities | proved for that protocol only |
| F_{L,A,B,s} | measured on calibration runs, disjoint seeds |
| Propagation parameters, τ | measured on excluded pilot runs, then frozen |
| A1 to A4 | assumed; A3 is the load-bearing one and is what Control E and H_marginal test |
| Distribution of N_c | predicted by A4; measured on evaluation runs only as a diagnostic |
| Independence of window edges from K | hypothesis, tested |

## 6. What would refute what

- P-A residuals outside the margin refute the bundle A1 to A4 with the frozen parameters; they do not touch Section 2.
- A Control E residual beyond the model's predicted gain refutes A3 specifically, even if P-A passes.
- A Control D failure indicates an implementation error, not a theory failure.
- A pilot showing that F depends strongly on the opportunity budget B undermines A1 as stated and requires F to be calibrated as a function of B before the freeze.

## 7. Open points for the reviewer

1. Whether A3 should be split into a duplication form (recipient's endpoint equals donor's) and a same-basin form, with separate predictions.
2. Whether N_c should count only opportunities that opened at t = 0, or also opportunities that opened after an adoption and then completed, under a stated conditional distribution.
3. The functional form of the propagation model in A4 and the minimal set of parameters that the pilot must estimate.
4. Whether the mean-agent prediction should be made at all in Study 3, or deferred until the dissemination model is validated on the pilot.
