import pathlib

from configuration.config import config
from core.events import EventListener
from data_handler.classes import data_storage
from output_formatter.output import TextFormatter


class FileWriter(EventListener):

    def write_keylogger_result_to_file(self):
        with open(self._get_result_file(), mode='a') as file:
            file.write(TextFormatter.get_formatted_keylogger_statistics())

    @staticmethod
    def _create_dir_if_doesnt_exist(path):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _get_result_file() -> str:
        path_to_file_list = ['%Y', '%m']
        path = config.RESULT_DIR

        for directory in path_to_file_list:
            path /= data_storage.end_time.strftime(directory)
        FileWriter._create_dir_if_doesnt_exist(path)

        path /= data_storage.end_time.strftime('%d.txt')
        return path

    def key_logging_stopped(self):
        """Обработчик сигнала завершения мониторинга клавиатуры."""
        self.write_keylogger_result_to_file()
