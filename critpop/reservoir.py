"""Echo-state network with a delayed-recall task and a measured largest Lyapunov exponent.
The subcritical-side system of docs/GAP_THEORY.md: the task fixes a memory depth k, input
noise plays the role of the cost, and the measured propagation multiplier is exp(lambda_max)."""
from dataclasses import dataclass

import numpy as np


@dataclass
class ESNResult:
    rho: float
    delay: int
    noise: float
    r2: float
    sigma_meas: float  # exp(largest Lyapunov exponent) along the driven trajectory


def _scaled_matrix(n: int, density: float, rho: float, rng: np.random.Generator) -> np.ndarray:
    W = rng.normal(0, 1, (n, n)) * (rng.random((n, n)) < density)
    ev = np.max(np.abs(np.linalg.eigvals(W)))
    return W * (rho / ev)


def run_esn(rho: float, delay: int, noise: float, rng: np.random.Generator, n: int = 200,
            density: float = 0.1, washout: int = 200, train: int = 1500, test: int = 800,
            input_scale: float = 0.5, ridge: float = 1e-6, lyap_steps: int = 400) -> ESNResult:
    W = _scaled_matrix(n, density, rho, rng)
    w_in = rng.uniform(-input_scale, input_scale, n)
    total = washout + train + test
    u = rng.uniform(-0.5, 0.5, total + delay)
    xi = rng.normal(0, 1, (total, n)) * noise
    X = np.zeros((total, n))
    x = np.zeros(n)
    for t in range(total):
        x = np.tanh(W @ x + w_in * u[t + delay] + xi[t])
        X[t] = x
    target = u[:total]  # u(t + delay - delay): recall the input from `delay` steps ago
    A, y = X[washout:washout + train], target[washout:washout + train]
    beta = np.linalg.solve(A.T @ A + ridge * np.eye(n), A.T @ y)
    At, yt = X[washout + train:], target[washout + train:]
    pred = At @ beta
    r2 = 1.0 - float(((yt - pred) ** 2).sum() / ((yt - yt.mean()) ** 2).sum())

    # largest Lyapunov exponent: renormalized perturbation along the same driven trajectory
    x0 = X[washout].copy()
    x1 = x0 + 1e-6 * rng.normal(0, 1, n) / np.sqrt(n)
    d0 = float(np.linalg.norm(x1 - x0))
    logs = []
    for t in range(washout + 1, washout + 1 + lyap_steps):
        drive = w_in * u[t + delay] + xi[t]
        x0 = np.tanh(W @ x0 + drive)
        x1 = np.tanh(W @ x1 + drive)
        d = float(np.linalg.norm(x1 - x0))
        logs.append(np.log(max(d, 1e-300) / d0))
        x1 = x0 + (x1 - x0) * (d0 / max(d, 1e-300))
    return ESNResult(rho, delay, noise, r2, float(np.exp(np.mean(logs))))
