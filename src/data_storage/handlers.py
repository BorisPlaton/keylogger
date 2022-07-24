from datetime import timedelta

from data_storage.storages import Statistic, KeylogData
from data_storage.utils import get_average_typing_speed


class StatisticHandler:
    """
    Класс, который отвечает на сигналы и записывает данные
    в базу данных.
    """

    def key_logging_stopped(self):
        """
        Когда программа перестает следить за клавиатурой,
        данные записываются в таблицу `statistic`.
        """
        self.statistic_db.add_record(
            self.storage.summary_pressed_keys_quantity,
            str(self.storage.start_time),
            str(self.storage.end_time),
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


class KeylogDataHandler:
    """
    Класс, который отвечает за работу с `data_storage.storages.KeylogData`.
    Имеет методы, которые считают дополнительные данные.
    """

    def update_summary_passed_time(self):
        """
        Обновляет общее время выполнения работы. Для обновления данных,
        должно быть время начала и время конца слежения за клавиатурой.
        """
        if not (self.storage.start_time and self.storage.end_time):
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

    def __init__(self, data_storage: KeylogData):
        """Сохраняет хранилище в данных, с которым будет работать."""
        self.storage = data_storage
