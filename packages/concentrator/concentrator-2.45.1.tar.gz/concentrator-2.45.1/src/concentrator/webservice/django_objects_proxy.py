from itertools import groupby
from operator import attrgetter

from django.db.models.fields import TextField
from django.db.models.functions import Cast

from m3 import plugins

from kinder.core.children.models import Children
from kinder.core.children.models import Delegate
from kinder.core.children.models import DelegateNotificationType
from kinder.core.children.models import DULTypeEnumerate
from kinder.core.declaration.models import DeclarationUnit
from kinder.core.dict.models import HealthNeed
from kinder.core.dict.models import UnitKind
from kinder.core.dict.models import GroupTypeEnumerate
from kinder.core.dict.models import GroupOrientationDocuments
from kinder.core.privilege.models import Privilege
from kinder.core.unit.models import Unit
from kinder.webservice.spyne_ws.exceptions import StatusSpyneException
from kinder.webservice.spyne_ws.exceptions import SpyneException

from concentrator import settings as concentrator_settings
from concentrator.constants import DELIMITER_PRIV
from concentrator.constants import MUNICIPAL_TYPE
from concentrator.models import DelegatePerson
from concentrator.models import DocExtraInfo
from concentrator.rules import *


class PrivilegeProxy:
    """
    Прокси класс для работы с привилегиями
    """

    def __init__(self, benefits):
        """
        benefits - list of Spyne Benefit instance
        """

        self._benefits = benefits

    @staticmethod
    def _get_benefit(benefit_info):

        benefit, benefit_type = benefit_info
        if benefit_type == MUNICIPAL_TYPE and DELIMITER_PRIV in benefit:
            # идентификатор муниципальных льготы составной, см LoadData,
            # id льготы, разделитель, id льготы в МО
            benefit = benefit.split(DELIMITER_PRIV)[0]

        try:
            privilege = Privilege.objects.annotate(
                id_as_text=Cast('id', output_field=TextField())
            ).get(id_as_text=str(benefit))
        except Privilege.DoesNotExist:
            raise SpyneException(f'Льгота с ID={benefit} не найдена')

        return privilege

    def get(self):

        privileges = []

        for benefit, benefit_type in self._benefits:

            privileges.append(
                PrivilegeProxy._get_benefit(
                    (benefit, benefit_type)))

        return privileges


class ChildrenProxy:
    """Прокси класс для работы с Ребенком."""

    def __init__(self, children, health_need, health_issued_by):
        """
        children - Spyne DeclaredPersonData instance
        """

        self._children = children
        self._health_need = health_need
        self._health_issued_by = health_issued_by
        self._health_need_confirmation = None

    def _get_health_need(self):
        health_need = None
        if self._health_need:
            try:
                health_need = (
                    HealthNeed.objects.annotate(
                        id_as_text=Cast('id', output_field=TextField())
                    ).select_related(
                        'group_type'
                    ).get(id_as_text=str(self._health_need)))
            except HealthNeed.DoesNotExist:
                raise SpyneException(
                    f'Потребность по здоровью с '
                    f'ID={self._health_need} не найдена')

            if (
                    health_need.group_type
                    and health_need.group_type.code in (
                        GroupTypeEnumerate.HEALTH, GroupTypeEnumerate.COMP)
            ):
                try:
                    self._health_need_confirmation = (
                        GroupOrientationDocuments.objects.get(
                            desired_group_type=health_need.group_type))
                except GroupOrientationDocuments.DoesNotExist:
                    raise SpyneException(
                        'Документ, подтверждающий специфику не найден')

        if not health_need or health_need.code == HealthNeed.NO:
            self._health_need_confirmation = None

        return health_need

    def _get_sex(self):
        return SexTypeRule.get_system(self._children.Sex)

    def _get_dul_data(self):
        """Возвращаем данные ДУЛ, заносящиеся в инстанс модели."""

        # С портала информация о ДУЛ приходит либо в 5 тегах, либо в 2.
        # Все теги разные, поэтому завязываемся на отсутствие двух тегов.
        if not (getattr(self._children, 'BirthDocForeign', None) and
                getattr(self._children, 'BirthDocForeignNumber', None)):
            data = dict(
                # всегда свидетельство о рождении
                dul_type=DULTypeEnumerate.SVID,
                dul_series=self._children.BirthDocSeria,
                dul_number=self._children.BirthDocNumber,
                dul_date=self._children.BirthDocIssueDate,
                zags_act_number=self._children.BirthDocActNumber,
                zags_act_place=self._children.BirthDocIssuer,)
        else:
            # Сажаем Тип ДУЛ всегда OTHER, хоть с портала может прийти
            # любое текстовое значение. Остальные поля затираем.
            data = dict(
                dul_type=DULTypeEnumerate.OTHER,
                dul_number=self._children.BirthDocForeignNumber,
                dul_series='',
                dul_date=None,
                zags_act_number='',
                zags_act_place='')
        return data

    def get(self):

        return Children(
            firstname=self._children.FirstName,
            surname=self._children.LastName,
            patronymic=self._children.MiddleName,
            snils=self._children.Snils,
            address_full=self._children.AddressResidence,
            reg_address_full=self._children.AddressRegistration,
            gender=self._get_sex(),
            date_of_birth=self._children.DateOfBirth,
            health_need=self._get_health_need(),
            health_need_confirmation=self._health_need_confirmation,
            health_issued_by=self._health_issued_by,
            birthplace=self._children.BirthPlace, **self._get_dul_data())


