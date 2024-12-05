import logging
from argparse import Namespace

from fastapi import FastAPI

from talisman_tools.commands.servers.commands.converter.methods.convert import register_convert_doc
from talisman_tools.commands.servers.server_helper import async_register_context_manager, register_exception_handlers
from tp_interfaces.domain.manager import DomainManager

logger = logging.getLogger(__name__)


def action(args: Namespace) -> FastAPI:
    app = FastAPI(title='document converter service')

    register_convert_doc(
        app=app,
        logger=logger
    )

    register_exception_handlers(app, logger)
    async_register_context_manager(app, DomainManager())
    return app
