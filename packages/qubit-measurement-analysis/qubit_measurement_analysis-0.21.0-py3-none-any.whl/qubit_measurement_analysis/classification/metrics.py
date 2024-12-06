from sklearn.metrics import confusion_matrix
from qubit_measurement_analysis.data import ShotCollection
import numpy as np


def calculate_accuracy(conf_matrix):
    """
    Calculates the accuracy from the confusion matrix.

    Parameters:
    - conf_matrix (numpy.ndarray): Confusion matrix

    Returns:
    - float: Accuracy value
    """
    return np.trace(conf_matrix) / np.sum(conf_matrix)


def calculate_fidelity(conf_matrix):
    """
    Calculates the fidelity from the confusion matrix.
    Fidelity is calculated as:
    fidelity = 1 - 0.5 * (FP + FN) / (TP + FP + FN + TN)

    Parameters:
    - conf_matrix (numpy.ndarray): Confusion matrix

    Returns:
    - float: Fidelity value
    """
    accuracy = calculate_accuracy(conf_matrix)
    error = 1 - accuracy
    fidelity = 1 - error / 2
    return fidelity


def calculate_binary_precision(conf_matrix):
    """
    Calculates precision for binary classification.

    Parameters:
    - conf_matrix (numpy.ndarray): Confusion matrix for binary classification

    Returns:
    - float: Precision for the positive class
    """
    tp = conf_matrix[1, 1]
    fp = conf_matrix[0, 1]
    precision = tp / (tp + fp) if (tp + fp) > 0 else None
    return np.float64(precision)


def calculate_binary_recall(conf_matrix):
    """
    Calculates recall for binary classification.

    Parameters:
    - conf_matrix (numpy.ndarray): Confusion matrix for binary classification

    Returns:
    - float: Recall for the positive class
    """
    tp = conf_matrix[1, 1]
    fn = conf_matrix[1, 0]
    recall = tp / (tp + fn) if (tp + fn) > 0 else None
    return np.float64(recall)


def calculate_macro_precision(conf_matrix):
    """
    Calculates macro-averaged precision for multiclass classification.
    Macro-averaged precision is the average of precision values for each class.

    Parameters:
    - conf_matrix (numpy.ndarray): Confusion matrix for multiclass classification

    Returns:
    - float: Macro-averaged precision
    """
    class_precision = np.diag(conf_matrix) / np.sum(conf_matrix, axis=0)
    return np.nanmean(class_precision)


def calculate_macro_recall(conf_matrix):
    """
    Calculates macro-averaged recall for multiclass classification.
    Macro-averaged recall is the average of recall values for each class.

    Parameters:
    - conf_matrix (numpy.ndarray): Confusion matrix for multiclass classification

    Returns:
    - float: Macro-averaged recall
    """
    class_recall = np.diag(conf_matrix) / np.sum(conf_matrix, axis=1)
    return np.nanmean(class_recall)


def calculate_micro_precision(conf_matrix):
    """
    Calculates micro-averaged precision for multiclass classification.
    Micro-averaged precision treats all classes equally by considering total TP, FP, and FN.

    Parameters:
    - conf_matrix (numpy.ndarray): Confusion matrix for multiclass classification

    Returns:
    - float: Micro-averaged precision
    """
    tp = np.trace(conf_matrix)
    fp = np.sum(conf_matrix, axis=0) - np.diag(conf_matrix)
    precision = tp / (tp + np.sum(fp))
    return precision


def calculate_micro_recall(conf_matrix):
    """
    Calculates micro-averaged recall for multiclass classification.
    Micro-averaged recall treats all classes equally by considering total TP, FP, and FN.

    Parameters:
    - conf_matrix (numpy.ndarray): Confusion matrix for multiclass classification

    Returns:
    - float: Micro-averaged recall
    """
    tp = np.trace(conf_matrix)
    fn = np.sum(conf_matrix, axis=1) - np.diag(conf_matrix)
    recall = tp / (tp + np.sum(fn))
    return recall