class DelegateProxy:
    """Прокси класс для работы с Представителем и Расширением представителя"""

    def __init__(self, delegate):
        """delegate - Spyne ApplicantData instance"""

        self._delegate = delegate

    def _get_doc_type(self):
        delegate_doc_type_rule = plugins.ExtensionManager().execute(
            'kinder.plugins.hmao_services.extensions.'
            'get_delegate_doc_type_rule'
        ) or DelegateDocTypeRule
        return delegate_doc_type_rule.get_system(self._delegate.DocType)

    def _get_delegate_type(self):
        return DelegateTypeRule.get_system(self._delegate.ApplicantType)

    def get(self):
        params = {
            'firstname': self._delegate.FirstName,
            'surname': self._delegate.LastName,
            'patronymic': self._delegate.MiddleName,
            'snils': self._delegate.Snils,
            'dul_type_id': self._get_doc_type(),
            'dul_series': self._delegate.DocSeria,
            'dul_number': self._delegate.DocNumber,
            'dul_date': self._delegate.DocIssueDate,
            'dul_place': self._delegate.DocIssuerDepartmentCode,
            'dul_issued_by': self._delegate.DocIssuerName,
            'type': self._get_delegate_type(),
            'email': self._delegate.Email,
            'phones': self._delegate.PhoneNumber
        }
        if concentrator_settings.SET_NOTIFICATION_TYPE:
            params.update({
                'notification_type': (DelegateNotificationType.EMAIL
                                      if self._delegate.Email else
                                      DelegateNotificationType.NONE)
            })
        delegate = Delegate(**params)

        # инстанцируем распширяющую модель представителя,
        # где храним Тип ДУЛ представителя пришедший с концентратора
        delegate_extension = DelegatePerson(
            delegate=delegate, doc_type=int(self._delegate.DocType)
        )
        return delegate, delegate_extension


