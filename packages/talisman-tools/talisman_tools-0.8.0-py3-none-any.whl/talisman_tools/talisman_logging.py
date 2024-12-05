import logging
from argparse import ArgumentParser, Namespace
from typing import Callable

from jsonformatter import JsonFormatter


def create_json_formatter() -> JsonFormatter:
    return JsonFormatter(
        fmt={"level": "levelname", "msg": "message", "time": "asctime"},
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        mix_extra=True,
        skipkeys=True,
        ensure_ascii=False,
        default=lambda o: "NON-SERIALIZABLE"
    )


def configure_json_logging(level=logging.INFO):
    stderr_handler = logging.StreamHandler()
    json_formatter = create_json_formatter()
    stderr_handler.setFormatter(json_formatter)
    logging.basicConfig(level=level, handlers=[stderr_handler])


def get_logging_factory(parser: ArgumentParser) -> Callable[[Namespace], None]:
    logging_levels = {
        'info': logging.INFO,
        'debug': logging.DEBUG,
        'warning': logging.WARNING,
        'error': logging.ERROR
    }
    parser.add_argument('--logging_level', choices=list(logging_levels.keys()), default='info')

    def configure_logging(args: Namespace) -> None:
        logging_level = logging_levels[args.logging_level]
        configure_json_logging(level=logging_level)

    return configure_logging
