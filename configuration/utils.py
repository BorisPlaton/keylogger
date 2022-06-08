from . import settings as st


class Config:

    def __init__(self):
        self._config_list = [
            constant for constant in dir(st) if not constant.startswith('__')
        ]
        self.setup_config()

    def setup_config(self):
        for constant in self._config_list:
            setattr(self, constant, getattr(st, constant))


config = Config()
