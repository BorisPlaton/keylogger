from datetime import timedelta, datetime
from enum import Enum
from typing import NamedTuple

from data_handler.storage import data_storage as ds


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


def get_average_key_speed(time_range: timedelta, key_pressing_amount: int) -> float:
    """Считает примерную, среднюю скорость набора текста."""
    minutes_amount = float("{:.2f}".format(time_range.total_seconds() / 60))
    return float("{:.2f}".format(key_pressing_amount / minutes_amount))


def get_wpm(key_speed: float | int) -> WordsPerMinuteTypes:
    """Анализирует скорость набора текста, и возвращает результат."""
    match key_speed:
        case key_speed if key_speed < 120:
            return WordsPerMinuteTypes.SLOW
        case key_speed if 120 <= key_speed < 160:
            return WordsPerMinuteTypes.AVERAGE
        case key_speed if 160 <= key_speed < 260:
            return WordsPerMinuteTypes.MEDIUM
        case key_speed if 260 <= key_speed < 350:
            return WordsPerMinuteTypes.GOOD
        case key_speed if 350 <= key_speed < 400:
            return WordsPerMinuteTypes.HIGH
        case key_speed if key_speed >= 400:
            return WordsPerMinuteTypes.PROFESSIONAL
        case _:
            raise ValueError(f"Неправильное значение key_speed '{key_speed}'")


def get_data_from_data_handler() -> DataHandlerValues:
    """
    Возвращает все значения из хранилища данных `data_handler.storage.DataHandler` и
    среднюю скорость набора текста за последнюю сессию и за всё время выполнения программы.
    """
    summary_pressed_keys_quantity = ds.summary_pressed_keys_quantity
    summary_passed_time = ds.summary_passed_time
    last_session_pressed_keys_quantity = ds.last_session_pressed_keys_quantity
    last_session_passed_time = ds.time_passed
    last_session_average_key_speed = get_average_key_speed(
        last_session_passed_time, last_session_pressed_keys_quantity)
    summary_average_key_speed = get_average_key_speed(summary_passed_time, summary_pressed_keys_quantity)

    data = DataHandlerValues(
        summary_pressed_keys_quantity=summary_pressed_keys_quantity,
        summary_passed_time=summary_passed_time,
        summary_average_key_speed=summary_average_key_speed,
        summary_wpm=get_wpm(summary_average_key_speed),
        last_session_passed_time=last_session_passed_time,
        last_session_average_key_speed=last_session_average_key_speed,
        last_session_pressed_keys_quantity=last_session_pressed_keys_quantity,
        last_session_wpm=get_wpm(last_session_average_key_speed),
        start_time=ds.start_time,
        end_time=ds.end_time,
    )
    return data
