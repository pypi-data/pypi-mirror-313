from dataclasses import dataclass
from typing import Protocol

from quackinter.line import Line


class OutputPrint(Protocol):
    def __call__(self, output: str, line: Line): ...


@dataclass
class Config:
    # Delay before we start in ms
    delay: int = 0
    # Interval between lines in ms
    interval: int | None = None
    # Interval between chars in ms
    char_interval: int = 80
    # In case we need to print somewhere,
    # where to print
    output: OutputPrint = lambda output, line: None
