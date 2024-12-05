from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Callable

from tp_interfaces.abstract import AbstractDocumentProcessor


def configure_configure_parser(parser: ArgumentParser) -> None:
    parser.add_argument('out_path', type=Path, metavar='<model out path>')

    def get_action() -> Callable[[AbstractDocumentProcessor, Namespace], None]:
        def action(processor: AbstractDocumentProcessor, args: Namespace) -> None:
            processor.save(args.out_path)
            print(f"Saved {processor} model")

        return action

    parser.set_defaults(processor_action=get_action)
