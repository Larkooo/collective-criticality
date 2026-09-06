# An order-statistic reference for collective search with delayed mixing

Gate 0 draft, revised September 5, 2026. This note defines an exact independent-search reference and a separate, falsifiable model of interacting search. No confirmatory result for the interacting model exists. The rewrite replaces the completed-opportunity-count formula in the earlier draft; the original remains in repository history.

The scientific question is whether communication mainly redistributes existing search progress, or also changes the candidates the population can discover. A distribution of isolated endpoints answers the first protocol below. Predicting interruption and continuation requires information about search paths as well.

## 1. Scope, observables, and calibration

A landscape L assigns fitness f_L(x) in [0,1] to each genotype x in {0,1}^d. Fitness is normalized by the landscape's exhaustive maximum. There are G islands, each containing s agents, so N=Gs. Let m be the per-agent, per-step probability of observing one agent on a different island; T is the interaction horizon. The local algorithm A and its search-trial count are fixed within a condition.

For the initial classical reference, use **zero copy temperature and strict improvement**. In this regime the current population maximum equals the best fitness encountered by the search, including initialization. This follows because each agent retains its previous fitness or replaces it with a higher one. A newly evaluated candidate that exceeds the previous population maximum must be retained by its evaluating agent. Diagnostic neighborhood probes and the exhaustive normalizer are grader operations and are excluded from the agent's discoveries and query budget.

Positive copy temperatures in the existing simulator permit downhill copying. The final population maximum can then be below an earlier discovery. Such conditions require an explicit best-ever archive if they are to be evaluated by best-found quality; they are outside this monotone reference. Historical temperature sweeps retain their original interpretation and scoring.

The two population observables are

\[
B_T=\max\{f_L(x):x\text{ was initialized or queried by the search by }T\},
\qquad Q_T=\frac1N\sum_i f_L(x_i(T)).
\]

They answer different questions: B_T measures discovery; Q_T measures the population's final holdings. Record search queries, initialization queries, communication events, and diagnostic work separately. Equal horizons do not guarantee equal query budgets because copying displaces climbing.

For an isolated island, define X_B as its best member's fitness after a fixed budget B. Write its distribution as F_{L,A,B,s}. This is a **fixed-budget endpoint**, not necessarily the value of a reached local optimum. If a convergence-conditioned quantity is needed, give it a separate distribution and record its stopping time.

Calibration is conditional on landscape, algorithm, budget, and island size. Seeds for calibration and evaluation are disjoint. Landscape-conditioned calibration on each evaluation landscape supports a conditional prediction task; it is not transfer to a landscape on which no calibration is allowed. A stronger cross-landscape claim requires a separate protocol. Average predictions within landscapes before aggregating, and propagate calibration uncertainty.

## 2. Exact independent-search reference

Let X_1,...,X_G be independent draws from a CDF F on [0,1], and M_G=max_i X_i. Since P(M_G<=x)=F(x)^G,

\[
\mathbb E[M_G]=\int_0^1[1-F(x)^G]dx.
\]

For an empirical CDF on n sorted observations x_(1)<=...<=x_(n), the same functional is exactly

\[
\widehat{\mathbb E}[M_G]=\sum_{i=1}^n x_{(i)}\left[(i/n)^G-((i-1)/n)^G\right].
\]

This is exact for the **empirical** distribution. It is an estimator, not an exact value for the unknown population F. Independence without identical distributions gives a product of individual CDFs in place of F^G. Mean and variance alone do not determine any of these maxima.

The classical Hartley–David bound, for mean mu and variance sigma², is

\[
0\leq\mathbb E[M_G]-\mu\leq\sigma\frac{G-1}{\sqrt{2G-1}}.
\]

For G=1 it is immediate. For G>=2 let q be a quantile function. The centered expectation equals

\[
\int_0^1(q(u)-\mu)(Gu^{G-1}-1)du.
\]

