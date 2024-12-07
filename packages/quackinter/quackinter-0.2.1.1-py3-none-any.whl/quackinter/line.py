from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from quackinter.commands.command import Command


@dataclass
class Line:
    line: str
    """
    The content of this line [sanitized].
    """
    line_num: int
    """
    A 1-based index of the line
    number this is.
    """
    orig_line: str
    """
    The content of this line [DIRTY].
    """
    command: "Command | None" = None
    """
    The Command this line was discovered
    to be.
    """
