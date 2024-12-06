import os
import zipfile
from base64 import b64encode
from io import StringIO
from urllib.parse import urljoin
from uuid import uuid4

from m3.actions import ApplicationLogicException
from kinder.webservice.smev3.utils.request_builder import BaseRequestBuilder

from concentrator.smev3_v321.models import UpdateClassifierRequest
from concentrator.smev3_v321.service_types import (
    classifier_data as data_schema)
from concentrator.smev3_v321.service_types import (
    update_classifier as update_schema)

from .settings import PLUGIN_DIR
from .settings import PLUGIN_URL
from .settings import UPDATE_CLASSIFIER_MEDIA_HOST
from .settings import UPDATE_CLASSIFIER_REQUEST_AUTH


class _AttachmentBuilder:
    """
    Построитель файла с изменениями
    """
    def __init__(self, request):
        self.request = request
    
    @property
    def data(self):
        """
        Данные для формирования xml
        """
        records = []
        classifier = self.request.classifier.get_classifier_class_by_name()
        for rec in self.request.data:
            attributes = []
            fields_info = classifier.get_fields_info()
            for name, value in rec.items():
                field_info = fields_info.get(name)
                params = {
                    'attribute_name': name,
                    field_info.type: value
                }
                attributes.append(
                    data_schema.attribute_value(**params)
                )
            records.append(
                data_schema.record(attribute_value=attributes)
            )

        if (self.request.request_type == 
                UpdateClassifierRequest.UPDATE_CLASSIFIERS):
            return data_schema.ClassifierDataUpdateRequest(record=records)
        elif (self.request.request_type == 
                UpdateClassifierRequest.DELETE_CLASSIFIERS):
            return data_schema.ClassifierDataDeleteRequest(record=records)
        else:
            raise ApplicationLogicException('Тип запроса не определён')

    def build(self):
        """
        Построение xml
        """
        mystdout = StringIO()
        self.data.export(
            mystdout, 0, pretty_print=False, namespaceprefix_='tns:')
        return mystdout.getvalue()
    
    def zip(self):
        """
        Формирование zip-архива
        """
        file_name = uuid4()
        zip_path = os.path.join(PLUGIN_DIR, f'{file_name}.zip')
        zip_url = f'{PLUGIN_URL}/{file_name}.zip'

        if UPDATE_CLASSIFIER_MEDIA_HOST:
            zip_url = urljoin(UPDATE_CLASSIFIER_MEDIA_HOST, zip_url)

        xml_str = self.build()

        with zipfile.ZipFile(zip_path, mode='w') as zf:
            zf.writestr(f'{file_name}.xml', xml_str)

        return zip_url


class UpdateClassifierRequestBuilder(BaseRequestBuilder):
    """
    Построитель запроса к ЕСНСИ
    """
    def build(self):
        response = update_schema.CnsiRequest(**self.get_content())
        mystdout = StringIO()
        response.export(
            mystdout, 0, name_='CnsiRequest', pretty_print=False, 
            namespaceprefix_='tns:')
        return mystdout.getvalue()

    def get_authorization_string(self):
        """
        Получение данных для авторизации
        """
        auth_str = b64encode(
            UPDATE_CLASSIFIER_REQUEST_AUTH.encode('utf-8'))
        return f"Basic {auth_str.decode('utf-8')}"

    def get_update_data(self):
        """
        Получение данных для обновления данных справочника
        """
        return update_schema.UpdateClassifierDataRequestType(
            authorizationString=self.get_authorization_string(),
            code=self.request.classifier.code,
            removeMissing=False
        )
    
    def get_delete_data(self):
        """
        Получение данных для удаления данных справочника
        """
        return update_schema.DeleteClassifierDataRequestType(
            authorizationString=self.get_authorization_string(),
            code=self.request.classifier.code
        )

    def get_content(self):
        """
        Получение данных запроса
        """
        if self.request.request_type == (
                UpdateClassifierRequest.UPDATE_CLASSIFIERS):
            return {
                'UpdateClassifierData': self.get_update_data()
            }
        
        if self.request.request_type == (
                UpdateClassifierRequest.DELETE_CLASSIFIERS):
            return {
                'DeleteClassifierData': self.get_delete_data()
            }

        raise ApplicationLogicException('Тип запроса не определён')

    @property
    def attachments(self):
        builder = _AttachmentBuilder(self.request)
        attachment_url = builder.zip()
        return [[attachment_url, ""]]


class RemoveMissingRequestBuilder(UpdateClassifierRequestBuilder):
    """
    Проставляет removeMissing=True
    """
    def get_update_data(self):
        return update_schema.UpdateClassifierDataRequestType(
            authorizationString=self.get_authorization_string(),
            code=self.request.classifier.code,
            removeMissing=True
        )
