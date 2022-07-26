import logging
from pathlib import Path


class OutputLogger:
    """Миксин для работы с логированием."""

    _default_log_format = "[%(asctime)s in %(name)s.%(funcName)s] - %(message)s"

    def __init__(
            self,
            logger_name: str,
            logger_level: int,
            is_stream_handler: bool = True,
            stream_log_format: str = None,
            is_file_handler: bool = False,
            file_log_format: str = None,
            log_file: str | Path = None,
    ):
        if is_file_handler and not file_log_format:
            file_log_format = self._default_log_format
        if is_stream_handler and not stream_log_format:
            stream_log_format = self._default_log_format

        self.logger_name = logger_name
        self.logger_level = logger_level

        self.is_file_handler = is_file_handler
        self.file_log_format: str = file_log_format
        self.log_file = log_file

        self.is_stream_handler = is_stream_handler
        self.stream_log_format: str = stream_log_format

    def set_logger(self):
        """
        Настраивает класс логер. Добавляет логирование в файл, если
        `is_file_handler` = True. Аналогично с выводом в консоль,
        если атрибут `is_stream_handler` = True.
        """
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.logger_level)

        if self.is_file_handler:
            logger.addHandler(self.get_file_handler())

        if self.is_stream_handler:
            logger.addHandler(self.get_stream_handler())

    @property
    def logger(self) -> logging.Logger:
        logger_instance = logging.getLogger(self.logger_name)

        if not logger_instance.hasHandlers():
            self.set_logger()

        return logger_instance

    @staticmethod
    def get_formatter(log_format: str) -> logging.Formatter:
        """Возвращает `logging.Formatter`, с форматом сообщения `log_format`."""
        formatter = logging.Formatter(log_format)
        return formatter

    def get_file_handler(self) -> logging.FileHandler:
        """Возвращает обработчик файла `logging.FileHandler`."""
        file_handler = logging.FileHandler(self.log_file)
        return self.setup_handler(
            file_handler,
            self.file_log_format,
        )

    def get_stream_handler(self) -> logging.StreamHandler:
        """Возвращает обработчик вывода в консоль `logging.StreamHandler`."""
        stream_handler = logging.StreamHandler()
        return self.setup_handler(
            stream_handler,
            self.stream_log_format,
        )

    def setup_handler(self, handler, handler_log_format: str):
        """Устанавливает стандартные настройки для обработчика."""
        handler.setFormatter(
            self.get_formatter(handler_log_format)
        )
        handler.setLevel(self.logger_level)
        return handler
