import abc
from collections import namedtuple

from django.conf import settings
from educommon.contingent import catalogs

from kinder.core.utils.address import name_from_guid
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationDoc
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration.models import DeclarationUnit
from kinder.core.children.models import Children
from kinder.core.children.models import Delegate
from kinder.core.children.models import DelegateTypeEnumerate


class SnapshotCreatorBase(metaclass=abc.ABCMeta):
    """
    Базовый класс для создания снимков объектов модели
    """
    SnapshotRow = namedtuple('SnapshotRow', [
        'field',
        'field_name',
        'value',
        'representation'
    ])

    # Поля снимка
    fields = ()

    # Наименования полей снимка
    field_names = {}

    def __init__(self, model, obj_id):
        self.model = model
        self.obj_id = obj_id

        # Получаем название полей из модели
        self.model_fields = dict([(f.name, f) for f in self.model._meta.fields])
        self.model_name = self.model._meta.verbose_name.capitalize()
    
    def get_field_name(self, field, obj):
        """
        Возвращает название поля, приоритет из field_names, 
        если там нет, то из self.model_fields
        """
        name = self.field_names.get(field)
        if not name:
            field_obj = self.model_fields.get(field)
            if field_obj:
                name = field_obj.verbose_name or field.name
    
        if name is None:
            return self.model_name

        return f'{self.model_name} - {name}'
    
    def get_field_representation(self, field, obj, value):
        """
        Возвращает значение поля для вывода пользователю

        По умолчанию возвращает то же значение, 
        но если есть метод get_FIELD_repr то вызовет его
        """
        repr_fn = getattr(self, f'get_{field}_repr', None)
        if repr_fn is None:
            return value
        
        return repr_fn(field, obj, value)
    
    def get_value(self, field, obj):
        """
        Возвращает значение из объекта по названию поля

        Процесс получения должен быть определён в методе get_FIELD_value
        """
        try:
            value_fn = getattr(self, f'get_{field}_value')
            return value_fn(field, obj)
        except AttributeError:
            return obj.get(field)
    
    def get_empty_snapshot(self):
        """
        "Пустой" снимок для None
        """
        snapshot = []

        for field in self.fields:
            row = self.SnapshotRow(
                field,
                self.get_field_name(field, None),
                None,
                '-'
            )
            snapshot.append(row)
        
        return snapshot
    
    @abc.abstractmethod
    def get_object(self):
        """
        Возвращает объект модели
        """
        raise NotImplementedError

    def get_snapshot(self):
        """
        Возвращает снимок для объекта модели
        """
        db_values = self.get_object()

        if db_values is None:
            return self.get_empty_snapshot()

        snapshot = []

        for field in self.fields:
            value = self.get_value(field, db_values)
            row = self.SnapshotRow(
                field,
                self.get_field_name(field, db_values),
                value,
                self.get_field_representation(field, db_values, value)
            )
            snapshot.append(row)
        
        return snapshot

    @classmethod
    def compare_values(cls, left, right):
        """
        Сравниваем значения 2 строк снимка
        """
        return left.value == right.value

    @classmethod
    def compare_snapshots(cls, left, right):
        """
        Проводит сравнение 2 снимков и возвращает разницу
        """
        diff = []
        for row_left, row_right in zip(left, right):
            if not cls.compare_values(row_left, row_right):
                field_name = (
                    row_right.field_name 
                    if row_right.value else row_left.field_name
                )
                diff.append({
                    'field': field_name,
                    'old_value': row_left.representation,
                    'new_value': row_right.representation
                })

        return diff

    def updated(self, snapshot):
        """
        Получить разницу для обновления объекта модели передав старый снимок
        """
        current_state = self.get_snapshot()
        return self.compare_snapshots(snapshot, current_state)
    
    def created(self):
        """
        Получить разницу для созданного объекта модели
        """
        return self.updated(self.get_empty_snapshot())

    def deleted(self, snapshot):
        """
        Получить разницу для удалённого объекта модели передав старый снимок
        """
        return self.compare_snapshots(snapshot, self.get_empty_snapshot())


