"""
SSPD (Symmetric Segment-Path Distance) implementation.

This module provides functions to calculate the Symmetric Segment-Path Distance
between trajectories.

Reference:
    P. Besse, B. Guillouet, J.-M. Loubes, and R. Francois,
    "Review and perspective for distance based trajectory clustering,"
    arXiv preprint arXiv:1508.04904, 2015.
"""

import numpy as np


def point_to_point(p1: np.complex64, p2: np.complex64) -> float:
    """
    Calculate the Euclidean distance between two complex points.

    Args:
        p1 (np.complex64): The first point.
        p2 (np.complex64): The second point.

    Returns:
        float: The Euclidean distance between p1 and p2.
    """
    return np.abs(p1 - p2)


def point_to_segment(
    p: np.complex64, seg_a: np.complex64, seg_b: np.complex64
) -> float:
    """
    Calculate the minimum distance from a point to a line segment.

    Args:
        p (np.complex64): The point.
        seg_a (np.complex64): The start point of the line segment.
        seg_b (np.complex64): The end point of the line segment.

    Returns:
        float: The minimum distance from the point to the line segment.
    """
    ab = seg_b - seg_a
    ap = p - seg_a

    proj_coef = np.clip(np.real((ap.conjugate() * ab) / (ab.conjugate() * ab)), 0, 1)

    closest_point = seg_a + proj_coef * ab
    return point_to_point(closest_point, p)


def point_to_trajectory(p: np.complex64, array: np.ndarray) -> float:
    """
    Calculate the minimum distance from a point to a trajectory.

    Args:
        p (np.complex64): The point.
        array (np.ndarray): The trajectory represented as an array of complex points.

    Returns:
        float: The minimum distance from the point to the trajectory.
    """
    distances = np.array(
        [point_to_segment(p, array[i], array[i + 1]) for i in range(len(array) - 1)]
    )
    return np.min(distances)


def segment_path_distance(
    trajectory: np.ndarray, target_trajectory: np.ndarray
) -> float:
    """
    Calculate the segment path distance from one trajectory to another.

    The segment path distance is the average of the minimum distances
    from each point in the first trajectory to the second trajectory.

    Args:
        trajectory (np.ndarray): The trajectory.
        target_trajectory (np.ndarray): The target trajectory.

    Returns:
        float: The segment path distance from trajectory to target_trajectory.
    """
    distances = np.array(
        [point_to_trajectory(p, target_trajectory) for p in trajectory]
    )
    return np.mean(distances)


def symmetrized_segment_path_distance(
    trajectory: np.ndarray, other_trajectory: np.ndarray
) -> float:
    """
    Calculate the symmetrized segment path distance between two trajectories.

    The symmetrized segment path distance is the average of the segment path
    distance from trajectory to other_trajectory and from other_trajectory to trajectory.

    Args:
        trajectory (np.ndarray): The first trajectory.
        other_trajectory (np.ndarray): The second trajectory.

    Returns:
        float: The symmetrized segment path distance between trajectory and other_trajectory.
    """
    spd_12 = segment_path_distance(trajectory, other_trajectory)
    spd_21 = segment_path_distance(other_trajectory, trajectory)
    return (spd_12 + spd_21) / 2


def cross_product(
    trajectories: np.ndarray, target_trajectories: np.ndarray
) -> np.ndarray:
    """
    Compute SSPD from M trajectories to N target trajectories.

    Args:
        trajectories (np.ndarray): Array of shape (M, L) containing M trajectories of length L.
        target_trajectories (np.ndarray): Array of shape (N, L) containing N target trajectories of length L.

    Returns:
        np.ndarray: Distance matrix of shape (M, N) containing SSPD between all pairs of trajectories.
    """
    if trajectories.ndim == 2:
        M = trajectories.shape[0]
    else:
        M = 1
        trajectories = trajectories.reshape(1, -1)

    if target_trajectories.ndim == 2:
        N = target_trajectories.shape[0]
    else:
        N = 1
        target_trajectories = target_trajectories.reshape(1, -1)

    result = np.zeros((M, N), dtype=np.float32)

    for i in range(M):
        for j in range(N):
            result[i, j] = symmetrized_segment_path_distance(
                trajectories[i], target_trajectories[j]
            )

    return result


def pairwise(trajectories: np.ndarray, target_trajectories: np.ndarray) -> np.ndarray:
    """
    Compute SSPD from trajectories to their corresponding target trajectories.

    Args:
        trajectories (np.ndarray): Array of shape (N, L1) containing N trajectories of length L1.
        target_trajectories (np.ndarray): Array of shape (N, L2) containing N target trajectories of length L2.

    Returns:
        np.ndarray: Array of shape (N,) containing SSPD between corresponding pairs of trajectories.
    """
    if trajectories.ndim != target_trajectories.ndim:
        raise ValueError("Trajectory sets must have the same dimensionality")

    if trajectories.ndim == 2:
        N = trajectories.shape[0]
    else:
        N = 1
        trajectories = trajectories.reshape(1, -1)

    if target_trajectories.ndim == 2:
        N_target = target_trajectories.shape[0]
    else:
        N_target = 1
        target_trajectories = target_trajectories.reshape(1, -1)

    if N != N_target:
        raise ValueError("Trajectory sets must have the same shape")

    result = np.zeros(N, dtype=np.float32)

    for i in range(N):
        result[i] = symmetrized_segment_path_distance(
            trajectories[i], target_trajectories[i]
        )

    return result


def self_cross_product(trajectories: np.ndarray) -> np.ndarray:
    """
    Compute SSPD between all pairs of trajectories, returning only the upper triangular part.

    Args:
        trajectories (np.ndarray): Array of shape (N, L) containing N trajectories of length L.

    Returns:
        np.ndarray: Flattened upper triangular part of the SSPD matrix, shape (N*(N-1)/2,).
        The vector is ordered as [d(0,1), d(0,2), ..., d(0,n-1), d(1,2), ..., d(1,n-1), ..., d(n-2,n-1)]
    """
    if trajectories.ndim == 1:
        return np.array([], dtype=np.float32)  # No pairs for single trajectory

    N = trajectories.shape[0]
    if N < 2:
        return np.array([], dtype=np.float32)  # No pairs for single trajectory

    result = np.zeros(N * (N - 1) // 2, dtype=np.float32)
    idx = 0

    for i in range(N - 1):
        for j in range(i + 1, N):
            result[idx] = symmetrized_segment_path_distance(
                trajectories[i], trajectories[j]
            )
            idx += 1

    return result
