from pathlib import Path

from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import ImpulseResponseData


def _raw_read(name: str | Path) -> tuple[AudioT, int]:
    import numpy as np
    import soundfile
    from pydub import AudioSegment

    from .tokenized_shell_vars import tokenized_expand

    expanded_name, _ = tokenized_expand(name)

    try:
        if expanded_name.endswith(".mp3"):
            sound = AudioSegment.from_mp3(expanded_name)
            raw = np.array(sound.get_array_of_samples()).astype(np.float32).reshape((-1, sound.channels))
            raw = raw / 2 ** (sound.sample_width * 8 - 1)
            sample_rate = sound.frame_rate
        elif expanded_name.endswith(".m4a"):
            sound = AudioSegment.from_file(expanded_name)
            raw = np.array(sound.get_array_of_samples()).astype(np.float32).reshape((-1, sound.channels))
            raw = raw / 2 ** (sound.sample_width * 8 - 1)
            sample_rate = sound.frame_rate
        else:
            raw, sample_rate = soundfile.read(expanded_name, always_2d=True, dtype="float32")
    except Exception as e:
        if name != expanded_name:
            raise OSError(f"Error reading {name} (expanded: {expanded_name}): {e}") from e
        else:
            raise OSError(f"Error reading {name}: {e}") from e

    return np.squeeze(raw[:, 0]), sample_rate


def get_sample_rate(name: str | Path) -> int:
    """Get sample rate from audio file using soundfile

    :param name: File name
    :return: Sample rate
    """
    import soundfile
    from pydub import AudioSegment

    from .tokenized_shell_vars import tokenized_expand

    expanded_name, _ = tokenized_expand(name)

    try:
        if expanded_name.endswith(".mp3"):
            return AudioSegment.from_mp3(expanded_name).frame_rate

        if expanded_name.endswith(".m4a"):
            return AudioSegment.from_file(expanded_name).frame_rate

        return soundfile.info(expanded_name).samplerate
    except Exception as e:
        if name != expanded_name:
            raise OSError(f"Error reading {name} (expanded: {expanded_name}): {e}") from e
        else:
            raise OSError(f"Error reading {name}: {e}") from e


def read_ir(name: str | Path) -> ImpulseResponseData:
    """Read impulse response data using soundfile

    :param name: File name
    :return: ImpulseResponseData object
    """
    import numpy as np

    from .datatypes import ImpulseResponseData

    # Read impulse response data from audio file
    out, sample_rate = _raw_read(name)
    offset = np.argmax(out)
    out = out[offset:]
    out = out / np.linalg.norm(out)

    return ImpulseResponseData(name=str(name), sample_rate=sample_rate, data=out)


def read_audio(name: str | Path) -> AudioT:
    """Read audio data from a file using soundfile

    :param name: File name
    :return: Array of time domain audio data
    """
    import librosa

    from .constants import SAMPLE_RATE

    out, sample_rate = _raw_read(name)
    out = librosa.resample(out, orig_sr=sample_rate, target_sr=SAMPLE_RATE, res_type="soxr_hq")

    return out


def get_num_samples(name: str | Path) -> int:
    """Get the number of samples resampled to the SonusAI sample rate in the given file

    :param name: File name
    :return: number of samples in resampled audio
    """
    import math

    import soundfile
    from pydub import AudioSegment

    from .constants import SAMPLE_RATE
    from .tokenized_shell_vars import tokenized_expand

    expanded_name, _ = tokenized_expand(name)

    if expanded_name.endswith(".mp3"):
        sound = AudioSegment.from_mp3(expanded_name)
        samples = sound.frame_count()
        sample_rate = sound.frame_rate
    elif expanded_name.endswith(".m4a"):
        sound = AudioSegment.from_file(expanded_name)
        samples = sound.frame_count()
        sample_rate = sound.frame_rate
    else:
        info = soundfile.info(name)
        samples = info.frames
        sample_rate = info.samplerate

    return math.ceil(SAMPLE_RATE * samples / sample_rate)
