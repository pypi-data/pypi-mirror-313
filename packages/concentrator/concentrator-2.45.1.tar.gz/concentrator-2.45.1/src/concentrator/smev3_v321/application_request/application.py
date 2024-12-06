from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Prefetch
from django.db.models import Q
from django.db.models import QuerySet
from django.db.transaction import atomic
from m3.plugins import ExtensionManager
from m3_gar_client.utils import find_house

from kinder import logger
from kinder.core.children.models import Children
from kinder.core.children.models import ChildrenDelegate
from kinder.core.children.models import Delegate
from kinder.core.declaration.enum import DeclarationTypeInteractionEnum as DTIE
from kinder.core.declaration.enum import DeclPortalEnum
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration.models import DeclarationSourceEnum
from kinder.core.declaration.models import DeclarationUnit
from kinder.core.declaration_status.models import DSS
from kinder.core.declaration_status.models import DeclarationStatus
from kinder.core.dict.models import DULDelegateType
from kinder.core.dict.models import DULTypeEnumerate
from kinder.core.dict.models import GroupOrientationDocuments
from kinder.core.dict.models import GroupSpec
from kinder.core.dict.models import GroupType
from kinder.core.dict.models import HealthNeed
from kinder.core.dict.models import WorkType
from kinder.core.dict.models import WorkTypeEnumerate
from kinder.core.group.models import Pupil
from kinder.core.helpers import date_to_str
from kinder.core.helpers import make_full_name
from kinder.core.models import RegionCode
from kinder.core.privilege.models import Privilege
from kinder.core.unit.models import Unit
from kinder.core.utils.address import ApplicationRequestAddressType
from kinder.core.utils.address import get_gar_code
from kinder.core.utils.address import get_full_address
from kinder.plugins.contingent.models import DelegateContingent
from kinder.settings import REGION_CODE

from concentrator.change import ChangeSource
from concentrator.models import DocExtraInfo
from concentrator.smev3_v321.base.tasks import PushChangeOrderInfoRequestTask
from concentrator.smev3_v321.constants import CHANGE_DECLARATION_CODE
from concentrator.smev3_v321.constants import CHANGE_DECLARATION_COMMENT
from concentrator.smev3_v321.constants import DECLARATION_CHANGES_REFUSED_CODE
from concentrator.smev3_v321.constants import (
    DECLARATION_CHANGES_REFUSED_COMMENT)
from concentrator.smev3_v321.constants import (
    DECLARATION_CHANGES_REFUSED_REASON)
from concentrator.smev3_v321.constants import DECLARATION_RECEIVED_COMMENT
from concentrator.smev3_v321.enums import StatusTechCode
from concentrator.smev3_v321.models import DeclarationOriginMessageID
from concentrator.smev3_v321.models import ExtendedChildrenDelegate
from concentrator.smev3_v321.models import OrderRequest
from concentrator.smev3_v321.order.constants import DECLARATION_CHANGED
from concentrator.smev3_v321.order.enums import (
    PendingUpdateOrderRequestSourceVersionEnum)
from concentrator.smev3_v321.order.helpers import (
    DispatchOrderRequestSMEV3RequestManager)
from concentrator.smev3_v321.service_types import kinder_conc
from concentrator.smev3_v321.utils import changes_to_str
from concentrator.smev3_v321.utils import (
    get_declaration_by_client_or_portal_id)
from concentrator.smev3_v321.utils import update_middle_name_params

from .changes import Smev3ChangeHelper
from .changes import Smev3ChangesMap
from .changes import Smev3ChildrenChangeHelper
from .changes import Smev3DeclarationDocsChangeHelper
from .changes import Smev3DeclarationPrivilegeChangeHelper
from .changes import Smev3DeclarationUnitChangeHelper
from .changes import Smev3DelegateChangeHelper
from .changes import Smev3StorageHelper
from .constants import MAX_AGE
from .enums import ApplicationRequestMessageEnum as _Message
from .model import ApplicationManagerData
from .utils import get_address_place_code
from .utils import process_attachments


if TYPE_CHECKING:
    from concentrator.smev3_v321.model import FormDataMessage


