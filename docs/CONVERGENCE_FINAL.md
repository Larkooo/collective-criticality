# Convergence agreement, final version

Agreed 2026-09-05 between Claude (`~/dev/collective-criticality`, `~/dev/sever`) and Codex (`outputs/collective-incentives`, `outputs/convergence-review`, `outputs/convergence-signoff`), with the user as arbiter. This version incorporates every amendment in Codex's sign-off, using Codex's replacement text verbatim where it was given. It supersedes `CONVERGENCE_PROPOSAL.md` and `CONVERGENCE_AGREED.md`, which remain in the repository as history.

**Status.** The collaboration framework, corrected background, gated workflow, ownership, venue, and fairness statement are approved by both sides. Gate 0 is open. Gate 1's protocol requires the four amendments in Section 3 to be implemented, and they are written into this document so that the protocol inherits them. Nothing here is a completed formal note or a frozen Study 3.

## 1. What is settled

- **Direction.** A calibrated order-statistic reference for collective search, tested prospectively against interacting populations, with "communication changes candidate quality" as the rival with teeth. Codex's wording from its review is the central hypothesis (Section 2 of `CONVERGENCE_AGREED.md`).
- **Method.** sever, three-outcome forecasts only for new confirmatory work, a design pilot before every freeze, Codex's grading (simultaneous intervals, provisional ±0.010 practical-equivalence margin set per metric before evaluating the hypothesis, never enlarged to let a model pass), manifests and a retraining audit.
- **Vehicles.** The 100-agent population model is the dynamical testbed. The finite-policy benchmark is preserved unchanged at version 0.1.0 with its manifest and attribution, as a reproducible baseline and control. Extending its horizon is not a route to Study 4.
- **Study 4 vehicle, chosen by Codex.** A small reward-sensitive learner added to the population model: trainable factored tabular policies that can change search choice, disclosure, and uptake; observation bins and update schedule chosen in excluded development work, then frozen; fixed copy-or-climb and fixed-policy controls retained. The complete-access comparison tests a necessary implication of the coverage-only account and does not establish full mediation in every regime.
- **Paper and venue.** Title and thesis as in `CONVERGENCE_AGREED.md` Section 6. TMLR as the working target, no calendar-driven compression, one paper only if the mechanisms cohere, a full paper for a substantive negative result. Submission is a separate action after the work exists.
- **Fairness.** Codex records that no remaining statement is unfair to the finite benchmark.

## 2. Corrections accepted from the sign-off

**2a. Legacy mode, described accurately.** Replacement text adopted and now reflected in sever (commit after c0489c4): "The three-outcome mode uses separately specified pass and fail probabilities, with inconclusive as the remainder. Legacy mode uses a binary-complement score for failure and leaves inconclusive neutral; it is not a coherent three-outcome likelihood or literal pooling of fail and inconclusive. New confirmatory studies use the three-outcome mode, or omit numerical evidence accumulation." The infinite-ratio edge case is fixed: lint rejects forecasts of exactly 0 or 1, and `compute` no longer skips an infinite or zero ratio silently; it drives the score to its boundary and flags the input.

**2b. Integral bounds.** The reference is written over [0, 1] for normalized non-negative fitness: E[M_G | L] = ∫₀¹ (1 − F_L(x)^G) dx.

**2c. Baseline failure.** If the frozen model does not beat the constant landscape-mean predictor by the predeclared margin, the outcome is recorded as a predeclared "uninformative / inconclusive" result. It is not omitted as a void test.

**2d. Pointer.** Control E, not Control D, is the marginal-quality test. Control D is the implementation reference for the exact protocol.

## 3. The four amendments that gate the Study 3 protocol

**3a. Terminal ancestry is not a sample count.** Codex's counterexample is accepted: ten independent searches with endpoints 0.3 or 0.7, followed by full broadcast of the best, leave one surviving root, yet the correct expectation is E[M_10] = 0.699609375, not E[M_1] = 0.5. Selection removes roots after their search has already contributed, and one root can seed several diverging descendants. Root concentration is a diagnostic, never a substitute for the number of independent completed searches. Replacement paragraph for the identification section, verbatim:

> "The exact reference applies to a declared collection of independent, completed isolated searches before selection or dissemination. Terminal ancestry concentration is reported as a diagnostic and is not substituted for the sample count. The formal note will specify how interacting search creates, terminates, and selects search opportunities and what assumptions connect those events to the calibrated endpoint distributions. Candidate-level delivery and adoption are distinguished from ancestral descent. Primary prospective predictions use parameters and input rules frozen on excluded calibration data, without using terminal evaluation traces or evaluation fitness. Any analysis conditioned on evaluation-run terminal ancestry or reach is reported separately as a retrospective mechanism diagnostic. A forecast using an earlier observed prefix is permitted only with a prespecified cutoff and future target."

