import pytest

from data_storage.storages import KeylogData


@pytest.fixture
def keylog_data():
    return KeylogData()
