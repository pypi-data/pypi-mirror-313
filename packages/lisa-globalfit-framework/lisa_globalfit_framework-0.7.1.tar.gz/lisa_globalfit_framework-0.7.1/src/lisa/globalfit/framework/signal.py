from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import h5py
import numpy as np
from h5py import Dataset
from matplotlib import pyplot as plt


@dataclass
class Signal:
    @abstractmethod
    def write_dataset(self, output: Path) -> None:
        pass

    @abstractmethod
    def plot(self, file: Path) -> None:
        pass

    @classmethod
    @abstractmethod
    def read_dataset(cls, file: Path) -> Self:
        pass


def read_dataset_array(file: h5py.File, path: str) -> np.ndarray:
    """Read a dataset from an HDF5 file to an in-memory array.

    :param file: File to read from.
    :param path: Path to dataset in file.
    :raises ValueError: If the path does not exist in the file or is not a dataset.
    :return: Array containing dataset values.
    """
    dataset = file.get(path)
    if not isinstance(dataset, Dataset):
        raise ValueError(f"invalid {path} dataset ({dataset})")
    return np.array(dataset[:])


@dataclass
class NoisyGaussianMixture(Signal):
    """Sum of gaussians with noise.

    :param means: Array of shape (n_distributions,) with true mean values.
    :param variances: Array of shape (n_distributions,) with true variance values.
    :param noise: Array of shape (n_samples,) with noise values. Implicitly uses the
        same time points as the signal.
    :param signal: Array of shape (2, n_samples) with time points and noisy signal
        values.
    """

    means: np.ndarray
    variances: np.ndarray
    noise: np.ndarray
    signal: np.ndarray

    def n_distributions(self) -> int:
        """Count the number of distributions in the signal.

        :return: Number of distributions.
        """
        return len(self.means)

    def write_dataset(self, output: Path) -> None:
        """Write the signal to a HDF5 file.

        :param output: File to write to.
        """
        with h5py.File(output, "w") as f:
            catalog = f.create_group("cat")
            catalog.create_dataset("means", data=self.means)
            catalog.create_dataset("variances", data=self.variances)

            instrument = f.create_group("instrument")
            instrument.create_dataset("noise", data=self.noise)

            observations = f.create_group("obs")
            observations.create_dataset("signal", data=self.signal)

    def plot(self, file: Path) -> None:
        """Plot the signal to an image file.

        :param file: File to write image to.
        """
        plt.figure()
        time_points, signal = self.signal
        plt.plot(time_points, signal, label="noisy signal", color="darkgrey")
        plt.plot(time_points, signal - self.noise, label="ideal data", color="tab:blue")
        plt.vlines(
            self.means,
            ymin=0,
            ymax=signal.max(),
            label="means",
            linestyles="--",
            color="tab:red",
        )
        plt.legend(loc="best")
        plt.savefig(file)
        plt.close()

    @classmethod
    def read_dataset(cls, file: Path) -> Self:
        """Read a dataset from a HDF5 file.

        :param file: File to read from.
        """
        with h5py.File(file, "r") as f:
            return cls(
                means=read_dataset_array(f, "cat/means"),
                variances=read_dataset_array(f, "cat/variances"),
                noise=read_dataset_array(f, "instrument/noise"),
                signal=read_dataset_array(f, "obs/signal"),
            )
