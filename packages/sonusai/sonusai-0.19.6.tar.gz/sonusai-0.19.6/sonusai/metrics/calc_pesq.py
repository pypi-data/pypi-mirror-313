import numpy as np

from sonusai.mixture.constants import SAMPLE_RATE


def calc_pesq(
    hypothesis: np.ndarray,
    reference: np.ndarray,
    error_value: float = 0.0,
    sample_rate: int = SAMPLE_RATE,
) -> float:
    """Computes the PESQ score of hypothesis vs. reference

    Upon error, assigns a value of 0, or user specified value in error_value

    :param hypothesis: estimated audio
    :param reference: reference audio
    :param error_value: value to use if error occurs
    :param sample_rate: sample rate of audio
    :return: value between -0.5 to 4.5
    """
    import warnings

    from pesq import pesq

    from sonusai import logger

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            score = pesq(fs=sample_rate, ref=reference, deg=hypothesis, mode="wb")
    except Exception as e:
        logger.debug(f"PESQ error {e}")
        score = error_value

    return score
