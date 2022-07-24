from enum import Enum, auto

from data_storage.handlers import KeylogDataHandler, StatisticHandler
from data_storage.storages import KeylogData
from events.event_channel import Event, EventChannel
from keylogging.keyloggers import KeyboardLogger, MenuKeylogger
from output_formatter.output import TextFormatter
from start.exceptions import WrongProgramTypeError
from time_handler.stopwatch import Stopwatch


class BaseProgram:
    """Интерфейс для запуска программы."""

    def start(self):
        """Запускает выполнение программы."""
        raise NotImplementedError("Невозможно запустить программу.")


class Keylog(BaseProgram):
    """
    Класс логирования нажатия клавиш. Создает все необходимые экземпляры
    классов и настраивает связи между ними. Имеет метод `start`, который
    отвечает за запуск программы.
    """

    def start(self):
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
        Создает экземпляры классов `Keylogger`, `Timer` и `OutputFormatter` для работы
        программы. Также создает благодаря методу `Project._create_event_relations`
        необходимые связи событий между экземплярами классов.
        """
        self._event_chanel = EventChannel()
        self._data_handler = KeylogDataHandler(KeylogData())

        self._menu_keylogger = MenuKeylogger(self._event_chanel)
        self._keyboard_keylogger = KeyboardLogger(self._event_chanel, self._data_handler.storage)
        self._timer = Stopwatch(self._data_handler.storage)
        self._output_formatter = TextFormatter()
        self._statistic_handler = StatisticHandler(self._data_handler.storage)

        self._create_event_relations()


class Results(BaseProgram):
    """
    Класс результатов выполнения программы. Показывает результаты
    нажатия клавиш.
    """

    def start(self):
        print('hello from results')


class ProgramType(Enum):
    KEYLOGGER = auto()
    RESULTS = auto()


def get_program(program_type: ProgramType) -> type(BaseProgram):
    """Фабрика, возвращающая экземпляр класса для запуска программы."""
    match True:
        case True if program_type is ProgramType.KEYLOGGER:
            return Keylog()
        case True if program_type is ProgramType.RESULTS:
            return Results()
        case _:
            raise WrongProgramTypeError("Неверный аргумент %s" % program_type)
