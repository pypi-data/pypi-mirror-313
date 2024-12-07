from quackinter.commands.command import Command
from quackinter.environment import Environment
from quackinter.line import Line
from quackinter.stack import Stack


class StringDelayCommand(Command):
    names = ["STRINGDELAY", "STRING_DELAY"]
    include_with_repeat = True

    STRING_DELAY_INTERVAL_OVERRIDE = "_STRING_DELAY"
    GLOBAL_ENV_TICK_COUNT = "_STRING_DELAY_TICK_COUNT"

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        new_delay = self.convert_int(data)
        self.global_env.global_vars[self.STRING_DELAY_INTERVAL_OVERRIDE] = new_delay
        self.global_env.global_vars[self.GLOBAL_ENV_TICK_COUNT] = 2

    def global_environment_init(self, environment: Environment) -> None:
        environment.global_vars[self.STRING_DELAY_INTERVAL_OVERRIDE] = None
        environment.global_vars[self.GLOBAL_ENV_TICK_COUNT] = 0

    def tick(self, stack: Stack, line: Line) -> None:
        global_vars = self.global_env.global_vars

        if global_vars[self.STRING_DELAY_INTERVAL_OVERRIDE] is None:
            return

        global_vars[self.GLOBAL_ENV_TICK_COUNT] -= 1

        if global_vars[self.GLOBAL_ENV_TICK_COUNT] == 0:
            global_vars[self.STRING_DELAY_INTERVAL_OVERRIDE] = None