class Application:
    """Сохранение заявления из концентратора СМЭВ 3."""

    # Поля по которым осуществляется поиск дублей ребенка и представителя.
    DOUBLE_SEARCH_FIELDS = (
        'firstname',
        'surname',
        'patronymic',
        'date_of_birth',
        'dul_type',
        'dul_series',
        'dul_number',
    )

    def __init__(
            self,
            application: kinder_conc.ApplicationType,
            attachments: list[str] | str | None = None
    ) -> None:
        self._application = application
        self._attachments = attachments

    def exclude_search_fields(self, data: dict[str, Any]) -> dict[str, Any]:
        """Фильтрация словаря с данными, от полей, использующихся для
        поиска дублей.

        :param data: Данный для фильтрации

        """

        excluded_data = {
            field: value for field, value in data.items()
            if field not in self.DOUBLE_SEARCH_FIELDS
        }
        return excluded_data

    def _create_or_update_child(
            self, existing_child: Children | None
    ) -> Children:
        """Создает или обновляет данные ребенка.

        :param existing_child: Возможный существующий ребенок
        :return: Новый или обновленный ребенок

        :raise: ValidationError

        """

        # Блок данных с общей информацией о ребенке
        child_info = self._application.ChildInfo
        # Блок данных с информацией о адресе проживания ребенка
        address = self._application.Address
        # Блок данных о здоровье ребенка
        medical_report = self._application.MedicalReport

        child_params = {}

        adaptation_program = self._application.AdaptationProgram
        if adaptation_program.AdaptationGroupType:
            try:
                # Специфика группы не является уникальным значением в ЕСНСИ,
                # поэтому для однозначной идентификации выполняется поиск
                # по связке значений: код ЕСНСИ и Направленность группы.
                child_params['health_need'] = (
                    HealthNeed.objects.get(
                        esnsi_code=adaptation_program.AdaptationGroupType.code,
                        group_type__esnsi_code=(
                            adaptation_program.AdaptationGroup.code)))
            except HealthNeed.DoesNotExist:
                raise ValidationError(
                    'Указано неверное значение AdaptationGroupType')

        if adaptation_program.NeedSpecialCareConditions is not None:
            child_params['health_need_special_support'] = (
                adaptation_program.NeedSpecialCareConditions)

        if medical_report:

            try:
                group_orientation_document = (
                    GroupOrientationDocuments.objects.get(
                        esnsi_code=medical_report.DocName.code))
            except GroupOrientationDocuments.DoesNotExist:
                raise ValidationError('Указано неверное значение DocName')

            if medical_report.DocSeries:
                child_params['health_series'] = medical_report.DocSeries

            if medical_report.DocExpirationDate:
                child_params['health_need_expiration_date'] = (
                    medical_report.DocExpirationDate)

            child_params.update({
                'health_need_confirmation': group_orientation_document,
                'health_number': medical_report.DocNumber,
                'health_need_start_date': medical_report.DocIssueDate,
                'health_issued_by': medical_report.DocIssued
            })

        if child_info.ChildMiddleName:
            child_params = update_middle_name_params(
                child_info.ChildMiddleName, child_params, is_initial=True)

        # Блок данных с информацией о ДУЛ ребенка
        if child_info.ChildBirthDocRF:
            child_params.update({
                'dul_type': DULTypeEnumerate.SVID,
                'dul_series': child_info.ChildBirthDocRF.ChildBirthDocSeries,
                'dul_number': child_info.ChildBirthDocRF.ChildBirthDocNumber,
                'dul_date': child_info.ChildBirthDocRF.ChildBirthDocIssueDate,
                'zags_act_place':
                    child_info.ChildBirthDocRF.ChildBirthDocIssued})

            if child_info.ChildBirthDocRF.ChildBirthDocActNumber:
                 child_params.update({
                     'zags_act_number': child_info.ChildBirthDocRF.ChildBirthDocActNumber
                 })
            if child_info.ChildBirthDocRF.ChildBirthDocActDate:
                child_params.update({
                    'zags_act_date': child_info.ChildBirthDocRF.ChildBirthDocActDate
                })

        elif child_info.ChildBirthDocForeign:
            child_params.update({
                'dul_type': DULTypeEnumerate.OTHER,
                'document_type':
                    child_info.ChildBirthDocForeign.ChildBirthDocName,
                'dul_number':
                    child_info.ChildBirthDocForeign.ChildBirthDocNumber,
                'dul_date':
                    child_info.ChildBirthDocForeign.ChildBirthDocIssueDate,
                'zags_act_place':
                    child_info.ChildBirthDocForeign.ChildBirthDocIssued,
            })

            if child_info.ChildBirthDocForeign.ChildBirthDocSeries:
                child_params['dul_series'] = (
                    child_info.ChildBirthDocForeign.ChildBirthDocSeries)

        elif hasattr(child_info, 'ChildBirthAct'):
            child_params.update({
                'dul_type': DULTypeEnumerate.OTHER,
                'document_type': 'Актовая запись',
                'zags_act_number':
                    child_info.ChildBirthAct.ChildBirthDocActNumber,
                'zags_act_date':
                    child_info.ChildBirthAct.ChildBirthDocActDate})

            if child_info.ChildBirthAct.ChildActBirthDocIssued:
                child_params.update({
                    'zags_act_place': child_info.ChildBirthAct.ChildActBirthDocIssued
                })

        place_guid = get_address_place_code(address)
        street_guid = get_gar_code(address.Street.code)
        house_guid = get_gar_code(address.House.code)

        address_type = ApplicationRequestAddressType(
            full_address=address.FullAddress,
            place=place_guid,
            street=street_guid,
            house=house_guid,
            apartment=address.Apartment if address.Apartment else ''
        )
        full_address = get_full_address(address_type)

        base_child_params = {
            'firstname': child_info.ChildName,
            'surname': child_info.ChildSurname,
            'patronymic': child_info.ChildMiddleName,
            'date_of_birth': child_info.ChildBirthDate,
            'address_place': place_guid,
            'address_street': street_guid,
            'address_full': full_address,
            'address_house': address.House.valueOf_,
            'address_house_guid': house_guid,
            'address_corps': address.Building1,
            'address_flat': address.Apartment
        }

        child_data = {**base_child_params, **child_params}
        if existing_child:
            update_data = self.exclude_search_fields(child_data)
            for field, value in update_data.items():
                setattr(existing_child, field, value)
            existing_child.save()
            child = existing_child
        else:
            child = Children.objects.create(**child_data)

        return child

    def _get_delegate_data(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """Возвращает основные и дополнительные данные для представителя."""

        # Блок данных с информацией о представителе.
        person_info = self._application.PersonInfo
        person_identity_doc_info = self._application.PersonIdentityDocInfo
        address = self._application.Address

        base_delegate_data = {
            'surname': person_info.PersonSurname,
            'firstname': person_info.PersonName,
            'patronymic': person_info.PersonMiddleName or '',
            'phones': person_info.PersonPhone,
            'email': person_info.PersonEmail,
            'dul_number': person_identity_doc_info.IdentityDocNumber,
            'dul_date': person_identity_doc_info.IdentityDocIssueDate,
            'address_place': get_gar_code(address.City.code),
            'address_street': get_gar_code(address.Street.code),
            'address_full': address.FullAddress,
            'address_house': address.House.valueOf_,
            'address_house_guid': get_gar_code(address.House.code),
            'address_flat': address.Apartment
        }

        # Доп. параметры для создания представителя
        params = {}

        try:
            params['dul_type'] = (
                DULDelegateType.objects.get(
                    esnsi_code=person_identity_doc_info.IdentityDocName.code))
        except DULDelegateType.DoesNotExist:
            raise ValidationError('Указано неверное значение IdentityDocName')

        if person_identity_doc_info.IdentityDocSeries:
            params['dul_series'] = person_identity_doc_info.IdentityDocSeries

        if person_identity_doc_info.IdentityDocIssueCode:
            params['dul_place'] = person_identity_doc_info.IdentityDocIssueCode

        if person_identity_doc_info.IdentityDocIssued:
            params['dul_issued_by']: person_identity_doc_info.IdentityDocIssued

        if person_info.PersonMiddleName:
            params = update_middle_name_params(
                person_info.PersonMiddleName, params,
                is_parents=person_info.Parents, is_initial=True)

        if (
            hasattr(self._application, 'ConfirmingRightIsLocatedRF') and
            self._application.ConfirmingRightIsLocatedRF
        ):
            params['confirming_rights_located_rf'] = True

        return base_delegate_data, params

    def _existing_delegates_query(
            self, child: Children
    ) -> tuple[QuerySet, bool]:
        """Осуществляет поиск представителей по ребенку, либо по
        всем представителям.

        :param child: Существующий или созданный ребенок.

        :return: Queryset с подходящими представителями, если такие есть.

        """

        base_delegate_data, params = self._get_delegate_data()

        delegate_filter = {
            'firstname': base_delegate_data.get('firstname').strip(),
            'surname': base_delegate_data.get('surname').strip(),
            'patronymic': base_delegate_data.get('patronymic').strip(),
            'dul_series__icontains': params.get('dul_series', ''),
            'dul_number__icontains': base_delegate_data.get('dul_number'),
        }

        is_child_delegate = True

        # Ищем представителя по ребенку, если нет, то среди всех представителей
        base_delegate_query = Delegate.objects.filter(**delegate_filter)
        delegate_query = (
            base_delegate_query.filter(childrendelegate__children=child))
        if not delegate_query.exists():
            delegate_query = base_delegate_query
            is_child_delegate = False

        return delegate_query, is_child_delegate

    def _create_or_update_delegate(
            self, child: Children
    ) -> tuple[Delegate, bool]:
        """Создает представителя или обновляет его данные.

        :param child: Ребенок, по которому будет происходить
            поиск представителя.
        :return: Кортеж след. вида:
            (
                Новый или обновленный представитель,
                Признак наличия связи между ребенком и представителем
            )

        :raise: ValidationError

        """

        person_info = self._application.PersonInfo
        base_delegate_data, params = self._get_delegate_data()

        existing_delegate_query, is_child_delegate = (
            self._existing_delegates_query(child))

        existing_delegate = existing_delegate_query.order_by('id').last()

        delegate_data = {**base_delegate_data, **params}

        if existing_delegate:
            update_delegate_data = self.exclude_search_fields(delegate_data)

            # Обновляем только отличающиеся поля существующего представителя
            for field, request_value in update_delegate_data.items():
                delegate_value = getattr(existing_delegate, field, None)
                if delegate_value != request_value:
                    setattr(existing_delegate, field, request_value)
            existing_delegate.save()
            delegate = existing_delegate
        else:
            delegate = Delegate.objects.create(**delegate_data)

        contingent_delegate_params = None
        # Если Представитель типа Законный представитель (Parents = false)
        # и передан блок с данными его документа (OtherRepresentative),
        # то обрабатывает блок.
        if not person_info.Parents and person_info.OtherRepresentative:
            other_representative = person_info.OtherRepresentative

            contingent_delegate_params = {
                'doc_description':
                    other_representative.OtherRepresentativeDocName,
                'number': other_representative.OtherRepresentativeDocNumber,
                'date_issue': other_representative.OtherRepresentativeDocDate,
                'issued_by': other_representative.OtherRepresentativeDocIssued
            }

            if other_representative.OtherRepresentativeDocSeries:
                contingent_delegate_params['series'] = (
                    other_representative.OtherRepresentativeDocSeries)

        contingent, _ = DelegateContingent.objects.get_or_create(
            delegate=delegate, defaults=contingent_delegate_params)

        return delegate, is_child_delegate

    def _create_or_update_children_delegate(
            self, child: Children, delegate: Delegate, is_child_delegate: bool
    ) -> None:
        """Создает/обновляет связь ребенка и представителя с доп. данными.

        :param child: Ребенок.
        :param delegate: Представитель.
        :param is_child_delegate: Признак существования связи ребенка
            и представителя.

        """

        if is_child_delegate:
            children_delegate_id = (
                ChildrenDelegate.objects.values_list('id', flat=True).get(
                    children=child, delegate=delegate))
        else:
            children_delegate_id = (
                ChildrenDelegate.objects.create(
                    children=child, delegate=delegate).id)

        if (
                not ExtendedChildrenDelegate.objects.filter(
                    children_delegate_id=children_delegate_id).exists()
        ):
            ExtendedChildrenDelegate.objects.create(
                children_delegate_id=children_delegate_id,
                order_id=str(self._application.orderId))

    def _get_mo(self):
        """Возвращает МО.

        :return: МО указанных ДОО
        :rtype: Unit

        :raise: ValidationError
        """

        units = self._application.EduOrganizations.EduOrganization
        top_units = [u for u in units if u.PriorityNumber] or units
        try:
            top_unit = Unit.objects.get(id=top_units[0].code)
        except (Unit.DoesNotExist, IndexError):
            raise ValidationError('Не удалось найти МО')
        return top_unit.get_mo()

    def _create_declaration(self, child: Children) -> Declaration:
        """Создает заявление.

        :param child: Инстанс ребенка

        :return: Новое заявление

        :raise: ValidationError

        """

        adaptation_program = self._application.AdaptationProgram
        entry_params = self._application.EntryParams

        # Доп. параметры для заявления
        params = {}

        try:
            params['desired_group_type'] = (
                GroupType.objects.get(
                    esnsi_code=adaptation_program.AdaptationGroup.code))
        except GroupType.DoesNotExist:
            raise ValidationError('Указано неверное значение AdaptationGroup')

        if adaptation_program.AgreementOnGeneralGroup is not None:
            params['consent_dev_group'] = (
                adaptation_program.AgreementOnGeneralGroup)

        if adaptation_program.AgreementOnCareGroup is not None:
            params['consent_care_group'] = (
                adaptation_program.AgreementOnCareGroup)

        try:
            params['work_type'] = (
                WorkType.objects.get(esnsi_code=entry_params.Schedule.code))
        except WorkType.DoesNotExist:
            raise ValidationError('Указано неверное значение Schedule')

        if entry_params.AgreementOnFullDayGroup is not None:
            params['consent_full_time_group'] = (
                entry_params.AgreementOnFullDayGroup)

        if hasattr(entry_params, 'AgreementOnOtherDayGroup') and entry_params.AgreementOnOtherDayGroup:

            if WorkType.objects.get(esnsi_code=entry_params.Schedule.code).code == WorkTypeEnumerate.FULL:
                if entry_params.AgreementOnOtherDayGroup:
                    params.update({'consent_short_time_group': True})

            elif WorkType.objects.get(esnsi_code=entry_params.Schedule.code).code == WorkTypeEnumerate.ALLDAY:
                if entry_params.AgreementOnOtherDayGroup:
                    params.update({'consent_full_time_group': True})

        if (
            hasattr(adaptation_program, 'AgreementAdaptationEducationGroup') and
            adaptation_program.AgreementAdaptationEducationGroup
        ):
            params['adapted_program_consent'] = adaptation_program.AgreementAdaptationEducationGroup

        try:
            params['spec'] = (
                GroupSpec.objects.get(esnsi_code=entry_params.Language.code))
        except GroupSpec.DoesNotExist:
            raise ValidationError('Указано неверное значение Language')

        declaration_status = DeclarationStatus.objects.get(code=DSS.RECEIVED)

        # Дата подачи заявления
        if self._application.FilingDate:
            params['date'] = self._application.FilingDate

        if self._application.EduOrganizations.AllowOfferOther:
            params['offer_other'] = self._application.EduOrganizations.AllowOfferOther

        return Declaration.objects.create(
            client_id=str(self._application.orderId),
            source=DeclarationSourceEnum.CONCENTRATOR,
            portal=DeclPortalEnum.PORTAL,
            type_interaction=DTIE.SMEV_3,
            children=child,
            desired_date=entry_params.EntryDate,
            status=declaration_status,
            mo=self._get_mo(), **params)

    def _add_docs(self, declaration: Declaration) -> None:
        """Добавляет прикреплённые файлы к заявке."""

        if self._attachments:
            process_attachments(self._attachments, declaration)

    def _add_declaration_units(self, declaration: Declaration) -> None:
        """Выполняет создание Желаемых ДОО для заявления.

        :param declaration: Заявление

        """

        # Отображение вида: идентификатор организации -> идентификатор ребенка.
        children_cache = {}

        # Разбор блока с информацией о братьях/сестрах ребенка.
        for sibling in self._application.BrotherSisterInfo:

            params = {}
            child_middle_name = sibling.ChildMiddleName
            if child_middle_name:
                params['children__patronymic__iexact'] = child_middle_name

            child_id = (
                Pupil.objects.filter(
                    grup__unit_id=sibling.EduOrganization.code,
                    children__surname__iexact=sibling.ChildSurname,
                    children__firstname__iexact=sibling.ChildName,
                    **params
                ).values_list('children_id', flat=True).first())

            if child_id:
                children_cache.setdefault(
                    sibling.EduOrganization.code, child_id)

        for unit in self._application.EduOrganizations.EduOrganization:

            params = {}

            child_id = children_cache.get(unit.code)
            if child_id:
                params['sibling_id'] = child_id

            DeclarationUnit.objects.create(
                declaration=declaration, unit_id=unit.code,
                ord=unit.PriorityNumber, **params)

    def _add_privilege(self, declaration: Declaration) -> None:
        """Добавляет льготу к заявке.

        :param declaration: Заявление

        :raise: ValidationError

        """

        benefit_info = self._application.BenefitInfo

        if not benefit_info:
            return

        try:
            privilege = (
                Privilege.objects.get(
                    esnsi_code=benefit_info.BenefitCategory.code))
        except Privilege.DoesNotExist:
            raise ValidationError('Льгота не найдена')

        # Блок данных с описанием документа
        benefit_doc_info = benefit_info.BenefitDocInfo

        privilege_params = {
            'doc_date': benefit_doc_info.DocIssueDate,
            'doc_issued_by': benefit_doc_info.DocIssued
        }

        if benefit_doc_info.DocExpirationDate:
            privilege_params['_privilege_end_date'] = (
                benefit_doc_info.DocExpirationDate)

        DeclarationPrivilege.objects.create(
            declaration=declaration,
            privilege=privilege,
            **privilege_params)

    @atomic
    def create(self, existing_child: Children | None) -> Declaration:
        """Создает и возвращает заявление.

        :param existing_child: Возможный найденный ребенок в системе.

        """

        child = self._create_or_update_child(existing_child)
        delegate, is_child_delegate = self._create_or_update_delegate(child)
        self._create_or_update_children_delegate(
            child, delegate, is_child_delegate)
        declaration = self._create_declaration(child)
        self._add_privilege(declaration)
        self._add_declaration_units(declaration)
        self._add_docs(declaration)

        # Создание запроса на проверку паспорта представителя
        ExtensionManager().execute(
            'passport_mvd_smev3.send_passport_mvd_request',
            delegate, declaration.id, quiet=True)

        return declaration


class ApplicationManager:
    """Выполняет первичную валидацию, полученных данных заявления
    из концентратора СМЭВ 3, поиск существующего заявление по идентификатору
    (order_id), создание/фиксирование изменений заявления.
    """

    def __init__(
            self, message: FormDataMessage,
            compare_date_with_filing: bool = False
    ) -> None:
        """Конструктор.

        :param message: Сообщение СМЭВ (AIO).
        :param compare_date_with_filing: Параметры для сравнения дат.
            Если параметр установлен, то при валидации Желаемой даты зачисления,
            она будет сравниваться с датой из тэга FilingDate

        """

        self.message = message
        self.application_type = message.parse_body.ApplicationRequest
        self.compare_date_with_filing = compare_date_with_filing

    def validate(self) -> None:
        """Выполняет первичную валидацию.

        :raise: ValidationError
        """

        if self.compare_date_with_filing:
            today = self.application_type.FilingDate.date()
        else:
            today = datetime.date.today()

        entry_date = self.application_type.EntryParams.EntryDate
        birth = self.application_type.ChildInfo.ChildBirthDate

        # Валидация Желаемой даты зачисления, которая должна быть
        # равна либо больше сегодняшней даты.
        # Или если заполнен параметр compare_date_with_filing, то дата
        # сравнивается со значением тега FilingDate
        if entry_date and entry_date < today:
            raise ValidationError(
                _Message.DESIRED_DATE_ERROR.format(today.strftime('%d.%m.%Y')))

        # Валидация Даты рождения ребенка
        birth_border = (
            datetime.date(today.year - MAX_AGE, today.month, today.day))
        if birth and birth <= birth_border:
            raise ValidationError(_Message.OLD)

        # Проверка, что все указанные организации есть в базе данных
        organizations = self.application_type.EduOrganizations.EduOrganization
        try:
            units_ids_set = {int(unit.code) for unit in organizations}
        except ValueError:
            raise ValidationError('Указаны некорректные коды организаций')
        units_ids_in_db = Unit.objects.filter(id__in=units_ids_set).values_list(
            'id', flat=True)
        not_existed_units_ids = units_ids_set - set(units_ids_in_db)
        if not_existed_units_ids:
            message = _Message.UNIT_NOT_EXISTS.format(
                ','.join(str(unit_id) for unit_id in not_existed_units_ids))
            raise ValidationError(message)

    def get_declaration_by_order_id(self) -> Declaration | None:
        """Возвращает заявление по идентификатору (order_id).

        :return: Существующего заявление.

        """

        _order_id = self.application_type.orderId

        # Доп. подзапросы на получение необходимых данных для
        # последующей проверки изменений
        declaration_query = (
            Declaration.objects.select_related(
                'children', 'status'
            ).prefetch_related(
                Prefetch(
                    'children__childrendelegate_set',
                    queryset=(
                        ChildrenDelegate.objects.filter(
                            extendedchildrendelegate__order_id=_order_id
                        ).select_related(
                            'delegate', 'delegate__delegatecontingent'
                        )),
                    to_attr='children_delegate')))

        declaration, _ = get_declaration_by_client_or_portal_id(
            declaration_query, _order_id)

        return declaration

    @staticmethod
    def get_comment_duplicates(
            declarations: tuple[list[int | datetime.date | str], ...]
    ) -> str:
        """Возвращает комментарий с информацией по найденным заявкам.

        Определены свои сообщения для Регионов
        (для случая, когда дубль заявления один): Мурманск, Владимир.
        Когда дублей заявления найдено более одного то формируется общее
        сообщение для всех Регионов.

        :param declarations: Информация по найденным заявкам.

        :return: Комментарий о дублях заявления.

        """

        # Формирует общее сообщение.
        _get_common_comment = (
            lambda _id, _date, _status:
                f' (Идентификатор "{_id}"; '
                f'Дата подачи "{date_to_str(_date)}"; Статус "{_status}").')

        if len(declarations) == 1:

            _id, _date, _status, *_child_fio = declarations[0]

            if REGION_CODE == RegionCode.MURMANSK:
                return (
                    _Message.MULTIPLE.format(
                        make_full_name(*_child_fio), _id,  date_to_str(_date)))

            if REGION_CODE == RegionCode.VLADIMIR:
                return (
                    _Message.MULTIPLE.format(_id, date_to_str(_date), _status))

            return _Message.MULTIPLE.format(
                _get_common_comment(_id, _date, _status))

        comment = (
            '\n'.join(
                f'{num}.{_get_common_comment(_id, _date, _status_name)}'
                for num, (_id, _date, _status_name, *_) in (
                    enumerate(declarations, start=1))))

        if REGION_CODE in (RegionCode.MURMANSK, RegionCode.VLADIMIR):
            return _Message.__base__.MULTIPLE.format(f':\n{comment}\n')

        return _Message.MULTIPLE.format(f':\n{comment}\n')

    def find_existing_children(self) -> QuerySet:
        """Поиск существующего ребенка.

        Выполняет поиск ребенка по след. критериям:
            1. ФИО (Не учитывается регистр);
            2. Дата рождения;
            3. Документ подтверждающий личность (Серия, Номер и Тип документа).

        :return: Выборка детей по заданным в заявлении параметрам.

        """

        child_info = self.application_type.ChildInfo

        base_filter = (
                Q(surname__iexact=child_info.ChildSurname)
                & Q(firstname__iexact=child_info.ChildName)
                & Q(patronymic__iexact=child_info.ChildMiddleName)
                & Q(date_of_birth=child_info.ChildBirthDate))

        if child_info.ChildBirthDocRF:
            birth_doc = child_info.ChildBirthDocRF
            dul_series, dul_number = Children.dul_auto_lookup(
                birth_doc.ChildBirthDocSeries,
                birth_doc.ChildBirthDocNumber,
                DULTypeEnumerate.SVID)
            base_filter &= (
                Q(dul_series=dul_series)
                & Q(dul_number=dul_number)
                & Q(dul_type=DULTypeEnumerate.SVID))

        elif child_info.ChildBirthDocForeign:
            birth_doc_foreign = child_info.ChildBirthDocForeign
            base_filter &= (
                Q(dul_number=birth_doc_foreign.ChildBirthDocNumber)
                & ~Q(dul_type=DULTypeEnumerate.SVID))

            if birth_doc_foreign.ChildBirthDocSeries:
                base_filter &= Q(
                    dul_series=birth_doc_foreign.ChildBirthDocSeries)

        elif hasattr(child_info, 'ChildBirthAct'):
            base_filter &= Q(
                dul_type=DULTypeEnumerate.OTHER,
                zags_act_number=child_info.ChildBirthAct.ChildBirthDocActNumber,
            )
            if child_info.ChildBirthAct.ChildBirthDocActDate:
                base_filter &= Q(zags_act_date=child_info.ChildBirthAct.ChildBirthDocActDate)
            if child_info.ChildBirthAct.ChildActBirthDocIssued:
                base_filter &= Q(zags_act_place=child_info.ChildBirthAct.ChildActBirthDocIssued)

        existing_children = Children.objects.filter(base_filter)

        return existing_children

    def create_declaration(self) -> ApplicationManagerData:
        """Создает новое заявление.

        :return: Ответ
        """

        existing_children = self.find_existing_children()

        existing_child = existing_children.order_by('id').last()

        try:
            declaration = Application(
                self.application_type, self.message.attachments
            ).create(existing_child)
        except ValidationError as e:
            logger.error(
                f'{_Message.DATA_ERROR} ApplicationRequest '
                f'({"; ".join(e.messages)})')
            return ApplicationManagerData(
                order_id=self.application_type.orderId,
                org_code=_Message.values[_Message.DATA_ERROR],
                tech_code=StatusTechCode.CODE_4.value,
                comment=_Message.DATA_ERROR)

        DeclarationOriginMessageID.objects.get_or_create(
            declaration_id=declaration.id,
            defaults={
                'message_id': self.message.origin_message_id,
                'replay_to': self.message.replay_to
            })

        return ApplicationManagerData(
            order_id=self.application_type.orderId,
            org_code=_Message.values[_Message.SUCCESS],
            tech_code=StatusTechCode.CODE_1.value,
            comment=DECLARATION_RECEIVED_COMMENT.format(
                date=declaration.date.strftime(settings.DATE_FORMAT),
                declaration_client_id=declaration.client_id,
            ),
        )

    def update_declaration(
            self, declaration: Declaration
    ) -> ApplicationManagerData:
        """Фиксирует изменения заявления.

        :return: Ответ.

        """

        change_map = Smev3ChangesMap()

        # Выполняет проверку изменений Желаемых ДОО
        unit_helper = Smev3DeclarationUnitChangeHelper(
            DeclarationUnit, 'DeclarationUnit')
        unit_helper.check_diff(self.application_type, declaration)

        # Выполняет проверку изменений Льгот
        benefits_helper = Smev3DeclarationPrivilegeChangeHelper(
            DeclarationPrivilege, 'DeclarationPrivilege')
        benefits_helper.check_diff(self.application_type, declaration)

        # Выполняет проверку изменений ребенка
        children_helper = Smev3ChildrenChangeHelper(
            Children, 'Children')
        children_helper.check_diff(self.application_type, declaration.children)

        helpers = [
            unit_helper,
            benefits_helper,
            children_helper
        ]

        check_diff = [
            (Declaration, 'Declaration', declaration)
        ]

        children_delegate, *_ = (
                declaration.children.children_delegate or (None,))
        if children_delegate is not None:
            delegate_helper = Smev3DelegateChangeHelper(Delegate, 'Delegate')
            delegate_helper.check_diff(self.application_type, children_delegate.delegate)
            helpers.append(delegate_helper)

        for model, model_name, instance in check_diff:
            helper = Smev3ChangeHelper(
                model, model_name, map_changes=change_map)
            helper.check_diff(self.application_type, instance)
            helpers.append(helper)

        if self.message.attachments:
            helper = Smev3DeclarationDocsChangeHelper(DocExtraInfo)
            helper.check_diff(declaration, self.message.attachments)
            helpers.append(helper)

        updated = (
            Smev3StorageHelper.create_change(
                declaration, helpers, source=ChangeSource.UPDATE_APPLICATION))

        if not updated:
            return ApplicationManagerData(
                order_id=self.application_type.orderId,
                org_code=_Message.values[_Message.NO_CHANGES],
                tech_code=StatusTechCode.CODE_4.value,
                comment=_Message.NO_CHANGES)

        changes = Smev3StorageHelper.get_change(updated)
        transaction.on_commit(
            lambda: PushChangeOrderInfoRequestTask().apply_async(
                (declaration.id,
                 CHANGE_DECLARATION_CODE,
                 CHANGE_DECLARATION_COMMENT.format(
                     changes=changes_to_str(changes)),
                 self.message.origin_message_id,
                 self.message.replay_to)))

        try:
            order_request = declaration.orderrequest
        except OrderRequest.DoesNotExist:
            order_request = None

        # Передается запрос OrderRequest с блоком UpdateOrderRequest
        # со статусом "Изменение заявление" в ЕПГУ
        if order_request:
            DispatchOrderRequestSMEV3RequestManager(
                order_request, PendingUpdateOrderRequestSourceVersionEnum.V_1,
                {
                    'declaration_id': declaration.id,
                    'event': DECLARATION_CHANGED,
                    'declaration_changes_rows': changes
                }).run()

        return ApplicationManagerData(
            order_id=self.application_type.orderId,
            org_code=_Message.values[_Message.CHANGES_SUCCESS],
            tech_code=StatusTechCode.CODE_1.value,
            comment=_Message.CHANGES_SUCCESS)

    def update_house_guid_if_empty(self) -> None:
        """Если код ГАР дома не указан, производится попытка найти его
        по коду ГАР улицы, номеру дома и строению.

        """

        address = self.application_type.Address
        address_street_code = get_gar_code(address.Street.code)
        address_house = address.House.valueOf_

        if not address.House.code and (address_street_code and address_house):
            corps = str(address.Building1 or '')
            structure = str(address.Building2 or '')
            house = find_house(
                address_street_code, address_house, corps, structure)
            if not house and structure:
                # Строение может быть указано через "/" (например, 17В/3)
                house = find_house(
                    address_street_code, f'{address_house}{corps}/{structure}')
            if house:
                address.House.code = house.guid

    def check_no_active_declarations(self) -> ApplicationManagerData | None:
        """Проверяет наличие дубликатов заявок в активном статусе
        и возвращает сообщение об этом.

        """

        existing_children = self.find_existing_children()

        no_active_without_didnt_come = ExtensionManager().execute(
            'kinder.plugins.didnt_come_declaration_status_check.extensions.'
            'no_active_without_didnt_come')
        # Неактивные статусы
        # (при наличии плагина "Не явился" не считается неактивным).
        no_active_statuses = (
                no_active_without_didnt_come or DSS.no_active_statuses())

        # Базовый список выбираемых данных для сообщения о дубликатах.
        _values_list = ('id', 'date', 'status__name')
        if REGION_CODE == RegionCode.MURMANSK:
            _values_list += (
                'children__surname', 'children__firstname',
                'children__patronymic')

        declarations = tuple(
            Declaration.objects.filter(
                children__in=existing_children
            ).exclude(
                status__code__in=no_active_statuses,
            ).values_list(*_values_list).order_by('-date'))

        if not declarations:
            return

        # Формирует ответ с сообщением о существовании дубля в системе.
        comment = ExtensionManager().execute(
            'kinder.plugins.didnt_come_declaration_status_check.extensions.'
            'make_didnt_come_application_request_comment', self, declarations)

        if comment is None:
            comment = self.get_comment_duplicates(declarations)

        return ApplicationManagerData(
            order_id=self.application_type.orderId,
            org_code=_Message.values[_Message.MULTIPLE],
            tech_code=StatusTechCode.CODE_4.value,
            comment=comment)

    def run(self) -> ApplicationManagerData:
        """Запускает процесс разбора полученных данных.

        :return: Ответ

        """

        try:
            self.validate()
        except ValidationError as e:
            logger.error(
                f'{_Message.DATA_ERROR} ApplicationRequest '
                f'({"; ".join(e.messages)})')
            return ApplicationManagerData(
                order_id=self.application_type.orderId,
                org_code=_Message.ORG_CODE_150,
                tech_code=StatusTechCode.CODE_4.value,
                comment='; '.join(e.messages))

        self.update_house_guid_if_empty()
        declaration = self.get_declaration_by_order_id()
        if declaration:
            if declaration.status.code in DSS.no_active_statuses():
                return ApplicationManagerData(
                    order_id=self.application_type.orderId,
                    org_code=DECLARATION_CHANGES_REFUSED_CODE,
                    tech_code=StatusTechCode.CODE_4.value,
                    comment=DECLARATION_CHANGES_REFUSED_COMMENT.format(
                        comment=DECLARATION_CHANGES_REFUSED_REASON)
                )

            return self.update_declaration(declaration)

        no_active_declarations_result = self.check_no_active_declarations()

        if no_active_declarations_result:
            return no_active_declarations_result

        return self.create_declaration()
