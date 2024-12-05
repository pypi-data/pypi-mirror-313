from argparse import ArgumentParser
from typing import Callable, Dict, Tuple

from talisman_tools.commands.dataset.parser import configure_dataset_parser
from talisman_tools.commands.model.parser import configure_model_parser
from talisman_tools.commands.servers.parser import configure_server_parser
from talisman_tools.commands.train.parser import configure_train_parser

# Note that subparsers should change the default `action` argument
SUBPARSERS: Dict[str, Tuple[str, Callable[[ArgumentParser], None]]] = {
    'server': ('Configure server', configure_server_parser),
    'model': ('Evaluate and configure models', configure_model_parser),
    'dataset': ('Handle datasets', configure_dataset_parser),
    'train': ('Train document processors', configure_train_parser)
}
