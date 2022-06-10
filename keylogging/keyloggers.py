import threading

from pynput.keyboard import Listener

from configuration.utils import config
from core.events import EventHandler, Event, EventListener
from data_handler.classes import data_storage


class AbstractKeylogger(EventHandler, EventListener):

    def start_logging(self):
        listener = Listener(on_release=self._key_pressed)
        with listener:
            listener.join()

    def _key_pressed(self, key):
        pass


class KeyboardLogger(AbstractKeylogger):

    def program_started(self):
        """Запускает мониторинг клавиатуры"""
        self.notify(Event.KEY_LOGGING_STARTED)
        self.start_logging()
        self.notify(Event.KEY_LOGGING_STOPPED)

    def _key_pressed(self, key):
        if key == config.STOP_KEY:
            return False
        data_storage.pressed_keys_quantity += 1


class MenuKeylogger(AbstractKeylogger):

    def __init__(self):
        super().__init__()
        self._is_active = True
        self.locker = threading.Lock()

    def start_logging(self):
        super().start_logging()
        if self.is_program_working():
            self.notify(Event.PROGRAM_STARTED)

    def key_logging_stopped(self):
        """Вызывается, если класс `Keylogger` перестал следить за клавиатурой."""
        self.start_logging()

    def is_program_working(self) -> bool:
        """Возвращает булево значение, что показывает активна ли программа."""
        return self._is_active

    def _key_pressed(self, key):
        match key:
            # Если нажата кнопка F1, запускается программа
            case config.START_KEY:
                return False
            # Если пользователь нажимает F2, программа заканчивает свою работу
            case config.EXIT_KEY:
                self._is_active = False
                return False
