from aio_client.base import const as aio_base_const
from aio_client.provider.api import PostProviderRequest
from aio_client.provider.api import push_request
from m3 import ApplicationLogicException

from concentrator.smev3.base.utils import is_cancel_allowed
from concentrator.smev3.cancel_request_service.constants import (
    CANCEL_SUCCESS_COMMENT)
from concentrator.smev3.cancel_request_service.constants import (
    CHANGE_STATUS_TO)
from kinder.core.declaration.models import Declaration
from kinder.core.declaration_status.enum import DSS
from kinder.core.declaration_status.models import DeclarationStatus
from kinder.webservice.api.declaration import get_declaration_by_client_id
from kinder.webservice.api.exceptions import ApiException

from concentrator.smev3.base.constants import SUCCESS_MESSAGE
from concentrator.smev3.base.exceptions import ContentFailure
from concentrator.smev3.base.utils import BaseExecutor
from concentrator.smev3.base.utils import SMEV3Response
from concentrator.smev3.base.utils import render_type2xml
from concentrator.smev3.base.utils import get_oktmo_region
from concentrator.smev3.base.utils import get_order_id
from concentrator.smev3.service_types import kinder_conc

from .constants import WHY_CHANGE


class CancelRequestExecutor(BaseExecutor):
    """Исполнитель сервиса cancelRequest."""

    name_service = 'cancelRequest'
    type_service = kinder_conc.cancelRequestType

    @classmethod
    def process(cls, message, request_body):
        """
        Обработка запроса

        :param message: Параметры запроса
        :type message: dict
        :param request_body: Объект FormDataType
        :type request_body: concentrator.smev3.service_types.kinder_conc
        .FormDataType
        :return: Ответ
        :rtype: SMEV3Response
        """

        try:
            declaration = get_declaration_by_client_id(
                Declaration.objects.select_related('status'),
                request_body.cancelRequest.orderId)
        except ApiException:
            declaration = None

        content_failure_code = None
        content_failure_comment = None

        try:
            response_body = render_type2xml(
                cls.get_response(declaration),
                name_type='FormDataResponse')
        except ContentFailure as exc:
            response_body = 'null'
            content_failure_code = exc.content_failure_code
            content_failure_comment = exc.content_failure_comment
        except ApplicationLogicException as exc:
            response_body = 'null'
            content_failure_code = aio_base_const.FAILURE
            content_failure_comment = str(exc)

        response = push_request(PostProviderRequest(
            origin_message_id=message['origin_message_id'],
            body=response_body,
            message_type=message['message_type'],
            attachments=None,
            content_failure_code=content_failure_code,
            content_failure_comment=(content_failure_comment or ''),
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
        """Формирует ответ на cancelRequest.

        :param declaration: Заявление
        :type declaration: Declaration
        :return: Ответ на запрос cancelRequest
        :rtype: FormDataResponseType
        :raise: ContentFailure
        """

        if not declaration:
            raise ContentFailure(
                aio_base_const.FAILURE,
                'Заявление по указанным параметрам не найдено')
        elif declaration.status.code in DSS.no_active_statuses():
            raise ContentFailure(aio_base_const.FAILURE,
                                 'Заявление в неактивном статусе')
        elif not is_cancel_allowed(declaration.status):
            raise ContentFailure(
                aio_base_const.FAILURE,
                'В статусе, в котором находится заявление, '
                'отмена не разрешена')

        try:
            declaration.change_status(DeclarationStatus.objects.get(
                code=CHANGE_STATUS_TO), why_change=WHY_CHANGE)
        except DeclarationStatus.DoesNotExist:
            raise ContentFailure(
                aio_base_const.FAILURE, f'''Статуса 
                {DSS.values.get(CHANGE_STATUS_TO)} не существует''')

        response = kinder_conc.FormDataResponseType(
            oktmo=get_oktmo_region(),
            cancelResponse=kinder_conc.cancelResponseType(
                orderId=get_order_id(declaration),
                result=kinder_conc.CancelResponseResultType.CANCELLED,
                comment=CANCEL_SUCCESS_COMMENT))

        return response
