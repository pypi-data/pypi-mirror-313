from typing import Callable, Dict

from tp_interfaces.serializers.abstract import AbstractSerializer
from .abstract import AbstractPluginManager, flattened


class SerializerPluginManager(AbstractPluginManager):
    def __init__(self):
        AbstractPluginManager.__init__(self, 'SERIALIZERS')

    @property
    def flattened(self) -> Dict[str, Callable[[], AbstractSerializer]]:
        return flattened(self.plugins)

    @staticmethod
    def _check_value(value) -> bool:
        return isinstance(value, dict)  # TODO: improve validation
