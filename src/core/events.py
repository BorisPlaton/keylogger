from enum import Enum
from functools import wraps

from core.exceptions import WrongEventName


class Event(Enum):
    TIME_PASSED = 'time_passed'
    KEY_LOGGING_STOPPED = 'time_stopped'
    KEY_LOGGING_STARTED = 'time_started'
    SHOW_STATISTICS = 'show_statistics'
    SHOW_MENU = 'menu_started'


def is_event_correct(func):
    """
    Проверяет, что событие класса `core.events.Event` существует,
    иначе вызывается исключение `core.exceptions.WrongEventName`
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args + tuple(kwargs.values()):
            if isinstance(arg, Event):
                return func(*args, **kwargs)
        else:
            raise WrongEventName("Неправильное название события")

    return wrapper
