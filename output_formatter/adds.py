from datetime import datetime, timedelta
from enum import Enum
from typing import NamedTuple, TypedDict


class WPMDescription(NamedTuple):
    words_per_minute: str
    description: str


class WordsPerMinuteTypes(Enum):
    SLOW = WPMDescription("<24 wpm", "медленная")
    AVERAGE = WPMDescription("24-32 wpm", "средняя")
    MEDIUM = WPMDescription("32-52 wpm", "хорошая")
    GOOD = WPMDescription("52-70 wpm", "быстрая")
    HIGH = WPMDescription("70-80 wpm", "высокая")
    PROFESSIONAL = WPMDescription(">80 wpm", "профессиональная")


class DataHandlerValues(NamedTuple):
    summary_passed_time: timedelta
    summary_pressed_keys_quantity: int
    summary_average_key_speed: float
    summary_wpm: WordsPerMinuteTypes
    last_session_passed_time: timedelta
    last_session_pressed_keys_quantity: int
    last_session_average_key_speed: float
    last_session_wpm: WordsPerMinuteTypes
    start_time: datetime
    end_time: datetime


class OutputFormattedData(TypedDict):
    SUMMARY_PRESSED_KEYS_QUANTITY: str
    SUMMARY_TIME_PASSED: str
    SUMMARY_AVERAGE_KEY_SPEED: str
    SUMMARY_WPM: str
    LAST_SESSION_AVERAGE_KEY_SPEED: str
    LAST_SESSION_PASSED_PASSED: str
    LAST_SESSION_PRESSED_KEYS_QUANTITY: str
    LAST_SESSION_WPM: str
    START_TIME: str
    END_TIME: str