class SnapshotCreator(SnapshotCreatorBase):
    """
    Основной класс для получения снимков
    """

    # Будет передано в values при получении объекта
    values = ()

    # Различные виды полей, которые часто встречаются
    dict_fields = ()
    date_fields = ()
    bool_fields = ()
    addr_fields = ()
    choice_fields = {}

    def get_object(self):
        return self.model.objects.filter(
            pk=self.obj_id).values(*self.values).first()
    
    @classmethod
    def compare_values(cls, left, right):
        left_value = left.value
        right_value = right.value

        # Пустые строки считаем None, 
        # т.к. для пользователя это одно и то же
        if isinstance(left_value, str) and not left_value:
            left_value = None
        
        if isinstance(right_value, str) and not right_value:
            right_value = None

        return left_value == right_value

    def _get_dict_repr(self, field, obj):
        """
        Получить репрезентацию объектов справочников
        """
        return obj[f'{field}__name'] or '-'
    
    def _get_date_repr(self, value):
        """
        Получить репрезентацию дат
        """
        return value.strftime(settings.DATE_FORMAT)
    
    def _get_bool_repr(self, value):
        """
        Получить репрезентацию логических значений
        """
        return 'Да' if value else 'Нет'
    
    def _get_address_repr(self, value):
        """
        Получить репрезентацию полей адреса
        """
        try:
            return name_from_guid(value, timeout=5)
        except Exception:
            return value

    def _get_choices_repr(self, field, value):
        """
        Получить репрезентацию полей выбора
        """
        choices = self.choice_fields[field]
        return choices[value]
    
    def get_field_representation(self, field, obj, value):
        if value is None:
            return '-'
        
        if isinstance(value, str) and not value:
            return '-'

        if field in self.dict_fields:
            return self._get_dict_repr(field, obj)
        
        if field in self.date_fields:
            return self._get_date_repr(value)
        
        if field in self.bool_fields:
            return self._get_bool_repr(value)
        
        if field in self.addr_fields:
            return self._get_address_repr(value)
        
        if field in self.choice_fields:
            return self._get_choices_repr(field, value)

        return super().get_field_representation(field, obj, value)


class DeclarationSnapshotCreator(SnapshotCreator):
    """
    Создатель снимков для заявок
    """
    fields = (
        'desired_date',
        'work_type',
        'spec',
        'consent_full_time_group',
        'offer_other',
        'consent_dev_group',
        'consent_care_group',
        'desired_group_type',
    )

    values = (
        'desired_date',
        'work_type',
        'work_type__name',
        'spec',
        'spec__name',
        'consent_full_time_group',
        'offer_other',
        'consent_dev_group',
        'consent_care_group',
        'desired_group_type',
        'desired_group_type__name',
    )

    dict_fields = (
        'work_type',
        'spec',
        'desired_group_type',
    )

    date_fields = (
        'desired_date',
    )

    bool_fields = (
        'consent_full_time_group',
        'offer_other',
        'consent_dev_group',
        'consent_care_group',
    )

    def __init__(self, obj_id):
        super().__init__(Declaration, obj_id)


class ChildSnapshotCreator(SnapshotCreator):
    """
    Создатель снимков для ребёнка
    """
    fields = (
        'firstname',
        'surname',
        'patronymic',
        'date_of_birth',
        'address_full',
        'address_place',
        'address_street',
        'address_house',
        'address_house_guid',
        'address_corps',
        'address_flat',
        'health_need_special_support',
        'health_need_confirmation',
        'health_series',
        'health_number',
        'health_need_start_date',
        'health_issued_by',
        'health_need_expiration_date',
        'dul_series',
        'dul_number',
        'dul_date',
        'zags_act_number',
        'zags_act_place',
        'zags_act_date',
        'health_need',
    )

    values = (
        'firstname',
        'surname',
        'patronymic',
        'date_of_birth',
        'address_full',
        'address_place',
        'address_street',
        'address_house',
        'address_house_guid',
        'address_corps',
        'address_flat',
        'health_need_special_support',
        'health_need_confirmation',
        'health_need_confirmation__name',
        'health_series',
        'health_number',
        'health_need_start_date',
        'health_issued_by',
        'health_need_expiration_date',
        'dul_series',
        'dul_number',
        'dul_date',
        'zags_act_number',
        'zags_act_place',
        'zags_act_date',
        'health_need',
        'health_need__name',
    )

    dict_fields = (
        'health_need_confirmation',
        'health_need'
    )

    date_fields = (
        'date_of_birth',
        'health_need_start_date',
        'health_need_expiration_date',
        'dul_date',
        'zags_act_date',
    )

    bool_fields = (
        'health_need_special_support',
    )

    addr_fields = (
        'address_place',
        'address_street',
    )

    def __init__(self, obj_id):
        super().__init__(Children, obj_id)


