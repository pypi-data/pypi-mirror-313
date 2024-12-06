import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sklearn.mixture import GaussianMixture

from qubit_measurement_analysis.data import ShotCollection, SingleShot


class ExtendedGaussianMixture(GaussianMixture):

    def relabel_points_ellipses(self, X, y, scaling_factor):
        """Classify points based on whether they fall into scaled ellipses of GMM components.

        Args:
            X (ndarray): ndarray of shape (n_samples, n_features), data to relabel
            y (ndarray): current labels for data
            scaling_factor (float): float, scaling factor for standard deviations along principal axes

        Returns:
            ndarray: ndarray of shape (n_samples,), class labels for each point. 'x' for outliers
        """
        n_components = self.n_components
        n_samples, n_features = X.shape
        outside_ellipse = np.zeros(n_samples, dtype=bool)

        means = self.means_
        covariances = self.covariances_

        for i in range(n_components):
            mu = means[i]
            Sigma = covariances[i]
            # Compute inverse of covariance matrix
            Sigma_inv = np.linalg.inv(Sigma)

            # Compute Mahalanobis distance squared for all points
            diff = X - mu
            D2 = np.einsum("ij,jk,ik->i", diff, Sigma_inv, diff)

            # Points where D2 <= (scaling_factor)^2 fall within the scaled ellipse
            threshold = scaling_factor**2
            outside_ellipse = outside_ellipse | (D2 <= threshold)

        y[~outside_ellipse] = -1
        return y

    def plot_ellipses(self, ax=None, sd_factor=1.0, **ellipse_kwargs):
        """Plot ellipses representing the Gaussian components of the GMM.

        Args:
            ax: Matplotlib axis object. Defaults to None.
            sd_factor (float, optional): Scaling factor for the standard deviations along principal axes. Defaults to 1.0.
        """
        if ax is None:
            _, ax = plt.subplots()

        means = self.means_
        covariances = self.covariances_

        for i in range(self.n_components):
            mu = means[i]
            Sigma = covariances[i]

            # Eigenvalue decomposition of covariance matrix to get ellipse properties
            eigenvalues, eigenvectors = np.linalg.eigh(Sigma)
            order = np.argsort(eigenvalues)[::-1]
            eigenvalues = eigenvalues[order]
            eigenvectors = eigenvectors[:, order]

            # The angle of the ellipse is the angle of the largest eigenvector
            angle = np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0])

            # Width and height of the ellipse are determined by the eigenvalues (scaled by the SD factor)
            width, height = 2 * sd_factor * np.sqrt(eigenvalues)

            # Create an Ellipse patch
            ellipse = Ellipse(
                mu, width, height, angle=np.degrees(angle), **ellipse_kwargs
            )

            ax.add_patch(ellipse)


class GaussianMixtureModels:
    def __init__(self, n_components_list: list[int], **gmm_kwargs) -> None:
        self.gmms = [
            ExtendedGaussianMixture(n_components, **gmm_kwargs)
            for n_components in n_components_list
        ]
        self.gmm_to_qubit_connection = None

    def __getitem__(self, index):
        return self.gmms[index]

    def fit(self, data: ShotCollection, mean_init: bool = True):
        qubits = [int(q) for q in data.qubits]
        self.gmm_to_qubit_connection = {q: i for i, q in enumerate(qubits)}

        for gmm_idx in self.gmm_to_qubit_connection.values():
            if mean_init:
                # get init means for selected qubit
                init_means = self._get_init_means(data[:, gmm_idx])
                # set mean
                self[gmm_idx].means_init = init_means

            X = data.all_values[:, gmm_idx]
            X = np.asarray([X.real, X.imag]).squeeze().T
            self[gmm_idx].fit(X)

    def predict(self, data: ShotCollection):
        bitstrings = {}
        qubits = [int(q) for q in data.qubits]

        for idx, qubit in enumerate(qubits):
            X = data.all_values[:, idx]
            X = np.asarray([X.real, X.imag]).squeeze().T
            y = self[self.gmm_to_qubit_connection[qubit]].predict(X)
            bitstrings[qubit] = y

        qubits_states_all = [
            dict(zip(bitstrings.keys(), values)) for values in zip(*bitstrings.values())
        ]
        singleshots = [
            SingleShot(array, qubits_states, data.is_demodulated, data.device)
            for array, qubits_states in zip(data.all_values, qubits_states_all)
        ]
        return ShotCollection(singleshots, data.device)

    def relabel_by_distance(self, data: ShotCollection, sd_factor: float):
        bitstrings = {}
        qubits = [int(q) for q in data.qubits]

        for idx, qubit in enumerate(qubits):
            X = data.all_values[:, idx]
            X = np.asarray([X.real, X.imag]).squeeze().T
            y = np.array([state[qubit] for state in data.all_qubits_classes])
            y = self[self.gmm_to_qubit_connection[qubit]].relabel_points_ellipses(
                X, y, sd_factor
            )
            bitstrings[qubit] = y

        qubits_states_all = [
            dict(zip(bitstrings.keys(), values)) for values in zip(*bitstrings.values())
        ]
        singleshots = [
            SingleShot(array, qubits_states, data.is_demodulated, data.device)
            for array, qubits_states in zip(data.all_values, qubits_states_all)
        ]
        return ShotCollection(singleshots, data.device)

    def _get_init_means(self, data: ShotCollection):
        means = []
        for state, n_components in zip(["0", "1"], [2, 3]):
            gmm_temp = GaussianMixture(n_components, covariance_type="diag")
            X = data.filter_by_pattern(state).all_values[:, 0]
            X = np.asarray([X.real, X.imag]).squeeze().T
            gmm_temp.fit(X)
            main_component = np.argmax(gmm_temp.weights_)
            means.append(gmm_temp.means_[main_component])
        return means
