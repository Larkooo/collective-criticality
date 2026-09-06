# Adaptive communication and the distance from criticality: a research program

Status: hypothesis and literature synthesis, 2026-09-06. Nothing here is a result. Written so that Codex can review it and so that its first testable piece can be attached to Study 3 without changing Study 3's frozen sections.

## 1. The idea as posed

Units in a system hold local information and must decide what to transmit, to whom, how far, and how confidently. Transmitting everything spreads noise and costs bandwidth; suppressing everything loses signal. An objective of the form

    max over policies π of [ useful information delivered − λ · communication cost − μ · instability ]

might, when optimized, produce dynamics near a transition between activity dying out and activity running away. Brain criticality would then be one instance of a general principle. The program's own rule, stated in the summary that prompted this document, is not to assume criticality is optimal but to derive an objective and see what falls out. This document takes that rule seriously, and what falls out is not criticality.

## 2. What the literature already shows, grouped by what it establishes

**Criticality maximizes some information-theoretic quantities.** Dynamic range in excitable networks (Kinouchi and Copelli 2006), information capacity and transmission near a critical branching point (Shew and Plenz 2013), computational capacity of recurrent networks at the edge of chaos (Bertschinger and Natschläger 2004; Boedecker et al. 2012), Fisher information and related utility measures at phase transitions (Chen and Prokopenko 2024 primer). In each case the quantity that peaks at criticality was chosen after the fact. Different quantities peak at different distances from the transition.

**The optimum is task-dependent, and often not at criticality.** Cramer et al. 2020, on neuromorphic hardware with plasticity: information-theoretic capacity peaks at criticality, but only complex memory-intensive tasks profit from it, while simple tasks suffer from it. Their reading is that biological networks operate in the vicinity of a critical point where computation can be tuned to task requirements. Wilting and Priesemann, from spike recordings: cortex sits slightly subcritical, with a safety margin. Hidalgo et al. 2014: agents whose fitness depends on modelling a heterogeneous environment self-tune toward criticality as environmental complexity increases, and remain non-critical for simple, predictable environments. Our own study 1: the performance optimum of a search population sits about twice above the percolation transition of its communication graph, on the connected side, for every ruggedness tested and for populations of 100 to 400.

**Self-organization to criticality by local rules is mechanistically established, but the rules tune an activity set point, not a communication objective.** Bornholdt and Rohlf 2000 (topology evolution), Levina, Herrmann and Geisel 2007 (dynamic synapses), Ma, Turrigiano, Wessel and Hengen 2019 (homeostatic tuning to criticality in vivo), Zeraati, Priesemann and Levina 2021 (review). Criticality is a by-product of a homeostatic target in these models. Whether an explicit communication-cost objective produces the same thing is open.

**Learning moves artificial networks toward the edge of chaos.** Trainability at initialization requires it (Schoenholz et al. 2017). Recent work reports that training moves both stable and chaotic recurrent networks closer to the transition, with richer representations learned on the ordered side of it, and a 2026 preprint studies critical branching mechanisms in recurrent networks directly.

