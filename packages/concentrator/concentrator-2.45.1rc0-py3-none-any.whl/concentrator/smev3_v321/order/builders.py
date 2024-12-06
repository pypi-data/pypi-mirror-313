from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from m3.plugins import ExtensionManager
from django.db.models import OuterRef
from django.db.models import Subquery

from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration_status.models import DeclarationStatusTransfer
from kinder.core.direct.models import DRS
from kinder.core.direct.models import TEXT_CHANGE_STATUS
from kinder.core.direct.models import DirectRefusalReason
from kinder.core.direct.models import DirectStatusLog
from kinder.core.direct.models import RefusalReasonInitiatorType
from kinder.webservice.smev3.utils.request_builder import BaseRequestBuilder

from concentrator.smev3_v321 import settings
from concentrator.smev3_v321.base.utils import get_adaptation_program
from concentrator.smev3_v321.base.utils import get_address
from concentrator.smev3_v321.base.utils import get_child_info
from concentrator.smev3_v321.base.utils import get_language
from concentrator.smev3_v321.base.utils import get_medical_report_without_files
from concentrator.smev3_v321.base.utils import get_person_identity_doc_info
from concentrator.smev3_v321.base.utils import get_person_info
from concentrator.smev3_v321.base.utils import get_schedule
from concentrator.smev3_v321.base.utils import is_cancel_allowed
from concentrator.smev3_v321.base.utils import render_type2xml
from concentrator.smev3_v321.constants import PRIVILEGE_DOC_ISSUED
from concentrator.smev3_v321.models import ApplicantAnswer
from concentrator.smev3_v321.service_types import kinder_order
from concentrator.smev3_v321.utils import get_auto_change_days

from .constants import DECLARATION_FORMATION
from .constants import DELEGATE_REFUSED
from .constants import DIRECTED_TO_DOO
from .constants import NEED_NOT_CONFIRMED
from .constants import WAITING_FOR_CONTRACT


if TYPE_CHECKING:
    from concentrator.smev3_v321.models import OrderRequest

    from .request_context import OrderRequestContext
    from .request_context import UpdateOrderRequestContext


