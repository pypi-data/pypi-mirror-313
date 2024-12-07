from abc import ABC, abstractmethod
from pathlib import Path

from lisa.globalfit.framework.model import ParametricModel
from lisa.globalfit.framework.msg.data import ModuleState
from lisa.globalfit.framework.msg.subjects import Subject


class SourceCatalog(ABC):
    """Gravitational wave detection catalog."""

    def __init__(self) -> None:
        pass

    @abstractmethod
    async def update(self, module: Subject, state: ModuleState) -> None:
        pass

    @abstractmethod
    async def get_source_parameters(self) -> dict[Subject, ParametricModel]:
        pass

    @abstractmethod
    async def write(self, filename: Path) -> None:
        pass
