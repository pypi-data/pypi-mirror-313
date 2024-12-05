from argparse import ArgumentParser, Namespace
from typing import Callable

from talisman_tools.plugin import KBPlugins
from tp_interfaces.helpers.io import read_json
from tp_interfaces.loader.interfaces import Loader


def get_loader_factory(parser: ArgumentParser) -> Callable[[Namespace], Loader]:
    parser.add_argument('-loader_config_path', metavar='<kb config path>', required=True)

    def load_kb(args: Namespace) -> Loader:
        config = read_json(args.loader_config_path)
        kb = KBPlugins.plugins[config.get("plugin")][config.get("model", "default")].from_config(config.get('config', {}))
        return kb

    return load_kb
