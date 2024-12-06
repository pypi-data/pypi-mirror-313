import datetime

from django.db import models as fields_types
from educommon.django.db import fields as educommon_fields

from concentrator.webservice.helpers import get_delegate
from concentrator.webservice.helpers import get_privilege_comment


BOOLEAN_FIELD_VALUE_MAP = {
    True: 'Да',
    False: 'Нет'
}

FIELD_TYPES_MAP = {
    fields_types.DateField: lambda v, c, f: datetime.datetime.strptime(
        v, '%Y-%m-%d %H:%M:%S').date(),
    educommon_fields.RangedDateField: lambda v, c, f: datetime.datetime.strptime(
        v, '%Y-%m-%d %H:%M:%S').date(),
    educommon_fields.BirthDateField: (
        lambda v, c, f:
        datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S').date()),
    fields_types.DateTimeField: lambda v, c, f: datetime.datetime.strptime(
        v, '%Y-%m-%d %H:%M:%S'),
    fields_types.ForeignKey: lambda v, c, f: foreign_key_converter(v, f),
}

RESULT_TYPES_MAP = {
    fields_types.DateField: lambda v, c, f: v.strftime('%d.%m.%Y'),
    educommon_fields.RangedDateField: lambda v, c, f: v.strftime('%d.%m.%Y'),
    educommon_fields.BirthDateField: lambda v, c, f: v.strftime('%d.%m.%Y'),
    fields_types.DateTimeField: lambda v, c, f: v.strftime('%d.%m.%Y %H:%M:%S')
}

DISPLAY_TYPES_MAP = {
    fields_types.DateField: lambda v, c, f: datetime.datetime.strptime(
        v, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y'),
    educommon_fields.RangedDateField: lambda v, c, f: datetime.datetime.strptime(
        v, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y'),
    educommon_fields.BirthDateField: (
        lambda v, c, f:
        datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y')),
    fields_types.DateTimeField: lambda v, c, f: datetime.datetime.strptime(
        v, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M:%S'),
    fields_types.ForeignKey: lambda v, c, f: foreign_key_converter_display(
        v, f),
    fields_types.SmallIntegerField: lambda v, c, f: dict(
        f.choices).get(v) or v,
    fields_types.BooleanField: lambda v, c, f: BOOLEAN_FIELD_VALUE_MAP.get(v),
}


class DisplayChangesMap:
    """Функции получения изменений из ChangeDeclaration по имени модели."""

    _models_map = None

    def __init__(self):
        # 'стандартные' функции
        self._models_map = {
            'Declaration': self.declaration,
            'Delegate': self.delegate,
            'Children': self.children,
            'DeclarationUnit': self.declarationunit,
            'DeclarationPrivilege': self.declarationprivilege,
            'PrivilegeComment': self.privilegecomment,
        }

    def get(self, model_name):
        """Функция отображения изменений по имени модели."""
        return self._models_map.get(model_name)

    def set(self, model_name, func):
        """Расширение функций отображения изменений (плагинами)."""
        self._models_map[model_name] = func

    @staticmethod
    def declaration(change):
        return change.declaration

    @staticmethod
    def children(change):
        return change.declaration.children

    @staticmethod
    def delegate(change):
        return get_delegate(change.declaration)

    @staticmethod
    def declarationunit(change):
        return change.declaration.declarationunit_set

    @staticmethod
    def declarationprivilege(change):
        return change.declaration.declarationprivilege_set

    @staticmethod
    def privilegecomment(change):
        return get_privilege_comment(change.declaration)


display_changes_map = DisplayChangesMap()


def foreign_key_converter(pk, field):
    """
    Пытаемся найти в Бд по ключу связь и получить name из связааной модели
    :param pk: id из внешней модели
    :param field: нистанс поля модели
    :return:

    """

    related_model = field.remote_field.model

    try:
        obj = related_model.objects.get(id=pk)
        return obj
    except related_model.DoesNotExist:
        return None


def foreign_key_converter_display(pk, field):
    """
    :param pk: id из внешней модели
    :param field: нистанс поля модели
    :return:

    """

    try:
        fk = foreign_key_converter(pk, field)
        if fk:
            return fk.display()
        else:
            return ""
    except field.remote_field.model.DoesNotExist:
        return None
