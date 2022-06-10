from core.datastuctures import Event
from keylogger.classes import Keylogger
from output_formatter.classes import OutputFormatter
from timer.classes import Stopwatch


def build_project():
    """
    Создает экземпляры классов `Keylogger`, `Timer` и `OutputFormatter` для работы
    программы. Также создает благодаря функции `_create_event_relations` необходимые связи
    событий между экземплярами классов. В конце запускает программу.
    """
    keylogger_ = Keylogger()
    timer_ = Stopwatch()
    output_formatter_ = OutputFormatter()

    _create_event_relations(keylogger_, timer_, output_formatter_)

    keylogger_.start_logging()


def _create_event_relations(keylogger_: Keylogger, timer_: Stopwatch, output_formatter_: OutputFormatter):
    """Создает связи событий между экземплярами классов Keylogger`, `Timer` и `OutputFormatter."""

    keylogger_.add_listener(timer_, Event.KEY_LOGGING_STARTED)
    keylogger_.add_listeners([timer_, output_formatter_], Event.KEY_LOGGING_STOPPED)

    timer_.add_listener(output_formatter_, Event.TIME_PASSED)
