from quackinter.commands.command import Command
from quackinter.stack import Stack
from quackinter.key_injector import KeyInjector

# fmt: off
all_cmds = ['accept', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']
# fmt: on


class GeneralKeyCommand(Command):
    conversion_chart = {
        "CONTROL": "CTRL",
        "WINDOWS": "WIN",
        "GUI": "WIN",
        "APP": "APPS",
        "MENU": "APPS",
        "UPARROW": "UP",
        "DOWNARROW": "DOWN",
        "LEFTARROW": "LEFT",
        "RIGHTARROW": "RIGHT",
        "GLOBE": "FN",
    }
    names = [*conversion_chart.keys(), *[cmd.upper() for cmd in all_cmds]]

    @classmethod
    def _normalize_cmd(cls, cmd: str) -> list[str]:
        new_cmd = cmd.replace("+", "-")
        for key, val in cls.conversion_chart.items():
            new_cmd = new_cmd.replace(key, val)

        new_cmd = new_cmd.split("-")

        return [
            (lowered.lower() if len(lowered) > 1 else lowered) for lowered in new_cmd
        ]

    @classmethod
    def is_this_command(cls, name: str, data: str) -> bool:
        normalized = cls._normalize_cmd(name)

        # Verify first cmd is in our major list
        if normalized[0] not in all_cmds:
            return False

        return all(cmd.lower() in KeyInjector.ACCEPTED_KEYS for cmd in normalized[1:])

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        key_injector = KeyInjector(stack.environment)
        norm_cmd = self._normalize_cmd(cmd)

        norm_data = data.strip().split(" ")
        new_cmd_list = []
        for data_cmd in norm_data:
            new_cmd_list.extend(self._normalize_cmd(data_cmd))

        key_injector.hotkey([*norm_cmd, *new_cmd_list])
