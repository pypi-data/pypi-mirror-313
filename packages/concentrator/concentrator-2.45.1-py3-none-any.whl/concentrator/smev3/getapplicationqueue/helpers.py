from django.db.models import Prefetch

from aio_client.base import const as aio_base_const
from aio_client.provider.api import PostProviderRequest
from aio_client.provider.api import push_request
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationUnit
from kinder.webservice.api.declaration import get_declaration_by_client_id
from kinder.webservice.api.exceptions import ApiException

from concentrator.smev3.base.constants import SUCCESS_MESSAGE
from concentrator.smev3.base.exceptions import ContentFailure
from concentrator.smev3.base.utils import BaseExecutor
from concentrator.smev3.base.utils import SMEV3Response
from concentrator.smev3.base.utils import get_oktmo_region
from concentrator.smev3.base.utils import get_queue_info_short
from concentrator.smev3.base.utils import get_spec_decl
from concentrator.smev3.base.utils import render_type2xml
from concentrator.smev3.service_types import kinder_conc


class GetApplicationQueueRequestExecutor(BaseExecutor):
    """Исполнитель сервиса GetApplicationQueueRequest."""

    name_service = 'GetApplicationQueueRequest'
    type_service = kinder_conc.GetApplicationQueueRequestType

    @classmethod
    def prepare_query(cls):
        """Выполняет подготовку запроса."""

        subquery_declaration_unit_ids = (
            DeclarationUnit.objects.only('unit_id'))

        query = Declaration.objects.prefetch_related(
            Prefetch('declarationunit_set',
                     queryset=subquery_declaration_unit_ids,
                     to_attr='declaration_unit_ids'))

        return query

    @classmethod
    def process(cls, message, request_body):

        try:
            declaration = get_declaration_by_client_id(
                cls.prepare_query(),
                request_body.GetApplicationQueueRequest.orderId)
        except ApiException:
            declaration = None

        try:
            response_body = render_type2xml(
                cls.get_response(declaration), name_type='FormDataResponse')
            content_failure_code = None
            content_failure_comment = None
        except ContentFailure as exc:
            response_body = 'null'
            content_failure_code = exc.content_failure_code
            content_failure_comment = exc.content_failure_comment

        response = push_request(PostProviderRequest(
            origin_message_id=message['origin_message_id'],
            body=response_body,
            message_type=message['message_type'],
            attachments=None,
            content_failure_code=content_failure_code,
            content_failure_comment=content_failure_comment or '',
            replay_to=message['replay_to'],
            is_test_message=message['is_test_message']
        ))

        return SMEV3Response(
            response,
            {
                'method_name': cls.name_service,
                'response': response_body,
                'result': content_failure_comment or SUCCESS_MESSAGE
            })

    @classmethod
    def get_response(cls, declaration):
        """Формирует ответ на GetApplicationQueueRequest.

        :param declaration: Заявление
        :type declaration: Declaration
        :return: ответ
        :rtype: FormDataResponseType
        :raise: ContentFailure
        """

        if not declaration:
            raise ContentFailure(
                aio_base_const.FAILURE,
                'Заявление по указанным параметрам не найдено')

        get_app_queue_type = kinder_conc.GetApplicationQueueResponseType(
            orderId=int(declaration.client_id),
            EntryDate=declaration.desired_date,
            AdaptationGroup=str(get_spec_decl(declaration)),
            ScheduleType=str(declaration.work_type_id or ''))

        all_declaration_unit_ids = declaration.declaration_unit_ids or ()
        for declaration_unit in all_declaration_unit_ids:
            number, all_queue = (
                get_queue_info_short(declaration, declaration_unit.unit_id))
            edu_org_queue_type = kinder_conc.EduOrganizationQueueType(
                Code=str(declaration_unit.unit_id),
                NumberInQueue=number,
                AllInQueue=all_queue,
            )
            get_app_queue_type.add_EduOrganizationQueue(edu_org_queue_type)

        response = kinder_conc.FormDataResponseType(
            oktmo=get_oktmo_region(),
            GetApplicationQueueResponse=get_app_queue_type)

        return response
