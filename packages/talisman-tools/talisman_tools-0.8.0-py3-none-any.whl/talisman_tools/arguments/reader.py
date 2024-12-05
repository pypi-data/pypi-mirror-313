from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Callable, Dict

from talisman_tools.plugin import ReaderPlugins
from tp_interfaces.readers.abstract import AbstractReader


def get_reader_factory(parser: ArgumentParser, arguments: Dict[str, str]) -> Callable[[Namespace], Dict[str, AbstractReader]]:
    readers = ReaderPlugins.flattened
    reader_choices = set(readers.keys())
    argument_group = parser.add_argument_group(title="Input documents arguments")
    argument_group.add_argument('reader', choices=reader_choices, help=f'Type of documents reader.')
    for arg, metavar in arguments.items():
        argument_group.add_argument(arg, type=Path, metavar=metavar)

    def get_reader(args: Namespace) -> Dict[str, AbstractReader]:
        reader = readers[args.reader]
        result = {}
        for arg in arguments:
            p = getattr(args, arg.lstrip('-'))
            if p is not None:
                result[arg] = reader(p)
        return result

    return get_reader
