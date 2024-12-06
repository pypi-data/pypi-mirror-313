"""Data processing functionality for Single-Shots.

This module provides the SingleShot class for storing and processing single-shot
measurement data in quantum experiments.
"""

import os
import uuid
import glob
from typing import Dict, Union, List, Optional, TypeVar, Callable
from functools import wraps

import numpy as np
from numpy.typing import ArrayLike, NDArray

from qubit_measurement_analysis.visualization.single_shot_plotter import (
    SingleShotPlotter as ssp,
)
from qubit_measurement_analysis import ArrayModule

from qubit_measurement_analysis.data._distance_utils import sspd_to as _sspd_to

T = TypeVar("T", bound="SingleShot")


def _create_new_instance(func: Callable) -> Callable:
    """Decorator for creating new SingleShot instances with transformed values."""

    @wraps(func)
    def wrapper(self: T, *args, **kwargs) -> T:
        new_value = func(self, *args, **kwargs)
        return type(self)(
            new_value, self.qubits_classes, self._is_demodulated, self.device, self.id
        )

    return wrapper


class SingleShot:
    """A class for storing and processing a single SingleShot entity.

    This class represents a single-shot measurement in quantum experiments,
    providing methods for data manipulation, analysis, and visualization.

    Attributes:
        value (NDArray): Complex-valued measurement data
        _qubits_classes (Dict[int, int]): Mapping of qubit indices to their states
        _is_demodulated (bool): Flag indicating if data has been demodulated
        xp (ArrayModule): Array processing module (CPU/GPU)
        id (str): Unique identifier for the shot
        _plotter (SingleShotPlotter): Visualization handler
    """

    __slots__ = (
        "_is_demodulated",
        "xp",
        "value",
        "_qubits_classes",
        "id",
        "_plotter",
    )

    def __init__(
        self,
        value: ArrayLike,
        qubits_classes: Dict[int, int],
        _is_demodulated: Optional[bool] = None,
        device: str = "cpu",
        _id: Optional[str] = None,
    ) -> None:
        """Initialize a SingleShot instance.

        Args:
            value: Complex-valued measurement data
            qubits_classes: Mapping of qubit indices to their states
            _is_demodulated: Flag indicating if data has been demodulated
            device: Computation device ("cpu" or "cuda")
            _id: Unique identifier for the shot

        Raises:
            TypeError: If value type doesn't match device or isn't complex
            ValueError: If value dimensions are invalid
        """
        self._is_demodulated = (
            bool(_is_demodulated) if _is_demodulated is not None else False
        )
        self.xp = ArrayModule(device)

        if not isinstance(value, self.xp.ndarray):
            raise TypeError(f"Device mismatch: expected {device=}, got {value.device=}")

        if not self.xp.issubdtype(value.dtype, self.xp.complexfloating):
            raise TypeError("value must be of `np.complexfloating` dtype")

        if value.ndim > 1 and value.shape[0] > 1 and not self._is_demodulated:
            raise ValueError("value of complex dtype must be 1 dimensional")

        self.value = (
            value.astype(self.xp.dtype) if value.dtype != self.xp.dtype else value
        )
        self.value = value if value.ndim > 1 else value.reshape(1, -1)
        self._qubits_classes = qubits_classes.copy()
        self.id = str(uuid.uuid4()) if _id is None else _id
        self._plotter = ssp(children=self)

    def __getitem__(self, index: Union[int, slice, tuple]) -> "SingleShot":
        """Get a slice of the value array.

        Args:
            index: Index or slice to retrieve

        Returns:
            A new SingleShot instance with the sliced data
        """
        regs_items = list(self.qubits_classes.items())
        if isinstance(index, tuple):
            new_reg_items = (
                [regs_items[index[0]]]
                if isinstance(index[0], int)
                else regs_items[index[0]]
            )
        else:
            new_reg_items = (
                [regs_items[index]] if isinstance(index, int) else regs_items[index]
            )

        return type(self)(
            self.value[index],
            {item[0]: item[1] for item in new_reg_items},
            self._is_demodulated,
            self.device,
            self.id,
        )

    def __repr__(self) -> str:
        """Return a string representation of the SingleShot instance."""
        return f"SingleShot(value={self.value}, qubits_classes='{self.qubits_classes}')"

    def __copy__(self) -> "SingleShot":
        """Create a shallow copy of the SingleShot instance."""
        return type(self)(
            self.value, self.qubits_classes, self._is_demodulated, self.device, self.id
        )

    def _arithmetic_op(
        self, other: Union["SingleShot", ArrayLike], op: Callable
    ) -> "SingleShot":
        """Helper method for arithmetic operations."""
        other_value = other.value if hasattr(other, "value") else other
        new_value = op(self.value, other_value)
        return type(self)(
            new_value, self.qubits_classes, self._is_demodulated, self.device
        )

    def __add__(self, other: Union["SingleShot", ArrayLike]) -> "SingleShot":
        return self._arithmetic_op(other, self.xp.transformations.add)

    def __sub__(self, other: Union["SingleShot", ArrayLike]) -> "SingleShot":
        return self._arithmetic_op(other, self.xp.transformations.sub)

    def __mul__(self, other: Union["SingleShot", ArrayLike]) -> "SingleShot":
        return self._arithmetic_op(other, self.xp.transformations.mul)

    def __truediv__(self, other: Union["SingleShot", ArrayLike]) -> "SingleShot":
        return self._arithmetic_op(other, self.xp.transformations.div)

    def __iadd__(self, other: Union["SingleShot", ArrayLike]) -> "SingleShot":
        return self.__add__(other)

    def __isub__(self, other: Union["SingleShot", ArrayLike]) -> "SingleShot":
        return self.__sub__(other)

    def __imul__(self, other: Union["SingleShot", ArrayLike]) -> "SingleShot":
        return self.__mul__(other)

    def __itruediv__(self, other: Union["SingleShot", ArrayLike]) -> "SingleShot":
        return self.__truediv__(other)

    @property
    def is_demodulated(self) -> bool:
        """Indicates whether the SingleShot instance has been demodulated."""
        return self._is_demodulated

    @property
    def _qubits_str(self) -> str:
        """Get the qubit register string."""
        return "".join(map(str, self.qubits_classes.keys()))

    @property
    def state(self) -> str:
        """Get the state string representation."""
        return "".join(map(str, self.qubits_classes.values()))

    @property
    def qubits_classes(self) -> Dict[int, str]:
        """Get a copy of the qubit classes mapping."""
        return self._qubits_classes.copy()

    @property
    def qubits(self) -> List[int]:
        """Get list of qubit indices."""
        return list(self.qubits_classes.keys())

    @property
    def classes(self) -> List[int]:
        """Get list of qubit states."""
        return list(self.qubits_classes.values())

    @property
    def shape(self) -> tuple:
        """Get the shape of the value array."""
        return self.value.shape

    @property
    def device(self) -> str:
        """Get the computation device name."""
        return self.xp.device

    def update_qubits_states(self, updated_elements: Dict[int, int]) -> None:
        """Update qubit states with new values.

        Args:
            updated_elements: Dictionary mapping qubit indices to new states
        """
        self._qubits_classes.update(updated_elements)

    def scatter(self, ax=None, **kwargs):
        """Create a scatter plot of the data."""
        return self._plotter.scatter(ax, **kwargs)

    def plot(self, ax=None, x=None, **kwargs):
        """Create a line plot of the data."""
        return self._plotter.plot(ax, x, **kwargs)

    @_create_new_instance
    def mean(self, axis: int = -1) -> NDArray:
        """Calculate the mean along the specified axis."""
        return self.xp.transformations.mean(self.value, axis)

    @_create_new_instance
    def mean_convolve(self, kernel_size: int, stride: int) -> NDArray:
        """Apply mean convolution with specified kernel size and stride."""
        return self.xp.transformations.mean_convolve(
            self.value, kernel_size, stride, self.xp
        )

    @_create_new_instance
    def mean_centring(self, axis: int = -1) -> NDArray:
        """Center the values by subtracting the mean."""
        return self.xp.transformations.mean_centring(self.value, axis)

    def demodulate(
        self,
        intermediate_freq: Dict[int, float],
        meas_time: ArrayLike,
        direction: str = "clockwise",
    ) -> "SingleShot":
        """Demodulate the signal.

        Args:
            intermediate_freq: Mapping of qubit indices to intermediate frequencies
            meas_time: Signal measurement time points
            direction: Rotation direction ("clockwise" or "counterclockwise")

        Raises:
            ValueError: If already demodulated or invalid frequency mapping
            TypeError: If meas_time is not 1D array

        Returns:
            New SingleShot instance with demodulated values
        """
        if self._is_demodulated:
            raise ValueError(
                "Cannot demodulate SingleShot which is already demodulated"
            )

        if not set(intermediate_freq.keys()).issubset(self.qubits_classes.keys()):
            raise ValueError(
                f"intermediate_freq.keys() must be subset of qubits_classes.keys(): "
                f"got {intermediate_freq.keys()} and {self.qubits_classes.keys()}"
            )

        meas_time = (
            self.xp.asarray(meas_time)
            if not isinstance(meas_time, self.xp.ndarray)
            else meas_time
        )
        if meas_time.ndim != 1:
            raise TypeError("meas_time must be a 1D array")

        if self.shape[-1] != meas_time.shape[-1]:
            raise ValueError(
                f"Last dimensions must match: got {self.shape[-1]} and {meas_time.shape[-1]}"
            )

        intermediate_freq = self.xp.array(list(intermediate_freq.values())).reshape(
            -1, 1
        )
        meas_time = meas_time.reshape(1, -1)

        value_new = self.xp.transformations.demodulate(
            self.value, intermediate_freq, meas_time, direction, self.xp
        )
        return type(self)(value_new, self.qubits_classes, True, self.device, self.id)

    @_create_new_instance
    def whittaker_eilers_smoother(self, lamb: float, d: int) -> NDArray:
        """Apply Whittaker-Eilers smoothing.

        Args:
            lamb: Smoothing parameter
            d: Difference order
        """
        return self.xp.transformations.whittaker_eilers_smoother(
            self.value, lamb, d, self.xp
        )

    def get_fft_amps_freqs(self, sampling_rate: float) -> tuple[NDArray, NDArray]:
        """Calculate FFT amplitudes and frequencies.

        Args:
            sampling_rate: Signal sampling rate

        Returns:
            Tuple of (amplitudes, frequencies)
        """
        _, signal_length = self.shape
        freqs = self.xp.fft.fftfreq(signal_length, d=1.0 / sampling_rate)
        fft_results = self.xp.fft.fft(self.value, axis=1)
        amplitudes = self.xp.abs(fft_results) / signal_length
        return amplitudes, freqs

    def sspd_to(self, other: Union["SingleShot", ArrayLike]) -> float:
        """Calculate SSPD distance to another shot/array."""
        return _sspd_to(source=self.value, other=other, xp=self.xp)

    def save(
        self,
        parent_dir: str,
        subfolder: str,
        verbose: bool = False,
    ) -> None:
        """Save the SingleShot instance.

        Args:
            parent_dir: Parent directory for saving
            subfolder: Subfolder name ('train', 'val', or 'test')
            verbose: Whether to print save information
        """
        directory = os.path.join(parent_dir, self._qubits_str, subfolder, self.state)
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"{self.id}.npy")
        self.xp.save(file_path, self.value)
        if verbose:
            print(f"Saved {self.state} {subfolder} data to {file_path}")

    @classmethod
    def load(
        cls,
        parent_dir: str,
        qubits_dir: str,
        state: str,
        subfolder: str,
        index: int,
        verbose: bool = False,
    ) -> "SingleShot":
        """Load a SingleShot instance.

        Args:
            parent_dir: Parent directory containing the data
            qubits_dir: Qubit number set folder (e.g., '123')
            state: System state (e.g., '001')
            subfolder: Subfolder name ('train', 'val', or 'test')
            index: File index to load
            verbose: Whether to print load information

        Returns:
            Loaded SingleShot instance

        Raises:
            ValueError: If loaded file has unsupported dtype
        """
        directory = os.path.join(parent_dir, qubits_dir, subfolder, state, "*.npy")
        dir_generator = glob.iglob(directory)
        filename = next(x for i, x in enumerate(dir_generator) if i == index)
        _id = os.path.splitext(os.path.basename(filename))[0]

        loaded_file = np.load(filename)
        if loaded_file.dtype != np.complex64:
            raise ValueError(
                "Unsupported dtype in loaded file. Must be 'np.complex64'."
            )

        value = loaded_file
        is_demodulated = loaded_file.shape[0] > 1
        qubits_classes = {int(q): int(s) for q, s in zip(qubits_dir, state)}

        loaded_instance = cls(value, qubits_classes, is_demodulated)
        loaded_instance.id = _id

        if verbose:
            print(f"[INFO] {filename} has been loaded.")
        return loaded_instance

    def to(self, device: str, use_cython: bool = False) -> "SingleShot":
        """Move data to specified device.

        Args:
            device: Target device ("cpu" or "cuda")
            use_cython: Whether or not to use C compiled code

        Returns:
            Self with data moved to target device
        """
        if device == self.device and self.xp.use_cython == use_cython:
            return self

        self.xp = ArrayModule(device, use_cython)
        if isinstance(self.value, self.xp.ndarray) and device.startswith("cuda"):
            self.value = self.xp.array(self.value)
        elif hasattr(self.value, "get") and device == "cpu":
            self.value = self.value.get()
        else:
            self.value = self.xp.array(self.value)

        return self
