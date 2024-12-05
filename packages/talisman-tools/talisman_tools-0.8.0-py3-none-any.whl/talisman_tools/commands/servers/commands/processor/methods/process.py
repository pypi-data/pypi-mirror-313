import logging
from functools import partial
from logging import Logger
from operator import itemgetter
from typing import Any, List, Optional, Sequence, Tuple, Union

from fastapi import FastAPI, HTTPException, Request
from tdm import TalismanDocumentModel

from talisman_tools.commands.servers.server_helper import log_debug_data
from tp_interfaces.abstract import AbstractDocumentProcessor, ImmutableBaseModel
from tp_interfaces.abstract.exception import WrongRequest
from tp_interfaces.helpers.batch import AbstractModelInput, async_batch_process_inputs
from tp_interfaces.logging.context import update_log_extras
from tp_interfaces.logging.time import TimeMeasurer

_logger = logging.getLogger(__name__)


def register_process_docs(
        app: FastAPI,
        endpoint: str,
        processor: AbstractDocumentProcessor,
        logger: Logger = _logger
):
    config_model = processor.config_type

    class ModelInput(AbstractModelInput):
        message: TalismanDocumentModel
        config: config_model

        def get_message(self) -> Any:
            return self.message

        def get_config(self) -> Optional[ImmutableBaseModel]:
            return self.config

    async def process_with_config(messages: Sequence[TalismanDocumentModel], config: ImmutableBaseModel) \
            -> Tuple[TalismanDocumentModel, ...]:
        docs = tuple(message.deserialize() for message in messages)
        with update_log_extras(doc_id=[doc.id for doc in docs]):
            output_docs = await processor.process_docs(docs, config)
            return tuple(TalismanDocumentModel.serialize(output_doc) for output_doc in output_docs)

    @app.post(endpoint, response_model=Union[List[TalismanDocumentModel], TalismanDocumentModel], response_model_exclude_none=True)
    async def process(request: Request, *, messages: Union[List[ModelInput], ModelInput]):
        response_post_processor = lambda x: x
        if not isinstance(messages, list):
            messages = [messages]
            response_post_processor = itemgetter(0)

        with update_log_extras(message_id=[message.message.id for message in messages]):
            log_debug_data(logger, f"got {len(messages)} documents for processing", request)
            task = partial(async_batch_process_inputs, inputs=messages, processor=process_with_config)
            try:
                response = await task()
            except WrongRequest as e:
                logger.error("WrongRequest exception while processing request", exc_info=e)
                raise HTTPException(status_code=422, detail=str(e) if len(str(e)) else "Internal error: " + e.__repr__())
            except Exception as e:
                logger.error("Exception while processing request", exc_info=e)
                raise HTTPException(status_code=500)
            log_debug_data(logger, f"processed {len(response)} documents", request)

            with TimeMeasurer("reponse post processing", inline_time=True, logger=_logger):
                return response_post_processor(response)
