from argparse import ArgumentParser
from typing import Callable, Dict, Tuple

from talisman_tools.commands.dataset.commands.convert import configure_convert_parser

# Note that subparsers should change the default `dataset_action` argument
SUBPARSERS: Dict[str, Tuple[str, Callable[[ArgumentParser], None]]] = {
    'convert': ('', configure_convert_parser)
}
