def linear_to_db(linear: float) -> float:
    """Convert linear value to dB value
    :param linear: Linear value
    :return: dB value
    """
    import numpy as np

    return 20 * np.log10(abs(linear))


def db_to_linear(db: float) -> float:
    """Convert dB value to linear value
    :param db: dB value
    :return: Linear value
    """
    return 10 ** (db / 20)
