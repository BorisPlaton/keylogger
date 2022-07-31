from configuration.settings import settings
from data_storage.storages import KeylogData
from events.event_channel import Event, EventChannel
from keylogging.listener import CustomKeyListener


class AbstractKeylogger:
    """Абстрактный класс за наблюдением нажатий клавиш."""

    def start_logging(self):
        """Начинает наблюдать за действиями клавиатуры."""
        self.listener = self.get_listener()
        with self.listener:
            try:
                self.listener.join()
            except ValueError:
                pass
        self.notify_user_choice()

    def notify_user_choice(self):
        """Делает действия, после мониторинга за клавиатурой."""
        raise NotImplementedError("You have to implement the `notify_user_choice` method.")

    def get_hotkeys(self) -> dict:
        """
        Возвращает словарь ключом которого являются горячие клавиши,
        а значение callback функция.
        """
        raise NotImplementedError("You have to implement the `get_hotkeys` method.")

    def stop_listener(self):
        """
        Вызывается в дочерних классах, для остановки слежения
        за клавиатурой.
        """
        self.listener.stop()

    def get_listener(self, press_func=None, release_func=None, *args, **kwargs) -> CustomKeyListener:
        """Возвращает экземпляр класса `CustomKeyListener`."""
        return CustomKeyListener(self.get_hotkeys(), press_func, release_func, *args, **kwargs)

    def __init__(self, event_chanel: EventChannel):
        self.event_chanel = event_chanel
        self.listener: CustomKeyListener | None = None


class KeyboardLogger(AbstractKeylogger):
    """Следит за нажатиями по клавиатуре. Считает количество нажатых клавиш."""

    def key_logging_started(self):
        """Запускает мониторинг клавиатуры."""
        self.data_storage.reset_last_session_data()
        self.start_logging()

    def notify_user_choice(self):
        """Вызывает события, связанные с выбранной кнопкой."""
        match True:
            case self.stop_logging:
                self.set_default_values()
                self.event_chanel.notify(Event.KEY_LOGGING_STOPPED)

    def set_default_values(self):
        """
        Устанавливает значения выбора пользователя в начальную
        позицию.
        """
        self.stop_logging = False

    def get_hotkeys(self) -> dict:
        """Реализация абстрактного метода родительского класса."""
        return {
            settings.STOP_KEY.key: self.stop_logging_pressed
        }

    def stop_logging_pressed(self):
        """Указывает, что запись завершена и останавливает слежение."""
        self.stop_logging = True
        self.stop_listener()

    def get_listener(self, *args, **kwargs) -> CustomKeyListener:
        return super().get_listener(lambda: self.data_storage.increment_last_session_keys_quantity())

    def __init__(self, event_chanel, data_storage: KeylogData):
        super().__init__(event_chanel)
        self.data_storage = data_storage
        self.stop_logging = False


class MenuKeylogger(AbstractKeylogger):
    """
    Следит за нажатиями по клавишам `config.START_KEY.key` и
    `config.EXIT_KEY.key` во время работы меню программы.
    """

    def show_menu(self):
        """Запускает мониторинг клавиатуры."""
        self.event_chanel.notify(Event.SHOW_MENU)
        self.start_logging()

    def key_logging_stopped(self):
        """Вызывается, если класс `KeyboardLogger` перестал следить за клавиатурой."""
        self.show_menu()

    def set_default_values(self):
        """
        Устанавливает значения выбора пользователя в начальную
        позицию.
        """
        self.start_key_logging = False

    def notify_user_choice(self):
        """Вызывает события, связанные с выбранной кнопкой."""
        match True:
            case self.start_key_logging:
                self.set_default_values()
                self.event_chanel.notify(Event.KEY_LOGGING_STARTED)

    def get_hotkeys(self) -> dict:
        """Реализация абстрактного метода родительского класса."""
        return {
            settings.START_KEY.key: self._start_keyboard_logger,
            settings.EXIT_KEY.key: self.stop_listener,
        }

    def _start_keyboard_logger(self):
        """
        Устанавливает значение `self.start_key_logging` истинным,
        и останавливает логгер.
        """
        self.start_key_logging = True
        self.stop_listener()

    def __init__(self, event_chanel):
        super().__init__(event_chanel)
        self.start_key_logging = False
        self.show_statistics = False