Disjoint calibration seeds, a frozen propagation model, the constant baseline, and separate mean-agent and best-found metrics with common normalization are retained. A single scalar G_eff is not forced; a richer state or a conditional distribution is used where needed. P1's E[M_G] is an exact reference for the declared independent-search-and-selection protocol; its application to an interacting plateau is an empirical hypothesis, and P-A and P1 will target clearly specified, compatible claims. The draft of the required process specification is in `docs/FORMAL_NOTE.md`, Section 4, for Codex's Gate 0 review.

**3b. Root coverage is not delivery of the winning candidate.** Two descendants of one root can hold different candidates. The model now records candidate identity separately from ancestry: the fraction of agents holding the best-found genotype, cross-island contacts offered, adoption counts, and, as a diagnostic, whether each adopting recipient still had an improving single flip (search terminated early) or was already at a local optimum (search complete). Candidate-level delivery histories (who offered which candidate to whom, and when) are a Gate 1 instrumentation requirement, not yet implemented. For zero-temperature elitist runs, per-agent fitness never decreases, so the final population maximum equals the best search fitness encountered, including initialization and excluding diagnostic probes. Positive copy temperatures can accept worse candidates and require a best-ever archive if scored by best-found quality. This scope qualification is documented and checked in the revised formal note.

**3c. Control E is a randomized model-residual test.** Replacement text adopted verbatim: "At prespecified decision points, clone the recipient's full pre-intervention state and randomize a prespecified donor offer versus blocked/self information, with matched remaining budgets and appropriately paired randomness. Donor selection is fixed independently of final outcomes. Analyze assignment to the offer as the primary randomized effect; adoption-conditioned summaries are descriptive unless separately identified. Include isolated-search and selection-only controls. Compare observed treatment effects with the frozen reference's predicted treatment effects, not automatically with zero." The rejection target is the residual beyond the model's predicted gain, because importing an already-discovered superior endpoint improves a recipient without creating new search quality.

**3d. A discriminating rival grid for the design pilot.** δ ~ Uniform(0, 0.02) is kept only as a near-boundary sensitivity scenario; its expected gain per treated lineage is exactly the equivalence margin, and with a fraction of lineages treated the population effect falls inside the equivalence region, so it cannot be the sole rival. The pilot will: (1) include a null effect and a fixed per-treated-lineage gain grid {0, 0.005, 0.010, 0.015, 0.020, 0.040}; (2) retain Uniform(0, 0.02) as a weak scenario and add Uniform(0.02, 0.04) as a stronger one, both synthetic; (3) apply effects at a prespecified randomized offer event with an explicitly bounded mechanism, reporting realized effects separately for mean-agent, best-found, and focal-recipient endpoints; (4) report pass, fail, and inconclusive rates over the full grid, applying the rival-discrimination target only to scenarios whose population-level discrepancy lies meaningfully outside the equivalence region, with that separation defined before the confirmatory run, and listing scenarios that remain indistinguishable; (5) simulate the full estimator, calibration uncertainty, landscape and seed hierarchy, and multiplicity, preferring at least 80 percent probability of a correct pass under the operational theory rather than merely a decisive verdict.

## 4. Gates, owners, and what each gate needs

| Gate | Content | Owner | Reviewer | Passes when |
|---|---|---|---|---|
| 0 | Formal note (draft in `docs/FORMAL_NOTE.md`) and literature pass with a novelty statement | Claude / Codex | Codex / Claude | Codex signs the note; novelty statement matches the literature |
| 1 | Design pilot on excluded landscapes under the theory and the Section 3d rival grid; estimator, G set, T set, m grid, sample size fixed; candidate-level delivery instrumentation added | Claude | Codex | Both agree the design discriminates; Section 3 amendments verified in the protocol |
| 2 | Study 3 preregistration (P-A, P1, P2 provisional, P3 replaced, Controls D and E), adversarial review, user review of criteria, freeze, run, verdict | Claude | Codex | Verdict recorded |
| 3 | Study 4 with the reward-sensitive learner, randomized reward crossed with randomized channel access, P-B | Codex | Claude | Verdict recorded |
| 4 | Study 5 pilot and preregistration with four protocols and P-C, accounting per Codex's requirements | joint | joint | Verdict recorded |
| 5 | Claims, manuscript, release with provenance | Claude / Codex | Codex / Claude | Only surviving claims appear |

A critical failure at any gate stops the line there and produces either a successor version with a new risky prediction or a full negative-result paper.

## 5. Record

- sever: three-outcome likelihoods, strict `supported`, legacy-mode labelling, boundary-forecast rejection, infinite-ratio handling, design-pilot step in METHOD.md. Pinned into this repository.
- Model: ancestry lineages, evaluation and adoption counts, contacts, best-candidate holders, adoption-completion diagnostics, final-state export. Defaults reproduce study 1 bit for bit; diagnostics change no result.
- Exploratory order-statistic check saved with data; gaps to the exact reference run from −0.013 to +0.020 and are not all within the provisional margin.
- Studies 1 and 2 stand as recorded: exploratory rejection; inconclusive.
