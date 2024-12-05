import logging
from argparse import Namespace

from fastapi import FastAPI

from talisman_tools.commands.servers.commands.loader.methods.load import register_load_docs
from talisman_tools.commands.servers.server_helper import async_register_context_manager, register_exception_handlers
from tp_interfaces.domain.manager import DomainManager
from tp_interfaces.loader.interfaces import Loader

logger = logging.getLogger(__name__)


def action(args: Namespace, loader: Loader) -> FastAPI:
    app = FastAPI(title='kb loader server', description='kb loader server')

    register_load_docs(
        app=app,
        loader=loader,
        logger=logger
    )

    register_exception_handlers(app)
    async_register_context_manager(app, DomainManager())
    async_register_context_manager(app, loader)

    return app
