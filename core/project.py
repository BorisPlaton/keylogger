from configuration.config import config
from core.events import Event
from files.file_writer import FileWriter
from keylogging.keyloggers import KeyboardLogger, MenuKeylogger
from output_formatter.output import TextFormatter
from time_handler.stopwatch import Stopwatch


class Project:

    def __init__(self):
        """
        Создает экземпляры классов `Keylogger`, `Timer` и `OutputFormatter` для работы
        программы. Также создает благодаря функции `_create_event_relations` необходимые связи
        событий между экземплярами классов. В конце запускает программу.
        """
        self._menu_keylogger = MenuKeylogger()
        self._keylogger = KeyboardLogger()
        self._timer = Stopwatch()
        self._output_formatter = TextFormatter()
        self._file_writer = FileWriter()

        self._create_event_relations()

    def start(self):
        """Метод запуска проекта"""
        self._menu_keylogger.start_logging()

    @property
    def is_active(self):
        return self._menu_keylogger.is_program_working()

    def _create_event_relations(self):
        """
        Создает связи событий между экземплярами классов `MenuKeylogger`, `Keylogger`,
        `Timer` и `OutputFormatter.
        """
        self._menu_keylogger.add_listener(self._output_formatter, Event.MENU_STARTED)
        self._menu_keylogger.add_listener(self._keylogger, Event.PROGRAM_STARTED)

        self._create_key_logging_started_event_relations()
        self._create_key_logging_stopped_event_relations()

    def _create_key_logging_stopped_event_relations(self):
        listener_list = [self._timer, self._output_formatter, self._menu_keylogger]
        if config.WRITE_TO_FILE:
            listener_list.insert(2, self._file_writer)
        self._keylogger.add_listeners(listener_list, Event.KEY_LOGGING_STOPPED)

    def _create_key_logging_started_event_relations(self):
        listener_list = [self._timer, self._output_formatter]
        self._keylogger.add_listeners(listener_list, Event.KEY_LOGGING_STARTED)
