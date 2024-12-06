import os
from pathlib import Path

from .types import TimeAlignedType


def load_text(audio: str | os.PathLike[str]) -> TimeAlignedType | None:
    """Load time-aligned text data given a TIMIT audio file.

    :param audio: Path to the TIMIT audio file.
    :return: A TimeAlignedType object.
    """
    import string

    from sonusai.mixture import get_sample_rate

    file = Path(audio).with_suffix(".TXT")
    if not os.path.exists(file):
        return None

    sample_rate = get_sample_rate(str(audio))

    with open(file, encoding="utf-8") as f:
        line = f.read()

    fields = line.strip().split()
    start = int(fields[0]) / sample_rate
    end = int(fields[1]) / sample_rate
    text = " ".join(fields[2:]).lower().translate(str.maketrans("", "", string.punctuation))

    return TimeAlignedType(start, end, text)


def load_words(audio: str | os.PathLike[str]) -> list[TimeAlignedType] | None:
    """Load time-aligned word data given a TIMIT audio file.

    :param audio: Path to the TIMIT audio file.
    :return: A list of TimeAlignedType objects.
    """

    return _load_ta(audio, "words")


def load_phonemes(audio: str | os.PathLike[str]) -> list[TimeAlignedType] | None:
    """Load time-aligned phonemes data given a TIMIT audio file.

    :param audio: Path to the TIMIT audio file.
    :return: A list of TimeAlignedType objects.
    """

    return _load_ta(audio, "phonemes")


def _load_ta(audio: str | os.PathLike[str], tier: str) -> list[TimeAlignedType] | None:
    from sonusai.mixture import get_sample_rate

    if tier == "words":
        file = Path(audio).with_suffix(".WRD")
    elif tier == "phonemes":
        file = Path(audio).with_suffix(".PHN")
    else:
        raise ValueError(f"Unknown tier: {tier}")

    if not os.path.exists(file):
        return None

    sample_rate = get_sample_rate(str(audio))

    entries: list[TimeAlignedType] = []
    first = True
    with open(file, encoding="utf-8") as f:
        for line in f.readlines():
            fields = line.strip().split()
            start = int(fields[0]) / sample_rate
            end = int(fields[1]) / sample_rate
            text = " ".join(fields[2:])

            if first:
                first = False
            else:
                if start < entries[-1].end:
                    start = entries[-1].end - (entries[-1].end - start) // 2
                    entries[-1] = TimeAlignedType(text=entries[-1].text, start=entries[-1].start, end=start)

                if end <= start:
                    end = start + 1 / sample_rate

            entries.append(TimeAlignedType(text=text, start=start, end=end))

    return entries


def _years_between(record, born):
    try:
        rec_fields = [int(x) for x in record.split("/")]
        brn_fields = [int(x) for x in born.split("/")]
        return rec_fields[2] - brn_fields[2] - ((rec_fields[1], rec_fields[0]) < (brn_fields[1], brn_fields[0]))
    except ValueError:
        return "??"


def _decode_dialect(d: str) -> str:
    if d in ["DR1", "1"]:
        return "New England"
    if d in ["DR2", "2"]:
        return "Northern"
    if d in ["DR3", "3"]:
        return "North Midland"
    if d in ["DR4", "4"]:
        return "South Midland"
    if d in ["DR5", "5"]:
        return "Southern"
    if d in ["DR6", "6"]:
        return "New York City"
    if d in ["DR7", "7"]:
        return "Western"
    if d in ["DR8", "8"]:
        return "Army Brat"

    raise ValueError(f"Unrecognized dialect: {d}")


def load_speakers(input_dir: Path) -> dict:
    speakers = {}
    with open(input_dir / "SPKRINFO.TXT") as file:
        for line in file:
            if not line.startswith(";"):
                fields = line.strip().split()
                speaker_id = fields[0]
                gender = fields[1]
                dialect = _decode_dialect(fields[2])
                age = _years_between(fields[4], fields[5])
                speakers[speaker_id] = {
                    "gender": gender,
                    "dialect": dialect,
                    "age": age,
                }
    return speakers
