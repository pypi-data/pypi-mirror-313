import logging
from dataclasses import dataclass
from typing import ClassVar

from lisa.globalfit.framework.modules.module import ModuleBase

logger = logging.getLogger(__name__)


@dataclass
class ModuleRegistry:
    items: ClassVar[dict[str, type[ModuleBase]]] = {}

    @classmethod
    def choices(cls) -> list[str]:
        return list(cls.items)

    @classmethod
    def register(cls, name: str):
        def decorator(module_class: type[ModuleBase]):
            cls.items[name] = module_class
            return module_class

        return decorator

    @classmethod
    def create(cls, name: str, *args, **kwargs) -> ModuleBase:
        try:
            kls = cls.items[name]
            return kls(*args, **kwargs)
        except KeyError:
            logger.error(f"unknown module identifier: {name}")
            raise
