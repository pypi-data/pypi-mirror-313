from typing import Callable, Type

from tp_interfaces.domain.interfaces import DomainProducer
from .abstract import AbstractPluginManager


def _get_stub() -> Type[DomainProducer]:
    from tp_interfaces.domain.stub import StubDomainProducer
    return StubDomainProducer


class DomainPluginManager(AbstractPluginManager):
    def __init__(self):
        AbstractPluginManager.__init__(self, 'DOMAIN_FACTORY', _get_stub)

    @staticmethod
    def _check_value(value) -> bool:
        return isinstance(value, Callable)
