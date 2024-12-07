from dataclasses import dataclass
from pathlib import Path

from lisa.globalfit.framework.catalog import SourceCatalog
from lisa.globalfit.framework.model import ModuleExecutionState
from lisa.globalfit.framework.msg.base import MessageBase
from lisa.globalfit.framework.msg.data import ModuleState


@dataclass
class ControlMessage(MessageBase):
    """Message for controlling Global Fit flow."""

    pass


@dataclass
class ConfigureModule(ControlMessage):
    """Configure an initialized module."""

    state: ModuleState
    configuration_file: Path | None = None


@dataclass
class IterateModule(ControlMessage):
    """Iterate a module for a given number of steps.

    :param idx_iteration: Current iteration counter.
    :param detections: Live catalog.
    :param step_count: Number of steps to execute in iteration.
    """

    idx_iteration: int
    detections: SourceCatalog
    step_count: int


@dataclass
class ContinueModule(ControlMessage):
    """Finish the current step and wait for next iteration order."""

    pass


@dataclass
class TerminateModule(ControlMessage):
    """Finish the current step and exit."""

    pass


@dataclass
class KillModule(ControlMessage):
    """Exit immediately."""

    pass


@dataclass
class ExecutionStateUpdate(ControlMessage):
    """Transition of execution state."""

    current_iteration: int
    new_state: ModuleExecutionState


@dataclass
class ModuleGroupConfiguration(ControlMessage):
    """Configuration of a module group."""

    group: str
    labels: tuple[str, ...]
