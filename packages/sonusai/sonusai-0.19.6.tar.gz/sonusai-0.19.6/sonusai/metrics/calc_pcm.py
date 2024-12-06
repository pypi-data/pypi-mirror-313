import numpy as np


def calc_pcm(
    hypothesis: np.ndarray, reference: np.ndarray, with_log: bool = False
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate phase constrained magnitude error

    These must include a noise to make a complete mixture estimate, i.e.,
        noise_est = mixture - sum-over-nsrc(s_est(:, nsrc, :))
    should be one of the sources in s_true and s_est.

    Calculates mean-over-srcs(mean-over-tf(| (|Sr(t, f)| + |Si(t, f)|) - (|Shr(t, f)| + |Shi(t, f)|) |))

    Reference:
        Self-attending RNN for Speech Enhancement to Improve Cross-corpus Generalization
        Ashutosh Pandey, Student Member, IEEE and DeLiang Wang, Fellow, IEEE
        https://doi.org/10.48550/arXiv.2105.12831

    :param hypothesis: complex [frames, nsrc, bins]
    :param reference: complex [frames, nsrc, bins]
    :param with_log: enable log
    :return: (error, error per bin, error per frame)
    """
    # LSM = 1/(T*F) * sumtf(| (|Sr(t, f)| + |Si(t, f)|) - (|Shr(t, f)| + |Shi(t, f)|) |)
    # LPCM = 1/2 * LSM(s, sh) + 1/2 * LSM(n, nh)

    # [frames, nsrc, bins]
    hypothesis_abs = np.abs(np.real(hypothesis)) + np.abs(np.imag(hypothesis))
    reference_abs = np.abs(np.real(reference)) + np.abs(np.imag(reference))
    err = np.abs(reference_abs - hypothesis_abs)

    # mean over frames, nsrc for value per bin
    err_b = np.mean(np.mean(err, axis=0), axis=0)
    # mean over bins, nsrc for value per frame
    err_f = np.mean(np.mean(err, axis=2), axis=1)
    # mean over bins and frames, nsrc for scalar value
    err = np.mean(np.mean(err, axis=(0, 2)), axis=0)

    if with_log:
        err_b = np.around(20 * np.log10(err_b + np.finfo(np.float32).eps), 3)
        err_f = np.around(20 * np.log10(err_f + np.finfo(np.float32).eps), 3)
        err = np.around(20 * np.log10(err + np.finfo(np.float32).eps), 3)

    return err, err_b, err_f
