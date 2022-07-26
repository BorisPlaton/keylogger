from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime
from typing import NamedTuple, Any

from core.endpoints_handler import EndpointsHandler


RESULTS_NAME = 'result_date'


class ArgumentChoice(NamedTuple):
    name: str
    value: Any


def get_parser() -> ArgumentParser:
    """Создаёт и возвращает экземпляр класса `argparse.ArgumentParser`."""
    arg_parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    arg_parser.add_argument(
        '-r', '--results',
        help="shows user's statistics for a specific date;shows today's results by default;\n"
             "date format should be 'YYYY-MM-DD', for example - 2022-05-25",
        nargs='?', metavar='DATE', const=datetime.now(), dest=RESULTS_NAME,
    )
    return arg_parser


def get_arguments() -> list[ArgumentChoice | None]:
    """Возвращает аргументы, которые были выбраны пользователем."""
    arg_parser = get_parser()
    args = arg_parser.parse_args()
    args_list: list[ArgumentChoice | None] = []

    if arg_value := getattr(args, RESULTS_NAME):
        args_list.append(ArgumentChoice(RESULTS_NAME, arg_value))

    return args_list


def main():
    """
    Запускает выполнение приложение в зависимости от параметров,
    которые были переданы в терминал.
    """
    handler = EndpointsHandler('core.endpoints')
    for argument in get_arguments():
        if argument.name == RESULTS_NAME:
            return handler.invoke('show_user_results', argument.value)
    else:
        return handler.invoke('start_keylog')
