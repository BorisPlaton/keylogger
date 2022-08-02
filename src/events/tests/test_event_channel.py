import pytest

from events.utils import Event


@pytest.mark.parametrize(
    'event',
    [
        Event.KEY_LOGGING_STARTED, Event.KEY_LOGGING_STOPPED,
        Event.SHOW_MENU
    ]
)
def test_event_channel(event, event_channel):
    var = []

    def func():
        var.append('func')

    event_channel.add_listener(event, func)
    assert not var
    event_channel.notify(event)
    assert 'func' in var
    assert len(var) == 1
    event_channel.remove(event, func)
    event_channel.notify(event)
    assert 'func' in var
    assert len(var) == 1


def test_event_dict_of_event_channel(event_channel):
    for event, listeners in event_channel.event_listeners.items():
        assert event in Event
        assert not listeners
