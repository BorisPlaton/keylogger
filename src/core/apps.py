from datetime import datetime

from data_storage.handlers import StatisticHandler
from data_storage.storages import KeylogData, Statistic
from events.event_channel import Event, EventChannel
from keylogging.keyloggers import KeyboardLogger, MenuKeylogger
from output_formatter.output import KeylogOutput, ResultsOutput
from time_handler.stopwatch import Stopwatch


class Keylogger:
    """
    Класс логирования нажатия клавиш. Создает все необходимые экземпляры
    классов и настраивает связи между ними. Имеет метод `core`, который
    отвечает за запуск программы.
    """

    def start_key_logging(self):
        """Запускает слежение за клавиатурой."""
        self._menu_keylogger.show_menu()

    def _create_event_relations(self):
        """Устанавливает слушателей на события."""
        self._event_chanel.add_listener(Event.SHOW_MENU, self._output_formatter.show_menu)

        self._event_chanel.add_listeners(
            Event.KEY_LOGGING_STARTED,
            [
                self._timer.key_logging_started,
                self._output_formatter.key_logging_started,
                self._keyboard_keylogger.key_logging_started
            ]
        )

        self._event_chanel.add_listeners(
            Event.KEY_LOGGING_STOPPED,
            [
                self._timer.key_logging_stopped,
                self._output_formatter.key_logging_stopped,
                self._statistic_handler.key_logging_stopped,
                self._menu_keylogger.key_logging_stopped,
            ]
        )

    def __init__(self):
        """
        Создает необходимые экземпляры классов для работы программы и
        связи между ними.
        """
        self._event_chanel = EventChannel()
        self._keylogger_data = KeylogData()

        self._menu_keylogger = MenuKeylogger(self._event_chanel)
        self._keyboard_keylogger = KeyboardLogger(self._event_chanel, self._keylogger_data)
        self._timer = Stopwatch(self._keylogger_data)
        self._output_formatter = KeylogOutput(self._keylogger_data)
        self._statistic_handler = StatisticHandler(self._keylogger_data)

        self._create_event_relations()


class Results:
    """
    Класс результатов выполнения программы. Показывает результаты
    нажатия клавиш.
    """

    def show_user_statistic_records(self, results_date: str | datetime, summary: bool = False):
        """
        Показывает все записи результатов пользователя
        за дату `results_date`.
        """
        self._output_formatter.show_user_statistic_records(results_date, summary)

    def __init__(self):
        self._output_formatter = ResultsOutput(Statistic())
