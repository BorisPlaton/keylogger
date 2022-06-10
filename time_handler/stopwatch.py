import threading
from datetime import datetime

from core.events import EventListener, EventHandler
from data_handler.classes import data_storage


class Stopwatch(EventHandler, EventListener):
    def __init__(self):
        super().__init__()
        self.locker = threading.Lock()
        self.time_passed = 0

    def key_logging_started(self):
        """Обработчик сигнала запуска мониторинга клавиатуры"""
        data_storage.start_time = datetime.now()

    def key_logging_stopped(self):
        """Обработчик сигнала остановки мониторинга клавиатуры"""
        data_storage.end_time = datetime.now()
