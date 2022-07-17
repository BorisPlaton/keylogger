from configuration.config import config
from core.event_channels import Event, event_channel
from files.file_writer import FileWriter
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
        self._file_writer = FileWriter()

        self._create_event_relations()

    def start(self):
        """Запускает выполнение программы"""
        self._menu_keylogger.start_logging()

    @property
    def is_active(self):
        return self._menu_keylogger.is_program_working()

    def _create_event_relations(self):
        """Устанавливает слушателей на события."""
        event_channel.add_listener(Event.MENU_STARTED, self._output_formatter.menu_started)
        event_channel.add_listener(Event.PROGRAM_STARTED, self._keylogger.program_started)

        event_channel.add_listeners(
            Event.KEY_LOGGING_STARTED,
            [self._timer.key_logging_started, self._output_formatter.key_logging_started]
        )

        event_channel.add_listeners(
            Event.KEY_LOGGING_STOPPED,
            [
                self._timer.key_logging_stopped,
                self._file_writer.key_logging_stopped,
                self._output_formatter.key_logging_stopped,
                self._menu_keylogger.key_logging_stopped,
            ]
            if config.WRITE_TO_FILE else
            [
                self._timer.key_logging_stopped,
                self._output_formatter.key_logging_stopped,
                self._menu_keylogger.key_logging_stopped,
            ]
        )
