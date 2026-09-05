# Paper outline, and what does not exist yet

**Title (agreed):** When does delayed communication improve collective search? Testing an order-statistic account.

**Thesis (agreed):** We compare a calibrated order-statistic reference with interacting search populations, testing where it predicts performance and where changes in candidate quality, dependence, or dissemination require a richer account. Incentive and language-model experiments test transfer rather than assume it.

**Venue:** TMLR as the working target. No calendar-driven compression. A substantive negative result gets a full paper.

## Sections and their sources

| Section | Content | Source | Exists? |
|---|---|---|---|
| 1 | Question, prior work, novelty statement | Gate 0 literature pass (Codex) | no |
| 2 | Reference, bound, Control D identities, process assumptions A1 to A4 | `docs/FORMAL_NOTE.md` | draft, under review |
| 3 | Classical tests: Study 3, P-A, P1, P2, P3, Controls D and E, with grading | Gate 2 | no |
| 3.1 | History: study 1 exploratory rejection, study 2 inconclusive, what they changed | `studies/`, `results/` | yes, as recorded |
| 4 | Incentive axis: Study 4 with a reward-sensitive learner; potential-game proposition as background | Gate 3 (Codex) | no |
| 5 | Language-model test: Study 5, four protocols, P-C | Gate 4 (joint) | no |
| 6 | Limits, and what would falsify the account further | all gates | no |
| Supp. | Study files, freeze records, verdicts, audit, manifest | repository | partly |

## Honest status

No confirmatory result for the order-statistic account exists. The two completed studies tested earlier theories, one of which is dead and one of which is unresolved. The exploratory check is suggestive and its gaps to the reference are not all inside the provisional margin. The paper cannot be drafted beyond Section 2 and Section 3.1 until Study 3 has a verdict. Writing more now would violate the method this repository runs under.

## On the existing finite-policy paper (Codex, `collective-incentives` v0.1.0)

That paper is complete for the claim it makes: a reproducible, audited baseline on three small tasks, with correctly stated established mathematics. It does not need new experiments to be what it is. It should not be extended into the joint paper, because its system is too small to show the dynamics the joint paper is about; its role is a preserved reference and control for the incentive axis, and its potential-game proposition becomes background in Section 4.
