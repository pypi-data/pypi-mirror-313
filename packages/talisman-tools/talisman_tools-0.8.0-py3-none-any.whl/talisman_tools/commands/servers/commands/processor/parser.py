from argparse import ArgumentParser, Namespace
from typing import Callable

from fastapi import FastAPI

from talisman_tools.arguments.domain import get_domain_factory
from talisman_tools.arguments.processor import get_processor_factory
from talisman_tools.plugin.cli import add_extra_cli_arguments


def configure_processor_parser(parser: ArgumentParser) -> None:
    domain_factory = get_domain_factory(parser)
    processor_factory = get_processor_factory(parser)

    extra_actions = add_extra_cli_arguments(parser, 'processor')

    def get_action() -> Callable[[Namespace], FastAPI]:
        def action_with_extra(args: Namespace) -> FastAPI:
            for action in extra_actions:
                action(args)
            from .action import action
            domain_factory(args)
            return action(args, processor_factory)

        return action_with_extra

    parser.set_defaults(server_action=get_action)
