import threading
from datetime import datetime, timedelta
from typing import TypedDict

from configuration.settings import settings
from data_handler.storage import data_storage
from data_handler.utils import get_data_from_data_handler


class OutputFormattedData(TypedDict):
    SUMMARY_PRESSED_KEYS_QUANTITY: str
    SUMMARY_TIME_PASSED: str
    SUMMARY_AVERAGE_KEY_SPEED: str
    LAST_SESSION_AVERAGE_KEY_SPEED: str
    LAST_SESSION_PASSED_PASSED: str
    LAST_SESSION_PRESSED_KEYS_QUANTITY: str
    START_TIME: str
    END_TIME: str


class TextFormatter:
    """Класс для вывода информации о работе программы в командную строку."""

    def __init__(self):
        super().__init__()
        self.locker = threading.RLock()

    def show_menu(self):
        """Печатает меню программы."""
        with self.locker:
            text = settings.MENU_TEXT.format(
                START_KEY=settings.START_KEY.string_format,
                EXIT_KEY=settings.EXIT_KEY.string_format,
                SHOW_RESULTS_KEY=settings.SHOW_RESULTS_KEY.string_format,
            )
            print(text)

    def show_key_logging_help_text(self):
        """Печатает дополнительную информация перед началом мониторинга клавиатуры."""
        with self.locker:
            text = settings.KEY_LOGGING_HELP_TEXT.format(
                START_TIME=TextFormatter.get_formatted_output_time(data_storage.start_time),
                STOP_KEY=settings.STOP_KEY.string_format,
            )
            print(text)

    def show_keylogger_statistics(self):
        """Печатает статистику мониторинга клавиатуры."""
        with self.locker:
            data = get_data_from_data_handler()
            text = settings.KEYLOGGER_STATISTICS.format(
                SUMMARY_PRESSED_KEYS_QUANTITY=data_storage.summary_pressed_keys_quantity,
                SUMMARY_TIME_PASSED=TextFormatter.get_formatted_duration_time(data.summary_passed_time),
                SUMMARY_AVERAGE_KEY_SPEED="≈" + str(data.summary_average_key_speed),
                LAST_SESSION_AVERAGE_KEY_SPEED="≈" + str(data.last_session_average_key_speed),
                LAST_SESSION_PASSED_PASSED=TextFormatter.get_formatted_duration_time(data.last_session_passed_time),
                LAST_SESSION_PRESSED_KEYS_QUANTITY=str(data.last_session_pressed_keys_quantity),
                START_TIME=TextFormatter.get_formatted_output_time(data.start_time),
                END_TIME=TextFormatter.get_formatted_output_time(data.end_time),
            )
            print(text)

    def show_statistics(self):
        print('Это тип статистика еси чо')

    @staticmethod
    def get_formatted_duration_time(duration_time: timedelta) -> str:
        """Возвращает отформатированную строку для `datetime.timedelta`."""
        formatted_time = str(duration_time).split('.')[0]
        return formatted_time

    @staticmethod
    def get_formatted_output_time(time: datetime):
        """
        Возвращает отформатированную строку для `datetime.datetime`.
        Формат времени задается в `configuration.settings.DATA_FORMAT`.
        """
        formatted_time = time.strftime(settings.DATA_FORMAT)
        return formatted_time

    def key_logging_started(self):
        """Обработчик сигнала начала мониторинга клавиатуры."""
        self.show_key_logging_help_text()

    def key_logging_stopped(self):
        """Обработчик сигнала завершения мониторинга клавиатуры."""
        self.show_keylogger_statistics()