Cauchy–Schwarz proves the upper bound: the squared integrals of the two factors are sigma² and (G-1)²/(2G-1). The lower bound follows from M_G>=X_1. Equality in the upper bound requires the centered quantile to be proportional to Gu^(G-1)-1. For example, q(u)=u^(G-1) attains it with its corresponding mean and variance. This is a continuous distribution; at G=2 it is uniform. The earlier description of the equality case as “two-point-like” was incorrect. For a specified mean/variance pair and a [0,1] support restriction, an equality distribution must also meet that support constraint.

This bounds the gain over one isolated draw, not over the interacting algorithm. No normal-tail asymptotic is assumed. Attribution: [Hartley and David, 1954](https://www.jstor.org/stable/2236514).

## 3. Control D: a protocol where the identity predicts the population

Run G islands independently for budget B. Within each island, identify its endpoint X_g and disseminate that endpoint to all its members. Then select the best island endpoint and broadcast it to every agent, with no further search. Internal dissemination and the final broadcast are explicit stages whose costs are recorded separately from the search budget.

For this protocol, B=M_G and Q=M_G. The expectation in Section 2 is therefore the exact population reference under F=F_{L,A,B,s}. Selection may leave one ancestral root without undoing any of the G searches.

For partial final broadcast, let a fixed fraction c of agents be reached by an externally selected set independent of all endpoint values. Every unreached agent retains its already disseminated island endpoint. Then

\[
\mathbb E[Q]=c\mathbb E[M_G]+(1-c)\mu.
\]

Proof: each reached term equals M_G; every unreached term has mean mu; selection of recipients is independent of these values. A random reach fraction independent of endpoint values can be averaged in the same way.

Without internal dissemination, unreached agents need not have mean mu: their mean is the mean of their own holdings, not the mean island maximum. For example, an island containing qualities 0.2 and 0.8 has endpoint 0.8 but mean holdings 0.5. The original draft omitted this condition.

For quality-dependent propagation, expectation cannot generally be factored. Defining C_T as the fraction holding best-found quality, and U_T as the remaining agents' mean quality, gives the pathwise identity

\[
Q_T=C_TB_T+(1-C_T)U_T.
\]

Set U_T=0 when C_T=1. Predict the expectation of the **joint expression**, not a product of independently averaged factors. Candidate identity, quality ties, delivery, and ancestral descent are distinct observables.

Control D checks implementation and calibration for this protocol. It does not validate early mixing.

## 4. Interacting search: state, interruptions, and a closed candidate reference

### 4.1 The actual state is a population, not a completed-search count

An island generally contains several genotypes. An external adoption by one agent does not reset the whole island, and a recipient's local-optimum status is not the completion status of an island. The simulator's full state is the collection of current agent genotypes, relevant policy state, remaining budgets, and the discovery archive when needed. Synchronous contacts and decisions use the pre-update state.

For diagnostics, an **agent search epoch** begins at initialization or at adoption of a different candidate. It records the recipient's full starting state and the sequence of local trials until the next adoption or budget exhaustion. Reaching a strict single-flip local optimum is a tagged event; it does not create an extra independent draw. Epochs opened by both initial and adopted candidates are logged. Internal and external adoptions must be distinguished. Budget-censored epochs are retained, including their discovered candidates.

A completed-epoch count is insufficient. Suppose independent draws are 0.3 or 0.7 with equal probability. Stop after one draw if it is 0.7, otherwise take a second. The expected maximum is 0.6. The count probabilities are P(N=1)=P(N=2)=1/2, but

\[
\tfrac12\mathbb E[M_1]+\tfrac12\mathbb E[M_2]=0.55.
\]

The count depends on observed quality, so conditioning on it changes the distribution of the retained observations. More generally,

\[
\mathbb E[B_T]=\sum_k P(N_c=k)\mathbb E[B_T\mid N_c=k]
\]

is always a law of total expectation, while replacing the conditional term by E[M_k] requires additional conditional-distribution assumptions. Predicting N_c on excluded data does not supply those assumptions. At short horizons N_c may be zero while useful partial candidates already exist. No convention for M_0 can recover their values from that count alone.

### 4.2 An explicit path-copy reference, R_copy

To make a restricted alternative executable, calibrate **whole isolated-island best-fitness paths**, not just endpoint draws. A calibration record contains Z_r(b) for local steps b=0,...,T, including initialization, and the associated query counts. Paths are nondecreasing in the zero-temperature regime. Different initial islands draw independent records conditional on L,A,s. Within a path, temporal dependence is preserved.

R_copy represents each island by a path label r and a cursor b. It is a deliberate coarse model of the agent-level process; treating the island as one representative is an assumption to test. The initial state of island g is (g,0). Fix the following update rule before the pilot:

1. At every global step, each of the s notional members of each island independently attempts an external contact with probability m. A contact selects another island uniformly. All contacts inspect that island's **representative**, rather than a random member. This distinction from the simulator is explicit.
2. Using only pre-step states, an island selects the strictly better visible representative of greatest quality. Ties between better donors use the lowest island index. Equal-quality offers do not trigger copying.
3. If it adopts, it copies the donor's pre-step path label and cursor and makes no local advance that step. Otherwise it advances its current cursor by one and reveals the next value on that fixed path.
4. All updates are simultaneous. Every revealed value enters the discovery archive. An abandoned path's unrevealed future is unavailable until some holder of that path reaches it; previous discoveries remain recorded.

Two recipients sharing a label can have different cursors. They reuse the same future path values rather than generating independent continuations. That coupling, not equality of means or marginal CDFs, is the restricted continuation hypothesis. The program `scripts/formal_checks.py` implements this update with explicit contact schedules. Its included paths are illustrative examples, not a calibrated population experiment.

Let P_path be the calibrated path law and K_m the contact/update rule above. The prospective prediction is the expectation of the archive maximum obtained by integrating the entire simulated history:

\[
\widehat b(m,T)=\mathbb E_{Z_1,...,Z_G\sim\widehat P_{path},\ H\sim K_m}
       [\max\{Z_r(b):(r,b)\text{ was visited by }T\}].
\]

Sampling paths and contacts approximates this expectation. The empirical-path uncertainty and the Monte Carlo error must both be reported. The conditional update uses current quality, so selection and interruption are represented jointly rather than factored into an isolated CDF and a marginal count.

Query accounting follows the calibrated query block for each local advance, charged for each representative that replays it; duplicate work is not free. Adoption steps and communication costs are recorded separately. This is reference-model accounting, not a claim that representative and agent-level workloads match automatically. The initial formal checks do not implement a calibrated cost comparison.

### 4.3 Exact properties of this restricted reference

**No-contact limit.** With m=0, each representative reaches its own Z_g(T). Thus its archive maximum is max_g Z_g(T), and Section 2 applies to the endpoint marginal of P_path.

**Delayed-broadcast limit.** After this independent phase, replace all representatives with the selected terminal path state. The archive stays max_g Z_g(T), even if only one root survives.

**Discovery upper bound at a matched horizon and path library.** Every visited cursor is at most T. Monotonicity therefore gives

\[
B_T^{copy}\leq\max_{r=1,...,G} Z_r(T)
\]

for each fixed library and contact realization. This is a theorem about R_copy. It is not a theorem about the original simulator or arbitrary communicating agents. Communication may raise representative holdings while losing some independently available discoveries.

These are nontrivial implementation constraints, but not novel independent-search theory. Prospective accuracy on an interacting agent population is the empirical question.

### 4.4 Assumptions connecting R_copy to the experiment

| Assumption | Meaning | Check |
|---|---|---|
| A1: path calibration | The isolated joint path law, including budget dependence and timing, is estimated adequately for the target landscape/algorithm/island size. | Excluded path and endpoint prediction checks; propagate calibration uncertainty. |
| A2: representative approximation | Replacing a multi-agent island by its best-path representative does not create a practically important prediction error in the declared regime. | Compare within-island heterogeneity, takeover timing, and the reference with microstate traces. |
| A3: duplicate continuation | After adoption, shared path labels are an adequate coupling of future search quality at the declared resolution. | Randomized Control E and joint continuation diagnostics, against the frozen reference prediction. |
| A4: contact approximation | Representative contacts and copying rules approximate actual random-member contacts and propagation in the declared regime. | Search-disabled propagation experiments and excluded interaction traces. |

All four matter. A full-population prediction failure does not, by itself, identify A3. An isolated-endpoint distribution plus a single average delay cannot establish A1, A2, or A4.

### 4.5 The constructive-continuation rival

Separate two claims previously joined in A3:

- **Duplicate future:** donor and recipient follow the same future path values at matching cursors. This defines R_copy.
- **Equal or dominated marginal endpoints:** a recipient's outcome distribution is equal to, or stochastically below, the donor's. This does not specify their joint distribution and does not define a unique prediction for the population maximum.

Two independent continuations with values 0.3 or 0.7 have expected maximum 0.6. Duplicating one such continuation gives 0.5, despite identical individual marginals. “Same basin” is not enough either: a stochastic local algorithm need not assign each starting genotype a unique final optimum.

A richer rival draws a fresh continuation from a kernel conditional on the full adopted state, island configuration, algorithm, and remaining budget. That kernel can change marginals, dependence, or both. It is calibrated on excluded runs or specified as a synthetic alternative for design-power analysis; it is not estimated from the outcome it predicts.

Control E randomizes a fixed donor offer versus blocked/self information from cloned recipient pre-intervention states with matched remaining budgets. Donor selection is independent of final outcomes. Analyze assignment to the offer, not only recipients who adopted. Isolated and selection-only controls quantify the gain already predicted from importing an existing better candidate. The tested residual is observed minus reference-predicted treatment effect. Attribution specifically to A3 also requires the state, budget, aggregation, and propagation controls to hold. Marginal quality alone cannot test the duplicate-future coupling: include a prespecified joint-outcome statistic or the pair maximum.

## 5. Propagation and mean-agent quality

Begin with search disabled and a fixed candidate set. The microstate contact mechanism is already specified: each agent attempts an external observation with probability m, chooses an external island uniformly and a member uniformly, and applies the strict-better rule using synchronous pre-step states. It is not necessary to fit an arbitrary “effective contact rate” when these events can be counted directly.

As a separate analytic approximation, suppose one uniquely best candidate has already been found, each island adopts it internally instantly, and each agent initiates Poisson contacts at rate m. With j of G islands informed, the next-island arrival rate is

\[
\lambda_j=s m\frac{j(G-j)}{G-1}.
\]

There are s(G-j) uninformed agents; each contacts an informed external island with probability j/(G-1). Summing the mean exponential waiting times gives

\[
\mathbb E[D_{all}]=\sum_{j=1}^{G-1}\frac1{\lambda_j}
   =\frac{2(G-1)H_{G-1}}{N m},\qquad G\geq2,\ m>0.
\]

This is a specified pure-propagation limit, not an exact formula for the synchronous copy-or-climb simulator. At G=1 no external dissemination is needed; at m=0 a unique seed cannot reach the other islands. The Poisson/instant-takeover approximation must be checked against the discrete microstate process before it is used for quantitative predictions.

In live search, candidate discovery times, endpoint values, and susceptibility to replacement are correlated. Calibrate their joint timing where needed, rather than replacing all discovery times with a fitted mean tau. The scaling 1/(T-tau) is a conditional available-time approximation, not a universal window law. Neither landscape invariance nor an interior optimum follows from the order-statistic identity.

**Decision for Study 3:** always report observed B_T and Q_T. Start the predictive test with B_T. Promote a mean-agent prediction to a confirmatory endpoint only if excluded search-disabled propagation tests and the island-to-agent aggregation check validate the joint model. Otherwise keep Q_T descriptive and state that the mean-performance-window mechanism remains untested. The representative mean from R_copy is not silently treated as the mean across actual agents.

If both metrics become confirmatory, evaluate their expectations under one coherent joint process. Do not multiply independently estimated coverage and best-quality means without validating the necessary factorization.

## 6. Answers to the four Gate 0 questions

1. **Split A3.** Duplicate future is a complete coupling specification in R_copy. Equal or dominated marginals need a separate joint continuation kernel and different predictions. Both remain hypotheses about actual agents.
2. **Log every epoch; do not substitute a count into F.** Initial and post-adoption epochs, local-optimum events, interruptions, budget censoring, and partial discoveries all matter. Use the joint path/contact process for prediction. A count mixture is available only under an explicitly verified conditional sampling law, such as a draw count independent of the sampled endpoint sequence.
3. **Specify contacts before fitting propagation.** Use the known discrete contact and strict-better mechanisms first. Validate the pure-propagation approximation separately. Additional parameters should describe measured internal takeover delay or a conditional continuation kernel, with bins/family fixed on excluded development data. A single contact multiplier and tau are not assumed sufficient.
4. **Defer confirmatory mean prediction if necessary.** Retain mean quality as a reported measurement. Make its prediction conditional on independent validation of propagation and aggregation, not on an attractive fit to the Study 3 evaluation curve.

## 7. What can fail and what is ready

| Claim or object | Status and failure interpretation |
|---|---|
| Maximum-CDF identity and Hartley–David bound | Established mathematical implications under stated assumptions. |
| Control D with internal and final dissemination | Exact protocol identity; numerical mismatch may expose implementation or calibration error. Finite-sample disagreement alone does not refute the identity. |
| R_copy update rule and no-contact/delayed-broadcast/upper-bound properties | Fully specified reference with executable checks; not an empirical description yet. |
| R_copy applied to interacting agents | A1–A4 form a testable approximation bundle; residuals outside a predeclared margin reject that bundle in scope. |
| Constructive continuation | Rival requiring a frozen conditional kernel or a declared synthetic design alternative. |
| Mean-agent prediction and window edges | Conditional future tests; no verified scaling or landscape invariance is claimed. |

The code checks are not a design pilot. Before freezing Study 3, add full candidate/contact event logs, isolated path calibration with initialization and query accounting, explicit prediction and baseline losses, and the agreed rival/power analysis. Margins are chosen for scientific usefulness; they are not enlarged to absorb model error. Calibration, simulation, and evaluation seeds have distinct roles and manifests.

The two existing studies retain their recorded status: Study 1 is exploratory with no preregistration freeze, and Study 2's freeze is intact with an inconclusive overall result. There is no completed confirmatory test of R_copy.

## 8. Position in the literature and writing record

The maximum identity and bound are established probability theory. The motivating competition between diffusion and exploration is also established; the simulator is closely related to [Lazer and Friedman, 2007](https://ndg.asc.upenn.edu/wp-content/uploads/2016/04/Lazer-Friedman-2007-ASQ.pdf), and island-model theory already studies diversity preservation through migration, including [Frahnow and Kötzing, 2018](https://arxiv.org/abs/1806.01128). We claim neither a new universal law nor priority for delayed communication. A possible contribution is a prospectively tested, auditable approximation that exposes which parts of candidate quality, continuation dependence, and propagation it can predict. Novelty remains subject to the broader Gate 0 literature review.

Editorial seed **17764446679665605942** ordered six review lenses: measurement versus mechanism; concrete event descriptions; equal summaries with different outcomes; donor/recipient counterfactuals; high-noise boundaries; and empty/zero-budget cases. It also seeds the small reference-property checks. It is not a calibration or confirmatory evaluation seed, and randomness provides no evidence for a mathematical claim.
