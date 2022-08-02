from pynput.keyboard import Key

from common.exceptions import ImproperlyConfiguredError
from configuration.settings import settings, KeyConfig
from data_storage.storages import KeylogData
from events.event_channel import EventChannel
from keylogging.hot_keys_keyloggers import HotKeyKeyboardLogger, HotKeyMenuKeylogger
from keylogging.keyloggers import KeyboardLogger, MenuKeylogger


def is_regular_key(key) -> bool:
    """Проверяет что значение поле `key.key` является типом `pynput.keyboard.Key`."""
    return isinstance(key, Key)


def get_keyboard_logger(
        event_chanel: EventChannel,
        data_storage: KeylogData) -> KeyboardLogger | HotKeyKeyboardLogger:
    """
    Фабрика, которая возвращает `KeyboardLogger` или `HotKeyKeyboardLogger`
    в зависимости от настроек проекта.
    """
    if is_regular_key(settings.STOP_KEY.key):
        return KeyboardLogger(event_chanel, data_storage)
    else:
        return HotKeyKeyboardLogger(event_chanel, data_storage)


def get_menu_keylogger(
        event_chanel: EventChannel) -> MenuKeylogger | HotKeyMenuKeylogger:
    """
    Фабрика, которая возвращает `MenuKeylogger` или `HotKeyMenuKeyLogger`
    в зависимости от настроек проекта.
    """
    if not isinstance(settings.START_KEY.key, type(settings.EXIT_KEY.key)):
        raise ImproperlyConfiguredError(
            "The variables `START_KEY` and `EXIT_KEY` have to be of the similar type."
        )
    elif is_regular_key(settings.START_KEY.key):
        return MenuKeylogger(event_chanel)
    else:
        return HotKeyMenuKeylogger(event_chanel)
