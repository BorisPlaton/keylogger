import typing
from datetime import datetime

import pytest

from common.utils import from_datetime_to_str, VALID_DATES, from_str_to_datetime
from configuration.settings import settings


def test_valid_dates_is_equal_to_settings_data_formats():
    for time_moment in settings.DATA_FORMATS:
        assert time_moment in typing.get_args(VALID_DATES)


@pytest.mark.parametrize(
    "time_format,time_moment",
    [
        ('START_TIME', datetime.now()),
        ('SESSION_START_TIME', datetime.now()),
        ('SESSION_END_TIME', datetime.now()),
        ('INPUT_DATE', datetime.now()),
        ('RESULT_DATE', datetime.now()),
        ('END_TIME', datetime.now()),
        ('DB_FORMAT', datetime.now()),
    ]
)
def test_from_datetime_to_str(time_format: VALID_DATES, time_moment: datetime):
    string_repr = from_datetime_to_str(time_format, time_moment)
    manual_string_repr = time_moment.strftime(settings.DATA_FORMATS[time_format])
    assert string_repr == manual_string_repr


@pytest.mark.parametrize(
    "time_format,time_moment",
    [
        ('START_TIME', datetime.now()),
        ('SESSION_START_TIME', datetime.now()),
        ('SESSION_END_TIME', datetime.now()),
        ('INPUT_DATE', datetime.now()),
        ('RESULT_DATE', datetime.now()),
        ('END_TIME', datetime.now()),
        ('DB_FORMAT', datetime.now()),
    ]
)
def test_from_str_to_datetime(time_format: VALID_DATES, time_moment: datetime):
    string_repr = from_datetime_to_str(time_format, time_moment)
    manual_repr = datetime.strptime(string_repr, settings.DATA_FORMATS[time_format])
    assert from_datetime_to_str(time_format, manual_repr) == string_repr


@pytest.mark.parametrize(
    'wrong_time_moment',
    [
        1, 2, 3,
        'fsf', set(), 'start_time', ''
    ]
)
def test_wrong_time_moment_raises_error(wrong_time_moment):
    with pytest.raises(Exception):
        from_datetime_to_str(wrong_time_moment, datetime.now())
    with pytest.raises(Exception):
        from_str_to_datetime(wrong_time_moment, 'some str')
