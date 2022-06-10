import threading
import time

from core.datastuctures import Listener, EventHandler
from data_handler.classes import data_storage


class Stopwatch(EventHandler, Listener):

    def __init__(self):
        super().__init__()
        self._stopwatch_thread = threading.Thread(target=self._start_stopwatch, name="Stopwatch-thread")
        self._start_event = threading.Event()
        self.time_passed = 0

    def start(self, resume: bool = False):
        """Запускает секундомер. Если параметр `resume` == True, то не очищает атрибут `time_passed`."""
        if not resume:
            self._clear_previous_time_result()
        self._start_event.set()
        self._stopwatch_thread.start()

    def stop(self):
        """Останавливает секундомер"""
        self._start_event.clear()

    def key_logging_started(self):
        """Сигнал запуска """
        self.start()

    def key_logging_stopped(self):
        self.stop()

    def _start_stopwatch(self):
        while self._start_event.is_set():
            data_storage.seconds += 1
            time.sleep(1)

    def _clear_previous_time_result(self):
        self.time_passed = 0
