from abc import ABC
from abc import abstractmethod
import datetime

from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator
from django.db.models import Q
from objectpack.models import VirtualModel

from kinder import settings as kinder_settings
from kinder.core.declaration.models import Declaration
from kinder.core.declaration_status.models import DSS
from kinder.core.dict.models import *
from kinder.core.emie_unit.models import EmieUnitModel
from kinder.core.privilege.models import Privilege
from kinder.core.privilege.models import PrivilegeInMo
from kinder.core.queue_module.api import get_date_of_birth_range
from kinder.core.unit.models import Unit
from kinder.core.unit.models import UnitStatus

from concentrator import settings
from concentrator.constants import DELIMITER_PRIV
from concentrator.dict.constants import OperationEnumerate
from concentrator.exceptions import NoValueException
from concentrator.rules import PrivilegeTypeRule
from concentrator.webservice.service import LoadData


class DictProxy(ABC):

    # Настройка для проверки, что отправка справочников через СМЭВ 2 запрещена
    is_load_data_disabled = settings.DISABLE_LOAD_DATA_SMEV2

    @abstractmethod
    def __init__(self):
        self.model = VirtualModel
        self.code = u'Код справочника'
        # self.name = self.model._meta.verbose_name

    @abstractmethod
    def process_obj(self, obj):
        """
        Обработка объекта модели:
        Преобразование в словарь для отправки в концентратор
        :param obj: Объект модели self.model
        :return: tuple

        """
        return ()

    def get_query(self):
        return self.model.objects.all()

    def get_objects_to_pass_list(self):
        objs_to_pass = []
        objs = self.get_query()
        for obj in objs:
            objs_to_pass.append(self.process_obj(obj))
        return objs_to_pass

    @staticmethod
    def check_wsdl_url():
        """Проверка, что указан адрес сервиса."""
        if not settings.SMEV_CONCENTRATOR_WSDL_URL:
            raise ImproperlyConfigured(
                'Can\'t send LoadData - not found SMEV_CONCENTRATOR_WSDL_URL'
            )

    def send_obj(self, obj, operation):
        """
        Отправка на синхронизацию в концентратор одного объекта модели
        :param obj: Объект для передачи в концентратор
        :param operation: Код операции (добавление, изменение, удаление)
                         LoadData.Operations
        :return:
        """
        if self.is_load_data_disabled:
            return

        self.check_wsdl_url()

        LoadData({
            operation: [self.process_obj(obj)],
            'code': self.code,
        }).load_data()

    def send_all(self, operation, size=200):
        u"""
        Отправка на синхронизацию в концентратор всех объектов модели.
        Отправляем  данные частями.
        Размер отправляемой части данных указывается  во входных параметрах.
        :param operation: Код операции (добавление, изменение, удаление)
                          LoadData.Operations
        :param size: размер отправляемого куска данных
        """
        if self.is_load_data_disabled:
            return

        data = self.get_objects_to_pass_list()
        paging = Paginator(data, size)
        for num_page in paging.page_range:
            page = paging.page(num_page)
            data_part = data[page.start_index()-1:page.end_index()]
            LoadData({operation: data_part, 'code': self.code}).load_data()


class GroupAgeSubCathegoryProxy(DictProxy):

    def __init__(self):
        self.model = GroupAgeSubCathegory
        self.code = u'Образование.Заявление.ДОО.ВозрастнаяГруппа'

    def process_obj(self, obj):
        age_from, age_to = obj.code.split('-')
        return (
            obj.id,
            [(u'Название', obj.name),
             (u'От', age_from),
             (u'До', age_to)]
        )


class HealthNeedProxy(DictProxy):
    # Значение по умолчанию для данного справочника
    DEFAULT_VALUE = HealthNeed.NO

    def __init__(self):
        self.model = HealthNeed
        self.code = u'Образование.Заявление.ДОО.СпецификаГрупп'

    def process_obj(self, obj):
        result = (
            obj.id,
            [(u'Название', obj.name)]
        )

        # Добавляем тэг с аттрибутом указывающим использовать
        # данный элемент справочника по умолчанию
        if obj.code == self.DEFAULT_VALUE:
            result[-1].append(
                 (u'ИспользоватьПоУмолчанию', 'true'))

        return result


