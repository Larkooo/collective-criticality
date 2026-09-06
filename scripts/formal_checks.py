"""Executable checks for the revised Gate 0 note; not a confirmatory study.

The path-copy reference accepts explicit contact schedules. It is a coarse island
model, not the original agent-level simulator. Run with Python 3.12+.
Use --model-checks --repo PATH to reproduce the temperature-scope witness.
"""
import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import random
import sys

EDITORIAL_SEED = 17764446679665605942


def path_copy(paths, contacts):
    """Synchronous copy-or-advance on fixed, monotone island paths.

    contacts[t][g] lists the other island representatives visible to g at step t.
    Copy uses the donor's pre-step path and cursor. Otherwise advance one position.
    Each path includes its initial observation and one observation per local step.
    """
    count = len(paths)
    if count == 0 or not paths[0]:
        raise ValueError('At least one nonempty path is required')
    horizon = len(contacts)
    for path in paths:
        if len(path) < horizon + 1:
            raise ValueError('Each path must cover the entire horizon')
        if any(not 0 <= value <= 1 for value in path):
            raise ValueError('Quality must lie in [0,1]')
        if any(a > b for a, b in zip(path, path[1:])):
            raise ValueError('Reference paths must be nondecreasing')
    states = [(g, 0) for g in range(count)]
    archive_best = max(path[0] for path in paths)
    adoptions = advances = 0
    for schedule in contacts:
        if len(schedule) != count:
            raise ValueError('One contact list per island is required')
        quality = [paths[root][cursor] for root, cursor in states]
        next_states = []
        for g, peers in enumerate(schedule):
            if any(j < 0 or j >= count or j == g for j in peers):
                raise ValueError('Invalid external island contact')
            better = [j for j in peers if quality[j] > quality[g]]
            if better:
                donor = max(better, key=lambda j: (quality[j], -j))
                next_states.append(states[donor])
                adoptions += 1
            else:
                root, cursor = states[g]
                next_states.append((root, cursor + 1))
                advances += 1
        states = next_states
        archive_best = max(archive_best, *(paths[r][c] for r, c in states))
    values = [paths[r][c] for r, c in states]
    return {'best_found': archive_best, 'representative_mean': sum(values) / count,
            'states': states, 'adoptions': adoptions, 'advances': advances}


def contact_schedule(count, size, rate, horizon, rng):
    if count < 1 or size < 1 or not 0 <= rate <= 1 or horizon < 0:
        raise ValueError('Invalid contact parameters')
    if count == 1:
        return [[[]] for _ in range(horizon)]
    schedule = []
    for _ in range(horizon):
        step = []
        for g in range(count):
            peers = []
            for _ in range(size):
                if rng.random() < rate:
                    j = rng.randrange(count - 1)
                    peers.append(j if j < g else j + 1)
            step.append(peers)
        schedule.append(step)
    return schedule


