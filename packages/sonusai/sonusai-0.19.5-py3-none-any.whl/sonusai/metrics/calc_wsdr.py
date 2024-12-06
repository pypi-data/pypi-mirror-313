import numpy as np


def calc_wsdr(
    hypothesis: np.ndarray,
    reference: np.ndarray,
    with_log: bool = False,
    with_negate: bool = False,
) -> tuple[float, np.ndarray, np.ndarray]:
    """Calculate weighted SDR (signal distortion ratio) using all source inputs of size [samples, nsrc].
       Uses true reference energy ratios to weight each cross-correlation coefficient cc = <y,yˆ>/∥y∥∥yˆ∥
       in a sum over all sources.

       range is -1 --> 1 as correlation/estimation improves or with_log -3db --> 70db (1e7 max)
       if with_negate, range is 1 --> -1 as correlation improves and with_log range 3db --> -70db (1e-7 min)

       Returns:  wsdr      scalar weighted signal-distortion ratio
                 ccoef     nsrc vector of cross correlation coefficients
                 cweights  nsrc vector of reference energy ratio weights

    Reference:
        WSDR: 2019-ICLR-dcunet-phase-aware-speech-enh

    :param hypothesis: [samples, nsrc]
    :param reference: [samples, nsrc]
    :param with_log: enable scaling (return 10*log10)
    :param with_negate: enable negation (for use as a loss function)
    :return: (wsdr, ccoef, cweights)
    """
    nsrc = reference.shape[-1]
    if hypothesis.shape[-1] != nsrc:
        raise ValueError("hypothesis has wrong shape")

    # Calculate cc = <y,yˆ>/∥y∥∥yˆ∥ always in range -1 --> 1, size [1,nsrc]
    ref_e = np.sum(reference**2, axis=0, keepdims=True)  # [1,nsrc]
    hy_e = np.sum(hypothesis**2, axis=0, keepdims=True)
    allref_e = np.sum(ref_e)
    cc = np.zeros(nsrc)  # calc correlation coefficient
    cw = np.zeros(nsrc)  # cc weights (energy ratio)
    for i in range(nsrc):
        denom = np.sqrt(ref_e[0, i]) * np.sqrt(hy_e[0, i]) + 1e-7
        cc[i] = np.sum(reference[:, i] * hypothesis[:, i], axis=0, keepdims=True) / denom
        cw[i] = ref_e[0, i] / (allref_e + 1e-7)

    # Note: tests show cw sums to 1.0 (+/- 7 digits), so just use cw for weighted sum
    if with_negate:  # for use as a loss function
        wsdr = float(np.sum(cw * -cc))  # cc always in range 1 --> -1
        if with_log:
            wsdr = max(wsdr, -1.0)
            wsdr = 10 * np.log10(wsdr + 1 + 1e-7)  # range 3 --> -inf (or 1e-7 limit of -70db)
    else:
        wsdr = float(np.sum(cw * cc))  # cc always in range -1 --> 1
        if with_log:
            wsdr = min(wsdr, 1.0)  # (np.sum(cw * cc) needs sat ==1.0 for log)
            wsdr = 10 * np.log10(-1 / (wsdr - 1 - 1e-7))  # range -3 --> inf (or 1e-7 limit of 70db)

    return float(wsdr), cc, cw
