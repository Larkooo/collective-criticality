"""Bit-for-bit regression: rerun the quick sweep and compare with results/quick.npz, which was
produced by the first version of the model. Every later change to critpop.model must keep this
passing with default arguments. Runs in about five seconds."""
import os
import sys
import tempfile

import numpy as np

from critpop.sweep import default_config, run_sweep

KEYS = ["traj", "i_mem", "i_pred", "i_np", "t_conv", "p", "T", "k", "seed"]

if __name__ == "__main__":
    out = os.path.join(tempfile.mkdtemp(), "quick.npz")
    run_sweep(default_config(quick=True), out)
    a, b = np.load("results/quick.npz"), np.load(out)
    same = all(np.array_equal(a[k], b[k]) for k in KEYS)
    print("regression:", "PASS, defaults reproduce the first study bit for bit" if same else "FAIL")
    sys.exit(0 if same else 1)