def mathematical_checks():
    cases = 0
    # Endogenous stopping: request a second draw only after a low first draw.
    actual = F(0)
    for first, second in product([F(3, 10), F(7, 10)], repeat=2):
        actual += (first if first == F(7, 10) else max(first, second)) / 4
    mixture = F(1, 2) * F(1, 2) + F(1, 2) * F(3, 5)
    assert actual == F(3, 5) and mixture == F(11, 20)
    cases += 1

    # Same marginals, different joint continuations.
    one = F(1, 2)
    two = sum(max(x, y) for x, y in product([F(3, 10), F(7, 10)], repeat=2)) / 4
    assert two - one == F(1, 10)
    cases += 1

    # A mean island maximum is not an unreached agent's mean holding.
    assert (F(2, 10) + F(8, 10)) / 2 == F(1, 2)
    assert max(F(2, 10), F(8, 10)) == F(8, 10)
    # Quality-dependent coverage cannot be factored into products of means.
    expected_product = (F(0) * F(3, 10) + F(1) * F(7, 10)) / 2
    product_of_means = F(1, 2) * F(1, 2)
    assert expected_product == F(35, 100) and product_of_means == F(25, 100)
    cases += 2

    # Equality family for Hartley-David: q(u)=u^(G-1), which is continuous.
    for g in range(2, 13):
        mu = F(1, g)
        variance = F(1, 2*g-1) - mu**2
        expected_max = F(g, 2*g-1)
        assert (expected_max-mu)**2 == variance * F((g-1)**2, 2*g-1)
        cases += 1

    paths = [[F(2, 10), F(4, 10), F(8, 10)],
             [F(3, 10), F(5, 10), F(7, 10)]]
    independent = path_copy(paths, [[[], []], [[], []]])
    early = path_copy(paths, [[[1], [0]], [[1], [0]]])
    assert independent['best_found'] == F(8, 10)
    assert early['best_found'] == F(7, 10)
    assert early['states'] == [(1, 1), (1, 2)]
    assert early['advances'] + early['adoptions'] == 4
    # Complete terminal broadcast replaces both states with the best state's pointer.
    winner = max(independent['states'], key=lambda rc: paths[rc[0]][rc[1]])
    broadcast_states = [winner, winner]
    assert len({r for r, _ in broadcast_states}) == 1
    assert all(paths[r][c] == F(8, 10) for r, c in broadcast_states)
    cases += 2

    assert path_copy([[F(3, 10)]], [])['best_found'] == F(3, 10)
    assert contact_schedule(1, 3, 1, 2, random.Random(1)) == [[[]], [[]]]
    cases += 2

    # Pure propagation continuous-time idealization: exact sum of waiting times.
    for g in range(2, 13):
        size, rate = 3, F(1, 100)
        waiting = sum(1 / (size * rate * F(j*(g-j), g-1)) for j in range(1, g))
        harmonic = sum(F(1, j) for j in range(1, g))
        formula = 2 * (g-1) * harmonic / (g * size * rate)
        assert waiting == formula
        cases += 1

    # Seeded property checks: reference values never exceed the full isolated budget.
    rng = random.Random(EDITORIAL_SEED)
    for _ in range(100):
        g, horizon = 3, 5
        paths = [sorted(F(rng.randrange(101), 100) for _ in range(horizon+1)) for _ in range(g)]
        contacts = contact_schedule(g, 2, .2, horizon, rng)
        result = path_copy(paths, contacts)
        assert result['best_found'] <= max(path[horizon] for path in paths)
        assert result['advances'] + result['adoptions'] == g*horizon
        cases += 1
    return {'checks_passed': cases, 'stopping_counterexample': {'actual': float(actual),
            'incorrect_count_mixture': float(mixture)},
            'equal_marginal_continuations': {'duplicate_max': float(one), 'independent_max': float(two)},
            'path_copy_example': {'isolated_best': .8, 'early_copy_best': .7,
                                  'post_broadcast_roots': 1, 'post_broadcast_best': .8}}


def model_check(repo):
    import numpy as np
    sys.path.insert(0, str(Path(repo).resolve()))
    from critpop.landscape import NK
    from critpop.model import run

    class Observed:
        def __init__(self, landscape):
            self.landscape, self.n, self.values = landscape, landscape.n, []

        def fitness(self, x):
            values = self.landscape.fitness(x)
            self.values.extend(values.tolist())
            return values

    landscape = NK(5, 2, np.random.default_rng(8))
    seen = Observed(landscape)
    result = run(seen, 3, 1.0, 1.0, 8, np.random.default_rng(1), return_state=True)
    best, final = max(seen.values), float(result.final_f.max())
    assert best > final + .04
    assert np.any(np.diff(result.max_f) < 0)
    for seed in range(10):
        zero_seen = Observed(landscape)
        zero = run(zero_seen, 3, 1.0, 0.0, 8, np.random.default_rng(seed), return_state=True)
        assert np.all(np.diff(zero.max_f) >= 0)
        assert np.isclose(max(zero_seen.values), zero.final_f.max(), rtol=0, atol=1e-12)
    return {'temperature': 1.0, 'landscape_seed': 8, 'run_seed': 1,
            'best_observed': best, 'final_best': final,
            'zero_temperature_control_runs_passed': 10,
            'interpretation': 'Monotonicity requires the zero-temperature elitist restriction.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-checks', action='store_true')
    parser.add_argument('--repo', default='.')
    args = parser.parse_args()
    report = {'status': 'passed', 'editorial_seed': EDITORIAL_SEED,
              'scope': 'Mathematical and implementation checks, not confirmatory performance evidence',
              'mathematical': mathematical_checks()}
    if args.model_checks:
        report['model_scope_witness'] = model_check(args.repo)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
