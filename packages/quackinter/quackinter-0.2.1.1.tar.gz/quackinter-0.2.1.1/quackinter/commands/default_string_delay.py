from quackinter.commands.command import Command
from quackinter.environment import Environment
from quackinter.stack import Stack


class DefaultStringDelayCommand(Command):
    names = ["DEFAULT_STRING_DELAY", "DEFAULTSTRINGDELAY"]

    GLOBAL_ENV_NAME = "_DEFAULT_STRING_DELAY"
    GLOBAL_ENV_OVERRIDE_NAME = "_DEFAULT_STRING_DELAY_OVERIDDEN"

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        # If the config was set, then any changes shall be overridden
        if stack.environment.global_vars[self.GLOBAL_ENV_OVERRIDE_NAME]:
            return
        new_value = self.convert_int(data.strip())
        stack.environment.global_vars[self.GLOBAL_ENV_NAME] = new_value

    def global_environment_init(self, environment: Environment) -> None:
        environment.global_vars[self.GLOBAL_ENV_NAME] = environment.config.char_interval
        environment.global_vars[self.GLOBAL_ENV_OVERRIDE_NAME] = (
            environment.config.interval is not None
        )
