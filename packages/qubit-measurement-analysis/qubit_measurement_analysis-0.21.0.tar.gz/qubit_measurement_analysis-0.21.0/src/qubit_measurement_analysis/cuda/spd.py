"Module for calculating SPD between trajectories using CUDA"

import os
import cupy as cp

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the CUDA kernel
with open(os.path.join(current_dir, "_spd_kernels.cu"), "r") as f:
    cuda_code = f.read()

# Compile the kernel
kernel_module = cp.RawModule(
    code=cuda_code, translate_cucomplex=True, options=("-std=c++17",)
)

# Get kernel functions
_spd_cross_product = kernel_module.get_function("spd_cross_product")
_spd_pairwise = kernel_module.get_function("spd_pairwise")


def cross_product(trajectories, target_trajectories):
    """
    Computes SPD from M trajectories to N target trajectories.
    Returns (M, N) distance matrix
    trajectories: 2d cupy array with M trajectories
    target_trajectories: 2d cupy array with N trajectories
    """
    traj_len = trajectories.shape[-1]
    num_trajectories = trajectories.shape[0] if trajectories.ndim > 1 else 1
    num_targets = target_trajectories.shape[0] if target_trajectories.ndim > 1 else 1

    # Allocate output array
    d_results = cp.zeros((num_trajectories, num_targets), dtype=cp.float32)

    # Calculate grid and block dimensions
    threads_per_block = 1024  # must be divisible by 32 (better to be eq to data len)
    grid_dim = (num_trajectories, num_targets, 1)

    # Launch kernel
    _spd_cross_product(
        grid_dim,
        (threads_per_block,),
        (
            target_trajectories,
            num_targets,
            trajectories,
            num_trajectories,
            traj_len,
            d_results,
        ),
    )

    # Free memory
    free_gpu_memory()
    return cp.asnumpy(d_results)


def pairwise(trajectories, target_trajectories):
    """
    Computes SPD from trajectories to their corresponding target trajectories
    """
    assert (
        trajectories.shape == target_trajectories.shape
    ), "Trajectory sets must have the same shape"

    traj_len = trajectories.shape[-1]
    num_trajectories = trajectories.shape[0] if trajectories.ndim > 1 else 1

    # Allocate output array
    d_results = cp.zeros(num_trajectories, dtype=cp.float32)

    # Calculate grid and block dimensions
    threads_per_block = 1024  # must be divisible by 32 (better to be eq to data len)
    blocks_per_grid = num_trajectories

    # Launch kernel
    _spd_pairwise(
        (blocks_per_grid,),
        (threads_per_block,),
        (
            target_trajectories,
            trajectories,
            num_trajectories,
            traj_len,
            d_results,
        ),
    )

    # Free memory
    free_gpu_memory()
    return cp.asnumpy(d_results)


def free_gpu_memory():
    "Helper function to free GPU memory"
    cp.get_default_memory_pool().free_all_blocks()
    cp.get_default_pinned_memory_pool().free_all_blocks()
