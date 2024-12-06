from sonusai.mixture.datatypes import Truth
from sonusai.mixture.truth_functions.datatypes import TruthFunctionConfig
from sonusai.mixture.truth_functions.datatypes import TruthFunctionData


def _core(data: TruthFunctionData, config: TruthFunctionConfig, polar: bool) -> Truth:
    import numpy as np

    if config.target_fft.bins != config.noise_fft.bins:
        raise ValueError("Transform size mismatch for crm truth")

    frames = len(data.target_audio) // config.frame_size
    truth = np.empty((frames, config.target_fft.bins * 2), dtype=np.float32)
    for frame in range(frames):
        offset = frame * config.frame_size
        target_f = config.target_fft.execute(data.target_audio[offset : offset + config.frame_size]).astype(
            np.complex64
        )
        noise_f = config.noise_fft.execute(data.noise_audio[offset : offset + config.frame_size]).astype(np.complex64)
        mixture_f = target_f + noise_f

        crm_data = np.empty(target_f.shape, dtype=np.complex64)
        with np.nditer(target_f, flags=["multi_index"], op_flags=[["readwrite"]]) as it:
            for _ in it:
                num = target_f[it.multi_index]
                den = mixture_f[it.multi_index]
                if num == 0:
                    crm_data[it.multi_index] = 0
                elif den == 0:
                    crm_data[it.multi_index] = complex(np.inf, np.inf)
                else:
                    crm_data[it.multi_index] = num / den

        truth[frame, : config.target_fft.bins] = np.absolute(crm_data) if polar else np.real(crm_data)
        truth[frame, config.target_fft.bins :] = np.angle(crm_data) if polar else np.imag(crm_data)

    return truth


def crm_validate(_config: dict) -> None:
    pass


def crm_parameters(config: TruthFunctionConfig) -> int:
    return config.target_fft.bins * 2


def crm(data: TruthFunctionData, config: TruthFunctionConfig) -> Truth:
    """Complex ratio mask truth generation function

    Calculates the true complex ratio mask (CRM) truth which is a complex number
    per bin = Mr + j*Mi. For a given noisy STFT bin value Y, it is used as

    (Mr*Yr + Mi*Yi) / (Yr^2 + Yi^2) + j*(Mi*Yr - Mr*Yi)/ (Yr^2 + Yi^2)

    Output shape: [:, 2 * bins]
    """
    import numpy as np

    frames = config.target_fft.frames(data.target_audio)
    parameters = crm_parameters(config)
    if config.target_gain == 0:
        return np.zeros((frames, parameters), dtype=np.float32)

    return _core(data=data, config=config, polar=False)


def crmp_validate(_config: dict) -> None:
    pass


def crmp_parameters(config: TruthFunctionConfig) -> int:
    return config.target_fft.bins * 2


def crmp(data: TruthFunctionData, config: TruthFunctionConfig) -> Truth:
    """Complex ratio mask polar truth generation function

    Same as the crm function except the results are magnitude and phase
    instead of real and imaginary.

    Output shape: [:, bins]
    """
    import numpy as np

    frames = config.target_fft.frames(data.target_audio)
    parameters = crmp_parameters(config)
    if config.target_gain == 0:
        return np.zeros((frames, parameters), dtype=np.float32)

    return _core(data=data, config=config, polar=True)
