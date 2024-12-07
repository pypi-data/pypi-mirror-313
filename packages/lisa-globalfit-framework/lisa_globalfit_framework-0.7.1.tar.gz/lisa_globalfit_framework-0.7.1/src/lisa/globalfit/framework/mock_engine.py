import asyncio
import json
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path

from lisa.globalfit.framework.bus import EventBus
from lisa.globalfit.framework.catalog import SourceCatalog
from lisa.globalfit.framework.exceptions import DeserializationError, FrameworkError
from lisa.globalfit.framework.io import CustomJSONEncoder
from lisa.globalfit.framework.modules.module import ModuleExecutionState
from lisa.globalfit.framework.modules.pool import ModulePool, ModulePoolEntry
from lisa.globalfit.framework.msg.base import MessageBase
from lisa.globalfit.framework.msg.control import (
    ExecutionStateUpdate,
    ModuleGroupConfiguration,
    TerminateModule,
)
from lisa.globalfit.framework.msg.data import ModuleState
from lisa.globalfit.framework.msg.subjects import (
    Subject,
    channel_any_group_any_module,
    channel_configure,
    channel_data_state,
    channel_status,
    channel_strip,
    channel_terminate,
    create_channel_name,
)

logger = logging.getLogger(__name__)


@dataclass
class IterationDecision:
    continue_iterating: bool


class Engine:
    DEFAULT_EVENTLOOP_SLEEP_S = 1

    def __init__(
        self,
        expected_groups: list[str],
        bus: EventBus,
        catalog: SourceCatalog,
        output: Path,
        pipeline_run_id: str,
        max_iterations: int,
    ) -> None:
        self.pipeline_run_id = pipeline_run_id
        self.expected_groups = set(expected_groups)
        self.actual_groups: set[str] = set()
        self.bus = bus
        self.catalog = catalog
        self.output = output
        self.max_iterations = max_iterations
        self.pool = ModulePool(workers={})

    async def setup(self) -> None:
        await self.bus.connect()
        # Subscribe to preprocessors updates.
        await self.set_safe_callback(
            subject=create_channel_name(
                self.pipeline_run_id, channel_configure("engine")
            ),
            msg_type=ModuleGroupConfiguration,
            fn=self.handle_group_configuration,
        )
        # Subscribe to all module updates.
        await self.set_safe_callback(
            subject=channel_any_group_any_module(self.pipeline_run_id, channel_status),
            msg_type=ExecutionStateUpdate,
            fn=self.pool.update_module_state,
        )
        await self.set_safe_callback(
            subject=channel_any_group_any_module(
                self.pipeline_run_id, channel_data_state
            ),
            msg_type=ModuleState,
            fn=self.handle_module_data,
        )

    async def shutdown(self) -> None:
        await self.bus.close()

    async def run(
        self,
        current_iteration: int,
    ) -> IterationDecision:
        if not self.expected_groups:
            raise FrameworkError("engine needs to expect at least one group")

        logger.info("starting engine")
        try:
            logger.info(
                f"running iteration {current_iteration}/{self.max_iterations-1}"
            )
            await self.wait_for_groups_configurations()
            await self.wait_for_modules_iteration(current_iteration)
        except FrameworkError:
            logger.error("shutting down engine")
            raise
        finally:
            await self.catalog.write(self.output.parent / "catalog.json")
            await self.shutdown_pool()
            await self.shutdown()
            return IterationDecision(
                continue_iterating=current_iteration < self.max_iterations - 1
            )

    async def write_iteration_decision(
        self, decision: IterationDecision, filename: Path
    ) -> None:
        with open(filename, "w") as f:  #  noqa: ASYNC230
            json.dump(decision, f, cls=CustomJSONEncoder)
        logger.info(f"wrote iteration decision to {filename}")

    async def wait_for_groups_configurations(
        self, check_interval: int = DEFAULT_EVENTLOOP_SLEEP_S
    ):
        while self.expected_groups != self.actual_groups:
            diff = self.expected_groups - self.actual_groups
            logger.info(f"waiting for {len(diff)} configurations: {diff}")
            await asyncio.sleep(check_interval)

    async def handle_group_configuration(
        self, subject: Subject, msg: ModuleGroupConfiguration
    ) -> None:
        # Perform base sanity checks.
        if msg.group not in self.expected_groups:
            logger.warning(f"got unexpected configuration for group {msg.group}")
            return
        if msg.group in self.actual_groups:
            logger.warning(f"got duplicate configuration for group {msg.group}")
            return

        new_entries = {
            create_channel_name(
                self.pipeline_run_id, msg.group, label
            ): ModulePoolEntry(
                group=msg.group,
                label=label,
                execution_state=ModuleExecutionState.CREATED,
                # TODO Should state be optional ?
                state=None,  # type: ignore
            )
            for label in msg.labels
        }
        self.pool.workers |= new_entries
        self.actual_groups.add(msg.group)
        logger.info(
            f"got configuration of {len(new_entries)} modules for group {msg.group}"
        )

    async def wait_for_modules_iteration(
        self,
        iteration_number: int,
        check_interval: int = DEFAULT_EVENTLOOP_SLEEP_S,
    ):
        while remaining := self.pool.select_modules(
            lambda module: not (
                module.execution_state == ModuleExecutionState.IDLE
                and module.current_iteration == iteration_number
                and module.state is not None
            )
        ):
            progress = f"{len(self.pool) - len(remaining)}/{len(self.pool)}"
            logger.info(f"{progress} modules iterated")
            logger.debug(f"current module pool state: {self.pool.workers}")
            await asyncio.sleep(check_interval)

        self.pool.write_checkpoint(self.output)
        logger.info("all modules finished iteration")

    async def shutdown_pool(self) -> None:
        await self.send_group(self.send_terminate, list(self.pool.workers))

    async def send_group(
        self, fn: Callable[[Subject], Awaitable[None]], subjects: list[Subject]
    ) -> None:
        await asyncio.gather(*(fn(s) for s in subjects))

    async def send_terminate(self, subject: Subject) -> None:
        logger.debug(f"sending terminate message to {subject}")
        msg = TerminateModule()
        await self.bus.publish(channel_terminate(subject), msg.encode())

    async def set_safe_callback(
        self, subject: Subject, msg_type: type[MessageBase], fn: Callable
    ) -> None:
        async def handler(subject: Subject, msg: bytes):
            try:
                decoded_msg = msg_type.decode(msg)
            except DeserializationError as err:
                # Discard unknown messages.
                logger.error(f"could not read message from {subject}: {err}")
                return

            module = channel_strip(subject)
            await fn(module, decoded_msg)

        await self.bus.subscribe(subject, handler)

    async def handle_module_data(self, subject: Subject, state: ModuleState):
        await self.catalog.update(subject, state)
        await self.pool.update_global_state(subject, state)
