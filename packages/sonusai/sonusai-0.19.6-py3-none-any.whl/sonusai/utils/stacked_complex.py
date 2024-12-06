import numpy as np


def stack_complex(unstacked: np.ndarray) -> np.ndarray:
    """Stack a complex array

    A stacked array doubles the last dimension and organizes the data as:
        - first half is all the real data
        - second half is all the imaginary data

    :param unstacked: An nD array (n > 1) containing complex data
    :return: A stacked array
    :raises TypeError:
    """
    if not unstacked.ndim > 1:
        raise ValueError("unstacked must have more than 1 dimension")

    shape = list(unstacked.shape)
    shape[-1] = shape[-1] * 2
    stacked = np.empty(shape, dtype=np.float32)
    half = unstacked.shape[-1]
    stacked[..., :half] = np.real(unstacked)
    stacked[..., half:] = np.imag(unstacked)

    return stacked


def unstack_complex(stacked: np.ndarray) -> np.ndarray:
    """Unstack a stacked complex array

    :param stacked: An nD array (n > 1) where the last dimension contains stacked complex data in which the first half
        is all the real data and the second half is all the imaginary data
    :return: An unstacked complex array
    :raises TypeError:
    """
    if not stacked.ndim > 1:
        raise ValueError("stacked must have more than 1 dimension")

    if stacked.shape[-1] % 2 != 0:
        raise ValueError("last dimension of stacked must be a multiple of 2")

    half = stacked.shape[-1] // 2
    unstacked = 1j * stacked[..., half:]
    unstacked += stacked[..., :half]

    return unstacked


def stacked_complex_real(stacked: np.ndarray) -> np.ndarray:
    """Get the real elements from a stacked complex array

    :param stacked: An nD array (n > 1) where the last dimension contains stacked complex data in which the first half
        is all the real data and the second half is all the imaginary data
    :return: The real elements
    :raises TypeError:
    """
    if not stacked.ndim > 1:
        raise ValueError("stacked must have more than 1 dimension")

    if stacked.shape[-1] % 2 != 0:
        raise ValueError("last dimension of stacked must be a multiple of 2")

    half = stacked.shape[-1] // 2
    return stacked[..., :half]


def stacked_complex_imag(stacked: np.ndarray) -> np.ndarray:
    """Get the imaginary elements from a stacked complex array

    :param stacked: An nD array (n > 1) where the last dimension contains stacked complex data in which the first half
        is all the real data and the second half is all the imaginary data
    :return: The imaginary elements
    :raises TypeError:
    """
    if not stacked.ndim > 1:
        raise ValueError("stacked must have more than 1 dimension")

    if stacked.shape[-1] % 2 != 0:
        raise ValueError("last dimension of stacked must be a multiple of 2")

    half = stacked.shape[-1] // 2
    return stacked[..., half:]
