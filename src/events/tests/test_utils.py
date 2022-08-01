import pytest

from events.exceptions import WrongEventName
from events.utils import is_event_correct, Event


@pytest.mark.parametrize(
    'wrong_event_name',
    {
        1, 2, 'KEY_LOGGING_STOPPED', Event,
        '', False
    }
)
def test_is_event_correct_decorator_raises_error(wrong_event_name):
    func = lambda: True
    func = is_event_correct(func)
    with pytest.raises(WrongEventName):
        func(wrong_event_name)


@pytest.mark.parametrize(
    'correct_event_name',
    {
        Event.SHOW_MENU, Event.KEY_LOGGING_STARTED,
        Event.KEY_LOGGING_STOPPED
    }
)
def test_is_event_correct_with_correct_events(correct_event_name):
    @is_event_correct
    def func(*args, **kwargs):
        return True

    assert func(correct_event_name)
    assert func(some_kwarg=correct_event_name)
    assert func(2, 3, {}, correct_event_name)
    assert func(2, 3, {}, k=correct_event_name)
