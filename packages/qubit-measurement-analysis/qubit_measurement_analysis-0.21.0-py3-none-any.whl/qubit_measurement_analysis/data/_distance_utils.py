"""Utility functions for distance calculations in qubit measurement analysis."""

from typing import Any, Iterable, Literal
import numpy as np


def sspd_to(
    source: Iterable,
    other: Iterable,
    xp: Any,
    method: Literal[
        "pairwise", "cross_product", "self_cross_product"
    ] = "cross_product",
) -> np.ndarray:
    """
    Compute SSPD from source to target.

    Args:
        self_values: The values of the source.
        other: The target to compute SSPD to.
        xp: The ArrayModule instance for computation.
        method: The method to use for SSPD computation.
               'cross_product' (default): Compute full distance matrix
               'pairwise': Compute distances between corresponding pairs
               'self_cross_product': Compute upper triangular part of self-distance matrix
    """
    if method not in ["cross_product", "pairwise", "self_cross_product"]:
        raise ValueError(
            "Method must be one of: 'cross_product', 'pairwise', 'self_cross_product'"
        )

    if not hasattr(other, "qubits"):
        return _compute_sspd(source, other, xp=xp, method=method)
    else:
        if hasattr(other, "value"):
            return _compute_sspd(source, other.value, xp=xp, method=method)
        elif hasattr(other, "all_values"):
            return _compute_sspd(source, other.all_values, xp=xp, method=method)


def _compute_sspd(source, target, xp, method):
    """
    Args:
        source: array of shape (N1, ch, L1) or (ch, L1)
        target: array of shape (N2, ch, L2) or (ch, L2)
        xp: array module instance
        method: 'pairwise' or 'cross_product'
    """
    N1, ch, _ = source.shape if source.ndim == 3 else (1, *source.shape)
    N2, ch, _ = target.shape if target.ndim == 3 else (1, *target.shape)
    source_indexing = lambda idx: (slice(None), idx) if source.ndim == 3 else idx
    target_indexing = lambda idx: (slice(None), idx) if target.ndim == 3 else idx

    if method == "cross_product":
        result = np.empty((ch, N1, N2))
        for idx in range(ch):
            result[idx] = xp.sspd_cross_product(
                source[source_indexing(idx)], target[target_indexing(idx)]
            )
    elif method == "pairwise":  # pairwise
        result = np.empty((ch, N1))
        for idx in range(ch):
            result[idx] = xp.sspd_pairwise(
                source[source_indexing(idx)], target[target_indexing(idx)]
            )
    else:  # self_cross_product
        assert N1 == N2
        result = np.empty((ch, (N1 - 1) * N1 // 2))
        for idx in range(ch):
            result[idx] = xp.sspd_self_cross_product(source)

    return result