class PrivilegeProxy(DictProxy):
    NAME_PARAM_MUN = 'privilegeinmo'

    def __init__(self):
        self.model = Privilege
        self.code = u'Образование.Льготы.ДОО.Региональные'

    def get_priviledges_params(self, privileges_query):
        u"""Возвращает Льготы как список нужных их параметров."""
        not_mun_query = privileges_query.exclude(
            type__id=PrivilegeType.MUN
        ).values('id', self.NAME_PARAM_MUN)

        # На каждую муниципальную льготу в мо отдельный блок в запросе
        mun_query = privileges_query.filter(
            type__id=PrivilegeType.MUN,
            privilegeinmo__isnull=False,
        ).values('id', self.NAME_PARAM_MUN)

        return list(not_mun_query) + list(mun_query)

    def get_query(self, operation):
        # основной запрос
        privileges = Privilege.objects

        # для операций Добавление и Изменение
        # добавляется фильтр "Не учитывать в новых заявлениях"
        if operation in (OperationEnumerate.ADD, OperationEnumerate.UPDATE):
            privileges = privileges.filter(cant_add=False)

        return self.get_priviledges_params(privileges)

    def process_obj(self, params):
        obj = Privilege.objects.get(id=params['id'])

        norm_doc_name = ''
        if obj.docs.exists():
            # Да, берется просто первый попавшийся нормативный документ.
            # Никакой дополнительной логики.
            # Не знаю, почему не строка из всех.
            norm_doc = obj.docs.all().select_related('doc')[0]
            norm_doc_name = getattr(getattr(norm_doc, 'doc', None),
                                    'name',
                                    u'Не указано')

        try:
            obj_fields = [
                (u'Название', obj.name),
                (u'Категория', obj.order_type.code),
                (u'ОснованиеДляЛьготы', norm_doc_name),
                (u'ТипЛьготы', PrivilegeTypeRule.get_concetr(obj.type.id))
            ]
        except AttributeError:
            raise NoValueException(
                u'У льготы "%s" не проставлен приоритет или тип' %
                obj.name)

        privilege_type = obj.type_id
        # Региональная льгота
        if privilege_type == PrivilegeType.REG:
            regions = Unit.objects.filter(kind=UnitKind.REGION)
            # Предполагаем, что в системе
            # всегда есть только один регион
            if regions:
                obj_fields.append((u'СубъектУчета', regions[0].ocato))
        elif privilege_type == PrivilegeType.MUN:
            obj.id = '%d%s%d' % (params['id'],
                              DELIMITER_PRIV,
                              params[self.NAME_PARAM_MUN])
            privilege_in_mo = PrivilegeInMo.objects.get(
                id=params[self.NAME_PARAM_MUN])
            obj_fields.append((u'СубъектУчета', privilege_in_mo.mo.ocato))
        else:
            obj_fields.append((u'СубъектУчета',''))

        return (
            obj.id,
            obj_fields
        )

    def get_objects_to_pass_list(self, operation):
        """
        :param operation: Код операции (добавление, изменение, удаление)
        LoadData.Operations
        :return:
        """
        return list(map(self.process_obj, self.get_query(operation)))

    def send_all(self, operation, size=200):
        u"""
        Отправка на синхронизацию в концентратор всех объектов модели.
        Отправляем  данные частями.
        Размер отправляемой части данных указывается  во входных параметрах.
        :param operation: Код операции (добавление, изменение, удаление)
                          LoadData.Operations
        :param size: размер отправляемого куска данных
        """
        if self.is_load_data_disabled:
            return

        data = self.get_objects_to_pass_list(operation)
        paging = Paginator(data, size)
        for num_page in paging.page_range:
            page = paging.page(num_page)
            data_part = data[page.start_index()-1:page.end_index()]
            LoadData({operation: data_part, 'code': self.code}).load_data()

    def send_obj(self, obj, operation):
        if self.is_load_data_disabled:
            return

        self.check_wsdl_url()
        privileges_query = Privilege.objects.filter(id=obj.id)

        LoadData({
            operation: [
                self.process_obj(params)
                for params in self.get_priviledges_params(privileges_query)
            ],
            'code': self.code,
        }).load_data()


