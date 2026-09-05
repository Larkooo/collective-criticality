"""NK fitness landscapes (Kauffman) with an exhaustively computed global optimum."""
import numpy as np


class NK:
    """n loci, each interacting with the next k loci (cyclic). Fitness is the mean of
    n random contributions, each keyed by a (k+1)-bit context. k=0 is smooth, single-peaked;
    larger k is more rugged with more local optima."""

    def __init__(self, n: int, k: int, rng: np.random.Generator):
        self.n, self.k = n, k
        self.table = rng.random((n, 1 << (k + 1)))
        self.idx = (np.arange(n)[:, None] + np.arange(k + 1)[None, :]) % n
        self._locus = np.arange(n)[None, :]
        self.fmax = self._global_max()

    def raw_fitness(self, X: np.ndarray) -> np.ndarray:
        """X: (m, n) bits -> (m,) fitness in [0, 1]."""
        ctx = np.zeros((X.shape[0], self.n), dtype=np.int64)
        for j in range(self.k + 1):
            ctx |= X[:, self.idx[:, j]].astype(np.int64) << j
        return self.table[self._locus, ctx].mean(axis=1)

    def fitness(self, X: np.ndarray) -> np.ndarray:
        """Fitness normalised so the global optimum is 1."""
        return self.raw_fitness(X) / self.fmax

    def _global_max(self) -> float:
        total, chunk = 1 << self.n, 1 << 14
        shifts = np.arange(self.n, dtype=np.int64)[None, :]
        best = 0.0
        for start in range(0, total, chunk):
            ints = np.arange(start, min(start + chunk, total), dtype=np.int64)[:, None]
            X = ((ints >> shifts) & 1).astype(np.uint8)
            best = max(best, float(self.raw_fitness(X).max()))
        return best
