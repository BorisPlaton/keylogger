from pynput.keyboard import Listener, Key

from core.datastuctures import EventHandler, Event
from data_handler.classes import data_storage


class Keylogger(EventHandler):

    def __init__(self):
        super().__init__()
        self.keylogger_listener = Listener(on_release=self._key_pressed)

    def start_logging(self):
        self.notify(Event.TIME_STARTED)
        with self.keylogger_listener as keylogger_listener:
            keylogger_listener.join()

    def stop_logging(self):
        self.keylogger_listener.stop()
        self.notify(Event.TIME_STOPPED)

    def _key_pressed(self, key):
        print(f'{key} release')
        if key == Key.f1:
            self.notify(Event.TIME_STOPPED)
            return False
