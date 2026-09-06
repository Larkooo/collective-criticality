"""Population of agents that copy a better neighbour when they see one, and otherwise
hill-climb locally. This is the Lazer & Friedman (2007) model with two additions:

* `p_link`      density of the random (Erdos-Renyi) communication graph. 0 = isolated
                agents, 1 = everyone sees everyone. This is the connectivity dial.
* `temperature` optional noise in the copy decision. With T > 0 an agent copies its best
                neighbour with probability sigmoid((f_neighbour - f_self) / T). T = 0 is
                the deterministic rule. This is the explicit temperature dial, used to test
                whether connectivity behaves like a temperature.
* `islands`     if set, the graph is `islands` complete cliques of equal size instead of an
                Erdos-Renyi graph, and `migration` is the per-agent per-step probability of
                observing one random agent on another island (study spread-vs-search).
* `n_trials`    single-bit flips an exploring agent tries per step, adopting the best improving
                one. 1 is the Lazer-Friedman rule. This is the local search rate dial.

With temperature <= 0, per-agent fitness never decreases: copying and local updates accept
only strict improvements. In that regime, the final population maximum equals the best search
fitness encountered, including initialization and excluding diagnostic probes. Positive copy
temperatures can accept worse neighbours, so their final maximum is not a best-ever archive.
Ancestry (lineage labels inherited on copying) is recorded as a diagnostic. It is not a count
of independent searches: selection removes roots after their search has contributed.

Defaults reproduce the first study exactly (same random draws in the same order).

Recorded per step: mean fitness, max fitness, diversity (mean pairwise Hamming distance
normalised by n), and the number of distinct solutions. Recorded per run: copy rate (mean
fraction of agents per step that adopted a neighbour's solution different from their own) and
the mean number of distinct solutions each agent visited. Recorded per run: Still et al.
(2012) memory / predictive-power / non-predictive information, computed on a coarse
proxy (agent fitness bin as the state, best-neighbour fitness bin as the signal)."""
from dataclasses import dataclass

import numpy as np

from .landscape import NK

N_FBINS = 10  # fitness bins for the information proxy; bin N_FBINS means "no neighbour"


@dataclass
class RunResult:
    mean_f: np.ndarray
    max_f: np.ndarray
    diversity: np.ndarray
    n_unique: np.ndarray
    i_mem: float
    i_pred: float
    i_np: float
    t_converge: int
    copy_rate: float = 0.0
    visited: float = 0.0
    n_evals: int = 0          # fitness evaluations spent on local search
    n_copies: int = 0         # adoptions of a neighbour's different solution
    lineages: int = 0         # distinct ancestral lineages surviving at the end (ancestry, not fitness)
    lineage_eff: float = 0.0  # effective number of lineages, 1 / sum p_i^2
    contacts: int = 0         # cross-island observation events offered (islands mode)
    best_holders: float = 0.0 # fraction whose final genotype equals a selected final-best genotype
    adopt_before_complete: int = -1  # adoptions while the recipient still had an improving single flip (diagnostics only)
    adopt_after_complete: int = -1   # adoptions by a recipient already at a local optimum (diagnostics only)
    holders_traj: np.ndarray | None = None  # per step, agents holding the genotype that ends as best-found
    final_f: np.ndarray | None = None
    final_X: np.ndarray | None = None
    final_lineage: np.ndarray | None = None


def _diversity(X: np.ndarray) -> float:
    m, n = X.shape
    ones = X.sum(0).astype(np.int64)
    return float((ones * (m - ones)).sum() / (m * (m - 1) / 2) / n)


def _n_unique(X: np.ndarray) -> int:
    return int(np.unique(np.packbits(X, axis=1), axis=0).shape[0])


def _mi(a: np.ndarray, b: np.ndarray, na: int, nb: int) -> float:
    joint = np.bincount(a * nb + b, minlength=na * nb).reshape(na, nb).astype(float)
    joint /= joint.sum()
    pa, pb = joint.sum(1, keepdims=True), joint.sum(0, keepdims=True)
    nz = joint > 0
    return float((joint[nz] * np.log2(joint[nz] / (pa * pb)[nz])).sum())


def _fbin(f: np.ndarray) -> np.ndarray:
    return np.minimum((f * N_FBINS).astype(np.int64), N_FBINS - 1)


