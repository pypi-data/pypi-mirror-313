"""Array module for unified CPU/GPU array operations.

This module provides a unified interface for array operations across CPU (NumPy)
and GPU (CuPy) backends, with automatic handling of device selection and memory
management.
"""

# pylint: disable=no-name-in-module,import-error,import-outside-toplevel
import importlib.util
import numpy as np
import scipy


class Transformations:
    def __init__(self) -> None:
        self.add = None
        self.sub = None
        self.mul = None
        self.div = None
        self.mean = None
        self.mean_filter = None
        self.mean_convolve = None
        self.mean_centring = None
        self.normalize = None
        self.standardize = None
        self.demodulate = None
        self.whittaker_eilers_smoother = None


class ArrayModule:

    def __init__(self, device="cpu", use_cython=False):
        self.device = device.lower()
        self.use_cython = use_cython

        if device == "cpu":
            self.np = np
            self.scipy = scipy
            self.array_transport = self.asarray
        elif self.device.startswith("cuda"):
            assert use_cython == False

            import cupy as cp
            import cupyx.scipy

            self.np = cp
            self.scipy = cupyx.scipy
            self.array_transport = cp.asnumpy
            cuda_device = int(self.device.split(":")[1]) if ":" in self.device else 0
            cp.cuda.Device(cuda_device).use()

        else:
            raise ValueError(f"Unsupported device: {self.device}")

        self.sspd_cross_product, self.sspd_pairwise, self.sspd_self_cross_product = (
            self._get_sspd_module()
        )

        self.transformations = Transformations()
        self._get_transformations_module()

    def __getattr__(self, name):
        return getattr(self.np, name)

    def __repr__(self) -> str:
        return f"{self.device} array module with {self.np} as numpy and {self.scipy} as scipy"

    def free_all_blocks(self):
        if self.device.startswith("cuda"):
            self.get_default_memory_pool().free_all_blocks()
            self.get_default_pinned_memory_pool().free_all_blocks()

    @property
    def dtype(self):
        return self.complex64

    @property
    def _is_cython_compiled(self):
        return (
            importlib.util.find_spec("qubit_measurement_analysis.cython._sspd")
            is not None
        )

    def _get_sspd_module(self):
        if self.device == "cpu":
            if self._is_cython_compiled and self.use_cython:
                from qubit_measurement_analysis.cython import _sspd as sspd

                return sspd.cross_product, sspd.pairwise, sspd.self_cross_product
            else:
                from qubit_measurement_analysis import _sspd

                return _sspd.cross_product, _sspd.pairwise, _sspd.self_cross_product
        else:
            from qubit_measurement_analysis.cuda import sspd

            return sspd.cross_product, sspd.pairwise, sspd.self_cross_product

    def _get_transformations_module(self):
        if self._is_cython_compiled and self.use_cython:
            from qubit_measurement_analysis.cython._transformations_wrapper import (
                _add,
                _sub,
                _mul,
                _div,
                _mean,
                _mean_convolve,
                _mean_centring,
                _demodulate,
                _whittaker_eilers_smoother,
            )

            self.transformations.add = _add
            self.transformations.sub = _sub
            self.transformations.mul = _mul
            self.transformations.div = _div
            self.transformations.mean = _mean
            self.transformations.mean_convolve = _mean_convolve
            self.transformations.mean_centring = _mean_centring
            self.transformations.demodulate = _demodulate
            self.transformations.whittaker_eilers_smoother = _whittaker_eilers_smoother

        else:
            from qubit_measurement_analysis._transformations import (
                _add,
                _sub,
                _mul,
                _div,
                _mean,
                _mean_convolve,
                _mean_centring,
                _demodulate,
                _whittaker_eilers_smoother,
            )

            self.transformations.add = _add
            self.transformations.sub = _sub
            self.transformations.mul = _mul
            self.transformations.div = _div
            self.transformations.mean = _mean
            self.transformations.mean_convolve = _mean_convolve
            self.transformations.mean_centring = _mean_centring
            self.transformations.demodulate = _demodulate
            self.transformations.whittaker_eilers_smoother = _whittaker_eilers_smoother
