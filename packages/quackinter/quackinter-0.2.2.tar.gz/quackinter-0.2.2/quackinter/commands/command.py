from abc import ABC, abstractmethod

from quackinter.environment import Environment
from quackinter.line import Line
from quackinter.stack import Stack
from quackinter.errors import NotANumberError


class Command(ABC):
    names = ["BASE"]
    ignore: bool = False
    """
    If we should not add this command
    to the "generated_lines"
    """
    include_with_repeat = False
    """
    True if this command should be included
    when repeat runs the command above.

    Example:
    ```
    STRINGDELAY 1000
    STRINGLN Hello World
    REPEAT 10
    ```
    STRINGDELAY needs to run every single repeat so that it takes
    one second between each character on every single REPEAT.
    """

    def __init__(self, environment: Environment) -> None:
        self.global_env = environment

    @abstractmethod
    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        pass

    @classmethod
    def is_this_command(cls, name: str, data: str) -> bool:
        return name.upper() in cls.names

    @staticmethod
    def convert_float(data: str):
        try:
            return float(data)
        except ValueError:
            raise NotANumberError(f"Value '{data}' is not a float.")

    @staticmethod
    def convert_int(data: str):
        try:
            return int(data.strip())
        except ValueError:
            raise NotANumberError(f"Value '{data}' is not an integer.")

    def global_environment_init(self, environment: Environment) -> None:
        pass

    def global_environment_exit(self, environment: Environment) -> None:
        pass

    def tick(self, stack: Stack, line: Line) -> None:
        """
        This function runs between every
        single line. It is ran after the
        given line.
        """
        return None
