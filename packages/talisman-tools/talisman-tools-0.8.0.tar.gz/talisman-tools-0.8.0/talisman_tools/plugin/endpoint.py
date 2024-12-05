from pathlib import Path
from typing import Callable, Dict

from talisman_tools.plugin.abstract import AbstractPluginManager, flattened
from tp_interfaces.abstract import ModelTypeFactory
from tp_interfaces.readers.abstract import AbstractReader


class EndpointPluginManager(AbstractPluginManager):
    def __init__(self):
        AbstractPluginManager.__init__(self, 'ENDPOINTS')

    @property
    def flattened(self) -> Dict[str, Callable[[Path], AbstractReader]]:
        return flattened(self.plugins, delimiter='/', start='/')

    @staticmethod
    def _check_value(value) -> bool:
        return isinstance(value, ModelTypeFactory)  # TODO: validate signature
