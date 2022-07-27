from pathlib import Path

from pynput.keyboard import Key

from configuration.settings import KeyConfig


BASE_DIR = Path(__file__).resolve().parent.parent

START_KEY = KeyConfig(Key.f1, 'F1')
STOP_KEY = KeyConfig(Key.f1, 'F1')
EXIT_KEY = KeyConfig(Key.f2, 'F2')
DB_LOCATION = BASE_DIR / 'keylog.db'

DATA_FORMATS = {
    'START_TIME': '%H:%M',
    'SESSION_START_TIME': '%d %B, %H:%M',
    'SESSION_END_TIME': '%d %B, %H:%M',
    'RESULT_DATE': '%d %B, %Y',
    'INPUT_DATE': '%Y-%m-%d'
}

KEY_LOGGING_HELP_TEXT = """
{START_TIME}, Начало работы:
 `{STOP_KEY}` Остановить запись
"""

MENU_TEXT = """
Меню:
 `{START_KEY}` Начать запись
 `{EXIT_KEY}` Завершение работы
"""

KEYLOGGER_STATISTICS = """
Статистика:
  Общие данные:
    - Прошло времени: {SUMMARY_TIME_PASSED}
    - Нажато клавиш: {SUMMARY_PRESSED_KEYS_QUANTITY} раз(a)
    - Скорость набора: {SUMMARY_AVERAGE_KEY_SPEED} кл/мин
  Последняя сессия:
    - Начало сессии: {SESSION_START_TIME}
    - Конец сессии: {SESSION_END_TIME}
    - Прошло времени: {LAST_SESSION_TIME_PASSED}
    - Нажато клавиш: {LAST_SESSION_PRESSED_KEYS_QUANTITY} раз(a)
    - Скорость набора: {LAST_SESSION_AVERAGE_KEY_SPEED} кл/мин
"""

RESULT_STATISTICS = """{RESULT_DATE}:
- Пройдено времени: {SUMMARY_TIME_PASSED}
- Нажато клавиш: {SUMMARY_PRESSED_KEYS_QUANTITY} раз(a)
- Скорость набора: {SUMMARY_AVERAGE_KEY_SPEED} кл/мин
"""
