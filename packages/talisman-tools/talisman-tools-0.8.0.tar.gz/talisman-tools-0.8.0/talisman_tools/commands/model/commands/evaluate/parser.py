import asyncio
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Callable

from talisman_tools.arguments.reader import get_reader_factory
from talisman_tools.commands.model.commands.evaluate.action import mode  # TODO: pulling unused dependencies
from tp_interfaces.abstract import AbstractDocumentProcessor


def configure_evaluate_parser(parser: ArgumentParser) -> None:
    parser.add_argument('eval_mode', type=str, choices=set(mode), metavar='<evaluation mode>')
    parser.add_argument('--config', type=Path, metavar='<document processing config path>')
    parser.add_argument('--eval_config', type=Path, metavar='<evaluation config path>')

    reader_factory = get_reader_factory(parser, {'gold_path': '<path to gold>', '-input_docs': '<input documents path>'})

    def get_action() -> Callable[[AbstractDocumentProcessor, Namespace], None]:
        def action(processor: AbstractDocumentProcessor, args: Namespace) -> None:
            from .action import evaluate
            readers = reader_factory(args)
            asyncio.run(evaluate(
                processor, args.eval_mode, readers['gold_path'], args.config, args.eval_config, input_reader=readers.get('-input_docs')
            ))

        return action

    parser.set_defaults(processor_action=get_action)
