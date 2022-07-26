from pynput.keyboard import Listener

from configuration.settings import settings
from data_storage.storages import KeylogData
from events.event_channel import Event, EventChannel


class AbstractKeylogger:
    """Абстрактный класс за наблюдением нажатий клавиш."""

    def start_logging(self):
        """Начинает наблюдать за действиями клавиатуры."""
        listener = Listener(on_release=self._key_pressed)
        with listener:
            listener.join()
        self.notify_user_choice()

    def notify_user_choice(self):
        """Делает действия, после мониторинга за клавиатурой."""

    def _key_pressed(self, key) -> bool:
        """
        Абстрактный метод. Должен иметь условие выхода, которое при выполнении
        возвращает `False` для завершения наблюдения за клавиатурой.
        """

    def __init__(self, event_chanel: EventChannel):
        self.event_chanel = event_chanel


class KeyboardLogger(AbstractKeylogger):
    """Следит за нажатиями по клавиатуре. Считает количество нажатых клавиш."""

    def __init__(self, event_chanel, data_storage: KeylogData):
        super().__init__(event_chanel)
        self.data_storage = data_storage
        self.stop_logging = False

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

    def _key_pressed(self, key):
        """
        Считает количество нажатых клавиш. При нажатии клавиши `config.STOP_KEY.key`
        заканчивает подсчет и записывает количество нажатых клавши за последнюю сессию.
        """
        if key == settings.STOP_KEY.key:
            self.data_storage.update_summary_pressed_keys_quantity()
            self.stop_logging = True
            return False
        self.data_storage.last_session_pressed_keys_quantity += 1


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
        self.show_statistics = False

    def notify_user_choice(self):
        """Вызывает события, связанные с выбранной кнопкой."""
        match True:
            case self.start_key_logging:
                self.set_default_values()
                self.event_chanel.notify(Event.KEY_LOGGING_STARTED)
            case self.show_statistics:
                self.set_default_values()
                self.event_chanel.notify(Event.SHOW_STATISTICS)

    def _key_pressed(self, key):
        """Анализирует нажатую кнопку пользователем в меню программы."""
        match key:
            case settings.START_KEY.key:
                self.start_key_logging = True
                return False
            case settings.EXIT_KEY.key:
                return False

    def __init__(self, event_chanel):
        super().__init__(event_chanel)
        self.start_key_logging = False
        self.show_statistics = False
