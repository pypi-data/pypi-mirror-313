from pathlib import Path
from typing import Callable, Dict

from tp_interfaces.readers.abstract import AbstractConfigurableReader, AbstractReader
from .abstract import AbstractPluginManager, flattened


class ReaderPluginManager(AbstractPluginManager):
    def __init__(self):
        AbstractPluginManager.__init__(self, 'READERS')

    @property
    def flattened(self) -> Dict[str, Callable[[Path], AbstractReader]]:
        return flattened(self.plugins)

    @staticmethod
    def _check_value(value) -> bool:
        return isinstance(value, dict)  # TODO: improve validation


class ConfigurableReaderPluginManager(AbstractPluginManager):
    def __init__(self):
        AbstractPluginManager.__init__(self, 'CONFIGURABLE_READERS')

    @property
    def flattened(self) -> Dict[str, Callable[[dict], AbstractConfigurableReader]]:
        return flattened(self.plugins)

    @staticmethod
    def _check_value(value) -> bool:
        return isinstance(value, dict)  # TODO: improve validation
