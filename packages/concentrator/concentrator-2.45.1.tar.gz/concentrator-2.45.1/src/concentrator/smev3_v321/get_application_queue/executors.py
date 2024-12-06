from __future__ import annotations

from typing import TYPE_CHECKING
import datetime

from aio_client.provider.api import PostProviderRequest
from aio_client.provider.api import push_request
from django.db.models import Prefetch
import pytz

from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationUnit
from kinder.core.queue_module.api import get_info_for_declaration
from kinder.core.queue_module.enum import COMMON_QUEUE_STATUSES
from kinder.settings import TIME_ZONE

from concentrator.smev3_v321.base.utils import get_oktmo_region
from concentrator.smev3_v321.base.utils import is_cancel_allowed
from concentrator.smev3_v321.base.utils import render_type2xml
from concentrator.smev3_v321.constants import SUCCESS_MESSAGE
from concentrator.smev3_v321.executors import AbstractExecutor
from concentrator.smev3_v321.model import ExecutionData
from concentrator.smev3_v321.service_types import kinder_conc
from concentrator.smev3_v321.utils import (
    get_declaration_by_client_or_portal_id)

from .constants import GetApplicationQueueMessage


if TYPE_CHECKING:
    from typing import Any

    from django.db.models import QuerySet

    from concentrator.smev3_v321.model import FormDataMessage


class GetApplicationQueueRequestExecutor(AbstractExecutor):
    """Исполнитель сервиса GetApplicationQueueRequest."""

    name_service: str = 'GetApplicationQueueRequest'
    service_type_name: str = (
        kinder_conc.GetApplicationQueueRequestType.__name__)

    @classmethod
    def prepare_query(cls) -> QuerySet:
        """Выполняет подготовку запроса."""

        subquery_declaration_unit_ids = (
            DeclarationUnit.objects.only('unit_id'))

        query = Declaration.objects.prefetch_related(
            Prefetch(
                'declarationunit_set',
                queryset=subquery_declaration_unit_ids,
                to_attr='declaration_unit_ids'))

        return query

    @classmethod
    def process(cls, message: FormDataMessage, **kwargs) -> ExecutionData:

        response_body = render_type2xml(
            cls.get_response(message), name_type='FormDataResponse')

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
    def get_response(cls, message: FormDataMessage) -> Any:
        """Формирует ответ на GetApplicationQueueRequest.

        :param message: Запрос

        :return: Тело ответа.
        :rtype: FormDataResponseType
        """

        order_id = message.parse_body.GetApplicationQueueRequest.orderId

        declaration, _ = get_declaration_by_client_or_portal_id(
            cls.prepare_query(), order_id)

        validation_error_response = cls.validate(declaration, order_id)
        if validation_error_response:
            return validation_error_response

        declaration_info = get_info_for_declaration(declaration, only_mo=True)
        if declaration_info:
            declaration_info = declaration_info[0]

        get_app_queue_type = (
            cls.parser_module.ApplicationQueueResponseType(
                orderId=order_id,
                Position=declaration_info['position'],
                Total=declaration_info['total'],
                WithoutQueue=declaration_info['out_of_order'],
                FirstQueue=declaration_info['first_order'],
                AdvantageQueue=declaration_info['preemptive_right'],
                RelevantDT=datetime.datetime.now(
                    pytz.timezone(TIME_ZONE)).replace(microsecond=0)
            )
        )

        response = cls.parser_module.FormDataResponseType(
            oktmo=get_oktmo_region(),
            GetApplicationQueueResponse=get_app_queue_type)

        return response

    @classmethod
    def validate(cls, declaration: Declaration, order_id: int) -> Any:
        """Валидирует заявление, если валидация не пройдена - возвращает ответ
         с ошибкой

        :param declaration: Заявление
        :param order_id: Идентификатор заявления

        :return: Тело ответа.
        :rtype: FormDataResponseType
         """

        kwargs = {}

        # Проверка существования заявления
        if not declaration:
            kwargs.update({
                'statusCode': cls.parser_module.statusCodeType(
                    GetApplicationQueueMessage.values[
                        GetApplicationQueueMessage.NOT_EXISTS]),
                'comment': GetApplicationQueueMessage.NOT_EXISTS})

        # Заявка должна быть со статусом, участвующим в очереди
        elif declaration.status.code not in COMMON_QUEUE_STATUSES:
            kwargs.update({
                'statusCode': cls.parser_module.statusCodeType(
                    GetApplicationQueueMessage.values[
                        GetApplicationQueueMessage.NOT_QUEUED]),
                'comment': GetApplicationQueueMessage.NOT_QUEUED,
                'cancelAllowed': is_cancel_allowed(declaration.status)
            })

        if kwargs:
            kwargs.update({
                'orderId': cls.parser_module.orderIdType(order_id),
            })

            return cls.parser_module.FormDataResponseType(
                changeOrderInfo=cls.parser_module.changeOrderInfoType(**kwargs))
