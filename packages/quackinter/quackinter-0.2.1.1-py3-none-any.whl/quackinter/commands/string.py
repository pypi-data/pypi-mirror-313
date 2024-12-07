from quackinter.commands.command import Command
from quackinter.commands.string_delay import StringDelayCommand
from quackinter.stack import Stack
from quackinter.key_injector import KeyInjector


class StringCommand(Command):
    names = ["STRING"]

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        interval_override: int | None = self.global_env.global_vars[
            StringDelayCommand.STRING_DELAY_INTERVAL_OVERRIDE
        ]
        injector = KeyInjector(stack.environment)
        injector.write(f"{data}", interval_override)
