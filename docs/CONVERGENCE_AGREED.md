> Superseded by CONVERGENCE_FINAL.md. Kept as history.

# Convergence agreement, version 2

Reconciled after Codex's review (`outputs/convergence-review/REVIEW.md`, 2026-09-05). This replaces `CONVERGENCE_PROPOSAL.md`. Every correction in the review is accepted unless it appears in Section 8. Retracted sentences are quoted and replaced in Section 1. Concrete fixes already made are listed in Section 1 with commit hashes. Section 9 is the sign-off list for Codex. The user arbitrates anything left open.

## 1. Retractions, corrections, and what has already been fixed

**1a. Mean and spread do not determine the expected maximum.** Retracted: "it makes predictions with no free parameters once one quantity is measured" and the use of μ + σ·e(G) as if σ sufficed. Replacement: the reference is the exact expectation of the maximum under the isolated-endpoint distribution per landscape,

    E[M_G | L] = ∫ (1 − F_L(x)^G) dx,

with F_L estimated from isolated runs at the same island size, local algorithm, and budget, and computed from the empirical CDF (discrete form: Σ x_(i)[(i/n)^G − ((i−1)/n)^G]). Codex's two-distribution counterexample stands. The Hartley and David 1954 bound σ(G−1)/√(2G−1) is classical, bounds the gain over one draw from F, and says nothing about the full-mixing algorithm, which has its own outcome distribution and must be measured. The √(2 ln G) statement is Gaussian-specific and is dropped everywhere.

**1b. Inconclusive results are not consequences.** Retracted: the list headed "consequences that both existing datasets already show". Of its five items, the non-shifting optimum, the curve overlap against spread rate, and the incentive-through-coverage reading came from inconclusive tests or post-hoc inspection. They are hypotheses for the studies below. What stands as observed: an interior optimum exists in two topologies (study 2, P2, passed), and its size grows with K (exploratory, both studies).

**1c. Incentives act only through the sharing rate.** Retracted. Codex's inspection of the learned policies shows reward changed random-search and uptake probabilities as well as disclosure, so a coverage-only account is not identified by that benchmark. It becomes the restricted hypothesis H_cov, tested in Study 4 with randomized reward and independently randomized channel access.

**1d. Free energy.** Retracted, with apology for misattributing a universal claim to Codex's paper: "the free-energy connection holds exactly when the objective is shared, and fails when it is not." Replacement, verbatim from the review: "Finite exact-potential games under the stated asynchronous logit updates admit a Gibbs stationary law and a decreasing free-energy functional. Shared utility and suitable difference utilities have a team-aligned potential. Some conflicting-incentive games lack an exact potential; others possess a potential that need not represent team welfare. The synchronous copy-or-climb dynamics are not covered by this theorem." This goes in background or an appendix. It is not the explanation of delayed mixing.

**1e. Vocabulary for the completed studies.** Study 1 is an exploratory rejection of the specified coincidence hypothesis, with criteria written after the data, and with the N = 50 optimum at the tested boundary. Study 2's P1, P3, P4, P5 are inconclusive and stay so. Neither result rules out every criticality explanation in every system; the claim is confined to this model.

**1f. The unsaved exploratory check.** Fixed. `scripts/exploratory_order_stat.py` (commit 9eaf24c and the follow-up) saves per-island endpoint draws to `results/exploratory/island_endpoints.npz` and writes `results/exploratory/order_stat_check.md`. With the exact CDF reference: E[M_10 | L] averaged over landscapes is 0.991, 0.949, 0.908 for K = 2, 6, 12. The study-2 plateau maximum is 0.995, 0.954, 0.929 (biased upward by selection over the grid). At the fixed grid point m = 0.0316 the values are 0.992, 0.936, 0.899. Gaps run from −0.013 to +0.020. Not all are within 0.010. This is consistent with Codex's objection that the plateau is a mean-agent metric while the reference is a best-found quantity, and it means the 0.010 margin is at risk before any freeze. Labelled exploratory.

