import logging
from datetime import datetime, timedelta
from typing import Literal

from configuration.settings import settings
from data_storage.storages import KeylogData, Statistic
from output_formatter.logger import OutputLogger


VALID_DATES = Literal[
    'START_TIME', 'SESSION_START_TIME', 'SESSION_END_TIME',
]


class BaseOutput:
    """Базовый класс для вывода информации."""

    def __init__(self):
        """Создаёт экземпляр класса `logging.Logger`."""
        self.logger = OutputLogger(
            '.'.join([__name__, self.__class__.__name__]),
            logging.INFO, stream_log_format='%(message)s'
        ).logger


class KeylogOutput(BaseOutput):
    """Класс для вывода информации о работе программы в командную строку."""

    def show_menu(self):
        """Печатает меню программы."""
        text = settings.MENU_TEXT.format(
            START_KEY=settings.START_KEY.string_format,
            EXIT_KEY=settings.EXIT_KEY.string_format,
        )
        self.logger.info(text)

    def show_key_logging_help_text(self):
        """Печатает дополнительную информация перед началом мониторинга клавиатуры."""
        text = settings.KEY_LOGGING_HELP_TEXT.format(
            START_TIME=KeylogOutput.get_formatted_output_time_for(
                'START_TIME', self.data_storage.start_time
            ),
            STOP_KEY=settings.STOP_KEY.string_format,
        )
        self.logger.info(text)

    def show_keylogger_statistics(self):
        """Печатает статистику мониторинга клавиатуры."""
        text = settings.KEYLOGGER_STATISTICS.format(
            SUMMARY_PRESSED_KEYS_QUANTITY=self.data_storage.summary_pressed_keys_quantity,
            SUMMARY_TIME_PASSED=self.get_formatted_duration_time(self.data_storage.summary_passed_time),
            SUMMARY_AVERAGE_KEY_SPEED="≈" + str(self.data_storage.average_typing_speed),
            LAST_SESSION_AVERAGE_KEY_SPEED="≈" + str(self.data_storage.last_session_typing_speed),
            LAST_SESSION_TIME_PASSED=self.get_formatted_duration_time(self.data_storage.last_session_time),
            LAST_SESSION_PRESSED_KEYS_QUANTITY=str(self.data_storage.last_session_pressed_keys_quantity),
            SESSION_START_TIME=self.get_formatted_output_time_for('SESSION_START_TIME', self.data_storage.start_time),
            SESSION_END_TIME=self.get_formatted_output_time_for('SESSION_END_TIME', self.data_storage.end_time),
        )
        self.logger.info(text)

    @staticmethod
    def get_formatted_duration_time(duration_time: timedelta) -> str:
        """Возвращает отформатированную строку для `datetime.timedelta`."""
        formatted_time = str(duration_time).split('.')[0]
        return formatted_time

    @staticmethod
    def get_formatted_output_time_for(time_moment: VALID_DATES, time: datetime) -> str:
        """
        Возвращает отформатированную строку для `datetime.datetime`.
        Формат времени задается в `configuration.settings.DATA_FORMAT`.
        """
        date_format = settings.DATA_FORMATS[time_moment]
        formatted_time = time.strftime(date_format)
        return formatted_time

    def key_logging_started(self):
        """Обработчик сигнала начала мониторинга клавиатуры."""
        self.show_key_logging_help_text()

    def key_logging_stopped(self):
        """Обработчик сигнала завершения мониторинга клавиатуры."""
        self.show_keylogger_statistics()

    def __init__(self, data_storge: KeylogData):
        """
        Сохраняет хранилище данных, которое передаётся по аргументу
        `data_storge`.
        """
        super().__init__()
        self.data_storage = data_storge


class ResultsOutput(BaseOutput):
    """Класс для вывода информации о статистике пользователя."""

    def __init__(self, data_storge: Statistic):
        """
        Сохраняет хранилище данных, которое передаётся по аргументу
        `data_storge`.
        """
        super().__init__()
        self.data_storage = data_storge

    def show_statistic_for_date(self, statistic_date: str | datetime):
        statistics = self.data_storage.get_records_by_time(statistic_date)
        self.logger.info(statistics)
