import threading
import time

from core.events import EventListener, EventHandler
from data_handler.classes import data_storage


class Stopwatch(EventHandler, EventListener):
    def __init__(self):
        super().__init__()
        self.locker = threading.Lock()
        self._start_event = threading.Event()
        self.time_passed = 0

    def start(self, resume: bool = False):
        """Запускает секундомер. Если параметр `resume` == True, то не очищает атрибут `time_passed`."""
        with self.locker:
            if not resume:
                self._clear_previous_time_result()
            self._start_event.set()
            thread = threading.Thread(target=self._start_stopwatch, name="Stopwatch-thread")
            thread.start()

    def stop(self):
        """Останавливает секундомер"""
        with self.locker:
            self._start_event.clear()

    def is_working(self):
        with self.locker:
            return self._start_event.is_set()

    def key_logging_started(self):
        """Сигнал запуска """
        self.start()

    def key_logging_stopped(self):
        self.stop()

    def _start_stopwatch(self):
        while self.is_working():
            time.sleep(1)
            data_storage.seconds += 1

    def _clear_previous_time_result(self):
        self.time_passed = 0
