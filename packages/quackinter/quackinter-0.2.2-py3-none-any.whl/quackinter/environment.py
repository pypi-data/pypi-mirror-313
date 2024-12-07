from __future__ import annotations
from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field

from quackinter.errors import NotInitiatedError, VariableNotDefinedError


if TYPE_CHECKING:
    from quackinter.config import Config
    from quackinter.commands.command import Command


@dataclass
class GlobalEnvironmentData:
    commands: list[type[Command]]
    config: Config
    global_vars: dict[str, Any] = field(default_factory=dict)


class Environment:
    """
    A class that stores variables that
    gets and sets, whilst also allowing
    you to create extensions of the heap.
    """

    def __init__(self, data: Environment | GlobalEnvironmentData):
        self._vars: dict[str, Any] = {}
        self.global_vars: dict[str, Any] = data.global_vars
        self.config: Config = data.config

        if isinstance(data, Environment):
            self.previous_env = data
            self.commands: list[Command] = data.commands
        else:
            self.previous_env = None
            self.commands = [cmd(self) for cmd in data.commands]

    def get_var(self, name: str) -> Any:
        """
        Get a variable that is local
        to this scope or higher.
        """
        if name in self._vars:
            return self._vars[name]
        if not self.previous_env:
            raise VariableNotDefinedError(f"{name} is not defined.")
        return self.previous_env.get_var(name)

    @property
    def vars(self):
        """
        Get all vars from this scope and above.
        DO NOT EDIT THE RESULT; IT WILL NOT
        UPDATE THE ENVIRONMENT.
        """
        if not self.previous_env:
            return {**self._vars}
        return {**self.previous_env.vars, **self._vars}

    def edit_var(self, name: str, val: Any) -> bool:
        """
        Edit a variable on the enviro stack,
        starting here and going down.
        """
        if name in self._vars:
            self._vars[name] = val
            return True
        if self.previous_env:
            return self.previous_env.edit_var(name, val)
        return False

    def add_var(self, name: str, val: Any) -> bool:
        """
        Add a var, or editing a variable
        lower in the stack.
        """
        successful_edit = self.edit_var(name, val)
        if successful_edit:
            return False

        self._vars[name] = val
        return True

    def remove_var(self, name: str) -> bool:
        """
        Remove a variable from the environment,
        starting with this point in the enviro
        stack, going down
        """
        if name in self._vars:
            self._vars.pop(name)
            return True

        if self.previous_env:
            return self.previous_env.remove_var(name)

        return False

    def extend(self):
        """
        Extend this environment by returning
        a new environment.
        """
        return Environment(self)

    def _global_init(self):
        """
        Initialize the given commands, and have
        this be the global environment.
        """
        for cmd in self.commands:
            cmd.global_environment_init(self)

    def _global_exit(self):
        if self.commands is None or self.config is None:
            raise NotInitiatedError(
                "Environment was supposed to exit but instead does not exist."
            )
        for cmd in self.commands:
            cmd.global_environment_exit(self)

    def is_global(self):
        return self.previous_env is None

    @classmethod
    def create_global(cls, commands: list[type[Command]], config: Config):
        global_data = GlobalEnvironmentData(commands, config)
        new_global = cls(global_data)
        new_global._global_init()
        return new_global

    def __enter__(self):
        if self.previous_env is None:
            return self
        return self

    def __exit__(self, exc_type: type[Exception], exc_value: str, exc_traceback: str):
        # General environment closing statement

        if self.previous_env is None:
            self._global_exit()
