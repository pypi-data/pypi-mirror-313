from dataclasses import dataclass
from typing import Self

from lisa.globalfit.framework.model import MarkovChainSamples, ParametricModel
from lisa.globalfit.framework.msg.base import MessageBase


@dataclass
class DataMessage(MessageBase):
    """Message for passing metadata between modules."""


@dataclass
class ModuleState(DataMessage):
    """Comprehensive state of a module.

    This state can be used as module checkpoint, from which MCMC sampling can be
    resumed.

    :param chain: Samples leading to current state.
    """

    chain: MarkovChainSamples
    log_prior: ParametricModel
    log_likelihood: ParametricModel
    log_proposal: ParametricModel
    checkpoint_key: str | None = None

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        return cls(
            chain=MarkovChainSamples.from_dict(obj["chain"]),
            log_prior=ParametricModel.from_dict(obj["log_prior"]),
            log_likelihood=ParametricModel.from_dict(obj["log_likelihood"]),
            log_proposal=ParametricModel.from_dict(obj["log_proposal"]),
            checkpoint_key=obj["checkpoint_key"],
        )


@dataclass
class ErrorMessage(DataMessage):
    """Message for reporting errors."""

    pass
