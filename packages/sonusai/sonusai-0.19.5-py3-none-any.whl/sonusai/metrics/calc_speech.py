import numpy as np

from sonusai.mixture.constants import SAMPLE_RATE
from sonusai.mixture.datatypes import SpeechMetrics

from .calc_pesq import calc_pesq


def calc_speech(hypothesis: np.ndarray, reference: np.ndarray, sample_rate: int = SAMPLE_RATE) -> SpeechMetrics:
    """Calculate speech metrics pesq, c_sig, c_bak, and c_ovl.

    These are all related and thus included in one function. Reference: matlab script "compute_metrics.m".

    :param hypothesis: estimated audio
    :param reference: reference audio
    :param sample_rate: sample rate of audio
    :return: SpeechMetrics named tuple
    """

    # Weighted spectral slope measure
    wss_dist_vec = _calc_weighted_spectral_slope_measure(hypothesis=hypothesis, reference=reference)
    wss_dist_vec = np.sort(wss_dist_vec)

    # Value from CMGAN reference implementation
    alpha = 0.95
    wss_dist = np.mean(wss_dist_vec[0 : round(np.size(wss_dist_vec) * alpha)])

    # Log likelihood ratio measure
    llr_dist = _calc_log_likelihood_ratio_measure(hypothesis=hypothesis, reference=reference, sample_rate=sample_rate)
    ll_rs = np.sort(llr_dist)
    llr_len = round(np.size(llr_dist) * alpha)
    llr_mean = np.mean(ll_rs[:llr_len])

    # Segmental SNR
    snr_dist, segsnr_dist = _calc_snr(hypothesis=hypothesis, reference=reference, sample_rate=sample_rate)
    seg_snr = np.mean(segsnr_dist)

    # PESQ
    _pesq = calc_pesq(hypothesis=hypothesis, reference=reference, sample_rate=sample_rate)

    # Now compute the composite measures
    csig = np.clip(3.093 - 1.029 * llr_mean + 0.603 * _pesq - 0.009 * wss_dist, 1, 5)
    cbak = np.clip(1.634 + 0.478 * _pesq - 0.007 * wss_dist + 0.063 * seg_snr, 1, 5)
    covl = np.clip(1.594 + 0.805 * _pesq - 0.512 * llr_mean - 0.007 * wss_dist, 1, 5)

    return SpeechMetrics(_pesq, csig, cbak, covl)


