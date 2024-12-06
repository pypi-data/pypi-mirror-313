from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import Augmentation
from sonusai.mixture.datatypes import ImpulseResponseData


def apply_augmentation(audio: AudioT, augmentation: Augmentation, frame_length: int = 1) -> AudioT:
    """Apply augmentations to audio data using SoX

    :param audio: Audio
    :param augmentation: Augmentation
    :param frame_length: Pad resulting audio to be a multiple of this
    :return: Augmented audio
    """
    from .augmentation import pad_audio_to_frame
    from .constants import BIT_DEPTH
    from .constants import CHANNEL_COUNT
    from .constants import ENCODING
    from .constants import SAMPLE_RATE
    from .sox_audio import Transformer

    has_effects = False

    try:
        # Apply augmentations
        tfm = Transformer()
        tfm.set_input_format(rate=SAMPLE_RATE, bits=BIT_DEPTH, channels=CHANNEL_COUNT, encoding=ENCODING)
        tfm.set_output_format(rate=SAMPLE_RATE, bits=BIT_DEPTH, channels=CHANNEL_COUNT, encoding=ENCODING)

        # TODO
        #  Always normalize and remove normalize from list of available augmentations
        #  Normalize to globally set level (should this be a global config parameter,
        #  or hard-coded into the script?)
        if augmentation.normalize is not None:
            tfm.norm(db_level=augmentation.normalize)
            has_effects = True

        if augmentation.gain is not None:
            tfm.gain(gain_db=augmentation.gain, normalize=False)
            has_effects = True

        if augmentation.pitch is not None:
            tfm.pitch(n_semitones=float(augmentation.pitch) / 100)
            tfm.rate(samplerate=SAMPLE_RATE)
            has_effects = True

        if augmentation.tempo is not None:
            tfm.tempo(factor=float(augmentation.tempo), audio_type="s")
            has_effects = True

        if augmentation.eq1 is not None:
            tfm.equalizer(*augmentation.eq1)
            has_effects = True

        if augmentation.eq2 is not None:
            tfm.equalizer(*augmentation.eq2)
            has_effects = True

        if augmentation.eq3 is not None:
            tfm.equalizer(*augmentation.eq3)
            has_effects = True

        if augmentation.lpf is not None:
            tfm.lowpass(frequency=augmentation.lpf)
            has_effects = True

        if has_effects:
            audio_out = tfm.build_array(input_array=audio, sample_rate_in=SAMPLE_RATE)
        else:
            audio_out = audio

    except Exception as e:
        raise RuntimeError(f"Error applying {augmentation}: {e}") from e

    # make sure length is multiple of frame_length
    return pad_audio_to_frame(audio=audio_out, frame_length=frame_length)


def apply_impulse_response(audio: AudioT, ir: ImpulseResponseData) -> AudioT:
    """Apply impulse response to audio data using SoX

    :param audio: Audio
    :param ir: Impulse response data
    :return: Augmented audio
    """
    import math
    import tempfile
    from pathlib import Path

    import numpy as np

    from sonusai.utils import linear_to_db

    from .constants import SAMPLE_RATE
    from .sox_audio import Transformer

    # Early exit if no ir or if all audio is zero
    if ir is None or not audio.any():
        return audio

    # Get current maximum level in dB
    max_db = linear_to_db(max(abs(audio)))

    # Convert audio to IR sample rate
    tfm = Transformer()
    tfm.set_output_format(rate=ir.sample_rate)
    audio_out = tfm.build_array(input_array=audio, sample_rate_in=SAMPLE_RATE)

    # Pad audio to align with original and give enough room for IR tail
    pad = math.ceil(ir.length / 2)
    audio_out = np.pad(array=audio_out, pad_width=(pad, pad))

    # Write coefficients to temporary file
    temp = tempfile.NamedTemporaryFile(mode="w+t")
    for d in ir.data:
        temp.write(f"{d:f}\n")
    temp.seek(0)

    # Apply IR and convert back to global sample rate
    tfm = Transformer()
    tfm.set_output_format(rate=SAMPLE_RATE)
    tfm.fir(coefficients=temp.name)
    try:
        audio_out = tfm.build_array(input_array=audio_out, sample_rate_in=ir.sample_rate)
    except Exception as e:
        raise RuntimeError(f"Error applying IR: {e}") from e

    path = Path(temp.name)
    temp.close()
    path.unlink()

    # Reset level to previous max value
    tfm = Transformer()
    tfm.norm(db_level=max_db)
    audio_out = tfm.build_array(input_array=audio_out, sample_rate_in=SAMPLE_RATE)

    return audio_out[: len(audio)]
