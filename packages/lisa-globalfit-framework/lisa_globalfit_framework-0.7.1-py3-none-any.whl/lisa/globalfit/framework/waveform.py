import logging
from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class Waveform:
    """Abstract base class representing a waveform."""

    @abstractmethod
    def evaluate(self, x: np.ndarray, *args: float) -> np.ndarray:
        """Evaluate the waveform at given points.

        :param x: Array of points at which to evaluate the waveform.
        :return: Array containing the values of the waveform at the given points.
        """


@dataclass
class WaveformRegistry:
    items: ClassVar[dict[str, type[Waveform]]] = {}

    @classmethod
    def choices(cls) -> list[str]:
        return list(cls.items)

    @classmethod
    def register(cls, name: str):
        def decorator(waveform_class: type[Waveform]):
            cls.items[name] = waveform_class
            return waveform_class

        return decorator

    @classmethod
    def create(cls, name: str, *args, **kwargs) -> Waveform:
        try:
            kls = cls.items[name]
            return kls(*args, **kwargs)
        except KeyError:
            logger.error(f"unknown waveform identifier: {name}")
            raise


@dataclass
@WaveformRegistry.register("gaussian1d")
class Gaussian1D(Waveform):
    def evaluate(self, x: np.ndarray, *args: float) -> np.ndarray:
        mean, variance = args
        return np.exp(-0.5 * ((x - mean) / variance) ** 2)
