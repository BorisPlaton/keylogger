from datetime import datetime
from typing import Literal

from configuration.settings import settings


VALID_DATES = Literal[
    'START_TIME', 'SESSION_START_TIME', 'SESSION_END_TIME', 'INPUT_DATE',
    'RESULT_DATE', 'END_TIME', 'DB_FORMAT',
]


def from_datetime_to_str(time_moment: VALID_DATES, convert_time: datetime) -> str:
    """
    Возвращает отформатированную строку для `datetime.datetime`.
    """
    date_format = settings.DATA_FORMATS[time_moment]
    return convert_time.strftime(date_format)


def from_str_to_datetime(time_moment: VALID_DATES, convert_time: str) -> datetime:
    """
    Возвращает экземпляр `datetime` из строки `convert_time`.
    """
    date_format = settings.DATA_FORMATS[time_moment]
    return datetime.strptime(convert_time, date_format)
