from functools import lru_cache
from pathlib import Path

from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import ImpulseResponseData


def get_next_noise(audio: AudioT, offset: int, length: int) -> AudioT:
    """Get next sequence of noise data from noise audio

    :param audio: Overall noise audio (entire file's worth of data)
    :param offset: Starting sample
    :param length: Number of samples to get
    :return: Sequence of noise audio data
    """
    import numpy as np

    return np.take(audio, range(offset, offset + length), mode="wrap")


def get_duration(audio: AudioT) -> float:
    """Get duration of audio in seconds

    :param audio: Time domain data [samples]
    :return: Duration of audio in seconds
    """
    from .constants import SAMPLE_RATE

    return len(audio) / SAMPLE_RATE


def validate_input_file(input_filepath: str | Path) -> None:
    from os.path import exists
    from os.path import splitext

    from soundfile import available_formats

    if not exists(input_filepath):
        raise OSError(f"input_filepath {input_filepath} does not exist.")

    ext = splitext(input_filepath)[1][1:].lower()
    read_formats = [item.lower() for item in available_formats()]
    if ext not in read_formats:
        raise OSError(f"This installation cannot process .{ext} files")


@lru_cache
def get_sample_rate(name: str | Path) -> int:
    """Get sample rate from audio file

    :param name: File name
    :return: Sample rate
    """
    from .soundfile_audio import get_sample_rate

    return get_sample_rate(name)


@lru_cache
def read_audio(name: str | Path) -> AudioT:
    """Read audio data from a file

    :param name: File name
    :return: Array of time domain audio data
    """
    from .soundfile_audio import read_audio

    return read_audio(name)


@lru_cache
def read_ir(name: str | Path) -> ImpulseResponseData:
    """Read impulse response data

    :param name: File name
    :return: ImpulseResponseData object
    """
    from .soundfile_audio import read_ir

    return read_ir(name)


@lru_cache
def get_num_samples(name: str | Path) -> int:
    """Get the number of samples resampled to the SonusAI sample rate in the given file

    :param name: File name
    :return: number of samples in resampled audio
    """
    from .soundfile_audio import get_num_samples

    return get_num_samples(name)
