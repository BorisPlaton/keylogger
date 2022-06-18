from typing import NamedTuple

from pynput.keyboard import Key


class KeyConfig(NamedTuple):
    key: Key
    string_format: str
