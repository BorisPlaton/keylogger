from pathlib import Path

from pynput.keyboard import Key

from configuration.settings import KeyConfig


BASE_DIR = Path(__file__).resolve().parent.parent

START_KEY = KeyConfig(Key.f1, 'F1')
STOP_KEY = KeyConfig(Key.f1, 'F1')
EXIT_KEY = KeyConfig(Key.f2, 'F2')

DB_LOCATION = BASE_DIR / 'keylog.db'

DATA_FORMATS = {
    'DB_FORMAT': '%Y-%m-%d %H:%M:%S.%f',
    'START_TIME': '%H:%M',
    'END_TIME': '%H:%M',
    'SESSION_START_TIME': '%d %B, %H:%M',
    'SESSION_END_TIME': '%d %B, %H:%M',
    'RESULT_DATE': '%d %B, %Y',
    'INPUT_DATE': '%Y-%m-%d'
}

KEY_LOGGING_HELP_TEXT = """
{START_TIME}, recording started:
 `{STOP_KEY}` Stop
"""

MENU_TEXT = """
Menu:
 `{START_KEY}` Start recording
 `{EXIT_KEY}` Exit
"""

KEYLOGGER_STATISTICS = """
Summary statistics:
  - Time passed: {SUMMARY_TIME_PASSED}
  - Keystrokes: {SUMMARY_PRESSED_KEYS_QUANTITY} times
  - Typing speed: {SUMMARY_AVERAGE_KEY_SPEED} key/min
Last session:
  - Started at: {SESSION_START_TIME}
  - Ended in: {SESSION_END_TIME}
  - Time passed: {LAST_SESSION_TIME_PASSED}
  - Keystrokes: {LAST_SESSION_PRESSED_KEYS_QUANTITY} times
  - Typing speed: {LAST_SESSION_AVERAGE_KEY_SPEED} key/min
"""

RESULT_STATISTICS = """{RESULT_DATE}:
- Time range: {START_TIME} - {END_TIME}
- Time passed: {SUMMARY_TIME_PASSED}
- Keystrokes: {SUMMARY_PRESSED_KEYS_QUANTITY} times
- Typing speed: {SUMMARY_AVERAGE_KEY_SPEED} key/min
"""

SUMMARY_RESULT_STATISTICS = """{RESULT_DATE}:
- Summary time passed: {SUMMARY_TIME_PASSED}
- Keystrokes: {SUMMARY_PRESSED_KEYS_QUANTITY} times
- Typing speed: {SUMMARY_AVERAGE_KEY_SPEED} key/min
"""
