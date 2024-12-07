from __future__ import annotations

import logging
from abc import abstractmethod
from collections.abc import Callable
from os import getenv
from pathlib import Path

from aiobotocore.session import get_session
from botocore.exceptions import ClientError

from lisa.globalfit.framework import __version__
from lisa.globalfit.framework.bus import EventBus
from lisa.globalfit.framework.exceptions import DeserializationError, FrameworkError
from lisa.globalfit.framework.model import ModuleExecutionState
from lisa.globalfit.framework.msg.base import MessageBase
from lisa.globalfit.framework.msg.control import (
    ConfigureModule,
    ExecutionStateUpdate,
    IterateModule,
    TerminateModule,
)
from lisa.globalfit.framework.msg.data import ModuleState
from lisa.globalfit.framework.msg.subjects import (
    Subject,
    channel_data_state,
    channel_get_group,
    channel_get_module,
    channel_get_pipeline,
    channel_status,
    channel_terminate,
)

logger = logging.getLogger(__name__)


class ModuleBase:
    """Abstract Global Fit module."""

    DEFAULT_POLL_INTERVAL_S = 1
    DEFAULT_S3_BUCKET_VAR = "S3_BUCKET"
    DEFAULT_S3_PREFIX = "lisa-checkpoint"

    def __init__(
        self, datafile: Path, output_checkpoint: Path, channel_name: str, bus: EventBus
    ) -> None:
        """Create base module.

        :param datafile: Input data file containing signal.
        :param output_checkpoint: Path to a save state, from which execution can be
            resumed after nominal termination or a crash.
        :param channel_name: Topic prefix to use when talking on the bus.
        :param bus: Event bus interface.
        """
        self.datafile = datafile
        self.output_checkpoint = output_checkpoint
        self.channel_name = channel_name
        self.bus = bus
        self.execution_state = ModuleExecutionState.CREATED
        self.current_iteration = -1
        self.current_step = -1

        # When we will have dynamic reallocation of modules (#5), the container
        # orchestrator (Argo) will be able to upload checkpoints to S3 automatically
        # at each iteration.
        # However, for now modules live for the entire duration of the global fit run,
        # so they need to manually push their checkpoints to S3.
        # This is done using environment variables because it's a temporary workaround
        # which is not meant to appear in the public API.
        self._s3_bucket = getenv(self.DEFAULT_S3_BUCKET_VAR)
        if self._s3_bucket is None:
            logger.info(
                f"env variable {self.DEFAULT_S3_BUCKET_VAR} is not set, "
                "checkpoints will not be uploaded to S3"
            )

    async def setup(self) -> None:
        await self.bus.connect()
        await self.set_safe_callback(
            channel_terminate(self.channel_name),
            TerminateModule,
            self._terminate,
        )

    async def set_safe_callback(
        self, subject: Subject, msg_type: type[MessageBase], fn: Callable
    ) -> None:
        async def handler(subject: Subject, msg: bytes) -> None:
            # Make sure message can be decoded.
            try:
                decoded_msg = msg_type.decode(msg)
            except DeserializationError as err:
                # Discard unknown messages.
                logger.error(f"could not read message on {subject}: {err}")
                return

            logger.debug(f"{self.channel_name} received {type(decoded_msg).__name__}")

            # Run callback using decoded message.
            await fn(decoded_msg)

        await self.bus.subscribe(subject, handler)

    async def publish_results(self, results: ModuleState) -> None:
        await self.bus.publish(channel_data_state(self.channel_name), results.encode())

    async def update_status(self, status: ModuleExecutionState) -> None:
        self.execution_state = status
        await self.bus.publish(
            channel_status(self.channel_name),
            ExecutionStateUpdate(
                current_iteration=self.current_iteration, new_state=status
            ).encode(),
        )

    async def run(
        self, initial_state: ConfigureModule, iteration_config: IterateModule
    ):
        await self._configure(initial_state)
        await self._iterate(iteration_config)

    async def _configure(self, msg: ConfigureModule) -> None:
        if self.execution_state != ModuleExecutionState.CREATED:
            logger.warning(
                f"{self.channel_name} got {msg} but status is {self.execution_state}"
            )

        await self.update_status(ModuleExecutionState.CONFIGURING)
        await self.configure(msg)
        await self.update_status(ModuleExecutionState.IDLE)

    async def _iterate(self, msg: IterateModule) -> None:
        if self.execution_state != ModuleExecutionState.IDLE:
            logger.warning(
                f"{self.channel_name} got {msg} but status is {self.execution_state}"
            )

        self.current_iteration = msg.idx_iteration
        await self.update_status(ModuleExecutionState.RUNNING)
        try:
            state = await self.iterate(msg)
            # FIXME We need to get the current step count as an input argument, because
            # we don't know how many have been done in the past.
            self.current_step = msg.step_count
            state.checkpoint_key = self._derive_checkpoint_key()
            await self.publish_results(state)
            await self._publish_checkpoint(state.checkpoint_key)
            await self.update_status(ModuleExecutionState.IDLE)
        except FrameworkError as err:
            logger.error(f"{self.channel_name}: {err}")
            await self.update_status(ModuleExecutionState.ERROR)

    async def _terminate(self, msg: TerminateModule) -> None:
        logger.debug(f"stopping {self.channel_name}")
        self.execution_state = ModuleExecutionState.DONE

    def _derive_checkpoint_key(self, prefix=DEFAULT_S3_PREFIX) -> str:
        return "-".join((prefix, self.channel_name))

    async def _publish_checkpoint(self, object_name: str) -> None:
        if self._s3_bucket is not None:
            metadata = {
                "gf-version": __version__,
                "gf-pipeline-run": channel_get_pipeline(self.channel_name),
                "gf-group": channel_get_group(self.channel_name),
                "gf-module": channel_get_module(self.channel_name),
                "gf-iteration": str(self.current_iteration),
            }
            async with get_session().create_client("s3") as s3:
                try:
                    # TODO Use aiofiles to get rid of ASYNC230.
                    with open(self.output_checkpoint, "rb") as f:  #  noqa: ASYNC230
                        res = await s3.put_object(
                            Bucket=self._s3_bucket,
                            Key=object_name,
                            Body=f,
                            Metadata=metadata,
                        )
                    logger.debug(f"uploaded checkpoint: {res}")
                # FIXME This might not be the correct exception type for aiobotocore.
                except ClientError as err:
                    logger.warning(f"could not upload checkpoint: {err}")
        else:
            logger.debug("skipping checkpoint upload")

    @abstractmethod
    async def configure(self, msg: ConfigureModule) -> None:
        pass

    @abstractmethod
    async def iterate(self, msg: IterateModule) -> ModuleState:
        pass
