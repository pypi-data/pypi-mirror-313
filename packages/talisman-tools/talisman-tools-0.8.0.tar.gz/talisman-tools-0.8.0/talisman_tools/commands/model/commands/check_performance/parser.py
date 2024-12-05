import asyncio
from argparse import ArgumentParser, Namespace
from typing import Callable

from talisman_tools.arguments.domain import get_domain_factory
from talisman_tools.arguments.reader import get_reader_factory
from tp_interfaces.abstract import AbstractDocumentProcessor


def configure_check_performance_parser(parser: ArgumentParser) -> None:
    domain_factory = get_domain_factory(parser)
    reader_factory = get_reader_factory(parser, {'docs_path': '<docs path>'})

    parser.add_argument('count', type=int, metavar='<launch count>', default=1)

    def get_action() -> Callable[[AbstractDocumentProcessor, Namespace], None]:
        def action(processor: AbstractDocumentProcessor, args: Namespace):
            from .action import async_measure

            domain_factory(args)
            docs = tuple(reader_factory(args)['docs_path'].read())

            asyncio.run(
                async_measure(docs, processor, args.count)
            )

        return action

    parser.set_defaults(processor_action=get_action)
