from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from quackinter.stack_context import StackContext


class QuackinterError(Exception):
    pass


class OutsideContextError(QuackinterError):
    pass


class InterpretationError(QuackinterError):
    def __init__(self, *args: object):
        super().__init__(*args)
        self.contexts: "list[StackContext]" = []

    def add_context(self, new_context: "StackContext"):
        self.contexts.append(new_context)


class InterpretationSyntaxError(InterpretationError):
    pass


class NotInitiatedError(InterpretationError):
    pass


class CommandNotDefinedError(InterpretationError):
    pass


class VariableNotDefinedError(InterpretationError):
    pass


class NotANumberError(InterpretationError):
    pass


class KeyNotExistError(InterpretationError):
    pass


class InvalidArgError(InterpretationError):
    pass


class UnsupportedError(InterpretationError):
    pass
