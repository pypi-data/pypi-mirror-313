def _add(array, other):
    return array + other


def _sub(array, other):
    return array - other


def _mul(array, other):
    return array * other


def _div(array, other):
    return array / other


def _mean(array, axis):
    # array: np.complex64, shape (ch, len) or (batch, ch, len)
    # axis: int
    return array.mean(axis, keepdims=True)


def _mean_convolve(array, kernel_size, stride, module):
    # array: np.complex64, shape (ch, len) or (batch, ch, len)
    # kernel_size: int
    # stride: int
    # module: numpy
    kernel = module.np.ones(kernel_size) / kernel_size
    kernel = kernel.reshape(1, 1, -1) if array.ndim == 3 else kernel.reshape(1, -1)
    return module.scipy.signal.fftconvolve(array, kernel, mode="valid", axes=-1)[
        ..., ::stride
    ]


def _whittaker_eilers_smoother(array, lamb, d, module):
    # array: np.complex64, shape (ch, len) or (batch, ch, len)
    # lamb: int
    # d: int
    # module: numpy

    # Handle different input shapes
    if array.ndim == 2:
        array = array[module.newaxis, :, :]  # Reshape to (1, number_channels, len)

    batch_size, number_channels, signal_len = array.shape

    # Create the difference matrix (D)
    D = module.scipy.sparse.eye(signal_len, format="csc")
    for _ in range(d):
        D = D[1:] - D[:-1]

    # Regularization matrix (penalizing large differences in the second derivative)
    DTD = D.T @ D

    # Construct the smoother matrix (I + λ * D^T * D)
    smoother_matrix = module.scipy.sparse.eye(signal_len, format="csc") + lamb * DTD

    # Make sure it's in the right format (sparse)
    smoother_matrix = smoother_matrix.tocsc()

    # Solve for each signal in the batch and each channel
    smoothed_signals = module.zeros_like(array)
    for i in range(batch_size):
        for j in range(number_channels):
            smoothed_signals[i, j] = module.scipy.sparse.linalg.spsolve(
                smoother_matrix, array[i, j]
            )

    if array.shape[0] == 1:  # No batch input, just multiple channels
        return smoothed_signals[0]
    return smoothed_signals


def _mean_centring(array, axis=-1):
    # array: np.complex64, shape (ch, len) or (batch, ch, len)
    return array - array.mean(axis=axis, keepdims=True)


def _demodulate(array, intermediate_freq, meas_time, direction, module):
    # array: np.complex64, shape (1, len) or (batch, 1, len)
    # intermediate_freq: np.float64, shape (ch, len)
    # meas_time: np.float64, shape (1, len)
    # direction: str, "clockwise" or other
    # module: numpy

    # Calculate phase using broadcasting
    phase = 2 * module.pi * intermediate_freq @ meas_time
    # Calculate rotation using broadcasting
    rotation = (
        module.exp(-1j * phase) if direction == "clockwise" else module.exp(1j * phase)
    )
    # Perform the rotation on the array
    demodulated = array * rotation
    return demodulated
