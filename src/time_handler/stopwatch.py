from datetime import datetime

from data.storages import KeylogData


class Stopwatch:
    """Секундомер. Записывает начало и конец выполнения программы."""

    def key_logging_started(self):
        """Обработчик сигнала запуска мониторинга клавиатуры"""
        self.data_storage.start_time = datetime.now()

    def key_logging_stopped(self):
        """Обработчик сигнала остановки мониторинга клавиатуры"""
        self.data_storage.end_time = datetime.now()
        self.data_storage.update_summary_passed_time()

    def __init__(self, data_storage: KeylogData):
        """
        Сохраняет хранилище данных, в которое надо записывать время
        начала и конца работы программы.
        """
        self.data_storage = data_storage
