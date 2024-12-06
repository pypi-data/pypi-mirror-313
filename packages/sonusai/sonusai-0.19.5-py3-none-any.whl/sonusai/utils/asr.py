from collections.abc import Callable
from dataclasses import dataclass

from sonusai.mixture import AudioT


@dataclass(frozen=True)
class ASRResult:
    text: str
    confidence: float | None = None
    lang: str | None = None
    lang_prob: float | None = None
    duration: float | None = None
    num_segments: int | None = None
    asr_cpu_time: float | None = None


def get_available_engines() -> list[str]:
    from importlib import import_module
    from pkgutil import iter_modules

    module = import_module("sonusai.utils.asr_functions")
    engines = [method for method in dir(module) if not method.startswith("_")]
    for _, name, _ in iter_modules():
        if name.startswith("sonusai_asr_"):
            module = import_module(f"{name}.asr_functions")
            for method in dir(module):
                if not method.startswith("_"):
                    engines.append(method)

    return engines


def _asr_fn(engine: str) -> Callable[..., ASRResult]:
    from importlib import import_module
    from pkgutil import iter_modules

    module = import_module("sonusai.utils.asr_functions")
    for method in dir(module):
        if method == engine:
            return getattr(module, method)

    for _, name, _ in iter_modules():
        if name.startswith("sonusai_asr_"):
            module = import_module(f"{name}.asr_functions")
            for method in dir(module):
                if method == engine:
                    return getattr(module, method)

    raise ValueError(f"engine {engine} not supported")


def calc_asr(audio: AudioT | str, engine: str, **config) -> ASRResult:
    """Run ASR on audio

    :param audio: Numpy array of audio samples or location of an audio file
    :param engine: ASR engine to use
    :param config: kwargs configuration parameters
    :return: ASRResult object containing text and confidence
    """
    from copy import copy

    import numpy as np

    from sonusai.mixture import read_audio

    if not isinstance(audio, np.ndarray):
        audio = copy(read_audio(audio))

    return _asr_fn(engine)(audio, **config)


def validate_asr(engine: str, **config) -> None:
    from importlib import import_module
    from pkgutil import iter_modules

    module = import_module("sonusai.utils.asr_functions")
    for method in dir(module):
        if method == engine:
            getattr(module, method + "_validate")(**config)
            return

    for _, name, _ in iter_modules():
        if name.startswith("sonusai_asr_"):
            module = import_module(f"{name}.asr_functions")
            for method in dir(module):
                if method == engine:
                    getattr(module, method + "_validate")(**config)
                    return

    raise ValueError(f"engine {engine} not supported")
