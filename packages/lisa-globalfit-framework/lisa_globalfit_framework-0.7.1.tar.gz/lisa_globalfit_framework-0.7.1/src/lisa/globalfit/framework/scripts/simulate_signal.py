import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from pathlib import Path

from lisa.globalfit.framework.simulator import Simulator


def add_simulator_args(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--n-gaussians",
        type=int,
        default=2,
        help="number of gaussians to sum",
    )
    parser.add_argument(
        "--n-samples",
        type=int,
        default=365,
        help="number of data points to simulate",
    )
    parser.add_argument(
        "--snr",
        type=int,
        default=20,
        help="signal to noise ratio",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("simulated_signal.h5"),
        help="output file to write the simulated data to",
    )


def get_args() -> Namespace:
    parser = ArgumentParser(
        "Simulate LISA-like signals",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    add_simulator_args(parser)
    return parser.parse_args()


def cmd_simulate_signal(args: Namespace):
    sim = Simulator()
    signal = sim.simulate_gaussians(args.n_gaussians, args.n_samples, args.snr)
    signal.write_dataset(args.output_path)
    signal.plot(args.output_path.with_suffix(".png"))


def main():
    args = get_args()
    cmd_simulate_signal(args)


if __name__ == "__main__":
    sys.exit(main())
