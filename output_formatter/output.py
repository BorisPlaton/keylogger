import threading
from datetime import datetime, timedelta

from configuration.config import config
from core.events import EventListener
from data_handler.adds import DataHandlerValues, WPMDescription
from data_handler.storage import data_storage
from data_handler.utils import get_data_from_data_handler
from output_formatter.adds import OutputFormattedData


class TextFormatter(EventListener):
    """Класс для вывода информации о работе программы в командную строку."""

    def __init__(self):
        self.locker = threading.RLock()

    def show_menu(self):
        """Печатает меню программы."""
        with self.locker:
            print(self.get_menu_text())

    def show_key_logging_help_text(self):
        """Печатает дополнительную информация перед началом мониторинга клавиатуры."""
        with self.locker:
            print(self.get_formatted_keylogger_help_text())

    def show_keylogger_statistics(self):
        """Печатает статистику мониторинга клавиатуры."""
        with self.locker:
            print(self.get_formatted_keylogger_statistics())

    @staticmethod
    def get_menu_text() -> str:
        """Возвращает отформатированную строку с меню программы."""
        text = config.MENU_TEXT.format(
            START_KEY=config.START_KEY.string_format,
            EXIT_KEY=config.EXIT_KEY.string_format
        )
        return text

    @staticmethod
    def get_formatted_keylogger_help_text() -> str:
        """Возвращает отформатированную строку с помощью по работе программы."""
        text = config.KEY_LOGGING_HELP_TEXT.format(
            START_TIME=TextFormatter.get_formatted_output_time(data_storage.start_time),
            STOP_KEY=config.STOP_KEY.string_format,
        )
        return text

    @staticmethod
    def get_formatted_keylogger_statistics() -> str:
        """Возвращает отформатированную строку с результатами выполнения программы."""
        formatted_data = TextFormatter.get_formatted_output_data(get_data_from_data_handler())
        text = config.KEYLOGGER_STATISTICS.format(**formatted_data)
        return text

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
        formatted_time = time.strftime(config.DATA_FORMAT)
        return formatted_time

    @staticmethod
    def get_formatted_output_data(data: DataHandlerValues) -> OutputFormattedData:
        """Набор данных для вывода в командную строку."""
        formatted_output_data = OutputFormattedData(
            SUMMARY_PRESSED_KEYS_QUANTITY=data_storage.summary_pressed_keys_quantity,
            SUMMARY_TIME_PASSED=TextFormatter.get_formatted_duration_time(data.summary_passed_time),
            SUMMARY_AVERAGE_KEY_SPEED="≈" + str(data.summary_average_key_speed),
            SUMMARY_WPM=TextFormatter.get_formatted_wpm(data.summary_wpm.value),
            LAST_SESSION_AVERAGE_KEY_SPEED="≈" + str(data.last_session_average_key_speed),
            LAST_SESSION_PASSED_PASSED=TextFormatter.get_formatted_duration_time(data.last_session_passed_time),
            LAST_SESSION_PRESSED_KEYS_QUANTITY=str(data.last_session_pressed_keys_quantity),
            LAST_SESSION_WPM=TextFormatter.get_formatted_wpm(data.last_session_wpm.value),
            START_TIME=TextFormatter.get_formatted_output_time(data.start_time),
            END_TIME=TextFormatter.get_formatted_output_time(data.end_time),
        )
        return formatted_output_data

    @staticmethod
    def get_formatted_wpm(wpm: WPMDescription):
        formatted_wpm = ', '.join([wpm.words_per_minute, wpm.description])
        return formatted_wpm

    def key_logging_started(self):
        """Обработчик сигнала начала мониторинга клавиатуры."""
        self.show_key_logging_help_text()

    def key_logging_stopped(self):
        """Обработчик сигнала завершения мониторинга клавиатуры."""
        self.show_keylogger_statistics()

    def menu_started(self):
        """Обработчик сигнала запуска меню программы."""
        self.show_menu()
