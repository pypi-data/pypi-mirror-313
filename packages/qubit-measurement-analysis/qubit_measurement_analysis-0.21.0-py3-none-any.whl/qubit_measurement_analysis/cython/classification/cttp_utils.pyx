"""Cython utilities for temporal post-processor implementation

@article{2310.18519,
Author = {Saeed A. Khan and Ryan Kaufman and Boris Mesits and Michael Hatridge and Hakan E. Türeci},
Title = {Practical Trainable Temporal Postprocessor for Multistate Quantum Measurement},
Year = {2023},
Eprint = {arXiv:2310.18519},
Howpublished = {PRX Quantum 5, 020364 (2024)},
Doi = {10.1103/PRXQuantum.5.020364},
}
"""

# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

import numpy as np
cimport numpy as np
from numpy import linalg as la
from libc.math cimport sqrt

# Type definitions
DTYPE = np.float32
COMPLEX_DTYPE = np.complex64
ctypedef np.float32_t DTYPE_t
ctypedef np.complex64_t COMPLEX_DTYPE_t

def prep_X(data):
    """Prepare input data for processing by splitting complex data into real and imaginary parts.
    
    Parameters
    ----------
    data : np.ndarray
        Complex input data with shape (batch, ch, len) or (ch, len)
        
    Returns
    -------
    np.ndarray
        Processed data with shape (batch, 2*len) containing concatenated real and imaginary parts
    """
    cdef np.ndarray X
    
    if len(data.shape) == 3:
        assert data.shape[1] == 1
        X = data.squeeze(1)  # (batch, len)
    else:
        assert data.shape[0] == 1
        X = data

    # Split complex data into real and imaginary parts
    return np.concatenate([X.real, X.imag], axis=-1)

def calc_state_parameters(list X_classes, double reg_lambda):
    """Calculate state parameters s and V.
    
    Parameters
    ----------
    X_classes : list
        List of arrays containing data for each class
    reg_lambda : float
        Regularization parameter
        
    Returns
    -------
    tuple
        s: State means for each class
        V: Covariance matrix
        VI: Inverse of covariance matrix
    """
    cdef:
        int C = len(X_classes)
        int NT = X_classes[0].shape[1] // 2  # Since we concatenated real/imag
        int i
        np.ndarray[DTYPE_t, ndim=2] s = np.zeros((C, 2 * NT), dtype=DTYPE)
        np.ndarray[DTYPE_t, ndim=2] V = np.zeros((2 * NT, 2 * NT), dtype=DTYPE)
        np.ndarray X_c
    
    # Calculate s and V
    for i in range(C):
        X_c = X_classes[i]
        s[i] = X_c.mean(0)
        V += np.cov(X_c, rowvar=False)
    
    # Add regularization
    V += reg_lambda * np.eye(V.shape[0], dtype=DTYPE)
    VI = la.inv(V)
    
    return s, V, VI

def calc_overlap_matrix(np.ndarray[DTYPE_t, ndim=2] s,
                       np.ndarray[DTYPE_t, ndim=2] VI):
    """Calculate state overlap matrix M.
    
    Parameters
    ----------
    s : np.ndarray
        State means for each class
    VI : np.ndarray
        Inverse of covariance matrix
        
    Returns
    -------
    np.ndarray
        Overlap matrix M
    """
    cdef:
        int C = s.shape[0]
        int c1, c2
        double Oij
        np.ndarray[DTYPE_t, ndim=2] M = np.zeros((C, C), dtype=DTYPE)
    
    for c1 in range(C):
        for c2 in range(C):
            Oij = s[c1].dot(VI.dot(s[c2]))
            M[c1, c2] = Oij + 1
            
            if c1 == c2:
                M[c1, c2] += 1
    
    return M

def calc_system_matrices(np.ndarray[DTYPE_t, ndim=2] M):
    """Calculate system matrices Q, QI, and T.
    
    Parameters
    ----------
    M : np.ndarray
        Overlap matrix
        
    Returns
    -------
    tuple
        Q: System matrix
        QI: Inverse of system matrix
        T: Diagonal bias matrix
    """
    cdef:
        int C = M.shape[0]
        int pi, c
        np.ndarray[DTYPE_t, ndim=2] Q = np.zeros((C - 1, C - 1), dtype=DTYPE)
        np.ndarray[DTYPE_t, ndim=2] T = np.zeros((C - 1, C - 1), dtype=DTYPE)
    
    # Calculate Q
    for pi in range(C - 1):
        for c in range(C - 1):
            Q[pi, c] = (M[pi, c] - M[pi + 1, c]) - (
                M[pi, -1] - M[pi + 1, -1]
            )
    QI = la.inv(Q)
    
    # Calculate T
    for pi in range(C - 1):
        T[pi, pi] = M[pi, -1] - M[pi + 1, -1]
    
    return Q, QI, T

def calc_optimal_filters(np.ndarray[DTYPE_t, ndim=2] s,
                        np.ndarray[DTYPE_t, ndim=2] VI,
                        np.ndarray[DTYPE_t, ndim=2] QI,
                        np.ndarray[DTYPE_t, ndim=2] T):
    """Calculate optimal filters and biases.
    
    Parameters
    ----------
    s : np.ndarray
        State means for each class
    VI : np.ndarray
        Inverse of covariance matrix
    QI : np.ndarray
        Inverse of system matrix
    T : np.ndarray
        Diagonal bias matrix
        
    Returns
    -------
    tuple
        f: Optimal filters
        b: Optimal biases
    """
    cdef:
        int C = s.shape[0]
        int c, p
        np.ndarray[DTYPE_t, ndim=2] Sv = np.zeros((C - 1, s.shape[1]), dtype=DTYPE)
        np.ndarray[DTYPE_t, ndim=2] f = np.zeros((C, s.shape[1]), dtype=DTYPE)
        np.ndarray[DTYPE_t, ndim=1] b = np.zeros(C, dtype=DTYPE)
    
    # Calculate pairwise filters
    for pi in range(C - 1):
        Sv[pi] = s[pi] - s[pi + 1]
    
    # Calculate optimal filters and biases
    for c in range(C):
        if c < C - 1:
            for p in range(C - 1):
                f[c] += QI[c, p] * VI.dot(Sv[p])
                b[c] -= QI[c, p] * T[p, p]
        else:
            f[c] = -np.sum(f[:-1], axis=0)
            b[c] = 1 - np.sum(b[:-1])
    
    return f, b

def predict_proba(np.ndarray X, np.ndarray f, np.ndarray b):
    """Calculate class probabilities for input data.
    
    Parameters
    ----------
    X : np.ndarray
        Input data
    f : np.ndarray
        Optimal filters
    b : np.ndarray
        Optimal biases
        
    Returns
    -------
    np.ndarray
        Class probabilities
    """
    return X.dot(f.T) + b
