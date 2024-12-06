import os
from pathlib import Path

from .types import TimeAlignedType


def _get_num_samples(audio: str | os.PathLike[str]) -> int:
    """Get number of samples from audio file using soundfile

    :param audio: Audio file name
    :return: Number of samples
    """
    import soundfile
    from pydub import AudioSegment

    if Path(audio).suffix == ".mp3":
        return AudioSegment.from_mp3(audio).frame_count()

    if Path(audio).suffix == ".m4a":
        return AudioSegment.from_file(audio).frame_count()

    return soundfile.info(audio).frames


def load_text(audio: str | os.PathLike[str]) -> TimeAlignedType | None:
    """Load text data from a LibriSpeech transcription file given a LibriSpeech audio filename.

    :param audio: Path to the LibriSpeech audio file.
    :return: A TimeAlignedType object.
    """
    import string

    from sonusai.mixture import get_sample_rate

    path = Path(audio)
    name = path.stem
    transcript_filename = path.parent / f"{path.parent.parent.name}-{path.parent.name}.trans.txt"

    if not os.path.exists(transcript_filename):
        return None

    with open(transcript_filename, encoding="utf-8") as f:
        for line in f.readlines():
            fields = line.strip().split()
            key = fields[0]
            if key == name:
                text = " ".join(fields[1:]).lower().translate(str.maketrans("", "", string.punctuation))
                return TimeAlignedType(0, _get_num_samples(audio) / get_sample_rate(str(audio)), text)

    return None


def load_words(audio: str | os.PathLike[str]) -> list[TimeAlignedType] | None:
    """Load time-aligned word data given a LibriSpeech audio file.

    :param audio: Path to the Librispeech audio file.
    :return: A list of TimeAlignedType objects.
    """
    return _load_ta(audio, "words")


def load_phonemes(audio: str | os.PathLike[str]) -> list[TimeAlignedType] | None:
    """Load time-aligned phonemes data given a LibriSpeech audio file.

    :param audio: Path to the LibriSpeech audio file.
    :return: A list of TimeAlignedType objects.
    """
    return _load_ta(audio, "phones")


def _load_ta(audio: str | os.PathLike[str], tier: str) -> list[TimeAlignedType] | None:
    from praatio import textgrid

    file = Path(audio).with_suffix(".TextGrid")
    if not os.path.exists(file):
        return None

    tg = textgrid.openTextgrid(str(file), includeEmptyIntervals=False)
    if tier not in tg.tierNames:
        return None

    entries: list[TimeAlignedType] = []
    for entry in tg.getTier(tier).entries:
        entries.append(TimeAlignedType(text=entry.label, start=entry.start, end=entry.end))

    return entries


def load_speakers(input_dir: Path) -> dict:
    speakers = {}
    with open(input_dir / "SPEAKERS.TXT") as file:
        for line in file:
            if not line.startswith(";"):
                fields = line.strip().split("|")
                speaker_id = fields[0].strip()
                gender = fields[1].strip()
                speakers[speaker_id] = {"gender": gender}
    return speakers
