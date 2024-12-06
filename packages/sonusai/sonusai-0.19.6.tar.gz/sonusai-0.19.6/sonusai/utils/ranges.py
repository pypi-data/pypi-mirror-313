def expand_range(s: str, sort: bool = True) -> list[int]:
    """Returns a list of integers from a string input representing a range."""
    import re

    clean_s = s.replace(":", "-")
    clean_s = clean_s.replace(";", ",")
    clean_s = re.sub(r" +", ",", clean_s)
    clean_s = re.sub(r",+", ",", clean_s)

    r: list[int] = []
    for i in clean_s.split(","):
        if "-" not in i:
            r.append(int(i))
        else:
            lo, hi = map(int, i.split("-"))
            r += range(lo, hi + 1)

    if sort:
        r = sorted(r)

    return r


def consolidate_range(r: list[int]) -> str:
    """Returns a string representing a range from an input list of integers."""
    from collections.abc import Generator

    def ranges(i: list[int]) -> Generator[tuple[int, int], None, None]:
        import itertools

        for _, b in itertools.groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
            b_list = list(b)
            yield b_list[0][1], b_list[-1][1]

    ls: list[tuple[int, int]] = list(ranges(r))
    result: list[str] = []
    for val in ls:
        entry = str(val[0])
        if val[0] != val[1]:
            entry += f"-{val[1]}"
        result.append(entry)

    return ", ".join(result)