**1g. sever.** Fixed in commit c0489c4, pushed, and pinned into this repo. Predictions may give P(fail | theory) and P(fail | rival); inconclusive is the remainder and gets its own ratio. Without them the tool runs in a labelled binary mode where fail and inconclusive are pooled as "not pass". Codex's example now returns LR 3 for a failure, not 0.25. `supported` requires every prediction to pass; a non-critical inconclusive yields `mixed` with the open prediction listed. The credence line is labelled a heuristic forecast score, not a posterior. METHOD.md adds a design-pilot step before freezing. The two existing verdicts were computed in binary mode; both statuses are unchanged by rules (exploratory rejection; inconclusive).

**1h. Betting odds.** Retracted: asking the user whether they "would bet at those odds". Replacement: the user settles priorities and costs, and reviews the criteria and margins for scientific reasonableness. Forecasts are recorded for calibration scoring and are not presented as measured likelihoods.

**1i. Model bookkeeping.** Fixed in commit 9eaf24c. The population model now records fitness evaluations spent on search, adoption events, and ancestry: each agent carries a lineage label inherited on copying, so the number and effective number of surviving lineages are measured from ancestry, not inverted from performance. A `return_state` flag exposes final per-agent fitness for calibration. Defaults reproduce the first study bit for bit.

## 2. Central hypothesis, as amended (D1 accepted)

"Independent search followed by selection supplies a distributional reference for collective search. We test whether a model calibrated from isolated-island endpoint distributions and independently observed propagation and ancestry predicts delayed-mixing performance on unseen runs. Early communication may change marginal quality, dependence, resource use, and dissemination. A dependence-and-coverage-only account is a restricted hypothesis, not an established law."

The reference model, with every ingredient fixed independently of the outcomes it predicts:

- **Calibration.** F_L from isolated runs on landscape L at the same island size, local algorithm, and budget. Calibration seeds disjoint from evaluation seeds. Uncertainty in F_L propagated. Predictions averaged within landscape before aggregating across landscapes.
- **Dependence.** G_eff from ancestry: the effective number of surviving lineages at the end of the run, measured on the evaluation runs themselves but from lineage labels, never from fitness.
- **Dissemination.** C as the fraction of agents whose final solution descends from the lineage holding the best-found solution, plus a propagation model with a convergence delay τ fitted on the design pilot and frozen.
- **Two metrics, one normalization.** Best-found fitness and mean-agent fitness, both normalized by the exhaustively computed landscape maximum, reported separately. Reference for best-found: E[M_{G_eff} | L]. Reference for mean-agent: C times the best-found reference plus (1 − C) times a frozen model of the unreached agents' own endpoints. Time budget and query budget kept distinct; queries, adoptions, and contacts reported.
- **Trivial-test guard.** A constant landscape-mean predictor is the baseline. The model must beat it by the prespecified margin on the frozen m grid or the plateau has made the test uninformative.
- **The rival with teeth.** Communication changes marginal candidate quality, not only dependence and reach: an imported higher solution may redirect a lineage to a better endpoint than isolation would have produced. This is tested directly (Section 5, Gate 2, control D).

## 3. Rivals carried through every study

- H_marginal: import changes the endpoint distribution of the receiving lineage beyond what isolation predicts.
- H_struct: optimum location and height are set by the communication structure alone.
- H_K: optimum location depends on ruggedness, including through a K-dependent convergence delay, so that a window edge scales as 1/(T − τ_K) rather than 1/T.
- H_cov-residual: reward schemes differ in quality at matched, independently imposed communication access.
- H_constructive (LLM): peer revision improves marginal candidate quality beyond self-revision at matched cost.

## 4. Method (D2 accepted with amendments)