def _calc_weighted_spectral_slope_measure(
    hypothesis: np.ndarray, reference: np.ndarray, sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    from scipy.fftpack import fft

    # The lengths of the reference and hypothesis must be the same.
    reference_length = np.size(reference)
    hypothesis_length = np.size(hypothesis)
    if reference_length != hypothesis_length:
        raise ValueError("Hypothesis and reference must be the same length.")

    # Window length in samples
    win_length = int(np.round(30 * sample_rate / 1000))
    # Window skip in samples
    skip_rate = int(np.floor(np.divide(win_length, 4)))
    # Maximum bandwidth
    max_freq = int(np.divide(sample_rate, 2))
    num_crit = 25

    n_fft = int(np.power(2, np.ceil(np.log2(2 * win_length))))
    n_fft_by_2 = int(np.multiply(0.5, n_fft))
    # Value suggested by Klatt, pg 1280
    k_max = 20.0
    # Value suggested by Klatt, pg 1280
    k_loc_max = 1.0

    # Critical band filter definitions (center frequency and bandwidths in Hz)
    cent_freq = np.array(
        [
            50.0000,
            120.000,
            190.000,
            260.000,
            330.000,
            400.000,
            470.000,
            540.000,
            617.372,
            703.378,
            798.717,
            904.128,
            1020.38,
            1148.30,
            1288.72,
            1442.54,
            1610.70,
            1794.16,
            1993.93,
            2211.08,
            2446.71,
            2701.97,
            2978.04,
            3276.17,
            3597.63,
        ]
    )
    bandwidth = np.array(
        [
            70.0000,
            70.0000,
            70.0000,
            70.0000,
            70.0000,
            70.0000,
            70.0000,
            77.3724,
            86.0056,
            95.3398,
            105.411,
            116.256,
            127.914,
            140.423,
            153.823,
            168.154,
            183.457,
            199.776,
            217.153,
            235.631,
            255.255,
            276.072,
            298.126,
            321.465,
            346.136,
        ]
    )

    # Minimum critical bandwidth
    bw_min = bandwidth[0]

    # Set up the critical band filters.
    # Note here that Gaussian-ly shaped filters are used.
    # Also, the sum of the filter weights are equivalent for each critical band filter.
    # Filter less than -30 dB and set to zero.

    # -30 dB point of filter
    min_factor = np.exp(-30.0 / (2.0 * 2.303))
    crit_filter = np.empty((num_crit, n_fft_by_2))
    for i in range(num_crit):
        f0 = (cent_freq[i] / max_freq) * n_fft_by_2
        bw = (bandwidth[i] / max_freq) * n_fft_by_2
        norm_factor = np.log(bw_min) - np.log(bandwidth[i])
        j = np.arange(n_fft_by_2)
        crit_filter[i, :] = np.exp(-11 * np.square(np.divide(j - np.floor(f0), bw)) + norm_factor)
        cond = np.greater(crit_filter[i, :], min_factor)
        crit_filter[i, :] = np.where(cond, crit_filter[i, :], 0)

    # For each frame of input speech, calculate the weighted spectral slope measure
    num_frames = int(reference_length / skip_rate - (win_length / skip_rate))
    start = 0
    window = 0.5 * (1 - np.cos(2 * np.pi * np.arange(1, win_length + 1) / (win_length + 1)))

    distortion = np.empty(num_frames)
    for frame_count in range(num_frames):
        # (1) Get the frames for the test and reference speech. Multiply by Hanning window.
        reference_frame = reference[start : start + win_length] / 32768
        hypothesis_frame = hypothesis[start : start + win_length] / 32768
        reference_frame = np.multiply(reference_frame, window)
        hypothesis_frame = np.multiply(hypothesis_frame, window)

        # (2) Compute the power spectrum of reference and hypothesis
        reference_spec = np.square(np.abs(fft(reference_frame, n_fft)))
        hypothesis_spec = np.square(np.abs(fft(hypothesis_frame, n_fft)))

        # (3) Compute filter bank output energies (in dB scale)
        reference_energy = np.matmul(crit_filter, reference_spec[0:n_fft_by_2])
        hypothesis_energy = np.matmul(crit_filter, hypothesis_spec[0:n_fft_by_2])

        reference_energy = 10 * np.log10(np.maximum(reference_energy, 1e-10))
        hypothesis_energy = 10 * np.log10(np.maximum(hypothesis_energy, 1e-10))

        # (4) Compute spectral slope (dB[i+1]-dB[i])
        reference_slope = reference_energy[1:num_crit] - reference_energy[0 : num_crit - 1]
        hypothesis_slope = hypothesis_energy[1:num_crit] - hypothesis_energy[0 : num_crit - 1]

        # (5) Find the nearest peak locations in the spectra to each critical band.
        #     If the slope is negative, we search to the left. If positive, we search to the right.
        reference_loc_peak = np.empty(num_crit - 1)
        hypothesis_loc_peak = np.empty(num_crit - 1)

        for i in range(num_crit - 1):
            # find the peaks in the reference speech signal
            if reference_slope[i] > 0:
                # search to the right
                n = i
                while (n < num_crit - 1) and (reference_slope[n] > 0):
                    n = n + 1
                reference_loc_peak[i] = reference_energy[n - 1]
            else:
                # search to the left
                n = i
                while (n >= 0) and (reference_slope[n] <= 0):
                    n = n - 1
                reference_loc_peak[i] = reference_energy[n + 1]

            # find the peaks in the hypothesis speech signal
            if hypothesis_slope[i] > 0:
                # search to the right
                n = i
                while (n < num_crit - 1) and (hypothesis_slope[n] > 0):
                    n = n + 1
                hypothesis_loc_peak[i] = hypothesis_energy[n - 1]
            else:
                # search to the left
                n = i
                while (n >= 0) and (hypothesis_slope[n] <= 0):
                    n = n - 1
                hypothesis_loc_peak[i] = hypothesis_energy[n + 1]

        # (6) Compute the weighted spectral slope measure for this frame.
        #     This includes determination of the weighting function.
        db_max_reference = np.max(reference_energy)
        db_max_hypothesis = np.max(hypothesis_energy)

        # The weights are calculated by averaging individual weighting factors from the reference and hypothesis frame.
        # These weights w_reference and w_hypothesis should range from 0 to 1 and place more emphasis on spectral peaks
        # and less emphasis on slope differences in spectral valleys.
        # This procedure is described on page 1280 of Klatt's 1982 ICASSP paper.

        w_max_reference = np.divide(k_max, k_max + db_max_reference - reference_energy[0 : num_crit - 1])
        w_loc_max_reference = np.divide(
            k_loc_max,
            k_loc_max + reference_loc_peak - reference_energy[0 : num_crit - 1],
        )
        w_reference = np.multiply(w_max_reference, w_loc_max_reference)

        w_max_hypothesis = np.divide(k_max, k_max + db_max_hypothesis - hypothesis_energy[0 : num_crit - 1])
        w_loc_max_hypothesis = np.divide(
            k_loc_max,
            k_loc_max + hypothesis_loc_peak - hypothesis_energy[0 : num_crit - 1],
        )
        w_hypothesis = np.multiply(w_max_hypothesis, w_loc_max_hypothesis)

        w = np.divide(np.add(w_reference, w_hypothesis), 2.0)
        slope_diff = np.subtract(reference_slope, hypothesis_slope)[0 : num_crit - 1]
        distortion[frame_count] = np.dot(w, np.square(slope_diff)) / np.sum(w)

        # This normalization is not part of Klatt's paper, but helps to normalize the measure.
        # Here we scale the measure by the sum of the weights.
        start = start + skip_rate

    return distortion


def _calc_log_likelihood_ratio_measure(
    hypothesis: np.ndarray, reference: np.ndarray, sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    from scipy.linalg import toeplitz

    # The lengths of the reference and hypothesis must be the same.
    reference_length = np.size(reference)
    hypothesis_length = np.size(hypothesis)
    if reference_length != hypothesis_length:
        raise ValueError("Hypothesis and reference must be the same length.")

    # window length in samples
    win_length = int(np.round(30 * sample_rate / 1000))
    # window skip in samples
    skip_rate = int(np.floor(win_length / 4))
    # LPC analysis order; this could vary depending on sampling frequency.
    if sample_rate < 10000:
        p = 10
    else:
        p = 16

    # For each frame of input speech, calculate the log likelihood ratio
    num_frames = int((reference_length - win_length) / skip_rate)
    start = 0
    window = 0.5 * (1 - np.cos(2 * np.pi * np.arange(1, win_length + 1) / (win_length + 1)))

    distortion = np.empty(num_frames)
    for frame_count in range(num_frames):
        # (1) Get the frames for the test and reference speech. Multiply by Hanning window.
        reference_frame = reference[start : start + win_length]
        hypothesis_frame = hypothesis[start : start + win_length]
        reference_frame = np.multiply(reference_frame, window)
        hypothesis_frame = np.multiply(hypothesis_frame, window)

        # (2) Get the autocorrelation lags and LPC parameters used to compute the log likelihood ratio measure.
        r_reference, ref_reference, a_reference = _lp_coefficients(reference_frame, p)
        r_hypothesis, ref_hypothesis, a_hypothesis = _lp_coefficients(hypothesis_frame, p)

        # (3) Compute the log likelihood ratio measure
        numerator = np.dot(np.matmul(a_hypothesis, toeplitz(r_reference)), a_hypothesis)
        denominator = np.dot(np.matmul(a_reference, toeplitz(r_reference)), a_reference)
        distortion[frame_count] = np.log(numerator / denominator)
        start = start + skip_rate
    return distortion


def _calc_snr(
    hypothesis: np.ndarray, reference: np.ndarray, sample_rate: int = SAMPLE_RATE
) -> tuple[float, np.ndarray]:
    # The lengths of the reference and hypothesis must be the same.
    reference_length = len(reference)
    hypothesis_length = len(hypothesis)
    if reference_length != hypothesis_length:
        raise ValueError("Hypothesis and reference must be the same length.")

    overall_snr = 10 * np.log10(
        np.sum(np.square(reference)) / (np.sum(np.square(reference - hypothesis))) + np.finfo(np.float32).eps
    )

    # window length in samples
    win_length = round(30 * sample_rate / 1000)
    # window skip in samples
    skip_rate = int(np.floor(win_length / 4))
    # minimum SNR in dB
    min_snr = -10
    # maximum SNR in dB
    max_snr = 35

    # For each frame of input speech, calculate the segmental SNR
    num_frames = int(reference_length / skip_rate - (win_length / skip_rate))
    start = 0
    window = 0.5 * (1 - np.cos(2 * np.pi * np.arange(1, win_length + 1) / (win_length + 1)))

    segmental_snr = np.empty(num_frames)
    eps = np.spacing(1)
    for frame_count in range(num_frames):
        # (1) Get the frames for the test and reference speech. Multiply by Hanning window.
        reference_frame = reference[start : start + win_length]
        hypothesis_frame = hypothesis[start : start + win_length]
        reference_frame = np.multiply(reference_frame, window)
        hypothesis_frame = np.multiply(hypothesis_frame, window)

        # (2) Compute the segmental SNR
        signal_energy = np.sum(np.square(reference_frame))
        noise_energy = np.sum(np.square(reference_frame - hypothesis_frame))
        segmental_snr[frame_count] = np.clip(
            10 * np.log10(signal_energy / (noise_energy + eps) + eps), min_snr, max_snr
        )

        start = start + skip_rate

    return overall_snr, segmental_snr


def _lp_coefficients(speech_frame, model_order):
    # (1) Compute autocorrelation lags
    win_length = np.size(speech_frame)
    autocorrelation = np.empty(model_order + 1)
    e = np.empty(model_order + 1)
    for k in range(model_order + 1):
        autocorrelation[k] = np.dot(speech_frame[0 : win_length - k], speech_frame[k:win_length])

    # (2) Levinson-Durbin
    a = np.ones(model_order)
    a_past = np.empty(model_order)
    ref_coefficients = np.empty(model_order)
    e[0] = autocorrelation[0]
    for i in range(model_order):
        a_past[0:i] = a[0:i]
        sum_term = np.dot(a_past[0:i], autocorrelation[i:0:-1])
        ref_coefficients[i] = (autocorrelation[i + 1] - sum_term) / e[i]
        a[i] = ref_coefficients[i]
        if i == 0:
            a[0:i] = a_past[0:i] - np.multiply(a_past[i - 1 : -1 : -1], ref_coefficients[i])
        else:
            a[0:i] = a_past[0:i] - np.multiply(a_past[i - 1 :: -1], ref_coefficients[i])
        e[i + 1] = (1 - ref_coefficients[i] * ref_coefficients[i]) * e[i]
    lp_params = np.concatenate((np.array([1]), -a))
    return autocorrelation, ref_coefficients, lp_params
