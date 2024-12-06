from sonusai.mixture.constants import SAMPLE_RATE
from sonusai.mixture.datatypes import AudioT


def write_audio(name: str, audio: AudioT, sample_rate: int = SAMPLE_RATE) -> None:
    """Write an audio file.

    To write multiple channels, use a 2D array of shape [channels, samples].
    The bits per sample and PCM/float are determined by the data type.

    """
    import torch
    import torchaudio

    data = torch.tensor(audio)

    if data.dim() == 1:
        data = torch.reshape(data, (1, data.shape[0]))
    if data.dim() != 2:
        raise ValueError("audio must be a 1D or 2D array")

    # Assuming data has more samples than channels, check if array needs to be transposed
    if data.shape[1] < data.shape[0]:
        data = torch.transpose(data, 0, 1)

    torchaudio.save(uri=name, src=data, sample_rate=sample_rate)