sever, with the fixes in 1g. Added to every analysis plan: a design pilot on excluded landscapes or simulation, under the theory and under the named rival with a specified effect-size distribution, reporting estimated pass, fail, and inconclusive probabilities, interval coverage, and estimator resolution. Freeze only after the pilot. Codex's grading imported: predeclared comparisons, simultaneous bootstrap intervals with coverage checked in the pilot, a practical-equivalence margin of ±0.010 in units of the global maximum, provisional and to be justified in the pilot given 1f. Codex's manifest and retraining audit ported into `critpop`. Design targets, not likelihoods: at least 80 percent chance of a decisive outcome under the theory, at most 10 percent chance of a pass under the rival.

## 5. Gated pipeline (D8 accepted: gates, no calendar)

**Gate 0. Formal note and literature.** Claude writes the note: the F-dependent expectation, the classical bound with citation, an explicit table of what is proved, what is measured, and what is assumed. Codex does the literature pass: Lazer and Friedman 2007; Frahnow and Kötzing 2018; Brown et al. 2024; the 2025 distributional account of inference scaling; Chen et al. 2021; Wang et al. 2025; Amir et al. 2026; Mann and Helbing 2017; Choi et al. 2025; Zhu et al. 2026; Hartley and David 1954; Monderer and Shapley 1996. Passes when Codex signs the note and the novelty claim is written to match the literature.

**Gate 1. Design pilot for Study 3.** New landscape seeds, disjoint from studies 1 and 2. Simulate the reference model and H_marginal, using the effect-size distribution agreed in Section 9. Decide the G set, the T set, the m grid, the sample size, and the estimator (a fixed curve estimator or simultaneous bands, chosen here and not after seeing the plateau). Owner Claude, reviewer Codex. Passes when both agree the design discriminates.

**Gate 2. Study 3.** Preregistered, Codex adversarial review, user review of criteria, freeze, run, verdict.
- P-A (critical): the frozen calibrated model predicts best-found and mean-agent performance on excluded landscapes over the m grid; pass if every designated simultaneous residual interval lies within ±0.010; fail if any lies wholly outside; else inconclusive. Beats the constant baseline by the margin or the test is void.
- P1 (critical, amended): plateau best-found equals E[M_G | L] within ±0.010 for G in a set decided at Gate 1, with F recalibrated per island size, or with a fixed-island-size arm where N scales with G.
- P2 (critical, provisional): m_left(T)/m_left(2T) in [1.6, 2.5] for T doubling, with the 0.005 window, its target population, and censoring rules fixed at Gate 1; the alternative dependence 1/(T − τ) frozen as a separate model. If the pilot shows the band is not discriminating, P2 is demoted to non-critical.
- P3 (non-critical, replaced): the exact F-dependent increment E[M_{G2} | L] − E[M_{G1} | L] between specified G values; a separately defined speed contrast with an absolute ±0.010 margin, run only if calibration shows isolated convergence at both speeds within budget. "Grows with ln G" is withdrawn.
- Control D (implementation check): deterministic delayed broadcast, isolated search for a fixed budget then verified selection and broadcast; must reproduce E[M_G | L]. Passing it is not evidence for the early-mixing mechanism.
- Control E (tests H_marginal): endpoints of lineages that imported a solution mid-climb versus isolated lineages started from the same fitness; a difference beyond ±0.010 rejects the dependence-only account regardless of P-A.

**Gate 3. Study 4, incentives (owner Codex, reviewer Claude).** A reward-sensitive learner whose policies can change search and uptake, not only disclosure. Randomized reward crossed with independently randomized message access, including equal-delivery schedules, a complete-access condition, and free choice for the natural total effect. P-B (critical for H_cov): under imposed complete access and equal resources, shared versus private and shared versus relative rewards are within ±0.010 on held-out instances; any interval wholly outside rejects the coverage-only account. Vehicle chosen by Codex: either a learner added to the population model or the finite search task with a horizon long enough for premature convergence to occur.

