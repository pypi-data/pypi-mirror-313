from dataclasses import dataclass


@dataclass(frozen=True)
class PathInfo:
    abs_path: str
    audio_filepath: str