def run(land: NK, n_agents: int, p_link: float, temperature: float, steps: int,
        rng: np.random.Generator, islands: int | None = None, migration: float = 0.0,
        n_trials: int = 1, return_state: bool = False, diagnostics: bool = False) -> RunResult:
    """diagnostics=True evaluates, at each adoption, whether the recipient was already at a
    local optimum. Those evaluations are measurement only: not charged to any budget and
    drawing no random numbers, so results are unchanged."""
    m, n = n_agents, land.n
    X = rng.integers(0, 2, (m, n), dtype=np.uint8)
    f = land.fitness(X)
    ar = np.arange(m)
    if islands is None:
        U = np.triu(rng.random((m, m)) < p_link, 1)
        A0 = U | U.T
    else:
        if m % islands:
            raise ValueError("n_agents must be a multiple of islands")
        size = m // islands
        isl = ar // size
        A0 = isl[:, None] == isl[None, :]
        np.fill_diagonal(A0, False)
    A = A0
    lineage = (ar // (m // islands)) if islands is not None else ar.copy()
    n_evals = n_copies = contacts = 0
    before_complete = after_complete = 0

    mean_f = np.empty(steps, np.float32)
    max_f = np.empty(steps, np.float32)
    div = np.empty(steps, np.float32)
    nu = np.empty(steps, np.int32)
    state_bins = np.empty((steps, m), np.int64)
    signal_bins = np.empty((steps, m), np.int64)
    packed = np.empty((steps, m, (n + 7) // 8), np.uint8)
    changed_frac = np.empty(steps, np.float64)
    t_conv = -1

    for t in range(steps):
        if islands is not None:
            A = A0.copy()
            mig = np.where(rng.random(m) < migration)[0]
            contacts += int(mig.size)
            if mig.size:
                other = (isl[mig] + rng.integers(1, islands, mig.size)) % islands
                A[mig, other * size + rng.integers(0, size, mig.size)] = True
        F = np.where(A, f[None, :], -np.inf)
        j_best = F.argmax(1)
        f_best = F[ar, j_best]
        has_nb = np.isfinite(f_best)
        signal_bins[t] = np.where(has_nb, _fbin(np.where(has_nb, f_best, 0.0)), N_FBINS)

        if temperature <= 0:
            copy = f_best > f
        else:
            gap = np.where(has_nb, f_best - f, -np.inf)
            with np.errstate(over="ignore"):
                p_copy = 1.0 / (1.0 + np.exp(-gap / temperature))
            copy = rng.random(m) < p_copy

        newX, newf = X.copy(), f.copy()
        newX[copy] = X[j_best[copy]]
        newf[copy] = f[j_best[copy]]
        changed = copy & (X[j_best] != X).any(1)
        changed_frac[t] = changed.mean()
        n_copies += int(changed.sum())
        if diagnostics and changed.any():
            rec = np.where(changed)[0]
            nb = np.repeat(X[rec][:, None, :], n, axis=1)
            nb[np.arange(rec.size)[:, None], np.arange(n)[None, :], np.arange(n)[None, :]] ^= 1
            improvable = (land.fitness(nb.reshape(-1, n)).reshape(rec.size, n) > f[rec][:, None]).any(1)
            before_complete += int(improvable.sum())
            after_complete += int((~improvable).sum())
        lineage = np.where(copy, lineage[j_best], lineage)

        idx = np.where(~copy)[0]
        n_evals += int(idx.size) * n_trials
        if idx.size and n_trials == 1:
            cand = X[idx].copy()
            cand[np.arange(idx.size), rng.integers(0, n, idx.size)] ^= 1
            fc = land.fitness(cand)
            better = fc > f[idx]
            newX[idx[better]] = cand[better]
            newf[idx[better]] = fc[better]
        elif idx.size:
            bits = rng.integers(0, n, (idx.size, n_trials))
            cand = np.repeat(X[idx][:, None, :], n_trials, axis=1)
            ii = np.repeat(np.arange(idx.size), n_trials)
            cand[ii, np.tile(np.arange(n_trials), idx.size), bits.ravel()] ^= 1
            fc = land.fitness(cand.reshape(-1, n)).reshape(idx.size, n_trials)
            best = fc.argmax(1)
            fb = fc[np.arange(idx.size), best]
            better = fb > f[idx]
            newX[idx[better]] = cand[np.arange(idx.size), best][better]
            newf[idx[better]] = fb[better]

        X, f = newX, newf
        packed[t] = np.packbits(X, axis=1)
        state_bins[t] = _fbin(f)
        mean_f[t], max_f[t] = f.mean(), f.max()
        div[t] = _diversity(X)
        nu[t] = _n_unique(X)
        if t_conv < 0 and nu[t] == 1:
            t_conv = t

    s = state_bins[:-1].ravel()
    i_mem = _mi(s, signal_bins[:-1].ravel(), N_FBINS, N_FBINS + 1)
    i_pred = _mi(s, signal_bins[1:].ravel(), N_FBINS, N_FBINS + 1)
    visited = float(np.mean([np.unique(packed[:, i, :], axis=0).shape[0] for i in range(m)]))
    counts = np.bincount(lineage, minlength=m).astype(float)
    p_lin = counts[counts > 0] / m
    best_holders = float((X == X[int(f.argmax())]).all(1).mean())
    holders_traj = (packed == packed[-1, int(f.argmax())][None, None, :]).all(2).sum(1).astype(np.int32)
    return RunResult(mean_f, max_f, div, nu, i_mem, i_pred, i_mem - i_pred, t_conv,
                     float(changed_frac.mean()), visited, n_evals, n_copies,
                     int((counts > 0).sum()), float(1.0 / (p_lin ** 2).sum()),
                     contacts, best_holders,
                     before_complete if diagnostics else -1, after_complete if diagnostics else -1,
                     holders_traj,
                     f.copy() if return_state else None, X.copy() if return_state else None,
                     lineage.copy() if return_state else None)
