from core.events import Event
from keylogging.keyloggers import KeyboardLogger, MenuKeylogger
from output_formatter.classes import OutputFormatter
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
        self._output_formatter = OutputFormatter()

        self._create_event_relations()

    def start(self):
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

        self._keylogger.add_listener(self._timer, Event.KEY_LOGGING_STARTED)
        self._keylogger.add_listeners(
            [self._timer, self._output_formatter, self._menu_keylogger], Event.KEY_LOGGING_STOPPED
        )

        self._timer.add_listener(self._output_formatter, Event.TIME_PASSED)
