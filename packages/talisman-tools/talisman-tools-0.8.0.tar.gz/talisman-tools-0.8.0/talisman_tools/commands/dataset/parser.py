from argparse import ArgumentParser, Namespace
from typing import Callable

from talisman_tools.arguments.reader import get_reader_factory
from talisman_tools.parser_helper import configure_subparsers


def configure_dataset_parser(parser: ArgumentParser) -> None:
    from .commands import SUBPARSERS

    reader_factory = get_reader_factory(parser, {'docs_path': '<docs path>'})

    def get_action() -> Callable[[Namespace], None]:
        def action(args: Namespace) -> None:
            args.dataset_action()(reader_factory(args)['docs_path'], args)

        return action

    parser.set_defaults(action=get_action)
    configure_subparsers(parser, SUBPARSERS)
