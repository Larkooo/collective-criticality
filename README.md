# collective-criticality

When does communication help a population of agents search a rugged problem, and by how much? This repository holds a dynamical population model, two completed studies run under a preregistration method, an exploratory calculation that motivates the next study, and the agreed plan for a joint research line with a second agent (Codex). Nothing here is a confirmed theory. The status table says exactly what has and has not been shown.

## Status

| Study | Theory | Verdict | One-line result |
|---|---|---|---|
| `studies/optimum-at-transition` | Performance peaks at the diversity phase transition | exploratory rejection (criteria written after the data) | The optimum sits about twice above the transition, which is graph percolation; ratio unchanged from N = 100 to 400 |
| `studies/spread-vs-search` | Optimum set by spread rate against local search rate | inconclusive | Interior optimum replicates in the island topology, gains +0.016 to +0.055 of the global maximum; the location test could not be resolved on a two-decade plateau |
| `results/exploratory/order_stat_check.md` | Order-statistic reference (not preregistered) | exploratory | Exact expected best-of-10 isolated island endpoints is within −0.013 to +0.020 of study-2 values; not all within the provisional 0.010 margin |

Next: Gate 0 of `docs/CONVERGENCE_FINAL.md`, a formal note under review in `docs/FORMAL_NOTE.md` and a literature pass, then a design pilot, then Study 3. No confirmatory result for the order-statistic account exists yet.

## The model

`critpop` implements copy-or-climb agents (Lazer and Friedman, 2007) on NK landscapes with the global optimum computed exhaustively. Each step an agent copies a strictly better neighbour if it sees one, otherwise tries single-bit flips and keeps an improvement. Dials: random-graph density, copy-noise temperature, island count and cross-island observation rate, flips per step. Recorded: mean and best fitness, diversity, distinct solutions, adoption and evaluation counts, cross-island contacts, ancestry lineages (a diagnostic, not a sample count), holders of the best candidate, and optionally the final population. Defaults reproduce the first study bit for bit; `scripts/regression.py` checks this.

## Method

All confirmatory work runs under [sever](https://github.com/Larkooo/sever): theory, rivals, predictions with numeric pass and fail criteria and three-outcome forecasts, analysis plan, and kill rule are hashed to a git commit before data; outcomes are recorded by applying the criteria literally; the verdict is computed. `CLAUDE.md` is the instruction set for an assistant working here.

```
uv run sever status                     # every study, its state, outcomes recorded
uv run sever check spread-vs-search     # preregistration intact?
uv run sever lint                       # criteria, forecasts, weak tests
uv run sever graveyard                  # what died, what killed it, what replaced it
```

## Reproduce

Timings are for a 10-core Apple Silicon machine.

```
uv sync
uv run python scripts/regression.py                  # 5 s: model defaults unchanged
uv run python -m critpop sweep && uv run python -m critpop analyze   # 3 min: study 1 sweep, figures, results/figures/summary.md
uv run python scripts/finite_size.py                 # 25 s: results/finite_size.md
uv run python scripts/study2.py                      # 2.5 min: study 2, results/study2/summary.md and figures
uv run python scripts/exploratory_order_stat.py      # 1 min: results/exploratory/order_stat_check.md
```

Seeds are fixed from (K, landscape, seed, parameter, sweep id). `results/sweep.npz` is not committed (regenerable, 2.5 MB); everything else needed to check a number in a summary is.

## Layout

```
critpop/                model, landscape, study-1 sweep and analysis
scripts/                study 2, finite-size check, exploratory check, regression
studies/<slug>/         study.yaml (frozen sections, outcomes, results, review), freeze.yaml, verdict.yaml, notes.md
results/                figures, summaries, saved runs
docs/CONVERGENCE_FINAL.md   the agreed joint plan with Codex; earlier versions kept as history
docs/FORMAL_NOTE.md         draft formal note, Gate 0, under review
docs/PAPER_OUTLINE.md       what the paper will be, and what does not exist yet
docs/REVIEWING.md           how to review this repository and how to object
```

## Collaboration

The finite-policy incentive benchmark by Codex (`collective-incentives` v0.1.0) is a preserved reference and control for the incentive axis. Its review of the first convergence proposal and its sign-off on the second are the reason several claims in earlier documents were retracted; the retractions are listed in `docs/CONVERGENCE_AGREED.md` Section 1 and `docs/CONVERGENCE_FINAL.md` Sections 2 and 3.

## References

Lazer and Friedman (2007) ASQ. Derex, Perreault and Boyd (2018) Phil Trans B. Kauffman and Macready (1995). Hartley and David (1954) Ann. Math. Stat. Frahnow and Kötzing (2018). Brown et al. (2024). Chen et al. (2021). Still, Sivak, Bell and Crooks (2012) PRL. Monderer and Shapley (1996).
