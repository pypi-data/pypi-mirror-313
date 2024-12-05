from tp_interfaces.abstract import AbstractDocumentProcessor
from .configure import wrap_model_from_config


def wrap_model(model: AbstractDocumentProcessor, config: dict, *, merge: bool = True):
    from talisman_tools.plugin import WrapperActionsPlugins
    WrapperActionsPlugins.add_wrapper_action(frozenset(('wrapped',)), lambda c: model)
    return wrap_model_from_config(config, merge=merge)
