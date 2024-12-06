import numpy as np

from sonusai.mixture.datatypes import AudioF
from sonusai.mixture.datatypes import Segsnr
from sonusai.mixture.datatypes import SnrFBinMetrics
from sonusai.mixture.datatypes import SnrFMetrics


def calc_segsnr_f(segsnr_f: Segsnr) -> SnrFMetrics:
    """Calculate metrics of snr_f truth data.

    Includes mean and standard deviation of the linear values (usually energy)
    and mean and standard deviation of the dB values (10 * log10).
    """
    if np.count_nonzero(segsnr_f) == 0:
        # If all entries are zeros
        return SnrFMetrics(0, 0, -np.inf, 0)

    tmp = np.ma.array(segsnr_f, mask=np.logical_not(np.isfinite(segsnr_f)))
    if np.ma.count_masked(tmp) == np.ma.size(tmp, axis=0):
        # If all entries are infinite
        return SnrFMetrics(np.inf, 0, np.inf, 0)

    snr_mean = np.mean(tmp, axis=0)
    snr_std = np.std(tmp, axis=0)

    tmp = 10 * np.ma.log10(tmp)
    if np.ma.count_masked(tmp) == np.ma.size(tmp, axis=0):
        # If all entries are masked, special case where all inputs are either 0 or infinite
        snr_db_mean = -np.inf
        snr_db_std = np.inf
    else:
        snr_db_mean = np.mean(tmp, axis=0)
        snr_db_std = np.std(tmp, axis=0)

    return SnrFMetrics(snr_mean, snr_std, snr_db_mean, snr_db_std)


def calc_segsnr_f_bin(target_f: AudioF, noise_f: AudioF) -> SnrFBinMetrics:
    """Calculate per-bin segmental SNR metrics.

    Includes per-bin mean and standard deviation of the linear values
    and mean and standard deviation of the dB values.
    """
    if target_f.ndim != 2 and noise_f.ndim != 2:
        raise ValueError("target_f and noise_f must have 2 dimensions")

    segsnr_f = (np.abs(target_f) ** 2) / (np.abs(noise_f) ** 2 + np.finfo(np.float32).eps)

    frames, bins = segsnr_f.shape
    if np.count_nonzero(segsnr_f) == 0:
        # If all entries are zeros
        return SnrFBinMetrics(np.zeros(bins), np.zeros(bins), -np.inf * np.ones(bins), np.zeros(bins))

    tmp = np.ma.array(segsnr_f, mask=np.logical_not(np.isfinite(segsnr_f)))
    if np.ma.count_masked(tmp) == np.ma.size(tmp, axis=0):
        # If all entries are infinite
        return SnrFBinMetrics(
            np.inf * np.ones(bins),
            np.zeros(bins),
            np.inf * np.ones(bins),
            np.zeros(bins),
        )

    snr_mean = np.mean(tmp, axis=0)
    snr_std = np.std(tmp, axis=0)

    tmp = 10 * np.ma.log10(tmp)
    if np.ma.count_masked(tmp) == np.ma.size(tmp, axis=0):
        # If all entries are masked, special case where all inputs are either 0 or infinite
        snr_db_mean = -np.inf * np.ones(bins)
        snr_db_std = np.inf * np.ones(bins)
    else:
        snr_db_mean = np.mean(tmp, axis=0)
        snr_db_std = np.std(tmp, axis=0)

    return SnrFBinMetrics(
        np.ma.getdata(snr_mean),
        np.ma.getdata(snr_std),
        np.ma.getdata(snr_db_mean),
        np.ma.getdata(snr_db_std),
    )
