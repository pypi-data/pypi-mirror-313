import logging
import os
from argparse import ArgumentParser, Namespace

from tp_interfaces.logging.context import get_log_extras

SERVICE_NAME = os.getenv('SERVICE_NAME', default='')


class TalismanFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self._service = SERVICE_NAME

    def filter(self, record) -> bool:
        if self._service:
            record.service = self._service
        for key, value in get_log_extras().items():
            setattr(record, key, value)
        return True


def uvicorn_server_factory(parser: ArgumentParser):
    from fastapi import FastAPI
    argument_group = parser.add_argument_group(title='Uvicorn server arguments')
    argument_group.add_argument('-remote', action='store_true', help='should listen for remote connections')
    argument_group.add_argument('-port', type=int, help='port to listen on', default=8000)
    argument_group.add_argument('-logging_conf', help='path to json file with logging config',
                                default='talisman-tools/default_logging_conf.json')

    def launcher(app: FastAPI, args: Namespace) -> None:
        import logging.config
        import logging.handlers
        import uvicorn
        from talisman_tools.configure.configure import read_config

        logging.config.dictConfig(read_config(args.logging_conf))

        f = TalismanFilter()
        for handler in logging.root.handlers:
            handler.addFilter(f)

        host = "0.0.0.0" if args.remote else "127.0.0.1"
        uvicorn.run(app, host=host, port=args.port, log_config=None)

    return launcher
