import pytest

from data_storage.storages import KeylogData
from events.event_channel import EventChannel


@pytest.fixture
def event_channel():
    return EventChannel()


@pytest.fixture
def data_storage():
    return KeylogData()
