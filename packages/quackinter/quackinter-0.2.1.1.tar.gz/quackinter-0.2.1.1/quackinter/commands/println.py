from quackinter.commands.command import Command
from quackinter.stack import Stack


class PrintLnCommand(Command):
    names = ["PRINTLN", "PRINT_LINE"]

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        self.global_env.config.output(data.strip(), stack.context.current_line)
