from quackinter.commands.command import Command
from quackinter.stack import Stack

from quackinter.key_injector import KeyInjector


class SysRqCommand(Command):
    names = ["SYSRQ"]

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        key_injector = KeyInjector(stack.environment)
        key_injector.hotkey(["alt", "prntscrn", data.strip()])
