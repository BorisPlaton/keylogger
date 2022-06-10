from pathlib import Path

from . import settings as st
from .utils import KeyConfig


class _Config:
    BASE_DIR: Path
    RESULTS_DIR: Path

    TIME_RANGE: int

    START_KEY: KeyConfig
    STOP_KEY: KeyConfig
    EXIT_KEY: KeyConfig

    MENU_TEXT: str
    KEY_LOGGING_HELP_TEXT: str
    KEYLOGGER_STATISTICS: str

    def __init__(self):
        self._config_list = [
            constant for constant in dir(st) if not constant.startswith('__')
        ]
        self.setup_config()

    def setup_config(self):
        for constant in self._config_list:
            setattr(self, constant, getattr(st, constant))


config = _Config()
