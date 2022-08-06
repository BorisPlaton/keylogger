import pytest
from pynput.keyboard import Key

from common.exceptions import ImproperlyConfiguredError
from configuration.settings import settings, KeyConfig
from keylogging.hot_keys_keyloggers import HotKeyMenuKeylogger, HotKeyKeyboardLogger
from keylogging.keyloggers import MenuKeylogger, KeyboardLogger
from keylogging.utils import is_regular_key, get_menu_keylogger, get_keyboard_logger


@pytest.mark.parametrize(
    'key',
    [
        1, 2, 's', set(),
        dict, Key, '', False
    ]
)
def test_is_regular_key_with_wrong_values(key):
    assert not is_regular_key(key)


@pytest.mark.parametrize(
    'key',
    [
        Key.f1, Key.cmd, Key.alt_r
    ]
)
def test_is_regular_key_with_pynput_key_values(key):
    assert is_regular_key(key)


def test_menu_logger_factory(event_channel):
    settings.START_KEY = KeyConfig('1', '')
    settings.EXIT_KEY = KeyConfig('2', '')
    menu_keylogger = get_menu_keylogger(event_channel)
    assert isinstance(menu_keylogger, HotKeyMenuKeylogger)
    settings.EXIT_KEY = KeyConfig(2, '')
    with pytest.raises(ImproperlyConfiguredError):
        get_menu_keylogger(event_channel)
    settings.START_KEY = settings.EXIT_KEY = KeyConfig(Key.f1, '')
    assert isinstance(get_menu_keylogger(event_channel), MenuKeylogger)


def test_keyboard_logger_factory(event_channel, data_storage):
    settings.STOP_KEY = KeyConfig('1', '')
    keyboard_keylogger = get_keyboard_logger(event_channel, data_storage)
    assert isinstance(keyboard_keylogger, HotKeyKeyboardLogger)
    settings.STOP_KEY = KeyConfig(Key.f1, '')
    assert isinstance(get_keyboard_logger(event_channel, data_storage), KeyboardLogger)
