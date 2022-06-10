import threading
from datetime import datetime, timedelta

from configuration.config import config
from core.events import EventListener
from data_handler.classes import data_storage


class OutputFormatter(EventListener):

    def __init__(self):
        self.locker = threading.RLock()

    def show_menu(self):
        """Вывод меню для начала или прекращения работы программы."""
        with self.locker:
            print(config.MENU_TEXT.format(
                START_KEY=config.START_KEY.string_format,
                EXIT_KEY=config.EXIT_KEY.string_format
            ))

    def show_key_logging_help_text(self):
        """Дополнительная информация, что выводится перед началом мониторинга клавиатуры."""
        with self.locker:
            print(config.KEY_LOGGING_HELP_TEXT.format(
                START_TIME=self._get_formatted_output_time(data_storage.start_time),
                STOP_KEY=config.STOP_KEY.string_format
            ))

    def show_keylogger_statistics(self):
        with self.locker:
            print(config.KEYLOGGER_STATISTICS.format(
                START_TIME=self._get_formatted_output_time(data_storage.start_time),
                END_TIME=self._get_formatted_output_time(data_storage.end_time),
                DURATION=self._get_formatted_duration_time(data_storage.duration_time),
                PRESSED_KEYS_QUANTITY=data_storage.pressed_keys_quantity,
            ))

    def key_logging_started(self):
        """Обработчик сигнала начала мониторинга клавиатуры."""
        self.show_key_logging_help_text()

    def key_logging_stopped(self):
        """Обработчик сигнала завершения мониторинга клавиатуры."""
        self.show_keylogger_statistics()

    def menu_started(self):
        """Обработчик сигнала запуска меню программы."""
        self.show_menu()

    @staticmethod
    def _get_formatted_duration_time(duration_time: timedelta):
        formatted_time = str(duration_time).split('.')[0]
        return formatted_time

    @staticmethod
    def _get_formatted_output_time(time: datetime):
        formatted_time = time.strftime("%d %b, %H:%M")
        return formatted_time
