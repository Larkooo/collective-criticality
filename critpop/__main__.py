import argparse

from .analyze import analyze
from .sweep import default_config, run_sweep


def main():
    ap = argparse.ArgumentParser(prog="critpop")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sweep", help="run the connectivity and temperature sweeps")
    s.add_argument("--out", default="results/sweep.npz")
    s.add_argument("--quick", action="store_true", help="small smoke-test configuration")
    s.add_argument("--workers", type=int, default=None)
    a = sub.add_parser("analyze", help="figures and summary from a sweep file")
    a.add_argument("path", nargs="?", default="results/sweep.npz")
    a.add_argument("--figdir", default="results/figures")
    args = ap.parse_args()
    if args.cmd == "sweep":
        run_sweep(default_config(args.quick), args.out, args.workers)
    else:
        analyze(args.path, args.figdir)


if __name__ == "__main__":
    main()
