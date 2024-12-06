"""Semi-analytical temporal post-processor implementation

@article{2310.18519,
Author = {Saeed A. Khan and Ryan Kaufman and Boris Mesits and Michael Hatridge and Hakan E. Türeci},
Title = {Practical Trainable Temporal Postprocessor for Multistate Quantum Measurement},
Year = {2023},
Eprint = {arXiv:2310.18519},
Howpublished = {PRX Quantum 5, 020364 (2024)},
Doi = {10.1103/PRXQuantum.5.020364},
}

"""

from typing import Union
import numpy as np
import numpy.linalg as la

from qubit_measurement_analysis.data import ShotCollection, SingleShot


def softmax(logits):
    # Subtract the maximum value from logits for numerical stability
    logits_exp = np.exp(logits - np.max(logits, axis=1, keepdims=True))
    probabilities = logits_exp / np.sum(logits_exp, axis=1, keepdims=True)
    return probabilities


class TPPSingle:
    def __init__(self, reg_lambda=1e-3) -> None:
        self.__f = None  # (C, DNT)
        self.__b = None  # (C,)

        self.__D = 2
        self.NT = None

        self.C = None
        self.classes = None
        self.class_mapping = {}

        self.s = None
        self.V = None
        self.VI = None

        self.M = None

        self.Q = None
        self.QI = None
        self.T = None

        # Regularization parameter
        self.reg_lambda = reg_lambda

    @property
    def f(self):
        return self.__f

    @property
    def b(self):
        return self.__b

    def __prep_X(self, data: Union[ShotCollection, SingleShot]):
        # data: (batch, ch, len)
        if len(data.shape) == 3:
            assert data.shape[1] == 1
            X = data.all_values.squeeze(1)  # (batch, len)
        # data: (ch, len)
        else:
            assert data.shape[0] == 1
            X = data.value

        X = np.concatenate([X.real, X.imag], axis=-1)
        # (batch, self.__D*len)
        return X

    def fit(self, data: ShotCollection):
        assert isinstance(data, ShotCollection)
        self.NT = data.shape[-1]
        self.classes = data.unique_classes.squeeze()  # (C,)
        self.C = len(self.classes)

        # 1. Calculate s and V^{-1}
        self.s = np.zeros((self.C, self.__D * self.NT))
        self.V = np.zeros((self.__D * self.NT, self.__D * self.NT))
        for i, c in enumerate(self.classes):
            self.class_mapping.update({i: c})

            current_collection = data.filter_by_pattern(str(c))
            X_c = self.__prep_X(current_collection)  # (batch, self.__D*len)

            self.s[i] = X_c.mean(0)  # (self.__D*len,)
            self.V += np.cov(X_c, rowvar=False)  # (self.__D*len, self.__D*len)

        # Add regularization to improve stability
        self.V += self.reg_lambda * np.eye(self.V.shape[0])
        self.VI = la.inv(self.V)

        # 2. Calculate state Overlap matrix
        self.M = np.zeros((self.C, self.C))

        for c1 in range(self.C):
            for c2 in range(self.C):
                # Calculate overlap
                Oij = self.s[c1, :].T @ self.VI @ self.s[c2, :]  # float
                self.M[c1, c2] = Oij + 1

                # Add same-class contribution if c1 == c2
                if c1 == c2:
                    self.M[c1, c2] = self.M[c1, c2] + 1

        # 3. Generate list of C-1 pairs of states
        Pp = []
        for p in range(self.C - 1):
            Pp.append([p, p + 1])

        # 4. Calculate system matrix
        self.Q = np.zeros((self.C - 1, self.C - 1))
        for pi, p in enumerate(Pp):
            for c in range(self.C - 1):
                self.Q[pi, c] = (self.M[p[0], c] - self.M[p[1], c]) - (
                    self.M[p[0], -1] - self.M[p[1], -1]
                )
        self.QI = la.inv(self.Q)

        # 5. Calculate diagonal bias matrix
        self.T = np.zeros((self.C - 1, self.C - 1))
        for pi, p in enumerate(Pp):
            self.T[pi, pi] = self.M[p[0], -1] - self.M[p[1], -1]

        # 6. Calculate pairwise filters
        Sv = np.zeros((self.C - 1, self.__D * self.NT))
        for pi, p in enumerate(Pp):
            Sv[pi] = self.s[p[0]] - self.s[p[1]]

        # 7. Calculate Optimal Filters and Biases
        self.__f = np.zeros((self.C, self.__D * self.NT))
        self.__b = np.zeros(self.C)
        for c in range(self.C):
            if c < self.C - 1:
                for p in range(self.C - 1):
                    self.__f[c] += self.QI[c, p] * self.VI @ Sv[p]
                    self.__b[c] -= self.QI[c, p] * self.T[p, p]

            else:
                self.__f[c] -= self.__f[:-1].sum(0)
                self.__b[c] = 1 - np.sum(self.__b[:-1])

    def predict(self, data: Union[ShotCollection, SingleShot]):
        X = self.__prep_X(data)  # (batch, self.__D*len)
        y_logits = X @ self.f.T + self.b  # (batch, C)
        y_preds = np.argmax(y_logits, -1)
        # map each predicted class to its original
        y_preds = np.vectorize(self.class_mapping.get)(y_preds)
        return y_preds

    def predict_proba(self, data: Union[ShotCollection, SingleShot]):
        X = self.__prep_X(data)  # (batch, self.__D*len)
        y_logits = X @ self.f.T + self.b  # (batch, C)
        return softmax(y_logits)


class TPP:
    def __init__(self, reg_lambda=1e-3) -> None:
        self.tpps = []
        self.tpp_to_qubit_connection = None
        self.reg_lambda = reg_lambda

    def __getitem__(self, index):
        return self.tpps[index]

    def fit(self, data: ShotCollection):
        self.tpp_to_qubit_connection = {q: i for i, q in enumerate(data.qubits)}

        for tpp_idx in self.tpp_to_qubit_connection.values():
            self.tpps.append(TPPSingle(reg_lambda=self.reg_lambda))
            self[tpp_idx].fit(data[:, tpp_idx])

    def predict(self, data: Union[ShotCollection, SingleShot]):
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
