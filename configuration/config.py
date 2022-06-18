from pathlib import Path

from . import settings as st
from .adds import KeyConfig


class _Config:
    """Класс для получения данных из `configuration.settings`."""

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

    def __init__(self):
        self._config_list = [
            constant for constant in dir(st) if not constant.startswith('__')
        ]   # Не берёт во внимание переменные файла `settings.py` по типу `__file__`, `__name__` и т.д.
        self.setup_config()

    def setup_config(self):
        """Устанавливает значения констант из `configuration.settings`."""
        for constant in self._config_list:
            setattr(self, constant, getattr(st, constant))


config = _Config()
