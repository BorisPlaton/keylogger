from core.apps import Keylog, Results


endpoints = {
    'start_keylog': Keylog().start_key_logging,
    'show_user_statistics': Results().show_user_statistic_records,
}