**Signatures are not evidence.** Zipf-like distributions arise generically from unobserved latent variables without any tuning (Schwab, Nemenman and Mehta 2014; Aitchison, Corradi and Latham 2016). Power-law avalanches arise from non-critical processes (Touboul and Destexhe 2017). Reviews of the field list the question as unresolved (Wilting and Priesemann 2019; O'Byrne and Jerbi 2022). Any theory in this space must predict something that scale-free statistics alone do not.

**A common measurement exists.** The multistep-regression estimator of Wilting and Priesemann 2018 recovers the branching parameter and autocorrelation time from heavily subsampled activity. It applies unchanged to neural spikes, to adoption cascades in a search population, and to message cascades in a multi-agent system. This is the primitive that lets a distance-from-criticality claim be compared across domains as a measured number rather than an analogy.

**Learned communication in multi-agent reinforcement learning has cost-aware gating but no dynamical analysis.** Gating and scheduling of messages (Jiang and Lu 2018; Kim et al. 2019; Singh, Jain and Sukhbaatar 2019), information-bottleneck communication (Wang et al. 2020), and 2025 to 2026 work on bandwidth-constrained variational and vector-quantized messages. I found no paper in this line that measures the propagation regime of the emergent communication network. That is a gap, not a claim that nobody has done it.

**Psychedelics as a perturbation.** LSD raises the fitted Ising temperature and algorithmic complexity of BOLD dynamics and moves the brain toward the disordered side (Ruffini et al. 2023); LSD and psilocybin raise the fractal dimension of cortical activity (Varley et al. 2020); a 2025 preprint reports the same direction for ayahuasca; the entropic-brain framing is Carhart-Harris. These are consistent with a gain increase that reduces the distance to the transition and can cross it. None of them measure a branching parameter, and the molecule-to-network chain in the summary is a decade-scale program in other people's laboratories.

## 3. The pattern

Four independent results have the same shape. Priesemann: slightly subcritical, with a margin. Cramer: the best distance from criticality depends on how much memory the task needs. Hidalgo: criticality is approached only as environmental complexity grows without bound. Ours: just above the transition needed for information to reach the population, and no closer.

The shape is: **the optimum lies on whichever side of the transition makes the task feasible, as close to the transition as the task's propagation requirement forces, with a gap set by the cost of over-propagation.** Criticality is the limit of that statement as the requirement grows without bound or the cost goes to zero. It is not the optimum for any finite task with a positive cost.

## 4. A candidate representation

Take a unit that, when active, activates each of its k downstream units with probability p, so the branching ratio is σ = kp and the transition is at σ = 1. Write δ for the distance from the transition, positive on the subcritical side. A communication policy sets p and the targeting; the objective is the one in Section 1 with three terms made concrete.

Delivery. A message must reach range L (generations, or equivalently a horizon). In a subcritical branching process the probability of surviving to generation L is approximately σ^L, so delivered information is I₀ e^{−δL} for small δ.

Cost. The expected number of activations per message is Σ σ^t = 1/δ. Bandwidth cost λ/δ.

Instability. The variance of cascade size scales as 1/δ³ for a subcritical branching process with fixed offspring variance. Penalty μ/δ³, or any penalty that diverges as δ → 0.

Then J(δ) = I₀ e^{−δL} − λ/δ − μ/δ³, and stationarity gives I₀ L e^{−δL} = λ/δ² + 3μ/δ⁴. For δL small: with bandwidth cost alone, δ* ≈ (λ / I₀L)^{1/2}; with instability cost alone, δ* ≈ (3μ / I₀L)^{1/4}. In every case δ* > 0 for positive cost, δ* decreases with the range demand L as a power law whose exponent identifies the dominant cost, and δ* → 0 only as L → ∞. That is Hidalgo's result derived, Cramer's result derived, and Priesemann's margin given a reason.

The supercritical side is the same calculation with the roles reversed. In a search population the task is feasible only above the percolation transition, because the best solution must reach everyone within the horizon; the cost of over-propagation is the loss of independent lineages. Performance is coverage times the value of the surviving independent searches, coverage saturates just above the transition, and the loss of lineages grows with connectivity, so the optimum sits just above the transition at a gap set by how fast coverage saturates relative to the horizon. Our study 1 measured that gap as a factor of about two in mean degree; Study 3's prediction P2 already tests whether it scales with the horizon.

The unifying statement: σ* = σ_c ± δ*(L, λ, μ), with the sign fixed by feasibility and δ* a decreasing function of the propagation demand and an increasing function of the costs.

## 5. What it predicts and what would kill it

- P1. δ* > 0 at any finite demand with positive cost. Killed by a system whose measured optimum is at σ = 1 within estimator resolution while its costs are demonstrably positive.
- P2. δ* falls with the range or horizon demand as a power law with exponent between 1/4 and 1/2 under the cost models above. Killed by a flat or non-monotone dependence.
- P3. δ* rises with λ and μ. Killed by insensitivity to an imposed communication cost.
- P4. The side of the transition is determined by feasibility: coverage tasks supercritical, stability tasks subcritical. Killed by a coverage task whose optimum is subcritical or the reverse.
- P5. Agents that learn communication policies under an explicit cost converge to a measured σ(π*) obeying P1 to P3. Killed by learned policies whose cascade branching ratio does not move with the task's range demand.
- P6. Across cortical areas, the measured distance from criticality decreases with the integration timescale the area's function demands. Checkable against published branching-parameter and timescale estimates; not our experiment.
- P7. Increasing gain pharmacologically (5-HT2A agonism) reduces δ and can cross the transition, with task-dependent performance: worse on short-range precision tasks, better on long-range integration or flexibility. Checkable against the literature; not our experiment.

Rivals carried: criticality is optimal (δ* = 0); signatures without criticality, so only measured σ counts; structure-only, δ independent of L; homeostatic by-product, σ set by an activity target unrelated to task demands; pluralism, no shared objective and the four results in Section 3 are a coincidence.

## 6. What "universal" would require

The claim earns the word only if δ* measured with the same estimator in at least three different systems collapses onto one curve against the demand variable, with the exponent in P2 consistent across them, and with P4 holding for the sign. An analogy across brains, markets, and democracies does not count and will not be written. Markets and democracies are not in scope until a propagation demand and a cost can be operationalized and σ can be measured in them.

## 7. Path

**Paper 1, feasible now, classical.** "Near-critical, not critical: task-determined distance from the propagation transition." Three systems, one estimator, one demand dial. (a) The branching process with cost: analytic δ*(L, λ, μ) plus simulation. (b) The search population: supercritical side; Study 3 as planned, plus the branching ratio of adoption cascades measured with the multistep-regression estimator on the same runs, so the study feeds both lines without touching its frozen sections. (c) A reservoir or recurrent network with a memory-length dial: subcritical side; optimal spectral radius against required memory, partly known and to be cited. Confirmatory content is P1 to P4 with a data collapse across (a) to (c). Preregistered under sever with a design pilot. This is the criticality question asked the way the summary says it should be asked, and the answer it is set up to find is "no, near it, at a distance you can compute."

**Paper 2, the thousands-of-agents idea in falsifiable form.** Multi-agent reinforcement learning with gated communication and an explicit bandwidth cost, the task's range demand as a dial, and the branching ratio of message cascades measured. Tests P5. Small systems first. This is the piece that no existing paper appears to contain.

**Neuroscience and psychedelics.** A check-against-literature section for P6 and P7, at most. Not experiments of ours, and not in Paper 1.

**Relation to the current line.** The order-statistic account in `CONVERGENCE_FINAL.md` is the supercritical-side instance of Section 4. Nothing in Study 3's frozen plan changes; one measurement is added to its analysis, reported separately, and any prediction about it is preregistered in a new study file rather than appended to the frozen one.

## 8. Sources consulted for this document

Kinouchi and Copelli 2006; Shew and Plenz 2013; Bertschinger and Natschläger 2004; Boedecker et al. 2012; Chen and Prokopenko 2024; Cramer et al. 2020; Wilting and Priesemann 2018, 2019; Hidalgo et al. 2014; Bornholdt and Rohlf 2000; Levina, Herrmann and Geisel 2007; Ma et al. 2019; Zeraati, Priesemann and Levina 2021; Schoenholz et al. 2017; Schwab, Nemenman and Mehta 2014; Aitchison, Corradi and Latham 2016; Touboul and Destexhe 2017; O'Byrne and Jerbi 2022; Jiang and Lu 2018; Kim et al. 2019; Singh, Jain and Sukhbaatar 2019; Wang et al. 2020; Ruffini et al. 2023; Varley et al. 2020; Carhart-Harris 2014, 2019. Recent 2025 to 2026 items found by search are listed in the accompanying message.
