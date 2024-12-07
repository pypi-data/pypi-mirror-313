from pathlib import Path

import h5py
from corner import corner
from matplotlib import pyplot as plt

from lisa.globalfit.framework.signal import read_dataset_array


class ModuleExecutionDrawer:
    def plot_corner(self, chains: Path, dataset: str, output: Path) -> None:
        with h5py.File(chains) as f:
            samples = read_dataset_array(f, dataset)

        # Stack all walkers chains.
        samples = samples.reshape(
            samples.shape[0] * samples.shape[1], samples.shape[-1]
        )

        # Write corner plot to image.
        fig = corner(samples, show_titles=True, quantiles=[0.16, 0.5, 0.84])
        plt.savefig(output)
        plt.close(fig)
