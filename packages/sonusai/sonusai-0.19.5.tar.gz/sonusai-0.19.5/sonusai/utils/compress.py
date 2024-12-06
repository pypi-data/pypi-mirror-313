from sonusai.mixture import AudioF


def power_compress(feature: AudioF) -> AudioF:
    import numpy as np

    mag = np.abs(feature)
    phase = np.angle(feature)
    mag = mag**0.3
    real_compress = mag * np.cos(phase)
    imag_compress = mag * np.sin(phase)

    return real_compress + 1j * imag_compress


def power_uncompress(feature: AudioF) -> AudioF:
    import numpy as np

    mag = np.abs(feature)
    phase = np.angle(feature)
    mag = mag ** (1.0 / 0.3)
    real_uncompress = mag * np.cos(phase)
    imag_uncompress = mag * np.sin(phase)

    return real_uncompress + 1j * imag_uncompress
