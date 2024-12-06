from collections import OrderedDict
from collections import namedtuple

from django.db.models import Q
from m3.plugins import ExtensionManager

from kinder.core.dict.models import UnitKind
from kinder.core.unit.constants import INFINITE_MAX_DESIRED_DOU
from kinder.core.unit.constants import ZERO_MAX_DESIRED_DOU
from kinder.core.unit.models import Unit
from kinder.core.unit.models import UnitStatus

from .enums import DataTypesEnum as DT
from .settings import UPDATE_CLASSIFIER_REGOKATO

# namedtuple для хранения информации о поле для выгрузки
FieldInfo = namedtuple('FieldInfo', ['type', 'length', 'required'])


class ClassifierBase:
    """Базовый класс справочников для передачи в ЕСНСИ (СМЭВ 3)."""

    model = None

    # имя и тип атрибута записи для ключевого поля классификатора
    pk_attr_name = None
    pk_attr_type = None

    # Словарь, где ключ - название поля, значение - экземляр FieldInfo.
    fields_info = {}

    def __init__(self):
        assert self.model

        self._filename = 'update'
        self._storage_sections = (
            'update_esnsi',
            self.get_service_code(),
        )

    def get_pk_val(self, obj):
        return obj.id

    def data_queryset(self):
        return self.model.objects.all()

    def get_obj(self, row):
        """Возвращает объект элемента выборки"""

        # если в исходном запросе указан values, то выдает объект с
        # отображенными в его атрибуты ключами словаря,
        # иначе отдается исходный элемент выборки
        res = row
        if isinstance(row, dict):
            res = namedtuple('row_val', row)(**row)
        return res

    def queryset_filter(self):
        """Возвращает актуальный QuerySet выборки данных для выгрузки."""
        return Q()

    @classmethod
    def get_service_code(cls):
        """Получить имя классификатора."""

        from concentrator.smev3_v321.models import ESNSIClassifier

        return ESNSIClassifier.objects.get(classifier_class=cls.__name__).code

    @classmethod
    def get_data(cls, obj):
        """Возвращает данные для запроса и выгрузки данных.

        :param obj: инстанс модели
        :type obj: model

        :return: Возвращает данные
        :rtype: dict
        """
        return {}
    
    @classmethod
    def get_fields_info(cls):
        """
        Передаваемые поля
        """
        fields_info = {**cls.fields_info}
        ExtensionManager().execute(
            'concentrator.smev3_v4.extensions.extend_esnsi_classifier_fields',
            cls, fields_info
        )

        return fields_info

    @classmethod
    def _prepare_text_attributes_values(
            cls, attributes_dict: dict) -> dict:
        """
        Подготоваливает текстовые значения словаря с атрибутами

        Для текстовых полей значение по умолчанию устанавливается равной пустой
        строке, если значения нет, и строки укорачиваются по длине атрибутов.

        :param attributes_dict: Словарь с атрибутами и их значениями

        :return: Новый словарь с атрибутами и их значениями после обработки
        """
        # Атрибуты должны передаваться в строго определенном порядке
        # (соответствующему fields_info в классах ниже)
        attrs = OrderedDict()
        fields_info = cls.get_fields_info()
        for attr_name, value in attributes_dict.items():
            field_info = fields_info[attr_name]
            if field_info.type in (DT.STRING, DT.TEXT):
                attrs[attr_name] = (value or '')[:field_info.length]
            else:
                attrs[attr_name] = value

        return attrs

    def is_data_valid(self, data_dict: dict) -> bool:
        """Проверка сформированного словаря с данными на валидность

        :param data_dict: Сформированный словарь с данными для объекта

        :return: Валидность сформированных данных
        """
        return True


