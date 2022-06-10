from datetime import datetime
import threading
from typing import Optional


class _DataHandler:

    def __init__(self):
        self._stopwatch_seconds_passed = 0
        self._pressed_keys_quantity = 0
        self._start_time: Optional[datetime] = None
        self._end_time: Optional[datetime] = None
        self._locker = threading.RLock()

    @property
    def start_time(self):
        """Начало работы программы."""
        with self._locker:
            return self._start_time

    @property
    def end_time(self):
        """Конец работы программы."""
        with self._locker:
            return self._end_time

    @property
    def duration_time(self):
        """Количество пройденных секунд."""
        with self._locker:
            return self.end_time - self.start_time

    @property
    def pressed_keys_quantity(self):
        """Количество нажатых клавиш."""
        with self._locker:
            return self._pressed_keys_quantity

    @start_time.setter
    def start_time(self, start_time_value: datetime):
        with self._locker:
            self._start_time = start_time_value

    @end_time.setter
    def end_time(self, end_time_value: datetime):
        with self._locker:
            self._end_time = end_time_value

    @duration_time.setter
    def duration_time(self, value: int):
        with self._locker:
            self._stopwatch_seconds_passed = value

    @pressed_keys_quantity.setter
    def pressed_keys_quantity(self, value: int):
        with self._locker:
            self._pressed_keys_quantity = value


data_storage = _DataHandler()
