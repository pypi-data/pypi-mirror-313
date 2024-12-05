from tp_interfaces.abstract import ModelTypeFactory
from .abstract import AbstractPluginManager


class ProcessorPluginManager(AbstractPluginManager):
    def __init__(self):
        AbstractPluginManager.__init__(self, 'PROCESSORS')

    @staticmethod
    def _check_value(value) -> bool:
        return isinstance(value, ModelTypeFactory)
