from collections.abc import Generator
from typing import LiteralString


def expand_braces(text: LiteralString | str | bytes, seen: set[str] | None = None) -> Generator[str, None, None]:
    """Brace-expansion pre-processing for glob.

    Expand all the braces, then run glob on each of the results.
    (Brace-expansion turns one string into a list of strings.)
    https://stackoverflow.com/questions/22996645/brace-expansion-in-python-glob
    """
    import itertools
    import re

    if seen is None:
        seen = set()

    if not isinstance(text, str):
        text = str(text)

    spans = [m.span() for m in re.finditer(r"\{[^{}]*}", text)][::-1]
    alts = [text[start + 1 : stop - 1].split(",") for start, stop in spans]

    if len(spans) == 0:
        if text not in seen:
            yield text
        seen.add(text)
    else:
        for combo in itertools.product(*alts):
            replaced = list(text)
            for (start, stop), replacement in zip(spans, combo, strict=False):
                replaced[start:stop] = replacement
            yield from expand_braces("".join(replaced), seen)


def braced_glob(pathname: LiteralString | str | bytes, recursive: bool = False) -> list[str]:
    from glob import glob

    result = []
    for expanded_path in expand_braces(pathname):
        result.extend(glob(expanded_path, recursive=recursive))

    return result


def braced_iglob(pathname: LiteralString | str | bytes, recursive: bool = False) -> Generator[str, None, None]:
    from glob import iglob

    for expanded_path in expand_braces(pathname):
        yield from iglob(expanded_path, recursive=recursive)
