from argparse import ArgumentParser, Namespace
from typing import Callable

from talisman_tools.arguments.domain import get_domain_factory
from tp_interfaces.abstract.processor.trainer import DEFAULT_CACHE_DIR


def configure_train_parser(parser: ArgumentParser) -> None:
    domain_factory = get_domain_factory(parser)

    parser.add_argument('config_path', type=str, metavar='<config.json>', help='Path to training configuration file')
    parser.add_argument('trained_model_path', type=str, metavar='<trained model path>', help='Path to save trained model to')
    parser.add_argument('-cache_dir', type=str, default=DEFAULT_CACHE_DIR, help='Path to directory with cache files')
    parser.add_argument('--ignore_cache', action='store_true', help='Do not use cache')

    def get_action() -> Callable[[Namespace], None]:
        def action(args: Namespace) -> None:
            from .action import train
            domain_factory(args)
            train(args)

        return action

    parser.set_defaults(action=get_action)
