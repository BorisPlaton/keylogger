from datetime import timedelta

from data_handler.storage import data_storage as ds
from output_formatter.adds import DataHandlerValues


def get_average_key_speed(time_range: timedelta, key_pressing_amount: int) -> float:
    """Считает примерную, среднюю скорость набора текста."""
    minutes_amount = float("{:.2f}".format(time_range.total_seconds() / 60))
    return float("{:.2f}".format(key_pressing_amount / minutes_amount))


def get_data_from_data_handler() -> DataHandlerValues:
    """
    Возвращает все значения из хранилища данных `data_handler.storage.DataHandler` и
    среднюю скорость набора текста за последнюю сессию и за всё время выполнения программы.
    """
    summary_pressed_keys_quantity = ds.summary_pressed_keys_quantity
    summary_passed_time = ds.summary_passed_time
    last_session_pressed_keys_quantity = ds.last_session_pressed_keys_quantity
    last_session_passed_time = ds.time_passed
    data = DataHandlerValues(
        summary_pressed_keys_quantity=summary_pressed_keys_quantity,
        summary_passed_time=summary_passed_time,
        summary_average_key_speed=get_average_key_speed(summary_passed_time, summary_pressed_keys_quantity),
        last_session_passed_time=last_session_passed_time,
        last_session_average_key_speed=get_average_key_speed(
            last_session_passed_time, last_session_pressed_keys_quantity),
        last_session_pressed_keys_quantity=last_session_pressed_keys_quantity,
        start_time=ds.start_time,
        end_time=ds.end_time,
    )
    return data
