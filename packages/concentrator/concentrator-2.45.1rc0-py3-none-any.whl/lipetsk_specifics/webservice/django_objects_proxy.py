from itertools import groupby
from operator import attrgetter

from django.db.models import Q
from kinder.core.children.models import Children
from kinder.core.children.models import ChildrenDelegate
from kinder.core.children.models import Delegate
from kinder.core.children.models import DelegateNotificationType
from kinder.core.children.models import DelegateTypeEnumerate
from kinder.core.children.models import DULTypeEnumerate
from kinder.core.declaration.models import DeclarationUnit
from kinder.core.dict.models import HealthNeed
from kinder.core.dict.models import UnitKind
from kinder.core.helpers import recursive_getattr
from kinder.core.privilege.models import Privilege
from kinder.core.unit.models import Unit
from kinder.plugins.privilege_attributes.models import (
    PrivilegeConfirmationAttributes)
from kinder.plugins.privilege_attributes.models import PrivilegeOwnerEnum
from kinder.webservice.spyne_ws.exceptions import SpyneException
from kinder.webservice.spyne_ws.exceptions import StatusSpyneException

from concentrator.constants import DELIMITER_PRIV
from concentrator.constants import MUNICIPAL_TYPE
from concentrator.models import DocExtraInfo
from lipetsk_specifics.rules import DelegateDocTypeRule
from lipetsk_specifics.rules import DelegateTypeRule
from lipetsk_specifics.rules import SexTypeRule

from .helpers import get_declaration_units
from .helpers import get_delegate


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
        try:
            if benefit_type == MUNICIPAL_TYPE and DELIMITER_PRIV in benefit:
                # идентификатор муниципальных льготы составной, см LoadData,
                # id льготы, разделитель, id льготы в МО
                benefit = benefit.split(DELIMITER_PRIV)[0]
            privilege = Privilege.objects.get(id=benefit)
        except Privilege.DoesNotExist:
            raise SpyneException(u'Льгота не найдена')

        return privilege

    def get(self):

        privileges = []

        for benefit, benefit_type in self._benefits:

            privileges.append(
                PrivilegeProxy._get_benefit(
                    (benefit, benefit_type)))

        return privileges


class LipetskDelegateProxy:
    """
    добавили сохранение AddressResidence AddressRegistration
    """

    def __init__(self, delegate):
        """
        delegate - Spyne ApplicantData instance
        """
        self._delegate = delegate

    def _get_doc_type(self):
        return DelegateDocTypeRule.get_system(self._delegate.DocType)

    def _get_delegate_type(self):
        return DelegateTypeRule.get_system(self._delegate.ApplicantType)

    def get(self):
        delegate = Delegate(
            firstname=self._delegate.FirstName,
            surname=self._delegate.LastName,
            patronymic=self._delegate.MiddleName,
            snils=self._delegate.Snils,
            dul_type_id=self._get_doc_type(),
            dul_series=self._delegate.DocSeria,
            dul_number=self._delegate.DocNumber,
            dul_date=self._delegate.DocIssueDate,
            dul_place=self._delegate.DocIssuerDepartmentCode,
            dul_issued_by=self._delegate.DocIssuerName,
            type=self._get_delegate_type(),
            email=self._delegate.Email,
            phones=self._delegate.PhoneNumber,
            address_full=self._delegate.AddressResidence,
            reg_address_full=self._delegate.AddressRegistration,
            notification_type=(DelegateNotificationType.EMAIL
                               if self._delegate.Email
                               else DelegateNotificationType.NONE)
        )

        return delegate


