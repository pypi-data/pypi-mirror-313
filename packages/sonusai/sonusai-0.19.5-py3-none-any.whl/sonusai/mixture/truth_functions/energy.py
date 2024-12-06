import numpy as np

from sonusai.mixture.datatypes import Truth
from sonusai.mixture.truth_functions.datatypes import TruthFunctionConfig
from sonusai.mixture.truth_functions.datatypes import TruthFunctionData


def _core(data: TruthFunctionData, config: TruthFunctionConfig, mapped: bool, snr: bool) -> Truth:
    from sonusai.utils import compute_energy_f

    target_energy = compute_energy_f(time_domain=data.target_audio, transform=config.target_fft)
    noise_energy = None
    if snr:
        noise_energy = compute_energy_f(time_domain=data.noise_audio, transform=config.noise_fft)

    frames = len(target_energy)
    truth = np.empty((frames, config.target_fft.bins), dtype=np.float32)
    for frame in range(frames):
        tmp = target_energy[frame]

        if noise_energy is not None:
            old_err = np.seterr(divide="ignore", invalid="ignore")
            tmp /= noise_energy[frame]
            np.seterr(**old_err)

        tmp = np.nan_to_num(tmp, nan=-np.inf, posinf=np.inf, neginf=-np.inf)

        if mapped:
            tmp = _calculate_mapped_snr_f(tmp, config.config["snr_db_mean"], config.config["snr_db_std"])

        truth[frame] = tmp

    return truth


def _calculate_mapped_snr_f(truth_f: np.ndarray, snr_db_mean: np.ndarray, snr_db_std: np.ndarray) -> np.ndarray:
    """Calculate mapped SNR from standard SNR energy per bin/class."""
    import scipy.special as sc

    old_err = np.seterr(divide="ignore", invalid="ignore")
    num = 10 * np.log10(np.double(truth_f)) - np.double(snr_db_mean)
    den = np.double(snr_db_std) * np.sqrt(2)
    q = num / den
    q = np.nan_to_num(q, nan=-np.inf, posinf=np.inf, neginf=-np.inf)
    result = 0.5 * (1 + sc.erf(q))
    np.seterr(**old_err)

    return result.astype(np.float32)


def energy_f_validate(_config: dict) -> None:
    pass


def energy_f_parameters(config: TruthFunctionConfig) -> int:
    return config.target_fft.bins


def energy_f(data: TruthFunctionData, config: TruthFunctionConfig) -> Truth:
    """Frequency domain energy truth generation function

    Calculates the true energy per bin:

    Ti^2 + Tr^2

    where T is the target STFT bin values.

    Output shape: [:, bins]
    """
    frames = config.target_fft.frames(data.target_audio)
    parameters = energy_f_parameters(config)
    if config.target_gain == 0:
        return np.zeros((frames, parameters), dtype=np.float32)

    return _core(data=data, config=config, mapped=False, snr=False)


def snr_f_validate(_config: dict) -> None:
    pass


def snr_f_parameters(config: TruthFunctionConfig) -> int:
    return config.target_fft.bins


def snr_f(data: TruthFunctionData, config: TruthFunctionConfig) -> Truth:
    """Frequency domain SNR truth function documentation

    Calculates the true SNR per bin:

    (Ti^2 + Tr^2) / (Ni^2 + Nr^2)

    where T is the target and N is the noise STFT bin values.

    Output shape: [:, bins]
    """
    frames = config.target_fft.frames(data.target_audio)
    parameters = snr_f_parameters(config)
    if config.target_gain == 0:
        return np.zeros((frames, parameters), dtype=np.float32)

    return _core(data=data, config=config, mapped=False, snr=True)


def mapped_snr_f_validate(config: TruthFunctionConfig) -> None:
    if len(config.config) == 0:
        raise AttributeError("mapped_snr_f truth function is missing config")

    for parameter in ("snr_db_mean", "snr_db_std"):
        if parameter not in config.config:
            raise AttributeError(f"mapped_snr_f truth function is missing required '{parameter}'")

        if len(config.config[parameter]) != config.target_fft.bins:
            raise ValueError(
                f"mapped_snr_f truth function '{parameter}' does not have {config.target_fft.bins} elements"
            )


def mapped_snr_f_parameters(config: TruthFunctionConfig) -> int:
    return config.target_fft.bins


def mapped_snr_f(data: TruthFunctionData, config: TruthFunctionConfig) -> Truth:
    """Frequency domain mapped SNR truth function documentation

    Output shape: [:, bins]
    """
    frames = config.target_fft.frames(data.target_audio)
    parameters = mapped_snr_f_parameters(config)
    if config.target_gain == 0:
        return np.zeros((frames, parameters), dtype=np.float32)

    return _core(data=data, config=config, mapped=True, snr=True)


def energy_t_validate(_config: dict) -> None:
    pass


def energy_t_parameters(_config: TruthFunctionConfig) -> int:
    return 1


def energy_t(data: TruthFunctionData, config: TruthFunctionConfig) -> Truth:
    """Time domain energy truth function documentation

    Calculates the true time domain energy of each frame:

    For OLS:
        sum(x[0:N-1]^2) / N

    For OLA:
        sum(x[0:R-1]^2) / R

    where x is the target time domain data,
    N is the size of the transform, and
    R is the number of new samples in the frame.

    Output shape: [:, 1]

    Note: feature transforms can be defined to use a subset of all bins,
    i.e., subset of 0:128 for N=256 could be 0:127 or 1:128. energy_t
    will reflect the total energy over all bins regardless of the feature
    transform config.
    """
    import torch

    frames = config.target_fft.frames(data.target_audio)
    parameters = energy_t_parameters(config)
    if config.target_gain == 0:
        return np.zeros((frames, parameters), dtype=np.float32)

    return config.target_fft.execute_all(torch.from_numpy(data.target_audio))[1].numpy()
