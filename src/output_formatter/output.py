import logging
from datetime import datetime

from common.utils import from_str_to_datetime
from configuration.settings import settings
from data_storage.storages import KeylogData, Statistic
from data_storage.utils import (
    calculate_summary_user_statistics, calculate_user_statistics, get_average_typing_speed
)
from output_formatter.logger import OutputLogger
from output_formatter.utils import (
    get_formatted_duration_time, from_datetime_to_str, get_formatted_user_result
)


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
            START_TIME=from_datetime_to_str(
                'START_TIME', self.data_storage.start_time
            ),
            STOP_KEY=settings.STOP_KEY.string_format,
        )
        self.logger.info(text)

    def show_keylogger_statistics(self):
        """Печатает статистику мониторинга клавиатуры."""
        text = settings.KEYLOGGER_STATISTICS.format(
            SUMMARY_PRESSED_KEYS_QUANTITY=self.data_storage.summary_pressed_keys_quantity,
            SUMMARY_TIME_PASSED=get_formatted_duration_time(self.data_storage.summary_passed_time),
            SUMMARY_AVERAGE_KEY_SPEED="≈" + str(get_average_typing_speed(
                self.data_storage.summary_passed_time,
                self.data_storage.summary_pressed_keys_quantity,
            )),
            LAST_SESSION_AVERAGE_KEY_SPEED="≈" + str(get_average_typing_speed(
                self.data_storage.last_session_time,
                self.data_storage.last_session_pressed_keys_quantity,
            )),
            LAST_SESSION_TIME_PASSED=get_formatted_duration_time(self.data_storage.last_session_time),
            LAST_SESSION_PRESSED_KEYS_QUANTITY=str(self.data_storage.last_session_pressed_keys_quantity),
            SESSION_START_TIME=from_datetime_to_str('SESSION_START_TIME', self.data_storage.start_time),
            SESSION_END_TIME=from_datetime_to_str('SESSION_END_TIME', self.data_storage.end_time),
        )
        self.logger.info(text)

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

    def show_user_statistic_records(self, statistic_date: str | datetime, summary: bool = False):
        """Показывает записи статистики пользователя за дату `statistic_date`."""
        try:
            statistic_date = self.convert_input_date_to_datetime(statistic_date)
        except ValueError:
            return self.logger.info(
                "`%s` is wrong date format. "
                "Check if your spelling matches the `%s` format." % (
                    statistic_date, settings.DATA_FORMATS['INPUT_DATE']
                )
            )

        if statistics_list := self.data_storage.get_records_by_time(statistic_date):
            self.logger.info('')
            (
                self._show_summary_user_statistics(statistics_list, statistic_date) if summary
                else self._show_user_statistics_separately(statistics_list, statistic_date)
            )
        else:
            self.logger.info(
                "No data for `%s`." % from_datetime_to_str('RESULT_DATE', statistic_date)
            )

    def _show_summary_user_statistics(self, statistics_list: list, statistic_date):
        """Показывает общую статистику за день."""
        summary_data = calculate_summary_user_statistics(statistics_list)
        self.logger.info(
            get_formatted_user_result(summary_data, statistic_date, True)
        )

    def _show_user_statistics_separately(self, statistics_list: list, statistic_date):
        """Показывает все записи статистики за день."""
        for amount, statistic in enumerate(statistics_list):
            self.logger.info(
                f"{amount + 1}. " + get_formatted_user_result(
                    calculate_user_statistics(statistic),
                    statistic_date
                )
            )

    @staticmethod
    def convert_input_date_to_datetime(statistic_date: str | datetime) -> datetime:
        """Преобразует данные из `statistic_date` типа `str` в тип `datetime`."""
        return (
            from_str_to_datetime('INPUT_DATE', statistic_date)
            if not isinstance(statistic_date, datetime)
            else statistic_date
        )

    def __init__(self, data_storage: Statistic):
        """
        Сохраняет хранилище данных, которое передаётся аргументом
        `data_storage`.
        """
        super().__init__()
        self.data_storage = data_storage
