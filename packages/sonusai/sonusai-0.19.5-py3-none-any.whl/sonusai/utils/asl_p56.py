from sonusai.mixture import AudioT


def asl_p56(audio: AudioT) -> float:
    """Implement ITU-T P.56 method B
    :param audio: audio for which to calculate active speech level
    :return: Active speech level mean square energy
    """
    import numpy as np
    import scipy.signal as signal

    from sonusai.mixture import SAMPLE_RATE

    eps = np.finfo(np.float32).eps

    # Time constant of smoothing in seconds
    T = 0.03

    # Coefficient of smoothing
    g = np.exp(-1 / (SAMPLE_RATE * T))

    # Hangover time in seconds
    H = 0.2
    # Rounded up to next integer
    H_samples = np.ceil(H * SAMPLE_RATE)

    # Margin in dB, difference between threshold and active speech level
    M = 15.9

    # Number of thresholds
    thresh_num = 15

    # Series of fixed threshold voltages to apply to the envelope. These are spaced
    # in geometric progression, at intervals of not more than 2:1 (6.02 dB), from a
    # value equal to about half the maximum code down to a value equal to one
    # quantizing interval or lower.
    c = 2 ** np.arange(-15, thresh_num - 15, dtype=np.float32)

    # Activity counter for each threshold
    a = np.full(thresh_num, -1)

    # Hangover counter for each threshold
    h = np.full(thresh_num, H_samples)

    # Long-term level square energy of audio
    sq = sum(np.square(audio))

    # Use a 2nd order IIR filter to detect the envelope q
    p = signal.lfilter([1 - g, 0], [1, -g], abs(audio))
    # q is the envelope, obtained from moving average of abs(audio) (with slight "hangover").
    q = signal.lfilter([1 - g, 0], [1, -g], p)

    for k in range(len(audio)):
        for j in range(thresh_num):
            if q[k] >= c[j]:
                a[j] = a[j] + 1
                h[j] = 0
            elif h[j] < H_samples:
                a[j] = a[j] + 1
                h[j] = h[j] + 1
            else:
                break
    asl_msq = 0
    if a[0] == -1:
        return asl_msq

    a += 2
    A_db1 = 10 * np.log10(sq / a[0] + eps)
    C_db1 = 20 * np.log10(c[0] + eps)
    if A_db1 - C_db1 < M:
        return asl_msq

    A_db = np.zeros(thresh_num)
    C_db = np.zeros(thresh_num)
    delta = np.zeros(thresh_num)
    A_db[0] = A_db1
    C_db[0] = C_db1
    delta[0] = A_db1 - C_db1

    for j in range(1, thresh_num):
        A_db[j] = 10 * np.log10(sq / (a[j] + eps) + eps)
        C_db[j] = 20 * np.log10(c[j] + eps)

    for j in range(1, thresh_num):
        if a[j] != 0:
            delta[j] = A_db[j] - C_db[j]
            if delta[j] <= M:
                # Interpolate to find the asl_ms_log
                asl_ms_log = _bin_interp(A_db[j], A_db[j - 1], C_db[j], C_db[j - 1], M, 0.5)
                # This is the mean square value NOT the RMS
                asl_msq = 10.0 ** (asl_ms_log / 10)
                break

    return asl_msq


def _bin_interp(u_cnt: float, l_cnt: float, u_thr: float, l_thr: float, margin: float, tol: float) -> float:
    tol = abs(tol)

    # Check if extreme counts are not already the true active value
    iter_num = 1
    if abs(u_cnt - u_thr - margin) < tol:
        return u_cnt

    if abs(l_cnt - l_thr - margin) < tol:
        return l_cnt

    # Initialize first middle for given (initial) bounds
    m_cnt = (u_cnt + l_cnt) / 2.0
    m_thr = (u_thr + l_thr) / 2.0

    while True:
        # Loop until diff falls inside the tolerance (-tol<=diff<=tol)
        diff = m_cnt - m_thr - margin
        if abs(diff) <= tol:
            break

        # If tolerance is not met up to 20 iterations, then relax the tolerance by 10
        iter_num += 1
        if iter_num > 20:
            tol = tol * 1.1

        if diff > tol:
            m_cnt = (u_cnt + m_cnt) / 2.0
            m_thr = (u_thr + m_thr) / 2.0
        elif diff < -tol:
            m_cnt = (m_cnt + l_cnt) / 2.0
            m_thr = (m_thr + l_thr) / 2.0

    return m_cnt
