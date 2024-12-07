from quackinter.commands.command import Command
from quackinter.stack import Stack

from pymsgbox import alert


class WaitForButtonPressCommand(Command):
    names = ["WAITFORBUTTONPRESS", "WAIT_FOR_BUTTON_PRESS"]

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        clean_data = data.strip()
        alert(clean_data if clean_data else "PRESS ENTER TO CONTINUE", button="CONTINUE")
