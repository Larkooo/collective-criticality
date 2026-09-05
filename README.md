# critpop

A minimal, reproducible test of one claim: in a population of innovating agents, the
amount of communication between them behaves like a temperature, and collective
performance peaks near a phase transition of the population's diversity.

The model is Lazer and Friedman (2007): agents sit on a rugged NK landscape, copy a
better neighbour when they see one, and otherwise hill-climb locally. Two dials are
added. `p_link` is the density of the communication graph. `temperature` is optional
noise in the copy decision. Everything else is held fixed.

## What is measured

Per run, at every step: mean fitness and best fitness relative to the exhaustively
computed global optimum, diversity as mean pairwise Hamming distance, and the number
of distinct solutions. Per run, once: the Still et al. (2012) decomposition of the
information an agent's state holds about its best neighbour into memory, predictive
power, and their difference, the non-predictive information. That last quantity is a
coarse proxy (fitness bins, not full solutions) and is labelled as such.

Susceptibility is the run-to-run variance of an observable across seeds on the same
landscape, averaged over landscapes, times the population size. Landscape-to-landscape
variance is deliberately excluded.

## The three tests

1. **Peak coincidence.** Does the connectivity that maximises mean fitness sit where
   the susceptibility peaks? If yes, the optimum is at a transition. If no, it is just
   an interior optimum, which Derex and Lazer already showed.
2. **Data collapse.** Rescale connectivity by the transition location for each
   ruggedness K. If diversity and performance curves for different K fall onto one
   master curve, connectivity is a universal control parameter for this system.
3. **Connectivity versus temperature.** Sweep explicit copy-noise temperature on a
   complete graph and compare the (diversity, performance) curve it traces with the
   one traced by the connectivity sweep. If they coincide, the two dials are
   interchangeable, which is the precise version of "connectivity is a temperature".

Plus one measurement: how non-predictive information varies with connectivity and
whether it tracks performance or susceptibility.

## Run

```
uv sync
uv run python -m critpop sweep --quick      # ~5 s smoke test
uv run python -m critpop sweep             # full sweep, a few minutes on 10 cores
uv run python -m critpop analyze           # figures and results/figures/summary.md
```

## Caveats

The diversity transition in this model is partly the percolation transition of the
random graph, which happens at mean degree 1 regardless of the landscape. Whether the
performance optimum tracks that threshold or moves with K is exactly what the collapse
test asks. The information proxy uses ten fitness bins and pools over all time steps,
so it is a qualitative measure. Nothing here involves language models. That is the
next step, not this one.

## References

- Lazer, D. and Friedman, A. (2007). The network structure of exploration and exploitation. ASQ.
- Derex, M., Perreault, C. and Boyd, R. (2018). Divide and conquer: intermediate levels of population fragmentation maximize cultural accumulation. Phil Trans R Soc B.
- Kauffman, S. and Macready, W. (1995). Technological evolution and adaptive organizations. Complexity.
- Still, S., Sivak, D., Bell, A. and Crooks, G. (2012). Thermodynamics of prediction. PRL.
- Hidalgo, J. et al. (2014). Information-based fitness and the emergence of criticality in living systems. PNAS.
