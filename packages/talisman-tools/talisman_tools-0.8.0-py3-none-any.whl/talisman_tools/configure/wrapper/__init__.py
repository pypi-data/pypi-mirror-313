__all__ = [
    'DEFAULT_WRAPPER_ACTIONS'
]

from .actions import configure_model_action, wrap_model_action

DEFAULT_WRAPPER_ACTIONS = {
    frozenset(("wrapper", "to_wrap")): wrap_model_action,
    frozenset(("model", )): configure_model_action
}
