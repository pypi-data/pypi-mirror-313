from argparse import ArgumentParser

from talisman_tools.helper.multiprocessing import setup_multiprocessing
from talisman_tools.parser_helper import configure_subparsers
from talisman_tools.talisman_logging import get_logging_factory


def main():
    parser = ArgumentParser(description='Talisman tools')
    logging_factory = get_logging_factory(parser)

    from talisman_tools.commands import SUBPARSERS
    configure_subparsers(parser, SUBPARSERS)

    args = parser.parse_args()
    logging_factory(args)  # initialize logging before performing any actions

    if not hasattr(args, 'action'):
        parser.print_help()
        exit(1)

    action = args.action()
    action(args)  # pass control to relevant subparser


if __name__ == "__main__":
    setup_multiprocessing()
    main()
