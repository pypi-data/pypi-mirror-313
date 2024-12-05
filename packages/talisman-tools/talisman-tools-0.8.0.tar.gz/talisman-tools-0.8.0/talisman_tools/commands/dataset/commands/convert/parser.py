from argparse import ArgumentParser, Namespace
from typing import Callable

from talisman_tools.arguments.serializer import get_serializer_factory
from tp_interfaces.readers.abstract import AbstractReader


def configure_convert_parser(parser: ArgumentParser) -> None:
    serializer_factory = get_serializer_factory(parser)

    def get_action() -> Callable[[AbstractReader, Namespace], None]:
        def action(reader: AbstractReader, args: Namespace) -> None:
            serializer_factory(args)(reader.read())

        return action

    parser.set_defaults(dataset_action=get_action)
