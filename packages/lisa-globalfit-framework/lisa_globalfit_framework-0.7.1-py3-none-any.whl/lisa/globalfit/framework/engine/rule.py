import logging
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Self

from lisa.globalfit.framework.msg.base import MessageBase
from lisa.globalfit.framework.msg.subjects import Subject

logger = logging.getLogger(__name__)


@dataclass
class Response:
    subject: Subject
    msg: MessageBase


RuleIdentifier = str


@dataclass
class Rule(ABC):
    id: RuleIdentifier
    # TODO [xs] Active status should remain internal to engine state.
    is_active: bool
    subject: str

    @abstractmethod
    def evaluate(self, subject: str, msg: bytes) -> list[Response]:
        pass

    @classmethod
    def from_file(cls, file: Path, variable_name: str = "__rule__") -> Self:
        # TODO Add random salt to imported module names to prevent collisions
        spec = spec_from_file_location(file.with_suffix("").name, file)
        if spec is None or spec.loader is None:
            raise ImportError(f"could not load rule from {file}")

        module = module_from_spec(spec)
        sys.modules[module.__name__] = module
        # This is potentially very dangerous, as it allows abitrary code execution when
        # loading rules.
        # Strict access control mechanisms need to be enforced for rule directories.
        spec.loader.exec_module(module)
        attr = getattr(module, variable_name, None)
        if attr is None:
            raise ImportError(f"could not find {variable_name!r} attribute in {file}")

        if not isinstance(attr, cls):
            raise TypeError(
                f"expected {cls.__name__} but got {attr.__class__.__name__}"
            )

        return attr
