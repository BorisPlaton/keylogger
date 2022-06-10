from enum import Enum

from core.exceptions import WrongEventName


class Event(Enum):
    TIME_PASSED = 'time_passed'
    KEY_LOGGING_STOPPED = 'time_stopped'
    KEY_LOGGING_STARTED = 'time_started'
    PROGRAM_STARTED = 'program_started'
    MENU_STARTED = 'menu_started'


class EventListener:

    def time_passed(self):
        """Событие, которое указывает, что определенный промежуток времени пройден."""
        pass

    def key_logging_stopped(self):
        """Событие, которое указывает, что слежение за клавиатурой остановлено."""
        pass

    def key_logging_started(self):
        """Событие, которое указывает, что слежение за клавиатурой начато."""
        pass

    def program_started(self):
        """Событие, которое указывает, что программа запустила своё выполнение."""
        pass

    def menu_started(self):
        """Событие, которе указывает, что меню перед стартом программы вызвано"""
        pass


class EventHandler:

    def __init__(self):
        self.event_listeners: dict[Event, list[EventListener]] = {event: [] for event in Event}

    def notify(self, event: Event):
        match event:
            case Event.TIME_PASSED:
                self._notify_time_passed()
            case Event.KEY_LOGGING_STOPPED:
                self._notify_key_logging_stopped()
            case Event.KEY_LOGGING_STARTED:
                self._notify_key_logging_started()
            case Event.PROGRAM_STARTED:
                self._notify_program_started()
            case Event.MENU_STARTED:
                self._notify_menu_started()
            case _:
                raise WrongEventName(f"Event {event} doesn't exist")

    def add_listener(self, listener: EventListener, event: Event):
        self.event_listeners[event].append(listener)

    def add_listeners(self, listeners: list[EventListener], event: Event):
        for listener in listeners:
            self.add_listener(listener, event)

    def _notify_key_logging_stopped(self):
        for listener in self.event_listeners[Event.KEY_LOGGING_STOPPED]:
            listener.key_logging_stopped()

    def _notify_time_passed(self):
        for listener in self.event_listeners[Event.TIME_PASSED]:
            listener.time_passed()

    def _notify_key_logging_started(self):
        for listener in self.event_listeners[Event.KEY_LOGGING_STARTED]:
            listener.key_logging_started()

    def _notify_program_started(self):
        for listener in self.event_listeners[Event.PROGRAM_STARTED]:
            listener.program_started()

    def _notify_menu_started(self):
        for listener in self.event_listeners[Event.MENU_STARTED]:
            listener.menu_started()
