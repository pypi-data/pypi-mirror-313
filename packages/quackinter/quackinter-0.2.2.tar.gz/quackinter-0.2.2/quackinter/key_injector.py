import typing
import platform as pf

import pyautogui as pyag
import pyperclip as pyclip

from quackinter.environment import Environment
from quackinter.errors import KeyNotExistError

# fmt: off
AcceptedKeysType = typing.Literal['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']
# fmt: on

accepted_keys = typing.get_args(AcceptedKeysType)


class KeyInjector:
    ACCEPTED_KEYS = accepted_keys

    def __init__(self, env: Environment):
        self.environment = env

    @property
    def char_interval(self):
        """
        The global string character interval
        in seconds.
        """
        return self.environment.global_vars.get("_DEFAULT_STRING_DELAY", 80) / 1000

    @classmethod
    def is_key(cls, key: str):
        return cls.normalize(key).lower() in cls.ACCEPTED_KEYS

    @classmethod
    def normalize(cls, key: str):
        return key.replace("GUI", "WIN").replace("WINDOWS", "WIN")

    def _verify_key(self, key: str):
        new_key = self.normalize(key)
        if not self.is_key(new_key):
            raise KeyNotExistError(f"{key} is not a valid key.")
        return new_key

    def press(self, key: str, char_override: int|None = None):
        pyag.press(self._verify_key(key), interval=(char_override/1000) if char_override is not None else self.char_interval)

    def write(self, text: str, interval_override: None | int = None):
        interval = (
            interval_override / 1000
            if interval_override is not None
            else self.char_interval
        )
        pyag.write(text, interval=interval)

    def copy_paste_write(self, text: str, interval_override: None | int = None):
        interval = (
            interval_override
            if interval_override is not None
            else self.char_interval * 1000
        )
        old_clipboard_data = pyclip.paste()
        for char in text:
            pyclip.copy(char)
            if pf.system() == "Darwin":
                self.hotkey(["command", "v"], interval_override=interval)
            else:
                self.hotkey(["ctrl", "v"], interval_override=interval)
        pyclip.copy(old_clipboard_data)

    def hotkey(self, hotkeys: list[str], interval_override: None | int = None):
        interval = (
            interval_override / 1000
            if interval_override is not None
            else self.char_interval
        )
        keys = [(key.lower() if len(key) > 1 else key) for key in hotkeys if key]
        pyag.hotkey(
            *[self._verify_key(key) for key in keys],
            interval=interval,
        )

    def hold(self, key: str | list[str]):
        new_key = [key] if isinstance(key, str) else key
        return pyag.hold([self._verify_key(key) for key in new_key if key])

    def key_down(self, key: str):
        pyag.keyDown(self._verify_key(key))

    def key_up(self, key: str):
        pyag.keyUp(self._verify_key(key))
