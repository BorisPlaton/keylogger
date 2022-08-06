from datetime import datetime

from core.utils import get_parser, get_arguments


def test_parser_all_default_args_value():
    args = get_parser().parse_args()
    assert getattr(args, 'results') is None
    assert getattr(args, 'separate')


def test_get_arguments_return_value():
    args = get_arguments('-r 55 -s')
    assert args.results == '55'
    assert not args.separate
    args = get_arguments('-r')
    assert args.results.replace(microsecond=0) == datetime.now().replace(microsecond=0)
