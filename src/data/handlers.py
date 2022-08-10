from data.storages import Statistic, KeylogData


class DataHandler:
    """
    Класс, который отвечает на сигналы и записывает данные
    в базу данных.
    """

    def key_logging_stopped(self):
        """
        Когда программа перестает следить за клавиатурой,
        данные записываются в таблицу `statistic`.
        """
        self.update_keylog_data_storage()
        self.add_record_to_db()

    def update_keylog_data_storage(self):
        """Обновляет данные в хранилище `KeylogData`."""
        self.storage.update_summary_pressed_keys_quantity()

    def add_record_to_db(self):
        """Добавляет запись результата сессии в базу данных."""
        self.statistic_db.add_record(
            self.storage.last_session_pressed_keys_quantity,
            self.storage.start_time,
            self.storage.end_time,
        )

    def __init__(self, storage: KeylogData):
        """
        Инициализируем необходимые классы для работы.
        Аргумент `storage` - это экземпляр класса DataHandler из
        которого будут браться данные для записи в таблицу.
        """
        self.statistic_db = Statistic()
        self.storage = storage
        self.statistic_db.create_table()
