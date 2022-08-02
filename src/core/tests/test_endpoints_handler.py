import pytest

from common.exceptions import ImproperlyConfiguredError


def test_handler_initialization(endpoints_handler, endpoints_module):
    assert not endpoints_handler.endpoints
    assert endpoints_handler.endpoints_dict_name == 'endpoints'
    with pytest.raises(ImproperlyConfiguredError):
        endpoints_handler.endpoints_dict_name = 2
        endpoints_handler.get_endpoints_dict(endpoints_module)
    with pytest.raises(ImproperlyConfiguredError):
        endpoints_handler.endpoints_dict_name = ''
        endpoints_handler.get_endpoints_dict(endpoints_module)


def test_invalid_configured_endpoints_module(endpoints_handler, endpoints_module):
    with pytest.raises(AttributeError):
        endpoints_handler.get_endpoints_dict(endpoints_module)
    with pytest.raises(ImproperlyConfiguredError):
        endpoints_handler.endpoints_dict_name = 'not_dict_type'
        endpoints_handler.get_endpoints_dict(endpoints_module)


def test_endpoint_invoking_endpoints(endpoints_handler, endpoints_module):
    endpoints_handler.endpoints_dict_name = 'endpoints_dict'
    endpoints_handler.load_endpoints(endpoints_module)
    assert 'first_endpoint' in endpoints_handler.endpoints
    assert endpoints_handler.invoke('first_endpoint')
    with pytest.raises(KeyError):
        endpoints_handler.invoke('not existing endpoint')