class DelegatePrivilegeProxy:
    u"""Прокси класс для работы с обладателем льготы"""

    # поля по которым ищется заявитель для метода get_founded_or_new
    tracked_fields = [
        'firstname', 'surname', 'patronymic',
        'dul_type_id', 'dul_series', 'dul_number']

    def __init__(self, delegate):
        """delegate - Spyne ApplicantData instance"""
        self._delegate = delegate

    @classmethod
    def _get_type(cls):
        """Возвращаем всегда Зак.представителя, т.к. в этот прокси класс
        предназначен для обработки только блока WhoHaveBenefit, через который
        мы можем создавать/изменять данные зак.представителя, НО НЕ родителя.
        Возможно логика поменяется."""
        return DelegateTypeEnumerate.LEX

    def _get_doc_type(self):
        return DelegateDocTypeRule.get_system(self._delegate.DocType)

    def get(self):
        u"""Возвращаем инстанс delegate по данным из запроса"""
        delegate = Delegate(
            firstname=self._delegate.FirstName,
            surname=self._delegate.LastName,
            patronymic=self._delegate.MiddleName,
            snils=self._delegate.Snils,
            dul_type_id=self._get_doc_type(),
            dul_series=self._delegate.DocSeria,
            dul_number=self._delegate.DocNumber,
            dul_date=self._delegate.DocIssueDate,
            dul_issued_by=self._delegate.DocIssuerName,
            dul_place=self._delegate.DocIssuerDepartmentCode,
            type=self._get_type())

        return delegate

    @classmethod
    def get_founded_or_new(cls, declaration, delegate_proxy):
        """Возвращает delegate найденного по ФИО или Типу, Номеру, Серии ДУЛ,
        либо если такого нет, создает нового Зак.представителя
        и связываем его с ребенком
        :param declaration: заявление
        :param params: словарь с ключами из tracked_fields
        """
        def _get_lookups(params, fields):
            """возвращает словарь с лукапами аналогичный params,
            добавляя префиксы и суффиксы к ключам"""
            items = []
            for field, val in list(params.items()):
                if field in fields:
                    if not field.endswith('_id'):
                        field += '__icontains'
                    items.append(('delegate__{0}'.format(field), val))
            return dict(items)

        # получаем из инстанса словарь с отслеживаемыми полями
        params = dict()
        for field in DelegatePrivilegeProxy.tracked_fields:
            val = recursive_getattr(delegate_proxy, field)
            if val:
                params[field] = val

        # фильтр по ФИО или данным ДУЛ
        fio_or_dul_flt = (
            Q(**_get_lookups(params, cls.tracked_fields[:3])) |
            Q(**_get_lookups(params, cls.tracked_fields[3:])))

        delegates = declaration.children.childrendelegate_set.filter(
            fio_or_dul_flt).select_related('delegate')

        # получаем инстанс найденной модели или создаем новый
        if delegates:
            delegate = delegates[0].delegate
        else:
            delegate = delegate_proxy
            delegate.type = cls._get_type()
            delegate.save()
            ChildrenDelegate.objects.create(
                children_id=declaration.children_id,
                delegate_id=delegate.id)

        return delegate

    @classmethod
    def get_from_diff(cls, difference):
        u"""Возвращаем инстанс delegate по данным из difference.
        Пока непонятно как инкапсулировать обработку
        диффки в классе, где она создается, поэтому обрабатываем здесь"""
        params = dict()
        for obj in difference:
            field, (_, new_val, old_val) = list(obj.items())[0]
            if 'delegate.' in field:
                field = field.replace('delegate.', '')
                # для полей которые необходимо сериализовать, но они пока
                # не нужны. если понадобятся использовать convert_value.
                if field in ['dul_date']:
                    continue
                # для полей fk приходится добавлять суффикс "_id"
                if field in ['dul_type']:
                    field = '{0}_id'.format(field)
                params[field] = new_val

        return Delegate(**params)

    @classmethod
    def get_fake_delegate(self, children):
        """Возвращается фейковый инстанс delegate по данным ребенка,
        для создания диффки с данными о смене обладателя льготы"""
        return Delegate(
            firstname=children.firstname,
            surname=children.surname,
            patronymic=children.patronymic,
            snils=children.snils,
            dul_type_id=children.dul_type,
            dul_series=children.dul_series,
            dul_number=children.dul_number,
            dul_place=children.zags_act_place,
            dul_issued_by=children.zags_act_number,
            dul_date=children.dul_date)


class LipetskChildrenProxy:
    """
        добавили сохранение DateOfActNumber
    """

    def __init__(self, children, delegate, health_need):
        """
        children - Spyne DeclaredPersonData instance
        delegate - Spyne ApplicantData instance
        """

        self._delegate = delegate
        self._children = children
        self._health_need = health_need

    def _get_health_need(self):
        health_need = None
        if self._health_need:
            try:
                health_need = HealthNeed.objects.get(
                    id=self._health_need)
            except HealthNeed.DoesNotExist:
                raise SpyneException(u'Потребность по здоровью не найдена')

        return health_need

    def _get_sex(self):
        return SexTypeRule.get_system(self._children.Sex)

    def get(self):
        return Children(
            firstname=self._children.FirstName,
            surname=self._children.LastName,
            patronymic=self._children.MiddleName,
            snils=self._children.Snils,
            address_full=self._children.AddressResidence,
            reg_address_full=self._children.AddressRegistration,
            dul_type=DULTypeEnumerate.SVID,
            dul_series=self._children.BirthDocSeria,
            dul_number=self._children.BirthDocNumber,
            dul_date=self._children.BirthDocIssueDate,
            gender=self._get_sex(),
            date_of_birth=self._children.DateOfBirth,
            health_need=self._get_health_need(),
            zags_act_number=self._children.BirthDocActNumber,
            zags_act_place=self._children.BirthDocIssuer,
            birthplace=self._children.BirthPlace,
            zags_act_date=self._children.DateOfActNumber)


class PrivConfirmAttrsProxy:
    u"""Прокси класс для работы с доп.аттрибутами льготы (фича Липецка)."""

    def __init__(self, child_data, declaration, declaration_privilege):
        """
        :param child_data: spyne-модель информации о ребенке
        :type child_data: DeclaredPersonData
        :param declaration: заявление django-модель)
        :type declaration: Declaration
        :param declaration_privilege: льгота по заявке (django-модель)
        :type declaration_privilege: DeclarationPrivilege
        """
        self._child_data = child_data
        self.declaration = declaration
        self._delegate = get_delegate(declaration)
        self._declaration_privilege = declaration_privilege
        self.privilege_owner = self._get_privilege_owner()

    def _get_privilege_owner(self):
        u"""Получение значения обладателя льготы из spyne-модели."""
        if self._child_data.Benefits:
            return self._child_data.Benefits.WhoHaveBenefit.Type
        else:
            return None

    def get(self):
        """Данные в теге  WhoHaveBenefit, помимо поля Type,
        приходят только для владельца льгот "Представитель"
        """
        if self.privilege_owner == PrivilegeOwnerEnum.DELEGATE:
            new_delegate = DelegatePrivilegeProxy(
                self._child_data.Benefits.WhoHaveBenefit).get()
            return PrivilegeConfirmationAttributes(
                delegate=new_delegate,
                declaration_privilege=self._declaration_privilege,
                privilege_owner=self.privilege_owner,
                portal=True
            )
        else:
            return PrivilegeConfirmationAttributes(
                delegate=get_delegate(self.declaration),
                declaration_privilege=self._declaration_privilege,
                privilege_owner=self.privilege_owner,
                portal=True
            )


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
                    # Получаем Id Учреждения с концентратора,
                    # которому пользователь хочет проставить
                    # приоритет первый(unit), находим в системе
                    # текущая организации с приоритетом =1 (sys_first_unit_id),
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
                # списке существующих (новая ДОО - приоритетная), то
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
