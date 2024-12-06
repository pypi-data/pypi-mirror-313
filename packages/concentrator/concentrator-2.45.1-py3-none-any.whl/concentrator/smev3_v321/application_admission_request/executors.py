from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from aio_client.provider.api import PostProviderRequest
from aio_client.provider.api import push_request
from django.db.models import OuterRef
from django.db.models import Prefetch
from django.db.models import Subquery

from kinder.core.children.models import Children
from kinder.core.children.models import ChildrenDelegate
from kinder.core.children.models import Delegate
from kinder.core.children.models import DelegateTypeEnumerate
from kinder.core.declaration.models import Declaration
from kinder.core.dict.models import DULDelegateType
from kinder.core.dict.models import DULTypeEnumerate
from kinder.core.dict.models import GroupOrientationDocuments
from kinder.core.dict.models import GroupSpec
from kinder.core.dict.models import GroupType
from kinder.core.dict.models import GroupTypeEnumerate
from kinder.core.dict.models import HealthNeed
from kinder.core.dict.models import WorkType
from kinder.core.dict.models import WorkTypeEnumerate
from kinder.core.direct.models import DRS
from kinder.core.direct.models import Direct
from kinder.core.direct.models import DirectDeclarationEnrollment
from kinder.core.direct.models import DirectDeclarationSourceEnum
from kinder.core.direct.report import DeclarationReporter

from concentrator.exceptions import ValidationError
from concentrator.smev3_v321.base.utils import render_type2xml
from concentrator.smev3_v321.constants import SUCCESS_MESSAGE
from concentrator.smev3_v321.enums import StatusCode
from concentrator.smev3_v321.exceptions import ContentFailure
from concentrator.smev3_v321.executors import AbstractExecutor
from concentrator.smev3_v321.model import ExecutionData
from concentrator.smev3_v321.models import ApplicantAnswer
from concentrator.smev3_v321.service_types import kinder_conc
from concentrator.smev3_v321.utils import (
    get_declaration_by_client_or_portal_id)
from concentrator.smev3_v321.utils import update_middle_name_params

from .constants import APPLICATION_ADMISSION_REQUEST_ERROR_COMMENT
from .constants import DIRECTS_NOT_FOUND_ERROR_COMMENT
from .constants import MULTIPLE_DIRECTS_FOUND_ERROR_COMMENT


if TYPE_CHECKING:
    from django.db.models import QuerySet

    from concentrator.smev3_v321.model import FormDataMessage


