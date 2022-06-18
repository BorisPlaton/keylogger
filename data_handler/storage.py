from datetime import datetime, timedelta
import threading
from typing import Optional


class DataHandler:

    def __init__(self):
        self._summary_pressed_keys_quantity = 0
        self._summary_passed_time: Optional[timedelta] = None
        self._last_session_pressed_keys_quantity = 0
        self._start_time: Optional[datetime] = None
        self._end_time: Optional[datetime] = None
        self._locker = threading.RLock()

    @property
    def start_time(self):
        """Начало работы программы."""
        with self._locker:
            return self._start_time

    @property
    def summary_passed_time(self):
        """Общее время работы программы."""
        with self._locker:
            return self._summary_passed_time

    @property
    def end_time(self):
        """Конец работы программы."""
        with self._locker:
            return self._end_time

    @property
    def time_passed(self):
        """Количество пройденного времени последней сессии программы."""
        with self._locker:
            return self.end_time - self.start_time

    @property
    def summary_pressed_keys_quantity(self):
        """Количество нажатых клавиш."""
        with self._locker:
            return self._summary_pressed_keys_quantity

    @property
    def last_session_pressed_keys_quantity(self):
        """Количество нажатых клавиш последней сессии."""
        with self._locker:
            return self._last_session_pressed_keys_quantity

    @start_time.setter
    def start_time(self, start_time_value: datetime):
        with self._locker:
            self._start_time = start_time_value

    @end_time.setter
    def end_time(self, end_time_value: datetime):
        with self._locker:
            self._end_time = end_time_value

    @summary_pressed_keys_quantity.setter
    def summary_pressed_keys_quantity(self, value: int):
        with self._locker:
            self._summary_pressed_keys_quantity = value

    @last_session_pressed_keys_quantity.setter
    def last_session_pressed_keys_quantity(self, value: int):
        with self._locker:
            self._last_session_pressed_keys_quantity = value

    @summary_passed_time.setter
    def summary_passed_time(self, value: datetime):
        with self._locker:
            if not self._summary_passed_time:
                self._summary_passed_time = value
            else:
                self._summary_passed_time += value


data_storage = DataHandler()