class DelegateSnapshotCreator(SnapshotCreator):
    """
    Создатель снимков для представителя
    """
    fields = (
        'firstname',
        'surname',
        'patronymic',
        'dul_type',
        'dul_series',
        'dul_number',
        'dul_issued_by',
        'dul_date',
        'email',
        'phones',
        'type',
        'delegatecontingent__doc_type',
        'delegatecontingent__series',
        'delegatecontingent__number',
        'delegatecontingent__date_issue',
        'delegatecontingent__issued_by',
    )

    values = (
        'firstname',
        'surname',
        'patronymic',
        'dul_type',
        'dul_type__name',
        'dul_series',
        'dul_number',
        'dul_issued_by',
        'dul_date',
        'email',
        'phones',
        'type',
        'delegatecontingent__doc_type',
        'delegatecontingent__series',
        'delegatecontingent__number',
        'delegatecontingent__date_issue',
        'delegatecontingent__issued_by',
    )

    dict_fields = (
        'dul_type',
    )

    date_fields = (
        'dul_date',
        'delegatecontingent__date_issue'
    )

    choice_fields = {
        'delegatecontingent__doc_type': catalogs.DocumentConfirmingTypes.values,
        'type': DelegateTypeEnumerate.values
    }

    field_names = {
        'delegatecontingent__doc_type': 'Тип документа, подтверждающего права',
        'delegatecontingent__series': 'Серия',
        'delegatecontingent__number': 'Номер',
        'delegatecontingent__date_issue': 'Дата выдачи',
        'delegatecontingent__issued_by': 'Кем выдан',
    }

    def __init__(self, obj_id):
        super().__init__(Delegate, obj_id)


class DeclarationUnitSnapshotCreator(SnapshotCreator):
    """
    Создатель снимков для желаемых организаций
    """
    fields = (
        'unit',
        'ord',
        'sibling'
    )

    values = (
        'unit',
        'unit__name',
        'ord',
        'sibling',
        'sibling__fullname',
    )

    dict_fields = (
        'unit',
    )

    def __init__(self, obj_id):
        super().__init__(DeclarationUnit, obj_id)
    
    def get_field_name(self, field, obj):
        field_name = super().get_field_name(field, obj)

        if obj and field in ('ord', 'sibling'):
            field_name = f'{field_name} ({obj["unit__name"]})'

        return field_name

    def get_sibling_repr(self, field, obj, value):
        return obj['sibling__fullname'] or '-'


class DeclarationPrivilegeSnapshotCreator(SnapshotCreator):
    """
    Создатель снимков для льгот в заявке
    """
    fields = (
        'privilege',
    )

    values = (
        'privilege',
        'privilege__name',
        'doc_issued_by',
        'doc_date',
        '_privilege_end_date',
    )

    field_names = {
        'privilege': 'Льгота'
    }

    def __init__(self, obj_id):
        super().__init__(DeclarationPrivilege, obj_id)
    
    def get_privilege_value(self, field, obj):
        return (
            obj['privilege'],
            obj['doc_issued_by'],
            obj['doc_date'],
            obj['_privilege_end_date'],
        )
    
    def get_privilege_repr(self, field, obj, value):
        doc_date = obj['doc_date']
        priv_date = obj['_privilege_end_date']

        values = [
            obj['privilege__name'],
            obj['doc_issued_by'] or '-',
            self._get_date_repr(doc_date) if doc_date else '-',
            self._get_date_repr(priv_date) if priv_date else '-',
        ]

        return f'{", ".join(values)}'


class DeclarationDocsSnapshotCreator(SnapshotCreatorBase):
    """
    Создатель снимков для списка документов заявки
    """
    fields = (
        'declaration_docs',
    )

    field_names = {
        'declaration_docs': 'Список документов'
    }

    def __init__(self, obj_id):
        super().__init__(Declaration, obj_id)

    def get_object(self):
        return {
            'declaration_docs': set(
                DeclarationDoc.objects.filter(
                    declaration_id=self.obj_id).values_list('name', flat=True)
            )
        }

    def get_declaration_docs_repr(self, field, obj, value):
        if not value:
            return '-'
        return ', '.join(sorted(value))
    
    def created(self):
        raise NotImplementedError
    
    def deleted(self, snapshot):
        raise NotImplementedError


_snapshot_creator_map = {
    Declaration: DeclarationSnapshotCreator,
    Children: ChildSnapshotCreator,
    Delegate: DelegateSnapshotCreator,
    DeclarationUnit: DeclarationUnitSnapshotCreator,
    DeclarationDoc: DeclarationDocsSnapshotCreator,
    DeclarationPrivilege: DeclarationPrivilegeSnapshotCreator,
}


def get_snapshot_creator_for_model(model):
    """
    Получить создатель снимка для модели
    """
    return _snapshot_creator_map[model]
