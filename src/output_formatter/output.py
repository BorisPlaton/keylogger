from datetime import datetime, timedelta
from typing import TypedDict

from configuration.settings import settings
from data_storage.handlers import KeylogDataHandler


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

    @staticmethod
    def show_menu():
        """Печатает меню программы."""
        text = settings.MENU_TEXT.format(
            START_KEY=settings.START_KEY.string_format,
            EXIT_KEY=settings.EXIT_KEY.string_format,
        )
        print(text)

    def show_key_logging_help_text(self):
        """Печатает дополнительную информация перед началом мониторинга клавиатуры."""
        text = settings.KEY_LOGGING_HELP_TEXT.format(
            START_TIME=TextFormatter.get_formatted_output_time(self.storage_handler.storage.start_time),
            STOP_KEY=settings.STOP_KEY.string_format,
        )
        print(text)

    def show_keylogger_statistics(self):
        """Печатает статистику мониторинга клавиатуры."""
        text = settings.KEYLOGGER_STATISTICS.format(
            SUMMARY_PRESSED_KEYS_QUANTITY=self.storage_handler.storage.summary_pressed_keys_quantity,
            SUMMARY_TIME_PASSED=self.get_formatted_duration_time(self.storage_handler.storage.summary_passed_time),
            SUMMARY_AVERAGE_KEY_SPEED="≈" + str(self.storage_handler.average_typing_speed),
            LAST_SESSION_AVERAGE_KEY_SPEED="≈" + str(self.storage_handler.last_session_typing_speed),
            LAST_SESSION_PASSED_PASSED=self.get_formatted_duration_time(self.storage_handler.last_session_time),
            LAST_SESSION_PRESSED_KEYS_QUANTITY=str(self.storage_handler.storage.last_session_pressed_keys_quantity),
            START_TIME=self.get_formatted_output_time(self.storage_handler.storage.start_time),
            END_TIME=self.get_formatted_output_time(self.storage_handler.storage.end_time),
        )
        print(text)

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

    def __init__(self, data_storge: KeylogDataHandler):
        self.storage_handler = data_storge
