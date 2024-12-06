import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Segment:
    person: str
    video: str
    id: str
    start: float
    stop: float


def load_speakers(input_dir: Path) -> dict:
    import csv

    speakers = {}

    # VoxCeleb1
    first = True
    with open(input_dir / "vox1_meta.csv", newline="") as file:
        data = csv.reader(file, delimiter="\t")
        for row in data:
            if first:
                first = False
            else:
                speakers[row[0].strip()] = {
                    "gender": row[2].strip(),
                    "dialect": row[3].strip(),
                    "category": row[4].strip(),
                }

    # VoxCeleb2
    first = True
    with open(input_dir / "vox2_meta.csv", newline="") as file:
        data = csv.reader(file, delimiter="\t")
        for row in data:
            if first:
                first = False
            else:
                speakers[row[1].strip()] = {
                    "gender": row[3].strip(),
                    "category": row[4].strip(),
                }

    return speakers


def load_segment(path: str | os.PathLike[str]) -> Segment:
    path = Path(path)

    with path.open("r") as file:
        segment = file.read().strip()

    header, frames = segment.split("\n\n")
    header_dict = _parse_header(header)
    start, stop = _get_segment_boundaries(frames)

    return Segment(
        person=header_dict["Identity"],
        video=header_dict["Reference"],
        id=path.stem,
        start=start,
        stop=stop,
    )


def _parse_header(header: str) -> dict:
    def _parse_line(line: str) -> tuple[str, str]:
        """Parse a line of header text into a dictionary.

        Header text has the following format:

        Identity  : \tid00017
        Reference : \t7t6lfzvVaTM
        Offset    : \t1
        FV Conf   : \t16.647\t(1)
        ASD Conf  : \t4.465

        """
        k, v = line.split("\t", maxsplit=1)
        k = k[:-2].strip()
        v = v.strip()
        return k, v

    return dict(_parse_line(line) for line in header.split("\n"))


def _get_segment_boundaries(frames: str) -> tuple[float, float]:
    """Get the start and stop points of the segment.

    Frames text has the following format:

    FRAME 	X 	Y 	W 	H
    000245 	0.392 	0.223 	0.253 	0.451
    ...
    000470 	0.359 	0.207 	0.260 	0.463

    """

    def _get_frame_seconds(line: str) -> float:
        frame = int(line.split("\t")[0])
        # YouTube is 25 FPS
        return frame / 25

    lines = frames.split("\n")
    return _get_frame_seconds(lines[1]), _get_frame_seconds(lines[-1])
