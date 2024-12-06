"""Data processing functionality for collection of Shots.

This module provides the ShotCollection class for managing and processing
collections of single-shot measurements in quantum experiments.
"""

import os
import re
import glob
import warnings
import random
from typing import (
    List,
    Callable,
    Iterator,
    Iterable,
    Union,
    Dict,
    Optional,
    TypeVar,
    Any,
)

from numpy.typing import NDArray

from qubit_measurement_analysis.data.single_shot import SingleShot
from qubit_measurement_analysis._array_module import ArrayModule
from qubit_measurement_analysis.visualization.shot_collection_plotter import (
    CollectionPlotter as cp,
)

from qubit_measurement_analysis.data._distance_utils import sspd_to as _sspd_to

T = TypeVar("T", bound="ShotCollection")


class ShotCollection:
    """A class for managing and processing collections of single-shot measurements.

    This class provides functionality for handling multiple SingleShot instances,
    including batch operations, filtering, and statistical analysis.

    Attributes:
        singleshots (List[SingleShot]): List of SingleShot instances
        xp (ArrayModule): Array processing module (CPU/GPU)
        all_values (NDArray): Combined array of all shot values
        all_qubits_classes (List[Dict]): List of qubit class mappings
        _is_demodulated (bool): Demodulation status of shots
        _plotter (CollectionPlotter): Visualization handler
        _ops (List): Pending lazy operations
    """

    def __init__(
        self, singleshots: Optional[List[SingleShot]] = None, device: str = "cpu"
    ) -> None:
        """Initialize a ShotCollection instance.

        Args:
            singleshots: Initial list of SingleShot instances
            device: Computation device ("cpu" or "cuda")
        """
        self.xp = ArrayModule(device)
        self.singleshots: List[SingleShot] = []
        self.all_values: Optional[NDArray] = None
        self.all_qubits_classes: Optional[List[Dict[int, int]]] = None
        self._is_demodulated: Optional[bool] = None
        self._plotter = cp(children=self)
        self._ops: List[tuple[Callable, dict]] = []

        if singleshots:
            self.extend(singleshots)

    def _validate_shots(self, shots: List[SingleShot]) -> None:
        """Validate a list of SingleShot instances.

        Args:
            shots: List of SingleShot instances to validate

        Raises:
            TypeError: If shots contain non-SingleShot objects
            ValueError: If shots have inconsistent properties
        """
        if not shots:
            return

        if not all(isinstance(shot, SingleShot) for shot in shots):
            raise TypeError("All elements must be SingleShot objects")

        first_shot_keys = set(shots[0].qubits_classes.keys())
        if not all(
            set(shot.qubits_classes.keys()) == first_shot_keys for shot in shots
        ):
            raise ValueError("All shots must have the same qubits_classes keys")

        first_shot_demodulated = shots[0].is_demodulated
        if not all(shot.is_demodulated == first_shot_demodulated for shot in shots):
            raise ValueError("All shots must have the same demodulation status")

        self._is_demodulated = first_shot_demodulated

    def _apply_vectorized(self, func: Callable, **kwargs) -> "ShotCollection":
        """Apply a vectorized operation lazily.

        Args:
            func: Operation to apply
            **kwargs: Operation parameters

        Returns:
            Self with pending operation
        """
        self._ops.append((func, kwargs))
        return self

    def _arithmetic_op(self, other: Any, op: Callable) -> "ShotCollection":
        """Helper method for arithmetic operations.

        Args:
            other: Value to operate with
            op: Operation to perform

        Returns:
            New ShotCollection with operation result

        Raises:
            TypeError: If operation with other type is not supported
        """
        if hasattr(other, "value") or hasattr(other, "all_values"):
            raise TypeError(f"Cannot perform operation with {type(other)}")

        new_values = op(self.all_values, other)
        new_shots = [
            SingleShot(value, qubits_classes, self.is_demodulated, self.device)
            for value, qubits_classes in zip(new_values, self.all_qubits_classes)
        ]
        return type(self)(new_shots, self.device)

    def __getitem__(
        self, index: Union[int, slice, tuple]
    ) -> Union[SingleShot, "ShotCollection"]:
        """Get item(s) by index.

        Args:
            index: Index specification

        Returns:
            SingleShot or ShotCollection depending on index type
        """
        if isinstance(index, tuple):
            shot_indices = index[0]
            shot_slices = index[1:]
            selected_shots = self.singleshots[shot_indices]
            selected_shots = (
                [selected_shots]
                if isinstance(selected_shots, SingleShot)
                else selected_shots
            )
            new_shots = [shot[shot_slices] for shot in selected_shots]
            return type(self)(new_shots, self.device)
        elif isinstance(index, slice):
            return type(self)(self.singleshots[index], self.device)
        else:
            return self.singleshots[index]

    def __len__(self) -> int:
        return len(self.singleshots)

    def __repr__(self) -> str:
        return f"ShotCollection(n_shots={len(self)}, device='{self.device}', pending_ops={len(self._ops)})"

    def __iter__(self) -> Iterator[SingleShot]:
        return iter(self.singleshots)

    def __copy__(self) -> "ShotCollection":
        return type(self)(self.singleshots, self.device)

    def __add__(self, other: Any) -> "ShotCollection":
        return self._arithmetic_op(other, self.xp.transformations.add)

    def __sub__(self, other: Any) -> "ShotCollection":
        return self._arithmetic_op(other, self.xp.transformations.sub)

    def __mul__(self, other: Any) -> "ShotCollection":
        return self._arithmetic_op(other, self.xp.transformations.mul)

    def __truediv__(self, other: Any) -> "ShotCollection":
        return self._arithmetic_op(other, self.xp.transformations.div)

    def __iadd__(self, other: Any) -> "ShotCollection":
        return self.__add__(other)

    def __isub__(self, other: Any) -> "ShotCollection":
        return self.__sub__(other)

    def __imul__(self, other: Any) -> "ShotCollection":
        return self.__mul__(other)

    def __itruediv__(self, other: Any) -> "ShotCollection":
        return self.__truediv__(other)

    @property
    def device(self) -> str:
        """Get the computation device name."""
        return self.xp.device

    def to(self, device: str, use_cython: bool = False) -> "ShotCollection":
        """Move data to specified device.

        Args:
            device: Target device ("cpu" or "cuda")
            use_cython: Whether or not to use C compiled code

        Returns:
            Self with data moved to target device
        """
        self.xp = ArrayModule(device, use_cython)
        for shot in self.singleshots:
            shot.to(device, use_cython)
        self._update_arrays()
        return self

    @property
    def shape(self) -> tuple:
        """Get the shape of the combined values array."""
        return self.all_values.shape

    @property
    def is_demodulated(self) -> bool:
        """Get the demodulation status of the collection."""
        return bool(self._is_demodulated)

    def scatter(self, ax=None, **kwargs):
        """Create a scatter plot of the data."""
        return self._plotter.scatter(ax, **kwargs)

    def plot_hist(
        self,
        ax=None,
        correct_key: Optional[str] = None,
        correct_color: Optional[str] = None,
        default_color: str = "tab:blue",
    ):
        """Plot histogram of the data."""
        return self._plotter.plot_hist(ax, correct_key, correct_color, default_color)

    def plot_hist_proba(
        self,
        ax=None,
        correct_key: Optional[str] = None,
        correct_color: Optional[str] = None,
        default_color: str = "tab:blue",
    ):
        """Plot probability histogram of the data."""
        return self._plotter.plot_hist_proba(
            ax, correct_key, correct_color, default_color
        )

    def append(self, shot: SingleShot) -> None:
        """Append a single shot to the collection."""
        self.extend([shot])

    def extend(self, shots: List[SingleShot]) -> None:
        """Extend the collection with multiple shots.

        Args:
            shots: List of SingleShot instances to add
        """
        self._validate_shots(shots)
        self.singleshots.extend(shots)
        self._update_arrays()
        self._update_qubits_classes()

    def shuffle(self, seed: Optional[int] = None) -> "ShotCollection":
        """Randomly shuffle the shots.

        Args:
            seed: Random seed for reproducibility

        Returns:
            Self with shuffled shots
        """
        random.seed(seed)
        random.shuffle(self.singleshots)
        self._update_arrays()
        self._update_qubits_classes()
        return self

    def classes_like(self, other: "ShotCollection") -> "ShotCollection":
        """Update qubit classes to match another collection.

        Updates the qubit classes of shots with matching IDs to match
        the classes in the other collection.

        Args:
            other: Collection to copy classes from

        Returns:
            Self with updated classes
        """
        other_id_to_classes = {
            shot.id: shot.qubits_classes for shot in other.singleshots
        }
        for shot in self.singleshots:
            if shot.id in other_id_to_classes:
                shot.update_qubits_states(other_id_to_classes[shot.id])
        self._update_qubits_classes()
        return self

    def _update_arrays(self) -> None:
        """Update the combined values array."""
        self.all_values = None
        self.xp.free_all_blocks()
        new_values = self.xp.array([shot.value for shot in self.singleshots])
        self.all_values = self.xp.stack(new_values)

    def _update_qubits_classes(self) -> None:
        """Update the combined qubit classes list."""
        self.all_qubits_classes = [shot.qubits_classes for shot in self.singleshots]

    @property
    def all_classes(self) -> NDArray:
        """Get array of all class labels."""
        return self.xp.vstack([shot.classes for shot in self.singleshots])

    @property
    def qubits(self) -> List[int]:
        """Get list of qubit indices."""
        return self[0].qubits

    def mean(self, axis: int = -1) -> Union[SingleShot, "ShotCollection"]:
        """Calculate mean along specified axis.

        Args:
            axis: Axis to compute mean along

        Returns:
            Mean result as SingleShot or ShotCollection

        Raises:
            ValueError: If collection is empty
        """
        if not self.singleshots:
            raise ValueError("Collection is empty")

        if axis == 0:
            qubits_classes = self.singleshots[0].qubits_classes
            if len(self.unique_classes_str) != 1:
                qubits_classes = {int(reg): -1 for reg in list(self._qubits_str)}
                warnings.warn(
                    "Collection contains multiple states. Taking mean regardless of state. Assigned state is '<UNK>'"
                )
            return SingleShot(
                self.all_values.mean(axis),
                qubits_classes,
                self.is_demodulated,
                self.device,
            )
        else:
            return self._apply_vectorized(self.xp.transformations.mean, axis=axis)

    @property
    def unique_classes(self) -> NDArray:
        """Get array of unique class combinations."""
        return self.xp.unique(self.all_classes, axis=0)

    @property
    def unique_classes_str(self) -> List[str]:
        """Get list of unique class strings."""
        return list({shot.state for shot in self.singleshots})

    def unique_classes_by_qubit(self, qubit: int) -> set:
        """Get unique classes for a specific qubit.

        Args:
            qubit: Qubit index

        Returns:
            Set of unique classes for the qubit

        Raises:
            AssertionError: If qubit not in collection
        """
        assert qubit in self.qubits
        return {qc[qubit] for qc in self.unique_qubits_classes}

    @property
    def unique_qubits_classes(self) -> List[Dict[int, int]]:
        """Get list of unique qubit class mappings."""
        seen = set()
        unique_dicts = []
        for d in self.all_qubits_classes:
            dict_tuple = tuple(sorted(d.items()))
            if dict_tuple not in seen:
                seen.add(dict_tuple)
                unique_dicts.append(d)
        return unique_dicts

    @property
    def counts(self) -> Dict[str, int]:
        """Get counts of each unique state."""
        return {
            state: len(self.filter_by_pattern(state))
            for state in self.unique_classes_str
        }

    @property
    def counts_proba(self) -> Dict[str, float]:
        """Get probability distribution of states."""
        return {
            state: len(self.filter_by_pattern(state)) / len(self)
            for state in self.unique_classes_str
        }

    def update_all_qubits_classes(
        self, updated_elements: Dict[int, Dict[int, int]]
    ) -> None:
        """Update qubit classes according to mapping.

        Args:
            updated_elements: Nested dict mapping {qubit: {old_class: new_class}}
        """
        for shot in self.singleshots:
            for key, value in shot.qubits_classes.items():
                if key in updated_elements and value in updated_elements[key]:
                    shot.update_qubits_states({key: updated_elements[key][value]})
        self._update_qubits_classes()

    @property
    def _qubits_str(self) -> Union[str, List[str]]:
        """Get string representation of qubit registers."""
        unique_registers = {shot._qubits_str for shot in self.singleshots}
        return (
            list(unique_registers)
            if len(unique_registers) > 1
            else list(unique_registers)[0]
        )

    def filter_by_pattern(self, patterns: Union[str, List[str]]) -> "ShotCollection":
        """Filter shots by state pattern(s).

        Args:
            patterns: Regex pattern(s) to match states against

        Returns:
            New ShotCollection with matching shots
        """
        patterns = [patterns] if isinstance(patterns, str) else patterns
        compiled_patterns = [re.compile(pattern) for pattern in patterns]
        matched_strings = {
            s
            for s in self.unique_classes_str
            if any(p.match(s) for p in compiled_patterns)
        }
        return type(self)(
            [shot for shot in self.singleshots if shot.state in matched_strings],
            self.device,
        )

    def filter_by_qubits_classes(
        self, qubits_classes: Union[Dict[int, int], List[Dict[int, int]]]
    ) -> "ShotCollection":
        """Filter shots by qubit class mapping(s).

        Args:
            qubits_classes: Mapping(s) of qubit indices to classes

        Returns:
            New ShotCollection with matching shots
        """
        qubits_classes = (
            [qubits_classes] if isinstance(qubits_classes, dict) else qubits_classes
        )
        filtered_shots = []
        for shot in self.singleshots:
            for filter_dict in qubits_classes:
                if all(
                    shot.qubits_classes.get(key) == value
                    for key, value in filter_dict.items()
                ):
                    filtered_shots.append(shot)
                    break
        return type(self)(filtered_shots, self.device)

    def demodulate_all(
        self,
        intermediate_freq: Dict[int, float],
        meas_time: Iterable,
        direction: str = "clockwise",
    ) -> "ShotCollection":
        """Demodulate all shots.

        Args:
            intermediate_freq: Mapping of qubit indices to frequencies
            meas_time: Measurement time points
            direction: Rotation direction

        Returns:
            Self with pending demodulation
        """
        intermediate_freq = self.xp.array(list(intermediate_freq.values())).reshape(
            -1, 1
        )
        meas_time = meas_time.reshape(1, -1)
        return self._apply_vectorized(
            self.xp.transformations.demodulate,
            intermediate_freq=intermediate_freq,
            meas_time=meas_time,
            direction=direction,
            module=self.xp,
        )

    def mean_centring_all(self, axis: int = -1) -> "ShotCollection":
        """Center all shots by subtracting mean."""
        return self._apply_vectorized(self.xp.transformations.mean_centring, axis=axis)

    def mean_convolve_all(self, kernel_size: int, stride: int) -> "ShotCollection":
        """Apply mean convolution to all shots."""
        return self._apply_vectorized(
            self.xp.transformations.mean_convolve,
            kernel_size=kernel_size,
            stride=stride,
            module=self.xp,
        )

    def whittaker_eilers_smoother_all(self, lamb: float, d: int) -> "ShotCollection":
        """Apply Whittaker-Eilers smoothing to all shots."""
        return self._apply_vectorized(
            self.xp.transformations.whittaker_eilers_smoother,
            lamb=lamb,
            d=d,
            module=self.xp,
        )

    def compute(self, free_all_blocks: bool = False) -> "ShotCollection":
        """Execute all pending operations.

        Args:
            free_all_blocks: Whether to free memory after computation

        Returns:
            New ShotCollection with operations applied
        """
        if not self._ops:
            return self

        result = self.all_values
        for func, kwargs in self._ops:
            result = func(result, **kwargs)
        result = result.astype(self.xp.complex64)

        is_demodulated = (
            self.xp.transformations.demodulate in [t[0] for t in self._ops]
            or self.is_demodulated
        )

        new_shots = [
            SingleShot(value, shot.qubits_classes, is_demodulated, self.device, shot.id)
            for value, shot in zip(result, self.singleshots)
        ]

        new_collection = type(self)(new_shots, self.device)
        self._ops.clear()

        if free_all_blocks:
            self.xp.free_all_blocks()

        return new_collection

    def sspd_to(
        self, other: Union[SingleShot, NDArray], method: str = "cross_product"
    ) -> NDArray:
        """Calculate SSPD to another shot/array.

        Args:
            other: Target to compute distance to
            method: Distance computation method

        Returns:
            Array of SSPD values
        """
        return _sspd_to(self.all_values, other, self.xp, method)

    def save_all(
        self,
        parent_dir: str,
        train_ratio: float,
        val_ratio: float,
        test_ratio: float,
        clear_existing: bool = False,
        verbose: bool = False,
    ) -> None:
        """Save collection with train/val/test splits.

        Args:
            parent_dir: Parent directory for saving
            train_ratio: Fraction for training set
            val_ratio: Fraction for validation set
            test_ratio: Fraction for test set
            clear_existing: Whether to clear existing files
            verbose: Whether to print progress

        Raises:
            ValueError: If ratios are invalid
        """
        if not all(0 <= r <= 1 for r in (train_ratio, val_ratio, test_ratio)):
            raise ValueError("Ratios must be between 0 and 1")

        if not abs(train_ratio + val_ratio + test_ratio - 1) < 1e-6:
            raise ValueError("Ratios must sum to 1")

        if clear_existing:
            if verbose:
                print("[INFO] Deleting files...")
            for subfolder in ["train", "val", "test"]:
                for state in self.unique_classes_str:
                    directory = os.path.join(
                        parent_dir, self._qubits_str, subfolder, state
                    )
                    for file in glob.glob(os.path.join(directory, "*.npy")):
                        os.remove(file)

        self.xp.random.shuffle(self.singleshots)
        num_shots = len(self)
        train_end = int(train_ratio * num_shots)
        val_end = train_end + int(val_ratio * num_shots)

        if verbose:
            print("[INFO] Start saving files...")

        for idx, shot in enumerate(self.singleshots):
            subfolder = (
                "train" if idx < train_end else "val" if idx < val_end else "test"
            )
            shot.save(parent_dir, subfolder, verbose)

    @classmethod
    def load(
        cls,
        parent_dir: str,
        qubits_dir: str,
        state: str,
        subfolder: str,
        num_samples: Optional[int] = None,
        verbose: bool = False,
    ) -> "ShotCollection":
        """Load shots from directory.

        Args:
            parent_dir: Parent directory containing data
            qubits_dir: Qubit number set folder (e.g., '123')
            state: System state (e.g., '001')
            subfolder: Subfolder name ('train', 'val', or 'test')
            num_samples: Number of samples to load (None for all)
            verbose: Whether to print progress

        Returns:
            New ShotCollection with loaded shots
        """
        collection = cls()

        if num_samples is None:
            directory = os.path.join(parent_dir, qubits_dir, subfolder, state)
            num_samples = len(glob.glob(os.path.join(directory, "*")))

        for idx in range(num_samples):
            shot = SingleShot.load(
                parent_dir, qubits_dir, state, subfolder, idx, verbose
            )
            collection.append(shot)

        return collection
