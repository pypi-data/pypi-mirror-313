from argparse import ArgumentParser
from typing import Callable, Dict, Tuple

from .converter import configure_converter_parser
from .loader import configure_loader_parser
from .processor import configure_processor_parser

# Every subcommand should have its own parser with description
# Note that subparsers should change the default `server_action` argument
SUBPARSERS: Dict[str, Tuple[str, Callable[[ArgumentParser], None]]] = {
    'loader': ('Configure loader server', configure_loader_parser),
    'processor': ('Configure processor server', configure_processor_parser),
    'converter': ('Configure document converter', configure_converter_parser)
}
