"Module for calculating SSPD between trajectories using CUDA"

import os
import cupy as cp
from qubit_measurement_analysis.cuda.spd import (
    pairwise as pairwise_spd,
    cross_product as cross_product_spd,
)

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load and compile the self pairwise kernel
with open(os.path.join(current_dir, "_sspd_self_pairwise_kernel.cu"), "r") as f:
    cuda_code = f.read()

# Compile the kernel
kernel_module = cp.RawModule(
    code=cuda_code, translate_cucomplex=True, options=("-std=c++17",)
)

# Get kernel function
_sspd_self_pairwise = kernel_module.get_function("sspd_self_pairwise")


def pairwise(trajectories, other_trajectories):
    """
    Computes SSPD from trajectories to their corresponding other trajectories
    """
    spd_12 = pairwise_spd(trajectories, other_trajectories)
    spd_21 = pairwise_spd(other_trajectories, trajectories)
    return (spd_12 + spd_21) / 2


def cross_product(trajectories, other_trajectories):
    """
    Computes SSPD from M trajectories to N other trajectories.
    Returns (M, N) distance matrix
    """
    spd_12 = cross_product_spd(trajectories, other_trajectories)
    spd_21 = cross_product_spd(other_trajectories, trajectories)
    return (spd_12 + spd_21.T) / 2


def self_cross_product(trajectories):
    """
    Computes SSPD between all pairs of trajectories, returning only the upper triangular part.

    Args:
        trajectories: Array of shape (N, L) containing N trajectories of length L.

    Returns:
        Flattened upper triangular part of the SSPD matrix, shape (N*(N-1)/2,).
        The vector is ordered as [d(0,1), d(0,2), ..., d(0,n-1), d(1,2), ..., d(1,n-1), ..., d(n-2,n-1)]
    """
    num_trajectories = trajectories.shape[0] if trajectories.ndim > 1 else 1
    traj_len = trajectories.shape[-1]
    num_pairs = (num_trajectories * (num_trajectories - 1)) // 2

    try:
        # Allocate output array and initialize to zero
        d_results = cp.zeros(num_pairs, dtype=cp.float32)

        # Calculate grid and block dimensions
        threads_per_block = 992  # must be divisible by 32
        blocks_per_grid = num_pairs

        # Launch kernel
        _sspd_self_pairwise(
            (blocks_per_grid,),
            (threads_per_block,),
            (
                trajectories,
                num_trajectories,
                traj_len,
                d_results,
            ),
        )

        return cp.asnumpy(d_results)

    finally:
        # Ensure memory is freed even if an error occurs
        cp.get_default_memory_pool().free_all_blocks()
        cp.get_default_pinned_memory_pool().free_all_blocks()