class DeclarationUnitProxy:
    """Прокси класс для работы с Желаемыми ДОО."""

    def __init__(self, units, declaration):
        """Инициализация.

        :param units: список организаций
        :type units: List[EduOrganization]
        :param declaration: заявление
        :type declaration: Declaration

        """

        self._declaration = declaration

        # Отбираем только те, у которых задан
        # Code (идентификатор) и Priority (приоритет), остальные игнорируем.
        units = [unit for unit in units if unit.Code and unit.Priority]

        # Проверка приоритетной желаемой ДОО.
        if len([1 for u in units if u.Priority == 1]) > 1:
            raise StatusSpyneException(
                message=(
                    u'Указано более одной приоритетной желаемой организации'),
                status='REJECT')

        # Выполняет выборку уникальных Желаемых ДОО.
        # Если были получены дубли,
        # то будет выбрана организация с наибольшим приоритетом.
        self._units = [
            sorted(group, key=attrgetter('Priority'))[0]
            for _, group in groupby(sorted(units, key=attrgetter('Code')),
                                    key=attrgetter('Code'))
        ]

    @staticmethod
    def _get_unit(spyne_unit):
        try:
            unit_id = int(spyne_unit.Code)
        except UnicodeEncodeError:
            raise SpyneException(u'Неверно передан идентификатор организации.'
                                 u'Проверьте корректность заполнения тега '
                                 u'<Code>')
        try:
            unit = Unit.objects.get(
                id=unit_id, kind__id=UnitKind.DOU)
        except Unit.DoesNotExist:
            raise SpyneException(u'Организация не найдена')

        return unit

    def get_mo(self):
        if not self._units:
            raise SpyneException(u'Не указаны желаемые организации')
        current_mo = None
        for desired_unit in self._units:

            unit = self._get_unit(desired_unit)
            if current_mo and current_mo != unit.get_mo():
                raise SpyneException(u'Все ЖУ должны быть из одного МО')
            else:
                current_mo = unit.get_mo()

        return current_mo

    def get(self):
        from concentrator.webservice.helpers import get_declaration_units
        declaration_units = []
        existing_priorities = []

        # словарь unit_id -> ord, хранящихся в системе
        sys_unit_ord = dict(get_declaration_units(self._declaration))

        # для начала сортируем список организаций:
        # - сначала по возрастанию приоритета из запроса, т.е. 1,2,2,...
        # - потом по возрастанию приоритета из системы. если ДОО новая и
        #     её нет среди желаемых, то проставляем большой приоритет 999
        # - потом по возрастанию Id организации
        self._units.sort(key=lambda u: (
            u.Priority, sys_unit_ord.get(int(u.Code), 999), u.Code))

        # ЖУ с приоритетом 1 обрабатываем однозначно. Остальным ЖУ
        # с приоритетом 2 проставляем приоритеты такие же как в системе,
        # так как по-другому их не возможно определить.
        for desired_unit in self._units:
            unit = self._get_unit(desired_unit)

            if desired_unit.Priority == 1:
                unit_order = desired_unit.Priority

                # только в случае если новая приоритетная ДОО есть среди
                # желаемых, выполняем подмену приоритетов
                if unit.id in sys_unit_ord:
                    tmp_order = sys_unit_ord.get(unit.id)
                    # Получаем Id организации с концентратора,
                    # которому пользователь хочет проставить
                    # приоритет первый(unit), находим в системе
                    # текущая организация с приоритетом =1 (sys_first_unit_id),
                    # и проставляем организации unit приоритет =1,
                    # а организации sys_first_unit_id,
                    # тот приоритет(tmp_order),
                    # который сейчас у организации unit.
                    for sys_first_unit_id, ord in list(sys_unit_ord.items()):
                        if ord == 1:
                            sys_unit_ord.update([(sys_first_unit_id, tmp_order)])
                            break
            else:
                unit_order = sys_unit_ord.get(unit.id, None)

                # если ДОО нет среди текущих желаемых организаций заявки
                # (новая ДОО - неприоритетная) или приоритет уже содержится в
                # списке существующих (новая ДОО - приоритетное), то
                # проставляем его сами по возрастанию id (см. сортировку выше)
                if unit_order is None or unit_order in existing_priorities:
                    if existing_priorities:
                        unit_order = max(existing_priorities) + 1
                    else:
                        unit_order = 1

            # добавляем приоритет в список существующих
            existing_priorities.append(unit_order)

            # в итоге получаем unit_order - приоритетс ЕПГУ
            # по необходимости скорректированный
            declaration_units.append(DeclarationUnit(
                unit=unit, ord=unit_order))

        return declaration_units


class DocExtraInfoProxy:

    def __init__(self, declaration, document_references):

        self._declaration = declaration
        self._document_references = document_references or []

    def save(self):

        for document_reference in self._document_references:

            doc_extra_info = DocExtraInfo(
                declaration=self._declaration,
                code=document_reference.Code)

            if document_reference.Name:
                doc_extra_info.name = document_reference.Name

            if document_reference.Description:
                doc_extra_info.description = document_reference.Description

            doc_extra_info.save()
