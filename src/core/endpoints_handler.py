from importlib import import_module

from core.exceptions import ImproperlyConfiguredError


class EndpointsHandler:
    """Вызывает функции, что переданы в словаре `endpoints`."""

    def invoke(self, endpoint: str, *args):
        """
        Вызывает функцию из словаря `self.endpoints`, которая
        получается по ключу `endpoint`. Если были переданы
        параметры, то передаются соответствующей функции.
        """
        try:
            func = self.endpoints[endpoint]
        except KeyError:
            raise KeyError("`%s` неверный endpoint." % endpoint)
        else:
            func(*args)

    def load_endpoints(self, endpoints_module: str):
        """
        Загружает переменную `endpoints` из `endpoints_module`,
        который должен быть *.py файлом. Если такой переменной нет,
        будет вызвано исключение.
        """
        endpoints_dict = getattr(import_module(endpoints_module), 'endpoints')
        if endpoints_dict is None:
            raise ImproperlyConfiguredError("Нет переменной `endpoints` в %s" % endpoints_module)
        elif not isinstance(endpoints_dict, dict):
            raise ImproperlyConfiguredError("Переменная `endpoints` должна быть типа `dict`.")
        setattr(self, 'endpoints', endpoints_dict)

    def __init__(self, endpoints_file=None):
        """
        Сохраняет словарь `endpoints` из модуля `endpoints_file`, если
        последний был передан.
        """
        self.endpoints = {}
        if endpoints_file:
            self.load_endpoints(endpoints_file)
