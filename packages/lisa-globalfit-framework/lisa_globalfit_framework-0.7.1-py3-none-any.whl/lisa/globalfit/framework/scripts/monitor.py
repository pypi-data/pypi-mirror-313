import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from asyncio import run

from lisa.globalfit.framework.monitoring.server import MonitoringServer


def add_execution_monitoring_args(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--port",
        type=int,
        help="server port",
        default=8080,
    )
    parser.add_argument(
        "--api-url",
        type=str,
        help="URL of the backend service",
        default="http://localhost:8080",
    )
    parser.add_argument(
        "--s3-bucket",
        type=str,
        help="name of S3 bucket storing module checkpoints",
        required=True,
    )


def get_args() -> Namespace:
    parser = ArgumentParser(
        "LISA GlobalFit Framework monitoring CLI",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    add_execution_monitoring_args(parser)
    return parser.parse_args()


async def cmd_monitor(args: Namespace):
    server = MonitoringServer(args.api_url, args.s3_bucket)
    await server.run(args.port)


def main():
    args = get_args()
    run(cmd_monitor(args))


if __name__ == "__main__":
    sys.exit(main())
