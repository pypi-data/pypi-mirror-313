from __future__ import annotations

from typing import TYPE_CHECKING

from aio_client.provider.api import PostProviderRequest
from aio_client.provider.api import push_request
from django.db.models import Q
from m3.plugins import ExtensionManager

from kinder.core.declaration.models import Declaration
from kinder.core.declaration.enum import DeclarationSourceEnum
from kinder.core.declaration_status.enum import DSS
from kinder.core.dict.models import DULTypeEnumerate
from kinder.core.helpers import get_q

from concentrator.smev3_v321.base.utils import render_type2xml
from concentrator.smev3_v321.constants import SUCCESS_MESSAGE
from concentrator.smev3_v321.enums import StatusCode
from concentrator.smev3_v321.enums import StatusTechCode
from concentrator.smev3_v321.executors import AbstractExecutor
from concentrator.smev3_v321.exceptions import ContentFailure
from concentrator.smev3_v321.model import ExecutionData
from concentrator.smev3_v321.order.helpers import (
    OrderRequestSMEV3RequestManager)
from concentrator.smev3_v321.order.request_context import OrderRequestContext
from concentrator.smev3_v321.service_types import kinder_conc

from .constants import APPLICATION_ORDER_INFO_REQUEST
from .constants import APPLICATION_ORDER_INFO_REQUEST_ERROR_COMMENT
from .constants import APPLICATION_ORDER_INFO_REQUEST_SUCCESS_COMMENT
from .constants import SUBSCRIPTION_UNAVAILABLE_COMMENT
from .utils import update_declaration_from_request


if TYPE_CHECKING:
    from typing import Any

    from concentrator.smev3_v321.model import FormDataMessage


class ApplicationOrderInfoRequestExecutor(AbstractExecutor):
    """Исполнитель сервиса ApplicationOrderInfoRequest."""

    name_service: str = APPLICATION_ORDER_INFO_REQUEST
    service_type_name: str = (
        kinder_conc.ApplicationOrderInfoRequestType.__name__)
    unavailable_sources_for_subscription: tuple[str, ...] = (
        DeclarationSourceEnum.EPGU,
        DeclarationSourceEnum.CONCENTRATOR,
        DeclarationSourceEnum.EPGULIPETSK,
    )

    @classmethod
    def _process(
            cls, request: Any
    ) -> tuple[int, str]:
        """Доп.метод для удобства обработки и возвращения результата.

        :param request: Запрос
        :type: ApplicationOrderInfoRequestType

        :return: Кортеж (код статуса ответа, комментарий)
        """

        child_info = request.ChildInfo
        child_birth_doc_rf = child_info.ChildBirthDocRF
        child_doc_info = None
        dul_filter = Q()

        if child_birth_doc_rf:
            child_doc_info = child_birth_doc_rf
            dul_filter = (
                Q(children__dul_type=DULTypeEnumerate.SVID)
                & Q(children__dul_series=child_doc_info.ChildBirthDocSeries))
        elif child_info.ChildBirthDocForeign:
            child_doc_info = child_info.ChildBirthDocForeign
            dul_filter = Q(children__dul_type=DULTypeEnumerate.INT_SVID)
            series = child_doc_info.ChildBirthDocSeries
            # Серия может быть не заполнена у иностранных документов
            dul_filter &= (
                Q(children__dul_series=series) if series else
                get_q('children__dul_series', is_empty=True)
            )
        elif hasattr(child_info, 'ChildBirthAct') and child_info.ChildBirthAct:
            act_info = child_info.ChildBirthAct
            dul_filter = Q(
                children__dul_type=DULTypeEnumerate.OTHER,
                children__zags_act_number=act_info.ChildBirthDocActNumber,
            )

            if act_info.ChildBirthDocActDate:
                dul_filter &= Q(children__zags_act_date=act_info.ChildBirthDocActDate)

            if act_info.ChildActBirthDocIssued:
                dul_filter &= Q(children__zags_act_place=act_info.ChildActBirthDocIssued)

        if child_doc_info:
            dul_filter &= Q(children__dul_number=child_doc_info.ChildBirthDocNumber)

        # Фильтр для поиска заявления по ФИ ребенка, Дате рождения
        # и ДУЛ (серия, номер).
        base_filter = (
            Q(children__surname__iexact=child_info.ChildSurname)
            & Q(children__firstname__iexact=child_info.ChildName)
            & Q(children__date_of_birth=child_info.ChildBirthDate)
            & dul_filter)

        declarations_query = Declaration.objects.filter(base_filter).exclude(
            status__code=DSS.ARCHIVE
        ).select_related('children')

        # Проверка наличия заявления
        if not declarations_query:
            return (
                StatusTechCode.CODE_4.value,
                APPLICATION_ORDER_INFO_REQUEST_ERROR_COMMENT)

        has_full_declaration, error_message = False, ''

        for declaration in declarations_query:
            if declaration.source in cls.unavailable_sources_for_subscription:
                raise ContentFailure(
                    StatusCode.CODE_150.value,
                    SUBSCRIPTION_UNAVAILABLE_COMMENT
                )

            # Проверка наличия нужных данных у представителя и попытка
            # обновления их данными из запроса (данные могут измениться).
            has_full_info, delegate_id, error_message = (
                update_declaration_from_request(declaration, request))

            if not has_full_info:
                continue
            has_full_declaration = True

            if child_birth_doc_rf:
                zags_act_number = child_birth_doc_rf.ChildBirthDocActNumber
                ExtensionManager().execute(
                    'kinder.plugins.tatarstan_specifics.extensions'
                    '.update_child_zags_act_number',
                    declaration, zags_act_number)

            OrderRequestSMEV3RequestManager(
                OrderRequestContext(**{
                    'declaration_id': declaration.id,
                    'order_id': request.orderId,
                    'delegate_id': delegate_id,
                    'parser_module': cls.parser_module.__name__
                })
            ).apply_async()

        # Если нет ни одного заявлений с полными данными, прекращаем обработку
        if not has_full_declaration:
            return StatusTechCode.CODE_4.value, error_message

        return (
            StatusTechCode.CODE_3.value,
            APPLICATION_ORDER_INFO_REQUEST_SUCCESS_COMMENT)

    @classmethod
    def process(cls, message: FormDataMessage, **kwargs):

        request = message.parse_body.ApplicationOrderInfoRequest
        try:
            tech_code, comment = cls._process(request)
            status_code = cls.parser_module.statusCodeType(techCode=tech_code)
        except ContentFailure as exc:
            comment = exc.content_failure_comment
            status_code = cls.parser_module.statusCodeType(exc.content_failure_code)

        response_body = render_type2xml(
            cls.parser_module.FormDataResponseType(
                changeOrderInfo=cls.parser_module.changeOrderInfoType(
                    orderId=cls.parser_module.orderIdType(request.orderId),
                    statusCode=status_code,
                    comment=comment,
                )
            ),
            name_type='FormDataResponse',
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
