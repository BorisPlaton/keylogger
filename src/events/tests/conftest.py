import pytest

from events.event_channel import EventChannel


@pytest.fixture
def event_channel():
    return EventChannel()
