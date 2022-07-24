from enum import Enum, auto
from functools import wraps

from events.exceptions import WrongEventName


class Event(Enum):
    KEY_LOGGING_STOPPED = auto()
    KEY_LOGGING_STARTED = auto()
    SHOW_STATISTICS = auto()
    SHOW_MENU = auto()


def is_event_correct(func):
    """
    Проверяет, что событие класса `start.events.Event` существует,
    иначе вызывается исключение `start.exceptions.WrongEventName`
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args + tuple(kwargs.values()):
            if isinstance(arg, Event):
                return func(*args, **kwargs)
        else:
            raise WrongEventName("Неправильное название события")

    return wrapper
