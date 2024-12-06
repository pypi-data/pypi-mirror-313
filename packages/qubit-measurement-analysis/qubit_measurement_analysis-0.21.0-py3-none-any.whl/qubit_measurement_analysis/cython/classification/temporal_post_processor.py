"""Python wrapper for Cython-accelerated temporal post-processor implementation

@article{2310.18519,
Author = {Saeed A. Khan and Ryan Kaufman and Boris Mesits and Michael Hatridge and Hakan E. Türeci},
Title = {Practical Trainable Temporal Postprocessor for Multistate Quantum Measurement},
Year = {2023},
Eprint = {arXiv:2310.18519},
Howpublished = {PRX Quantum 5, 020364 (2024)},
Doi = {10.1103/PRXQuantum.5.020364},
}
"""

from typing import Union, Dict, List
import numpy as np

from qubit_measurement_analysis.data import ShotCollection, SingleShot
from qubit_measurement_analysis.cython.classification.cttp_utils import (
    prep_X,
    calc_state_parameters,
    calc_overlap_matrix,
    calc_system_matrices,
    calc_optimal_filters,
    predict_proba,
)


class CTPPSingle:
    """Cython-accelerated version of TPPSingle."""

    def __init__(self, reg_lambda: float = 1e-3) -> None:
        self._f = None  # (C, DNT)
        self._b = None  # (C,)
        self.NT = None
        self.C = None
        self.classes = None
        self.class_mapping = {}
        self.reg_lambda = reg_lambda

    @property
    def f(self):
        return self._f

    @property
    def b(self):
        return self._b

    def fit(self, data: ShotCollection) -> None:
        """Fit the temporal post-processor to the data using Cython-optimized computations.

        Parameters
        ----------
        data : ShotCollection
            Collection of shots with class labels
        """
        assert isinstance(data, ShotCollection)
        self.NT = data.shape[-1]
        self.classes = data.unique_classes.squeeze()
        self.C = len(self.classes)

        # Prepare data for each class
        X_classes = []
        for i, c in enumerate(self.classes):
            self.class_mapping[i] = c
            current_collection = data.filter_by_pattern(str(c))
            X_c = prep_X(current_collection.all_values)
            X_classes.append(X_c)

        # Calculate state parameters using Cython
        s, V, VI = calc_state_parameters(X_classes, self.reg_lambda)

        # Calculate overlap matrix using Cython
        M = calc_overlap_matrix(s, VI)

        # Calculate system matrices using Cython
        Q, QI, T = calc_system_matrices(M)

        # Calculate optimal filters and biases using Cython
        self._f, self._b = calc_optimal_filters(s, VI, QI, T)

    def predict(self, data: Union[ShotCollection, SingleShot]) -> np.ndarray:
        """Predict classes for new data using Cython-optimized computations.

        Parameters
        ----------
        data : Union[ShotCollection, SingleShot]
            Input data to classify

        Returns
        -------
        np.ndarray
            Predicted class labels
        """
        X = prep_X(data.all_values if isinstance(data, ShotCollection) else data.value)
        y_logits = predict_proba(X, self._f, self._b)
        y_preds = np.argmax(y_logits, axis=-1)
        return np.vectorize(self.class_mapping.get)(y_preds)


class CTPP:
    """Cython-accelerated version of TPP."""

    def __init__(self, reg_lambda: float = 1e-3) -> None:
        self.tpps: List[CTPPSingle] = []
        self.tpp_to_qubit_connection: Dict = None
        self.reg_lambda = reg_lambda

    def __getitem__(self, index: int) -> CTPPSingle:
        return self.tpps[index]

    def fit(self, data: ShotCollection) -> None:
        """Fit temporal post-processors for each qubit using Cython-optimized computations.

        Parameters
        ----------
        data : ShotCollection
            Collection of shots with class labels for multiple qubits
        """
        self.tpp_to_qubit_connection = {q: i for i, q in enumerate(data.qubits)}

        for tpp_idx in self.tpp_to_qubit_connection.values():
            self.tpps.append(CTPPSingle(reg_lambda=self.reg_lambda))
            self[tpp_idx].fit(data[:, tpp_idx])

    def predict(
        self, data: Union[ShotCollection, SingleShot]
    ) -> Union[ShotCollection, SingleShot]:
        """Predict classes for new data across all qubits using Cython-optimized computations.

        Parameters
        ----------
        data : Union[ShotCollection, SingleShot]
            Input data to classify

        Returns
        -------
        Union[ShotCollection, SingleShot]
            Classified shots
        """
        bitstrings = {}
        for idx, qubit in enumerate(data.qubits):
            data_temp = data[:, idx] if isinstance(data, ShotCollection) else data[idx]
            y_preds = self[self.tpp_to_qubit_connection[qubit]].predict(data_temp)
            bitstrings[qubit] = y_preds

        qubits_classes = [
            dict(zip(bitstrings.keys(), values)) for values in zip(*bitstrings.values())
        ]

        singleshots = [
            SingleShot(array, qubits_states, data.is_demodulated, data.device)
            for array, qubits_states in zip(data.all_values, qubits_classes)
        ]

        if isinstance(data, ShotCollection):
            return ShotCollection(singleshots, data.device)
        else:
            return singleshots[0]