class ApplicationAdmissionRequestExecutor(AbstractExecutor):
    """Исполнитель сервиса GetApplicationAdmissionRequest."""

    name_service: str = 'ApplicationAdmissionRequest'
    service_type_name: str = (
        kinder_conc.ApplicationAdmissionRequestType.__name__)

    @classmethod
    def prepare_query(cls) -> QuerySet:
        """Выполняет подготовку запроса."""

        subquery_first_two_delegates = (
            ChildrenDelegate.objects.filter(
                id__in=Subquery(
                    ChildrenDelegate.objects.filter(
                        children_id=OuterRef('children_id')
                    ).order_by('id').values('id')[:2])
            ).select_related('delegate'))

        query = (
            Declaration.objects.prefetch_related(
                Prefetch(
                    'children__childrendelegate_set',
                    queryset=subquery_first_two_delegates,
                    to_attr='first_two_childrendelegates')
            ).prefetch_related(
                Prefetch(
                    'direct_set',
                    queryset=Direct.objects.filter(status__code=DRS.REGISTER),
                    to_attr='all_directs')))

        return query

    @classmethod
    def prepare_response(
            cls, order_id: int, status_code: int, comment: str | None = None
    ) -> Any:
        """Формирует ответ для сервиса.

        Формирует ответ FormDataResponseType с блоком данных changeOrderInfo.

        :param order_id: Идентификатор заявления
        :param status_code: Код ответа
        :param comment: Сообщение ответа

        :return: Тело ответа.
        :rtype: FormDataResponseType

        """

        return cls.parser_module.FormDataResponseType(
            changeOrderInfo=cls.parser_module.changeOrderInfoType(
                orderId=cls.parser_module.orderIdType(order_id),
                statusCode=cls.parser_module.statusCodeType(status_code),
                comment=comment))

    @classmethod
    def process(cls, message: FormDataMessage, **kwargs) -> ExecutionData:

        request = getattr(message.parse_body, cls.name_service)

        declaration, _ = get_declaration_by_client_or_portal_id(
            cls.prepare_query(), request.orderId)

        content_failure_comment = None

        try:
            response = cls.get_response(declaration, request)
        except ContentFailure as exc:
            response = cls.prepare_response(
                request.orderId, exc.content_failure_code,
                exc.content_failure_comment)
            content_failure_comment = exc.content_failure_comment

        response_body = render_type2xml(response, name_type='FormDataResponse')

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
    def get_response(cls, declaration: Declaration, request: Any) -> Any:
        """Формирует ответ на GetApplicationAdmissionRequest.

        :param declaration: Заявление.
        :param request: Сгенерированное тело запроса.
        :type: ApplicationAdmissionRequestType

        :return: Тело ответа.
        :rtype: FormDataResponseType

        :raise: ContentFailure

        """

        if not declaration:
            raise ContentFailure(
                StatusCode.CODE_150.value,
                APPLICATION_ADMISSION_REQUEST_ERROR_COMMENT)

        direct, *other = declaration.all_directs or (None,)
        if not direct:
            raise ContentFailure(
                StatusCode.CODE_150.value, DIRECTS_NOT_FOUND_ERROR_COMMENT)
        elif other:
            raise ContentFailure(
                StatusCode.CODE_150.value, MULTIPLE_DIRECTS_FOUND_ERROR_COMMENT)

        child = declaration.children

        children_delegate_1, *other_children_delegate = (
            declaration.children.first_two_childrendelegates or (None,))

        person_info = request.PersonInfo

        patronymic = person_info.PersonMiddleName
        person_doc_info = request.PersonIdentityDocInfo

        delegate_params = {
            'surname': person_info.PersonSurname,
            'firstname': person_info.PersonName,
            'patronymic': patronymic,
            'phones': person_info.PersonPhone,
            'email': person_info.PersonEmail,
            'dul_type': DULDelegateType.objects.filter(
                esnsi_code=person_doc_info.IdentityDocName.code).first(),
            'dul_series': person_doc_info.IdentityDocSeries,
            'dul_number': person_doc_info.IdentityDocNumber,
            'dul_date': person_doc_info.IdentityDocIssueDate,
            'dul_place': person_doc_info.IdentityDocIssueCode,
            'dul_issued_by': person_doc_info.IdentityDocIssued,
        }

        delegate_params = (
            update_middle_name_params(
                patronymic, delegate_params, is_parents=True))

        delegate = cls.create_or_update_delegate(
            child, children_delegate_1, delegate_params)

        person2info = request.Person2Info

        if person2info:
            person2middlename = person2info.Person2MiddleName

            delegate2_params = {
                'surname': person2info.Person2Surname,
                'firstname': person2info.Person2Name,
                'patronymic': person2middlename,
                'phones': person2info.Person2Phone,
                'email': person2info.Person2Email,
            }

            delegate2_params = update_middle_name_params(
                person2middlename, delegate2_params, is_parents=True)

            # Если совпали типы у родителей, то определяем второго как
            # законного представителя
            if delegate2_params.get('type') == delegate_params.get('type'):
                delegate2_params['type'] = DelegateTypeEnumerate.LEX

            children_delegate_2, *_ = other_children_delegate or (None,)
            cls.create_or_update_delegate(
                child, children_delegate_2, delegate2_params)

        child_info = request.ChildInfo
        child.surname = child_info.ChildSurname
        child.firstname = child_info.ChildName
        child.patronymic = child_info.ChildMiddleName
        child.date_of_birth = child_info.ChildBirthDate

        doc_info = child_info.ChildBirthDocRF
        if doc_info:
            child.dul_series = doc_info.ChildBirthDocSeries
            child.dul_number = doc_info.ChildBirthDocNumber
            child.dul_date = doc_info.ChildBirthDocIssueDate
            child.zags_act_number = doc_info.ChildBirthDocActNumber
            child.zags_act_date = doc_info.ChildBirthDocActDate
            child.zags_act_place = doc_info.ChildBirthDocIssued

        elif hasattr(child_info, 'ChildBirthAct') and child_info.ChildBirthAct:
            doc_info = child_info.ChildBirthAct
            child.dul_type = DULTypeEnumerate.OTHER
            child.zags_act_number = doc_info.ChildBirthDocActNumber
            child.zags_act_date = doc_info.ChildBirthDocActDate
            child.zags_act_place = doc_info.ChildActBirthDocIssued

        else:
            foreign_doc_info = child_info.ChildBirthDocForeign
            child.dul_type = DULTypeEnumerate.INT_SVID
            if foreign_doc_info.ChildBirthDocSeries:
                child.dul_series = foreign_doc_info.ChildBirthDocSeries
            child.dul_number = foreign_doc_info.ChildBirthDocNumber
            child.dul_date = foreign_doc_info.ChildBirthDocIssueDate
            child.zags_act_place = foreign_doc_info.ChildBirthDocIssued

        address = request.Address
        child.address_full = address.FullAddress
        child.address_place = address.Region.code
        child.address_street = address.Street.code
        child.address_house_guid = address.House.code
        child.address_corps = address.Building1
        child.address_flat = address.Apartment

        entry_params = request.EntryParams
        declaration.spec = GroupSpec.objects.filter(
            esnsi_code=entry_params.Language.code).first()
        declaration.desired_date = entry_params.EntryDate
        declaration.work_type = WorkType.objects.filter(
            esnsi_code=entry_params.Schedule.code).first()
        agreement_on_full_day = entry_params.AgreementOnFullDayGroup

        if hasattr(entry_params, 'AgreementOnOtherDayGroup') and entry_params.AgreementOnOtherDayGroup:

            if WorkType.objects.get(esnsi_code=entry_params.Schedule.code).code == WorkTypeEnumerate.FULL:
                if entry_params.AgreementOnOtherDayGroup:
                    declaration.consent_short_time_group = True

            elif WorkType.objects.get(esnsi_code=entry_params.Schedule.code).code == WorkTypeEnumerate.ALLDAY:
                if entry_params.AgreementOnOtherDayGroup:
                    declaration.consent_full_time_group = True


        if agreement_on_full_day:
            declaration.consent_full_time_group = agreement_on_full_day

        adaptation_program = request.AdaptationProgram
        desired_group_type = GroupType.objects.filter(
            esnsi_code=adaptation_program.AdaptationGroup.code).first()
        declaration.desired_group_type = desired_group_type

        health_need_query = HealthNeed.objects.filter(
            group_type=desired_group_type)
        # AdaptationGroupType необязательный, если группа общеразвивающая
        if desired_group_type.code != GroupTypeEnumerate.DEV:
            health_need_query = health_need_query.filter(
                esnsi_code=adaptation_program.AdaptationGroupType.code)
        child.health_need = health_need_query.first()

        agreement_on_general_group = adaptation_program.AgreementOnGeneralGroup

        if hasattr(adaptation_program, 'AgreementAdaptationEducationGroup'):
            declaration.adapted_program_consent = adaptation_program.AgreementAdaptationEducationGroup

        if agreement_on_general_group:
            declaration.consent_dev_group = agreement_on_general_group

        agreement_on_care = adaptation_program.AgreementOnCareGroup

        if agreement_on_care:
            declaration.consent_care_group = agreement_on_care

        need_special_care = adaptation_program.NeedSpecialCareConditions

        if need_special_care:
            child.health_need_special_support = need_special_care

        medical_report = request.MedicalReport

        if medical_report:
            child.health_number = medical_report.DocNumber
            child.health_need_start_date = medical_report.DocIssueDate
            child.health_issued_by = medical_report.DocIssued
            child.health_need_expiration_date = (
                medical_report.DocExpirationDate)
            child.health_series = medical_report.DocSeries

            try:
                group_orientation_document = (
                    GroupOrientationDocuments.objects.get(
                        esnsi_code=medical_report.DocName.code))
            except GroupOrientationDocuments.DoesNotExist:
                raise ValidationError('Указано неверное значение DocName')

            child.health_need_confirmation = group_orientation_document

        child.save()
        declaration.save()

        params = dict(
            direct_id=direct.id, delegate_id=delegate.id,
            doc_list_review=request.DocListReview,
            license_charter=request.LicenseCharter,
        )
        rep = DeclarationReporter(params, params)
        report_url = rep.make_report()
        DirectDeclarationEnrollment.objects.create(
            service_type=request.ServicesType,
            direct=direct,
            user=None,
            file=report_url,
            source=DirectDeclarationSourceEnum.EPGU)

        ApplicantAnswer.objects.update_or_create(
            direct=direct, defaults=dict(answer=True, comment=''))

        mo_name = declaration.mo.name

        return cls.prepare_response(
            request.orderId, 
            StatusCode.CODE_230.value,
            comment=f'Согласие с предоставленным местом направлено на рассмотрение в {mo_name}.'
        )

    @classmethod
    def create_or_update_delegate(
            cls, child: Children, children_delegate: ChildrenDelegate,
            params: dict[str, Any]
    ) -> Delegate:
        """Создает или обновляет данные представителя.

        :param child: Ребенок из заявления.
        :param children_delegate: Связь между ребенком и представителем.
        :param params: Данные представителя.

        :return: Возвращает нового или с обновленными данными представителя.

        """

        if not children_delegate:
            delegate = Delegate.objects.create(**params)
            ChildrenDelegate.objects.create(children=child, delegate=delegate)
        else:
            delegate = children_delegate.delegate
            for param_name, value in params.items():
                setattr(delegate, param_name, value)
            delegate.save()
        return delegate
