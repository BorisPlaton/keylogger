from pynput.keyboard import GlobalHotKeys

from configuration.settings import settings
from keylogging.keyloggers import MenuKeylogger, KeyboardLogger


class CustomKeyListener(GlobalHotKeys):
    """
    Класс для регистрации нажатий клавиш. Расширяет функционал
    базового класса `GlobalHotKeys`.
    """

    def __init__(self, hotkeys, press_func=None, release_func=None, *args, **kwargs):
        super().__init__(hotkeys, *args, **kwargs)
        self.press_func = press_func
        self.release_func = release_func

    def _on_press(self, key):
        """Вызывает перед родительским методом функцию `self.press_func`."""
        if self.press_func:
            self.press_func()
        super()._on_press(key)

    def _on_release(self, key):
        """Вызывает перед родительским методом функцию `self.release_func`."""
        if self.release_func:
            self.release_func()
        super()._on_release(key)


class HotKeyKeyboardLogger(KeyboardLogger):

    def get_listener(self, press_func=None, release_func=None) -> CustomKeyListener:
        """Возвращает экземпляр класса `CustomKeyListener`."""
        return CustomKeyListener(
            {settings.STOP_KEY.key: self._stop_logging},
            press_func or (lambda: self.data_storage.increment_last_session_keys_quantity()),
            release_func
        )

    def _stop_logging(self):
        """Указывает, что запись завершена и останавливает слежение."""
        self.stop_logging = True
        self.listener.stop()


class HotKeyMenuKeylogger(MenuKeylogger):

    def get_listener(self, press_func=None, release_func=None) -> CustomKeyListener:
        """Возвращает экземпляр класса `CustomKeyListener`."""
        return CustomKeyListener(
            {
                settings.START_KEY.key: self._start_keyboard_logger,
                settings.EXIT_KEY.key: lambda: self.listener.stop(),
            }
        )

    def _start_keyboard_logger(self):
        """
        Устанавливает значение `self.start_key_logging` истинным,
        и останавливает логгер.
        """
        self.start_key_logging = True
        self.listener.stop()
