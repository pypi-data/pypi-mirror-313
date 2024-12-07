from typing import Iterable, Literal, TypedDict

from quackinter.commands.command import Command
from quackinter.errors import InvalidArgError
from quackinter.key_injector import KeyInjector
from quackinter.stack import Stack


class Encoding(TypedDict):
    name: str
    zero_fill: bool


encodings: list[Encoding] = [
    {"name": "CP1252", "zero_fill": True},
    # With some testing Windows seems to prefer CP437 over CP850
    {"name": "CP437", "zero_fill": False},
    {"name": "CP850", "zero_fill": False},
]


class AltCharCommand(Command):
    names = ["ALTCHAR", "ALT_CHAR"]

    @classmethod
    def attempt_decode(
        cls, use_encodings: Iterable[Encoding], char: str
    ) -> str | Literal[False]:
        for i in use_encodings:
            try:
                return bytes([int(char)]).decode(i["name"])
            except UnicodeDecodeError:
                pass
        return False

    @classmethod
    def convert_code(cls, code: str) -> str:
        use_encodings = filter(
            (
                (lambda enc: enc["zero_fill"])
                if code.startswith("0")
                else (lambda enc: not enc["zero_fill"])
            ),
            encodings,
        )

        value = cls.attempt_decode(
            use_encodings,
            code,
        )
        if value is not False:
            return value
        raise InvalidArgError(f"{code} is not a valid alt code.")

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        clean_data = data.strip()

        if len(clean_data) > 4 or not clean_data.isdigit():
            raise InvalidArgError(
                "Argument must be four numbers or less for an alt code"
            )

        injector = KeyInjector(stack.environment)
        char = self.convert_code(clean_data)
        injector.copy_paste_write(char)
