from datetime import datetime
from typing import Optional

from core.events import EventListener, EventHandler
from data_handler.storage import data_storage


class Stopwatch(EventHandler, EventListener):
    """Секундомер, для подсчета времени выполнения программы."""

    def __init__(self):
        super().__init__()
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    def key_logging_started(self):
        """Обработчик сигнала запуска мониторинга клавиатуры"""
        self.start_time = datetime.now()
        data_storage.start_time = self.start_time

    def key_logging_stopped(self):
        """Обработчик сигнала остановки мониторинга клавиатуры"""
        self.end_time = datetime.now()
        data_storage.end_time = self.end_time
        data_storage.summary_passed_time = self.end_time - self.start_time
