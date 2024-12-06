from dataclasses import dataclass


@dataclass(frozen=True)
class TimeAlignedType:
    start: float
    end: float
    text: str

    @property
    def duration(self) -> float:
        return self.end - self.start
