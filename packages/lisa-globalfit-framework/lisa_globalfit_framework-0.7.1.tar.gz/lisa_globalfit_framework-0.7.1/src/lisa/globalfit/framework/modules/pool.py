import json
import logging
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from lisa.globalfit.framework.io import CustomJSONEncoder
from lisa.globalfit.framework.model import ModuleExecutionState
from lisa.globalfit.framework.msg.control import ExecutionStateUpdate
from lisa.globalfit.framework.msg.data import ModuleState
from lisa.globalfit.framework.msg.subjects import Subject, create_channel_name

logger = logging.getLogger(__name__)


@dataclass
class ModulePoolEntry:
    group: str
    label: str
    execution_state: ModuleExecutionState
    state: ModuleState
    current_iteration: int = -1

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        return cls(
            group=obj["group"],
            label=obj["label"],
            execution_state=ModuleExecutionState(obj["execution_state"]),
            state=ModuleState.from_dict(obj["state"]),
            current_iteration=obj["current_iteration"],
        )


@dataclass
class ModulePool:
    workers: dict[Subject, ModulePoolEntry]

    def select_modules(
        self,
        checker: Callable[[ModulePoolEntry], bool],
    ) -> list[Subject]:
        return [subject for subject, entry in self.workers.items() if checker(entry)]

    async def update_module_state(
        self,
        module: Subject,
        update: ExecutionStateUpdate,
    ) -> None:
        # TODO Add sanity checks and log messages.
        if module not in self.workers:
            logger.error(f"trying to update status of module {module} not in pool")
            return

        entry = self.workers[module]
        logger.debug(f"module {module}: {entry.execution_state} -> {update.new_state}")

        entry.execution_state = update.new_state
        entry.current_iteration = update.current_iteration

    def write_checkpoint(self, file: Path) -> None:
        with open(file, "w") as f:
            json.dump(self, f, cls=CustomJSONEncoder)
        logger.info(f"wrote module pool checkpoint {file}")

    def __len__(self):
        return len(self.workers)

    @classmethod
    def from_json(cls, file: Path) -> Self:
        return cls(
            workers={
                subject: ModulePoolEntry.from_dict(module)
                for subject, module in json.loads(file.read_text())["workers"].items()
            }
        )

    @classmethod
    def from_group_configuration(cls, file: Path, *channel_args: str) -> Self:
        return cls(
            workers={
                create_channel_name(
                    *channel_args,
                    module["group_label"],
                    module["module_label"],
                ): ModulePoolEntry(
                    label=module["module_label"],
                    group=module["group_label"],
                    execution_state=ModuleExecutionState.CREATED,
                    state=ModuleState.from_dict(module["initial_state"]),
                )
                for module in json.loads(file.read_text())
            },
        )

    async def update_global_state(self, module: Subject, state: ModuleState) -> None:
        if module not in self.workers:
            logger.error(f"trying to update state of module {module} not in pool")
            return

        if not state.checkpoint_key:
            logger.warning(f"missing checkpoint key for module {module}")

        logger.debug(f"updating global state with results from {module}")
        self.workers[module].state = state
