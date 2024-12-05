from argparse import ArgumentParser, Namespace
from typing import Callable

from fastapi import FastAPI

from talisman_tools.arguments.domain import get_domain_factory
from talisman_tools.arguments.loader import get_loader_factory


def configure_loader_parser(parser: ArgumentParser) -> None:
    loader_factory = get_loader_factory(parser)
    domain_factory = get_domain_factory(parser)

    def get_action() -> Callable[[Namespace], FastAPI]:
        def action_with_extra(args: Namespace) -> FastAPI:
            from .action import action
            domain_factory(args)
            loader = loader_factory(args)
            return action(args, loader)

        return action_with_extra

    parser.set_defaults(server_action=get_action)
