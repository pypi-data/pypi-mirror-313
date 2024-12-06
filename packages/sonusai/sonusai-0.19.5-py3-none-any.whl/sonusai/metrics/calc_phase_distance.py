import numpy as np


def calc_phase_distance(
    reference: np.ndarray, hypothesis: np.ndarray, eps: float = 1e-9
) -> tuple[float, np.ndarray, np.ndarray]:
    """Calculate weighted phase distance error (weight normalization over bins per frame)

    :param reference: complex [frames, bins]
    :param hypothesis: complex [frames, bins]
    :param eps: epsilon value
    :return: mean, mean per bin, mean per frame
    """
    ang_diff = np.angle(reference) - np.angle(hypothesis)
    phd_mod = (ang_diff + np.pi) % (2 * np.pi) - np.pi
    rh_angle_diff = phd_mod * 180 / np.pi  # angle diff in deg

    # Use complex divide to intrinsically keep angle diff +/-180 deg, but avoid div by zero (real hyp)
    # hyp_real = np.real(hypothesis)
    # near_zeros = np.real(hyp_real) < eps
    # hyp_real = hyp_real * (np.logical_not(near_zeros))
    # hyp_real = hyp_real + (near_zeros * eps)
    # hypothesis = hyp_real + 1j*np.imag(hypothesis)
    # rh_angle_diff = np.angle(reference / hypothesis) * 180 / np.pi  # angle diff +/-180

    # weighted mean over all (scalar)
    reference_mag = np.abs(reference)
    ref_weight = reference_mag / (np.sum(reference_mag) + eps)  # frames x bins
    err = np.around(np.sum(ref_weight * rh_angle_diff), 3)

    # weighted mean over frames (value per bin)
    err_b = np.zeros(reference.shape[1])
    for bi in range(reference.shape[1]):
        ref_weight = reference_mag[:, bi] / (np.sum(reference_mag[:, bi], axis=0) + eps)
        err_b[bi] = np.around(np.sum(ref_weight * rh_angle_diff[:, bi]), 3)

    # weighted mean over bins (value per frame)
    err_f = np.zeros(reference.shape[0])
    for fi in range(reference.shape[0]):
        ref_weight = reference_mag[fi, :] / (np.sum(reference_mag[fi, :]) + eps)
        err_f[fi] = np.around(np.sum(ref_weight * rh_angle_diff[fi, :]), 3)

    return err, err_b, err_f
