# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: initializedcheck=False

import numpy as np
cimport numpy as np
from scipy import sparse, signal
from libc.math cimport exp, M_PI
from cython.parallel import prange
from libc.stdlib cimport malloc, free
from libc.complex cimport complex as ccomplex

np.import_array()

ctypedef np.complex64_t DTYPE_complex64_t
ctypedef np.float64_t DTYPE_float64_t

ctypedef fused array_dims:
    np.ndarray[DTYPE_complex64_t, ndim=2]
    np.ndarray[DTYPE_complex64_t, ndim=3]

def add(array_dims array, array_dims other):
    return array + other

def sub(array_dims array, array_dims other):
    return array - other

def mul(array_dims array, array_dims other):
    return array * other

def div(array_dims array, array_dims other):
    return array / other

def mean(array_dims array, int axis):
    return np.mean(array, axis=axis, keepdims=True)

def mean_convolve(array_dims array, int kernel_size, int stride):
    cdef np.ndarray[DTYPE_float64_t, ndim=1] kernel = np.ones(kernel_size, dtype=np.float64) / kernel_size
    cdef np.ndarray[DTYPE_float64_t, ndim=3] kernel_reshaped
    
    kernel_reshaped = kernel.reshape((1, 1, -1)) if array.ndim == 3 else kernel.reshape((1, -1))
    result = signal.fftconvolve(array, kernel_reshaped, mode="valid", axes=-1)
    return result[..., ::stride]

def whittaker_eilers_smoother(array_dims array, int lamb, int d):
    """
    Optimized Whittaker smoother using numpy's vectorized operations
    """
    cdef np.ndarray[DTYPE_complex64_t, ndim=3] input_array
    cdef np.ndarray[DTYPE_complex64_t, ndim=3] result
    cdef Py_ssize_t batch_size, number_channels, signal_len
    
    input_array = array if array.ndim == 3 else array[np.newaxis, :, :]
    
    batch_size = input_array.shape[0]
    number_channels = input_array.shape[1]
    signal_len = input_array.shape[2]
    
    # Create the difference matrix using numpy operations
    D = np.eye(signal_len, dtype=np.float32)
    for _ in range(d):
        D = np.diff(D, axis=0)
    
    # Create the smoother matrix using efficient numpy operations
    DTD = D.T @ D
    smoother_matrix = np.eye(signal_len, dtype=np.float32) + lamb * DTD
    
    # Reshape input for vectorized operations
    reshaped_input = input_array.reshape(-1, signal_len)
    
    # Solve the system using numpy's optimized solver and ensure complex64 output
    solved = np.linalg.solve(smoother_matrix, reshaped_input.T)
    reshaped_result = solved.T.astype(np.complex64)
    
    # Reshape back to original dimensions
    result = reshaped_result.reshape(batch_size, number_channels, signal_len)
    
    return result[0] if array.ndim == 2 else result

def mean_centring(array_dims array, int axis=-1):
    return array - np.mean(array, axis=axis, keepdims=True)

def demodulate(array_dims array,
              np.ndarray[DTYPE_float64_t, ndim=2] intermediate_freq,
              np.ndarray[DTYPE_float64_t, ndim=2] meas_time,
              str direction):
    cdef np.ndarray[DTYPE_float64_t, ndim=2] phase
    cdef np.ndarray[DTYPE_complex64_t, ndim=2] rotation
    
    # Calculate phase as float64
    phase = 2 * M_PI * (intermediate_freq @ meas_time)
    
    # Create complex64 rotation matrix
    if direction == "clockwise":
        rotation = np.exp(-1j * phase).astype(np.complex64)
    else:
        rotation = np.exp(1j * phase).astype(np.complex64)
    
    return array * rotation
