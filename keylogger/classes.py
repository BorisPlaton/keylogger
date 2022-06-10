from pynput.keyboard import Listener, Key

from core.datastuctures import EventHandler, Event
from data_handler.classes import data_storage


class Keylogger(EventHandler):

    def __init__(self):
        super().__init__()
        self.keylogger_listener = Listener(on_release=self._key_pressed)

    def start_logging(self):
        self.notify(Event.KEY_LOGGING_STARTED)
        with self.keylogger_listener as keylogger_listener:
            keylogger_listener.join()

    def _key_pressed(self, key):
        if key == Key.f1:
            self.notify(Event.KEY_LOGGING_STOPPED)
            return False
        data_storage.pressed_keys_quantity += 1
