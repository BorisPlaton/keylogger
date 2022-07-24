from typing import Callable

from events.utils import is_event_correct, Event


class EventChannel:
    """
    Шина событий, которая уведомляет слушателей, о произошедшем
    событии, а именно - вызывает callback-функции.
    """

    @is_event_correct
    def notify(self, event: Event):
        """Вызывает callback-функции, которые слушали данное событие."""
        for callback in self.event_listeners[event]:
            callback()

    @is_event_correct
    def add_listener(self, event: Event, callback: Callable):
        """Добавляет слушателя на событие."""
        self.event_listeners[event].append(callback)

    @is_event_correct
    def remove(self, event: Event, callback: Callable):
        """
        Убирает callback-функцию с события, если она есть в
        списке слушателей.
        """
        try:
            self.event_listeners[event].remove(callback)
        except ValueError:
            pass

    @is_event_correct
    def add_listeners(self, event: Event, listeners: list[Callable]):
        """Добавляет множество слушателей на событие."""
        for callback in listeners:
            self.add_listener(event, callback)

    def __init__(self):
        """
        Инициализируется словарь, ключами которого есть события,
        а значениями являются списки, со слушателями, что
        наследуется от данного класса `EventChannel`.
        """
        self.event_listeners: dict[Event, list[Callable]] = {event: [] for event in Event}