class UnitClassifier(ClassifierBase):
    """Организации (детсады)."""

    model = Unit
    fields_info = {
        'CODE': FieldInfo(type=DT.STRING, length=50, required=True),
        'TITLE': FieldInfo(type=DT.STRING, length=255, required=True),
        'REGOKATO': FieldInfo(type=DT.STRING, length=10, required=True),
        'ADDRESS': FieldInfo(type=DT.STRING, length=255, required=True),
        'FIAS': FieldInfo(type=DT.STRING, length=50, required=True),
        'PHONE': FieldInfo(type=DT.STRING, length=50, required=False),
        'EMAIL': FieldInfo(type=DT.STRING, length=50, required=False),
        'SCHEDULE': FieldInfo(type=DT.STRING, length=100, required=False),
        'OKTMO': FieldInfo(type=DT.STRING, length=8, required=True),
        'WEBSITE': FieldInfo(type=DT.STRING, length=255, required=False),
    }

    def queryset_filter(self):
        """Возвращает фильтр для QuerySet выборки данных для выгрузки.

        Условия:
        - Тип: ДОО
        - НЕ проставлен чек бокс "Не показывать на портале"
        - Статус НЕ один из ("Закрыто", "Ликвидировано",
            "Присоединена к другой организации")
        - У ДОО заполнены все поля, обязательные согласно описанию в конфлюенс
            (название, адрес, код ФИАС).

        Важно: заполнение ОКТМО проверяется отдельно
        """
        return Q(
            kind=UnitKind.DOU,
            is_not_show_on_poral=False,
        ) & ~Q(
            status__in=UnitStatus.ALL_CLOSED_STATUS,
        ) & Q(
            Q(name__isnull=False) & ~Q(name__exact='') &
            Q(address_full__isnull=False) & ~Q(address_full__exact='') &
            Q(address_place__isnull=False) & ~Q(address_place__exact='')
        )

    @classmethod
    def get_data(cls, obj):
        """"""
        data = {
            'CODE': f'{obj.id}',
            'TITLE': obj.name,
            'REGOKATO': UPDATE_CLASSIFIER_REGOKATO,
            'ADDRESS': obj.address_full,
            'FIAS': obj.address_place,
            'PHONE': obj.telephone,
            'EMAIL': obj.email,
            'SCHEDULE': obj.reception_time,
            'OKTMO': obj.get_mo_octmo() or obj.octmo,
            'WEBSITE': obj.site,
        }
        new_data = cls._prepare_text_attributes_values(data)
        return new_data

    def is_data_valid(self, data_dict: dict) -> bool:
        # ОКТМО не должно быть пустым
        if not data_dict['OKTMO']:
            return False

        return True


class MaxDooClassifier(ClassifierBase):
    """Максимальное количество детсадов, которое может выбрать заявитель."""

    # Пуск - Организации - МО - поле "Максимальное количество желаемых ДОО"
    model = Unit
    fields_info = {
        'CODE': FieldInfo(type=DT.STRING, length=8, required=True),
        'TITLE': FieldInfo(type=DT.STRING, length=255, required=False),
        'REGOKATO': FieldInfo(type=DT.STRING, length=10, required=True),
        'EDUORGMAX': FieldInfo(type=DT.INTEGER, length=None, required=True),
    }
    # Максимально допустимое число для EDUORGMAX
    max_edu_org_max = 50

    def queryset_filter(self):
        return Q(kind=UnitKind.MO) & ~Q(max_desired_dou=ZERO_MAX_DESIRED_DOU)

    @classmethod
    def get_max_desired_dou(cls, obj):
        """Получение максимального количества ДОО с доп.обработкой."""
        # Ограничиваем максимальное количество ДОО определенным числом
        if (obj.max_desired_dou == INFINITE_MAX_DESIRED_DOU or
                obj.max_desired_dou > cls.max_edu_org_max):
            return cls.max_edu_org_max

        return obj.max_desired_dou

    @classmethod
    def get_data(cls, obj):
        """"""
        data = {
            'CODE': obj.octmo,
            'TITLE': obj.name,
            'REGOKATO': UPDATE_CLASSIFIER_REGOKATO,
            'EDUORGMAX': cls.get_max_desired_dou(obj)
        }
        ExtensionManager().execute(
            'concentrator.smev3_v4.extensions.extend_esnsi_classifier_data',
            cls, obj, data
        )
        new_data = cls._prepare_text_attributes_values(data)
        return new_data


class EduControlUnitClassifier(ClassifierBase):
    """Органы управления образованием."""

    model = Unit
    fields_info = {
        'OKTMO': FieldInfo(type=DT.STRING, length=50, required=True),
        'EDU_DEPARTMENT_ADDRESS': FieldInfo(type=DT.STRING, length=500, required=True),
        'EDU_DEPARTMENT_NAME': FieldInfo(type=DT.STRING, length=500, required=True),
        'EDU_DEPARTMENT_PHONE': FieldInfo(type=DT.STRING, length=50, required=True),
        'EDU_DEPARTMENT_WEBSITE': FieldInfo(type=DT.STRING, length=2000, required=False),
        'EDU_DEPARTMENT_EMAIL': FieldInfo(type=DT.STRING, length=250, required=True),
    }

    def queryset_filter(self):
        q = Q(
            kind=UnitKind.MO,
            octmo__isnull=False,
            address_full__isnull=False,
            telephone__isnull=False,
            email__isnull=False
        )

        return q

    @classmethod
    def get_data(cls, obj):
        """"""
        data = {
            'OKTMO': obj.octmo,
            'EDU_DEPARTMENT_ADDRESS': obj.address_full,
            'EDU_DEPARTMENT_NAME': obj.name,
            'EDU_DEPARTMENT_PHONE': obj.telephone,
            'EDU_DEPARTMENT_WEBSITE': obj.site,
            'EDU_DEPARTMENT_EMAIL': obj.email,
        }
        new_data = cls._prepare_text_attributes_values(data)
        return new_data
