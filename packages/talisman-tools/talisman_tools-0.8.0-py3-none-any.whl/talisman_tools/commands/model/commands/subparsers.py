from argparse import ArgumentParser
from typing import Callable, Dict, Tuple

from talisman_tools.commands.model.commands.check_performance import configure_check_performance_parser
from talisman_tools.commands.model.commands.configure import configure_configure_parser
from talisman_tools.commands.model.commands.evaluate import configure_evaluate_parser
from talisman_tools.commands.model.commands.process import configure_process_parser

# Note that subparsers should change the default `processor_action` argument
SUBPARSERS: Dict[str, Tuple[str, Callable[[ArgumentParser], None]]] = {
    'check_performance': ('Check performance of document processors', configure_check_performance_parser),
    'configure': ('Configure models from configuration files', configure_configure_parser),
    'evaluate': ('Evaluate document processors on a number of metrics', configure_evaluate_parser),
    'process': ('Process documents with document processor', configure_process_parser)
}
