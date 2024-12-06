from django.db import models as fields_types
from educommon.django.db import fields as educommon_fields
from m3.plugins import ExtensionManager

from kinder.core.audit_log_kndg.helpers import get_field
from kinder.core.declaration.enum import DeclarationTypeInteractionEnum as DTIE
from kinder.core.helpers import recursive_getattr


def format_change(model, field_name):
    """Возвращает строку вида : "Ребенок: Фамилия".

    :param model: verbose name модели
    :param field_name: verbose name поля модели

    """
    return f'{model}: {field_name}'


def format_changes(model, field_list):
    """
    Возвращает строку вида : "Ребенок: Фамилия, Имя"
    :param model: verbose name модели
    :param field_list: список verbose name полей модели
    :return:
    :rtype: str

    """

    return format_change(model, ', '.join(map(str, field_list)))


def convert_value(types_map, data, name_field, value):
    """
    :param types_map: функция приведения данных к нужному формату
    :param data: инстанс модели из хранилища
    :param name_field: строковое наименование поля
    :param value: значение
    :return:

    """

    # многосложное ли поле?
    if '.' in name_field:
        # если поле находится не в текущей модели, а нужно проваливаться
        # по FKey'ам, то сначала получим инстанс последней модели(data)
        # и уже у нее определим инстанс поля(field_instance)
        name_field = name_field.replace('.', '__')
        path_to_data, name_field = name_field.rsplit('__', 1)
        data = recursive_getattr(data, path_to_data)

    field_instance = get_field(data, name_field)
    field_type = type(field_instance)

    type_converter = types_map.get(field_type, lambda v, c, f: v)

    date_field_types = (
        fields_types.DateField, fields_types.DateTimeField,
        educommon_fields.RangedDateField, educommon_fields.BirthDateField)
    if field_type in date_field_types and not value:
        return None

    return type_converter(value, field_type, field_instance)


def get_storage_helper(declaration):
    """Возвращает класс для отслеживания изменений.

    :param declaration: Заявление
    :type declaration: Declaration
    :rtype: Optional[Union[StorageHelper, Smev3StorageHelper]]
    """

    if (
            declaration.type_interaction is not None
            and declaration.type_interaction == DTIE.SMEV_3
    ):
        return ExtensionManager().execute(
            'concentrator.smev3_v321.application_request.extensions.'
            'get_storage_helper')

    from concentrator.change import StorageHelper

    return StorageHelper

