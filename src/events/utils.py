from enum import Enum, auto
from functools import wraps

from events.exceptions import WrongEventName


class Event(Enum):
    KEY_LOGGING_STOPPED = auto()
    KEY_LOGGING_STARTED = auto()
    SHOW_MENU = auto()


def is_event_correct(func):
    """
    Проверяет, что событие класса `core.events.Event` переданы
    аргументом в декорируемую функцию, иначе вызывается исключение
    `core.exceptions.WrongEventName`
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args + tuple(kwargs.values()):
            if isinstance(arg, Event) and arg in [event for event in Event]:
                return func(*args, **kwargs)
        else:
            raise WrongEventName(f"Can't find a argument with type `<enum 'Event'>` in {args}.")

    return wrapper
