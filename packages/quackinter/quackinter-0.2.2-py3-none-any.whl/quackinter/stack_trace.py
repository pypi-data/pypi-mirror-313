from dataclasses import dataclass

from quackinter.errors import InterpretationError
from quackinter.line import Line
from quackinter.stack_context import StackContext


@dataclass
class StackTraceback:
    line_num: int
    line_content: str
    line: Line
    context: StackContext

    @classmethod
    def from_context(cls, context: StackContext):
        return StackTraceback(
            context.current_line_num, context.current_line.orig_line, context.current_line, context
        )


@dataclass
class StackTrace:
    traceback: list[StackTraceback]
    error: InterpretationError

    @classmethod
    def from_error(cls, e: InterpretationError):
        traceback_list: list[StackTraceback] = []
        for context in e.contexts:
            traceback = StackTraceback.from_context(context)
            traceback_list.append(traceback)
        return StackTrace(traceback_list, e)
