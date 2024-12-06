"""NumPy implementation of the TensorTree library
"""

import numpy as np

from .core import General_Impl


class NP_Impl(General_Impl):
    """Specialized numpy operations"""

    def __init__(self):
        super().__init__(np, "axis")

    @staticmethod
    def zeros(*args, **kwargs) -> np.array:
        return np.zeros(*args, **kwargs)

    @staticmethod
    def ones(*args, **kwargs) -> np.array:
        return np.ones(*args, **kwargs)

    @staticmethod
    def copy(data: np.array) -> np.array:
        return np.copy(data)

    @staticmethod
    def shape(data: np.array) -> np.array:
        return data.shape

    @staticmethod
    def to_numpy(data: np.array) -> np.array:
        return data

    @staticmethod
    def array(*args, **kwargs) -> np.array:
        return np.array(*args, **kwargs)

    @staticmethod
    def masked_array(data, mask, *args, **kwargs) -> np.array:
        return np.ma.masked_array(data, mask, *args, **kwargs)

    @staticmethod
    def mean(data: np.ndarray, axis) -> np.ndarray:
        return data.mean(axis)

    @staticmethod
    def all(data: np.ndarray, axis) -> np.ndarray:
        return np.all(data, axis)

    @staticmethod
    def any(data: np.ndarray, axis) -> np.ndarray:
        return np.any(data, axis)

    @staticmethod
    def repeat(data: np.ndarray, *args, **kwargs) -> np.ndarray:
        return np.repeat(data, *args, **kwargs)
