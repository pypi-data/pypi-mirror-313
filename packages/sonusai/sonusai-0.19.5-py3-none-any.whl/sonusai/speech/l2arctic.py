import os
import string
from pathlib import Path

from .types import TimeAlignedType


def _get_duration(name: str) -> float:
    import soundfile

    try:
        return soundfile.info(name).duration
    except Exception as e:
        raise OSError(f"Error reading {name}: {e}") from e


def load_text(audio: str | os.PathLike[str]) -> TimeAlignedType | None:
    """Load time-aligned text data given a L2-ARCTIC audio file.

    :param audio: Path to the L2-ARCTIC audio file.
    :return: A TimeAlignedType object.
    """
    file = Path(audio).parent.parent / "transcript" / (Path(audio).stem + ".txt")
    if not os.path.exists(file):
        return None

    with open(file, encoding="utf-8") as f:
        line = f.read()

    return TimeAlignedType(
        0,
        _get_duration(str(audio)),
        line.strip().lower().translate(str.maketrans("", "", string.punctuation)),
    )


def load_words(audio: str | os.PathLike[str]) -> list[TimeAlignedType] | None:
    """Load time-aligned word data given a L2-ARCTIC audio file.

    :param audio: Path to the L2-ARCTIC audio file.
    :return: A list of TimeAlignedType objects.
    """
    return _load_ta(audio, "words")


def load_phonemes(audio: str | os.PathLike[str]) -> list[TimeAlignedType] | None:
    """Load time-aligned phonemes data given a L2-ARCTIC audio file.

    :param audio: Path to the L2-ARCTIC audio file.
    :return: A list of TimeAlignedType objects.
    """
    return _load_ta(audio, "phones")


def _load_ta(audio: str | os.PathLike[str], tier: str) -> list[TimeAlignedType] | None:
    from praatio import textgrid

    file = Path(audio).parent.parent / "textgrid" / (Path(audio).stem + ".TextGrid")
    if not os.path.exists(file):
        return None

    tg = textgrid.openTextgrid(str(file), includeEmptyIntervals=False)
    if tier not in tg.tierNames:
        return None

    entries: list[TimeAlignedType] = []
    for entry in tg.getTier(tier).entries:
        entries.append(TimeAlignedType(text=entry.label, start=entry.start, end=entry.end))

    return entries


def load_annotations(
    audio: str | os.PathLike[str],
) -> dict[str, list[TimeAlignedType]] | None:
    """Load time-aligned annotation data given a L2-ARCTIC audio file.

    :param audio: Path to the L2-ARCTIC audio file.
    :return: A dictionary of a list of TimeAlignedType objects.
    """
    from praatio import textgrid

    file = Path(audio).parent.parent / "annotation" / (Path(audio).stem + ".TextGrid")
    if not os.path.exists(file):
        return None

    tg = textgrid.openTextgrid(str(file), includeEmptyIntervals=False)
    result: dict[str, list[TimeAlignedType]] = {}
    for tier in tg.tierNames:
        entries: list[TimeAlignedType] = []
        for entry in tg.getTier(tier).entries:
            entries.append(TimeAlignedType(text=entry.label, start=entry.start, end=entry.end))
        result[tier] = entries

    return result


def load_speakers(input_dir: Path) -> dict:
    speakers = {}
    with open(input_dir / "readme-download.txt") as file:
        processing = False
        for line in file:
            if not processing and line.startswith("|---|"):
                processing = True
                continue

            if processing:
                if line.startswith("|**Total**|"):
                    break
                else:
                    fields = line.strip().split("|")
                    speaker_id = fields[1]
                    gender = fields[2]
                    dialect = fields[3]
                    speakers[speaker_id] = {"gender": gender, "dialect": dialect}

    return speakers
