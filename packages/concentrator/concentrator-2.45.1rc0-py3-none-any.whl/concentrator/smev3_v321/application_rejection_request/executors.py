from __future__ import annotations

from typing import TYPE_CHECKING

from aio_client.provider.api import PostProviderRequest
from aio_client.provider.api import push_request
from django.db.models import Prefetch

from kinder.core.declaration.models import Declaration
from kinder.core.direct.models import DRS
from kinder.core.direct.models import Direct

from concentrator.smev3_v321.base.utils import is_cancel_allowed
from concentrator.smev3_v321.base.utils import render_type2xml
from concentrator.smev3_v321.constants import SUCCESS_MESSAGE
from concentrator.smev3_v321.executors import AbstractExecutor
from concentrator.smev3_v321.model import ExecutionData
from concentrator.smev3_v321.models import ApplicantAnswer
from concentrator.smev3_v321.service_types import kinder_conc
from concentrator.smev3_v321.utils import (
    get_declaration_by_client_or_portal_id)

from .enums import ApplicationRejectionMessageEnum as MessageEnum


if TYPE_CHECKING:
    from typing import Any

    from django.db.models import QuerySet

    from concentrator.smev3_v321.model import FormDataMessage


class ApplicationRejectionRequestExecutor(AbstractExecutor):
    """Исполнитель сервиса ApplicationRejectionRequest."""

    name_service: str = 'ApplicationRejectionRequest'
    service_type_name: str = (
        kinder_conc.ApplicationRejectionRequestType.__name__)

    @classmethod
    def prepare_query(cls) -> QuerySet:
        """Выполняет подготовку запроса."""

        subquery_directs = (
            Direct.objects.filter(
                status__code__in=(DRS.REGISTER, DRS.DOGOVOR)))

        query = (
            Declaration.objects.select_related(
                'status'
            ).prefetch_related(
                Prefetch(
                    'direct_set',
                    queryset=subquery_directs,
                    to_attr='all_directs')))

        return query

    @classmethod
    def process(cls, message: FormDataMessage, **kwargs) -> ExecutionData:

        request = message.parse_body.ApplicationRejectionRequest

        declaration, _ = get_declaration_by_client_or_portal_id(
            cls.prepare_query(), request.orderId)

        response_body = render_type2xml(
            cls.get_response(request, declaration),
            name_type='FormDataResponse'
        )

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
    def get_response(cls, request: Any, declaration: Declaration) -> Any:
        """Формирует и возвращает тело ответа.

        :param request: Сгенерированное тело запроса.
        :type: ApplicationRejectionRequestType
        :param declaration: Заявление.

        :return: Тело ответа.
        :rtype: FormDataResponseType

        """

        if not declaration:
            return cls.get_bad_response(
                request.orderId, MessageEnum.DECL_NOT_FOUND)

        direct, *other = declaration.all_directs or (None,)
        if not direct:
            return cls.get_bad_response(
                request.orderId, MessageEnum.DIRECT_NOT_FOUND)
        elif other:
            return cls.get_bad_response(
                request.orderId, MessageEnum.MULTIPLY_DIRECT_FOUND)

        ApplicantAnswer.objects.update_or_create(
            direct=direct,
            defaults=dict(answer=False, comment=request.comment))

        response = cls.parser_module.FormDataResponseType(
            changeOrderInfo=cls.parser_module.changeOrderInfoType(
                orderId=cls.parser_module.orderIdType(request.orderId),
                statusCode=cls.parser_module.statusCodeType(
                    MessageEnum.values.get(MessageEnum.REJECT_ACCEPTED)),
                comment=MessageEnum.REJECT_ACCEPTED,
                cancelAllowed=is_cancel_allowed(declaration.status)))

        return response

    @classmethod
    def get_bad_response(cls, order_id: int, comment: str) -> Any:
        """Формирует тело ответа в случае ошибки.

        :param order_id: Идентификатор заявки из запроса
        :param comment: Комментарий из запроса

        :return: Тело ответа.
        :rtype: FormDataResponseType

        """

        response = cls.parser_module.FormDataResponseType(
            changeOrderInfo=cls.parser_module.changeOrderInfoType(
                orderId=cls.parser_module.orderIdType(order_id),
                statusCode=cls.parser_module.statusCodeType(
                    MessageEnum.values.get(comment)),
                comment=comment))

        return response
