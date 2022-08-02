import pytest

from core.endpoints_handler import EndpointsHandler


@pytest.fixture
def endpoints_handler():
    return EndpointsHandler()


@pytest.fixture
def endpoints_module():
    return 'core.tests.source.endpoints_test'
