from pathlib import Path

from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import ImpulseResponseData


def read_impulse_response(name: str | Path) -> ImpulseResponseData:
    """Read impulse response data using torchaudio

    :param name: File name
    :return: ImpulseResponseData object
    """
    import numpy as np
    import torch
    import torchaudio

    from .tokenized_shell_vars import tokenized_expand

    expanded_name, _ = tokenized_expand(name)

    # Read impulse response data from audio file
    try:
        raw, sample_rate = torchaudio.load(expanded_name, backend="soundfile")
    except Exception as e:
        if name != expanded_name:
            raise OSError(f"Error reading {name} (expanded: {expanded_name}): {e}") from e
        else:
            raise OSError(f"Error reading {name}: {e}") from e

    raw = torch.squeeze(raw[0, :])
    offset = torch.argmax(raw)
    raw = raw[offset:]
    # Inexplicably, torch.linalg.vector_norm() causes multiprocessing contexts to hang.
    # Use np.linalg.norm() instead.
    # raw = raw / torch.linalg.vector_norm(raw)

    data = np.array(raw).astype(np.float32)
    data = data / np.linalg.norm(data)

    return ImpulseResponseData(name=str(name), sample_rate=sample_rate, data=data)


def get_sample_rate(name: str | Path) -> int:
    """Get sample rate from audio file using torchaudio

    :param name: File name
    :return: Sample rate
    """
    import torchaudio

    from .tokenized_shell_vars import tokenized_expand

    expanded_name, _ = tokenized_expand(name)

    try:
        return torchaudio.info(expanded_name).sample_rate
    except Exception as e:
        if name != expanded_name:
            raise OSError(f"Error reading {name} (expanded: {expanded_name}):\n{e}") from e
        else:
            raise OSError(f"Error reading {name}:\n{e}") from e


def read_audio(name: str | Path) -> AudioT:
    """Read audio data from a file using torchaudio

    :param name: File name
    :return: Array of time domain audio data
    """
    import numpy as np
    import torch
    import torchaudio

    from .constants import SAMPLE_RATE
    from .tokenized_shell_vars import tokenized_expand

    expanded_name, _ = tokenized_expand(name)

    try:
        out, samplerate = torchaudio.load(expanded_name, backend="soundfile")
        out = torch.reshape(out[0, :], (1, out.size()[1]))
        out = torchaudio.functional.resample(
            out,
            orig_freq=samplerate,
            new_freq=SAMPLE_RATE,
            resampling_method="sinc_interp_hann",
        )
    except Exception as e:
        if name != expanded_name:
            raise OSError(f"Error reading {name} (expanded: {expanded_name}):\n{e}") from e
        else:
            raise OSError(f"Error reading {name}:\n{e}") from e

    result = np.squeeze(np.array(out))
    return result
