from typing import NamedTuple


class WerResult(NamedTuple):
    wer: float
    words: int
    substitutions: float
    deletions: float
    insertions: float


def calc_wer(hypothesis: list[str] | str, reference: list[str] | str) -> WerResult:
    """Computes average word error rate between two texts represented as corresponding strings or lists of strings.

    :param hypothesis: the hypothesis sentence(s) as a string or list of strings
    :param reference: the reference sentence(s) as a string or list of strings
    :return: a WerResult object with error, words, insertions, deletions, substitutions
    """
    import jiwer

    transformation = jiwer.Compose(
        [
            jiwer.ToLowerCase(),
            jiwer.RemovePunctuation(),
            jiwer.RemoveWhiteSpace(replace_by_space=True),
            jiwer.RemoveMultipleSpaces(),
            jiwer.Strip(),
            jiwer.RemoveEmptyStrings(),
            jiwer.ReduceToListOfListOfWords(word_delimiter=" "),
        ]
    )

    if isinstance(reference, str):
        reference = [reference]
    if isinstance(hypothesis, str):
        hypothesis = [hypothesis]

    # jiwer does not allow empty string
    measures = {"insertions": 0, "substitutions": 0, "deletions": 0, "hits": 0}
    if any(len(t) == 0 for t in reference):
        if any(len(t) != 0 for t in hypothesis):
            measures["insertions"] = len(hypothesis)
    else:
        measures = jiwer.compute_measures(
            truth=reference,
            hypothesis=hypothesis,
            truth_transform=transformation,
            hypothesis_transform=transformation,
        )

    errors = measures["substitutions"] + measures["deletions"] + measures["insertions"]
    words = measures["hits"] + measures["substitutions"] + measures["deletions"]

    if words != 0:
        wer = errors / words
        substitutions_rate = measures["substitutions"] / words
        deletions_rate = measures["deletions"] / words
        insertions_rate = measures["insertions"] / words
    else:
        wer = float("inf")
        substitutions_rate = float("inf")
        deletions_rate = float("inf")
        insertions_rate = float("inf")

    return WerResult(
        wer=wer,
        words=int(words),
        substitutions=substitutions_rate,
        deletions=deletions_rate,
        insertions=insertions_rate,
    )
