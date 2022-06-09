from enum import Enum

from core.exceptions import WrongEventName


class Event(Enum):
    TIME_PASSED = 'time_passed'
    TIME_STOPPED = 'time_stopped'
    TIME_STARTED = 'time_started'


class Listener:

    def call_time_passed(self):
        self.time_passed()

    def call_time_stopped(self):
        self.time_stopped()

    def call_time_started(self):
        self.time_started()

    def time_passed(self):
        pass

    def time_stopped(self):
        pass

    def time_started(self):
        pass


class EventHandler:

    def __init__(self):
        self.event_listeners = {event: [] for event in Event}

    def notify(self, event: Event):
        match event:
            case Event.TIME_PASSED:
                self._notify_time_passed()
            case Event.TIME_STOPPED:
                self._notify_time_stopped()
            case Event.TIME_STARTED:
                self._notify_time_started()
            case _:
                raise WrongEventName(f"Event {event} doesn't exist")

    def add_listener(self, listener: Listener, event: Event):
        self.event_listeners[event].append(listener)

    def add_listeners(self, listeners: list[Listener], event: Event):
        for listener in listeners:
            self.add_listener(listener, event)

    def _notify_time_stopped(self):
        for listener in self.event_listeners[Event.TIME_STOPPED]:
            listener.time_stopped()

    def _notify_time_passed(self):
        for listener in self.event_listeners[Event.TIME_PASSED]:
            listener.time_passed()

    def _notify_time_started(self):
        for listener in self.event_listeners[Event.TIME_PASSED]:
            listener.time_started()
