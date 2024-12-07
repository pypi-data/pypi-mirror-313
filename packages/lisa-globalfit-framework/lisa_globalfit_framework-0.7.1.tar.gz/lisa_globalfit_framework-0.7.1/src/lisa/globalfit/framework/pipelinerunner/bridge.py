import asyncio
import logging
import sys
from argparse import ArgumentParser, Namespace

from lisa.globalfit.framework.args import add_bus_args, add_common_args
from lisa.globalfit.framework.buses import DefaultPullEventBus
from lisa.globalfit.framework.pipelinerunner.workflow import (
    WorkflowSpec,
)

logger = logging.getLogger(__name__)

INBOX = "infra.pipelinerunner.submit"


def get_args() -> Namespace:
    parser = ArgumentParser()

    add_common_args(parser)
    add_bus_args(parser)

    parser.add_argument(
        "workflow",
        type=str,
    )

    parser.add_argument(
        "--labels",
        type=str,
        nargs="+",
    )

    parser.add_argument(
        "--parameters",
        "-p",
        action="extend",
        nargs="+",
        default=[],
    )

    return parser.parse_args()


async def main_async():
    args = get_args()
    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s %(message)s",
        datefmt=r"%Y-%m-%dT%H:%M:%S",
    )

    if args.workdir is None:
        logger.error("missing --workdir argument")
        sys.exit(1)

    params = dict(param.split("=") for param in args.parameters)
    bus = DefaultPullEventBus(servers=args.servers)
    spec = WorkflowSpec(
        resource=args.workflow,
        labels=args.labels if args.labels is not None else [],
        parameters={"workdir": args.workdir, **params},
    )
    await bus.connect()
    await bus.publish(INBOX, spec.encode())
    logger.info(f"submitted workflow {spec}")


def main():
    return asyncio.run(main_async())


if __name__ == "__main__":
    main()
