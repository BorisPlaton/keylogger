from datetime import datetime

from time_handler.stopwatch import Stopwatch


def test_key_logging_started_event(keylog_data):
    stopwatch = Stopwatch(keylog_data)
    start_time = datetime.now().replace(microsecond=0)
    assert keylog_data.start_time is None
    stopwatch.key_logging_started()
    assert start_time == keylog_data.start_time.replace(microsecond=0)
    assert keylog_data.summary_passed_time is None
    assert keylog_data.end_time is None


def test_key_logging_stopped_event(keylog_data):
    stopwatch = Stopwatch(keylog_data)
    end_time = datetime.now().replace(microsecond=0)
    assert keylog_data.end_time is None
    stopwatch.key_logging_stopped()
    keylog_data.end_time = keylog_data.end_time.replace(microsecond=0)
    assert end_time == keylog_data.end_time
    assert keylog_data.summary_passed_time is None
