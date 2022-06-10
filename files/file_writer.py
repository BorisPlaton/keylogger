from core.events import EventListener


class FileWriter(EventListener):

    def write_keylogger_result_to_file(self):
        pass

    def key_logging_stopped(self):
        """Обработчик сигнала завершения мониторинга клавиатуры."""
        self.write_keylogger_result_to_file()
