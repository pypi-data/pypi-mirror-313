from time import sleep

from quackinter.commands.command import Command
from quackinter.stack import Stack


class DelayCommand(Command):
    names = ["DELAY"]

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        sleep(self.convert_int(data) / 1000)
