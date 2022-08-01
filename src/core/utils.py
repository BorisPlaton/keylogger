from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime
from typing import TypedDict

from core.endpoints_handler import EndpointsHandler


class ParserArguments(TypedDict):
    results: str | datetime | None
    separate: bool


def get_parser() -> ArgumentParser:
    """Создаёт и возвращает экземпляр класса `argparse.ArgumentParser`."""
    arg_parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    arg_parser.add_argument(
        '-r', '--results',
        help="show user's statistics for a specific date;show today's results by default;\n"
             "date format should be 'YYYY-MM-DD', for example - 2022-05-25",
        nargs='?', metavar='DATE', const=datetime.now(),
    )
    arg_parser.add_argument(
        '-s', '--separate',
        help="if -r option is provided, all result records will be shown separately;",
        action='store_false',
    )
    return arg_parser


def get_arguments(arguments: str = '') -> ParserArguments:
    """Возвращает аргументы, которые были выбраны пользователем."""
    args = get_parser().parse_args(arguments.split())
    args_dict: ParserArguments = {
        'results': args.results,
        'separate': args.separate,
    }
    return args_dict


def main():
    """
    Запускает выполнение приложение в зависимости от параметров,
    которые были переданы в терминал.
    """
    handler = EndpointsHandler('core.endpoints')
    user_args = get_arguments()
    if result_date := user_args['results']:
        return handler.invoke('show_user_statistics', result_date, user_args['separate'])
    else:
        return handler.invoke('start_keylog')
