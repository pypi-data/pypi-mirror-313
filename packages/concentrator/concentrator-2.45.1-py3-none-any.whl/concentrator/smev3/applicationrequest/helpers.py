from aio_client.provider.api import PostProviderRequest
from aio_client.provider.api import push_request

from concentrator.smev3.base.constants import SUCCESS_MESSAGE
from concentrator.smev3.base.utils import BaseExecutor
from concentrator.smev3.base.utils import SMEV3Response
from concentrator.smev3.base.utils import get_oktmo_region
from concentrator.smev3.base.utils import render_type2xml
from concentrator.smev3.service_types import kinder_conc

from .constants import Response
from .steps import CheckOrderStep


class ApplicationRequestExecutor(BaseExecutor):
    """Исполнитель сервиса ApplicationRequest."""

    name_service = 'ApplicationRequest'
    type_service = kinder_conc.ApplicationType

    @classmethod
    def process(cls, message, request_body):

        attachments = message['attachments']

        response_body = render_type2xml(
            cls.get_response(request_body.ApplicationRequest, attachments),
            name_type='FormDataResponse')

        response = push_request(PostProviderRequest(
            origin_message_id=message['origin_message_id'],
            body=response_body,
            message_type=message['message_type'],
            attachments=None,
            content_failure_code=None,
            replay_to=message['replay_to'],
            is_test_message=message['is_test_message']
        ))

        return SMEV3Response(
            response,
            {
                'method_name': cls.name_service,
                'response': response_body,
                'result': SUCCESS_MESSAGE
            })

    @classmethod
    def get_response(cls, request_declaration, attachments):
        """Запуск шагов проверки заявления и возвращение ответа."""

        next_step = CheckOrderStep(
            request_declaration, attachments=attachments)
        result = None

        while result is None:
            next_step = next(next_step)
            if isinstance(next_step, Response):
                result = next_step

        response = kinder_conc.FormDataResponseType(
            oktmo=get_oktmo_region(),
            changeOrderInfo=kinder_conc.changeOrderInfoType(
                orderId=kinder_conc.orderIdType(result.order_id),
                statusCode=kinder_conc.statusCodeType(result.status_code),
                comment=result.comment))

        return response