class OrderRequestBuilder(BaseRequestBuilder):
    """Строитель запроса OrderRequest СМЭВ 3."""

    parser_module = kinder_order

    def __init__(
            self,
            request: OrderRequest,
            context: OrderRequestContext,
            *args, **kwargs
    ) -> None:
        super().__init__(request)

        self.context = context

    def _get_status_history_data(self) -> Any:
        """Получение данных по истории статусов заявки

        :return: Данные по истории статусов заявления
        :rtype: statusHistoryListType
        """

        history_data = []

        _declaration = self.request.declaration

        if not _declaration.declarationstatuslog_set.exists():

            epgu_status_code, epgu_comment = (
                self.context.epgu_status_mapper[
                    {'status__code': _declaration.status.code}])

            return self.parser_module.statusHistoryListType(
                [self.parser_module.statusHistoryType(
                    statusCode=self.parser_module.statusCodeType(
                        orgCode=epgu_status_code),
                    statusDate=_declaration.date,
                    statusComment=epgu_comment,
                    cancelAllowed=is_cancel_allowed(_declaration.status))])

        auto_change_days = Subquery(
            DeclarationStatusTransfer.objects.filter(
                from_status=OuterRef('old_status'),
                to_status=OuterRef('status'),
                auto_change_days__gt=0
            ).values('auto_change_days')[:1])

        declaration_status_log = (
            _declaration.declarationstatuslog_set.annotate(
                auto_change_days=auto_change_days
            ).values(
                'id', 'old_status__code', 'status__code', 'datetime',
                'comment', 'auto_change_days'
            ).order_by('datetime').all())

        for status_history in declaration_status_log:
            epgu_status_code, epgu_comment = (
                self.context.epgu_status_mapper[status_history])

            history_data.append(self.parser_module.statusHistoryType(
                statusCode=self.parser_module.statusCodeType(
                    orgCode=epgu_status_code),
                statusDate=status_history['datetime'],
                statusComment=epgu_comment,
                cancelAllowed=is_cancel_allowed(_declaration.status)))

        return self.parser_module.statusHistoryListType(history_data)

    def _get_edu_organizations_data(self) -> list[Any]:
        """Получение данных по желаемым ДОО в заявке.

        :return: Список данных по желаемым ДОО
        :rtype: EduOrganizationType
        """

        declaration_unit_data = (
            self.request.declaration.declarationunit_set.values_list(
                'unit_id', 'ord', 'unit__name'))

        return [
            self.parser_module.EduOrganizationType(
                code=unit_id,
                PriorityNumber=unit_ord,
                valueOf_=unit_name)
            for unit_id, unit_ord, unit_name in declaration_unit_data]

    def _get_application_data(self) -> Any:
        """Получение всех данных по заявке

        :return: Данные по заявлению
        :rtype: ApplicationType
        """

        _declaration = self.request.declaration

        if self.context.delegate_id:
            delegate = (
                _declaration.children.childrendelegate_set.select_related(
                    'delegate'
                ).get(delegate_id=self.context.delegate_id).delegate)
        else:
            delegate = (
                _declaration.children.childrendelegate_set.select_related(
                    'delegate'
                ).first().delegate)

        application_data = self.parser_module.ApplicationType(
            PersonIdentityDocInfo=(
                get_person_identity_doc_info(
                    self.parser_module, delegate, _declaration)),
            PersonInfo=get_person_info(self.parser_module, delegate),
            ChildInfo=get_child_info(self.parser_module, _declaration),
            Address=get_address(self.parser_module, _declaration.children),
            EntryParams=self.parser_module.EntryParamsType(
                EntryDate=_declaration.desired_date,
                Language=self.parser_module.DataElementType(
                    **get_language(_declaration.spec)),
                Schedule=self.parser_module.DataElementType(
                    **get_schedule(_declaration.work_type)),
                AgreementOnFullDayGroup=_declaration.consent_full_time_group,
                AgreementOnOtherDayGroup=ExtensionManager().execute(
                    'concentrator.smev3_v4.extensions.get_agreement_on_other_group', _declaration)),
            AdaptationProgram=(
                get_adaptation_program(self.parser_module, _declaration)),
            MedicalReport=get_medical_report_without_files(
                self.parser_module, _declaration),
            EduOrganizations=self.parser_module.EduOrganizationsType(
                EduOrganization=self._get_edu_organizations_data(),
                AllowOfferOther=_declaration.offer_other))

        for declaration_unit in _declaration.declarationunit_set.all():
            if declaration_unit.sibling:
                application_data.add_BrotherSisterInfo(
                    self.parser_module.BrotherSisterInfoType(
                        ChildSurname=declaration_unit.sibling.surname,
                        ChildName=declaration_unit.sibling.firstname,
                        ChildMiddleName=declaration_unit.sibling.patronymic,
                        EduOrganization=self.parser_module.DataElementType(
                            code=declaration_unit.unit_id,
                            valueOf_=declaration_unit.unit.name)))

        declaration_privilege = DeclarationPrivilege.objects.filter(
            privilege=_declaration.best_privilege,
            declaration=_declaration, privilege__esnsi_code__isnull=False
        ).first()

        if declaration_privilege:

            end_date_info = {}
            if declaration_privilege._privilege_end_date:
                end_date_info['DocExpirationDate'] = (
                    declaration_privilege._privilege_end_date)

            doc_info = self.parser_module.DocInfoType(
                DocIssueDate=(
                    declaration_privilege.doc_date or _declaration.date),
                DocIssued=(
                    declaration_privilege.doc_issued_by
                    or PRIVILEGE_DOC_ISSUED),
                **end_date_info)

            application_data.set_BenefitInfo(
                self.parser_module.BenefitInfoWithoutFilesType(
                    BenefitCategory=self.parser_module.DataElementType(
                        code=declaration_privilege.privilege.esnsi_code,
                        valueOf_=declaration_privilege.privilege.name),
                    BenefitDocInfo=doc_info))

        return application_data

    def build(self) -> str:
        """Формирует запрос OrderRequest.

        :return: запрос xml
        """
        return render_type2xml(
            self.parser_module.OrderRequestType(**self.get_content()),
            name_type='OrderRequest'
        )

    def get_content(self) -> dict[str, Any]:
        """Возвращает данные для запроса OrderRequest.

        :return: словарь с данными.

        """

        content = {
            'env': settings.ORDER_REQUEST_SERVICE_ENV,
            'CreateOrderRequest': self.parser_module.CreateOrderRequestType(
                orderId_InfoRequest=self.context.order_id,
                requestDate=self.request.declaration.date,
                statusHistoryList=self._get_status_history_data(),
                application=self._get_application_data())
        }

        return content


