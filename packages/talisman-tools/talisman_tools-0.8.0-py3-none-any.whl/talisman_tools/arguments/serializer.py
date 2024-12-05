from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Callable, Iterable

from tdm import TalismanDocument

from talisman_tools.plugin import SerializerPlugins


def get_serializer_factory(parser: ArgumentParser):
    serializers = SerializerPlugins.flattened
    argument_group = parser.add_argument_group(title="Output documents arguments")
    argument_group.add_argument('output', type=Path, metavar='<output path>')
    argument_group.add_argument('-serializer', type=str, metavar='<serializer type>', choices=set(serializers.keys()), default='default')

    def get_serializer(args: Namespace) -> Callable[[Iterable[TalismanDocument]], None]:
        from functools import partial
        return partial(serializers[args.serializer]().serialize, path=args.output)

    return get_serializer
