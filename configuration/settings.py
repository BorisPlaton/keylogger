from pathlib import Path

from pynput.keyboard import Key

from configuration.utils import KeyConfig


BASE_DIR = Path(__file__).resolve().parent.parent
WRITE_TO_FILE = True
RESULT_DIR = BASE_DIR / 'Results'
TIME_RANGE = 60

START_KEY = KeyConfig(Key.f1, 'F1')
STOP_KEY = KeyConfig(Key.f1, 'F1')
EXIT_KEY = KeyConfig(Key.f2, 'F2')

KEY_LOGGING_HELP_TEXT = """
Начало работы: {START_TIME}
{STOP_KEY} - Остановить запись
"""

MENU_TEXT = """
{START_KEY} - Начать запись
{EXIT_KEY} - Завершение работы
"""

KEYLOGGER_STATISTICS = """
Количество нажатых клавиш: {PRESSED_KEYS_QUANTITY}
Всего пройденного времени: {SUMMARY_TIME_PASSED}
Последний сеанс: {DURATION}
Начало: {START_TIME}
Конец: {END_TIME}
"""
