from sonusai.mixture.datatypes import AudioF
from sonusai.mixture.datatypes import Truth
from sonusai.mixture.truth_functions.datatypes import TruthFunctionConfig
from sonusai.mixture.truth_functions.datatypes import TruthFunctionData


def target_f_validate(_config: dict) -> None:
    pass


def target_f_parameters(config: TruthFunctionConfig) -> int:
    if config.ttype == "tdac-co":
        return config.target_fft.bins

    return config.target_fft.bins * 2


def target_f(data: TruthFunctionData, config: TruthFunctionConfig) -> Truth:
    """Frequency domain target truth function

    Calculates the true transform of the target using the STFT
    configuration defined by the feature. This will include a
    forward transform window if defined by the feature.

    Output shape: [:, 2 * bins] (target stacked real, imag) or
                  [:, bins] (target real only for tdac-co)
    """
    import torch

    target_freq = config.target_fft.execute_all(torch.from_numpy(data.target_audio))[0].numpy()
    return _stack_real_imag(target_freq, config.ttype)


def target_mixture_f_validate(_config: dict) -> None:
    pass


def target_mixture_f_parameters(config: TruthFunctionConfig) -> int:
    if config.ttype == "tdac-co":
        return config.target_fft.bins * 2

    return config.target_fft.bins * 4


def target_mixture_f(data: TruthFunctionData, config: TruthFunctionConfig) -> Truth:
    """Frequency domain target and mixture truth function

    Calculates the true transform of the target and the mixture
    using the STFT configuration defined by the feature. This
    will include a forward transform window if defined by the
    feature.

    Output shape: [:, 4 * bins] (target stacked real, imag; mixture stacked real, imag) or
                  [:, 2 * bins] (target real; mixture real for tdac-co)
    """
    import numpy as np
    import torch

    target_freq = config.target_fft.execute_all(torch.from_numpy(data.target_audio))[0].numpy()
    mixture_freq = config.mixture_fft.execute_all(torch.from_numpy(data.mixture_audio))[0].numpy()

    frames, bins = target_freq.shape
    truth = np.empty((frames, bins * 4), dtype=np.float32)
    truth[:, : bins * 2] = _stack_real_imag(target_freq, config.ttype)
    truth[:, bins * 2 :] = _stack_real_imag(mixture_freq, config.ttype)
    return truth


def target_swin_f_validate(_config: dict) -> None:
    pass


def target_swin_f_parameters(config: TruthFunctionConfig) -> int:
    return config.target_fft.bins * 2


def target_swin_f(data: TruthFunctionData, config: TruthFunctionConfig) -> Truth:
    """Frequency domain target with synthesis window truth function

    Calculates the true transform of the target using the STFT
    configuration defined by the feature. This will include a
    forward transform window if defined by the feature and also
    the inverse transform (or synthesis) window.

    Output shape: [:, 2 * bins] (stacked real, imag)
    """
    import numpy as np

    from sonusai.utils import stack_complex

    truth = np.empty((len(data.target_audio) // config.frame_size, config.target_fft.bins * 2), dtype=np.float32)
    for idx, offset in enumerate(range(0, len(data.target_audio), config.frame_size)):
        target_freq = config.target_fft.execute(
            np.multiply(data.target_audio[offset : offset + config.frame_size], config.swin)
        )[0]
        truth[idx] = stack_complex(target_freq)

    return truth


def _stack_real_imag(data: AudioF, ttype: str) -> Truth:
    import numpy as np

    from sonusai.utils import stack_complex

    if ttype == "tdac-co":
        return np.real(data)

    return stack_complex(data)
