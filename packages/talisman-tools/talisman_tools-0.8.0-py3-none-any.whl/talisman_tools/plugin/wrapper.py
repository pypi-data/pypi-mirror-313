from tp_interfaces.abstract import ModelTypeFactory
from .abstract import AbstractPluginManager


class WrapperPluginManager(AbstractPluginManager):
    def __init__(self):
        AbstractPluginManager.__init__(self, 'WRAPPERS')

    @staticmethod
    def _check_value(value) -> bool:
        return isinstance(value, ModelTypeFactory)
