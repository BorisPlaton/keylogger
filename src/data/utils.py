from datetime import datetime, timedelta
from typing import TypedDict

from common.utils import from_str_to_datetime


class UserStatistic(TypedDict):
    SUMMARY_PRESSED_KEYS_QUANTITY: int
    SUMMARY_TIME_PASSED: timedelta
    SUMMARY_AVERAGE_KEY_SPEED: float
    START_TIME: datetime
    END_TIME: datetime


def calculate_user_statistics(statistic: tuple[int, str, str]) -> UserStatistic:
    """
    Вычисляет необходимые данные о статистике пользователя и
    возвращает их.
    """
    keystrokes = statistic[0]
    start_time = from_str_to_datetime('DB_FORMAT', statistic[1])
    end_time = from_str_to_datetime('DB_FORMAT', statistic[2])
    passed_time = end_time - start_time
    typing_speed = get_average_typing_speed(passed_time, keystrokes)
    data: UserStatistic = {
        'SUMMARY_PRESSED_KEYS_QUANTITY': keystrokes,
        'SUMMARY_TIME_PASSED': passed_time,
        'SUMMARY_AVERAGE_KEY_SPEED': typing_speed,
        'START_TIME': start_time,
        'END_TIME': end_time,
    }
    return data


def calculate_summary_user_statistics(statistics_list: list[tuple[int, str, str]]) -> UserStatistic | None:
    """
    Вычисляет общую статистику из списка данных `statistics_list`
    и возвращает результат.
    """
    summary_data: UserStatistic | None = None
    for index, statistic in enumerate(statistics_list):
        data = calculate_user_statistics(statistic)
        if not summary_data:
            summary_data = data
        else:
            summary_data = add_user_statistics(summary_data, data)
    return summary_data


def add_user_statistics(first_statistic: UserStatistic, second_statistic: UserStatistic) -> UserStatistic:
    """Суммирует данные и возвращает их результат."""
    summary_data: UserStatistic = {}
    for key in UserStatistic.__annotations__:
        if key == 'START_TIME':
            summary_data['START_TIME'] = (
                first_statistic['START_TIME']
                if first_statistic['START_TIME'] < second_statistic['START_TIME']
                else second_statistic['START_TIME']
            )
        elif key == 'END_TIME':
            summary_data['END_TIME'] = (
                first_statistic['END_TIME']
                if first_statistic['END_TIME'] > second_statistic['END_TIME']
                else second_statistic['END_TIME']
            )
        else:
            summary_data[key] = first_statistic[key] + second_statistic[key]
    else:
        summary_data['SUMMARY_AVERAGE_KEY_SPEED'] = get_average_typing_speed(
            summary_data['SUMMARY_TIME_PASSED'],
            summary_data['SUMMARY_PRESSED_KEYS_QUANTITY']
        )
    return summary_data


def get_average_typing_speed(time_range: timedelta, key_pressing_amount: int) -> float:
    """Считает среднюю скорость набора текста."""
    minutes_amount = time_range.total_seconds() / 60
    return float('{:.2f}'.format(key_pressing_amount / minutes_amount))