class UnitProxy(DictProxy):

    unit_statuses_for_delete = (
        UnitStatus.IN_CAPITAL_REPAIR,
        UnitStatus.RECONSTRUCTION,
        UnitStatus.SUSPENDED,
        UnitStatus.PENDING_OPEN,
        UnitStatus.LIQUIDATED,
        UnitStatus.CLOSED,
        UnitStatus.JOINED_OTHER
    )
    unit_statuses_for_add = settings.STATUS_UNIT_LIST

    def __init__(self):
        self.model = Unit
        self.code = u'Образование.Организации.ДОО.Региональные'

    def get_query(self, operation):
        """
        На добавление и изменение отправляем все ДОО не закрытые,
        и не в статусах прекращение деятельности
        На удаление все ДОО
        :param operation:
        :return:
        """
        # Базовый фильтр: Все ДОО
        query = self.model.objects.filter(kind_id=UnitKind.DOU)
        if operation != OperationEnumerate.DELETE:
            query = query.filter(
                Q(is_not_show_on_poral=False) & Q(
                    status__in=UnitProxy.unit_statuses_for_add))

        # Расширенный фильтр: Только государственные ДОО
        # Действует при включенном параметре SMEV_ONLY_GOV_DOU_OR_EMPTY
        if kinder_settings.SMEV_ONLY_GOV_DOU_OR_EMPTY:
            query = query.filter(
                Q(dou_type__code__in=DouType.GOVERNMENT_TYPES) | Q(
                    dou_type__isnull=True))
        return query

    def get_objects_to_pass_list(self, operation):
        """
        :param operation: Код операции (добавление, изменение, удаление)
        LoadData.Operations
        :return:
        """
        return [self.process_obj(obj) for obj in self.get_query(operation)]

    @staticmethod
    def _get_address(address_full):
        """
        Необходимо по текущему полному адресу
        получить адрес для концентратора, не выполняя запрос на сервер ФИАСА.
        Адрес для концентратора отличается от ФИАСА отсутствием индекса.
        """

        # Если адрес не заполнен или там пустая строка, то отдаем None
        if not address_full:
            return None

        # Полный адрес состоит из строк разделенных ", ".
        address_components = address_full.split(', ')
        first_cmp = address_components[0]
        # Первый компонент ФИАС это индекс. Он нам не нужен.
        if first_cmp.isdigit():
            return ', '.join(address_components[1:])
        else:
            # Если первый компонент не индекс, то оставляем все как есть.
            return address_full

    @staticmethod
    def _get_parent_okato(obj):
        u"""Получает ОКАТО ДОО или ближайшего по иерархии родителя"""
        return obj.ocato or obj.get_ancestors(ascending=True).filter(
            ocato__isnull=False
        ).exclude(
            ocato=u''
        ).values_list('ocato', flat=True).first()

    def process_obj(self, obj):
        try:
            dmu = EmieUnitModel.objects.get(unit=obj)
        except EmieUnitModel.DoesNotExist:
            dmu = None

        fields_list = [
            (u'ПолноеНазвание', obj.full_name),
            (u'КраткоеНазвание', obj.name),
            (u'Адрес', UnitProxy._get_address(obj.address_full)),
            (u'ДатаВвода', obj.commissioning_date),
            (u'РежимРаботы', obj.reception_time),
            (u'КонтактныеТелефоны', obj.telephone),
            (u'КонтактныеEmail', obj.email),
            (u'Характеристики', dmu.additional_info_info if dmu else ''),
            (u'СубъектУчета', UnitProxy._get_parent_okato(obj)),
            (u'ВидОО', obj.type.id if obj.type else '1'),  # 1 - "Детский сад"
            (u'Широта', obj.latitude),
            (u'Долгота', obj.longitude),
        ]

        obj_groups = obj.group_set
        specifics = obj_groups.filter(
            health_need__isnull=False
        ).values_list(
            'health_need__id', flat=True).distinct()
        for sp in specifics:
            fields_list.append((u'СпецификаГрупп', sp))

        age_sub_cats = obj_groups.filter(
            sub_age_cat__isnull=False
        ).values_list(
            'sub_age_cat__id', flat=True).distinct()
        for age_sub_cat in age_sub_cats:
            fields_list.append((u'ВозрастныеГруппы', age_sub_cat))

        return obj.id, fields_list

    def send_all(self, operation, size=200):
        u"""
        Отправка на синхронизацию в концентратор всех объектов модели.
        Отправляем  данные частями.
        Размер отправляемой части данных указывается  во входных параметрах.
        :param operation: Код операции (добавление, изменение, удаление)
                          LoadData.Operations
        :param size: размер отправляемого куска данных
        """
        if self.is_load_data_disabled:
            return

        data = self.get_objects_to_pass_list(operation)
        paging = Paginator(data, size)
        for num_page in paging.page_range:
            page = paging.page(num_page)
            data_part = data[page.start_index()-1:page.end_index()]
            LoadData({operation: data_part, 'code': self.code}).load_data()


