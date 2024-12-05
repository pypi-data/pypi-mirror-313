from argparse import ArgumentParser, Namespace
from typing import Callable

from fastapi import FastAPI

from talisman_tools.arguments.domain import get_domain_factory


def configure_converter_parser(parser: ArgumentParser) -> None:
    domain_factory = get_domain_factory(parser)

    def get_action() -> Callable[[Namespace], FastAPI]:
        def action_with_extra(args: Namespace) -> FastAPI:
            from .action import action
            domain_factory(args)
            return action(args)

        return action_with_extra

    parser.set_defaults(server_action=get_action)
