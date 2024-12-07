from __future__ import annotations

from typing import TYPE_CHECKING

from quackinter.environment import Environment
from quackinter.stack_context import StackContext
from quackinter.utils import extract_cmd
from quackinter.errors import (
    CommandNotDefinedError,
    InterpretationError,
    NotInitiatedError,
)

if TYPE_CHECKING:
    from quackinter.commands.command import Command


class Stack:
    def __init__(
        self,
        environment: Environment,
    ) -> None:
        self.config = environment.config
        self._context: StackContext | None = None
        self.old_enviro = environment
        if environment:
            self.environment = environment.extend()
        else:
            self.environment = Environment()

    def run(self, ducky: list[str], offset: int = 0) -> str | None:
        self._context = StackContext(ducky, self.environment, self, offset)
        for line in self._context:
            cmd_str, data = extract_cmd(line.line)
            command = self._find_command(cmd_str, data)
            line.command = command

            try:
                if not command:
                    raise CommandNotDefinedError(f"{cmd_str} is not a command.")

                command.execute(self, cmd_str, data)
            except InterpretationError as ie:
                ie.add_context(self._context)
                raise ie

    def _find_command(self, cmd: str, data: str) -> "Command | None":
        for i in self.environment.commands:  # type: ignore
            if i.is_this_command(cmd, data):
                return i
        return None

    def new_stack(self):
        return Stack(self.environment)

    @property
    def context(self):
        if self._context is None:
            raise NotInitiatedError("Stack was not initiated")
        return self._context
