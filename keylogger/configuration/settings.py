from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from pynput.keyboard import Key

from configuration.config import Settings


class KeyConfig(NamedTuple):
    key: Key
    string_format: str


@dataclass
class PyConfig:
    BASE_DIR: Path
    RESULT_DIR: Path
    START_KEY: KeyConfig
    STOP_KEY: KeyConfig
    EXIT_KEY: KeyConfig
    DATA_FORMAT: str
    MENU_TEXT: str
    KEY_LOGGING_HELP_TEXT: str
    KEYLOGGER_STATISTICS: str
    TIME_RANGE: int
    WRITE_TO_FILE: bool


settings: PyConfig | Settings = Settings()
settings.setup_from_pyfile('configuration.base_settings')
