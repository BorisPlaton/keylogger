from datetime import datetime, timedelta
from typing import NamedTuple, TypedDict


class DataHandlerValues(NamedTuple):
    summary_passed_time: timedelta
    summary_pressed_keys_quantity: int
    summary_average_key_speed: float
    last_session_passed_time: timedelta
    last_session_pressed_keys_quantity: int
    last_session_average_key_speed: float
    start_time: datetime
    end_time: datetime


class OutputFormattedData(TypedDict):
    SUMMARY_PRESSED_KEYS_QUANTITY: str
    SUMMARY_TIME_PASSED: str
    SUMMARY_AVERAGE_KEY_SPEED: str
    LAST_SESSION_AVERAGE_KEY_SPEED: str
    LAST_SESSION_PASSED_PASSED: str
    LAST_SESSION_PRESSED_KEYS_QUANTITY: str
    START_TIME: str
    END_TIME: str
