from pynput.keyboard import Listener

from configuration.config import config
from core.events import EventHandler, Event, EventListener
from data_handler.storage import data_storage as ds


class AbstractKeylogger(EventHandler, EventListener):
    """Абстрактный класс за наблюдением нажатий клавиш."""

    def start_logging(self):
        """Начинает наблюдать за действиями клавиатуры."""
        listener = Listener(on_release=self._key_pressed)
        with listener:
            listener.join()

    def _key_pressed(self, key) -> bool:
        """
        Абстрактный метод. Должен иметь условие выхода, которое при выполнении
        возвращает `False` для завершения наблюдения за клавиатурой.
        """
        pass


class KeyboardLogger(AbstractKeylogger):
    """Следит за нажатиями по клавиатуре. Считает количество нажатых клавиш."""

    def program_started(self):
        """Запускает мониторинг клавиатуры."""
        self.notify(Event.KEY_LOGGING_STARTED)
        self.start_logging()
        self.notify(Event.KEY_LOGGING_STOPPED)

    def _key_pressed(self, key):
        """
        Считает количество нажатых клавиш. При нажатии клавиши `config.STOP_KEY.key`
        заканчивает подсчет и записывает количество нажатых клавши за последнюю сессию.
        """
        if key == config.STOP_KEY.key:
            ds.last_session_pressed_keys_quantity = (
                    ds.summary_pressed_keys_quantity - ds.last_session_pressed_keys_quantity
            )
            return False
        ds.summary_pressed_keys_quantity += 1


class MenuKeylogger(AbstractKeylogger):
    """
    Следит за нажатиями по клавишам `config.START_KEY.key` и
    `config.EXIT_KEY.key` во время работы меню программы.
    """

    def __init__(self):
        super().__init__()
        self._is_active = True

    def start_logging(self):
        """Запускает мониторинг клавиатуры."""
        self.notify(Event.MENU_STARTED)
        super().start_logging()
        if self.is_program_working():
            self.notify(Event.PROGRAM_STARTED)

    def key_logging_stopped(self):
        """Вызывается, если класс `Keylogger` перестал следить за клавиатурой."""
        self.start_logging()

    def is_program_working(self) -> bool:
        """Возвращает булево значение, что показывает активна ли программа."""
        return self._is_active

    def _key_pressed(self, key):
        match key:
            # Если нажата кнопка F1, запускается программа
            case config.START_KEY.key:
                return False
            # Если пользователь нажимает F2, программа заканчивает свою работу
            case config.EXIT_KEY.key:
                self._is_active = False
                return False
