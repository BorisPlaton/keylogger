from data_handler.storage import data_storage as ds
from database.abs import BaseDB


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

    def add_record(self, keys_quantity, start_time, end_time):
        """Добавляет запись в таблицу."""
        self.db.execute(
            """
            INSERT INTO statistic(keys_quantity, start_time, end_time) 
            VALUES (?, ?, ?);
            """,
            [keys_quantity, start_time, end_time]
        )

    def get_records_by_time(self, record_date):
        """Возвращает записи результатов за какую-то дату."""
        records_list = self.db.conn.execute(
            """
            SELECT keys_quantity, start_time, end_time 
            FROM statistic
            WHERE STRFTIME("%Y-%m-%d", start_time) = STRFTIME("%Y-%m-%d", ?)
            """,
            [record_date]
        )
        return records_list.fetchall()


class StatisticHandler:

    def __init__(self):
        self.statistic_db = Statistic()
        self.statistic_db.create_table()

    def key_logging_stopped(self):
        self.statistic_db.add_record(
            ds.summary_pressed_keys_quantity,
            str(ds.start_time),
            str(ds.end_time),
        )
