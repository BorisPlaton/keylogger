from datetime import timedelta, datetime

from configuration.settings import settings
from data_storage.connection import SQLConnection


class BaseDB:
    """Базовый класс для баз данных."""

    def __init__(self):
        self.db = SQLConnection(settings.DB_LOCATION).cur


class Statistic(BaseDB):

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

    def get_records_by_time(self, record_date):
        """Возвращает записи результатов за дату `record_date`."""
        records_list = self.db.conn.execute(
            """
            SELECT keys_quantity, start_time, end_time 
            FROM statistic
            WHERE STRFTIME("%Y-%m-%d", start_time) = STRFTIME("%Y-%m-%d", ?)
            """,
            [record_date]
        )
        return records_list.fetchall()


class BaseKeylogData:
    """
    Хранилище статистики пользователя. Имеет только базовые поля
    для хранения данных.
    """
    last_session_pressed_keys_quantity = 0
    summary_pressed_keys_quantity = 0
    summary_passed_time: timedelta | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None


class KeylogData(BaseKeylogData):
    """
    Класс, который отвечает за работу с `data_storage.storages.BaseKeylogData`.
    Имеет методы, которые считают дополнительные данные.
    """

    def update_summary_passed_time(self):
        """
        Обновляет общее время выполнения работы. Для обновления данных,
        должно быть время начала и время конца слежения за клавиатурой.
        """
        if not (self.start_time and self.storage.end_time):
            return
        if self.storage.summary_passed_time:
            self.storage.summary_passed_time += self.last_session_time
        else:
            self.storage.summary_passed_time = self.last_session_time

    @property
    def last_session_time(self) -> timedelta | None:
        """Количество пройденного времени за последнюю сессию."""
        if self.storage.start_time and self.storage.end_time:
            return self.storage.end_time - self.storage.start_time

    @property
    def last_session_typing_speed(self):
        """Возвращает скорость печати текста за последнюю сессию."""
        return get_average_typing_speed(
            self.last_session_time,
            self.storage.last_session_pressed_keys_quantity,
        )

    @property
    def average_typing_speed(self):
        """
        Возвращает скорость печати текста за всё время работы
        программы.
        """
        return get_average_typing_speed(
            self.storage.summary_passed_time,
            self.storage.summary_pressed_keys_quantity,
        )
