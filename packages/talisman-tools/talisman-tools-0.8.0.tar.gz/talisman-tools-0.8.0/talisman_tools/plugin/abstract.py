from importlib.metadata import entry_points
from types import ModuleType
from typing import Any, Dict, Optional, TypeVar

GROUP = "talisman.plugins"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AbstractPluginManager(metaclass=Singleton):
    def __init__(self, attr: str, default=None):
        self._registered_plugins = {}
        if default is not None:
            self._registered_plugins[None] = default

        for entry_point in entry_points(group=GROUP):
            name = entry_point.name
            module = entry_point.load()
            if not isinstance(module, ModuleType):
                continue
            try:
                value = getattr(module, attr)
                if self._check_value(value):
                    self._registered_plugins[name] = value
            except AttributeError:
                pass

        self._disabled_plugins = set()

    @property
    def plugins(self) -> Dict[Optional[str], Any]:
        return {plugin: value for plugin, value in self._registered_plugins.items() if plugin not in self._disabled_plugins}

    @staticmethod
    def _check_value(value) -> bool:
        return True

    def disable_plugin(self, plugin: str):
        self._disabled_plugins.add(plugin)

    def enable_plugin(self, plugin: str):
        self._disabled_plugins.discard(plugin)


_T = TypeVar('_T')


def flattened(data: Dict[str, Dict[str, _T]], *, delimiter: str = ':', start: str = '') -> Dict[str, _T]:
    result = {}
    for plugin, readers in data.items():
        for key, reader in readers.items():
            result[f"{start}{plugin}{delimiter}{key}"] = reader
    return result
