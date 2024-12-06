from __future__ import annotations

from io import StringIO
from typing import TYPE_CHECKING
import re

from kinder.core.children.models import DelegateTypeEnumerate
from kinder.core.declaration.models import Declaration
from kinder.core.declaration_status.enum import DSS
from kinder.core.dict.models import DULTypeEnumerate
from kinder.core.dict.models import GroupSpec
from kinder.core.dict.models import GroupTypeEnumerate
from kinder.core.helpers import format_phone
from kinder.core.unit.models import Unit
from kinder.core.unit.models import UnitKind
from kinder.core.utils.address import get_address_dict
from kinder.core.utils.address import name_from_guid

from concentrator import settings

from .rules import DULDelegateTypeRule
from .rules import GroupTypeRule
from .rules import GroupTypeWithoutHealthNeedRule
from .rules import HealthNeedRule
from .rules import WorkTypeRule


if TYPE_CHECKING:

    try:
        from typing import TypedDict
    except ImportError:
        from typing_extensions import TypedDict

    from kinder.core.children.models import Children
    from kinder.core.children.models import DULDelegateType
    from kinder.core.declaration.models import DeclarationStatus
    from kinder.core.dict.models import GroupType
    from kinder.core.dict.models import HealthNeed
    from kinder.core.dict.models import WorkType


    class DataElementType(TypedDict, total=False):
        """Словарь данных для блока DataElementType."""

        code: str
        valueOf_: str | None


def is_cancel_allowed(status: DeclarationStatus) -> bool:
    """Проверяет разрешена ли отмена заявления в указанном статусе.

    :param status: Статус заявления.

    :return: Разрешена ли отмена.

    """

    if status.code in list(DSS.values.keys()):
        if getattr(settings, status.code.upper(), False):
            return True
    elif settings.OTHER_STATUS:
        return True

    return False


def get_oktmo_region() -> str | None:
    """Возвращает ОКТМО головного учреждения.

    :return: октмо или None

    """

    region = Unit.objects.filter(kind=UnitKind.REGION).last()

    return region.octmo if region else None


def get_identity_doc_name(dul_type: DULDelegateType) -> DataElementType:
    """Возвращает данные для блока IdentityDocName.

    :param dul_type: Тип документа представителя

    :return: словарь с данными.

    """

    if dul_type:

        if dul_type.esnsi_code:
            identity_doc_name_params = {
                'code': dul_type.esnsi_code, 'valueOf_': dul_type.name
            }
        else:
            code, value = (
                DULDelegateTypeRule.get_service_list(
                    int(dul_type.code), ('', None)))
            identity_doc_name_params = {'code': code, 'valueOf_': value}
    else:
        identity_doc_name_params = {'code': '', 'valueOf_': None}

    return identity_doc_name_params


def get_adaptation_group_type(
        health_need: HealthNeed, desired_group_type_code: str
) -> DataElementType:
    """Возвращает данные для блока AdaptationGroupType.

    :param health_need: Специфика группы
    :param desired_group_type_code: Код направленности группы

    :return: словарь с данными.

    """

    adaptation_group_type_params = {}
    if health_need:
        if health_need.esnsi_code:

            adaptation_group_type_params = {
                'code': health_need.esnsi_code,
                'valueOf_': health_need.name
            }
        else:
            code, value = (
                HealthNeedRule.get_service(
                    (health_need.code, desired_group_type_code), (None, None)))
            if not all([code, value]):
                code, value = GroupTypeWithoutHealthNeedRule.get_service(
                    desired_group_type_code, (None, None))
            if code and value:
                adaptation_group_type_params = {
                    'code': code, 'valueOf_': value
                }

    return adaptation_group_type_params


def get_adaptation_group(desired_group_type: GroupType) -> DataElementType:
    """Возвращает данные для блока AdaptationGroup.

    :param desired_group_type: Направленность группы

    :return: словарь с данными.

    """

    if desired_group_type:

        if desired_group_type.esnsi_code:

            adaptation_group_params = {
                'code': desired_group_type.esnsi_code,
                'valueOf_': desired_group_type.name
            }
        else:
            code, value = (
                GroupTypeRule.get_service_list(
                    desired_group_type.code, ('', None)))
            adaptation_group_params = {'code': code, 'valueOf_': value}

    else:
        adaptation_group_params = {'code': '', 'valueOf_': None}

    return adaptation_group_params