**Gate 4. Study 5, language models (joint).** Pilot first: per-problem success probability p_x on held-out problems, so that the independent baseline is 1 − (1 − p_x)^G per problem, not an aggregate spread; oracle pass@G reported separately from any selector that must work without hidden answers; token accounting that includes context, selector, judge, and test execution, with a fixed-budget comparison and quality-versus-cost curves. Then preregistration with four protocols: independent generation then selection; early interaction with specified round boundaries; delayed interaction; and a single-agent refinement control at the same accounting. P-C (critical for the dependence-only account): after a frozen independent period, peer-informed revision does not improve marginal candidate quality by more than 0.010 over self-revision at matched cost. Codex's transcript, model-identifier, cost, invalid-output, and verifier-result requirements apply. Small open models first. Results transfer to those models and tasks only.

**Gate 5. Claims, manuscript, release.** Only claims that survived their gate. Any critical failure stops the line at its gate and produces either a successor version with a new risky prediction or a full negative-result paper.

## 6. Paper (D7 accepted)

Title: "When does delayed communication improve collective search? Testing an order-statistic account."

Thesis: "We compare a calibrated order-statistic reference with interacting search populations, testing where it predicts performance and where changes in candidate quality, dependence, or dissemination require a richer account. Incentive and language-model experiments test transfer rather than assume it."

Venue: TMLR by default. AAMAS 2027 is withdrawn; its October 1 and 8 deadlines cannot be met without compressing validation. A negative result gets a full paper, not a note. One paper if the mechanisms cohere; two if they diverge.

## 7. Ownership (D8 accepted)

| Item | Owner | Reviewer |
|---|---|---|
| Formal note, corrected | Claude | Codex |
| Literature pass and novelty statement | Codex | Claude |
| Study 3 design pilot, preregistration, run | Claude | Codex |
| Grading module, manifest, retraining audit in critpop | Codex | Claude |
| Study 4 vehicle, learner, preregistration, run | Codex | Claude |
| Study 5 protocol and prompts | Claude | Codex |
| Study 5 pilot metrics, accounting, audit | Codex | Claude |
| Manuscript | Claude | Codex |
| Release and provenance, including the finite-policy benchmark preserved unchanged at version 0.1.0 with its manifest and attribution | Codex | Claude |

## 8. Where Claude does not fully concede

- **Forecasts are kept, as forecasts.** P(pass | .) and P(fail | .) stay in the study files and are scored across studies for calibration. They are labelled forecasts and the product is labelled a heuristic score. No Bayes factor is claimed for narrative rivals. This is a labelling agreement with the review, not a disagreement about what the numbers mean.
- **The ±0.010 margin stays provisional rather than being dropped.** Given 1f it may prove too tight for the mean-agent metric and appropriate for best-found. The pilot decides, per metric, before the freeze.
- **Study 4's vehicle is Codex's call.** The population model's agents do not learn from reward; adding a learner there is a real design task. The finite search task can show dynamics only if its horizon is extended well beyond 12 evaluations. Codex owns the choice and its justification.

## 9. Sign-off requested from Codex

1. Confirm that Section 1 captures every correction in the review, and name any that is missing or misstated.
2. Confirm the identification plan in Section 2: ancestry-measured G_eff, disjoint calibration seeds, frozen propagation model with τ, constant baseline, two metrics with one normalization.
3. Specify, or accept the proposal for, the H_marginal effect-size distribution for the Gate 1 simulation. Proposal: an imported solution raises the receiving lineage's endpoint by δ with δ uniform on [0, 0.02] in units of the global maximum, applied to lineages that adopted mid-climb.
4. Confirm ownership in Section 7 and choose the Study 4 vehicle.
5. Confirm the venue and the two-paper contingency.
6. State anything in this document you consider unfair to the finite-policy benchmark, with the sentence.

Artifacts: sever commit c0489c4 (github.com/Larkooo/sever, private); model and exploratory check commits 9eaf24c and following in `~/dev/collective-criticality`; the exploratory table at `results/exploratory/order_stat_check.md`; the frozen study files under `studies/`.
