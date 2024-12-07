from quackinter.commands.command import Command
from quackinter.errors import InterpretationSyntaxError, NotANumberError, InvalidArgError
from quackinter.line import Line
from quackinter.stack import Stack
from quackinter.stack_context import StackContext


class RepeatCommand(Command):
    names = ["REPEAT"]

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        line = stack.context.get_line_offset(1)
        clean_data = data.strip()

        if not clean_data.isnumeric():
            raise NotANumberError("The value given is not a number")
        
        if int(clean_data) > 1_000_000 or int(clean_data) < 1:
            raise InvalidArgError("Value given to REPEAT must be number through 1 Million and 1")

        if line is None:
            raise InterpretationSyntaxError("There must be a line before repeat to run")

        extra_context = self._add_context(stack.context)

        lines_to_run = [line.line for line in [*extra_context, line]]
        offset = stack.context.current_line_num - len(lines_to_run) - 1
        for _ in range(int(clean_data)):
            new_stack = stack.new_stack()
            new_stack.run(lines_to_run, offset=offset)

    def _add_context(self, context: StackContext):
        """
        Looks for further lines above 
        the one we are referring to, to see
        if there is any more necessary context;
        for example, a STRINGDELAY that is above
        the line we want to repeat.

        Ex:
        ```
        REM STRINGDELAY is referred to every
        REM time the REPEAT runs
        STRINGDELAY 30
        STRINGLN Hello World!
        REPEAT 3
        ```
        """
        count = 2
        extra_context: list[Line] = []
        while True:
            possible_line = context.get_line_offset(count)
            if (
                possible_line is None
                or possible_line.command is None
                or not possible_line.command.include_with_repeat
            ):
                break
            extra_context.append(possible_line)
            count += 1
        return extra_context[::-1]
