import numpy as np


def int16_to_float(x: np.ndarray) -> np.ndarray:
    """Convert int16 array to floating point with range +/- 1"""
    return x.astype(np.float32) / 32768


def float_to_int16(x: np.ndarray) -> np.ndarray:
    """Convert float point array with range +/- 1 to int16"""
    return (x * 32768).astype(np.int16)