def get_schedule(work_type: WorkType) -> DataElementType:
    """Возвращает данные для блока Schedule.

    :param work_type: Режим работы

    :return: словарь с данными.

    """

    if work_type:
        if work_type.esnsi_code:

            schedule_params = {
                'code': work_type.esnsi_code, 'valueOf_': work_type.name
            }
        else:
            code, value = (
                WorkTypeRule.get_service_list(work_type.code, ('', None)))
            schedule_params = {'code': code, 'valueOf_': value}
    else:
        schedule_params = {'code': '', 'valueOf_': None}

    return schedule_params


def get_language(spec: GroupSpec) -> DataElementType:
    """Возвращает данные для блока Language.

    :param spec: Язык обучения

    :return: словарь с данными.

    """

    if spec and spec.code != GroupSpec.DEFAULT_CODE:
        language_params = {
            'code': spec.esnsi_code,
            'valueOf_': spec.name
        }
    else:
        language_code, language_value = (
            GroupSpec.objects.filter(
                code=GroupSpec.RUS
            ).values_list('esnsi_code', 'name').first() or ('', None))
        language_params = {
            'code': language_code,
            'valueOf_': language_value
        }

    return language_params


def get_medical_report(child: Children) -> DataElementType:
    """Возвращает данные для блока DocName (MedicalReport).

    :param child: Ребенок

    :return: словарь с данными.

    """

    medical_report_params = {'code': '', 'valueOf_': None}

    if child.health_need_confirmation:
        medical_report_params.update({
            'code': child.health_need_confirmation.esnsi_code,
            'valueOf_': child.health_need_confirmation.name
        })

    return medical_report_params


def get_person_info(schema, delegate):
    """Формирует и возвращает блок данных "Сведения о заявителе".

    :param schema: Инстанс генератора
    :param delegate: Представитель
    :type delegate: Delegate
    :return: Блок данных "Сведения о заявителе"
    :rtype: PersonInfoType
    """

    parents = delegate.type in DelegateTypeEnumerate.PARENTS

    person_info_params = {
        'PersonSurname': delegate.surname,
        'PersonName': delegate.firstname,
        'PersonPhone': format_phone(
            delegate.phones or delegate.phone_for_sms) or '-',
        'PersonEmail': delegate.email or '-',
        'Parents': parents,
    }

    if delegate.patronymic:
        person_info_params['PersonMiddleName'] = delegate.patronymic

    delegate_contingent = getattr(delegate, 'delegatecontingent', None)
    if not parents and delegate_contingent:
        other_representative_params = {
            'OtherRepresentativeDocName':
                delegate_contingent.doc_description,
            'OtherRepresentativeDocNumber': delegate_contingent.number,
            'OtherRepresentativeDocDate': delegate_contingent.date_issue,
            'OtherRepresentativeDocIssued': delegate_contingent.issued_by
        }

        if delegate_contingent.series:
            other_representative_params['OtherRepresentativeDocSeries'] = (
                delegate_contingent.series)

        person_info_params['OtherRepresentative'] = (
            schema.OtherRepresentativeType(**other_representative_params))

    return schema.PersonInfoType(**person_info_params)


def get_person_identity_doc_info(schema, delegate, declaration):
    """Формирует и возвращает блок данных "Паспортные данные заявителя".

    :param schema: Инстанс генератора
    :param delegate: Представитель
    :type delegate: Delegate
    :param declaration: Заявление
    :type declaration: Declaration
    :return: Блок данных "Паспортные данные заявителя"
    :rtype: PersonIdentityDocInfoType
    """

    person_identity_doc_info_params = {
        'IdentityDocName':
            schema.DataElementType(**get_identity_doc_name(delegate.dul_type)),
        'IdentityDocNumber':
            '' if delegate.dul_number is None else delegate.dul_number[:10],
        'IdentityDocIssueDate': delegate.dul_date or declaration.date.date(),
        'IdentityDocIssued': delegate.dul_issued_by or ''
    }

    if delegate.dul_series:
        person_identity_doc_info_params['IdentityDocSeries'] = (
            delegate.dul_series[:10])

    if delegate.dul_place:
        # в ответе в IdentityDocIssueCode нужны только цифры
        person_identity_doc_info_params['IdentityDocIssueCode'] = re.sub(
            "[^0-9]", "", delegate.dul_place)[:6]

    return schema.PersonIdentityDocInfoType(**person_identity_doc_info_params)


