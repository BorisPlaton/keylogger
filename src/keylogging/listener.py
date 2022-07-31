from pynput.keyboard import GlobalHotKeys


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
