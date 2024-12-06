from __future__ import annotations

from typing import TYPE_CHECKING

from aio_client.provider.api import PostProviderRequest
from aio_client.provider.api import push_request

from concentrator.smev3_v321.base.utils import render_type2xml
from concentrator.smev3_v321.constants import SUCCESS_MESSAGE
from concentrator.smev3_v321.executors import AbstractExecutor
from concentrator.smev3_v321.model import ExecutionData
from concentrator.smev3_v321.service_types import kinder_conc

from .application import ApplicationManager


if TYPE_CHECKING:
    from typing import Any

    from concentrator.smev3_v321.model import FormDataMessage


class ApplicationRequestExecutor(AbstractExecutor):
    """Исполнитель сервиса ApplicationRequest."""

    name_service = 'ApplicationRequest'
    service_type_name = kinder_conc.ApplicationType.__name__

    @classmethod
    def process(cls, message: FormDataMessage, **kwargs):

        response_body = render_type2xml(
            cls.get_response(message, **kwargs), name_type='FormDataResponse')

        response = push_request(PostProviderRequest(
            origin_message_id=message.origin_message_id,
            body=response_body,
            message_type=message.message_type,
            replay_to=message.replay_to,
            is_test_message=message.is_test_message))

        return ExecutionData(
            response,
            {
                'method_name': cls.name_service,
                'response': response_body,
                'result': SUCCESS_MESSAGE
            })

    @classmethod
    def get_response(cls, message: FormDataMessage, **kwargs) -> Any:
        """Формирует и возвращает ответ.

        :param message: Сообщение СМЭВ (AIO).

        :return: Ответ
        :rtype: FormDataResponseType

        """

        # Если параметр установлен, то при валидации Желаемой даты зачисления,
        # она будет сравниваться с датой из тэга FilingDate
        compare_date_with_filing = kwargs.get('compare_with_filing', False)

        data = ApplicationManager(message, compare_date_with_filing).run()

        response = cls.parser_module.FormDataResponseType(
            changeOrderInfo=cls.parser_module.changeOrderInfoType(
                orderId=cls.parser_module.orderIdType(data.order_id),
                statusCode=cls.parser_module.statusCodeType(data.org_code),
                comment=data.comment))

        return response
