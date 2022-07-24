from datetime import datetime


class Stopwatch:
    """Секундомер. Записывает начало и конец выполнения программы."""

    def key_logging_started(self):
        """Обработчик сигнала запуска мониторинга клавиатуры"""
        self.data_storage.start_time = datetime.now()

    def key_logging_stopped(self):
        """Обработчик сигнала остановки мониторинга клавиатуры"""
        self.data_storage.end_time = datetime.now()

    def __init__(self, data_storage):
        """
        Сохраняет хранилище данных, в которое надо записывать время
        начала и конца работы программы.
        """
        self.data_storage = data_storage
