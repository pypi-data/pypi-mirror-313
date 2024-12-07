from __future__ import annotations

from typing import Generator, TYPE_CHECKING
from time import sleep

from quackinter.environment import Environment
from quackinter.errors import QuackinterError
from quackinter.line import Line
from quackinter.sanitizer import Sanitizer

if TYPE_CHECKING:
    from quackinter.stack import Stack


class StackContext:
    def __init__(
        self, ducky: list[str], environment: Environment, stack: "Stack", offset: int
    ) -> None:
        self._ducky_code = ducky
        self.stack = stack
        self.config = environment.config
        self.offset = offset

        self._current_line: Line | None = None
        self.is_running = False
        self.generated_lines: list[Line] = []

        self.environment = environment

    def get_line_gen(self) -> Generator[Line]:
        if self.is_running:
            raise QuackinterError(
                "StackContext is still running, cannot run a new instance."
            )

        self.is_running = True
        self.generated_lines = []
        for index, line in enumerate(self._ducky_code):
            corrected_index = index + self.offset + 1
            if not line.strip():
                continue

            new_line = Line(self._sanitize_line(line), corrected_index, line)
            self.generated_lines.append(new_line)
            self._current_line = new_line
            yield new_line
            self._tick_commands(new_line)
            sleep(self.environment.global_vars.get("_DEFAULT_DELAY", 0) / 1000)
        self.is_running = False
        self._current_line = None

    def _tick_commands(self, line: Line):
        for cmd in self.environment.commands:
            cmd.tick(self.stack, line)

    def _sanitize_line(self, line: str) -> str:
        return Sanitizer.santize_str(line)

    def _get_count_back(self, start: int, count: int):
        """
        Continues to go back a line until count is zero.
        If the last command was a comment or `ignore` was true,
        it won't count towards `count`.
        """
        current_index = start
        current_offset = count
        while current_offset:
            current_index -= 1
            if current_index < 0:
                return None
            command = self.generated_lines[current_index]
            if command.command and command.command.ignore:
                continue
            current_offset -= 1
        return current_index

    def get_line_offset(self, count: int) -> None | Line:
        """
        Get a line from $count lines ago. Enter `1` to
        get the previous line from this one, `0` to get
        this line.
        """
        if not self.is_running:
            raise QuackinterError(
                "To get previous lines, StackContext must be running."
            )
        curr_ind = len(self.generated_lines) - 1
        new_ind = self._get_count_back(curr_ind, count)
        if new_ind is None:
            return None
        return self.generated_lines[new_ind]

    def __iter__(self):
        return self.get_line_gen()

    @property
    def current_line_num(self):
        """
        A 1-based index of the current
        line that we are on.
        """
        if not self.is_running or not self._current_line:
            raise QuackinterError(
                "To get the current line index, StackContext must be running."
            )
        return self._current_line.line_num

    @property
    def current_line(self):
        if not self.is_running or not self._current_line:
            raise QuackinterError(
                "To get the current line index, StackContext must be running."
            )
        return self._current_line
