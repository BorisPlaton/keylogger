from configuration.settings import settings
from database.connection import SQLConnection


class BaseDB:
    """Базовый класс для баз данных."""

    def __init__(self):
        self.db = SQLConnection(settings.DB_LOCATION).cur
