from pathlib import Path

from praatio import textgrid
from praatio.utilities.constants import Interval

from .types import TimeAlignedType


def create_textgrid(
    prompt: Path,
    output_dir: Path,
    text: TimeAlignedType | None = None,
    words: list[TimeAlignedType] | None = None,
    phonemes: list[TimeAlignedType] | None = None,
) -> None:
    if text is None and words is None and phonemes is None:
        return

    min_t, max_t = _get_min_max({"phonemes": phonemes, "text": text, "words": words})

    tg = textgrid.Textgrid()

    if text is not None:
        entries = [Interval(text.start, text.end, text.text)]
        text_tier = textgrid.IntervalTier("text", entries, min_t, max_t)
        tg.addTier(text_tier)

    if words is not None:
        entries = []
        for word in words:
            entries.append(Interval(word.start, word.end, word.text))
        words_tier = textgrid.IntervalTier("words", entries, min_t, max_t)
        tg.addTier(words_tier)

    if phonemes is not None:
        entries = []
        for phoneme in phonemes:
            entries.append(Interval(phoneme.start, phoneme.end, phoneme.text))
        phonemes_tier = textgrid.IntervalTier("phonemes", entries, min_t, max_t)
        tg.addTier(phonemes_tier)

    output_filename = str(output_dir / prompt.stem) + ".TextGrid"
    tg.save(output_filename, format="long_textgrid", includeBlankSpaces=True)


def _get_min_max(tiers: dict[str, TimeAlignedType | list[TimeAlignedType] | None]) -> tuple[float, float]:
    starts = []
    ends = []
    for tier in tiers.values():
        if tier is None:
            continue
        if isinstance(tier, TimeAlignedType):
            starts.append(tier.start)
            ends.append(tier.end)
        else:
            starts.append(tier[0].start)
            ends.append(tier[-1].end)

    return min(starts), max(ends)


def annotate_textgrid(
    tiers: dict[str, TimeAlignedType | list[TimeAlignedType] | None] | None, prompt: Path, output_dir: Path
) -> None:
    import os

    if tiers is None:
        return

    file = Path(output_dir / prompt.stem).with_suffix(".TextGrid")
    if not os.path.exists(file):
        tg = textgrid.Textgrid()
        min_t, max_t = _get_min_max(tiers)
    else:
        tg = textgrid.openTextgrid(str(file), includeEmptyIntervals=False)
        min_t = tg.minTimestamp
        max_t = tg.maxTimestamp

    for k, v in tiers.items():
        if v is None:
            continue
        entries = [Interval(entry.start, entry.end, entry.text) for entry in v]
        if k == "phones":
            name = "annotation_phonemes"
        else:
            name = "annotation_" + k
        tg.addTier(textgrid.IntervalTier(name, entries, min_t, max_t))

    tg.save(str(file), format="long_textgrid", includeBlankSpaces=True)
