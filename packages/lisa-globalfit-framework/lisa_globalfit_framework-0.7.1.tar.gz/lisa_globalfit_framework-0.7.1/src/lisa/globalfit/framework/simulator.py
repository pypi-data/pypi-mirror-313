import logging

import numpy as np

from lisa.globalfit.framework.signal import NoisyGaussianMixture
from lisa.globalfit.framework.waveform import Gaussian1D

logger = logging.getLogger(__name__)


class Simulator:
    def __init__(self) -> None:
        self.rng = np.random.default_rng(seed=42)

    def simulate_gaussians(
        self,
        n_distributions: int,
        n_samples: int,
        snr: int,
    ) -> NoisyGaussianMixture:
        logger.info(f"simulating {n_distributions} gaussians with snr {snr}")

        # Generate time points.
        time_points = np.arange(n_samples)

        # Initialize the sum of Gaussian-shaped time series.
        sum_of_gaussians = np.zeros(n_samples)

        # Draw random mean values between start and end of signal.
        means = self.rng.uniform(0, n_samples, n_distributions)

        # Draw random standard deviations between normal and somewhat flattened.
        variances = self.rng.uniform(1, 10, n_distributions)

        # Generate each Gaussian-shaped time series and add to the sum.
        waveform = Gaussian1D()
        for i in range(n_distributions):
            # Generate values based on a Gaussian curve, add them to the sum.
            sum_of_gaussians += waveform.evaluate(time_points, means[i], variances[i])

        # Add noise to the signal.
        noise_factor = sum_of_gaussians.max() / snr
        noise = noise_factor * self.rng.standard_normal(n_samples)
        sum_of_gaussians += noise

        return NoisyGaussianMixture(
            means=means,
            variances=variances,
            noise=noise,
            signal=np.stack((time_points, sum_of_gaussians)),
        )
