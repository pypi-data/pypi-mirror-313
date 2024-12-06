from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from aio_client.provider.api import PostProviderRequest
from aio_client.provider.api import push_request
from django.db.models import Exists
from django.db.models import OuterRef

from kinder.core.declaration.models import Declaration
from kinder.core.declaration_status.enum import DSS
from kinder.core.queue_module.helpers import get_position_info
from kinder.core.queue_module.models import DeclarationPositionLog

from concentrator.smev3_v321.base.utils import render_type2xml
from concentrator.smev3_v321.constants import SUCCESS_MESSAGE
from concentrator.smev3_v321.executors import AbstractExecutor
from concentrator.smev3_v321.model import ExecutionData
from concentrator.smev3_v321.service_types import kinder_conc
from concentrator.smev3_v321.utils import (
    get_declaration_by_client_or_portal_id)

from .constants import GetApplicationQueueReasonRequest


if TYPE_CHECKING:
    from django.db.models import QuerySet

    from concentrator.smev3_v321.model import FormDataMessage


class GetApplicationQueueReasonRequestExecutor(AbstractExecutor):
    """Исполнитель сервиса GetApplicationQueueReasonRequest."""

    name_service: str = 'GetApplicationQueueReasonRequest'
    service_type_name: str = (
        kinder_conc.GetApplicationQueueReasonRequestType.__name__)

    @classmethod
    def prepare_query(cls, request: Any) -> QuerySet:
        """Выполняет подготовку запроса

        :param request: Запрос
        :type: GetApplicationQueueReasonRequestType

        :return: Запрос, аннотированный наличием лога смены позиции заявления в очереди
        """

        # Дата с и Дата по, полученные из запроса.
        date_range = (request.PeriodStart, request.PeriodEnd)

        # Подзапрос на выборку существования лога изменения позиции
        # заявления в очереди по организации МО за полученный период.
        subquery_position_log = Exists(
            DeclarationPositionLog.objects.filter(
                created__date__range=date_range,
                declaration=OuterRef('id'), unit=OuterRef('mo')))

        query = (
            Declaration.objects.select_related('status').annotate(
                position_log_exists=subquery_position_log))

        return query

    @classmethod
    def validate(cls, declaration: Declaration | None) -> dict[str, Any]:
        """Выполняет валидацию данных заявления.

        :param declaration: Заявление

        :return: Словарь с данным для ответа (changeOrderInfo)

         """

        # Проверка существования заявления.
        if not declaration:
            return {
                'statusCode': cls.parser_module.statusCodeType(
                    GetApplicationQueueReasonRequest.values.get(
                        GetApplicationQueueReasonRequest.NOT_EXISTS)),
                'comment': GetApplicationQueueReasonRequest.NOT_EXISTS
            }

        # Заявка должна быть со статусом, участвующим в очереди.
        if declaration.status.code not in DSS.status_queue_full():
            return {
                'statusCode': cls.parser_module.statusCodeType(
                    GetApplicationQueueReasonRequest.values.get(
                        GetApplicationQueueReasonRequest.NOT_QUEUED)),
                'comment': GetApplicationQueueReasonRequest.NOT_QUEUED
            }

        # Проверка изменения позиции заявления в очереди.
        if not declaration.position_log_exists:
            return {
                'statusCode': cls.parser_module.statusCodeType(
                    GetApplicationQueueReasonRequest.values.get(
                        GetApplicationQueueReasonRequest.NO_CHANGES)),
                'comment': GetApplicationQueueReasonRequest.NO_CHANGES
            }

        return {}

    @classmethod
    def process(cls, message: FormDataMessage, **kwargs) -> ExecutionData:

        request = getattr(message.parse_body, cls.name_service)

        response_body = render_type2xml(
            cls.get_response(request), name_type='FormDataResponse')

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
    def get_response(cls, request: Any) -> Any:
        """Формирует ответ на GetApplicationQueueReasonRequest.

        :param request: Тело запроса.
        :type: GetApplicationQueueReasonRequestType

        :return: Тело ответа.
        :rtype: FormDataResponseType

        """

        declaration, _ = get_declaration_by_client_or_portal_id(
            cls.prepare_query(request), request.orderId)

        order_id = int(request.orderId)

        validation_errors = cls.validate(declaration)
        if validation_errors:
            return cls.parser_module.FormDataResponseType(
                changeOrderInfo=cls.parser_module.changeOrderInfoType(**{
                    'orderId': cls.parser_module.orderIdType(order_id),
                    **validation_errors
                }))

        if not declaration.position_log_exists:
            return cls.parser_module.FormDataResponseType(
                GetApplicationQueueReasonResponse=(
                    cls.parser_module.GetApplicationQueueReasonResponseType(
                        orderId=order_id,
                        IncreaseQueue=0, GotAPlace=0,
                        IncreaseBenefits=0)))

        # Дата с и Дата по, полученные из запроса.
        date_range = (request.PeriodStart, request.PeriodEnd)

        unit = declaration.mo
        unit_kind_id = unit.kind_id

        increase_queue, got_place, increase_benefits = get_position_info(
            date_range, declaration.id, unit_kind_id, unit.id)

        response = cls.parser_module.FormDataResponseType(
            GetApplicationQueueReasonResponse=(
                cls.parser_module.GetApplicationQueueReasonResponseType(
                    orderId=order_id,
                    IncreaseQueue=increase_queue, GotAPlace=got_place,
                    IncreaseBenefits=increase_benefits)))

        return response
