import pytest

from data.storages import KeylogData


@pytest.fixture
def keylog_data():
    return KeylogData()
