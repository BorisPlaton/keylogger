from importlib import import_module

from common.exceptions import ImproperlyConfiguredError


class EndpointsHandler:
    """
    Вызывает функции, что переданы в переменной с именем
    `EndpointsHandler.endpoints_dict_name`.
    """

    endpoints_dict_name = 'endpoints'

    def invoke(self, endpoint: str, *args):
        """
        Вызывает функцию из словаря `self.endpoints`, которая
        получается по ключу `endpoint`. Если были переданы
        параметры, то передаются соответствующей функции.
        """
        try:
            func = self.endpoints[endpoint]
        except KeyError:
            raise KeyError("`%s` is a wrong endpoint." % endpoint)
        else:
            return func(*args)

    def load_endpoints(self, endpoints_module: str):
        """
        Загружает переменную с именем `EndpointsHandler.endpoints_dict_name`
        из `endpoints_module`.
        """
        self.endpoints = self.get_endpoints_dict(endpoints_module)

    def get_endpoints_dict(self, endpoints_module: str):
        """
        Возвращает словарь с именем `EndpointsHandler.endpoints_dict_name`
        из файла `endpoints_module`.
        """
        if not isinstance(self.endpoints_dict_name, str):
            raise ImproperlyConfiguredError("`EndpointsHandler.endpoints_dict_name` variable must be a string.")
        elif not self.endpoints_dict_name:
            raise ImproperlyConfiguredError("`EndpointsHandler.endpoints_dict_name` variable can't be empty.")

        endpoints_dict = getattr(import_module(endpoints_module), self.endpoints_dict_name)

        if not isinstance(endpoints_dict, dict):
            raise ImproperlyConfiguredError("Variable `endpoints` must be a `dict` type.")

        return endpoints_dict

    def __init__(self, endpoints_file=None):
        """
        Сохраняет словарь `endpoints` из модуля `endpoints_file`, если
        последний был передан.
        """
        self.endpoints = {}
        if endpoints_file:
            self.load_endpoints(endpoints_file)
