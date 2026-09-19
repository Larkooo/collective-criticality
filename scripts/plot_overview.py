"""Plot the recorded island-search experiment without running new simulations."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=root / "docs/assets/communication.png")
    args = parser.parse_args()
    runs = np.load(root / "results/study2/runs.npy", allow_pickle=False)
    plt.rcParams.update({"font.size": 11, "font.family": "sans-serif"})
    fig, ax = plt.subplots(figsize=(10, 5.2), layout="constrained")
    fig.set_facecolor("#f7f5ef")
    ax.set_facecolor("#f7f5ef")
    for ruggedness, color in [(2, "#3e7368"), (6, "#a16538"), (12, "#626b9b")]:
        selected = runs[(runs["sweep"] == "A") & (runs["nt"] == 1) & (runs["k"] == ruggedness)]
        rates = np.unique(selected["m"])
        means = []
        for rate in rates:
            point = selected[selected["m"] == rate]
            if len(point) != 24 or len(np.unique(point["land"])) != 4:
                raise ValueError("Expected four landscapes and six seeds at every rate")
            means.append(float(point["perf"].mean()))
        ax.plot(rates, means, "o-", color=color, linewidth=2, markersize=5,
                label=f"K = {ruggedness}")
        print(f"K={ruggedness}: no sharing={means[0]:.4f}, "
              f"best interior={max(means[1:-1]):.4f}, maximum sharing={means[-1]:.4f}")
    ax.set_xscale("symlog", linthresh=0.001)
    ax.set_xlim(-0.00012, 1.3)
    ax.set_xticks([0, 0.001, 0.01, 0.1, 1], ["0", "0.001", "0.01", "0.1", "1"])
    ax.set_ylim(0.83, 1.01)
    ax.set_xlabel("Probability of observing another group per agent, per step", labelpad=12)
    ax.set_ylabel("Final mean solution quality / global optimum", labelpad=12)
    ax.set_title("Sharing discoveries helps — up to a point", loc="left", fontsize=17, pad=20)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#aaa69c")
    ax.grid(axis="y", color="#d8d5cb", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.legend(title="Landscape ruggedness", frameon=False, loc="lower center", ncols=3)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=160)
    plt.close(fig)
    print(args.out)


if __name__ == "__main__":
    main()
