from argparse import ArgumentParser, Namespace
from typing import Callable, Set

from .abstract import AbstractPluginManager


class CLIPluginManager(AbstractPluginManager):
    def __init__(self):
        AbstractPluginManager.__init__(self, 'CLI_OPTIONS')

    @staticmethod
    def _check_value(value) -> bool:
        return isinstance(value, dict) and all(CLIPluginManager._check_pair(k, v) for k, v in value.items())

    @staticmethod
    def _check_pair(key, value) -> bool:
        return isinstance(key, str) and isinstance(value, set) and all(isinstance(v, Callable) for v in value)  # TODO: improve validation


def add_extra_cli_arguments(parser: ArgumentParser, key: str) -> Set[Callable[[Namespace], None]]:
    from talisman_tools.plugin import CLIPlugins
    actions = set()
    for cli_factory in CLIPlugins.plugins.values():
        factories = cli_factory.get(key)
        if factories:
            actions.update(factory(parser) for factory in factories)
    return actions
