from datetime import timedelta, datetime
from typing import Literal, TypedDict

from configuration.settings import settings

VALID_DATES = Literal[
    'START_TIME', 'SESSION_START_TIME', 'SESSION_END_TIME', 'INPUT_DATE',
    'RESULT_DATE', 'END_TIME',
]


class UserStatistic(TypedDict):
    SUMMARY_PRESSED_KEYS_QUANTITY: int
    SUMMARY_TIME_PASSED: timedelta | str
    SUMMARY_AVERAGE_KEY_SPEED: float
    START_TIME: str | datetime
    END_TIME: datetime


def get_formatted_duration_time(duration_time: timedelta) -> str:
    """Возвращает отформатированную строку для `datetime.timedelta`."""
    formatted_time = str(duration_time).split('.')[0]
    return formatted_time


def convert_to_str_for(time_moment: VALID_DATES, convert_time: datetime) -> str:
    """
    Возвращает отформатированную строку для `datetime.datetime`.
    """
    date_format = settings.DATA_FORMATS[time_moment]
    return convert_time.strftime(date_format)


def convert_to_datetime_for(time_moment: VALID_DATES, convert_time: str) -> datetime:
    """
    Возвращает экземпляр `datetime` из строки для `convert_time`.
    """
    date_format = settings.DATA_FORMATS[time_moment]
    return datetime.strptime(convert_time, date_format)


def get_formatted_user_result(statistic: UserStatistic, result_date):
    """Возвращает отформатированную строку статистики пользователя."""
    statistic.update(
        {
            'SUMMARY_TIME_PASSED': get_formatted_duration_time(statistic['SUMMARY_TIME_PASSED']),
            'START_TIME': convert_to_str_for('START_TIME', statistic['START_TIME']),
            'END_TIME': convert_to_str_for('END_TIME', statistic['END_TIME']),
        }
    )
    text = settings.RESULT_STATISTICS.format(
        **statistic, RESULT_DATE=convert_to_str_for('RESULT_DATE', result_date)
    )
    return text


def calculate_user_statistic(statistic: tuple[int, str, str]) -> UserStatistic:
    """
    Вычисляет необходимые данные о статистике пользователя и
    возвращает их.
    """
    keystrokes = statistic[0]
    passed_time = get_passed_time(statistic[1], statistic[2])
    typing_speed = get_average_typing_speed(passed_time, keystrokes)
    print(statistic)
    data: UserStatistic = {
        'SUMMARY_PRESSED_KEYS_QUANTITY': keystrokes,
        'SUMMARY_TIME_PASSED': passed_time,
        'SUMMARY_AVERAGE_KEY_SPEED': typing_speed,
        'START_TIME': convert_to_datetime_for('START_TIME', statistic[1]),
        'END_TIME': convert_to_datetime_for('END_TIME', statistic[1]),
    }
    return data


def get_summary_user_statistic(statistics_list: list[tuple[int, str, str]]) -> UserStatistic:
    """
    Вычисляет общую статистику из списка данных `statistics_list`
    и возвращает результат.
    """
    summary_data: UserStatistic = {
        'SUMMARY_PRESSED_KEYS_QUANTITY': 0,
        'SUMMARY_TIME_PASSED': timedelta(),
        'SUMMARY_AVERAGE_KEY_SPEED': 0,
        'START_TIME': '',
        'END_TIME': '',

    }
    for index, statistic in enumerate(statistics_list):
        data = calculate_user_statistic(statistic)
        if not summary_data['START_TIME']:
            summary_data['START_TIME'] = data['START_TIME']
        if index == len(statistics_list) - 1:
            summary_data['END_TIME'] = data['END_TIME']
        summary_data['SUMMARY_PRESSED_KEYS_QUANTITY'] += data['SUMMARY_PRESSED_KEYS_QUANTITY']
        summary_data['SUMMARY_TIME_PASSED'] += data['SUMMARY_TIME_PASSED']
    else:
        summary_data.update(
            {
                'SUMMARY_AVERAGE_KEY_SPEED': get_average_typing_speed(
                    summary_data['SUMMARY_TIME_PASSED'],
                    summary_data['SUMMARY_PRESSED_KEYS_QUANTITY']
                ),
            }
        )

    return summary_data


def get_passed_time(
        start: datetime | str,
        end: datetime | str,
        time_format: str = '%Y-%m-%d %H:%M:%S.%f') -> timedelta:
    """
    Форматирует дату из строки в `datetime.datetime`
    и ищет разницу во времени.
    """
    start = datetime.strptime(start, time_format) if isinstance(start, str) else start
    end = datetime.strptime(end, time_format) if isinstance(end, str) else end
    return end - start


def get_average_typing_speed(time_range: timedelta, key_pressing_amount: int) -> float:
    """Считает среднюю скорость набора текста."""
    minutes_amount = time_range.total_seconds() / 60
    return float('{:.2f}'.format(key_pressing_amount / minutes_amount))
