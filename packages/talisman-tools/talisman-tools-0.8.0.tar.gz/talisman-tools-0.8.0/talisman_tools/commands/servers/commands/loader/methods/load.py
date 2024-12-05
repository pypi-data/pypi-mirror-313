import logging
from logging import Logger

from fastapi import FastAPI, HTTPException, Request
from tdm import TalismanDocumentModel

from tp_interfaces.domain.manager import DomainManager
from tp_interfaces.loader.interfaces import Loader
from tp_interfaces.logging.context import update_log_extras

_logger = logging.getLogger(__name__)


def register_load_docs(
        app: FastAPI,
        loader: Loader,
        logger: Logger = _logger
):
    cfg_type = loader.config_type

    @app.post('/', response_model=str)
    async def load_docs(request: Request, *, message: TalismanDocumentModel, config: cfg_type):
        with update_log_extras(doc_id=message.id):
            async with DomainManager() as manager:
                await manager.domain
            doc = message.deserialize()
            try:
                status = await loader.load_doc_and_bind_facts(doc, config)
            except Exception as e:
                logger.error("Non handled exception while request processing", exc_info=e)
                raise HTTPException(status_code=500)

            if status is None:
                raise HTTPException(status_code=500, detail='No document was loaded')
            return status
