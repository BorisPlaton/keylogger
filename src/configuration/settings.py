from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from configuration.config import Settings


class KeyConfig(NamedTuple):
    key: int | str
    string_format: str


@dataclass
class PyConfig:
    BASE_DIR: Path
    RESULT_DIR: Path
    START_KEY: KeyConfig
    STOP_KEY: KeyConfig
    EXIT_KEY: KeyConfig
    DATA_FORMATS: dict[str, str]
    MENU_TEXT: str
    KEY_LOGGING_HELP_TEXT: str
    KEYLOGGER_STATISTICS: str
    DB_LOCATION: str | Path
    SUMMARY_RESULT_STATISTICS: str
    RESULT_STATISTICS: str


settings: PyConfig | Settings = Settings()
settings.setup_from_pyfile('configuration.base_settings')
