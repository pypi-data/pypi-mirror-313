import json
import logging
from dataclasses import dataclass
from pathlib import Path

from lisa.globalfit.framework.io import CustomJSONEncoder
from lisa.globalfit.framework.msg.data import ModuleState

logger = logging.getLogger(__name__)


@dataclass
class ModuleConfiguration:
    group_label: str
    module_label: str
    initial_state: ModuleState
    static_configuration_reference: str


@dataclass
class PreprocessorOutput:
    modules: list[ModuleConfiguration]

    def write_json(self, output_file: Path) -> None:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.modules, f, cls=CustomJSONEncoder)
        logger.info(f"wrote group configuration to {output_file}")
