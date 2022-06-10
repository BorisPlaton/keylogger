import threading


class _DataHandler:

    def __init__(self):
        self._stopwatch_seconds_passed = 0
        self._pressed_keys_quantity = 0
        self._locker = threading.Lock()

    @property
    def seconds(self):
        with self._locker:
            return self._stopwatch_seconds_passed

    @seconds.setter
    def seconds(self, value: int):
        with self._locker:
            self._stopwatch_seconds_passed = value

    @property
    def pressed_keys_quantity(self):
        with self._locker:
            return self._pressed_keys_quantity

    @pressed_keys_quantity.setter
    def pressed_keys_quantity(self, value: int):
        with self._locker:
            self._pressed_keys_quantity = value


data_storage = _DataHandler()
