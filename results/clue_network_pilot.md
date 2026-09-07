# Distributed-clue network run with gemma3:4b: depth 4, fault rate 0.2, 3 instances per sigma

| sigma | accuracy | mean calls | mean notes at target | mean corrupted numbers at target | all clues arrived |
|---|---|---|---|---|---|
| 0.8 | 0.00 | 21.7 | 0.0 | 0.0 | 0.00 |
| 1.4 | 0.00 | 58.0 | 2.0 | 1.3 | 0.67 |

Elapsed 391s.


Reading: three instances per rate is a harness check, not a measurement. Delivery moved in the predicted direction (no clue reached the target at 0.8; all three arrived in two of three instances at 1.4), and the target then failed on the contradictions it received (1.3 corrupted numbers on average), which is what the measured confusion curve predicts at this fault rate. No further model runs on this benchmark; see results/clue_theory_budget.md for why it cannot show a gap.
