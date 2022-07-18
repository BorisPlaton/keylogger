from core.event_channels import Event, event_channel
from database.statistic import statistic_db
from keylogging.keyloggers import KeyboardLogger, MenuKeylogger
from output_formatter.output import TextFormatter
from time_handler.stopwatch import Stopwatch


class Project:
    """
    Класс проекта. Создает все необходимые экземпляры классов и
    настраивает связи между ними. Имеет метод `start`, который отвечает
    за запуск программы.
    """

    def __init__(self):
        """
        Создает экземпляры классов `Keylogger`, `Timer` и `OutputFormatter` для работы
        программы. Также создает благодаря функции `_create_event_relations` необходимые связи
        событий между экземплярами классов.
        """
        self._menu_keylogger = MenuKeylogger()
        self._keylogger = KeyboardLogger()
        self._timer = Stopwatch()
        self._output_formatter = TextFormatter()

        self._create_event_relations()

    def start(self):
        """Запускает выполнение программы"""
        self._menu_keylogger.show_menu()

    def _create_event_relations(self):
        """Устанавливает слушателей на события."""
        event_channel.add_listener(Event.SHOW_MENU, self._output_formatter.show_menu)

        event_channel.add_listeners(
            Event.KEY_LOGGING_STARTED,
            [
                self._timer.key_logging_started,
                self._output_formatter.key_logging_started,
                self._keylogger.key_logging_started
            ]
        )

        event_channel.add_listeners(
            Event.KEY_LOGGING_STOPPED,
            [
                self._timer.key_logging_stopped,
                self._output_formatter.key_logging_stopped,
                statistic_db.key_logging_stopped,
                self._menu_keylogger.key_logging_stopped,
            ]
        )

        event_channel.add_listener(Event.SHOW_STATISTICS, self._output_formatter.show_statistics)
