import datetime
import os
import traceback
import uuid

from aio_client.consumer.api import push_request
from aio_client.consumer.models import PostConsumerRequest

from kinder import logger
from kinder.core.dict.models import PrivilegeOrderType

from concentrator.smev3_v321 import settings
from concentrator.smev3_v321.base.utils import render_type2xml
from concentrator.smev3_v321.models import AttachmentRequest
from concentrator.smev3_v321.service_types import lists_children_received_place

from .providers import AttachmentRequestReportProvider
from .report import Reporter


class AttachmentRequestHelper:
    """
    Хэлпер для выполнения запросов AttachmentRequest
    """
    file_name_template = 'Список_%d-%m-%Y'
    service_name = 'AttachmentRequest'

    PRIVILEGE_PRIORITY_MAP = {
        str(PrivilegeOrderType.FIRST_ORDER): 'Внеочередное право',
        str(PrivilegeOrderType.OUT_OF_ORDER): 'Первоочередное право',
        str(PrivilegeOrderType.PREEMPTIVE_RIGHT): 'Преимущественное право',
    }

    def __init__(self, unit_id):
        self.unit_id = unit_id

    def get_request(self):
        """
        Формирование запроса
        """
        attachment_url = self.create_attachment()
        attachments = [[attachment_url, '']]

        request = lists_children_received_place.AttachmentRequestType(
            env='EPGU',
            EduOrganizationCode=str(self.unit_id)
        )

        request = render_type2xml(
            request,
            name_type='AttachmentRequest'
        )

        return request, attachments
    
    def send_request(self, request, attachments):
        """
        Отправка запроса
        """
        request_obj = AttachmentRequest.objects.create()
        request_obj.generate_message_id()

        return push_request(PostConsumerRequest(
            message_id=str(request_obj.message_id),
            body=request,
            message_type=settings.ATTACHMENT_REQUEST_MESSAGE_TYPE,
            attachments=attachments,
        ))
    
    def make_request(self):
        """
        Сформировать и отправить запрос
        """
        return self.send_request(*self.get_request())
    
    def _get_provider(self):
        """
        Провайдер с данными отчёта
        """
        return AttachmentRequestReportProvider()
    
    def _get_reporter(self, file_path):
        """
        Построитель отчёта
        """
        return Reporter(file_path)
    
    def _get_data(self):
        """
        Обработка данных провайдера отчёта
        """
        provider = self._get_provider()
        provider.init(self.unit_id)

        for row in provider.pupils_data():
            yield (
                row.get('declaration__client_id'),
                row.get('declaration__date') and row.get(
                    'declaration__date').strftime('%d.%m.%Y %H:%M:%S'),
                self.PRIVILEGE_PRIORITY_MAP.get(
                    row.get('privilege_best_priority')),
                row.get('grup__age_cat__name'),
                row.get('grup__type__name'),
                row.get('grup__work_type__name'),
                '; '.join(filter(
                    None, (row.get('grup__program__syllabus__name'), 
                           row.get('grup__spec__name')))),
            )

    def create_attachment(self):
        """
        Создание отчёта, возвращает url отчёта для отправки в attachments  
        """
        dir_name = uuid.uuid4().hex
        dir_path = os.path.join(settings.PLUGIN_DIR, self.service_name, dir_name)
        file_name = datetime.datetime.now().strftime(f'{self.file_name_template}')
        file_path = os.path.join(dir_path, file_name)
        url = f'{settings.PLUGIN_URL}/{self.service_name}/{dir_name}/{file_name}.pdf'

        if settings.ATTACHMENT_REQUEST_MEDIA_HOST:
            url = f'{settings.ATTACHMENT_REQUEST_MEDIA_HOST}{url}'

        os.makedirs(dir_path)
        reporter = self._get_reporter(file_path)
        reporter.report(self._get_data())

        return url
