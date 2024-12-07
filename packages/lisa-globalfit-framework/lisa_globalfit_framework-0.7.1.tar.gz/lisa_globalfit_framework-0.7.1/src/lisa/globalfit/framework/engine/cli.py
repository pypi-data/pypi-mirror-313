import asyncio
import logging
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from asyncio.exceptions import CancelledError
from pathlib import Path
from signal import SIGINT, SIGTERM

from lisa.globalfit.framework.args import add_bus_args, add_common_args
from lisa.globalfit.framework.buses import DefaultPullEventBus
from lisa.globalfit.framework.engine.engine import Engine
from lisa.globalfit.framework.engine.rule import Rule

logger = logging.getLogger(__name__)


def get_args() -> Namespace:
    parser = ArgumentParser(
        "LISA GlobalFit Framework Engine CLI",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    add_common_args(parser)
    add_bus_args(parser)

    rule_selection_group = parser.add_mutually_exclusive_group(required=True)
    rule_selection_group.add_argument(
        "--rules-directory",
        "-d",
        help="Directory containing rules",
        type=Path,
    )
    rule_selection_group.add_argument(
        "--rule",
        "-f",
        help="File containing individual rule, can be passed multiple times",
        type=Path,
        nargs="+",
    )

    return parser.parse_args()


async def run_engine(args: Namespace):
    if args.rules_directory:
        files = Path(args.rules_directory).rglob("*.py")
    else:
        files = args.rule

    rules = [Rule.from_file(f) for f in files]
    engine = Engine(
        bus=DefaultPullEventBus(args.servers),
    )
    try:
        await engine.setup()
        await engine.register_rules(rules)
        await engine.run()
    except CancelledError:
        pass
    finally:
        await engine.shutdown()


def main():
    args = get_args()
    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s %(message)s",
        datefmt=r"%Y-%m-%dT%H:%M:%S",
    )

    loop = asyncio.get_event_loop()
    if logging.root.level == logging.DEBUG:
        loop.set_debug(True)
    task = asyncio.ensure_future(run_engine(args))

    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, task.cancel)

    loop.run_until_complete(task)


if __name__ == "__main__":
    main()
