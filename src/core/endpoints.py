from core.apps import Keylogger, Results


endpoints = {
    'start_keylog': Keylogger().start_key_logging,
    'show_user_statistics': Results().show_user_statistic_records,
}
