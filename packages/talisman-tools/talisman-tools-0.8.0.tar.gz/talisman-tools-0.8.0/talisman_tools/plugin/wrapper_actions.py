from typing import Callable, FrozenSet

from talisman_tools.configure.wrapper import DEFAULT_WRAPPER_ACTIONS
from tp_interfaces.abstract import AbstractDocumentProcessor
from .abstract import AbstractPluginManager


class WrapperActionsPluginManager(AbstractPluginManager):
    def __init__(self):
        AbstractPluginManager.__init__(self, 'WRAPPER_ACTIONS', DEFAULT_WRAPPER_ACTIONS)

    def add_wrapper_action(self, key: FrozenSet[str], action: Callable[[dict], AbstractDocumentProcessor]) -> None:
        # TODO: rewrite it with some context menager that restore initial PM state on exit
        self._registered_plugins[None][key] = action

    @staticmethod
    def _check_value(value) -> bool:
        return isinstance(value, dict) and all(WrapperActionsPluginManager._validate_key_value(k, v) for k, v in value.items())

    @staticmethod
    def _validate_key_value(key, value) -> bool:
        return isinstance(key, frozenset)
