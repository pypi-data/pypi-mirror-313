from qubit_measurement_analysis.cython._transformations import (
    add,
    sub,
    mul,
    div,
    mean,
    mean_convolve,
    mean_centring,
    demodulate,
    whittaker_eilers_smoother,
)


def _add(array, other):
    return add(array, other)


def _sub(array, other):
    return sub(array, other)


def _mul(array, other):
    return mul(array, other)


def _div(array, other):
    return div(array, other)


def _mean(array, axis):
    return mean(array, axis)


def _mean_convolve(array, kernel_size, stride, module):
    return mean_convolve(array, kernel_size, stride)


def _whittaker_eilers_smoother(array, lamb, d, module):
    return whittaker_eilers_smoother(array, lamb, d)


def _mean_centring(array, axis=-1):
    return mean_centring(array, axis)


def _demodulate(array, intermediate_freq, meas_time, direction, module):
    return demodulate(array, intermediate_freq, meas_time, direction)
