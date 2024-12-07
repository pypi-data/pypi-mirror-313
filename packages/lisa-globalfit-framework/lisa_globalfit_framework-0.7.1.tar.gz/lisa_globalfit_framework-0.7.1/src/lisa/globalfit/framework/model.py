from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Self

import numpy as np
import numpy.typing as npt


@dataclass
class ParametricModel:
    """Well-known parametric model.

    :param name: Identifier of the model.
    :param parameters: Parameters of the model.
    """

    name: str
    parameters: npt.NDArray

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        return cls(name=obj["name"], parameters=np.array(obj["parameters"]))

    def __eq__(self, other) -> bool:
        """Check whether two models are equivalent.

        Use with caution!

        This is more of a helper for unit tests than a real feature, since it performs
        equality checks on floating point arrays.

        """
        if not isinstance(other, ParametricModel):
            return False
        if self.name != other.name:
            return False
        return np.array_equal(self.parameters, other.parameters)


@dataclass
class MarkovChainSamples:
    """Sequence of Markov chain samples.

    :param idx_iteration: Current Global Fit iteration.
    :param: idx_step_end: Step of the last element in waveforms parameters.
    :param waveforms: Model of the waveform. Its name represents the function identifier
        of the associated waveform generator. Its parameters represent the samples and
        have a shape of n_steps * n_walkers * n_dim. Its size is estimated to be of the
        following order of magnitude.

             1000 (steps) * 20 (parameters) * 5 (walkers) * 4 (f32) ~ 400kB.
    """

    idx_iteration: int
    idx_step_end: int
    waveforms: ParametricModel

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        return cls(
            idx_iteration=obj["idx_iteration"],
            idx_step_end=obj["idx_step_end"],
            waveforms=ParametricModel.from_dict(obj["waveforms"]),
        )


class ModuleExecutionState(IntEnum):
    # TODO Use state machine if we need to handle complex transitions.
    CREATED = auto()
    CONFIGURING = auto()
    IDLE = auto()
    RUNNING = auto()
    ERROR = auto()
    DONE = auto()
