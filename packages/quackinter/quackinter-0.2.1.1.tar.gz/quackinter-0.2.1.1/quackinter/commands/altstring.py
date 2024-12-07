from quackinter.commands.command import Command
from quackinter.key_injector import KeyInjector
from quackinter.stack import Stack


class AltStringCommand(Command):
    names = ["ALTSTRING", "ALT_STRING", "ALTCODE", "ALT_CODE"]

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        injector = KeyInjector(stack.environment)
        injector.copy_paste_write(data)
