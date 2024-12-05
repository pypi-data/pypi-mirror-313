import logging

from talisman_tools.configure import configure_model
from tp_interfaces.abstract import AbstractDocumentProcessor

logger = logging.getLogger(__name__)


def wrap_model_action(config: dict) -> AbstractDocumentProcessor:
    """
    create model from config and wraps it with respect to specified wrapper and wrapper configuration
    :param config: dict with required "wrapper" and "to_wrap" keys. Optional "plugin" and "config" keys are taken into account
    :return: wrapped document processor
    """
    from talisman_tools.plugin import WrapperPlugins  # inline import to avoid circular imports
    if isinstance(config["wrapper"], dict):
        plugin = config["wrapper"].get("plugin")
        model = config["wrapper"]["model"]
    elif isinstance(config["wrapper"], str):
        plugin = None
        model = config["wrapper"]
    else:
        logger.error(f'"wrapper" configuration should be either `dict` or `str`. Actual type: {type(config["wrapper"])}')
        raise ValueError
    try:
        plugin_models = WrapperPlugins.plugins[plugin]
    except KeyError as e:
        logger.error(f"'{plugin}' has no registered wrappers. Available plugins: {list(WrapperPlugins.plugins.keys())}", exc_info=e)
        raise
    try:
        wrapper_factory = plugin_models[model]
    except KeyError as e:
        logger.error(f"'{plugin}' contains no '{model}' wrapper. Available models: {list(plugin_models.keys())}", exc_info=e)
        raise
    try:
        return wrapper_factory.from_config(configure_model(config['to_wrap']), config.get("config", {}))
    except Exception as e:
        raise ValueError(f"Couldn't instantiate {plugin}.{model} with specified config") from e


def configure_model_action(config: dict) -> AbstractDocumentProcessor:
    """
    create model from config
    :param config: dict with required "model" key
    :return: configured model
    """
    return configure_model(config)
