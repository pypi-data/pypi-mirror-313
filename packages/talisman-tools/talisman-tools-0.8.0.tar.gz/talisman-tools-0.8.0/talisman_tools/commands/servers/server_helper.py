import logging.config
from contextlib import AbstractContextManager
from typing import AsyncContextManager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

_logger = logging.getLogger(__name__)


def register_context_manager(app: FastAPI, context_manager: AbstractContextManager):
    @app.on_event("startup")
    async def enter_manager():
        context_manager.__enter__()

    @app.on_event("shutdown")
    async def exit_manager():
        context_manager.__exit__(None, None, None)


def async_register_context_manager(app: FastAPI, context_manager: AsyncContextManager):
    @app.on_event("startup")
    async def enter_manager():
        await context_manager.__aenter__()

    @app.on_event("shutdown")
    async def exit_manager():
        await context_manager.__aexit__(None, None, None)


def register_exception_handlers(app: FastAPI, logger: logging.Logger = _logger):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc: RequestValidationError):
        error_content = jsonable_encoder({"detail": exc.args})
        logger.error("Pydantic validation error", extra=error_content)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_content,
        )


def log_debug_data(logger: logging.Logger, msg: str, request: Request = None, **kwargs) -> None:
    extras = {}
    if request is not None:
        extras['client'] = request.client
    extras.update({key: jsonable_encoder(value) for key, value in kwargs.items()})
    logger.debug(msg, extra=extras)