class UpdateOrderRequestBuilder(OrderRequestBuilder):
    """Строитель запроса UpdateOrderRequest СМЭВ 3."""

    def __init__(
            self, request: OrderRequest,
            context: UpdateOrderRequestContext, *args, **kwargs
    ) -> None:
        super().__init__(request, context)

    def _get_status_history_data(self) -> Any:
        """Получение данных по статусу заявки (код и комментарий для ЕПГУ).

        :return: Данные истории изменений статуса заявления
        :rtype: statusHistoryListType
        """

        _declaration = self.request.declaration

        auto_change_days = Subquery(
            DeclarationStatusTransfer.objects.filter(
                from_status=OuterRef('old_status'),
                to_status=OuterRef('status'),
                auto_change_days__gt=0
            ).values('auto_change_days')[:1])

        current_decl_status_code = _declaration.status.code
        status_date = _declaration.date
        status_mapper = self.context.epgu_status_mapper

        # Произошло изменение статуса заявления,
        # достаем текущий установленный статус
        if self.context.declaration_status_changed:

            decl_status_log = _declaration.declarationstatuslog_set.latest(
                'datetime')

            # Комментарий при смене статуса заявления
            declaration_comment = decl_status_log.comment

            # Если произошла авто-смена статуса заявления при изменении статуса
            # направления, берем комментарий при смене статуса направления
            if declaration_comment == TEXT_CHANGE_STATUS:
                comment = DirectStatusLog.objects.filter(
                    direct__declaration=_declaration).latest(
                    'created_at').comment
            else:
                comment = declaration_comment

            doc_date_before = get_auto_change_days(decl_status_log)

            epgu_status_code, epgu_comment = (
                self.context.epgu_status_mapper[
                    {
                        'status__code': current_decl_status_code,
                        'comment': comment,
                        'auto_change_days': doc_date_before
                     }])
        # Произошло изменение статуса направления
        elif self.context.direct_status_log:
            new_direct_status = self.context.direct_status_log['status']

            if new_direct_status == DRS.REGISTER:
                has_applicant_answer = ApplicantAnswer.objects.filter(
                    direct=self.context.direct
                ).values_list('answer', flat=True).first()

                if has_applicant_answer:
                    epgu_status_code, epgu_comment = status_mapper[
                        {'status__code': DECLARATION_FORMATION}]
                else:
                    epgu_status_code, epgu_comment = status_mapper[
                        {'status__code': DIRECTED_TO_DOO}]

            elif new_direct_status in (DRS.REJECT, DRS.REFUSED):
                initiator_type = DirectRefusalReason.objects.filter(
                    direct_status_log_id=self.context.direct_status_log['id']
                ).values_list('reason__initiator_type', 'reason__name').first()

                # Для статуса Не явился не выбирается инициатор
                if new_direct_status == DRS.REJECT:
                    epgu_status_code, epgu_comment = (
                        self.context.epgu_status_mapper[
                            {
                                'status__code': NEED_NOT_CONFIRMED,
                                'created_at':
                                    self.context.direct_status_log[
                                        'created_at'],
                                'old_status':
                                    self.context.direct_status_log[
                                        'old_status'],
                                'new_status_code': new_direct_status,
                            }])
                elif (initiator_type['reason__initiator_type'] ==
                        RefusalReasonInitiatorType.EMPLOYEE):
                    epgu_status_code, epgu_comment = (
                        self.context.epgu_status_mapper[
                            {
                                'status__code': NEED_NOT_CONFIRMED,
                                'reason': initiator_type['reason__name'],
                                'created_at':
                                    self.context.direct_status_log['created_at'],
                                'old_status':
                                    self.context.direct_status_log['old_status'],
                                'new_status_code': new_direct_status,
                            }])
                elif initiator_type == RefusalReasonInitiatorType.PARENT:
                    epgu_status_code, epgu_comment = (
                        self.context.epgu_status_mapper[
                            {
                                'status__code': DELEGATE_REFUSED,
                                'new_status_code': new_direct_status,
                            }])
            elif new_direct_status == DRS.DOGOVOR:
                epgu_status_code, epgu_comment = (
                    self.context.epgu_status_mapper[
                        {
                            'status__code': WAITING_FOR_CONTRACT,
                            'created_at':
                                self.context.direct_status_log['created_at'],
                        }])
        # Произошло событие "Отправка в ЭДС запроса ApplicationRequest" или
        # "В ЭДС пришло изменение и изменения отклонены"
        # (Заявление - вкладка "Изменения с ЕПГУ" - выбрать запись - Отказать)
        elif self.context.event:
            epgu_status_code, epgu_comment = (
                self.context.epgu_status_mapper[
                    {'status__code': self.context.event}])
        # Произошло событие изменение полей заявления (кроме статуса).
        # Достаем последний установленный статус из лога статусов,
        # если он пуст, то берем текуший статус заявки
        else:
            decl_status_log = _declaration.declarationstatuslog_set.annotate(
                auto_change_days=auto_change_days
            ).values(
                'id', 'old_status__code', 'status__code', 'datetime',
                'comment', 'auto_change_days'
            ).order_by('id').last()

            if decl_status_log:
                epgu_status_code, epgu_comment = (
                    self.context.epgu_status_mapper[decl_status_log])
                status_date = decl_status_log['datetime']
            else:
                epgu_status_code, epgu_comment = (
                    self.context.epgu_status_mapper[
                        {'status__code': current_decl_status_code}])

        return self.parser_module.statusHistoryListType([
            self.parser_module.statusHistoryType(
                statusCode=self.parser_module.statusCodeType(
                    orgCode=epgu_status_code),
                statusDate=status_date,
                statusComment=epgu_comment,
                cancelAllowed=is_cancel_allowed(_declaration.status))
        ])

    def get_content(self) -> dict[str, Any]:
        """Возвращает данные для запроса UpdateOrderRequest.

        :return: словарь с данными.

        """

        content = {
            'env': settings.ORDER_REQUEST_SERVICE_ENV,
        }

        if (
                self.context.declaration_status_changed
                or self.context.direct_status_log
                or self.context.event
        ):

            content = {
                **content,
                'UpdateOrderRequest': self.parser_module.UpdateOrderRequestType(
                    orderId=int(self.context.order_id),
                    statusHistoryList=self._get_status_history_data())
            }

        else:

            content = {
                **content,
                'UpdateOrderRequest': self.parser_module.UpdateOrderRequestType(
                    orderId=int(self.context.order_id),
                    statusHistoryList=self._get_status_history_data(),
                    application=self._get_application_data())
            }

        return content
