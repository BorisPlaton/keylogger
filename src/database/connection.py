import sqlite3
from sqlite3 import Connection


class SQLConnection:
    """Класс для организации соединения с базой данных."""

    def connect(self):
        """Открывает соединение."""
        self.conn = sqlite3.connect(self.db_name, isolation_level=None)

    def close(self):
        """Закрывает соединение."""
        self.conn.close()

    @property
    def cur(self):
        """Возвращает курсор для выполнения запросов."""
        return self.conn.cursor()

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn: Connection | None = None
        self.connect()
