from quackinter.commands.command import Command
from quackinter.stack import Stack


class RemCommand(Command):
    names = ["REM"]
    ignore = True

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        pass
