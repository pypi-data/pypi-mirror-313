import asyncio
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Callable

from talisman_tools.arguments.domain import get_domain_factory
from talisman_tools.arguments.reader import get_reader_factory
from talisman_tools.arguments.serializer import get_serializer_factory
from tp_interfaces.abstract import AbstractDocumentProcessor


def configure_process_parser(parser: ArgumentParser) -> None:
    domain_factory = get_domain_factory(parser)
    reader_factory = get_reader_factory(parser, {'docs_path': '<docs path>'})
    serializer_factory = get_serializer_factory(parser)

    parser.add_argument('--config', type=Path, metavar='<document processing config path>')
    parser.add_argument('--batch', type=int, metavar='<batch size>', default=1000)

    def get_action() -> Callable[[AbstractDocumentProcessor, Namespace], None]:
        def action(processor: AbstractDocumentProcessor, args: Namespace) -> None:
            domain_factory(args)
            reader = reader_factory(args)['docs_path']
            serializer = serializer_factory(args)
            from .action import async_action
            return asyncio.run(async_action(processor, serializer, reader, args))

        return action

    parser.set_defaults(processor_action=get_action)
