from __future__ import annotations

from typing import TYPE_CHECKING

from m3.plugins import ExtensionManager

from aio_client.base import const as aio_base_const
from aio_client.provider.api import PostProviderRequest
from aio_client.provider.api import push_request
from django.db.models import OuterRef
from django.db.models import Prefetch
from django.db.models import Subquery

from kinder.core.children.models import ChildrenDelegate
from kinder.core.declaration.models import Declaration
from kinder.core.direct.models import DRS
from kinder.core.direct.models import Direct

from concentrator.smev3_v321.base.utils import get_adaptation_program
from concentrator.smev3_v321.base.utils import get_address
from concentrator.smev3_v321.base.utils import get_child_info
from concentrator.smev3_v321.base.utils import get_language
from concentrator.smev3_v321.base.utils import get_medical_report_without_files
from concentrator.smev3_v321.base.utils import get_person_identity_doc_info
from concentrator.smev3_v321.base.utils import get_person_info
from concentrator.smev3_v321.base.utils import get_schedule
from concentrator.smev3_v321.base.utils import render_type2xml
from concentrator.smev3_v321.constants import SUCCESS_MESSAGE
from concentrator.smev3_v321.enums import StatusCode
from concentrator.smev3_v321.exceptions import ContentFailure
from concentrator.smev3_v321.executors import AbstractExecutor
from concentrator.smev3_v321.model import ExecutionData
from concentrator.smev3_v321.service_types import kinder_conc
from concentrator.smev3_v321.utils import (
    get_declaration_by_client_or_portal_id)


if TYPE_CHECKING:
    from typing import Any

    from django.db.models import QuerySet

    from concentrator.smev3_v321.model import FormDataMessage


class GetApplicationAdmissionRequestExecutor(AbstractExecutor):
    """Исполнитель сервиса GetApplicationAdmissionRequest."""

    name_service: str = 'GetApplicationAdmissionRequest'
    service_type_name: str = (
        kinder_conc.GetApplicationAdmissionRequestType.__name__)

    @staticmethod
    def unit_subquery(value: str) -> Subquery:
        """Возвращает подзапрос со значением указанного поля организации,
        в которую есть направление

        :param value: Значение, которое нужно получить из подзапроса
        :return: Подзапрос
        """

        return Subquery(
            Direct.objects.filter(
                declaration_id=OuterRef('id'),
                status__code__in=(DRS.REGISTER, DRS.DOGOVOR),
                group__unit__is_not_show_on_poral=False
            ).values(value)[:1])

    @classmethod
    def prepare_query(cls) -> QuerySet:
        """Выполняет подготовку запроса."""

        subquery_first_delegate = (
            ChildrenDelegate.objects.filter(
                id=Subquery(
                    ChildrenDelegate.objects.filter(
                        children_id=OuterRef('children_id')
                    ).order_by('id').values('id')[:1])
            ).select_related('delegate'))

        subquery_unit_code = cls.unit_subquery('group__unit__code')
        subquery_unit_name = cls.unit_subquery('group__unit__name')


        query = (
            Declaration.objects.annotate(
                unit_code=subquery_unit_code,
                unit_name=subquery_unit_name,
            ).select_related(
                'children'
            ).filter(
                unit_code__isnull=False
            ).prefetch_related(
                Prefetch(
                    'children__childrendelegate_set',
                    queryset=subquery_first_delegate,
                    to_attr='first_childrendelegate')))

        return query

    @classmethod
    def process(cls, message: FormDataMessage, **kwargs) -> ExecutionData:

        request = message.parse_body.GetApplicationAdmissionRequest

        content_failure_comment = None

        try:
            response_body = render_type2xml(
                cls.get_response(request), name_type='FormDataResponse')
        except ContentFailure as exc:
            response_body = render_type2xml(
                cls.parser_module.FormDataResponseType(
                    changeOrderInfo=cls.parser_module.changeOrderInfoType(
                        orderId=cls.parser_module.orderIdType(request.orderId),
                        statusCode=cls.parser_module.statusCodeType(
                            StatusCode.CODE_150.value),
                        comment=exc.content_failure_comment)),
                name_type='FormDataResponse',
            )
            content_failure_comment = exc.content_failure_comment

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
                'result': content_failure_comment or SUCCESS_MESSAGE
            })

    @classmethod
    def get_response(cls, request: Any) -> Any:
        """Формирует ответ на GetApplicationAdmissionRequest.

        :param request: Сгенерированное тело запроса.
        :type: GetApplicationAdmissionRequestType

        :return: Тело ответа.
        :rtype: FormDataResponseType

        :raise: ContentFailure

        """

        declaration, _ = get_declaration_by_client_or_portal_id(
            cls.prepare_query(), request.orderId)

        if not declaration:
            raise ContentFailure(
                aio_base_const.FAILURE,
                'Заявление по указанным параметрам не найдено')

        child = declaration.children
        children_delegate, *_ = child.first_childrendelegate or (None,)
        if not children_delegate:
            raise ContentFailure(
                aio_base_const.FAILURE, 'Не найден представитель')

        delegate = children_delegate.delegate

        entry_params = cls.parser_module.EntryParamsType(
            EntryDate=declaration.desired_date,
            Language=cls.parser_module.DataElementType(
                **get_language(declaration.spec)),
            Schedule=cls.parser_module.DataElementType(
                **get_schedule(declaration.work_type)),
            AgreementOnFullDayGroup=declaration.consent_full_time_group,
            AgreementOnOtherDayGroup=ExtensionManager().execute(
                'concentrator.smev3_v4.extensions.get_agreement_on_other_group', declaration)
        )
        unit_params = ExtensionManager().execute(
            'concentrator.smev3_v4.extensions.get_unit_params', cls.parser_module, declaration)

        if not unit_params:
            unit_params = {'EduOrganizationCode': declaration.unit_code}

        get_application_admission_response = (
            cls.parser_module.GetApplicationAdmissionResponseType(
                orderId=request.orderId,
                PersonInfo=get_person_info(cls.parser_module, delegate),
                PersonIdentityDocInfo=(
                    get_person_identity_doc_info(
                        cls.parser_module, delegate, declaration)),
                ChildInfo=get_child_info(cls.parser_module, declaration),
                Address=get_address(cls.parser_module, child),
                EntryParams=entry_params,
                AdaptationProgram=(
                    get_adaptation_program(cls.parser_module, declaration)),
                MedicalReport=get_medical_report_without_files(
                    cls.parser_module, declaration),
                **unit_params))

        response = cls.parser_module.FormDataResponseType(
            GetApplicationAdmissionResponse=get_application_admission_response)

        return response