def get_adaptation_program(schema, declaration):
    """Формирует и возвращает блок данных "Направленность группы".

    :param schema: Инстанс генератора
    :param declaration: Заявление
    :type declaration: Declaration
    :return: Блок данных "Направленность группы"
    :rtype: AdaptationProgramType
    """

    child = declaration.children

    adaptation_program_params = {}

    # Блок AdaptationGroupType передается только в случае, если все
    # данные заполнены (Специфика и Желаемая направленность группы
    # при зачислении) и Желаемая направленность группы при зачислении
    # не Общеразвивающая.
    if (
            child.health_need and declaration.desired_group_type
            and declaration.desired_group_type.code != GroupTypeEnumerate.DEV
    ):
        adaptation_program_params['AdaptationGroupType'] = (
            schema.DataElementType(
                **get_adaptation_group_type(
                    child.health_need, declaration.desired_group_type.code)))

    adaptation_program_params['AgreementAdaptationEducationGroup'] = (
        declaration.adapted_program_consent)

    adaptation_program = schema.AdaptationProgramType(
        AdaptationGroup=schema.DataElementType(
            **get_adaptation_group(declaration.desired_group_type)),
        AgreementOnGeneralGroup=declaration.consent_dev_group,
        AgreementOnCareGroup=declaration.consent_care_group,
        NeedSpecialCareConditions=child.health_need_special_support,
        **adaptation_program_params)

    return adaptation_program


def get_address(schema, child):
    """Формирует и возвращает блок данных "Адрес".

    :param schema: Инстанс генератора
    :param child: Ребенок
    :type child: Children
    :return: Блок данных "Адрес"
    :rtype: AddressType
    """

    address_dict = get_address_dict(
        child.address_place, child.address_street, child.address_house_guid)

    address_params = {
        'FullAddress': child.address_full or '',
        'Index': address_dict.get('postal_code', '') or '',
        'Building1': child.address_corps or '',
        'Building2': address_dict.get('structure_number', '') or '',
        'Apartment': child.address_flat or ''
    }

    region_params = {
        'code': child.address_place or '',
        'valueOf_': address_dict.get('place_name', '')
    }

    area_params = city_params = place_params = {
        'code': child.address_place or '',
        'valueOf_': name_from_guid(child.address_place)
    }

    street_params = {
        'code': child.address_street or '',
        'valueOf_': address_dict.get('street_name', '')
    }

    house_params = {
        'code': child.address_house_guid or '',
        'valueOf_': address_dict.get('house_number', child.address_house) or '',
    }

    city_area = additional_area = additional_street = {
        'code': '', 'valueOf_': None
    }

    address_type = schema.AddressType(
        Region=schema.DataElementType(**region_params),
        Area=schema.DataElementType(**area_params),
        City=schema.DataElementType(**city_params),
        CityArea=schema.DataElementType(**city_area),
        Place=schema.DataElementType(**place_params),
        Street=schema.DataElementType(**street_params),
        AdditionalArea=schema.DataElementType(**additional_area),
        AdditionalStreet=schema.DataElementType(**additional_street),
        House=schema.DataElementType(**house_params),
        **address_params)

    return address_type


