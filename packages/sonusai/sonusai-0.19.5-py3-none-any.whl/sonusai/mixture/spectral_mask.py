from sonusai.mixture.datatypes import AudioF
from sonusai.mixture.datatypes import SpectralMask


def apply_spectral_mask(audio_f: AudioF, spectral_mask: SpectralMask, seed: int | None = None) -> AudioF:
    """Apply frequency and time masking

    Implementation of SpecAugment: A Simple Data Augmentation Method for Automatic Speech Recognition

    Ref: https://arxiv.org/pdf/1904.08779.pdf

    f_width consecutive bins [f_start, f_start + f_width) are masked, where f_width is chosen from a uniform
    distribution from 0 to the f_max_width, and f_start is chosen from [0, bins - f_width).

    t_width consecutive frames [t_start, t_start + t_width) are masked, where t_width is chosen from a uniform
    distribution from 0 to the t_max_width, and t_start is chosen from [0, frames - t_width).

    A time mask cannot be wider than t_max_percent times the number of frames.

    :param audio_f: Numpy array of transform audio data [frames, bins]
    :param spectral_mask: Spectral mask parameters
    :param seed: Random number seed
    :return: Augmented feature
    """
    import numpy as np

    if audio_f.ndim != 2:
        raise ValueError("feature input must have three dimensions [frames, bins]")

    frames, bins = audio_f.shape

    f_max_width = spectral_mask.f_max_width
    if f_max_width not in range(0, bins + 1):
        f_max_width = bins

    rng = np.random.default_rng(seed)

    # apply f_num frequency masks to the feature
    for _ in range(spectral_mask.f_num):
        f_width = int(rng.uniform(0, f_max_width))
        f_start = rng.integers(0, bins - f_width, endpoint=True)
        audio_f[:, f_start : f_start + f_width] = 0

    # apply t_num time masks to the feature
    t_upper_bound = int(spectral_mask.t_max_percent / 100 * frames)
    for _ in range(spectral_mask.t_num):
        t_width = min(int(rng.uniform(0, spectral_mask.t_max_width)), t_upper_bound)
        t_start = rng.integers(0, frames - t_width, endpoint=True)
        audio_f[t_start : t_start + t_width, :] = 0

    return audio_f
