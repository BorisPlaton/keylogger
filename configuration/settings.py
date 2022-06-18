from pathlib import Path

from pynput.keyboard import Key

from configuration.adds import KeyConfig


BASE_DIR = Path(__file__).resolve().parent.parent
WRITE_TO_FILE = True
RESULT_DIR = BASE_DIR / 'RESULTS'
TIME_RANGE = 60

START_KEY = KeyConfig(Key.f1, 'F1')
STOP_KEY = KeyConfig(Key.f1, 'F1')
EXIT_KEY = KeyConfig(Key.f2, 'F2')

DATA_FORMAT = "%d %b, %H:%M"

KEY_LOGGING_HELP_TEXT = """
Начало работы:
 {START_TIME}
 {STOP_KEY} - Остановить запись
"""

MENU_TEXT = """
Меню:
 {START_KEY} - Начать запись
 {EXIT_KEY} - Завершение работы
"""

KEYLOGGER_STATISTICS = """
Статистика:
 1. Общие данные
    - Прошло времени: {SUMMARY_TIME_PASSED}
    - Нажато клавиш: {SUMMARY_PRESSED_KEYS_QUANTITY} раз(a)
    - Скорость набора:
        {SUMMARY_WPM}
        {SUMMARY_AVERAGE_KEY_SPEED} кл/мин
 2. Последняя сессия
    - Начало сессии: {START_TIME}
    - Конец сессии: {END_TIME}
    - Прошло времени: {LAST_SESSION_PASSED_PASSED}
    - Нажато клавиш: {LAST_SESSION_PRESSED_KEYS_QUANTITY} раз(a)
    - Скорость набора:
        {LAST_SESSION_WPM}
        {LAST_SESSION_AVERAGE_KEY_SPEED} кл/мин
"""
