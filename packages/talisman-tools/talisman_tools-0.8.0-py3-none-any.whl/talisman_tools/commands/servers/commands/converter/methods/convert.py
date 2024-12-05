import logging
from logging import Logger
from typing import Optional

from fastapi import FastAPI, Request
from tdm import TalismanDocumentModel
from tdm.datamodel.domain import DocumentType, PropertyType
from tdm.v0 import TalismanDocumentModel as LegacyTalismanDocumentModel

from tp_interfaces.abstract import ImmutableBaseModel
from tp_interfaces.domain.manager import DomainManager
from tp_interfaces.helpers.batch import AbstractModelInput

_logger = logging.getLogger(__name__)

_metadata_map = {
    'title': 'Заголовок',
    'file_name': 'Название файла',
    'file_type': 'Формат файла',
    'size': 'Размер файла',
    'created_time': 'Дата создания',
    'access_time': 'Дата последнего просмотра',
    'modifired_time': 'Дата изменения',
    'publication_date': 'Дата публикации',
    'publication_author': 'Автор публикации',
    'description': 'Примечание',
    'url': 'Источник',
    'access_level': 'Уровень доступа',
    'user': 'Автор документа',
    'path': 'Путь до файла',
    'trust_level': 'Уровень доверия',
    'markers': 'Метки',
    'preview_text': 'Предпросмотр текста',
    'platform': 'Платформа',
    'account': 'Аккаунт',
    'story': 'Сюжет',
    'language': 'Язык документа',
    'job_id': 'Запуск сбора',
    'periodic_job_id': 'Периодический запуск сбора',
    'task_id': 'Задача импорта',
    'periodic_task_id': 'Периодическая задача импорта',
    'parent_uuid': 'Родительский документ'
}


def register_convert_doc(
        app: FastAPI,
        logger: Logger = _logger
):
    class ModelInput(AbstractModelInput):
        message: LegacyTalismanDocumentModel
        config: ImmutableBaseModel

        def get_message(self) -> LegacyTalismanDocumentModel:
            return self.message

        def get_config(self) -> Optional[ImmutableBaseModel]:
            return self.config

    @app.post('/', response_model=TalismanDocumentModel, response_model_exclude_none=True)
    async def convert(request: Request, *, message: ModelInput):
        async with DomainManager() as manager:
            domain = await manager.domain

        titles = tuple(domain.get_types(PropertyType, filter_=lambda p: p.name == 'Название'))
        doc_type = domain.types[DocumentType].pop().id

        message.message.set_domain(domain)
        document = message.message.to_doc(doc_type, titles, _metadata_map)
        logger.debug(f"document {document.id} successfully converted")
        result = TalismanDocumentModel.serialize(document)
        return result
