"""Subcritical Galton-Watson branching process with Poisson offspring: exact delivery
probability, expected size, and size variance via the generating function, plus a Monte
Carlo check. Used as the analytic anchor for docs/GAP_THEORY.md Section 2."""
import numpy as np


def reach_probability(sigma: float, depth: int) -> float:
    """P(cascade survives to generation `depth`) for Poisson(sigma) offspring, exact."""
    q = 0.0  # P(extinct by generation 0) = 0 (the root exists)
    for _ in range(depth):
        q = float(np.exp(sigma * (q - 1.0)))
    return 1.0 - q


def expected_size(sigma: float) -> float:
    return 1.0 / (1.0 - sigma)


def size_variance(sigma: float) -> float:
    return sigma / (1.0 - sigma) ** 3


def objective(sigma: np.ndarray, depth: int, lam: float, mu: float, value: float = 1.0) -> np.ndarray:
    """J = value * P(reach depth) - lam * E[size] - mu * Var(size)."""
    return np.array([value * reach_probability(s, depth) - lam * expected_size(s) - mu * size_variance(s) for s in sigma])


def optimum_gap(depth: int, lam: float, mu: float, grid: np.ndarray | None = None) -> tuple[float, float]:
    """(delta*, J*) over a fine grid in delta = 1 - sigma. Returns (nan, best J) if the
    maximum is at the smallest-sigma end, which is the silence regime."""
    delta = np.logspace(-4, 0, 800) if grid is None else grid
    J = objective(1.0 - delta, depth, lam, mu)
    j = int(np.argmax(J))
    if j == len(delta) - 1 or J[j] <= 0:
        return float("nan"), float(J[j])
    if 0 < j < len(delta) - 1:  # parabolic refinement in log delta
        y0, y1, y2 = J[j - 1:j + 2]
        den = y0 - 2 * y1 + y2
        if den < 0:
            off = 0.5 * (y0 - y2) / den
            return float(10 ** (np.log10(delta[j]) + off * (np.log10(delta[j]) - np.log10(delta[j - 1])))), float(J[j])
    return float(delta[j]), float(J[j])


def monte_carlo_check(sigma: float, depth: int, n: int, rng: np.random.Generator) -> dict:
    reached, sizes = 0, np.zeros(n)
    for i in range(n):
        gen, total, alive = 0, 1, 1
        while alive and gen < depth:
            alive = int(rng.poisson(sigma, alive).sum())
            total += alive
            gen += 1
        reached += alive > 0
        # continue to extinction for the size (cap to avoid rare long runs)
        while alive and total < 10_000:
            alive = int(rng.poisson(sigma, alive).sum())
            total += alive
        sizes[i] = total
    return {"reach_mc": reached / n, "reach_exact": reach_probability(sigma, depth),
            "size_mc": float(sizes.mean()), "size_exact": expected_size(sigma),
            "var_mc": float(sizes.var()), "var_exact": size_variance(sigma)}


def cost_per_delivery(delta: np.ndarray, depth: int) -> np.ndarray:
    """Throughput objective: expected cascade size per delivered message, exact."""
    return np.array([expected_size(1.0 - d) / max(reach_probability(1.0 - d, depth), 1e-300) for d in delta])


def throughput_gap(depth: int, grid: np.ndarray | None = None) -> float:
    delta = np.logspace(-4, 0, 800) if grid is None else grid
    c = cost_per_delivery(delta, depth)
    j = int(np.argmin(c))
    if 0 < j < len(delta) - 1:
        y0, y1, y2 = np.log(c[j - 1:j + 2])
        den = y0 - 2 * y1 + y2
        if den > 0:
            off = 0.5 * (y0 - y2) / den
            return float(10 ** (np.log10(delta[j]) + off * (np.log10(delta[j]) - np.log10(delta[j - 1]))))
    return float(delta[j])
