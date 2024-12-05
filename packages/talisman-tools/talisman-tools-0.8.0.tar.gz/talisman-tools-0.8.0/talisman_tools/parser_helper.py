from argparse import ArgumentParser
from typing import Callable, Dict, Tuple


def configure_subparsers(
        parser: ArgumentParser,
        subparsers: Dict[str, Tuple[str, Callable[[ArgumentParser], None]]]
) -> None:
    subparsers_handler = parser.add_subparsers(help='Available sub-commands')
    for subparser_name, (description, configure) in subparsers.items():
        subparser = subparsers_handler.add_parser(subparser_name, help=description)
        try:
            configure(subparser)
        except ImportError:
            pass