class ExcludedUnitProxy(UnitProxy):
    """
    Прокси для ДОО исключенных из работы с концентратором
    """

    def get_query(self, operation=''):
        # Базовый фильтр: Все ДОО с запретом отображения на портале,
        # либо в статусах прекращение деятельности ДОО
        query = self.model.objects.filter(
            kind_id=UnitKind.DOU)

        query_filter = Q(is_not_show_on_poral=True) | Q(
            status__in=UnitProxy.unit_statuses_for_delete)

        # Расширенный фильтр: Все ДОО кроме государственных
        # Действует при включенном параметре SMEV_ONLY_GOV_DOU_OR_EMPTY
        if kinder_settings.SMEV_ONLY_GOV_DOU_OR_EMPTY:
            query_filter = query_filter | (
                Q(dou_type__isnull=False) & ~Q(
                    dou_type__code__in=DouType.GOVERNMENT_TYPES))
        query = query.filter(query_filter)

        return query


class GroupStatisticProxy(DictProxy):
    """
    Самый неординарный прокси.
    Собирает информацию о количестве заявок в организацию
    в разрезе возрастных категорий
    """

    def __init__(self):
        super(GroupStatisticProxy, self).__init__()
        self.code = (
            u'Образование.Организации.ДОО.Региональные.'
            u'Статистика.ВозрастнаяГруппа')

    def process_obj(self, obj):
        pass

    def get_objects_to_pass_list(self):
        objs_to_pass = []
        units = Unit.objects.all()
        in_queue_statuses_codes = DSS.status_queue_full()
        for age_cat in GroupAgeSubCathegory.objects.all():
            try:
                ages = list(map(int, age_cat.code.split('-')))
            except ValueError:
                # В справочнике "Возрастных подкатегорий" может
                # встретиться "лишняя" запись не из фикстуры с дробным
                # значением. Такую запись пропускаем.
                continue

            date_from, date_to = get_date_of_birth_range(
                datetime.date.today(),
                *ages
            )
            declarations = Declaration.objects.filter(
                children__date_of_birth__gte=date_from,
                children__date_of_birth__lte=date_to
            ).select_related('declarationunit')

            for unit in units:
                decl_count = declarations.filter(
                    declarationunit=unit,
                    status__code__in=in_queue_statuses_codes
                ).distinct().count()

                obj = ('%s:%s' % (unit.id, age_cat.id),
                       [(u'КодОО', unit.id),
                        (u'КодГруппы', age_cat.code),
                        (u'КоличествоЗаявлений', decl_count)])
                objs_to_pass.append(obj)
        return objs_to_pass
