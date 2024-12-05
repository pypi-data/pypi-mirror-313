import logging
from logging import Logger
from typing import Type

from fastapi import FastAPI, HTTPException, Request

from talisman_tools.commands.servers.server_helper import log_debug_data
from tp_interfaces.abstract import AbstractUpdatableModel, AbstractUpdate

_logger = logging.getLogger(__name__)


def register_update(app: FastAPI, model: AbstractUpdatableModel, input_type: Type[AbstractUpdate], logger: Logger = _logger):
    @app.post("/update/")
    async def update(request: Request, *, update_model: input_type):
        log_debug_data(logger, "update requested", request, update=update_model.json())
        try:
            model.update(update_model)
            log_debug_data(logger, "successfull update", request, update=update_model.json())
        except Exception as e:
            logger.error("error during update", exc_info=e, extra={"update": update_model.json()})
            raise HTTPException(status_code=400, detail=str(e))
