from argparse import ArgumentParser, Namespace

from talisman_tools.plugin import DomainPlugins
from tp_interfaces.domain.manager import DomainManager
from tp_interfaces.helpers.io import read_json


def get_domain_factory(parser: ArgumentParser):
    parser.add_argument('-domain_config_path', metavar='<domain config path>')

    def set_domain(args: Namespace) -> None:
        if args.domain_config_path is None:
            return

        config = read_json(args.domain_config_path)
        domain_producer = DomainPlugins.plugins[config.get("plugin")]().from_config(config.get('config', {}))
        DomainManager().set_producer(domain_producer)

    return set_domain
