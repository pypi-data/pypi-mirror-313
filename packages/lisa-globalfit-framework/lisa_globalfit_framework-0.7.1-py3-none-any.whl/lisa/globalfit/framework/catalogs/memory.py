import json
from dataclasses import dataclass
from pathlib import Path

from lisa.globalfit.framework.catalog import SourceCatalog
from lisa.globalfit.framework.io import CustomJSONEncoder
from lisa.globalfit.framework.model import ParametricModel
from lisa.globalfit.framework.msg.data import ModuleState
from lisa.globalfit.framework.msg.subjects import Subject


@dataclass
class InMemorySourceCatalog(SourceCatalog):
    def __init__(
        self, detection_map: dict[Subject, ParametricModel] | None = None
    ) -> None:
        super().__init__()
        self.detection_map = detection_map or {}

    async def get_source_parameters(self) -> dict[Subject, ParametricModel]:
        return self.detection_map

    async def update(self, module: Subject, state: ModuleState) -> None:
        # TODO Should the detection catalog be updated if the best sample from the
        # chain in the current iteration has a lower posterior probability than the
        # best sample from all previous iterations ?
        # The posterior should probably be passed along the waveform parameters, so
        # that its evolution can be monitored during execution.
        self.detection_map[module] = state.chain.waveforms

    async def write(self, filename: Path) -> None:
        filename.write_text(json.dumps(self, cls=CustomJSONEncoder))
