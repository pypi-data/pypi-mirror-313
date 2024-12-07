import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from lisa.globalfit.framework.model import MarkovChainSamples, ParametricModel
from lisa.globalfit.framework.modules.pool import ModulePool
from lisa.globalfit.framework.msg.data import ModuleState
from lisa.globalfit.framework.preprocessing import (
    ModuleConfiguration,
    PreprocessorOutput,
)
from lisa.globalfit.framework.signal import NoisyGaussianMixture

logger = logging.getLogger(__name__)

DUMMY_CONFIG_FILENAME = "dummy_config.json"


@dataclass
class StubPreprocessor:
    group_label: str

    def preprocess(
        self, dataset: Path, checkpoint: ModulePool | None = None
    ) -> PreprocessorOutput:
        logger.debug(f"pre-processing dataset {dataset}")

        if checkpoint is not None:
            return self.preprocess_from_checkpoint(checkpoint)

        # Read input data.
        data = NoisyGaussianMixture.read_dataset(dataset)

        # Create module configurations, based on true values found in the catalog.
        return PreprocessorOutput(
            modules=[
                ModuleConfiguration(
                    group_label=self.group_label,
                    module_label=f"{data.means[i]:.0f}",
                    initial_state=ModuleState(
                        chain=MarkovChainSamples(
                            idx_iteration=0,
                            idx_step_end=0,
                            waveforms=ParametricModel(
                                name="norm",
                                # Cheat using the actual "catalog" value as initial
                                # state.
                                parameters=np.array(
                                    [[data.means[i], data.variances[i]]]
                                ),
                            ),
                        ),
                        # For now, we cheat by using the actual "catalog" values as
                        # prior.
                        log_prior=ParametricModel(
                            name="multivariate_normal",
                            # Only specify prior mean, use default covariance matrix.
                            parameters=np.array([data.means[i], data.variances[i]]),
                        ),
                        log_likelihood=ParametricModel("gaussian1d", np.array([])),
                        # TODO Use actual proposal distribution.
                        log_proposal=ParametricModel(
                            name="unused", parameters=np.array([])
                        ),
                    ),
                    static_configuration_reference=DUMMY_CONFIG_FILENAME,
                )
                for i in range(data.n_distributions())
            ]
        )

    def preprocess_from_checkpoint(self, checkpoint: ModulePool) -> PreprocessorOutput:
        group_workers = [
            entry
            for entry in checkpoint.workers.values()
            if entry.group == self.group_label
        ]
        logger.debug(
            f"got checkpoint with {len(group_workers)} {self.group_label} entries"
        )
        logger.info(group_workers)
        return PreprocessorOutput(
            modules=[
                # FIXME Propagate static configuration reference.
                ModuleConfiguration(
                    entry.group, entry.label, entry.state, DUMMY_CONFIG_FILENAME
                )
                for entry in group_workers
            ]
        )

    def write_group_configuration(
        self, config: PreprocessorOutput, output: Path
    ) -> None:
        config.write_json(output)
