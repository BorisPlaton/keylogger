from datetime import timedelta

from common.utils import from_datetime_to_str
from configuration.settings import settings
from data_storage.utils import UserStatistic


def get_formatted_duration_time(duration_time: timedelta) -> str:
    """Возвращает отформатированную строку для `datetime.timedelta`."""
    formatted_time = str(duration_time).split('.')[0]
    return formatted_time


def get_formatted_user_result(statistic: UserStatistic, result_date, summary=False) -> str:
    """Возвращает отформатированную строку статистики пользователя."""
    format_data = {
        'SUMMARY_TIME_PASSED': get_formatted_duration_time(statistic['SUMMARY_TIME_PASSED']),
        'SUMMARY_AVERAGE_KEY_SPEED': statistic['SUMMARY_AVERAGE_KEY_SPEED'],
        'SUMMARY_PRESSED_KEYS_QUANTITY': statistic['SUMMARY_PRESSED_KEYS_QUANTITY'],
        'RESULT_DATE': from_datetime_to_str('RESULT_DATE', result_date)
    }
    if not summary:
        format_data.update(
            {
                'START_TIME': from_datetime_to_str('START_TIME', statistic['START_TIME']),
                'END_TIME': from_datetime_to_str('END_TIME', statistic['END_TIME']),
            }
        )
    format_text = settings.SUMMARY_RESULT_STATISTICS if summary else settings.RESULT_STATISTICS
    return format_text.format(**format_data)