def get_medical_report_without_files(schema, declaration):
    """Формирует и возвращает блок данных "Реквизиты документа,
    подтверждающего группу коменсирующей направленности".

    :param schema: Инстанс генератора
    :param declaration: Заявление
    :type declaration: Declaration
    :return: Блок данных "Реквизиты документа, подтверждающего группу
    коменсирующей направленности"
    :rtype: Optional[MedicalReportWithoutFilesType]
    """

    child = declaration.children

    # Обязательные поля для передачи.
    required_fields = (
        child.health_need_confirmation, child.health_number,
        child.health_need_start_date, child.health_issued_by)

    # Если хотя бы одно обязательное поле заполнено в системе,
    # то блок (MedicalReportWithoutFilesType) будет передан.
    if not any(required_fields):
        return None

    medical_report_params = {}

    if child.health_series:
        medical_report_params['DocSeries'] = child.health_series

    if child.health_need_expiration_date:
        medical_report_params['DocExpirationDate'] = (
            child.health_need_expiration_date)

    # Если Дата выдачи документа подтверждающего специфику не заполнена,
    # то заполняет датой подачи заявление (
    # временный костыль, т.к. она скоро станет обязательной)
    medical_report_type = schema.MedicalReportWithoutFilesType(
        DocName=schema.DataElementType(**get_medical_report(child)),
        DocNumber=child.health_number or '',
        DocIssueDate=child.health_need_start_date or declaration.date.date(),
        DocIssued=child.health_issued_by or '', **medical_report_params)

    return medical_report_type


def get_child_info(schema, declaration):
    """Формирует и возвращает блок данных "Сведения о ребёнке".

    :param schema: Инстанс генератора
    :param declaration: Заявление
    :type declaration: Declaration
    :return: Блок данных "Сведения о ребёнке"
    :rtype: ChildInfoType
    """

    child = declaration.children
    declaration_date = declaration.date.date()

    # Значение по умолчанию для тэга ChildBirthDocIssued, если
    # Место государственной регистрации (отдел ЗАГС) не заполнено.
    child_birth_doc_issued_default = 'не указано'

    # Если тип документа ребенка Свидетельство о рождении,
    # то формирует блок документов типа ChildBirthDocRFType,
    # иначе ChildBirthDocForeignType.
    if child.dul_type == DULTypeEnumerate.SVID:
        # Если Дата создания актовой записи не заполнена,
        # то заполняет датой подачи заявления.
        child_doc_data = {
            'ChildBirthDocRF': schema.ChildBirthDocRFType(
                ChildBirthDocSeries=child.dul_series,
                ChildBirthDocNumber=child.dul_number,
                ChildBirthDocIssueDate=child.dul_date or declaration_date,
                ChildBirthDocActNumber=child.zags_act_number,
                ChildBirthDocActDate=child.zags_act_date or declaration_date,
                ChildBirthDocIssued=(
                    child.zags_act_place or child_birth_doc_issued_default))
        }
    elif hasattr(schema, 'ChildBirthActType') and child.dul_type == DULTypeEnumerate.OTHER:
        child_doc_data = {
            'ChildBirthAct': schema.ChildBirthActType(
                ChildBirthDocActNumber=child.zags_act_number,
                ChildBirthDocActDate=child.zags_act_date,
                ChildActBirthDocIssued=child.zags_act_place
            )
        }
    else:
        child_doc_data = {
            'ChildBirthDocForeign': schema.ChildBirthDocForeignType(
                ChildBirthDocName=(
                    child.document_type
                    or DULTypeEnumerate.values.get(child.dul_type)),
                ChildBirthDocSeries=child.dul_series,
                ChildBirthDocNumber=child.dul_number,
                ChildBirthDocIssueDate=child.dul_date or declaration_date,
                ChildBirthDocIssued=(
                    child.zags_act_place or child_birth_doc_issued_default))
        }

    child_info_type = schema.ChildInfoType(
        ChildSurname=child.surname,
        ChildName=child.firstname,
        ChildMiddleName=child.patronymic,
        ChildBirthDate=child.date_of_birth, **child_doc_data)

    return child_info_type


def render_type2xml(type_, name_type, pretty_print=False):
    """Рендерит классы в xml.

    :param type_: инстанс типа
    :param name_type: наименование типа
    :param pretty_print: признак "красивого" вывода в xml
    :return: сформированный xml
    """

    buffer = StringIO()
    type_.export(
        buffer, 0, name_=name_type, pretty_print=pretty_print)

    return buffer.getvalue()
