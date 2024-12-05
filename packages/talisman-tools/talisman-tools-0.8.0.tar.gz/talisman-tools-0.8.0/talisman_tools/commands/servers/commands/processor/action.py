import logging
from argparse import Namespace
from typing import Callable

from fastapi import FastAPI

from talisman_tools.commands.servers.commands.processor.methods.process import register_process_docs
from talisman_tools.commands.servers.commands.processor.methods.schema import register_schema
from talisman_tools.commands.servers.commands.processor.methods.update import register_update
from talisman_tools.commands.servers.server_helper import async_register_context_manager, register_exception_handlers
from talisman_tools.plugin import EndpointPlugins
from tp_interfaces.abstract import AbstractDocumentProcessor, AbstractUpdatableModel
from tp_interfaces.domain.manager import DomainManager

logger = logging.getLogger(__name__)


def register_process(app: FastAPI, processor):
    async_register_context_manager(app, processor)

    @app.on_event("startup")
    def process_register():
        register_process_docs(
            app=app,
            endpoint='/',
            processor=processor,
            logger=logger
        )

    @app.on_event("startup")
    def schema_register():
        register_schema(
            app=app,
            endpoint='/schema',
            processor=processor,
            logger=logger
        )


def action(args: Namespace, processor_factory: Callable[[Namespace], AbstractDocumentProcessor]) -> FastAPI:
    processor = processor_factory(args)
    logger.info(f"Loaded {processor}")

    app = FastAPI(title="talisman-ie REST server", description=f"talisman-ie REST server for {processor}")

    if isinstance(processor, AbstractUpdatableModel):
        register_update(app, processor, processor.update_type)

    for endpoint, register in EndpointPlugins.flattened.items():
        register()(app=app, endpoint=endpoint, processor=processor, logger=logger)

    register_exception_handlers(app, logger=logger)
    if DomainManager():
        async_register_context_manager(app, DomainManager())
    register_process(app, processor)

    return app