class Metrics:

    @staticmethod
    def __calculate_metric(metric, data_true, data_pred):
        assert isinstance(data_true, ShotCollection) and isinstance(
            data_pred, ShotCollection
        )
        assert data_true.shape == data_pred.shape

        metrics = []
        for i, _ in enumerate(data_true.qubits):
            y_true = data_true.all_classes[:, i]
            y_pred = data_pred.all_classes[:, i]
            cm = confusion_matrix(y_true, y_pred)
            metrics.append(metric(cm))
        return metrics if len(metrics) > 1 else metrics[0]

    @staticmethod
    def get_conf_matrix(data_true: ShotCollection, data_pred: ShotCollection):
        assert isinstance(data_true, ShotCollection) and isinstance(
            data_pred, ShotCollection
        )
        assert data_true.shape == data_pred.shape

        if data_true.shape[1] > 1:
            assert sorted(data_true.unique_classes_str) == sorted(
                data_pred.unique_classes_str
            )
            str_states_true = [shot.state for shot in data_true]
            str_states_pred = [shot.state for shot in data_pred]

            bitstring_to_class = {
                bit: idx for idx, bit in enumerate(sorted(data_true.unique_classes_str))
            }
            int_states_true = [bitstring_to_class[bit] for bit in str_states_true]
            int_states_pred = [bitstring_to_class[bit] for bit in str_states_pred]
            cm = confusion_matrix(int_states_true, int_states_pred)
            return cm

        else:
            y_true = data_true.all_classes.flatten()
            y_pred = data_pred.all_classes.flatten()
            cm = confusion_matrix(y_true, y_pred)
            return cm

    @staticmethod
    def accuracy(data_true: ShotCollection, data_pred: ShotCollection):
        return Metrics.__calculate_metric(calculate_accuracy, data_true, data_pred)

    @staticmethod
    def acc(data_true: ShotCollection, data_pred: ShotCollection):
        return Metrics.accuracy(data_true, data_pred)

    @staticmethod
    def fidelity(data_true: ShotCollection, data_pred: ShotCollection):
        return Metrics.__calculate_metric(calculate_fidelity, data_true, data_pred)

    @staticmethod
    def fid(data_true: ShotCollection, data_pred: ShotCollection):
        return Metrics.fidelity(data_true, data_pred)

    @staticmethod
    def recall(
        data_true: ShotCollection, data_pred: ShotCollection, averaging: str = None
    ):
        if averaging == "micro":
            return Metrics.__calculate_metric(
                calculate_micro_recall, data_true, data_pred
            )
        elif averaging == "macro":
            return Metrics.__calculate_metric(
                calculate_macro_recall, data_true, data_pred
            )
        elif averaging is None:
            return Metrics.__calculate_metric(
                calculate_binary_recall, data_true, data_pred
            )
        else:
            raise ValueError(
                "Invalid average type. Choose 'micro' or 'macro' for multiclass classification."
            )

    @staticmethod
    def rec(
        data_true: ShotCollection, data_pred: ShotCollection, averaging: str = None
    ):
        return Metrics.recall(data_true, data_pred, averaging)

    @staticmethod
    def precision(
        data_true: ShotCollection, data_pred: ShotCollection, averaging: str = None
    ):
        if averaging == "micro":
            return Metrics.__calculate_metric(
                calculate_micro_precision, data_true, data_pred
            )
        elif averaging == "macro":
            return Metrics.__calculate_metric(
                calculate_macro_precision, data_true, data_pred
            )
        elif averaging is None:
            return Metrics.__calculate_metric(
                calculate_binary_precision, data_true, data_pred
            )
        else:
            raise ValueError(
                "Invalid average type. Choose 'micro' or 'macro' for multiclass classification."
            )

    @staticmethod
    def prec(
        data_true: ShotCollection, data_pred: ShotCollection, averaging: str = None
    ):
        return Metrics.precision(data_true, data_pred, averaging)
