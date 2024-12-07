import asyncio
import logging
from argparse import ArgumentParser, Namespace
from asyncio import Event, Task
from pathlib import Path
from signal import SIGINT, SIGTERM

from lisa.globalfit.framework.args import add_bus_args, add_logging_args
from lisa.globalfit.framework.bus import PullEventBus
from lisa.globalfit.framework.buses import DefaultPullEventBus
from lisa.globalfit.framework.exceptions import DeserializationError
from lisa.globalfit.framework.msg.streams import STREAM_INFRA
from lisa.globalfit.framework.pipelinerunner.workflow import (
    WorkflowResult,
    WorkflowSpec,
)

logger = logging.getLogger(__name__)

SUBJECT_SUBMIT = "infra.pipelinerunner.submit"
SUBJECT_RESULT = "infra.pipelinerunner.result"
SUBJECT_NOTIFICATION = "infra.pipelinerunner.notification"


class WorkflowSubmitter:
    CONSUMER_NAME = "workflow-submitter"

    def __init__(self, bus: PullEventBus) -> None:
        self.bus = bus
        self.should_stop = Event()

    async def setup(self) -> None:
        # TODO Handle bus disconnects after setup.
        await self.bus.connect()
        await self.bus.add_stream(STREAM_INFRA)

    async def run(self):
        logger.info("starting workflow submitter")
        tasks = (
            Task(self.handle_msg_submit()),
            Task(self.handle_msg_result()),
        )
        await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

    async def handle_msg_submit(self) -> None:
        sub = await self.bus.subscribe(SUBJECT_SUBMIT, f"{self.CONSUMER_NAME}-sumbit")
        while not self.should_stop.is_set():
            msg = await sub.fetch_message()
            await msg.in_progress()
            try:
                spec = WorkflowSpec.decode(msg.data)
                await self.submit_workflow(spec)
                await msg.ack()
            except DeserializationError as err:
                logger.error(f"got invalid workflow submission: {err}")
                await msg.discard()
        await sub.unsubscribe()

    async def handle_msg_result(self) -> None:
        sub = await self.bus.subscribe(
            SUBJECT_NOTIFICATION, f"{self.CONSUMER_NAME}-result"
        )
        while not self.should_stop.is_set():
            msg = await sub.fetch_message()
            await msg.in_progress()
            name, status, duration = msg.data.decode().split()
            logger.info(
                f"workflow {name} ended with status {status} ({float(duration):.1f}s)"
            )
            # TODO Retrieve more complete workflow info, including labels
            result = WorkflowResult(name, status, [])
            await self.bus.publish(SUBJECT_RESULT, result.encode())
            await msg.ack()
        await sub.unsubscribe()

    async def submit_workflow(self, spec: WorkflowSpec) -> None:
        # TODO Properly handle exceptions.
        logger.info(f"submitting workflow {spec}")
        args: tuple[str, ...] = ("submit", "--output", "name")

        # Handle both local files and Workflow Templates.
        if Path(spec.resource).is_file():
            args += (spec.resource,)
        else:
            args += ("--from", f"WorkflowTemplate/{spec.resource}")

        if spec.parameters:
            for k, v in spec.parameters.items():
                args += ("-p", f"{k!s}={v!s}")

        proc = await asyncio.create_subprocess_exec(
            "argo",
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        if proc.returncode == 127:
            raise ValueError("command 'argo' not found")

        stdout, stderr = await proc.communicate()
        workflow_name = stdout.decode().strip()
        if not workflow_name:
            err = stderr.decode().strip()
            raise ValueError(f"could not submit workflow: {err}")

        logger.info(f"submitted workflow {workflow_name}")

    async def shutdown(self) -> None:
        logger.info("shutting down DAG submitter")
        await self.bus.close()


def get_args() -> Namespace:
    parser = ArgumentParser()

    add_logging_args(parser)
    add_bus_args(parser)

    return parser.parse_args()


async def run_submitter(args: Namespace) -> None:
    bus = DefaultPullEventBus(servers=args.servers)
    submitter = WorkflowSubmitter(bus)
    try:
        await submitter.setup()
        await submitter.run()
    except asyncio.CancelledError:
        await submitter.shutdown()


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
    task = asyncio.ensure_future(run_submitter(args))

    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, task.cancel)

    loop.run_until_complete(task)


if __name__ == "__main__":
    main()
