from datetime import timedelta, datetime

from configuration.settings import settings
from data_storage.connection import SQLConnection


class BaseDB:
    """Базовый класс для баз данных."""

    def __init__(self):
        self.db = SQLConnection(settings.DB_LOCATION).cur


class Statistic(BaseDB):
    """Класс для работы с таблицей `statistic` в базе данных."""

    def create_table(self):
        """Создает таблицу `statistic`."""
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS statistic (
                id INTEGER PRIMARY KEY,
                keys_quantity INTEGER,
                start_time TEXT,
                end_time TEXT
            );
            """
        )

    def add_record(self, keys_quantity: int, start_time, end_time):
        """Добавляет запись статистики пользователя в таблицу."""
        self.db.execute(
            """
            INSERT INTO statistic(keys_quantity, start_time, end_time)
            VALUES (?, ?, ?);
            """,
            [keys_quantity, start_time, end_time]
        )

    def get_records_by_time(self, record_date: str | datetime) -> list[tuple[int, str, str]]:
        """Возвращает записи результатов за дату `record_date`."""
        records_list = self.db.execute(
            """
            SELECT keys_quantity, start_time, end_time
            FROM statistic
            WHERE STRFTIME("%Y-%m-%d", start_time) = STRFTIME("%Y-%m-%d", ?)
            """,
            [record_date]
        )
        return records_list.fetchall()


class KeylogData:
    """Хранилище статистики пользователя."""

    last_session_pressed_keys_quantity = 0
    summary_pressed_keys_quantity = 0
    summary_passed_time: timedelta | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

    def update_summary_passed_time(self):
        """
        Обновляет общее время выполнения работы. Для обновления
        данных, должно быть время начала и время конца слежения
        за клавиатурой.
        """
        if not (self.start_time and self.end_time):
            return
        if self.summary_passed_time:
            self.summary_passed_time += self.last_session_time
        else:
            self.summary_passed_time = self.last_session_time

    def update_summary_pressed_keys_quantity(self):
        """
        Добавляет данные по нажатиям клавиш за последнюю
        сессию в данные за всё время выполнения работы.
        """
        self.summary_pressed_keys_quantity += self.last_session_pressed_keys_quantity

    def reset_last_session_data(self):
        """Обновляет данные за последнюю сессию."""
        self.last_session_pressed_keys_quantity = 0

    @property
    def last_session_time(self) -> timedelta | None:
        """Количество пройденного времени за последнюю сессию."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
