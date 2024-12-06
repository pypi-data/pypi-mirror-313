import os

from .types import TimeAlignedType


def load_text(audio: str | os.PathLike[str]) -> TimeAlignedType | None:
    """Load time-aligned text data given a McGill-Speech audio file.

    :param audio: Path to the McGill-Speech audio file.
    :return: A TimeAlignedType object.
    """
    import string
    import struct

    from sonusai.mixture import get_sample_rate

    if not os.path.exists(audio):
        return None

    sample_rate = get_sample_rate(str(audio))

    with open(audio, mode="rb") as f:
        content = f.read()

    riff_id, file_size, wave_id = struct.unpack("<4si4s", content[:12])
    if riff_id.decode("utf-8") != "RIFF":
        return None

    if wave_id.decode("utf-8") != "WAVE":
        return None

    fmt_id, fmt_size = struct.unpack("<4si", content[12:20])

    if fmt_id.decode("utf-8") != "fmt ":
        return None

    if fmt_size != 16:
        return None

    (
        _wave_format_tag,
        channels,
        _samples_per_sec,
        _avg_bytes_per_sec,
        _block_align,
        bits_per_sample,
    ) = struct.unpack("<hhiihh", content[20:36])

    i = 36
    samples = None
    text = None
    while i < file_size:
        chunk_id = struct.unpack("<4s", content[i : i + 4])[0].decode("utf-8")
        chunk_size = struct.unpack("<i", content[i + 4 : i + 8])[0]

        if chunk_id == "data":
            samples = chunk_size / channels / (bits_per_sample / 8)
            break

        if chunk_id == "afsp":
            chunks = struct.unpack(f"<{chunk_size}s", content[i + 8 : i + 8 + chunk_size])[0]
            chunks = chunks.decode("utf-8").split("\x00")
            for chunk in chunks:
                if chunk.startswith('text: "'):
                    text = chunk[7:-1].lower().translate(str.maketrans("", "", string.punctuation))
        i += 8 + chunk_size + chunk_size % 2

    if text and samples:
        return TimeAlignedType(start=0, end=samples / sample_rate, text=text)

    return None
