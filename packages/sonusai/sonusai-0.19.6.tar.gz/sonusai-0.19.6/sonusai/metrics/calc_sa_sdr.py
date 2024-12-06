import numpy as np


def calc_sa_sdr(
    hypothesis: np.ndarray,
    reference: np.ndarray,
    with_scale: bool = False,
    with_negate: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
    """Calculate source-aggregated SDR (signal distortion ratio) using all source inputs which are [samples, nsrc].

    These should include a noise to be a complete mixture estimate, i.e.,
        noise_est = sum-over-all-srcs(s_est(0:nsamples, :) - sum-over-non-noisesrc(s_est(0:nsamples, n))
    should be one of the sources in reference (s_true) and hypothesis (s_est).

    Calculates -10*log10(sumn(||sn||^2) / sumn(||sn - shn||^2)
    Note: for SA method, sums are done independently on ref and error before division, vs. SDR and SI-SDR
    where sum over n is taken after divide (before log).  This is more stable in noise-only cases and also
    when some sources are poorly estimated.
    TBD: add soft-max option with eps and tau params

    Reference:
        SA-SDR: A Novel Loss Function for Separation of Meeting Style Data
        Thilo von Neumann, Keisuke Kinoshita, Christoph Boeddeker, Marc Delcroix, Reinhold Haeb-Umbach
        https://doi.org/10.48550/arXiv.2110.15581

    :param hypothesis: [samples, nsrc]
    :param reference: [samples, nsrc]
    :param with_scale: enable scaling (scaling is same as in SI-SDR)
    :param with_negate: enable negation (for use as a loss function)
    :return: (sa_sdr, opt_scale)
    """
    if with_scale:
        # calc 1 x nsrc scaling factors
        ref_energy = np.sum(reference**2, axis=0, keepdims=True)
        # if ref_energy is zero, just set scaling to 1.0
        with np.errstate(divide="ignore", invalid="ignore"):
            opt_scale = np.sum(reference * hypothesis, axis=0, keepdims=True) / ref_energy
            opt_scale[opt_scale == np.inf] = 1.0
            opt_scale = np.nan_to_num(opt_scale, nan=1.0)
        scaled_ref = opt_scale * reference
    else:
        scaled_ref = reference
        opt_scale = np.ones((1, reference.shape[1]), dtype=float)

    # multisrc sa-sdr, inputs must be [samples, nsrc]
    err = scaled_ref - hypothesis

    # -10*log10(sumk(||sk||^2) / sumk(||sk - shk||^2)
    # sum over samples and sources
    num = np.sum(reference**2)
    den = np.sum(err**2)
    if num == 0 and den == 0:
        ratio = np.inf
    else:
        ratio = num / (den + np.finfo(np.float32).eps)

    sa_sdr = 10 * np.log10(ratio)

    if with_negate:
        # for use as a loss function
        sa_sdr = -sa_sdr

    return sa_sdr, opt_scale
