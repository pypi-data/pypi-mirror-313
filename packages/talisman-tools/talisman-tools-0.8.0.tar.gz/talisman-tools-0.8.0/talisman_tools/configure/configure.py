import json
import logging
import operator
from itertools import groupby, starmap
from os import PathLike
from pathlib import Path
from pickle import PickleError
from typing import Callable, Dict, FrozenSet, Iterable, List, Tuple, Union

import yaml

from tp_interfaces.abstract import AbstractDocumentProcessor
from tp_interfaces.abstract.processor.processor import AbstractSerializableDocumentProcessor
from tp_interfaces.processors.updatable_composite import UpdatableSequentialDocumentProcessor
from tp_interfaces.serializable import load_object

ActionsType = Dict[FrozenSet[str], Callable[[dict], AbstractDocumentProcessor]]

_logger = logging.getLogger(__name__)


def _process_config(config: dict) -> AbstractDocumentProcessor:
    from talisman_tools.plugin import WrapperActionsPlugins

    plugin = config.get("plugin")
    actions = WrapperActionsPlugins.plugins[plugin]

    proper_actions = [action for required_key_set, action in actions.items() if required_key_set <= set(config.keys())]
    if len(proper_actions) > 1:
        raise Exception("Provided config can be processed by multiple actions")
    if len(proper_actions) == 0:
        raise Exception("Provided config can not be processed by any action")

    action, = proper_actions
    return action(config)


def wrap_model_from_config(config: Union[List[dict], dict], *, merge: bool = True) -> AbstractDocumentProcessor:
    if isinstance(config, list) and len(config) == 1:
        config = config[0]
    if isinstance(config, dict):
        return _process_config(config)
    if isinstance(config, list):
        if len(config) == 0:
            raise Exception("Provided list config has no elements")

        def _process_sequential_config(cfg: dict) -> Tuple[str, AbstractDocumentProcessor]:
            return cfg.get("name", ''), _process_config(cfg)

        processors = tuple(map(_process_sequential_config, config))
        if len(processors) != len(set(map(operator.itemgetter(0), processors))):
            raise ValueError(f"processor names collision")

        return UpdatableSequentialDocumentProcessor.build(processors, merge=merge)

    else:
        raise Exception("Provided config contains neither list, nor dict")


def configure_model(config: Union[List[dict], dict], *, merge: bool = True) -> AbstractDocumentProcessor:
    from talisman_tools.plugin import ProcessorPlugins  # inline import to avoid circular imports

    if isinstance(config, list) and len(config) == 1:
        config = config[0]
    if isinstance(config, dict):  # build model from config
        if config.get("plugin") is None and config["model"] == "wrapper":
            return wrap_model_from_config(config["config"], merge=merge)
        return ProcessorPlugins.plugins[config["plugin"]][config["model"]].from_config(config.get("config", {}))
    if isinstance(config, list):
        if len(config) == 0:
            raise Exception("Couldn't configure empty list model")
        key = lambda c: (c.get("plugin", ''), c["model"])
        groupped = {k: tuple(v) for k, v in groupby(config, key=key)}

        models = []

        for (plugin, model), cfgs in groupped.items():
            if plugin == '' and model == "wrapper":
                for cfg in cfgs:
                    models.append((cfg.get("name", ''), configure_model(cfg, merge=merge)))
                continue
            type_ = ProcessorPlugins.plugins[plugin][model]
            for cfg in cfgs:
                models.append((cfg.get("name", ''), type_.from_config(cfg.get("config", {}))))

        return UpdatableSequentialDocumentProcessor.build(models, merge=merge)


def load_or_configure(model_or_config_named_paths: Iterable[Tuple[str, Union[str, PathLike]]], *, merge: bool = True) \
        -> AbstractDocumentProcessor:
    def load_as_model(model_path: Path) -> AbstractDocumentProcessor:
        return load_object(model_path, expected_class=AbstractSerializableDocumentProcessor)

    def load_as_config(config_path: Path) -> AbstractDocumentProcessor:
        config = read_config(config_path)
        return configure_model(config, merge=merge)

    def convert_to_model(model_or_config_path: Path) -> AbstractDocumentProcessor:
        if model_or_config_path.is_dir() or model_or_config_path.suffix == '.pkl':
            return load_as_model(model_or_config_path)

        if model_or_config_path.suffix == '.json' or model_or_config_path.suffix == '.yaml':
            return load_as_config(model_or_config_path)

        _logger.warning(f'Unrecognized filename extension for {model_or_config_path}')

        try:
            return load_as_config(model_or_config_path)
        except ValueError:
            pass

        try:
            return load_as_model(model_or_config_path)
        except PickleError:
            pass

        raise ValueError(f'Unable to read {model_or_config_path} neither as model configuration file nor as serialized model file!')

    def convert(name: str, model_or_config_path: Union[str, PathLike]) -> Tuple[str, AbstractDocumentProcessor]:
        return name, convert_to_model(Path(model_or_config_path))

    models = tuple(starmap(convert, model_or_config_named_paths))

    if not models:
        raise ValueError("Neither model paths nor model configs were provided")

    # here we could get `Composite(Composite(...), Composite(...))`
    return UpdatableSequentialDocumentProcessor.build(models, merge=merge)


def read_config(path: Union[str, Path]):
    with open(path, "r", encoding="utf-8") as f:
        if Path(path).suffix[1:] == "yaml":
            return yaml.safe_load(f)
        return json.load(f)
